# Confidence Calibration

## Purpose

Confidence levels communicate the reliability of classifications to downstream users. Miscalibrated confidence undermines framework utility:
- **Overconfidence** → False precision, wrong decisions
- **Underconfidence** → Excessive caveating, decision paralysis

This document provides objective criteria for assigning and verifying confidence levels.

---

## Confidence Level Definitions

### 90-100%: Near Certain

**Meaning:** Classification is almost certainly correct. Would be surprising if wrong.

**Evidence Requirements:**
- [ ] Official announcement (Tier 1) directly confirms classification
- [ ] At least 2 independent Tier 1 sources corroborate
- [ ] No credible contradicting evidence exists
- [ ] Conclusion consistent with all anchor points
- [ ] Adversarial challenge found no compelling counter-argument

**Appropriate Language:**
- "Deutsche Bank is in CDM production..."
- "JPMorgan has confirmed..."
- "Evidence definitively shows..."

**Betting Test:** Would give 9:1 odds or better

---

### 70-89%: High Confidence

**Meaning:** Classification is likely correct. Some uncertainty but strong evidence base.

**Evidence Requirements:**
- [ ] At least 1 Tier 1 source OR 3+ Tier 2 sources support
- [ ] Logical inference chain is clear and defensible
- [ ] Adversarial challenge did not surface strong counter-evidence
- [ ] Minor uncertainties exist but don't undermine core conclusion
- [ ] Consistent with peer comparisons

**Appropriate Language:**
- "Evidence strongly suggests..."
- "Barclays is likely an Architect-Follower based on..."
- "With high confidence, we assess..."

**Betting Test:** Would give 3:1 to 9:1 odds

---

### 50-69%: Moderate Confidence

**Meaning:** Classification is more likely than alternatives but significant uncertainty remains.

**Evidence Requirements:**
- [ ] Tier 2 sources only, no Tier 1 confirmation
- [ ] Inference required to connect evidence to conclusion
- [ ] Some gaps in evidence coverage
- [ ] Alternative interpretations are plausible but less likely
- [ ] Trajectory or future direction unclear

**Appropriate Language:**
- "Available evidence suggests..."
- "We tentatively classify X as..."
- "Based on limited information..."

**Betting Test:** Would give 1:1 to 3:1 odds

---

### 30-49%: Low Confidence

**Meaning:** Best guess given limited information. Classification could easily be wrong.

**Evidence Requirements:**
- [ ] Primarily Tier 3 evidence or inference from absence
- [ ] Significant gaps in evidence coverage
- [ ] Alternative interpretations are equally plausible
- [ ] Classification is "most likely" rather than "likely"

**Appropriate Language:**
- "Limited evidence suggests..."
- "We hypothesize X may be..."
- "Requires validation, but initial assessment..."

**Betting Test:** Would not bet at even odds

---

### Below 30%: Insufficient Evidence

**Meaning:** Cannot reliably classify. Evidence base is inadequate.

**Evidence Requirements:**
- [ ] No direct evidence found despite thorough search
- [ ] Classification based entirely on business model inference or analogy
- [ ] Unable to distinguish between hypotheses

**Appropriate Language:**
- "Insufficient evidence to classify"
- "Classification: UNKNOWN"
- "Requires direct validation"

**Action:** Do not state as finding. Flag for validation.

---

## Confidence Calibration Checklist

After determining classification, use this checklist to assign confidence:

### Step 1: Evidence Tier Assessment

What is the highest evidence tier supporting your classification?

| Highest Tier | Maximum Confidence |
|--------------|-------------------|
| Tier 1 (confirming) | Up to 95% |
| Tier 2 only | Up to 75% |
| Tier 3 only | Up to 50% |
| Tier 4 / inference only | Up to 35% |
| No supporting evidence | Up to 25% |

**Your maximum:** ____%

### Step 2: Corroboration Adjustment

How many independent sources support your classification?

| Corroboration | Adjustment |
|---------------|------------|
| 3+ independent sources | +10% |
| 2 independent sources | +5% |
| 1 source only | +0% |
| Uncorroborated | -10% |

**Adjustment:** ____%

### Step 3: Contradiction Assessment

Does any evidence contradict your classification?

| Contradiction Status | Adjustment |
|---------------------|------------|
| No contradictions | +0% |
| Minor contradiction (resolved) | -5% |
| Significant contradiction (resolved) | -10% |
| Unresolved contradiction | -15% to -25% |

**Adjustment:** ____%

### Step 4: Adversarial Survival

How did your classification fare in adversarial testing?

| Adversarial Result | Adjustment |
|--------------------|------------|
| Strengthened by challenge | +5% |
| Unchanged | +0% |
| Weakened but maintained | -5% |
| Required revision | -10% |

**Adjustment:** ____%

### Step 5: Coherence Check

Is your classification consistent with framework?

| Coherence Status | Adjustment |
|------------------|------------|
| Fully consistent with anchors and peers | +5% |
| Minor inconsistency (explained) | +0% |
| Inconsistency requiring explanation | -5% |
| Significant incoherence | -10% |

**Adjustment:** ____%

### Step 6: Calculate Final Confidence

```
Final Confidence = Maximum + Corroboration + Contradiction + Adversarial + Coherence
Final Confidence = ____% + ____% + ____% + ____% + _____% = ____%
```

Cap at 95% (never claim certainty) and floor at 20% (below this, classify as UNKNOWN).

---

## The Betting Test

A powerful calibration check is the betting test:

**Ask yourself:** "If someone offered me a bet at the odds implied by my confidence, would I take it?"

| Confidence | Implied Odds | Bet Structure |
|------------|--------------|---------------|
| 90% | 9:1 | I risk $9 to win $1 if right |
| 80% | 4:1 | I risk $4 to win $1 if right |
| 70% | 2.3:1 | I risk $2.30 to win $1 if right |
| 60% | 1.5:1 | I risk $1.50 to win $1 if right |
| 50% | 1:1 | I risk $1 to win $1 if right |

**If you wouldn't take the bet, your confidence is too high.**

---

## Cross-Bank Calibration

After completing a phase, verify confidence is consistent across banks:

### Consistency Test 1: Evidence-Confidence Correlation

| Bank | Highest Tier | # Sources | Confidence |
|------|--------------|-----------|------------|
| Bank A | Tier 1 | 3 | 85% |
| Bank B | Tier 2 | 4 | 70% |
| Bank C | Tier 2 | 2 | 65% |
| Bank D | Tier 3 | 2 | 45% |

**Check:** Does confidence decrease as evidence quality decreases? If not, recalibrate.

### Consistency Test 2: Similar Evidence, Similar Confidence

If two banks have similar evidence profiles, they should have similar confidence levels.

**Example Issue:**
- Bank A: 1 Tier 2 source → 75% confidence
- Bank B: 2 Tier 2 sources → 60% confidence

This is inconsistent. Either A is overconfident or B is underconfident.

### Consistency Test 3: Classification-Confidence Alignment

| Classification | Expected Confidence Range |
|----------------|---------------------------|
| ARCHITECT-Native | 85-95% (requires production confirmation) |
| ARCHITECT-Leader | 70-90% |
| ARCHITECT-Follower | 55-85% |
| PRAGMATIST (confirmed) | 70-90% |
| PRAGMATIST (inferred) | 45-70% |
| UNKNOWN | <40% |

**Check:** Does your confidence fall in expected range for classification?

---

## Confidence Language Guide

### Phrases by Confidence Level

**90%+:**
- "Bank X has confirmed..."
- "Evidence definitively establishes..."
- "Bank X is [classification]..."

**70-89%:**
- "Evidence strongly suggests..."
- "Bank X is likely [classification]..."
- "With high confidence..."
- "Based on substantial evidence..."

**50-69%:**
- "Available evidence suggests..."
- "Bank X appears to be..."
- "We tentatively assess..."
- "Based on limited but consistent evidence..."

**30-49%:**
- "Initial evidence suggests..."
- "Bank X may be [classification]..."
- "Preliminary assessment indicates..."
- "Subject to validation..."

**<30%:**
- "Insufficient evidence to classify..."
- "Cannot determine positioning..."
- "Requires direct validation..."
- "Classification: UNKNOWN"

### Phrases to Avoid

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| "Clearly..." | Implies certainty without evidence | "Evidence indicates..." |
| "Obviously..." | Dismisses need for evidence | "Based on [source]..." |
| "We know that..." | Overstates certainty | "Evidence suggests..." |
| "Without doubt..." | Never appropriate | State confidence % |
| "It seems like..." | Too vague | Be specific about evidence |

---

## Confidence Documentation Template

For each bank, document confidence rationale:

```markdown
## Confidence Assessment: [BANK NAME]

### Classification: [POSTURE-VARIANT]

### Confidence Level: [X]%

### Calibration Calculation
- Maximum (Tier [X] evidence): [X]%
- Corroboration adjustment: [+/-X]%
- Contradiction adjustment: [+/-X]%
- Adversarial adjustment: [+/-X]%
- Coherence adjustment: [+/-X]%
- **Final:** [X]%

### Betting Test
At [X]% confidence, implied odds are [Y]:1.
Would I bet at these odds? [Yes/No]
If no, adjusted confidence: [X]%

### Confidence Rationale
[2-3 sentences explaining why this confidence level is appropriate]

### What Would Change Confidence
- To increase: [What evidence would we need?]
- To decrease: [What evidence would undermine?]
```
