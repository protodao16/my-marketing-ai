# Safe on-chain check — automation for the DPL lead-gen sweep

`safe-check.mjs` reproduces what the internal **evm-checker**
(https://evm-checker.safe.protofire.io/) does, as a batchable script, so the
on-chain columns of the lead sheet (`Safe state on chain`, `Safes created`) can
be filled automatically for every lead instead of pasting RPCs one by one.

It is deterministic: Safe deploys to the **same canonical addresses on every EVM
chain**, and those addresses come from `@safe-global/safe-deployments` (the
authoritative package Safe's own tooling uses) — not hardcoded guesses.

## What it checks, per chain
1. `eth_chainId` + latest block height (sanity / vitals).
2. `eth_getCode` on every Safe singleton, SafeL2 singleton and proxy factory for
   **1.3.0 / 1.4.1 / 1.5.0** → `YES`/`NO` deployed.
3. `ProxyCreation` log scan (`eth_getLogs`, chunked) on each deployed factory →
   number of distinct Safes actually created, and the block range.
4. Prints ready-to-paste `Safe state on chain` and `Safes created` cells.

## Setup
```bash
cd research/tools
npm install @safe-global/safe-deployments
```

## Run
Single chain by RPC:
```bash
node safe-check.mjs --rpc https://rpc.example.xyz --name "Example Chain"
```
Resolve the RPC from a chainlist dump (download once from
https://chainlist.org/rpcs.json):
```bash
node safe-check.mjs --chainlist ./rpcs.json --chainId 61900 --name "MOVA Chain"
```
Batch every lead:
```bash
node safe-check.mjs --batch ./leads.json --chainlist ./rpcs.json
```
Flags: `--chunk 50000` (shrink if a node caps `eth_getLogs` ranges),
`--no-logs` (skip the ProxyCreation scan for a fast code-only pass).

## Where to run it
The check needs outbound access to each target RPC. Inside the locked-down web
session that access is blocked by the org egress policy (RPC hosts, chainlist and
protofire.io all return 403), so run this **locally** (or anywhere with open
network), or have the egress allowlist extended to the RPC hosts + chainlist.org.
The npm install works in either place.
