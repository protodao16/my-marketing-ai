import csv

# Dead networks
DEAD = {
    "Rari": "Shut down 2024",
    "re.al": "Shut down June 2025",
    "Milkomeda A1": "Milkomeda wound down 2024",
    "Tombchain": "Defunct",
    "Kekchain": "Abandoned meme chain",
    "Nahmii": "Inactive since 2023",
    "Boba_Bnb": "Boba BNB sunset",
    "Empire": "Abandoned",
    "Tenet": "Defunct 2024",
}

UNCERTAIN = {
    "Bitnet", "ETHF", "DSC", "ALV", "Genesys", "MEER", "Elysium",
    "Dexit", "Zeniq", "MultiVAC", "RSS3", "Bahamut",
    "Lung", "Ubiq", "ZYX", "Polis", "GoChain", "HPB",
    "Hoo", "REIchain", "Nova Network", "Pego", "Darwinia",
    "ENULS", "Loop", "MUUCHAIN", "Bitindi", "Vision",
    "JBC", "Omax", "Step", "Bitrock",
}

# Network context for message customization
# (ecosystem_tag, custom_middle_line_Safe_UniV3, custom_middle_line_UniV3, custom_middle_line_Canonical)
CONTEXT = {
    "AILayer":        ("AI infra L1",
                       "thought both could be useful here, Safe for protocol and team multisigs, Uniswap V3 for real LP depth, both are what Tier-1 protocols check before building on a new AI chain",
                       "with your AI infra positioning a canonical Uniswap V3 would attract real LPs and market makers and give developers a reliable liquidity layer",
                       None),
    "Ham":            ("Base ecosystem L2",
                       "thought both could be useful here, Safe for team and protocol multisigs, Uniswap V3 for concentrated liquidity, both are standard infrastructure for Base ecosystem chains",
                       "with your Base ecosystem positioning a canonical Uniswap V3 would give protocols a reliable liquidity primitive",
                       None),
    "LUKSO":          ("NFT and creator economy L1",
                       "thought both could be useful here, Safe for creator and DAO treasuries, Uniswap V3 for real token liquidity, both are what protocols usually look for before building on a creator-focused chain",
                       "with your NFT and creator economy focus a canonical Uniswap V3 would give LSP token pairs proper liquidity depth",
                       None),
    "Genesys":        ("EVM L1",
                       "thought both could be a good fit, Safe for team multisigs and protocol treasuries, Uniswap V3 as the standard AMM layer",
                       "a canonical Uniswap V3 would be the standard AMM layer protocols expect to find",
                       None),
    "BounceBit":      ("BTC restaking L1",
                       None,
                       None,
                       "means your pools won't show up in the official Uniswap interface and aggregators like 1inch tend to deprioritize non-canonical pools when routing BTC restaking liquidity"),
    "Endurance":      ("gaming L1 (ACE ecosystem)",
                       "thought both could fit well here, Safe for studio and protocol treasuries, Uniswap V3 as the liquidity layer game tokens need, both are what studios usually check before building on a gaming chain",
                       "with your gaming ecosystem focus a canonical Uniswap V3 would give game tokens proper liquidity and attract market makers",
                       None),
    "Planq":          ("Cosmos EVM L1",
                       "thought both could be useful here, Safe for team multisigs and DAO treasuries, Uniswap V3 for concentrated liquidity, standard infra for any growing Cosmos EVM chain",
                       "a canonical Uniswap V3 would give the ecosystem a proper concentrated liquidity layer",
                       None),
    "Ancient8":       ("Web3 gaming L2",
                       "thought both could work well here, Safe for game studio and protocol multisigs, Uniswap V3 for in-game token liquidity, both are what studios check before committing to a gaming L2",
                       "with your gaming L2 focus a canonical Uniswap V3 would give in-game tokens real liquidity depth",
                       None),
    "HAQQ":           ("Islamic finance L1",
                       "thought both could be a strong fit here, Safe for halal-compliant treasury management, Uniswap V3 as a transparent liquidity layer, both are what Islamic DeFi protocols look for",
                       "with your Islamic finance positioning a canonical Uniswap V3 would add a transparent and widely trusted liquidity layer",
                       None),
    "RSS3":           ("social and content protocol",
                       "thought both could be useful here, Safe for protocol and DAO treasuries, Uniswap V3 for token liquidity, standard infra for a social protocol expanding into DeFi",
                       "a canonical Uniswap V3 would give RSS3 token pairs proper liquidity routing",
                       None),
    "DeFiChain EVM":  ("Bitcoin-backed DeFi L1",
                       "thought both could be a great fit here, Safe for protocol multisigs, Uniswap V3 as a concentrated liquidity layer on top of Bitcoin-backed assets",
                       "with your Bitcoin-backed DeFi focus a canonical Uniswap V3 would give the EVM side proper liquidity depth that VanillaSwap can't match alone",
                       None),
    "Bahamut":        ("PoSA EVM L1",
                       "thought both could be a good fit, Safe for team and protocol treasuries, Uniswap V3 as the standard concentrated liquidity layer",
                       "a canonical Uniswap V3 would add a reliable liquidity layer on top of what you have",
                       None),
    "Immutable zkEVM":("gaming and NFT zkEVM",
                       None,
                       "with your gaming and NFT focus a canonical Uniswap V3 would attract DeFi protocols and market makers that Quickswap alone can't pull",
                       None),
    "Q Protocol":     ("governance-focused EVM L1",
                       "thought both could be a strong fit, Safe as the standard for DAO and governance multisigs, Uniswap V3 as the liquidity layer protocols building on Q would expect",
                       "a canonical Uniswap V3 would give the Q ecosystem a trusted liquidity layer that governance protocols can build around",
                       None),
    "inEVM":          ("Injective EVM layer",
                       None,
                       None,
                       "means your pools won't show up in the official Uniswap interface and aggregators tend to deprioritize non-canonical pools when routing Injective ecosystem liquidity"),
    "DeFiVerse":      ("Oasys gaming L1",
                       "thought both could fit well here, Safe for game studio multisigs, Uniswap V3 as the liquidity layer gaming tokens need",
                       "with your Oasys gaming focus a canonical Uniswap V3 would give game tokens a proper liquidity layer",
                       None),
    "Bitrock":        ("fast EVM L1",
                       "thought both could work here, Safe for team and protocol multisigs, Uniswap V3 as the standard AMM layer",
                       "a canonical Uniswap V3 would be the standard AMM layer protocols expect",
                       None),
    "AirDAO":         ("community EVM L1",
                       "thought both could be a good fit, Safe for team and DAO treasuries, Uniswap V3 for real LP depth, both are standard infra for a growing community chain",
                       "a canonical Uniswap V3 would give the AirDAO ecosystem proper token liquidity",
                       None),
    "Horizen EON":    ("Horizen EVM sidechain",
                       None,
                       None,
                       "means your pools won't show up in the official Uniswap interface and aggregators tend to deprioritize non-canonical pools when routing"),
    "Bifrost Network":("cross-chain staking L1",
                       "thought both could be a strong fit here, Safe for protocol and validator multisigs, Uniswap V3 for staking derivative liquidity",
                       "with your cross-chain staking focus a canonical Uniswap V3 would give LSDs proper liquidity depth on the EVM side",
                       None),
    "Dexalot":        ("orderbook DEX subnet (Avalanche)",
                       "thought both could be a good fit, Safe for team and protocol multisigs, Uniswap V3 as a complementary AMM layer alongside your orderbook",
                       "a canonical Uniswap V3 alongside your orderbook would attract LPs looking for passive yield",
                       None),
    "Beam":           ("gaming L1 (Merit Circle)",
                       None,
                       None,
                       "means your pools won't show up in the official Uniswap interface and aggregators tend to deprioritize non-canonical pools, which matters for a gaming chain where token liquidity is key"),
    "Kroma":          ("Ethereum L2",
                       None,
                       None,
                       "means your pools won't show up in the official Uniswap interface and aggregators like 1inch tend to deprioritize non-canonical pools when routing"),
    "Aura Network":   ("Cosmos NFT and gaming chain",
                       "thought both could be a good fit, Safe for DAO and protocol multisigs, Uniswap V3 for token liquidity on the EVM side",
                       "with your NFT and gaming focus a canonical Uniswap V3 would give EVM-side tokens proper liquidity",
                       None),
    "Rollux":         ("Bitcoin L2 (Syscoin)",
                       None,
                       None,
                       "means your pools won't show up in the official Uniswap interface and aggregators tend to deprioritize non-canonical pools when routing Bitcoin L2 liquidity"),
    "Oasys":          ("gaming-focused L1",
                       "thought both could fit well here, Safe for game studio and protocol multisigs, Uniswap V3 as the liquidity layer gaming tokens need",
                       "with your gaming L1 positioning a canonical Uniswap V3 would give in-game tokens real depth and attract market makers",
                       None),
    "Crab":           ("Darwinia canary network",
                       "thought both could be a good fit here, Safe for team multisigs, Uniswap V3 as the standard liquidity layer",
                       "a canonical Uniswap V3 would give the Crab ecosystem a proper AMM layer",
                       None),
    "Cube":           ("gaming EVM L1",
                       "thought both could work well here, Safe for game studio multisigs, Uniswap V3 for in-game token liquidity",
                       "with your gaming focus a canonical Uniswap V3 would give the Cube ecosystem real LP depth",
                       None),
    "Ultron":         ("DeFi-focused L1",
                       None,
                       "with your DeFi focus a canonical Uniswap V3 would give the ecosystem proper concentrated liquidity on top of what iZiSwap provides",
                       None),
    "Bifrost":        ("Polkadot parachain",
                       "thought both could be a strong fit, Safe for protocol and DAO multisigs, Uniswap V3 for liquid staking derivative liquidity",
                       "with your LSD focus a canonical Uniswap V3 would give vDOT and other LSDs proper liquidity depth on the EVM side",
                       None),
    "CLV":            ("Polkadot EVM parachain",
                       "thought both could work well here, Safe for protocol and team multisigs, Uniswap V3 as the standard concentrated liquidity layer",
                       "a canonical Uniswap V3 would give CLV a proper liquidity layer for DeFi protocols to build on",
                       None),
    "REI":            ("lightweight EVM L1",
                       "thought both could be a good fit, Safe for team and DAO multisigs, Uniswap V3 for real LP depth",
                       "a canonical Uniswap V3 would give REI Network a trusted liquidity layer protocols expect",
                       None),
    "Acala":          ("Polkadot DeFi hub",
                       "thought both could be a strong fit, Safe for DAO and protocol multisigs, Uniswap V3 for deep EVM-side liquidity",
                       "with your DeFi hub positioning a canonical Uniswap V3 would bring concentrated liquidity that Acala Swap can't provide",
                       None),
    "OntologyEVM":    ("Ontology EVM layer",
                       None,
                       "with your DID and data focus a canonical Uniswap V3 would give the EVM ecosystem a trusted liquidity layer on top of what iZiSwap provides",
                       None),
    "Lachain":        ("LatAm-focused EVM L1",
                       "thought both could be a great fit, Safe for local protocol and team multisigs, Uniswap V3 as the liquidity layer LatAm DeFi projects expect",
                       "with your LatAm focus a canonical Uniswap V3 would give the ecosystem a trusted liquidity layer",
                       None),
    "Hydra":          ("PoS EVM chain",
                       None,
                       None,
                       "means your pools won't show up in the official Uniswap interface and aggregators tend to deprioritize non-canonical pools when routing"),
    "DFK":            ("DeFi Kingdoms gaming chain",
                       "thought both could fit well, Safe for in-game treasury and DAO multisigs, Uniswap V3 as the standard liquidity layer game tokens need",
                       "with your gaming and DeFi focus a canonical Uniswap V3 would give JEWEL and other tokens proper liquidity depth",
                       None),
    "Syscoin":        ("Bitcoin UTXO + EVM L1",
                       "thought both could be a good fit, Safe for team and protocol multisigs, Uniswap V3 as the standard EVM liquidity layer",
                       "with your Bitcoin + EVM hybrid positioning a canonical Uniswap V3 would give the EVM side a trusted liquidity layer",
                       None),
    "Theta":          ("video and media L1",
                       "thought both could be useful here, Safe for content protocol and team multisigs, Uniswap V3 for token liquidity",
                       "with your media and streaming focus a canonical Uniswap V3 would give TFUEL and token pairs proper liquidity",
                       None),
    "CSC":            ("CoinEx Smart Chain",
                       "thought both could work well, Safe for exchange and protocol multisigs, Uniswap V3 for concentrated liquidity",
                       "a canonical Uniswap V3 would give CSC proper concentrated liquidity on top of what OneSwap and IFSwap provide",
                       None),
    "Callisto":       ("security-focused EVM L1",
                       "thought both could be a good fit, Safe for protocol and team multisigs, Uniswap V3 as the standard AMM layer",
                       "a canonical Uniswap V3 would give Callisto a proper concentrated liquidity layer",
                       None),
    "Godwoken":       ("Nervos CKB EVM layer",
                       "thought both could work well here, Safe for protocol and team multisigs, Uniswap V3 for concentrated liquidity",
                       "with your Nervos CKB positioning a canonical Uniswap V3 would give the EVM layer a standard liquidity primitive",
                       None),
    "Elastos":        ("SmartWeb EVM L1",
                       "thought both could be a good fit, Safe for DAO and protocol multisigs, Uniswap V3 for real LP depth",
                       "with your SmartWeb focus a canonical Uniswap V3 would give Elastos EVM proper liquidity depth",
                       None),
    "Ronin":          ("gaming L1 (Axie Infinity)",
                       None,
                       None,
                       "means your pools won't show up in the official Uniswap interface and aggregators like 1inch tend to deprioritize non-canonical pools when routing gaming liquidity"),
    "EnergyWeb":      ("energy sector EVM L1",
                       "thought both could be a strong fit, Safe for energy project and DAO multisigs, Uniswap V3 as the liquidity layer energy tokens and REC markets need",
                       "with your energy sector focus a canonical Uniswap V3 would give EWT and clean energy tokens proper liquidity",
                       None),
    "Palm":           ("NFT-focused EVM chain",
                       "thought both could work well, Safe for creator and protocol multisigs, Uniswap V3 for token liquidity on the NFT side",
                       "with your NFT focus a canonical Uniswap V3 would give PALM token pairs proper liquidity routing",
                       None),
    "Fusion":         ("cross-chain DeFi L1",
                       "thought both could be a good fit, Safe for team and DAO multisigs, Uniswap V3 as a standard AMM layer",
                       "with your cross-chain DeFi focus a canonical Uniswap V3 would complement Chainge Finance with proper concentrated liquidity",
                       None),
    "Karura":         ("Acala canary network on Kusama",
                       "thought both could work well here, Safe for DAO and protocol multisigs, Uniswap V3 for real EVM-side liquidity depth",
                       "with your Kusama DeFi positioning a canonical Uniswap V3 would give the EVM side a trusted liquidity layer",
                       None),
    "Energi":         ("PoS EVM L1 with treasury",
                       "thought both could be a good fit, Safe for treasury and DAO multisigs, Uniswap V3 as the standard AMM layer",
                       "with your treasury-focused model a canonical Uniswap V3 would give NRG proper liquidity depth",
                       None),
    "Bitcoin":        ("Bitcoin mainnet",
                       None, None, None),  # Special case - skip
    "Onus":           ("Vietnamese DeFi L1",
                       "thought both could be a great fit, Safe for local protocol and team multisigs, Uniswap V3 as the standard AMM layer for a growing Southeast Asian chain",
                       "with your Southeast Asian DeFi focus a canonical Uniswap V3 would give ONUS ecosystem tokens proper liquidity",
                       None),
    "Polis":          ("PoS EVM L1",
                       "thought both could work well, Safe for team and DAO multisigs, Uniswap V3 as the standard concentrated liquidity layer",
                       "a canonical Uniswap V3 would give Polis a proper AMM layer",
                       None),
    "Pego":           ("high-throughput EVM L1",
                       "thought both could be a good fit, Safe for team and protocol multisigs, Uniswap V3 as the standard concentrated liquidity layer",
                       "a canonical Uniswap V3 would give Pego a trusted liquidity layer",
                       None),
}

# Default context for networks not in CONTEXT
DEFAULT_CONTEXT = {
    "Safe+UniV3": "thought both could be a good fit here, Safe for team and protocol multisigs, Uniswap V3 for real LP depth, both are what Tier-1 protocols usually check before building on a new chain",
    "UniV3": "a canonical Uniswap V3 would give the ecosystem proper concentrated liquidity and attract market makers",
    "Canonical UniV3": "means your pools won't show up in the official Uniswap interface and aggregators tend to deprioritize non-canonical pools when routing",
}

def get_dex_name(dexs_str):
    """Get first DEX name for message"""
    return dexs_str.split(',')[0].strip()

def build_message(net, offer, dexs, tvl, safe_pf, safe_ex, context_data):
    if not context_data or context_data[0] is None:
        # skip Bitcoin etc
        if net == "Bitcoin":
            return "N/A - Bitcoin mainnet, Safe/Uniswap V3 not applicable"

    ctx = CONTEXT.get(net)

    if offer == "Safe+UniV3":
        middle = (ctx[1] if ctx and ctx[1] else DEFAULT_CONTEXT["Safe+UniV3"])
        dex_line = f"looked at {net}'s DeFi setup, {get_dex_name(dexs)} is the only DEX and no Safe multisig yet" if dexs.count(',') == 0 else f"looked at {net}'s DeFi setup, {dexs} are the DEXes there and no Safe multisig yet"
        msg = (
            f"hey Name, Vic from Protofire, trusted Safe & Uniswap partner\n\n"
            f"{dex_line}\n\n"
            f"{middle}\n\n"
            f"we've done Safe on 140+ networks and Uniswap V3 for BOB, Abstract, Mode, open to connecting teams on a group chat here?"
        )

    elif offer == "UniV3":
        dex_count = len([d for d in dexs.split(',') if d.strip()])
        middle = (ctx[2] if ctx and ctx[2] else DEFAULT_CONTEXT["UniV3"])
        dex_line = f"looked at {net}'s DEX setup, {get_dex_name(dexs)} is running but no Uniswap V3 yet" if dex_count == 1 else f"looked at {net}'s DEX setup, {dexs} are running but no Uniswap V3 yet"
        msg = (
            f"hey Name, Vic from Protofire, trusted Safe & Uniswap partner\n\n"
            f"{dex_line}\n\n"
            f"{middle}\n\n"
            f"we've deployed canonical v3 for BOB, Abstract, Mode, thought we could do the same for {net}, open to connecting teams on a group chat here?"
        )

    elif offer == "Canonical UniV3":
        v3_dex = get_dex_name(dexs)
        # find V3 dex
        for d in dexs.split(','):
            if 'V3' in d or 'v3' in d:
                v3_dex = d.strip()
                break
        middle = (ctx[3] if ctx and ctx[3] else DEFAULT_CONTEXT["Canonical UniV3"])
        msg = (
            f"hey Name, Vic from Protofire, trusted Safe & Uniswap partner\n\n"
            f"noticed {net}'s {v3_dex} is live but not a canonical Uniswap deployment, {middle}\n\n"
            f"we've deployed canonical v3 on BOB, Abstract, Mode, thought we could handle the migration for {net} cleanly, open to connecting teams on a group chat here?"
        )

    return msg


with open('/root/.claude/uploads/659137d7-bddf-59d5-9b98-94d40d245789/9b39590b-W3_node_Leadgen__Sheet69.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

fieldnames = [
    'Network','Status','Offer','Chain_ID','DEXs','DEXs_count',
    'Protocols','Launch_Date','TVL','safe_protofire','safe_exists',
    'Message_Draft','Notes'
]

with open('/home/user/my-marketing-ai/leads_cohort_final_v2.csv', 'w', newline='') as out:
    writer = csv.DictWriter(out, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    for row in rows:
        net = row['Network'].strip()
        safe_pf = row['safe_protofire'].strip()
        safe_ex = row['safe_exists'].strip()
        dexs = row['DEXs'].strip()
        tvl = row['TVL'].strip()

        if net in DEAD:
            status = f"DEAD - {DEAD[net]}"
        elif net in UNCERTAIN:
            status = "Uncertain - verify"
        else:
            status = "Active"

        has_v3_fork = 'V3' in dexs or 'v3' in dexs
        already_safe = safe_pf == 'YES'
        has_safe = safe_ex == 'YES'

        if already_safe and has_v3_fork:
            offer = "Canonical UniV3"
        elif already_safe:
            offer = "UniV3"
        elif has_safe and has_v3_fork:
            offer = "Canonical UniV3"
        elif has_safe:
            offer = "UniV3"
        else:
            offer = "Safe+UniV3"

        ctx = CONTEXT.get(net, (None, None, None, None))
        if 'DEAD' in status or net == 'Bitcoin':
            msg = f"N/A - {status}"
        else:
            msg = build_message(net, offer, dexs, tvl, safe_pf, safe_ex, ctx)

        writer.writerow({
            'Network': net,
            'Status': status,
            'Offer': offer,
            'Chain_ID': row['Chain ID'].strip(),
            'DEXs': dexs,
            'DEXs_count': row['DEXS number'].strip(),
            'Protocols': row['Protocols number'].strip(),
            'Launch_Date': row['Launch date'].strip(),
            'TVL': tvl,
            'safe_protofire': safe_pf,
            'safe_exists': safe_ex,
            'Message_Draft': msg,
            'Notes': row['Comments'].strip(),
        })

print("Done")
