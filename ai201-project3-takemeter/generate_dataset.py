import csv
import random

# Evidence-based posts - include reasoning, numbers, company names
evidence_based = [
    "Apple's services division is growing at 12% YoY and carries 70% margins. With 2B+ installed base, recurring revenue becomes increasingly predictable. That's why AAPL trades at premium valuation despite mature hardware sales.",
    "Looking at Microsoft's cloud growth: Azure up 29% last quarter. Enterprise spending on AI infrastructure will benefit MSFT disproportionately given their OpenAI partnership and Copilot integration across Office suite.",
    "Tesla's factory in Berlin produces 600k vehicles annually at lower cost than Fremont. Elon's margin expansion strategy is working - gross margins returned to 25% despite price cuts.",
    "JPMorgan's net interest margin compressed 15bps YoY due to deposit flight. Unless rates stay elevated, their 2024 earnings growth is limited. Compare this to Wells Fargo who's better positioned with diversified revenue.",
    "Nvidia's data center revenue is 88% of total now, up from 67% two years ago. This concentration risk is real, but the TAM for AI compute is expanding 40% annually. Valuations should reflect that growth rate.",
    "Berkshire reduced Apple holdings by 50% to $84.7B. Buffett doesn't move that much cash without conviction. Says something about valuations at 30x earnings.",
    "Eli Lilly's GLP-1 drug sales hit $6.9B in 2024, growing 150% YoY. Market is pricing in obesity + diabetes addressable market expansion. Realistic CAGR probably 20-25%, not the 40% some bulls assume.",
    "Costco's renewal rate hit 90.5%, highest on record. When membership moat strengthens and consumer defensibility improves, long-term returns compound. Price target upgrade justified.",
    "Broadcom's gross margins are 73%, up from 68% three years ago. Their fab partnerships with TSMC and Samsung create supply resilience competitors lack. This structural advantage gets underpriced.",
    "Meta's AI training costs are $50B+ annually but represent 18% of revenue. Compare to Alphabet's training spend at 12% of revenue. Meta's capex heavy strategy might pay off in AI models.",
    "UnitedHealth's optum medical loss ratio of 83.2% is expanding. Healthcare inflation outpacing their pricing power. Margin compression likely continues unless they unlock synergies.",
    "Boeing's 737 MAX issues cost them $900M so far. But 5,000+ planes on backlog at $130M average suggests $650B revenue pipeline. Recovery thesis has legs once quality improves.",
    "Vanguard's ETF flows are $500B+, eating into active management. Illustrates decade-long shift to passive. Companies with strong moats benefit more from this wind.",
    "AMD gained 3.5 points of server CPU market share in 6 months. EPYC success is real. Intel's 18A node delays compound the problem.",
    "Shopify's operating leverage is finally showing. FCF positive at $3.4B annualized on $6.7B revenue. SaaS multiples might be decompressing too much.",
    "Pfizer's drug pipeline has 40+ programs in late stage. Peak sales of Comirnaty declining but oncology portfolio is strong. Valuation reflects pharma maturity, not growth.",
    "GE's separation of energy, healthcare, and aviation is unlocking value. Each division trades at discount combined. Patient realization of breakup thesis.",
    "Visa processes $15T in payment volume annually, growing 8% YoY. Pricing power remains intact with 0bps of competitive pressure. Why growth multiples compressed mystifies me.",
    "Domino's unit economics show 8% average unit volume growth despite pizza commoditization. Franchise model + delivery data moat = pricing power.",
    "Intel's gross margins fell to 41% from 56% in 2019. Foundry Services losses are structural until they fix manufacturing. Pure-play foundry comparison to TSMC doesn't hold.",
    "Mastercard's network growth compounds at 11% CAGR. Emerging markets exposure gives them 40% growth tailwind that Visa lacks. Valuation gap should exist.",
    "XOM's downstream margins are 6%, upstream 35%. Oil prices fell 20% but midstream collected stable EBITDA. Integrated energy model provides buffer.",
    "Adobe's SaaS transition complete - 96% of revenue is subscription now. Customer lifetime value expanded 18% YoY. Digital transformation tailwind continues.",
    "Starbucks' China comparable sales declined 3% last quarter but margin expansion offset it. Mature market dynamics show in comps, not in profitability.",
    "Accenture's consulting backlog exceeds $25B with 4-year conversion. Digital + cloud services represent 45% of revenue, growing 18% CAGR.",
    "Stripe's latest valuation at $95B suggests 6x revenue multiple. Compare to Paypal at 1.8x. Payment rail differentiation matters to investors.",
    "Netflix churn rate below 2.2% and ARPU growing 8% drives margin expansion. Crackdown on password sharing added 7M subs that weren't obvious.",
    "Realty Income's AFFO per share grew 5% YoY on same-store sales growth of 2.3%. REIT discount to NAV isn't justified given Moody's upgrade.",
    "Squarespace's gross margin improved 150bps YoY to 78% while investing in AI. Unit economics inflection justifies growth multiple.",
    "SentinelOne's 95% net dollar retention and 45% gross margins are enterprise software gold standards. Cybersecurity spending survives recessions.",
    "Zelensky banned the export of Bitcoin mined in Ukraine. Creates supply shock implications for any Bitcoin reserve thesis. Regulatory risk escalating.",
    "Warren Buffett's $189B cash pile signals bearish conviction. If Buffett sees attractive entry points disappearing, retail investors should listen.",
    "Citrix settled with activist for board seats. Management + technology refresh needed. Valuation at 0.8x sales seems low for hybrid work beneficiary.",
    "Applied Materials' capital equipment sales fell 20% but gross margins held at 48%. China restrictions create headwind but not existential.",
    "SolarWinds' zero-trust architecture improvements post-hack give them competitive moat. Insider threat becomes market differentiator.",
    "Unity's loss of Elon's confidence after pricing changes accelerated Epic integration. Less diversification risk than many think.",
    "Okta's identity platform processes 15B authentications daily. Enterprise software defensibility through integration lock-in is real.",
    "Ping Identity's federation model competes with Okta on API depth. Market size supports 2-3 winners. Not a zero-sum game.",
    "Datadog's platform breadth - 5 product pillars - makes them sticky. 3-year net retention rate of 140% reflects that.",
    "Crowdstrike's Falcon platform achieved 47% gross margins at scale. Cybersecurity budgets immune to recession.",
    "Palo Alto Networks' shift to platform revenue (68% of total) changes margin profile. Pure-play security comparison no longer applies.",
    "Zscaler's zero-trust networking disrupts traditional network security. $1B+ TAM in traffic inspection alone.",
    "Fortinet's FortiGate appliances own the SMB firewall market. Market saturation real but ZTNA pivot offers growth.",
    "Snowflake's consumption model provides visibility into customer demand. This quarter's usage beats guidance by 12%.",
    "Databricks raised at $43B valuation without IPO. If private unicorns trade at 15x sales post-IPO, unpriced value exists.",
    "Figma's 150M DAUs and 30% revenue growth justifies premium valuation. Design tooling switching costs are high.",
    "Canva's design-for-everyone thesis captures SMB market Figma ignores. Different TAMs, not competing directly.",
    "Notion's workspace database expansion competes with traditional CRM. Enterprise adoption accelerating.",
    "Monday.com's 97% net dollar retention shows work OS category adoption deepening. Not just project management anymore.",
    "HubSpot's verticalization strategy - bringing CRM+operations to agencies - works. Vertical SaaS outperforms horizontal.",
    "Salesforce's Slack integration finally drove user growth acceleration. Ecosystem moat expanding.",
    "Workday's HCM + financials stack prevents rip-and-replace. Cloud ERP adoption justified at premium multiples.",
    "ServiceNow's workflow automation extends beyond IT ops. Platform TAM expands beyond $100B available market.",
    "CrowdStrike's module attachment rate of 2.4 per customer suggests expansion upside. Platform strategy rewarding discipline.",
    "Upland Software's acquisition strategy consolidates disparate tools. Private equity playbook applied to SaaS consolidation.",
    "Tyler Technologies' government SaaS has 35%+ margins. Moat from complex integrations + switching costs massive.",
    "Veeva's life sciences focus - pharma + biotech - has no real competition. Vertical domination justified.",
    "Model N's pricing optimization software captures 5-10% of deal value. Enterprise economics strong.",
    "Alteryx's low-code analytics platform sees enterprise demand. Self-serve analytics doesn't replace their use case.",
    "Palantir's 12-year customer relationships and $5B revenue base show stickiness. Government + commercial mix validates model.",
    "RealPage's property management software has 95%+ retention. Switching costs in multifamily real estate incredibly high.",
    "Blackline's close automation platform has 85% gross margins. Finance operations outsourcing is permanent trend.",
    "Bill.com's bills + payments integration captures SMB pain point. Network effects real as customers expand usage.",
    "Paylocity's payroll + HR stack competes in $20B SMB market. Vertical integration rewarded in HR tech.",
    "ADP's 40M+ payrolls represent 40% of US market. Switching costs from decade-old integrations massive.",
    "Paychex's payroll focus (vs ADP's benefits breadth) outperforms. Simplicity + reliability outweighs feature richness for SMB.",
    "Paycom's employee self-service model reduces HR labor 30%. Tangible ROI drives net dollar retention of 105%.",
    "Insperity's co-employment model captures liability + compliance risk. Market consolidation ongoing.",
    "TriNet's PEO model serves 300K+ employees across clients. Bundled HR + benefits + compliance sticky.",
    "Workiva's platform consolidates regulatory reporting across ESG + financials. Compliance spending recession-proof.",
]

# Speculative takes - predictions, price targets, buy/sell calls
speculative_take = [
    "Tesla hits $300 by 2026. Elon's FSD narrative has shifted from aspirational to realistic. Insurance data will break bearish narrative.",
    "NVDA crashes 40% when AI hype resets. A100s are obsolete, H100 margins compress, and everyone builds custom silicon. Valuation isn't prepared.",
    "Apple will trade at $150 in 12 months. Services growth stalls without new hardware category. Tim Cook's capital allocation doesn't inspire.",
    "Microsoft becomes a $4T company on Copilot monetization alone. Enterprise lock-in + AI integration = margin explosion.",
    "Amazon Web Services breaks 35% operating margin by 2026. Generative AI workloads are pure software margin expansion.",
    "Meta's metaverse bet finally shows returns in 2027. $30B investment pays off when VR adoption follows mobile trajectory.",
    "Broadcom rallies to $800. Networking TAM expansion plus memory supply constraints keep their ASP elevated.",
    "Intel returns to 15% gross margins by 2028 when Foundry Services hit scale. Geopolitical support + technology recovery.",
    "AMD takes 60% server CPU share, pushing Intel below $20. Process advantage is permanent, not temporary.",
    "Oracle's cloud pivot results in stock doubling. Databases + infrastructure AI = unbeatable stack.",
    "Salesforce trades at $250 again. Slack integration drives CRM stickiness higher than management admits.",
    "Adobe becomes a $400B company when Firefly monetization kicks in. Generative AI in creative workflows changes industry economics.",
    "Shopify becomes the top payment processor, crushing Stripe valuation. They own the SMB merchant, the data is theirs.",
    "Netflix hits $300 ARPU by 2030 through advertising + password sharing fees. Content cost leverage + less churn.",
    "Roblox hits $100 in revenue when creator economy monetization accelerates. User-generated content becomes mainstream.",
    "Figma's valuation justifies $50B exit. Design tools → business logic → design OS category winner.",
    "Notion becomes a $200B company. Workspace database becomes productivity OS, competes with Microsoft.",
    "Discord sells for $50B, Spotify at $600B. Creator economy consolidation phase 2 starts.",
    "Cloudflare hits $200 by 2027. DDoS + WAF becomes commodity but security analytics margins expand.",
    "Datadog becomes a $500B company. Observability stack → business intelligence → every company needs unified platform.",
    "CrowdStrike becomes top cybersecurity vendor, VMware integration drives $400B valuation. Platform consolidation wins.",
    "Palo Alto Networks breaks $100B market cap. Complete platform migration from point products reshapes industry.",
    "Zscaler replaces traditional firewalls entirely by 2026. Zero-trust adoption inflects from early to mainstream.",
    "Okta becomes the identity OS, reaches $500B valuation. Enterprise software built on identity foundation.",
    "Twilio becomes the communication stack for every enterprise app. $200B TAM creates $300B+ valuation.",
    "SendGrid acquisition makes Twilio unstoppable in email-SMS-voice convergence. Sticky primitives.",
    "Stripe becomes the Payments AWS, unicorn unicorn stage. Global expansion + API completeness = $100B+ revenue.",
    "Block becomes a $150B company. Cash app + Square + TBD create fintech heavyweight.",
    "PayPal falls to $50 as crypto integration fails. Legacy payment rails disrupted by fintech natives.",
    "Affirm becomes the consumer credit standard. Buy now pay later TAM justifies $100B+ valuation.",
    "Klarna becomes fintech unicorn again after 2024 losses reverse. European BNPL leader resurgent.",
    "Upstart's AI underwriting beats traditional lenders. Stock returns 300% as credit losses prove edge.",
    "SoFi becomes the millennial bank, hits $50B valuation. Products stick, lending economics improve.",
    "Robinhood goes to $150 per share. Crypto volatility + options trading drives commission expansion.",
    "Coinbase becomes the Bitcoin proxy, reaches $200B market cap. Institutional adoption accelerates.",
    "MicroStrategy becomes a Bitcoin proxy, MSTR hits $700. Macro inflation fears drive Bitcoin up 200%.",
    "Riot Blockchain becomes profitable at $3B market cap. Bitcoin mining economics work at $60k BTC.",
    "Mara takes over as Bitcoin miner leader. Production efficiency + capital raise strategy works.",
    "Dogecoin hits $1.00. Elon tweets, retail FOMO, technical factors align.",
    "Ethereum flips Bitcoin in market cap. Staking yields + DeFi adoption accelerates. Layer 2s provide scalability.",
    "Solana becomes the ETH killer, SOL hits $500. Developers migrate for speed + low fees.",
    "Arbitrum becomes the dominant rollup. Sequencer economics + developer grants create sticky ecosystem.",
    "Polygon becomes layer 1 replacement, MATIC hits $5. EVM equivalence + enterprise adoption.",
    "Chainlink becomes oracle monopoly, LINK hits $100. Every smart contract needs external data.",
    "Uniswap becomes cross-chain DEX leader, UNI hits $50. LP economics + governance align incentives.",
    "Aave becomes DeFi lending standard, AAVE hits $800. Risk management proves edge, Flash loans drive adoption.",
    "Maker becomes stablecoin benchmark, MKR hits $10k. DAI becomes settlement layer.",
    "Lido becomes staking standard, LDO hits $100. Validator fragmentation makes pooling dominant.",
    "Curve becomes stable asset central hub. CRV economics reward long-term governance.",
    "Balancer becomes portfolio rebalancing standard. BAL hits $50 on fee generation.",
    "Convex becomes Curve wrapper leader. CVX hits $200 on vote escrow dominance.",
    "Yearn becomes yield aggregation standard. YFI becomes $50k. Passive yield becomes mainstream.",
    "Alpaca Finance becomes leveraged farming leader. ALPACA hits $10. Liquidation resilience = product market fit.",
    "Compound becomes lending protocol leader again. COMP governance + risk management.",
    "dYdX becomes perpetual futures DEX killer. DYDX hits $50 on sovereign chain thesis.",
    "Jupiter becomes Solana swap leader. JUP gets to $5. Concentrated liquidity + routing wins.",
    "Magic Eden becomes NFT marketplace consolidator. ME hits $20. Digital scarcity narrative returns.",
    "OpenSea falls below $500M market cap. Competition + declining NFT volumes.",
    "Blur becomes NFT wash trading hub. BLUR stays <$1. Gamification doesn't fix fundamentals.",
    "Immutable becomes game NFT standard. IMX hits $3. Gaming adoption requires onchain assets.",
    "Axie Infinity becomes gaming breakout. AXS returns to $20. Scholarship model sustainability proven.",
    "Sandbox becomes metaverse leader. SAND hits $5. Enterprise land sales prove adoption.",
    "Decentraland fails to launch, MANA collapses to $0.10. Metaverse hype fades, users vanish.",
    "Arweave becomes permanent storage backbone. AR hits $100. Immutable data becomes valuable.",
    "Helium becomes the IoT network standard. HNT hits $50. Wireless coverage incentives work.",
    "Filecoin becomes decentralized AWS. FIL hits $200. Storage economics reward network growth.",
    "Render becomes GPU marketplace monopoly. RNDR hits $100. AI training compute demand explodes.",
    "Livepeer becomes live streaming standard. LPT hits $50. Transcoding economics create moat.",
    "Audius becomes music distribution disruptor. AUDIO becomes worthless. Spotify dominance inescapable.",
    "Sound becomes music NFT standard. SOUND hits $20. Artist economics improve.",
]

# Market reaction - emotional responses to market movements
market_reaction = [
    "Holy cow, the Fed just raised 25bps AGAIN. My portfolio is getting destroyed. Bonds never going back up and the yield curve is inverted.",
    "Market's down 3% today because of jobs report. Tech is getting crushed. Time to panic sell or double down?",
    "TSLA mooned on Elon's tweet. This is insane. Meme stock confirmation.",
    "AAPL breaking out above $200! Institutional money flowing in. Tech rally beginning!",
    "Recession fears mounting. Unemployment ticked up to 4.2%. Cash is king right now. Equities are dead.",
    "Powell's hawkish comments tanked the entire market at 2:45pm. Every sector red. Why do we even invest?",
    "Inflation data came in hotter than expected. Oil surging $5/bbl. Energy stocks flying.",
    "Nvidia reporting 200% earnings beat! This is the AI bottom we were waiting for.",
    "Crypto winter is over. Bitcoin breaking above $45k. Altseason incoming. Load up now.",
    "Housing data collapsed. Mortgage rates at 7%. Real estate market freezing.",
    "Jobs report crushed expectations with 300k new jobs. Fed staying hawkish longer. Tech destroyed.",
    "Earnings season starting strong but guidance is guiding down. Market doesn't care about growth.",
    "Chip shortage resolved. Semiconductor supply chain healing. Prices normalizing.",
    "Supply chain still a mess. Shipping costs up 50% YoY. Inflation isn't transitory.",
    "China lockdowns hitting global economy. Worst quarter since COVID.",
    "China reopening! Stimulus flowing, growth returns. Buy the dip.",
    "War in Europe escalating. Energy prices exploding. Stagflation incoming.",
    "War de-escalation hopes rising. Oil falling $8/bbl. Inflation pressure relieving.",
    "Crypto exchange imploded overnight. All deposits gone. Never again touching digital assets.",
    "SPY hit all time high today. This market is broken. Fundamentals don't matter.",
    "Circuit breakers tripped today. Market volatility exploding. VIX above 50.",
    "VIX crashed to 10. Complacency is back. Danger zone.",
    "Treasury yields inverted again. Recession signals flashing. Get to cash NOW.",
    "Yield curve normalized finally. Economic growth ahead. Rally continues.",
    "Credit spreads blowing out. Corporate bonds selling off. Default risk rising.",
    "Credit markets stable now. Risk-on trade accelerating. Equities should rally.",
    "EUR/USD at parity first time ever. Dollar strength crushing emerging markets.",
    "Yen collapsing against dollar. BOJ intervention coming. Currency chaos.",
    "Gold hitting new highs above $2200. Inflation expectations unanchored.",
    "Gold selling off hard. Fed credibility restored. Inflation story dead.",
    "Commodities rally explosive. Supercycle thesis confirmed. Own energy stocks.",
    "Commodity bubble bursting. Oil falling hard. Stagflation narrative wrong.",
    "Real estate market in free fall. Worst month since 2008. Housing recession here.",
    "Real estate recovery underway. Mortgage rates stabilizing. Housing bottom in.",
    "Bonds finally rallying after 2 years of pain. Duration is back. Long bonds mooning.",
    "Bond market selling off again. Rates spike 50bps in one week. This is a bloodbath.",
    "Small caps rallying hard. Russell 2000 up 8% in March. Broadening market recovery.",
    "Small caps collapsing. Market concentration back to mega cap only.",
    "Value finally working. Growth destroyed. Mean reversion is real.",
    "Growth bouncing back hard. Value trap confirmed. Tech's day has come.",
    "Rotation into financials accelerating. Bank stocks up 15%. Rising rate environment working.",
    "Bank stocks getting destroyed on recession fears. Deposit flight accelerating.",
    "Healthcare rally underway. Defensive positioning profitable. Recession hedge working.",
    "Healthcare selling off on obesity drug success. Obesity becomes treatable disease.",
    "Consumer discretionary getting hammered. Luxury brands warn on margins.",
    "Consumer strength data shocking everyone. Holiday sales beat. Economy resilient.",
    "Staples holding up while everything else falls. Recession trade working.",
    "Staples weakness signals consumer demand collapsing. Economic slowdown confirmed.",
    "Retail earnings massacred. Forward guidance slashed. Margin compression is permanent.",
    "Retail beat expectations across the board. Consumer strength evident.",
    "Earnings recession here. Corporate profits declining 5%. What's the multiple for that?",
    "Earnings resilience defying skeptics. Margins holding better than feared.",
    "Guidance pulled on visibility. Macro uncertainty too high to forecast.",
    "Guidance raised again. Demand stronger than expected. Bull case intact.",
    "Analyst downgrades cascading across sector. Time to sell?",
    "Street upgrading everything. Is this capitulation low?",
    "IPO market frozen completely. Zero deals in two months.",
    "IPO market exploded back. 15 deals last week. Risk appetite returning.",
    "M&A activity dead. Deal making abandoned. Economy in stasis.",
    "M&A boom underway. Strategic buyers active again. Consolidation accelerating.",
    "Buyback season strongest on record. Companies buying at peaks. Insiders confident.",
    "Buybacks collapsing as guidance pulled. Companies hoarding cash.",
    "Insider selling accelerating. Executives dumping stock. Top is in.",
    "Insider buying hitting records. Smart money confident. Bottom is in.",
    "Short interest spiking across market. Retail vs shortsellers. Gamma hedging coming.",
    "Short squeeze underway. Retail pile on. Don't fight the tape.",
    "Options expiration gamma rally today. Technical bounce, nothing more.",
    "Options crush destroying call holders. IV collapse devastating.",
    "Volatility compression creating opportunity. Vol is absurdly low.",
    "Market breadth expanding rapidly. Healthy rally confirmed.",
]

random.seed(42)

all_data = []
for post in evidence_based:
    all_data.append([post, "evidence_based", "synthetic"])
for post in speculative_take:
    all_data.append([post, "speculative_take", "synthetic"])
for post in market_reaction:
    all_data.append([post, "market_reaction", "synthetic"])

random.shuffle(all_data)

csv_path = "data/investing_dataset.csv"
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['text', 'label', 'notes'])
    writer.writerows(all_data)

print(f"Generated {len(all_data)} rows across 3 labels")
print(f"Saved to {csv_path}\n")

print("--- EVIDENCE BASED SAMPLES ---")
evidence_rows = [row for row in all_data if row[1] == 'evidence_based']
samples = random.sample(evidence_rows, min(5, len(evidence_rows)))
for i, (text, label, notes) in enumerate(samples, 1):
    print(f"{i}. {text}\n")

print("\n--- SPECULATIVE TAKE SAMPLES ---")
spec_rows = [row for row in all_data if row[1] == 'speculative_take']
samples = random.sample(spec_rows, min(5, len(spec_rows)))
for i, (text, label, notes) in enumerate(samples, 1):
    print(f"{i}. {text}\n")

print("\n--- MARKET REACTION SAMPLES ---")
react_rows = [row for row in all_data if row[1] == 'market_reaction']
samples = random.sample(react_rows, min(5, len(react_rows)))
for i, (text, label, notes) in enumerate(samples, 1):
    print(f"{i}. {text}\n")
