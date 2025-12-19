# Null Result Handling

## Overview

Null results (searches that find nothing relevant) are often as informative as positive findings. This appendix provides systematic approaches for interpreting, documenting, and using absence of evidence.

---

## The Null Result Decision Tree

```
IF search returns no relevant results:
│
├── Is the search well-constructed?
│   └── NO → Reformulate query (see /appendices/search-strategies.md)
│   └── YES ↓
│
├── Is the topic inherently low-visibility?
│   └── YES → Null is UNINFORMATIVE (doesn't support either hypothesis)
│             Examples: Internal initiatives at private banks
│                       Pre-announcement stage work
│                       Non-English language markets
│   └── NO ↓
│
├── Would we EXPECT to find evidence if ARCHITECT?
│   └── YES → Null is INFORMATIVE toward PRAGMATIST
│             Apply "Absence of expected evidence" likelihood ratio
│   └── NO → Null is UNINFORMATIVE
│
├── Has the search space been exhausted?
│   └── NO → Execute Attempt 2, 3, 4 (see search strategies)
│   └── YES ↓
│
└── CLASSIFY NULL RESULT:
    ├── INFORMATIVE ABSENCE → Use in Bayesian update
    ├── UNINFORMATIVE ABSENCE → Document but do not update
    └── INCONCLUSIVE → Flag as gap requiring validation
```

---

## Null Result Categories

### Category 1: Informative Absence

**Definition:** Absence of evidence is itself evidence because we would expect to find evidence if the hypothesis were true.

**When to Apply:**
- Bank is large, public, and transparent
- The topic is one typically disclosed (production, significant initiatives)
- Peers in similar position have disclosed
- Sufficient search depth reached (Tier 1 and Tier 2 exhausted)

**Example:**
> "After exhaustive search of official sources and trade press, no evidence of Deutsche Bank CDM engagement found. Given DB's size, transparency, and the fact that comparable peers (BNP, Barclays) have disclosed their CDM positions, this absence is informative. Apply LR = 0.21 (absence after exhaustive Tier 1 search) toward PRAGMATIST."

**Likelihood Ratios for Informative Absence:**
| Search Depth | LR | Meaning |
|--------------|-----|---------|
| Tier 1 exhausted | 0.21 | Moderate evidence for Pragmatist |
| Tier 1+2 exhausted | 0.11 | Strong evidence for Pragmatist |
| Full protocol exhausted | 0.06 | Very strong evidence for Pragmatist |

---

### Category 2: Uninformative Absence

**Definition:** Absence of evidence does not support either hypothesis because we wouldn't necessarily expect to find evidence.

**When to Apply:**
- Bank operates in low-transparency jurisdiction
- Bank is private or has limited disclosure requirements
- Topic is pre-announcement or confidential
- Search space may not cover relevant sources (language barriers, etc.)
- Work may be happening internally without external disclosure

**Example:**
> "No evidence of Pictet Group CDM activity found in general searches. However, Pictet is a Swiss private bank with limited public disclosure. The absence is uninformative — they may or may not be engaged without public evidence. LR = 1.0 (no update)."

**Handling:**
- Document the null result
- Note why it's uninformative
- Do not update probability
- May still affect confidence (uncertainty increases)

---

### Category 3: Inconclusive Absence

**Definition:** Ambiguous situation where we're uncertain whether absence is meaningful.

**When to Apply:**
- Mixed signals (some disclosure expected, but topic may be confidential)
- Incomplete search (time constraints, access issues)
- Peer behavior is mixed (some disclose, others don't)

**Example:**
> "No evidence of MUFG CDM activity found. Uncertain whether this reflects non-engagement or simply that Japanese banks don't disclose such initiatives publicly. Classification: Inconclusive absence."

**Handling:**
- Document the ambiguity
- Apply modest probability update (LR = 0.5 to 0.7)
- Flag as gap requiring validation
- Note what would resolve the ambiguity

---

## Null Result Documentation Template

```markdown
NULL RESULT RECORD

### Search Identification
- Search ID: [BANK-S##]
- Query: [Exact query]
- Tier: [1/2/3]
- Attempt: [1/2/3/4]
- Date: [YYYY-MM-DD]

### Result
- Results returned: [N]
- Results reviewed: [N]
- Relevant results: 0

### Null Classification
[ ] INFORMATIVE ABSENCE
    → Applies because: [Why we expected to find evidence]
    → Likelihood Ratio: [0.21 / 0.11 / 0.06]
    → Supports: PRAGMATIST hypothesis

[ ] UNINFORMATIVE ABSENCE
    → Applies because: [Why evidence might not be visible]
    → Likelihood Ratio: 1.0 (no update)
    → Impact: None

[ ] INCONCLUSIVE ABSENCE
    → Uncertain because: [Why ambiguous]
    → Likelihood Ratio: [0.5-0.7 estimate]
    → Flag for: Validation needed

### Explanation
[2-3 sentences explaining the null result and its interpretation]

### Follow-up Action
[ ] Query reformulated → New query: [X]
[ ] Lateral search executed → Query: [X]
[ ] Direct source checked → Source: [X]
[ ] Accepted and documented
```

---

## Aggregating Multiple Null Results

When multiple searches return null, aggregate carefully:

### Same Hypothesis, Same Tier

If multiple Tier 1 searches all return null, this strengthens the informative absence but doesn't multiply infinitely.

**Aggregation Rule:**
- First null in tier: Apply base LR
- Second null (same tier): Apply LR^0.7 (diminishing returns)
- Third null (same tier): Apply LR^0.5 (strongly diminishing)

**Example:**
- Search 1.1 null: LR = 0.21
- Search 1.2 null: LR = 0.21^0.7 = 0.34
- Search 1.3 null: LR = 0.21^0.5 = 0.46
- Combined: 0.21 × 0.34 × 0.46 = 0.033

**Rationale:** Searches within the same tier are not fully independent; they're looking for similar evidence in overlapping source sets.

### Different Tiers

Null results across different tiers are more independent and can be combined with less discount:

**Example:**
- Tier 1 null (aggregated): LR = 0.15
- Tier 2 null (aggregated): LR = 0.25
- Combined: 0.15 × 0.25 = 0.0375

---

## Patterns of Null Results

### Pattern 1: Complete Silence

**Observation:** No evidence across all tiers for a bank we expected to find covered.

**Interpretation:** Strong evidence for PRAGMATIST classification, BUT:
- Verify search quality (did we look in right places?)
- Consider transparency factors
- Flag as "inferred PRAGMATIST" with appropriate confidence discount

**Confidence Cap:** Maximum 75% confidence for classification based purely on absence

---

### Pattern 2: Tier 1 Silence, Tier 2/3 Signals

**Observation:** No official announcements, but indirect signals (job postings, vendor mentions, conference attendance).

**Interpretation:** 
- Bank may be in early stages (evaluation/pilot)
- Or bank hasn't publicly committed
- Or signals are noise/false positives

**Resolution:**
- Weight Tier 2/3 signals appropriately (weak evidence)
- Do not upgrade to ARCHITECT-Leader or Native without Tier 1
- Classify as ARCHITECT-Follower (tentative) or PRAGMATIST (evaluating)

---

### Pattern 3: Historical Evidence, Current Silence

**Observation:** Found evidence from 2+ years ago, nothing recent.

**Interpretation:**
- Initiative may have stalled
- Bank may have pivoted away
- Or continuing quietly

**Resolution:**
- Classify based on most recent evidence
- Note trajectory as "STALLED" if old evidence, current silence
- Reduce confidence due to uncertainty

---

### Pattern 4: Peer Disclosure, Target Silence

**Observation:** Comparable peers have disclosed CDM positions, but target bank has not.

**Interpretation:**
- Informative absence — if peers disclose, target's silence is meaningful
- Strengthens PRAGMATIST inference

**Resolution:**
- Apply informative absence LR
- Document peer comparison as supporting evidence

---

## When NOT to Treat Absence as Evidence

### Situations Where Absence is Expected

1. **Pre-announcement phase:** Banks don't disclose initiatives until ready
2. **Competitive sensitivity:** Some banks keep technology strategies quiet
3. **Jurisdictional norms:** Not all markets have disclosure expectations
4. **Private institutions:** Privately held banks have minimal disclosure
5. **Non-English markets:** English-language searches may miss coverage

### Red Flags for Over-Interpreting Absence

- [ ] Did you only search in English for a non-English bank?
- [ ] Is this bank known for confidential technology strategies?
- [ ] Are comparably-sized peers also silent (not just this bank)?
- [ ] Is the initiative type typically disclosed before completion?
- [ ] Did you exhaust reformulation and lateral searches?

If any boxes checked, be cautious about treating absence as informative.

---

## Null Result Impact on Confidence

Even uninformative nulls affect confidence by increasing uncertainty:

| Null Result Pattern | Confidence Impact |
|---------------------|-------------------|
| Informative absence (exhaustive search) | Supports Pragmatist, can justify 70-80% confidence |
| Multiple uninformative absences | Increases uncertainty, cap confidence at 60% |
| Inconclusive absences | Flag for validation, cap confidence at 50% |
| Single uninformative null | Minimal impact |

**General Rule:** The more null results, the more uncertain the classification, regardless of informativeness. This is because nulls limit our ability to verify hypotheses.
