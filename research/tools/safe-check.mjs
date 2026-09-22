#!/usr/bin/env node
// safe-check.mjs — replicate the Safe "evm-checker" on-chain check for lead-gen.
//
// What it does, per chain, given an RPC URL:
//   1. eth_chainId sanity + latest block height.
//   2. eth_getCode on every canonical Safe contract address (singletons, L2
//      singletons, proxy factories) for versions 1.3.0 / 1.4.1 / 1.5.0, using
//      the AUTHORITATIVE addresses from @safe-global/safe-deployments — the same
//      source Safe's own tooling uses. YES = deployed, NO = absent.
//   3. eth_getLogs for ProxyCreation events on each deployed proxy factory,
//      scanned in chunks (to respect node eth_getLogs range caps), to count how
//      many Safes were actually created.
//   4. Emits a JSON blob + ready-to-paste cells matching the DPL/Caldera columns
//      "Safe state on chain" and "Safes created".
//
// This is exactly the deterministic work the evm-checker web UI performs; running
// it as a script lets us batch every lead and drop the output straight into the sheet.
//
// USAGE:
//   node safe-check.mjs --rpc https://rpc.example.xyz [--name "Chain"] [--chunk 100000] [--no-logs]
//   node safe-check.mjs --chainlist ./rpcs.json --chainId 61900        # resolve RPC from chainlist
//   node safe-check.mjs --batch ./leads.json --chainlist ./rpcs.json   # [{name, chainId?, rpcUrl?}, ...]
//
// For each chain it tries, in order: the rpcUrl you gave, then every https RPC
// chainlist lists for that chainId, until one answers — so one dead/rate-limited
// endpoint no longer sinks the chain. A failure on one chain never aborts the batch.
//
// NOTE: needs outbound access to the target RPC (and to chainlist if --chainlist
// is a URL). Run it where the network is open. npm deps install fine anywhere.
//
// Dep: npm install @safe-global/safe-deployments

import fs from "node:fs";
import {
  getSafeSingletonDeployment,
  getSafeL2SingletonDeployment,
  getProxyFactoryDeployment,
} from "@safe-global/safe-deployments";

const VERSIONS = ["1.3.0", "1.4.1", "1.5.0"];
// topic0 of ProxyCreation(address,address) — identical hash across 1.3.0/1.4.1/1.5.0
// (the 1.4.1+ factory only indexes `proxy`, which changes where it sits in `topics`,
// not the signature hash).
const PROXY_CREATION_TOPIC0 =
  "0x4f51faf6c4561ff95f067657e43439f0f856d97c04d9ec9070a6199ad418e235";

function args() {
  const a = process.argv.slice(2);
  const o = { chunk: 100000, logs: true };
  for (let i = 0; i < a.length; i++) {
    const k = a[i];
    if (k === "--rpc") o.rpc = a[++i];
    else if (k === "--name") o.name = a[++i];
    else if (k === "--chainId") o.chainId = Number(a[++i]);
    else if (k === "--chainlist") o.chainlist = a[++i];
    else if (k === "--batch") o.batch = a[++i];
    else if (k === "--chunk") o.chunk = Number(a[++i]);
    else if (k === "--no-logs") o.logs = false;
  }
  return o;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// JSON-RPC call with a per-request timeout + retry/backoff on rate-limit (429)
// and transient 5xx. The timeout (AbortController) is essential: a hung RPC that
// never responds would otherwise stall the whole batch forever.
async function rpc(url, method, params = [], { retries = 3, timeoutMs = 20000 } = {}) {
  let lastErr;
  for (let attempt = 0; attempt <= retries; attempt++) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
        signal: ctrl.signal,
      });
      if (res.status === 429 || (res.status >= 500 && res.status < 600)) {
        lastErr = new Error(`HTTP ${res.status} from RPC`);
        clearTimeout(timer);
        await sleep(600 * (attempt + 1)); // 0.6s, 1.2s, 1.8s ...
        continue;
      }
      if (!res.ok) throw new Error(`HTTP ${res.status} from RPC`);
      const j = await res.json();
      if (j.error) throw new Error(`${method}: ${j.error.message || JSON.stringify(j.error)}`);
      return j.result;
    } catch (e) {
      lastErr = e.name === "AbortError" ? new Error(`timeout after ${timeoutMs}ms`) : e;
      if (attempt < retries) await sleep(600 * (attempt + 1));
    } finally {
      clearTimeout(timer);
    }
  }
  throw lastErr;
}

// Authoritative address set for a version: the canonical defaultAddress plus any
// network-specific address (e.g. the eip155 variant) safe-deployments lists.
function addressesFor(version, chainId) {
  const out = [];
  const add = (label, dep) => {
    if (!dep) return;
    const set = new Set();
    if (dep.defaultAddress) set.add(dep.defaultAddress);
    const forChain = (dep.networkAddresses || {})[String(chainId)];
    if (Array.isArray(forChain)) forChain.forEach((x) => set.add(x));
    else if (forChain) set.add(forChain);
    for (const addr of set) out.push({ label: `${label} ${version}`, address: addr });
  };
  add("Safe singleton", getSafeSingletonDeployment({ version }));
  add("SafeL2 singleton", getSafeL2SingletonDeployment({ version }));
  add("Proxy factory", getProxyFactoryDeployment({ version }));
  return out;
}

async function checkCode(url, chainId) {
  const results = [];
  for (const version of VERSIONS) {
    for (const { label, address } of addressesFor(version, chainId)) {
      let deployed = null;
      try {
        const code = await rpc(url, "eth_getCode", [address, "latest"]);
        deployed = code && code !== "0x" && code !== "0x0";
      } catch (e) {
        deployed = `ERR:${e.message}`;
      }
      results.push({ label, address, deployed });
    }
  }
  return results;
}

async function countSafes(url, factories, latest, chunk) {
  const proxies = new Set();
  let firstBlock = null;
  let lastBlock = null;
  let scanErrors = 0;
  for (const f of factories) {
    for (let from = 0; from <= latest; from += chunk) {
      const to = Math.min(from + chunk - 1, latest);
      let logs;
      try {
        logs = await rpc(url, "eth_getLogs", [
          {
            address: f.address,
            topics: [PROXY_CREATION_TOPIC0],
            fromBlock: "0x" + from.toString(16),
            toBlock: "0x" + to.toString(16),
          },
        ]);
      } catch (e) {
        scanErrors++;
        continue; // node may cap range harder than `chunk`; note and move on
      }
      for (const log of logs) {
        if (log.topics && log.topics[1]) proxies.add("0x" + log.topics[1].slice(26));
        else if (log.data && log.data.length >= 66) proxies.add("0x" + log.data.slice(26, 66));
        const bn = parseInt(log.blockNumber, 16);
        firstBlock = firstBlock === null ? bn : Math.min(firstBlock, bn);
        lastBlock = lastBlock === null ? bn : Math.max(lastBlock, bn);
      }
    }
  }
  return { count: proxies.size, firstBlock, lastBlock, scanErrors };
}

let CHAINLIST = null;
function loadChainlist(pathOrUrl) {
  if (CHAINLIST || !pathOrUrl) return CHAINLIST;
  if (/^https?:\/\//.test(pathOrUrl)) return null; // handled async in getCandidates
  CHAINLIST = JSON.parse(fs.readFileSync(pathOrUrl, "utf8"));
  return CHAINLIST;
}

// Ordered, de-duplicated list of RPC URLs to try for a job.
async function rpcCandidates(job, o) {
  const list = [];
  const push = (u) => { if (u && !list.includes(u)) list.push(u); };
  push(o.rpc);                 // --rpc flag (single mode)
  push(job.rpcUrl);            // rpcUrl from leads.json (preferred for the lead)
  push(job.rpc);
  const chainId = job.chainId ?? o.chainId;
  const src = o.chainlist ?? job.chainlist;
  if (src && chainId != null) {
    let data = loadChainlist(src);
    if (!data && /^https?:\/\//.test(src)) data = await (await fetch(src)).json();
    const entry = (data || []).find((c) => c.chainId === chainId);
    if (entry) {
      for (const r of entry.rpc || []) {
        const u = typeof r === "string" ? r : r.url;
        if (u && u.startsWith("https") && !u.includes("${")) push(u);
      }
    }
  }
  return list;
}

async function run(job, o) {
  const out = { name: job.name || "(unnamed)" };
  const candidates = await rpcCandidates(job, o);
  if (!candidates.length) {
    out.error = "no RPC to try (not in chainlist and no rpcUrl given) — likely pre-mainnet/testnet; add an rpcUrl in leads.json";
    return out;
  }
  // Try each candidate until one answers eth_chainId.
  let url, chainId, latestBlock, lastErr;
  for (const cand of candidates) {
    try {
      chainId = parseInt(await rpc(cand, "eth_chainId"), 16);
      latestBlock = parseInt(await rpc(cand, "eth_blockNumber"), 16);
      url = cand;
      break;
    } catch (e) {
      lastErr = e;
    }
  }
  if (!url) {
    out.error = `all ${candidates.length} RPC(s) unreachable. Last: ${lastErr && lastErr.message}`;
    out.triedRpcs = candidates;
    return out;
  }
  out.rpc = url;
  out.chainId = chainId;
  out.latestBlock = latestBlock;
  if (job.chainId != null && job.chainId !== chainId)
    out.chainIdWarning = `leads.json said ${job.chainId} but RPC reports ${chainId}`;

  out.code = await checkCode(url, chainId);
  const deployedFactories = out.code.filter(
    (c) => c.label.startsWith("Proxy factory") && c.deployed === true
  );
  if (o.logs !== false && deployedFactories.length)
    out.safes = await countSafes(url, deployedFactories, latestBlock, o.chunk || 100000);

  const anyDeployed = out.code.some((c) => c.deployed === true);
  out.cell_safe_state =
    out.code
      .map((c) => `${c.label}: ${c.deployed === true ? "YES" : c.deployed === false ? "NO" : c.deployed}`)
      .join("\n") + `\nBy eth_getCode at block ${latestBlock}, ${new Date().toISOString().slice(0, 10)}.`;
  out.cell_safes_created = out.safes
    ? `${out.safes.count} distinct Safe proxies` +
      (out.safes.firstBlock != null ? `, blocks ${out.safes.firstBlock}-${out.safes.lastBlock}` : "") +
      (out.safes.scanErrors ? ` (${out.safes.scanErrors} log-scan chunks failed — try --chunk 50000)` : "")
    : anyDeployed
    ? "Safe singleton(s) present but no proxy factory — unusual; check manually"
    : "NO Safe contracts deployed at all — not the 'deployed-but-no-UI' lead pattern";
  return out;
}

(async () => {
  const o = args();
  let jobs;
  if (o.batch) jobs = JSON.parse(fs.readFileSync(o.batch, "utf8"));
  else jobs = [{ name: o.name, rpcUrl: o.rpc, chainId: o.chainId }];

  for (const job of jobs) {
    let r;
    try {
      r = await run(job, o); // per-job isolation: one bad chain never aborts the batch
    } catch (e) {
      r = { name: job.name || "(unnamed)", error: `unexpected: ${e.message}` };
    }
    console.log("\n========================================");
    console.log(`CHAIN: ${r.name}`);
    if (r.error) { console.log("SKIPPED:", r.error); continue; }
    console.log(`RPC:   ${r.rpc}`);
    console.log(`chainId=${r.chainId} latestBlock=${r.latestBlock}`);
    if (r.chainIdWarning) console.log("WARN:  " + r.chainIdWarning);
    console.log("\n--- Safe state on chain ---\n" + r.cell_safe_state);
    console.log("\n--- Safes created ---\n" + r.cell_safes_created);
  }
  console.log("\n(done)");
})();
