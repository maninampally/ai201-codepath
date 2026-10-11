# TakeMeter — Planning & Decision Rules

## Label Definitions

### `evidence_based`
A claim supported by financial metrics, economic data, causal reasoning, or an explicit chain of logic. The post must show **why** the data supports the claim — a single statistic attached to a conclusion does not qualify.

**Signal phrases:**
- Specific numbers with context ("margins fell to 41% from 56%")
- Causal chains ("X leads to Y which causes Z")
- Comparisons ("unlike competitors, this company has...")
- Multi-factor analysis (metric + reasoning + implication)

**NOT evidence_based:**
- "Stock will hit $50" (prediction without supporting data)
- "Company has 5% growth" (single stat alone)
- Emotional assertions ("This company is undervalued")

---

### `speculative_take`
An unsupported or lightly supported prediction, buy/sell call, price target, or strong opinion without an explicit argument. Includes posts with one isolated stat used as decoration for a judgment.

**Signal phrases:**
- Price targets ("TSLA hits $300 by 2026")
- Trade calls ("Load up now", "Buy the dip")
- Directional claims ("Stock crashes 40%")
- Predictions with weak justification ("Will moon because AI")

**NOT speculative_take:**
- Emotional reactions to news ("Market crashed, I'm scared")
- Observations of current events ("Fed raised rates today")

---

### `market_reaction`
An immediate emotional, humorous, celebratory, fearful, or surprised response to a market event. Primary purpose is expression, not analysis or advice.

**Signal phrases:**
- Emotional language ("Holy cow", "destroyed", "mooning")
- Reactions to news ("Powell's comments tanked the market")
- Market observations without prediction ("Circuit breakers tripped")
- Humor/sarcasm in response to volatility

**NOT market_reaction:**
- Analysis of why something happened (that's evidence_based)
- Advice or calls to action (that's speculative_take)

---

## Hard Edge Cases & Decision Rules

### Rule 1: Single Statistic + Conclusion
**Definition:** A post cites one metric and immediately concludes with a judgment or recommendation.

**Decision:** → `speculative_take`

**Why:** A single data point without supporting causal logic does not show *why* the data matters. It's decoration for an unsupported claim.

**Example:** "Model N captures 5-10% of deal value. Enterprise economics strong." → No reasoning connecting the statistic to the conclusion. `speculative_take`.

---

### Rule 2: Data + Prediction
**Definition:** Post contains metrics or observations but concludes with a forward-looking trade call or price target.

**Decision:** → `speculative_take`

**Why:** The conclusion is a prediction, not an explanation. Even if data is present, the post's purpose is advising a trade.

**Example:** "Costco's renewal rate hit 90.5%. When membership moat strengthens, returns compound. Price target upgrade justified." → Metric present, but conclusion is a trade call. `speculative_take`.

---

### Rule 3: Market Sentiment + Directional Call
**Definition:** Post observes market behavior or sentiment but concludes with a market prediction.

**Decision:** → `speculative_take`

**Why:** Observing sentiment is not the same as expressing emotion. If the post concludes with "the bottom is in" or "we're headed lower," it's a directional claim, not a reaction.

**Example:** "Insider buying hitting records. Smart money confident. Bottom is in." → Observation of insider action + market call. `speculative_take`.

---

### Rule 4: Trade Call in Emotional Framing
**Definition:** Post sounds like a market reaction (celebratory or fearful tone) but concludes with advice to buy/sell.

**Decision:** → `speculative_take`

**Why:** If the post ends with "load up now," it's a trade recommendation, regardless of emotional framing earlier. Purpose is advice, not expression.

**Example:** "Crypto winter is over. Bitcoin breaking above $45k. Altseason incoming. Load up now." → Emotional framing, but conclusion is a buy call. `speculative_take`.

---

### Rule 5: Reasoning Chain + Trade Call
**Definition:** Post provides metrics, causal logic, and concludes with a price target or buy/sell recommendation.

**Decision:** → `evidence_based`

**Why:** The post demonstrates *why* the conclusion follows from the data. Even though it ends with a recommendation, the core claim is evidenced.

**Example:** "Apple's services growing 12% YoY at 70% margins. With 2B installed base, recurring revenue is predictable. That's why AAPL trades at premium valuation." → Metric + logic + conclusion about valuation. `evidence_based`.

---

### Rule 6: Immediate Reaction to Market Event
**Definition:** Post responds to breaking news or market action with emotion or humor, without analyzing the event.

**Decision:** → `market_reaction`

**Why:** Primary purpose is expression, not understanding. The post doesn't explain *why* something happened or *what it means* — it just reacts.

**Example:** "Powell's hawkish comments tanked the entire market at 2:45pm. Every sector red. Why do we even invest?" → Observation + emotional reaction. `market_reaction`.

---

## Annotation Workflow

1. **Read the post.** Is it explaining something, predicting something, or reacting to something?

2. **Check for data.** Is there a specific metric or data point?
   - If yes → apply Rule 1, 2, or 5
   - If no → likely `speculative_take` or `market_reaction`

3. **Check the conclusion.** Does the post end with a prediction/call, explanation, or reaction?
   - Prediction/call → `speculative_take`
   - Explanation with data → `evidence_based`
   - Emotion/surprise → `market_reaction`

4. **Verify the causal chain.** If data + conclusion, is there *why* connecting them?
   - Yes, clear chain → `evidence_based`
   - No, assertion only → `speculative_take`

5. **Edge case tie-breaker:** When unclear, ask:
   - "Could I explain the claim using only the data provided?" If yes → `evidence_based`
   - "Is this post trying to convince me to buy/sell or predict a price?" If yes → `speculative_take`
   - "Is this post expressing surprise, fear, or humor about market news?" If yes → `market_reaction`

---

## Boundary Examples Walked Through

**Example A:** "Broadcom's gross margins are 73%, up from 68%. Their fab partnerships create supply resilience competitors lack. This advantage gets underpriced."

- Data? Yes (73%, 68%, partnerships).
- Causal chain? Yes (partnerships → resilience → competitive advantage).
- Conclusion? Valuation claim (underpriced).
- Answer: `evidence_based`. The post shows *why* the data supports the claim.

**Example B:** "Broadcom rallies to $800. Supply constraints keep ASP elevated."

- Data? Yes (ASP constraint).
- Causal chain? Weak ("constraints keep ASP elevated" is asserted, not explained).
- Conclusion? Price target ($800).
- Answer: `speculative_take`. Prediction + weak justification.

**Example C:** "Broadcom stock is exploding! Best time to be in semis!"

- Data? No.
- Conclusion? Enthusiastic reaction + implicit buy call.
- Emotion? Yes.
- Answer: `speculative_take` (ends with implied buy) or `market_reaction` (pure emotion)? Rule 4: if there's an implicit call, lean `speculative_take`. But if purely celebratory with no call, `market_reaction`.

---

## Dataset Composition

**Target:** 210 examples total, 70 per label

**Characteristics:**
- **evidence_based:** Real company names, realistic metrics, reasoning chains. Companies: Apple, Microsoft, Nvidia, Intel, GE, Visa, Boeing, Pfizer, etc. Examples show margin analysis, market share shifts, product adoption, customer retention.

- **speculative_take:** Varied prediction styles. Price targets, market calls, directional claims. Mix of bullish (Tesla to $300) and bearish (NVDA crashes 40%). Crypto, legacy tech, fintech predictions included.

- **market_reaction:** Emotional triggers. Fed announcements, earnings surprises, market crashes, circuit breakers, volatility spikes, geopolitical events. Language varies: panic, celebration, sarcasm, frustration.

---

## Validation Checklist

- [ ] All 210 examples labeled
- [ ] No example labeled with multiple labels
- [ ] Difficult cases use decision rules consistently
- [ ] At least 5 per-label examples reviewed by human for accuracy
- [ ] No duplicate texts
- [ ] All texts between 15–100 words (inclusive)
- [ ] Label distribution: 70 / 70 / 70
