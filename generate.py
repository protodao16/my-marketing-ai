#!/usr/bin/env python3
"""Assemble enriched CSV + messages CSV for EVM network outreach (rows 31-60)."""
import csv

SRC = "source_original.csv"
OUT_ENRICHED = "W3_node_Leadgen_Uniswap_enriched.csv"
OUT_MESSAGES = "W3_node_Leadgen_Uniswap_messages.csv"

# Per-network research + personalization for batch rows 31-60 (Prom..Mint).
# Each entry:
#   fork, version, dex_notes, website, project_desc, why_fit, case, research_notes
#   dex_display: how to refer to the DEX in messages
#   hook: case-specific personalization clause (mid-message)
#   observation: short "saw X" clause for CASE_6 / CASE_4 / CASE_3 openers
DATA = {}  # filled below via add()

def add(name, **kw):
    DATA[name] = kw

# ---- CASE_5 message builder (has Uniswap V2, no V3) ----
def case5(chain, dex, hook):
    return {
        "tg_cold": f"hey [Name], Vic from Protofire DAO. looked at {chain}'s DEX setup — you've got {dex} running on V2 which is solid, but no V3 yet. worth considering: V3's concentrated liquidity attracts a different class of LPs — active managers and yield optimizers. V2 is great for passive liquidity, but V3 is what pulls in sophisticated market makers. {hook}. we've deployed V3 on 12+ chains and can layer it on top of your existing V2 — same familiar UI, same stack, just more powerful. usually 2–4 weeks. open to a quick chat?",
        "tg_followup": f"hey [Name], circling back on the V3 idea for {chain} — we can layer it on {dex} without disrupting your current V2 pools. want me to send a quick scope?",
        "li_connect": f"Hi [Name] — Vic at Protofire DAO. {chain} has {dex} on V2 but no V3 yet; V3 is what pulls in active LPs/market makers. We can layer it on. Worth a chat?",
        "li_first": f"Thanks for connecting, [Name]. Saw {chain} runs {dex} on V2 — solid, but no V3. {hook}. V3's concentrated liquidity brings in active managers and yield optimizers that V2 alone won't. We've deployed V3 on 12+ chains and can layer it on your existing V2 (same UI, ~2–4 weeks). Open to a quick chat?",
        "li_followup": f"Hey [Name], no rush — whenever you want to give {chain}'s LPs a V3 option on top of {dex}, it's a clean add-on for us. Happy to share how it went on other chains.",
    }

# ---- CASE_6 message builder (has DEX; canonical-recognition / exploratory) ----
def case6(chain, dex, observation, hook):
    return {
        "tg_cold": f"hey [Name], Vic from Protofire DAO — we deploy core DeFi infra for EVM chains. had a look at {chain} and saw {observation}. curious what it's built on under the hood? depending on the stack there might be a straightforward path to canonical Uniswap DAO recognition, which gets you prioritized by aggregators like 1inch and adds the official DAO badge. {hook}. we've done this for BOB, Abstract, Nibiru and others. if it's already a Uniswap fork we can potentially work with what you have. worth a quick chat?",
        "tg_followup": f"hey [Name], following up — even a quick note on what {dex} runs on would help me tell you if there's a clean path to canonical recognition for {chain}. no pressure.",
        "li_connect": f"Hi [Name] — Vic at Protofire DAO. Curious what {chain}'s DEX runs on under the hood — there may be a clean path to canonical Uniswap DAO recognition. Worth a chat?",
        "li_first": f"Thanks for connecting, [Name]. Saw {observation} on {chain}. {hook}. Curious what it's built on — depending on the stack there may be a straightforward path to canonical Uniswap DAO recognition (aggregator prioritization + official badge). We've done this for BOB, Abstract, Nibiru. If it's already a Uniswap fork we can work with what you have. Worth a quick chat?",
        "li_followup": f"Hey [Name], no rush — if you can point me to {dex}'s docs or repo I can tell you quickly whether canonical recognition is on the table for {chain}. Happy either way.",
    }

# ---- CASE_4 message builder (no Safe, no Uniswap, TVL minimal -> Safe only) ----
def case4(chain, dex_observation, hook):
    return {
        "tg_cold": f"hey [Name], Vic from Protofire DAO. been following {chain} and had a look at the stack. {dex_observation}, but there's no Safe multisig on {chain}. at this stage the highest-leverage move is probably a proper Safe deployment — it's what signals to protocols, DAOs and bridges that a chain is serious, and it unlocks the kind of TVL that makes a DEX worth running. {hook}. we've deployed Safe for 130+ networks including Gnosis and others — fast to ship, low friction. open to a quick chat?",
        "tg_followup": f"hey [Name], following up on the Safe idea for {chain} — genuinely low-lift on our end, and it's the piece bridges/protocols look for first. worth a quick call?",
        "li_connect": f"Hi [Name] — Vic at Protofire DAO. For {chain}, a proper Safe multisig is probably the highest-leverage next step to signal you're serious. Open to a chat?",
        "li_first": f"Thanks for connecting, [Name]. Had a look at {chain} — {dex_observation}, but there's no Safe multisig on {chain}. At this stage a proper Safe is the move: it's what protocols, DAOs and bridges look for, and it unlocks the TVL that makes a DEX worth running. {hook}. We've deployed Safe for 130+ networks — fast, low friction. Open to a quick chat?",
        "li_followup": f"Hey [Name], no pressure — the Safe deploy is quick and low-cost, and it's usually the unlock for the next stage of an ecosystem. Here whenever you want to scope it.",
    }

# ---- CASE_3 message builder (no Safe, no Uniswap, TVL meaningful -> Safe first, Uniswap next) ----
def case3(chain, dex_observation, hook):
    return {
        "tg_cold": f"hey [Name], Vic from Protofire DAO. looked at {chain}'s stack before messaging. two things stand out: {dex_observation}, and I couldn't confirm a Safe on the chain. with the TVL you've built on {chain}, Safe is honestly the first thing — it's what blue-chip protocols and DAOs require before they deploy on a chain. once that's in, a canonical Uniswap v3 is the natural next step to activate that liquidity. {hook}. we've deployed Safe for 130+ networks and Uniswap v2+v3 for BOB, Mode, Abstract, Zora. want to connect our teams?",
        "tg_followup": f"hey [Name], circling back — given the TVL you've built on {chain}, the Safe piece is quick to ship and unblocks the institutional side. worth 15 min?",
        "li_connect": f"Hi [Name] — Vic at Protofire DAO. Noticed {chain} has real TVL but no Safe multisig yet; that's usually the first blocker for bigger protocols. Worth a chat?",
        "li_first": f"Thanks for connecting, [Name]. Looked at {chain} — {dex_observation}, and I couldn't confirm a Safe on the chain. With the TVL you've built on {chain}, Safe is the first thing blue-chip protocols/DAOs check for. {hook}. Then a canonical Uniswap v3 activates that liquidity. We've done Safe for 130+ chains and Uniswap for BOB, Mode, Zora. Open to connecting teams?",
        "li_followup": f"Hey [Name], no rush — the Safe deployment is low-friction and tends to unlock the TVL that makes the DEX worth running. Happy to scope it whenever.",
    }

# ---- CASE_1 message builder (Safe already ours, no Uniswap -> warm Uniswap pitch) ----
def case1(chain, hook):
    return {
        "tg_cold": f"hey [Name], Vic here from Protofire — we deployed Safe for {chain} a while back. been looking at your stack and noticed you don't have a canonical Uniswap DEX yet. {hook}. your LPs and market makers need a proper interface — and aggregators like 1inch prioritize chains with a canonical Uniswap v3. we've deployed Uniswap v2+v3 for BOB, MODE, Abstract, Zora and 10+ others — full stack, not just contracts. two UI options: whitelabel on your domain or shared. usually 2–4 weeks. want to connect our teams?",
        "tg_followup": f"hey [Name], circling back on the Uniswap idea for {chain} — since we already run your Safe, adding a canonical v2+v3 is a natural next step. want me to send a quick scope?",
        "li_connect": f"Hi [Name] — Vic at Protofire DAO. We deployed Safe for {chain} a while back; noticed there's no canonical Uniswap DEX yet. That's usually the next unlock. Worth a chat?",
        "li_first": f"Thanks for connecting, [Name]. We deployed Safe for {chain} a while back, and noticed you don't have a canonical Uniswap DEX yet. {hook}. Aggregators like 1inch prioritize chains with a canonical Uniswap v3, and your LPs need a proper interface. We've deployed Uniswap v2+v3 for BOB, MODE, Abstract, Zora and 10+ others — full stack, whitelabel or shared UI, ~2–4 weeks. Want to connect our teams?",
        "li_followup": f"Hey [Name], no rush — since we already run your Safe, layering a canonical Uniswap on top is low-friction on our end. Happy to scope it whenever.",
    }

# ---- CASE_2 message builder (Safe exists not ours, no Uniswap -> cold Uniswap pitch) ----
def case2(chain, hook):
    return {
        "tg_cold": f"hey [Name], Vic from Protofire DAO — we build core infra for EVM chains. had a look at {chain}'s stack — you've got Safe covered, but no canonical Uniswap DEX yet. {hook}. without one, your swap volume is leaking to other chains and your LPs don't have a proper interface to manage positions. we deploy Uniswap v2+v3 end-to-end — contracts, routing API, graph node, frontend, and the canonical DAO governance proposal that gets your DEX officially recognized. done this for BOB, MODE, Abstract, Zora and others. whitelabel on your domain or shared UI — 2–4 weeks either way. open to a quick sync?",
        "tg_followup": f"hey [Name], following up on the Uniswap idea for {chain} — end-to-end deploy on our side, and it plugs the swap-volume leak. worth a quick call?",
        "li_connect": f"Hi [Name] — Vic at Protofire DAO. {chain} has Safe covered but no canonical Uniswap DEX yet; that's usually where swap volume leaks. Worth a chat?",
        "li_first": f"Thanks for connecting, [Name]. Had a look at {chain} — you've got Safe covered, but no canonical Uniswap DEX yet. {hook}. We deploy Uniswap v2+v3 end-to-end — contracts, routing API, graph node, frontend, plus the canonical DAO proposal that gets it officially recognized. Done this for BOB, MODE, Abstract, Zora. Whitelabel or shared UI, ~2–4 weeks. Open to a quick sync?",
        "li_followup": f"Hey [Name], no rush — the Uniswap deploy is end-to-end on our side and tends to stop the swap-volume leak to other chains. Here whenever you want to scope it.",
    }

BUILDERS = {"CASE_1": case1, "CASE_2": case2, "CASE_3": case3, "CASE_4": case4, "CASE_5": case5, "CASE_6": case6}

# DATA entries are appended by a separate data module for clarity.
