# Reasoning Gates Template

## Overview

Reasoning gates are mandatory checkpoints that force structured analysis before proceeding. They prevent rushing through research and ensure each evidence tier is properly synthesized.

**Rule:** You may NOT proceed past a reasoning gate until all sections are completed.

---

## Pre-Research Gate: Pre-Mortem Analysis

Complete BEFORE beginning any searches:

```markdown
## PRE-MORTEM ANALYSIS: [BANK NAME]

### Anticipated Failure Modes

**Failure Mode 1: Insufficient Public Information**
This bank may not publicly disclose CDM activities because:
[Write specific hypothesis — e.g., "German banks are less transparent about technology initiatives than US/UK peers"]

- Probability this applies: [X]%
- Mitigation strategy: [What alternative sources or approaches?]
- Fallback if mitigation fails: [What will you conclude?]

**Failure Mode 2: Misleading Evidence**
I might find evidence that appears to support [classification] but is misleading because:
[Write specific hypothesis — e.g., "Vendor marketing may overstate bank's CDM adoption"]

- Probability this applies: [X]%
- Mitigation strategy: [What verification steps?]
- Red flags to watch for: [List specific warning signs]

**Failure Mode 3: Outdated Information**
Evidence might reflect historical position rather than current status because:
[Write specific hypothesis — e.g., "2018 pilot participation doesn't mean current engagement"]

- Probability this applies: [X]%
- Mitigation strategy: [What recency checks?]
- Time threshold for "current": [X months]

**Failure Mode 4: Confirmation Bias**
I might unconsciously favor evidence supporting [my prior expectation] because:
[Write specific hypothesis — e.g., "Original framework claims pilot status, which may anchor my search"]

- Probability this applies: [X]%
- Mitigation strategy: [What structured disconfirmation?]
- Adversarial commitment: [What specific counter-hypothesis will I test?]

### Anticipated Difficulty Assessment
Based on pre-mortem analysis, this research will be:
[ ] EASY — Bank is well-covered, public, strong CDM presence expected
[ ] MODERATE — Some coverage expected, may require Tier 2/3 evidence
[ ] DIFFICULT — Limited coverage expected, may result in low confidence

Justification: [1-2 sentences]

### Success Criteria
This research will be successful if I can:
1. [Specific criterion 1]
2. [Specific criterion 2]
3. [Specific criterion 3]

I am ready to proceed: [ ] YES
```

---

## Reasoning Gate 1: After Tier 1 Searches

Complete AFTER all Tier 1 searches, BEFORE Tier 2:

```markdown
## REASONING GATE 1: TIER 1 SYNTHESIS — [BANK NAME]

### Evidence Delta Analysis

For each finding, state what changed in your beliefs:

| Finding ID | Prior Belief | Updated Belief | Magnitude |
|------------|--------------|----------------|-----------|
| [BANK-001] | [What you assumed before] | [What you now believe] | [Significant/Marginal/None] |
| [BANK-002] | [What you assumed before] | [What you now believe] | [Significant/Marginal/None] |
| [NULL-001] | [Expected to find X] | [Did not find X] | [Significant/Marginal/None] |

### Probability Update

Using Bayesian framework from /methodology/bayesian-updating.md:

**Prior (entering Tier 1):**
- P(ARCHITECT) = [X]%
- P(PRAGMATIST) = [Y]%
- Prior Odds = [ratio]

**Tier 1 Evidence:**
| Finding | Evidence Type | Likelihood Ratio |
|---------|---------------|------------------|
| [BANK-001] | [Type] | [LR] |
| [BANK-002] | [Type] | [LR] |
| [NULL-001] | Absence after search | [LR] |

**Combined LR:** [Product of LRs]

**Posterior:**
- Posterior Odds = [Prior Odds] × [Combined LR] = [result]
- P(ARCHITECT | Tier 1) = [X]%
- P(PRAGMATIST | Tier 1) = [Y]%

### Evidence Sufficiency Check

[ ] Do I have Tier 1 evidence sufficient to classify with >80% confidence?
    → If YES: Justify skipping Tier 2 and proceed to synthesis
    → If NO: Continue to Tier 2

[ ] What SPECIFIC question must Tier 2 answer?
    [Write the question — e.g., "Is there any evidence of production timeline?"]

[ ] If Tier 2 finds NOTHING relevant, my conclusion will be:
    [Write the conditional conclusion — e.g., "PRAGMATIST at ~75% confidence"]

### Counterfactual Test

"If I had found the OPPOSITE of what I found in Tier 1, how would my assessment change?"

Counterfactual scenario: [Describe what opposite evidence would look like]
Impact on classification: [How would classification change?]
Implication: [Does this confirm my findings actually matter, or would I conclude the same either way?]

### Mini-Adversarial Check

For the strongest piece of Tier 1 evidence, challenge it:

**Evidence:** [BANK-###]
**Alternative interpretation:** [What else could this evidence mean?]
**Source motivation:** [Could the source be biased?]
**Verdict:** [Accept / Accept with caveat / Reduce weight]

### Gate Clearance

[ ] All sections above are complete (not just checked, but substantively filled)
[ ] Probability update is calculated correctly
[ ] Counterfactual test confirms evidence is informative
[ ] Decision on proceeding to Tier 2 is documented

**Cleared to proceed to Tier 2:** [ ] YES / [ ] NO (address gaps first)
```

---

## Reasoning Gate 2: After Tier 2 Searches

Complete AFTER all Tier 2 searches, BEFORE Tier 3:

```markdown
## REASONING GATE 2: TIER 2 SYNTHESIS — [BANK NAME]

### Evidence Delta Analysis

| Finding ID | Prior Belief (post-Tier 1) | Updated Belief | Magnitude |
|------------|----------------------------|----------------|-----------|
| [BANK-003] | [What you believed] | [What you now believe] | [Significant/Marginal/None] |
| [BANK-004] | [What you believed] | [What you now believe] | [Significant/Marginal/None] |

### Probability Update

**Prior (entering Tier 2 = Posterior from Tier 1):**
- P(ARCHITECT) = [X]%
- P(PRAGMATIST) = [Y]%

**Tier 2 Evidence:**
| Finding | Evidence Type | Likelihood Ratio |
|---------|---------------|------------------|
| [BANK-003] | [Type] | [LR] |
| [BANK-004] | [Type] | [LR] |

**Combined LR (Tier 2):** [Product]

**Posterior:**
- P(ARCHITECT | Tier 1+2) = [X]%
- P(PRAGMATIST | Tier 1+2) = [Y]%

### Corroboration Assessment

Do Tier 2 findings corroborate or contradict Tier 1?

| Tier 1 Finding | Tier 2 Finding | Relationship |
|----------------|----------------|--------------|
| [BANK-001] | [BANK-003] | [Corroborates / Contradicts / Independent] |
| [BANK-002] | [BANK-004] | [Corroborates / Contradicts / Independent] |

**Consistency verdict:** [Consistent / Minor inconsistencies / Major contradiction]

If contradictions exist, trigger: /appendices/contradiction-resolution.md

### Observable Implications Test

For my current leading hypothesis ([ARCHITECT/PRAGMATIST]), what should I observe?

**If ARCHITECT hypothesis is correct:**
| Observable Implication | Found? | Notes |
|------------------------|--------|-------|
| Bank mentioned in ISDA/FINOS contributor lists | [ ] Yes [ ] No | |
| Named individuals speaking at CDM events | [ ] Yes [ ] No | |
| Job postings for CDM-related roles | [ ] Yes [ ] No | |
| Vendor partnerships for CDM tooling | [ ] Yes [ ] No | |
| Production or pilot announcement | [ ] Yes [ ] No | |

**Implications found:** [X] / 5
**If <3/5:** Downgrade ARCHITECT hypothesis or explain why implications wouldn't be visible

**If PRAGMATIST hypothesis is correct:**
| Observable Implication | Found? | Notes |
|------------------------|--------|-------|
| Absence of CDM mentions in technology communications | [ ] Yes [ ] No | |
| Traditional vendor partnerships (not CDM-native) | [ ] Yes [ ] No | |
| Regulatory compliance without CDM mentioned | [ ] Yes [ ] No | |
| Capacity consumed by other priorities | [ ] Yes [ ] No | |
| No speakers at CDM-specific events | [ ] Yes [ ] No | |

**Implications found:** [X] / 5
**If <3/5:** Upgrade away from PRAGMATIST or explain anomaly

### Evidence Sufficiency Check

[ ] Do I have sufficient evidence to classify with target confidence?
    → If YES: Justify skipping Tier 3 and proceed to synthesis
    → If NO: Continue to Tier 3

[ ] What can Tier 3 add that Tier 1+2 haven't provided?
    [Write specific value-add — e.g., "Trajectory signals from job postings"]

[ ] Diminishing returns assessment:
    [ ] Tier 3 likely to change classification → Continue
    [ ] Tier 3 unlikely to change but may refine confidence → Continue briefly
    [ ] Tier 3 unlikely to add value → Skip with justification

### Mini-Adversarial Check

"I am currently leaning toward [CLASSIFICATION]. The strongest argument against this is:"
[Write 2-3 sentences with the best counter-argument]

"This counter-argument is [compelling / somewhat compelling / not compelling] because:"
[Explain why]

### Gate Clearance

[ ] All sections complete
[ ] Probability update calculated
[ ] Corroboration assessed
[ ] Observable implications tested
[ ] Adversarial check performed

**Cleared to proceed:** [ ] To Tier 3 / [ ] To Synthesis (justify skip)
```

---

## Reasoning Gate 3: After Tier 3 Searches

Complete AFTER Tier 3 searches, BEFORE synthesis:

```markdown
## REASONING GATE 3: TIER 3 SYNTHESIS — [BANK NAME]

### Evidence Delta Analysis

| Finding ID | Prior Belief (post-Tier 2) | Updated Belief | Magnitude |
|------------|----------------------------|----------------|-----------|
| [BANK-005] | [What you believed] | [What you now believe] | [Significant/Marginal/None] |

### Final Probability Update

**Prior (entering Tier 3 = Posterior from Tier 2):**
- P(ARCHITECT) = [X]%
- P(PRAGMATIST) = [Y]%

**Tier 3 Evidence:**
| Finding | Evidence Type | Likelihood Ratio |
|---------|---------------|------------------|
| [BANK-005] | [Type] | [LR] |

**Final Posterior:**
- P(ARCHITECT | All Evidence) = [X]%
- P(PRAGMATIST | All Evidence) = [Y]%

### Evidence Pattern Assessment

What overall pattern does the evidence show?

[ ] **Strong Architect signal:** Multiple tiers point to active engagement
[ ] **Weak Architect signal:** Some engagement evidence but gaps
[ ] **Neutral:** Evidence is mixed or uninformative
[ ] **Weak Pragmatist signal:** Limited engagement evidence, some activity
[ ] **Strong Pragmatist signal:** Consistent absence across tiers

### Trajectory Assessment

Based on temporal analysis of evidence:

**Historical position (>18 months ago):** [Describe if known]
**Current position:** [Describe based on evidence]
**Future signals:** [Any forward-looking evidence?]

**Trajectory classification:**
[ ] ACCELERATING — Moving toward greater CDM engagement
[ ] STABLE — Maintaining current position
[ ] STALLED — Announced intentions not materializing
[ ] DECELERATING — Reducing engagement
[ ] UNKNOWN — Insufficient temporal data

### Readiness for Synthesis

[ ] I have gathered evidence across all relevant tiers
[ ] I have documented null results as well as findings
[ ] I have updated probabilities at each gate
[ ] I have tested observable implications
[ ] I have challenged my emerging conclusion
[ ] I am ready to synthesize

**Evidence inventory complete:** [ ] YES

**Proceed to:** [ ] Full Synthesis (Pass 3) / [ ] Abbreviated Synthesis (Tier B/C)
```

---

## Quick Gates for Tier B and C Banks

### Tier B Abbreviated Gate (Use after each search tier)

```markdown
## ABBREVIATED GATE: [BANK NAME] — After Tier [X]

### Key Findings
1. [Most important finding]
2. [Second most important]
3. [Third if applicable]

### Probability Update
- Prior P(Architect): [X]% → Posterior P(Architect): [Y]%
- Direction: [Toward Architect / Toward Pragmatist / Unchanged]

### Sufficiency Check
[ ] Enough to classify? → [Yes: proceed to output / No: continue searching]

### Quick Adversarial
Best argument against my emerging conclusion: [1-2 sentences]
Response: [1-2 sentences]

### Proceed: [ ] YES
```

---

### Tier C Rapid Gate (Use once after all searches)

```markdown
## RAPID GATE: [BANK NAME]

### Evidence Summary
- Searches executed: [count]
- Relevant findings: [count]
- Highest evidence tier reached: [1/2/3/4]

### Quick Classification
Based on evidence gathered:
- Classification: [ARCHITECT-variant / PRAGMATIST-variant / UNKNOWN]
- Confidence: [X]%
- Key supporting evidence: [1-2 sentences]

### Single Adversarial Question
What is ONE thing that, if true, would make this classification wrong?
[Answer in 1-2 sentences]

Did I check for this? [ ] Yes → Result: [finding]
                      [ ] No → Flag as: [uncertainty]

### Output Ready: [ ] YES
```
