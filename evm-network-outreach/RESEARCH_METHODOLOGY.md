# EVM Network Research & Outreach — Methodology & Findings

Generated: 2026-07-22. Source: `W3_node_Leadgen__Sheet64.csv` (149 EVM networks).

## Outputs
- **`evm_networks_enriched.csv`** — all 149 original rows + new columns. STEP 1–2 (`safe_protofire`, `safe_exists`) computed for **all** networks; STEP 3/5/6 research + messages filled for the **first 30** only (per task scope).
- **`evm_networks_outreach_messages.csv`** — first 30 networks: `network_name, case, tg_cold, tg_followup, li_connect, li_first, li_followup`.

## New columns in the enriched CSV
`safe_protofire, safe_exists, uniswap_fork, uniswap_version, dex_notes, website_found, project_description, why_good_fit, outreach_case, tg_cold, tg_followup, li_connect, li_first, li_followup, research_notes`

---

## STEP 1 — `safe_protofire` (IMPORTANT LIMITATION)
`https://safe.protofire.io/safes/` and all of `protofire.io` are **blocked by this environment's network policy** (confirmed policy-level 403 at the proxy — not a transient error). The authoritative hub list could not be fetched directly.

**Proxy source used instead:** Protofire's public config repo **`github.com/protofire/safe-configs`** (`configs/chains.json`, 149 chains, keyed by chainId + name) — this feeds the Safe Config Service behind the hub. Matched against our networks by exact chain_id and fuzzy name.
- Confirmed `YES` (all 149): **Botanix** (manual evidence — LinkedIn announcement), Saakuru, Mint, re.al, Immutable zkEVM, Horizen EON, Beam (repo "Meritcircle"), Kroma, Tenet, Boba_Bnb, DFK, CrossFi (repo has "CrossFi Testnet").
- Excluded false positives from chain_id collisions: **JOC** (chain 81 = Astar *Shibuya*), **inEVM** (2525 = "BB1").
- Caveats: the repo is **stale** (omits some known 2025 Protofire deployments), so `NO` is not proof of non-deployment. **None of the first 30 are Protofire-deployed except Botanix.** `safe_protofire` should be re-verified against the live hub when it is reachable.

## STEP 2 — `safe_exists` (via Chain ID)
For each network's `chain_id`, checked membership in the `networkAddresses` keys of the three Safe deployment files (v1.3.0 gnosis_safe, v1.4.1 safe, v1.5.0 safe). `YES` if present in ANY; `NO` if absent; **`UNCLEAR`** if the source row has no chain_id. This is fully reproducible (562 unique chain_ids across the three files).
- Flag: **JOC** `safe_exists=YES` on chain_id 81 is likely the Astar Shibuya deployment, not Japan Open Chain — verify.

## STEP 3 — DEX research (first 30)
Web-searched each DEX ("[DEX] [chain] AMM", "[DEX] uniswap fork"). Recorded `uniswap_fork` (YES/NO/UNCLEAR), `uniswap_version` (V2/V3/BOTH/UNKNOWN), and evidence in `dex_notes`. Genuinely undetermined DEXes are marked **UNCLEAR** rather than guessed. Note: DefiLlama's authoritative `forkedFrom` field was network-blocked, so a few classifications rely on project docs/GitHub and are flagged.

Key non-Uniswap DEXes found: OroSwap (Astroport), Carbon DeFi (Bancor), Althea iFi (Ambient), WoofSwap (Solidly ve(3,3)), Tigris/Mezo (ve(3,3), lineage unconfirmed).

## STEP 4 — Case assignment
Decision rule applied (documented so it can be audited):
- **V2 Uniswap fork, no V3** → `CASE_5` (V2→V3 upgrade)
- **DEX exists but fork UNCLEAR** → `CASE_6` (exploratory)
- **No Uniswap fork** (non-Uniswap DEX or none): `safe_protofire=YES`→`CASE_1`; else `safe_exists=YES`→`CASE_2`; else TVL≥$500k→`CASE_3`, else `CASE_4`
- **Already has a Uniswap V3 fork:** if no Safe → Safe pitch (`CASE_3`/`CASE_4` by TVL, personalized "DEX covered, Safe is the gap"); if Safe present → `CASE_6` (canonical-DAO-recognition angle; lower priority)

TVL threshold: <$500k = minimal, ≥$500k = meaningful.

**Distribution (first 30):** CASE_6 ×17, CASE_5 ×7, CASE_4 ×4, CASE_3 ×2, CASE_1 ×0, CASE_2 ×0.
**Finding:** No first-30 network is CASE_1/CASE_2 — every network that has Safe already also has a Uniswap-fork or unclear DEX, so the warm/cold *greenfield*-Uniswap pitch never applies here. Many chains fall to CASE_6 because they already run a Uniswap-v3-style fork (the honest angle is canonical recognition, not a fresh deploy).

## STEP 5/6 — Website, description, fit
`website_found` and `project_description` researched per network (first 30). `why_good_fit` justifies the lead. A tailored benefit line (based on each project's focus/field) is woven into `tg_cold` and `li_first`.

## Outreach messages
Built from the task's per-case base templates, personalized with chain name, DEX name, TVL signal, a project-specific detail, and a benefit line. Tone: casual/conference, short. `li_connect` enforced ≤300 chars. **Contact names are `[Name]` placeholders** — the source data has no contacts.

## Flagged for manual review
- **Titan** — network identity + "Hyperion DEX" unverified (name collides with unrelated projects). No outreach until identified.
- **Botanix** — WARM (Protofire Safe) BUT the L2 announced wind-down (withdrawal deadline ~2026-07-09, now passed). Likely defunct — do not prioritize.
- **ENI** — reported ~$215.6M TVL looks large for the profile; verify before leaning on it.
- **JOC** — chain_id 81 / Shibuya collision (see above).
- **ZIGChain, Coti, OpenGPU** — no chain_id in source → `safe_exists` unverified.
- **Coti** — Safe on COTI was deployed by *Palmera* (a competing Safe partner), not Protofire.
- DEXes marked UNCLEAR (BCSwap, JOC Dex, Gate Swap, SimitciSwap, Dopin, Moonchain Swap, OpenBiSea, Tigris) — confirm stack directly with the project.
