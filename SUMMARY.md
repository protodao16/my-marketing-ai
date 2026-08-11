# EVM Network Research & Outreach — Batch rows 31–60

Enriched the lead dataset and generated outreach messages for **networks 31–60 (Prom → Mint)**.
Networks 1–30 (Eteria → Moonchain) were already completed in the source file and are left untouched.

## Files
- `W3_node_Leadgen_Uniswap_enriched.csv` — full original dataset (149 networks) with rows 31–60 enriched:
  `uniswap_fork`, `uniswap_version`, `dex_notes`, `website_found`, `project_description`,
  `why_good_fit`, `outreach_case`, the five message columns, and `research_notes`.
- `W3_node_Leadgen_Uniswap_messages.csv` — `network_name, case, tg_cold, tg_followup, li_connect, li_first, li_followup` for the 30 batch networks.
- `source_original.csv`, `generate.py`, `data_and_run.py` — inputs / reproducible build.

## STEP 1 — DEX research
For each DEX we searched `"[DEX] [chain] AMM"` plus project docs/GitHub. Classified `uniswap_fork` as
YES / NO / UNCLEAR with a version and a one-line evidence note. Rules applied:
- Algebra Integral (e.g. Camelot V3) counted as a **Uniswap-V3 derivative → YES/V3**.
- Solidly/ve(3,3), Astroport, Bancor, Curve, Ambient, DODO/PMM → **NO**.
- Genuinely undetermined lineage → **UNCLEAR** (never guessed).

## STEP 2 — Case logic (derived from the completed rows 1–30)
1. Confirmed Uniswap **V2 only** (no V3) → **CASE_5** (V2→V3 upgrade), regardless of Safe.
2. DEX lineage **UNCLEAR** → **CASE_6** (exploratory), regardless of Safe.
3. Confirmed Uniswap **V3 / BOTH**:
   - Safe present (or unverified) → **CASE_6** (canonical DAO recognition).
   - Safe **confirmed absent** → Safe pitch: **CASE_3** if TVL ≥ $500k, else **CASE_4**.
4. **No Uniswap** (confirmed non-Uniswap DEX or no real AMM):
   - `safe_protofire=YES` → **CASE_1**; else `safe_exists=YES` → **CASE_2**;
   - else no Safe & TVL ≥ $500k → **CASE_3**; else → **CASE_4**.

TVL threshold: minimal < $500k ≤ meaningful.

Batch distribution: CASE_2 ×3, CASE_4 ×6, CASE_5 ×6, CASE_6 ×15 (no CASE_1/CASE_3 in this batch).

## Flags for manual review
- **MTT Network** — ~$8 TVL, DEX unverified: effectively dormant. Confirm chain is live before outreach.
- **WINR** — listed ~$743k TVL likely reflects Arbitrum-side Camelot pairs, not the Orbit chain; treated as minimal (CASE_4). Verify on-chain TVL.
- **Dymension** — Hub is Cosmos-SDK (no EVM chainId); native AMM is Osmosis/Balancer-style. Safe/Uniswap deployable only at individual EVM RollApp level — likely mis-scoped; verify target.
- **Zero Network** — SakuraSwap is a **Protofire-built** Uniswap V2+V3 fork (warm on the DEX side) yet source lists `safe_protofire=NO`. Verify the relationship/flag.
- **Shido** — chain_id blank in source (tentatively 9008); DEX fork inferred from repos + v3-subgraph (not code-confirmed); Safe unverified. Verify before outreach.
- **CrossFi / Saakuru / Mint** — `safe_protofire=YES` (warm); messages reference the existing Safe relationship.
- **DuckChain** — chain_id 5545 (blank in source); Camelot V2+V3 already live (canonical Uniswap largely redundant); Safe unverified. Low priority.
- **Polynomial** — watch the lookalike phishing domain `polynominaldex.xyz` (real site is polynomial.fi).
- Egress limits blocked several DefiLlama/GitHub/docs fetches; UNCLEAR calls (Fizzswap, StraxSwap, RaccoonSwap, Fibonacci, MateSwap, HyperInDex, Diamondswap) rest on search snippets — worth on-chain factory confirmation before high-touch outreach.
