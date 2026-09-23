#!/usr/bin/env node
// safe-check.mjs — FINAL, self-contained Safe on-chain checker for lead-gen.
// Replicates the internal evm-checker (evm-checker.safe.protofire.io) as a
// batchable script. Download this ONCE; for new batches only edit leads.json.
//
// Per chain, given an RPC (or a chainId resolvable via chainlist rpcs.json):
//   1. eth_chainId + latest block (sanity/vitals).
//   2. eth_getCode on every canonical Safe singleton / SafeL2 / proxy factory for
//      1.3.0 / 1.4.1 / 1.5.0 — addresses from @safe-global/safe-deployments
//      (the authoritative source; not hardcoded). YES = deployed.
//   3. ProxyCreation eth_getLogs scan on each deployed factory -> # of Safes.
//   4. Writes each chain's result to the output file IMMEDIATELY (so nothing is
//      lost if a later chain misbehaves) and prints progress live.
//
// Robustness (why this version does not stall):
//   - every RPC request has a timeout (AbortController);
//   - every CHAIN has a hard overall deadline — a hung RPC can't freeze the batch;
//   - the log scan is bounded (adaptive chunk size, capped request count);
//   - one bad chain is SKIPPED, never aborts the run; retries on 429/5xx.
//
// USAGE (PowerShell):
//   node .\safe-check.mjs --batch .\leads.json --chainlist .\rpcs.json
//   node .\safe-check.mjs --rpc https://rpc.example.xyz --name "Example"
// Options: --out result.txt (default result.txt) | --chunk N | --no-logs
//          | --deadline 150 (seconds per chain) | --timeout 15 (seconds per request)
//
// Setup once:  npm install @safe-global/safe-deployments
// Get chainlist once (optional, for chainId-only leads):
//   curl -s https://chainlist.org/rpcs.json -o rpcs.json

import fs from "node:fs";
import {
  getSafeSingletonDeployment,
  getSafeL2SingletonDeployment,
  getProxyFactoryDeployment,
} from "@safe-global/safe-deployments";

const VERSIONS = ["1.3.0", "1.4.1", "1.5.0"];
const PROXY_CREATION_TOPIC0 =
  "0x4f51faf6c4561ff95f067657e43439f0f856d97c04d9ec9070a6199ad418e235";

function args() {
  const a = process.argv.slice(2);
  const o = { chunk: 0, logs: true, out: "result.txt", deadline: 150, timeout: 15 };
  for (let i = 0; i < a.length; i++) {
    const k = a[i];
    if (k === "--rpc") o.rpc = a[++i];
    else if (k === "--name") o.name = a[++i];
    else if (k === "--chainId") o.chainId = Number(a[++i]);
    else if (k === "--chainlist") o.chainlist = a[++i];
    else if (k === "--batch") o.batch = a[++i];
    else if (k === "--out") o.out = a[++i];
    else if (k === "--chunk") o.chunk = Number(a[++i]);
    else if (k === "--deadline") o.deadline = Number(a[++i]);
    else if (k === "--timeout") o.timeout = Number(a[++i]);
    else if (k === "--no-logs") o.logs = false;
  }
  return o;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function rpc(url, method, params = [], { retries = 2, timeoutMs = 15000 } = {}) {
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
        lastErr = new Error(`HTTP ${res.status}`);
        clearTimeout(timer);
        await sleep(800 * (attempt + 1));
        continue;
      }
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const j = await res.json();
      if (j.error) throw new Error(j.error.message || JSON.stringify(j.error));
      return j.result;
    } catch (e) {
      lastErr = e.name === "AbortError" ? new Error(`timeout ${timeoutMs}ms`) : e;
      if (attempt < retries) await sleep(800 * (attempt + 1));
    } finally {
      clearTimeout(timer);
    }
  }
  throw lastErr;
}

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

async function checkCode(url, chainId, reqOpts) {
  const results = [];
  for (const version of VERSIONS) {
    for (const { label, address } of addressesFor(version, chainId)) {
      let deployed;
      try {
        const code = await rpc(url, "eth_getCode", [address, "latest"], reqOpts);
        deployed = code && code !== "0x" && code !== "0x0";
      } catch (e) {
        deployed = `ERR:${e.message}`;
      }
      results.push({ label, address, deployed });
    }
  }
  return results;
}

async function countSafes(url, factories, latest, o, reqOpts) {
  // Adaptive chunk: keep total getLogs calls per factory bounded (~300) so a
  // very long chain cannot turn into thousands of requests.
  const chunk = o.chunk > 0 ? o.chunk : Math.max(100000, Math.ceil((latest + 1) / 300));
  const proxies = new Set();
  let firstBlock = null, lastBlock = null, scanErrors = 0;
  for (const f of factories) {
    for (let from = 0; from <= latest; from += chunk) {
      const to = Math.min(from + chunk - 1, latest);
      try {
        const logs = await rpc(url, "eth_getLogs", [{
          address: f.address, topics: [PROXY_CREATION_TOPIC0],
          fromBlock: "0x" + from.toString(16), toBlock: "0x" + to.toString(16),
        }], reqOpts);
        for (const log of logs) {
          if (log.topics && log.topics[1]) proxies.add("0x" + log.topics[1].slice(26));
          else if (log.data && log.data.length >= 66) proxies.add("0x" + log.data.slice(26, 66));
          const bn = parseInt(log.blockNumber, 16);
          firstBlock = firstBlock === null ? bn : Math.min(firstBlock, bn);
          lastBlock = lastBlock === null ? bn : Math.max(lastBlock, bn);
        }
      } catch (e) { scanErrors++; }
    }
  }
  return { count: proxies.size, firstBlock, lastBlock, scanErrors, chunk };
}

let CHAINLIST = null;
function loadChainlist(pathOrUrl) {
  if (CHAINLIST || !pathOrUrl || /^https?:\/\//.test(pathOrUrl)) return CHAINLIST;
  try { CHAINLIST = JSON.parse(fs.readFileSync(pathOrUrl, "utf8")); } catch { CHAINLIST = []; }
  return CHAINLIST;
}

async function rpcCandidates(job, o) {
  const list = [];
  const push = (u) => { if (u && !list.includes(u)) list.push(u); };
  push(o.rpc); push(job.rpcUrl); push(job.rpc);
  const chainId = job.chainId ?? o.chainId;
  const src = o.chainlist ?? job.chainlist;
  if (src && chainId != null) {
    let data = loadChainlist(src);
    if (!data && /^https?:\/\//.test(src)) { try { data = await (await fetch(src)).json(); } catch {} }
    const entry = (data || []).find((c) => c.chainId === chainId);
    if (entry) for (const r of entry.rpc || []) {
      const u = typeof r === "string" ? r : r.url;
      if (u && /^https?:\/\//.test(u) && !u.includes("${")) push(u);
    }
  }
  return list;
}

async function runInner(job, o) {
  const out = { name: job.name || "(unnamed)" };
  const reqOpts = { retries: 2, timeoutMs: o.timeout * 1000 };
  const probeOpts = { retries: 1, timeoutMs: Math.min(10000, o.timeout * 1000) };
  const candidates = await rpcCandidates(job, o);
  if (!candidates.length) {
    out.error = "no RPC to try (no rpcUrl and chainId not in chainlist). Add an rpcUrl in leads.json.";
    return out;
  }
  let url, chainId, latestBlock, lastErr;
  for (const cand of candidates) {
    process.stdout.write(`   trying ${cand} ... `);
    try {
      chainId = parseInt(await rpc(cand, "eth_chainId", [], probeOpts), 16);
      latestBlock = parseInt(await rpc(cand, "eth_blockNumber", [], probeOpts), 16);
      url = cand; console.log("OK"); break;
    } catch (e) { lastErr = e; console.log(`fail (${e.message})`); }
  }
  if (!url) { out.error = `all ${candidates.length} RPC(s) failed. Last: ${lastErr && lastErr.message}`; return out; }
  out.rpc = url; out.chainId = chainId; out.latestBlock = latestBlock;
  if (job.chainId != null && job.chainId !== chainId)
    out.chainIdWarning = `leads.json said ${job.chainId} but RPC reports ${chainId}`;
  out.code = await checkCode(url, chainId, reqOpts);
  const factories = out.code.filter((c) => c.label.startsWith("Proxy factory") && c.deployed === true);
  if (o.logs !== false && factories.length) out.safes = await countSafes(url, factories, latestBlock, o, reqOpts);
  const anyDeployed = out.code.some((c) => c.deployed === true);
  out.cell_safe_state = out.code.map((c) =>
    `${c.label}: ${c.deployed === true ? "YES" : c.deployed === false ? "NO" : c.deployed}`).join("\n") +
    `\nBy eth_getCode at block ${latestBlock}, ${new Date().toISOString().slice(0, 10)}.`;
  out.cell_safes_created = out.safes
    ? `${out.safes.count} distinct Safe proxies` +
      (out.safes.firstBlock != null ? `, blocks ${out.safes.firstBlock}-${out.safes.lastBlock}` : "") +
      (out.safes.scanErrors ? ` (${out.safes.scanErrors} scan chunks failed)` : "")
    : anyDeployed ? "Safe singleton(s) present but no proxy factory — check manually"
    : "NO Safe contracts deployed at all — not the 'deployed-but-no-UI' pattern";
  return out;
}

function withDeadline(promise, ms, name) {
  return Promise.race([
    promise,
    new Promise((resolve) => setTimeout(() => resolve({ name, error: `deadline ${ms / 1000}s exceeded (RPC too slow/hung)` }), ms)),
  ]);
}

function render(r) {
  let s = "\n========================================\n";
  s += `CHAIN: ${r.name}\n`;
  if (r.error) return s + "SKIPPED: " + r.error + "\n";
  s += `RPC:   ${r.rpc}\nchainId=${r.chainId} latestBlock=${r.latestBlock}\n`;
  if (r.chainIdWarning) s += "WARN:  " + r.chainIdWarning + "\n";
  s += "\n--- Safe state on chain ---\n" + r.cell_safe_state + "\n";
  s += "\n--- Safes created ---\n" + r.cell_safes_created + "\n";
  return s;
}

(async () => {
  const o = args();
  const jobs = o.batch ? JSON.parse(fs.readFileSync(o.batch, "utf8"))
                       : [{ name: o.name, rpcUrl: o.rpc, chainId: o.chainId }];
  fs.writeFileSync(o.out, `Safe-check run ${new Date().toISOString()} — ${jobs.length} chain(s)\n`);
  console.log(`Checking ${jobs.length} chain(s)... (results also written to ${o.out})`);
  for (const job of jobs) {
    console.log(`\n>> ${job.name || "(unnamed)"}`);
    let r;
    try { r = await withDeadline(runInner(job, o), o.deadline * 1000, job.name || "(unnamed)"); }
    catch (e) { r = { name: job.name || "(unnamed)", error: `unexpected: ${e.message}` }; }
    const block = render(r);
    process.stdout.write(block);
    fs.appendFileSync(o.out, block);      // flush per chain — nothing is ever lost
  }
  const tail = "\n(done)\n";
  process.stdout.write(tail); fs.appendFileSync(o.out, tail);
})();
