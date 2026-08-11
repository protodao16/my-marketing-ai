#!/usr/bin/env python3
"""Batch data for rows 31-60 + assembly of enriched & messages CSVs."""
import csv
from generate import case1, case2, case3, case4, case5, case6

# Each network: fork, version, dex_notes, website, project, why_fit, case,
# research_notes, and message-builder args.
# msg is a lambda producing the 5-message dict.
N = {}
def reg(name, fork, version, dex_notes, website, project, why_fit, case, notes, msg):
    N[name] = dict(fork=fork, version=version, dex_notes=dex_notes, website=website,
                   project=project, why_fit=why_fit, case=case, notes=notes, msg=msg)

reg("Prom", "YES;UNCLEAR", "V2;UNKNOWN",
    "savmSwap: YES/V2 — Multiple sources (DefiLlama, SatoshiVM docs) describe savmSwap as a Uniswap V2 fork, deployed on both Prom and SatoshiVM. | v60: UNCLEAR — swap+LP AMM on Prom (v60.io, DefiLlama ~$113K) but fork lineage unconfirmed; looks V2-style, unverified.",
    "https://prom.io",
    "Modular zkEVM L2 (Polygon CDK) focused on Web3 gaming and NFT marketplaces; native token PROM (formerly Prometeus Network).",
    "~$507K TVL on a V2-era DEX (savmSwap) with no V3 and no Safe — a V3 upgrade plus canonical infra would modernize a gaming/NFT chain's liquidity layer.",
    "CASE_5",
    "savmSwap confirmed UniV2; v60 lineage unclear. No Safe (chain_id 277). ~$507K TVL. V2->V3 lead; Safe also a gap.",
    lambda: case5("Prom", "savmSwap",
        "for a gaming/NFT L2, V3 concentrated liquidity gives market makers tighter pricing on your key pairs as volume ramps"))

reg("HashKey Chain", "NO;UNCLEAR", "—",
    "DODO AMM: NO — DODO uses an oracle-based Proactive Market Maker (PMM), explicitly not a Uniswap AMM fork. | HyperInDex: UNCLEAR — self-described hybrid DEX combining AMM (DODO/PMM-style) + order book; not a clear Uniswap fork.",
    "https://hsk.xyz",
    "Regulatory-compliant, institutional-grade Ethereum L2 (OP Stack) by HashKey Group bridging TradFi and Web3; gas token HSK.",
    "Safe present and a high-credibility institutional L2, but incumbent DEXes are DODO/orderbook (non-Uniswap) — a canonical Uniswap AMM would seed a compliant spot-liquidity venue. DeFi still nascent (~$2K DEX TVL).",
    "CASE_2",
    "DODO=not Uniswap; HyperInDex lineage unclear (PMM+orderbook). Safe present (chain_id 177). DeFi nascent (~$2K TVL) but high-value institutional logo (HashKey Group). CASE_2 cold Uniswap.",
    lambda: case2("HashKey Chain",
        "your current venues are DODO/orderbook-style, so there's no canonical constant-product AMM for long-tail pairs — and for an institution-grade L2 a DAO-recognized Uniswap is the liquidity layer partners expect"))

reg("MTT Network", "UNCLEAR", "UNKNOWN",
    "Yaakoswap: UNCLEAR — listed on DefiLlama as a DEX on MTT Network with a swap AMM, but no docs/GitHub confirm fork lineage; ~$8 TVL suggests an effectively dormant project.",
    "https://www.mtt.network",
    "MetaDot Mainnet — EVM-compatible chain (Cosmos SDK) purpose-built for e-sports tournaments; native token MTT (chain_id 6880).",
    "Essentially dormant (~$8 TVL) with an unverified DEX — very low near-term value; exploratory at best.",
    "CASE_6",
    "Yaakoswap lineage unclear; ~$8 TVL = effectively defunct. safe_exists=YES (chain_id 6880). DEPRIORITIZE — confirm the chain is still active before outreach.",
    lambda: case6("MTT Network", "Yaakoswap",
        "Yaakoswap is your DEX but its stack isn't documented and on-chain activity looks dormant",
        "if the chain is being revived, a canonical Uniswap + Safe would be the base layer to rebuild DeFi credibility on"))

reg("WINR", "YES", "V3",
    "Camelot V3: YES/V3 — Camelot V3 is built on Algebra Integral (v1.9) concentrated liquidity, a Uniswap-V3 derivative. Note: much of the reported Camelot/WINR TVL appears to sit on Arbitrum, not the WINR Orbit chain.",
    "https://winr.games",
    "Gaming-focused Arbitrum Orbit L2/L3 (Conduit) powering the WINR on-chain gaming ecosystem; native token WINR (chain_id 777777).",
    "Runs a Uniswap-V3-derived DEX (Camelot/Algebra) but has NO Safe — the gap is multisig custody. On-chain TVL likely far below the ~$743K listed (Arbitrum-side pairs), so treated as minimal.",
    "CASE_4",
    "Camelot V3 = Algebra (UniV3-derivative). No Safe (chain_id 777777). Listed TVL ~$743K likely Arbitrum-side, not on-chain -> treated as minimal -> CASE_4. Verify on-chain TVL.",
    lambda: case4("WINR",
        "you've already got a Uniswap-v3-derived DEX (Camelot on Algebra)",
        "for a gaming chain custodying player and treasury funds, a proper Safe multisig is the piece bridges and partners check for before committing"))

reg("Hydra Chain", "YES", "BOTH",
    "HydraDEX: YES/BOTH — official docs describe a Uniswap-V3-compatible concentrated-liquidity AMM with coexisting V2 and V3 pools and hybrid routing (Hydra/LockTrip Medium: 'Hydra DEX Launches Concentrated Liquidity and V3 Pools').",
    "https://hydrachain.org",
    "Permissionless EVM L1 with instant finality and PoSA masternode consensus (LockTrip/LOC team); native token HYDRA (chain_id 4488).",
    "Already runs a full Uniswap V2+V3-style DEX and has Safe — fit is canonical DAO recognition/tooling around the existing stack rather than a net-new DEX. Low TVL (~$21K).",
    "CASE_6",
    "HydraDEX = UniV2+V3-style (own build). Safe present (chain_id 4488). Low TVL. CASE_6 canonical recognition; DEX likely redundant.",
    lambda: case6("Hydra Chain", "HydraDEX",
        "HydraDEX already runs Uniswap-V2+V3-style pools and Safe is live",
        "since you already run V2+V3 pools, the value is canonical DAO recognition — getting your DEX officially recognized so aggregators prioritize it"))

reg("Form Network", "UNCLEAR", "UNKNOWN",
    "Fibonacci Dex: UNCLEAR — the primary DEX on Form (swap + LP pools per Fibonacci docs) but no source confirms V2 vs V3 fork lineage. Name-collision caution vs FibSwap and the separate Fibonacci Network L1.",
    "https://form.network",
    "Ethereum L2 built for SocialFi (OP Stack + Celestia DA, incubated by Roll Labs); native token FORM (chain_id 478).",
    "Distinctive SocialFi thesis and Safe present, but the incumbent DEX's lineage is unclear and TVL is minimal (~$5.9K) — exploratory.",
    "CASE_6",
    "Fibonacci lineage unclear (name collisions). Safe present (chain_id 478). Minimal TVL. CASE_6 exploratory.",
    lambda: case6("Form Network", "Fibonacci Dex",
        "Fibonacci is your DEX but its underlying stack isn't documented",
        "for a SocialFi L2, a canonical DAO-recognized Uniswap gives your social-token markets an aggregator-visible venue"))

reg("Story", "YES;YES", "BOTH",
    "PiperX: YES/BOTH — sources state PiperX is 'forked from Uniswap' with both standard (V2) and concentrated (V3) pools. | Story Hunt: YES/V3 — StoryHunt docs describe a native AMM 'inspired by Uniswap V3' (concentrated liquidity).",
    "https://www.story.foundation",
    "Purpose-built EVM L1 (EVM + Cosmos SDK) for tokenizing and managing intellectual property ('IPFi'); native token IP (chain_id 1514).",
    "~$632K TVL, Safe live, and two Uniswap-derived DEXes (PiperX V2+V3, Story Hunt V3) already running — strong fit for canonical DAO recognition + routing/graph tooling.",
    "CASE_6",
    "PiperX (BOTH) + Story Hunt (V3), both Uniswap-derived. Safe present (chain_id 1514). ~$632K TVL. Strong CASE_6 canonical-recognition lead.",
    lambda: case6("Story", "PiperX / Story Hunt",
        "PiperX (V2+V3) and Story Hunt (V3) already run Uniswap-derived DEXes and Safe is live",
        "with real IP-token liquidity building, canonical DAO recognition would make your V3 the venue aggregators route IPFi flow through"))

reg("Stratis", "UNCLEAR", "UNKNOWN",
    "StraxSwap: UNCLEAR — confirmed native DEX of the Stratis EVM ecosystem (DefiLlama, straxswap.com) with swaps + LP, but no source confirms Uniswap fork/version. Likely a V2-style AMM, unverified.",
    "https://www.stratisplatform.com",
    "Enterprise-focused chain that migrated to an EVM-compatible L2 (Stratis EVM), mid-rebrand toward 'Xertra'; native token STRAX (chain_id 105105).",
    "Safe present, but chain is mid-rebrand/migration with low TVL (~$26K) and an unverified DEX stack — exploratory, lower priority.",
    "CASE_6",
    "StraxSwap lineage unclear. Safe present (chain_id 105105). Mid-rebrand to Xertra; low TVL. CASE_6 exploratory.",
    lambda: case6("Stratis", "StraxSwap",
        "StraxSwap is your native DEX but its underlying stack isn't documented",
        "as the EVM chain settles post-rebrand, a canonical DAO-recognized Uniswap would give it a credible, aggregator-visible liquidity layer"))

reg("Silicon zkEVM", "UNCLEAR", "UNKNOWN",
    "Fizzswap V3/V2: UNCLEAR — the V2/V3 split-product naming is the classic pattern for a Uniswap V2+V3 fork pair, and Fizzswap is a native DEX in the Silicon ecosystem, but no primary doc/GitHub confirms the lineage. Strong circumstantial signal, unconfirmed.",
    "https://silicon.network",
    "zkEVM Ethereum L2 on Polygon CDK focused on low-fee dApp deployment (chain_id 2355).",
    "Polygon-CDK zkEVM where Uniswap deploys cleanly, but tiny TVL (~$7.7K) and no Safe indicate a very early ecosystem — exploratory.",
    "CASE_6",
    "Fizzswap V2/V3 naming suggests UniV2+V3 fork but unconfirmed. No Safe (chain_id 2355). Minimal TVL. CASE_6 exploratory.",
    lambda: case6("Silicon zkEVM", "Fizzswap",
        "Fizzswap already runs V2/V3-style pools but its fork lineage isn't documented",
        "if Fizzswap is Uniswap-based there's likely a clean path to canonical recognition; if not, a canonical Uniswap + Safe would anchor DeFi on a young zkEVM"))

reg("Parex", "UNCLEAR", "UNKNOWN",
    "RaccoonSwap: UNCLEAR — confirmed Parex's native multichain AMM DEX (whitepaper at racconswap.gitbook.io) for PRX swaps/pools, but no source states Uniswap fork/version; single-product (no V2/V3 split) hints at a basic constant-product AMM, unverified.",
    "https://parex.network",
    "EVM-compatible L1 aimed at consumer-friendly DeFi and a dApp/publishing platform; native token PRX (chain_id 322202).",
    "Small isolated L1 with low TVL (~$15K), a single unverified in-house DEX, and no Safe — exploratory, low priority.",
    "CASE_6",
    "RaccoonSwap lineage unclear (in-house AMM). No Safe (chain_id 322202). Low TVL. CASE_6 exploratory.",
    lambda: case6("Parex", "RaccoonSwap",
        "RaccoonSwap is your native AMM but its underlying stack isn't documented",
        "if you want PRX markets visible to aggregators, a canonical DAO-recognized Uniswap (plus a Safe) is the credible base"))

reg("Zero Network", "YES;YES", "BOTH",
    "SakuraSwap CLMM/AMM: YES/BOTH — Protofire's own blog ('SakuraSwap: Building a Uniswap v3 DEX with Protofire') and DefiLlama confirm it's built on Uniswap v3 architecture and fully compatible with the Uniswap v3 interface; CLMM = Uniswap V3 concentrated liquidity, AMM = V2-style pools.",
    "https://zero.network",
    "ZK Stack (zkSync Elastic Network) Ethereum L2 by the Zerion team, with native account abstraction and gasless UX (chain_id 543210).",
    "~$148K TVL, Safe present, and its flagship DEX (SakuraSwap) is a Uniswap V2+V3 fork BUILT BY PROTOFIRE — a warm relationship; fit is canonical DAO recognition + deeper tooling.",
    "CASE_6",
    "SakuraSwap = Protofire-built UniV2+V3 fork (WARM on DEX side). Safe present (chain_id 543210). Source lists safe_protofire=NO but SakuraSwap is Protofire-built — VERIFY warm status. ~$148K TVL. CASE_6.",
    lambda: case6("Zero Network", "SakuraSwap",
        "SakuraSwap — which we built with your team — already runs Uniswap V2+V3, and Safe is live",
        "since we built SakuraSwap on Uniswap v3 with you, the natural next step is canonical DAO recognition so aggregators prioritize it"))

reg("Superposition", "YES;YES", "BOTH",
    "Camelot V3: YES/V3 — Algebra Integral concentrated liquidity (Uniswap-V3 derivative). | Camelot V2: YES/V2 — Uniswap-V2-style fork. Camelot docs list Superposition as a supported Arbitrum-Orbit chain with V2+V3 pools.",
    "https://superposition.so",
    "DeFi-focused Arbitrum Orbit L3 built with Arbitrum Stylus (Rust); native Longtail AMM, 'pays-you-to-use' yield (chain_id 55244).",
    "Genuine DeFi chain with Safe and Camelot liquidity (~$77K), but native stack is Stylus/Algebra — a canonical Uniswap would be net-new (non-redundant) but competing; fit is canonical recognition or a second venue.",
    "CASE_6",
    "Camelot V2 + V3(Algebra) + native Stylus AMM. Safe present (chain_id 55244). CASE_6; canonical Uniswap would compete with Camelot — position as second venue/recognition.",
    lambda: case6("Superposition", "Camelot / Longtail",
        "Camelot (V2 + Algebra V3) and a native Stylus AMM already run here, and Safe is live",
        "your native stack is Stylus/Algebra — a canonical DAO-recognized Uniswap would be a net-new, aggregator-prioritized venue rather than a duplicate"))

reg("Artela", "YES", "V2",
    "ArtexSwap: YES/V2 — Artela/Gate docs state it offers 'basic operations similar to UniswapV2' (constant-product AMM), wrapping standard Uniswap-V2 mechanics with Artela's Aspect security layer (MEV/rug checks) rather than changing swap math.",
    "https://artela.network",
    "Extensible EVM-compatible L1 adding a WASM VM and 'Aspect' native extensions (EVM++) for parallel execution; native token ART (chain_id 11820).",
    "Only DEX is a Uniswap-V2 clone (ArtexSwap) with no V3 — a V3 concentrated-liquidity layer is a clean upgrade for a chain courting sophisticated builders.",
    "CASE_5",
    "ArtexSwap = UniV2 clone (+ Aspect security wrapper). Safe present (chain_id 11820). No tracked TVL. CASE_5 V2->V3.",
    lambda: case5("Artela", "ArtexSwap",
        "your Aspect/EVM++ security angle pairs well with V3 — concentrated liquidity plus your MEV/rug checks is a strong story for serious market makers"))

reg("Waterfall", "NO", "—",
    "Aquadex: NO — described as a Curve-based AMM optimized for low-slippage/stable trading (Curve = not Uniswap); appears early-stage/pre-launch, so live status uncertain.",
    "https://waterfall.network",
    "EVM-compatible L1 BlockDAG using DAG-based fast-finality PoS for scalability; native coin WATER (chain_id 181).",
    "Safe present but the only DEX is Curve-style (stable-focused) and early-stage — a canonical Uniswap AMM would cover the volatile-pair liquidity the Curve design doesn't.",
    "CASE_2",
    "Aquadex = Curve-based (not Uniswap), early/pre-launch. Safe present (chain_id 181). No tracked TVL. CASE_2 cold Uniswap (complements Curve).",
    lambda: case2("Waterfall",
        "your Aquadex is Curve-style (built for stable pairs) — a canonical Uniswap v2+v3 would give volatile long-tail pairs the venue they're missing"))

reg("CrossFi", "UNCLEAR", "UNKNOWN",
    "xSwap DEX: UNCLEAR — CrossFi docs describe xSwap as an AMM DEX (swaps + LPs, incl. xUSD) that presents as a standard constant-product Uniswap-style AMM, but docs don't state V2 vs V3, so lineage/version unverified. (Distinct from the unrelated XSwap on XDC.)",
    "https://crossfi.org",
    "Modular L1 combining Cosmos SDK (consensus) with an EVM execution layer; native token XFI (chain_id 4158).",
    "Warm — Protofire already deployed Safe here (safe_protofire=YES). EVM with real TVL (~$40K) and only an in-house AMM of unknown lineage — canonical Uniswap is a clear add on an existing relationship.",
    "CASE_6",
    "safe_protofire=YES (WARM). xSwap = Uniswap-style AMM, version undocumented -> UNCLEAR. ~$40K TVL. CASE_6 with warm Safe angle.",
    lambda: case6("CrossFi", "xSwap DEX",
        "we deployed your Safe already, and xSwap is your in-house AMM whose stack isn't public",
        "since we already run your Safe, the easy next step is confirming what xSwap is built on and, if useful, adding a canonical DAO-recognized Uniswap"))

reg("Odyssey", "UNCLEAR", "UNKNOWN",
    "Diamondswap: UNCLEAR — a constant-product AMM (DIONE/USDC, farms) but Dione markets it as 'more than a fork', built on the Diamond Standard (EIP-2535) proxy pattern; custom architecture + vague sourcing means Uniswap lineage can't be confirmed.",
    "https://www.dioneprotocol.com",
    "Dione Protocol's EVM-compatible L1 focused on renewable/green energy and high throughput; gas token DIONE (chain_id 153153).",
    "Meaningful-ish TVL (~$158K) and no Safe, but the incumbent DEX's bespoke Diamond-Standard design suggests a preference for custom infra — exploratory.",
    "CASE_6",
    "Diamondswap = custom Diamond-Standard AMM, lineage unclear. No Safe (chain_id 153153). ~$158K TVL. CASE_6 exploratory; Safe also a gap.",
    lambda: case6("Odyssey", "Diamondswap",
        "Diamondswap runs a custom Diamond-Standard (EIP-2535) AMM rather than a documented Uniswap fork",
        "if you'd want an aggregator-recognized venue alongside Diamondswap, a canonical Uniswap (plus a Safe for the treasury) is the standard path"))

reg("DuckChain", "YES;YES;UNCLEAR", "BOTH",
    "Camelot V3: YES/V3 — Algebra V1.9 concentrated liquidity (Uniswap-V3 derivative), deployed on DuckChain. | Camelot V2: YES/V2 — Uniswap-V2 fork. | DuckSwap: UNCLEAR — low-volume native AMM, fork base unconfirmed. Note: DuckChain chain_id = 5545.",
    "https://duckchain.io",
    "EVM-compatible L2 on TON ('Telegram AI Chain') bringing Telegram users into crypto with AI features; native token DUCK (chain_id 5545).",
    "Already hosts Camelot's full V2+V3 (Algebra) stack, so a canonical Uniswap would be largely redundant; very low TVL (~$1.9K) and unconfirmed Safe — low priority.",
    "CASE_6",
    "Camelot V2+V3(Algebra) already present; DuckSwap unclear. chain_id 5545 (blank in source). safe_exists UNCLEAR. ~$1.9K TVL. LOW priority CASE_6.",
    lambda: case6("DuckChain", "Camelot / DuckSwap",
        "Camelot already runs V2 + Algebra-V3 here (with a native DuckSwap too)",
        "with Camelot's V2+V3 already live, the main value is canonical DAO recognition — otherwise it's redundant"))

reg("QL1", "YES", "V2",
    "QOMSWAP: YES/V2 — QL1's native DEX; the QL1 explorer lists its LP/router token as 'QSWAP-V2' and it runs standard swap/LP/farm AMM features, consistent with a Uniswap-V2 fork (V2 naming + feature set; not code-audited).",
    "https://qom.one",
    "Community-driven L1 combining EVM with the Cosmos ecosystem and IBC; native token QOM.",
    "V2-style DEX (QOMSWAP), no V3 — a V3 upgrade would modernize its swap layer; sparse public docs and unverified TVL make it lower-confidence.",
    "CASE_5",
    "QOMSWAP = UniV2 (per 'QSWAP-V2' naming). safe_exists UNCLEAR; chain_id not in source. No tracked TVL. CASE_5 V2->V3; lower-confidence, verify.",
    lambda: case5("QL1", "QOMSWAP",
        "layering V3 on top gives your QOM markets tighter pricing and pulls in active LPs that V2 farming alone won't"))

reg("VinuChain", "YES", "V3",
    "VinuSwap: YES/V3 — VinuSwap docs/repo describe a thin fork of Uniswap v3, importing tick/sqrt-price/liquidity/fee-growth math unmodified from Uniswap V3 core, with concentrated liquidity + custom fee-manager (vinu.gitbook.io/vinuswap).",
    "https://www.vinuchain.org",
    "EVM-compatible L1 with a 'Determinably Feeless' model (stakers get feeless txs), from the Vita Inu (VINU) memecoin ecosystem; native token VC (chain_id 207).",
    "Already runs a Uniswap-V3 fork (VinuSwap) but has NO Safe and tiny TVL (~$9.6K) — the real gap is multisig custody before capital scales.",
    "CASE_4",
    "VinuSwap = thin UniV3 fork. No Safe (chain_id 207). ~$9.6K TVL. CASE_4 Safe pitch.",
    lambda: case4("VinuChain",
        "VinuSwap already gives you a Uniswap-v3 fork",
        "a memecoin-origin treasury and its LP pools really shouldn't sit behind an EOA — a proper Safe is table-stakes before bigger market makers commit"))

reg("Shido", "YES;YES", "BOTH",
    "Shido Dex V3/V2: YES/BOTH — Shido runs open-source repos (ShidoGlobal/shido-liquidity-pool[-core]) deployed with ChainId.SHIDO and a Uniswap-style 'v3-subgraph' indexer; combined with the V2/V3 product split this indicates a Uniswap V2+V3 fork (README not directly fetchable — strong circumstantial evidence).",
    "https://shido.io",
    "EVM-compatible (also WASM/IBC/Cosmos) high-performance L1 PoS chain for DeFi; native token SHIDO (chain_id tentatively 9008).",
    "Healthy TVL (~$906K) with a native Uniswap-style V2+V3 AMM — strong fit for canonical DAO recognition; Safe status and chain_id need verification.",
    "CASE_6",
    "Shido Dex V2+V3 = Uniswap fork (circumstantial: repos + v3-subgraph). chain_id UNKNOWN in source (tentatively 9008 — VERIFY). safe_exists UNCLEAR -> verify/deploy Safe. ~$906K TVL. CASE_6.",
    lambda: case6("Shido", "Shido Dex",
        "Shido Dex already runs Uniswap-style V2 and V3 pools",
        "with ~$900K TVL on a native Uniswap-style DEX, canonical DAO recognition is what gets it aggregator-prioritized"))

reg("Asset Chain", "YES", "V3",
    "Asset Chain Swap: YES/V3 — classified on DefiLlama/aggregators as a Uniswap V3 fork (AMM) on Asset Chain.",
    "https://xend.finance",
    "Xend Finance's PoS EVM L1 built for Real-World Assets (RWA); ecosystem token RWA (formerly XEND) (chain_id 42420).",
    "Runs a Uniswap-V3 fork but has NO Safe — for an RWA chain, multisig custody is the conspicuous missing piece institutions require. TVL minimal (~$166K).",
    "CASE_4",
    "Asset Chain Swap = UniV3 fork. No Safe (chain_id 42420). ~$166K TVL. RWA chain. CASE_4 Safe pitch.",
    lambda: case4("Asset Chain",
        "Asset Chain Swap already gives you a Uniswap-v3 fork",
        "for a chain built around RWAs, a Safe multisig is exactly what institutional asset partners require before custodying value on you"))

reg("Matchain", "YES;YES", "V2",
    "MSwap: YES/V2 — described as a Uniswap V2 fork DEX on Matchain (mswap.info). | IncaSwap: YES/V2 — classified as a UniswapV2 fork deployed on Matchain.",
    "https://www.matchain.io",
    "Decentralized-AI L2 on BNB Chain (OP Stack + zk-rollup) focused on on-chain identity (MatchID), data sovereignty and AI; native token MAT (chain_id 698).",
    "Both DEXes are Uniswap-V2 forks with no V3, and Safe is present — a clean V2->V3 upgrade for a high-activity identity/AI L2. Low DEX TVL (~$19K).",
    "CASE_5",
    "MSwap + IncaSwap both UniV2. Safe present (chain_id 698). ~$19K TVL. CASE_5 V2->V3.",
    lambda: case5("Matchain", "MSwap, IncaSwap",
        "as identity/AI activity drives token flow, V3 concentrated liquidity is what lets market makers quote your pairs efficiently"))

reg("HeLa", "YES", "V3",
    "cytoswap: YES/V3 — GitHub org hela-cytoswap hosts cytoswap-v3-staker (a direct analog of Uniswap's v3-staker) and advertises a V3 canonical staking contract with concentrated-liquidity pools, indicating a Uniswap V3 fork; no clear V2.",
    "https://helalabs.com",
    "EVM L1 using a fiat/USDC-backed stablecoin (HLUSD) as native gas token, with a separate finite-supply $HELA token; (chain_id 8668).",
    "Runs a Uniswap-V3 fork (cytoswap) but has NO Safe — multisig custody is the gap; TVL minimal (~$117K). Unusual stablecoin-gas model but EVM-compatible.",
    "CASE_4",
    "cytoswap = UniV3 fork (v3-staker). No Safe (chain_id 8668). ~$117K TVL. CASE_4 Safe pitch.",
    lambda: case4("HeLa",
        "cytoswap already gives you a Uniswap-v3 fork",
        "with a fiat-backed stablecoin as gas, a proper Safe is the custody layer institutions and bridges expect before routing value through you"))

reg("Electroneum", "YES;YES", "BOTH",
    "ElectroSwap V3/V2: YES/BOTH — ElectroSwap docs state it is 'built on the solid foundation of Uniswap V2 and V3', offering both V2 pools and V3 concentrated liquidity on the Electroneum Smart Chain.",
    "https://electroneum.com",
    "Mobile-focused EVM L1 (Electroneum Smart Chain, IBFT) aimed at financial inclusion for the unbanked; native token ETN (chain_id 52014).",
    "Already runs a canonical Uniswap V2+V3 fork (ElectroSwap) but has NO Safe — the gap is multisig custody; TVL minimal (~$140K).",
    "CASE_4",
    "ElectroSwap = UniV2+V3. No Safe (chain_id 52014). ~$140K TVL. CASE_4 Safe pitch (DEX already covered).",
    lambda: case4("Electroneum",
        "ElectroSwap already covers Uniswap V2+V3",
        "for a chain focused on financial inclusion, a Safe multisig is what signals to partners and bridges that treasury custody is done properly"))

reg("Polynomial", "NO", "—",
    "Polynomial Liquidity: NO — Polynomial is a decentralized perpetuals/derivatives exchange (pool-based perps AMM upgrading to an orderbook), not a spot Uniswap AMM (polynomial.fi). Beware lookalike phishing domain 'polynominaldex.xyz'.",
    "https://www.polynomial.fi",
    "OP-Stack L2 in the Optimism Superchain purpose-built to hyperscale on-chain derivatives (perps, options, structured vaults) with unified liquidity; (chain_id 8008).",
    "Safe present and meaningful TVL (~$594K), but liquidity is perps/derivatives — there's no spot AMM, so a canonical Uniswap would add the spot-swap venue the chain lacks.",
    "CASE_2",
    "Polynomial = perps/derivatives DEX, not spot AMM (not Uniswap). Safe present (chain_id 8008). ~$594K TVL. CASE_2 cold Uniswap (spot venue). Note phishing lookalike polynominaldex.xyz.",
    lambda: case2("Polynomial",
        "your liquidity today is perps/derivatives — there's no spot AMM, so a canonical Uniswap v2+v3 gives your users and LPs an actual spot-swap venue"))

reg("Dymension", "NO", "—",
    "Dymension DEX: NO — the 'DEX' is a native AMM module in the Dymension Hub for shared RollApp/IRO liquidity, a Cosmos-SDK Balancer/Osmosis-GAMM-style AMM, not a Uniswap fork. No EVM chainId at the Hub level (EVM exists only at individual RollApps).",
    "https://dymension.xyz",
    "Modular Cosmos-SDK 'chain launchpad' settlement hub (network of RollApps) providing shared security and liquidity via a built-in AMM; native token DYM.",
    "Poor fit — the Hub is Cosmos-SDK (no EVM chainId), so canonical Safe/Uniswap can't deploy to the Hub itself, and its native AMM already serves swaps; EVM only exists per-RollApp. Manual review needed.",
    "CASE_4",
    "Dymension Hub = Cosmos-SDK, no EVM chainId; native AMM = Osmosis/Balancer-style (not Uniswap). Safe/Uniswap only deployable at individual EVM RollApp level. MANUAL REVIEW — likely mis-scoped fit. CASE_4 tentative.",
    lambda: case4("Dymension",
        "your Hub AMM is a Cosmos-style module, not an EVM Uniswap",
        "the honest first question is which EVM RollApp we'd target — at that layer a Safe and canonical Uniswap make sense, but the Hub itself is Cosmos-SDK"))

reg("Neo X Mainnet", "YES;YES", "V2",
    "Carrot Swap: YES/V2 — launched a Uniswap-V2-style CPMM (CLMM/Stable on roadmap) per Carrot docs. | Asteroneo: YES/V2 — explicitly 'modeled off Uniswap V2's code' (Neo News Today).",
    "https://neox.org",
    "EVM-compatible sidechain of Neo with dBFT finality, using GAS as native/gas token; brings DeFi to the Neo ecosystem (chain_id 47763).",
    "Two live Uniswap-V2 forks (Carrot, Asteroneo) with no V3, and Safe present — a clean V2->V3 upgrade; low TVL (~$7.5K) tempers upside.",
    "CASE_5",
    "Carrot Swap + Asteroneo both UniV2. Safe present (chain_id 47763). ~$7.5K TVL. CASE_5 V2->V3.",
    lambda: case5("Neo X Mainnet", "Carrot Swap, Asteroneo",
        "both your DEXes are V2 today — layering V3 on top is what pulls in the active LPs and market makers a maturing Neo DeFi scene needs"))

reg("LaChain Network", "UNCLEAR", "UNKNOWN",
    "MateSwap: UNCLEAR — described as the first Argentine DEX on LaChain (trade/stake/farm, a classic UniV2-fork pattern), but site unreachable and no contract-level evidence; a same-named 'Mate' GitBook describes a BSC BEP-20 token + multi-AMM aggregation, so identity is ambiguous.",
    "https://www.lachain.network",
    "EVM-compatible chain built by a LatAm consortium ('built in LatAm, for LatAm') for regional DeFi/payments; native token LAC (chain_id 274).",
    "Safe present on a regional-adoption L1, but MateSwap's fork lineage is unverified and TVL modest (~$45K) — exploratory; confirm the DEX stack first.",
    "CASE_6",
    "MateSwap lineage unclear (site unreachable; name collision). Safe present (chain_id 274). ~$45K TVL. CASE_6 exploratory.",
    lambda: case6("LaChain Network", "MateSwap",
        "MateSwap is your DEX but its underlying stack couldn't be verified",
        "for a LatAm-focused chain, a canonical DAO-recognized Uniswap would give regional builders an aggregator-visible, audited liquidity layer"))

reg("Saakuru", "YES", "V2",
    "Taffy Finance: YES/V2 — explicitly 'a fork of Uniswap v2' with a 0.3% trade fee, tailored for GameFi/gasless trading on Saakuru (Saakuru Labs Medium 'Introducing Taffy DEX').",
    "https://saakuru.com",
    "Gasless EVM L2 (over the Oasys ecosystem; pairs settle in WOAS) focused on GameFi and Web2-friendly dApps; (chain_id 7225878).",
    "Warm — Protofire already deployed Safe (safe_protofire=YES). Runs a Uniswap-V2 fork (Taffy) with no V3 — a clean V2->V3 upgrade on an existing relationship; gasless GameFi focus supports DeFi tooling.",
    "CASE_5",
    "safe_protofire=YES (WARM). Taffy Finance = UniV2 fork, no V3. ~$84K TVL. CASE_5 V2->V3 with warm Safe angle.",
    lambda: case5("Saakuru", "Taffy Finance",
        "since we already deployed your Safe, layering V3 onto Taffy is a natural next step — concentrated liquidity gives your GameFi pairs tighter pricing"))

reg("Mint", "YES", "V3",
    "MintSwap Finance: YES/V3 — the MintSwapFinance GitHub org hosts mintswap-v3-core and mintswap-v3-periphery, direct forks of Uniswap v3-core/v3-periphery (canonical V3 concentrated-liquidity contracts); no V2 repo.",
    "https://www.mintswap.finance",
    "Ethereum OP-Stack L2 in the Optimism Superchain focused on NFTs/NFTFi (Mintverse ecosystem), ETH-denominated UX; (chain_id 185).",
    "Warm — Protofire already deployed Safe (safe_protofire=YES). Runs a canonical Uniswap V3 fork (MintSwap) — strong fit for canonical DAO recognition + tooling on an existing relationship.",
    "CASE_6",
    "safe_protofire=YES (WARM). MintSwap = direct UniV3 fork (v3-core/periphery). No tracked TVL. CASE_6 canonical recognition + warm Safe.",
    lambda: case6("Mint", "MintSwap Finance",
        "we deployed your Safe already, and MintSwap runs a canonical Uniswap V3 fork",
        "since we already run your Safe and MintSwap is a clean Uniswap v3 fork, the natural next step is canonical DAO recognition so aggregators prioritize your NFTFi liquidity"))

# ------------------- assembly -------------------
SRC = "source_original.csv"
OUT_ENRICHED = "W3_node_Leadgen_Uniswap_enriched.csv"
OUT_MESSAGES = "W3_node_Leadgen_Uniswap_messages.csv"

# column indices
C_FORK, C_VER, C_NOTES, C_WEB, C_PROJ, C_FIT, C_CASE = 12,13,14,15,16,17,18
C_TGC, C_TGF, C_LIC, C_LIF, C_LIFU, C_RES = 19,20,21,22,23,24

with open(SRC, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

BATCH_ROWS = list(range(31, 61))  # logical rows Prom..Mint
missing = []
messages_out = []
for idx in BATCH_ROWS:
    r = rows[idx]
    name = r[0]
    if name not in N:
        missing.append((idx, name))
        continue
    d = N[name]
    m = d["msg"]()
    r[C_FORK] = d["fork"]
    r[C_VER] = d["version"]
    r[C_NOTES] = d["dex_notes"]
    r[C_WEB] = d["website"]
    r[C_PROJ] = d["project"]
    r[C_FIT] = d["why_fit"]
    r[C_CASE] = d["case"]
    r[C_TGC] = m["tg_cold"]
    r[C_TGF] = m["tg_followup"]
    r[C_LIC] = m["li_connect"]
    r[C_LIF] = m["li_first"]
    r[C_LIFU] = m["li_followup"]
    r[C_RES] = d["notes"]
    rows[idx] = r
    # validate li_connect <= 300 chars
    if len(m["li_connect"]) > 300:
        print(f"WARN li_connect >300 for {name}: {len(m['li_connect'])}")
    messages_out.append([name, d["case"], m["tg_cold"], m["tg_followup"],
                         m["li_connect"], m["li_first"], m["li_followup"]])

if missing:
    print("MISSING:", missing)

with open(OUT_ENRICHED, "w", newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(rows)

with open(OUT_MESSAGES, "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(["network_name","case","tg_cold","tg_followup","li_connect","li_first","li_followup"])
    w.writerows(messages_out)

print(f"Enriched rows written: {len(rows)} (incl header). Batch filled: {len(messages_out)}.")
print(f"Messages CSV rows: {len(messages_out)}.")
# case distribution
from collections import Counter
print("Case distribution:", dict(Counter(m[1] for m in messages_out)))
