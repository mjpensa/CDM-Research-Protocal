# Contradiction Resolution Protocol

## Overview

When evidence conflicts, the natural tendency is to either ignore the inconvenient piece or arbitrarily choose one. This protocol ensures contradictions are handled systematically and transparently.

---

## Step 1: Verify Both Sources

Before attempting to resolve a contradiction, verify that both sources are legitimate evidence.

### Source Reliability Comparison

| Criterion | Questions to Ask |
|-----------|------------------|
| **Authority** | Is each source authoritative for this claim type? |
| **Date** | What is the date of each source? |
| **Specificity** | How specific is each claim? |
| **Motivation** | Does either source have motivation to be inaccurate? |
| **Independence** | Are the sources truly independent or citing the same original? |

### Reliability Decision Matrix

| Source A Tier | Source B Tier | Resolution Rule |
|---------------|---------------|-----------------|
| Tier 1 | Tier 1 | Must resolve — both authoritative |
| Tier 1 | Tier 2 | Tier 1 typically prevails unless Tier 2 is more recent and specific |
| Tier 1 | Tier 3 | Tier 1 prevails; document Tier 3 as weak counter-evidence |
| Tier 2 | Tier 2 | Must resolve — need tiebreaker |
| Tier 2 | Tier 3 | Tier 2 typically prevails |
| Tier 3 | Tier 3 | Neither is strong; reduce confidence regardless of resolution |

### Recency Comparison

| Source A Age | Source B Age | Resolution Rule |
|--------------|--------------|-----------------|
| Current (<6mo) | Current | Consider both equally |
| Current | Recent (6-18mo) | Current typically prevails |
| Current | Dated (>18mo) | Current prevails unless dated is foundational |
| Recent | Recent | Consider both equally |
| Recent | Dated | Recent typically prevails |
| Dated | Dated | Neither is strong; flag for validation |

---

## Step 2: Identify the Nature of Contradiction

### Type A: Temporal Contradiction

**Definition:** Both claims are true but describe different points in time.

**Example:**
- Source A (2023): "Bank X is evaluating CDM"
- Source B (2025): "Bank X has no CDM plans"

**Resolution:** Not actually contradictory. Bank may have evaluated and decided against. Document the evolution: "Bank X evaluated CDM in 2023 but currently has no plans (as of 2025)."

**Classification Impact:** Use most recent status for classification; note historical context.

---

### Type B: Definitional Contradiction

**Definition:** Sources are using terms differently, creating apparent conflict.

**Example:**
- Source A: "Bank X has a CDM pilot"
- Source B: "Bank X has not committed to CDM"

**Resolution:** May not be contradictory. "Pilot" and "commitment" are different stages. Bank may have pilot without production commitment.

**Classification Impact:** Clarify terminology. Both can be true simultaneously.

**Common Definitional Confusions:**
| Term A | Term B | Clarification |
|--------|--------|---------------|
| Pilot | Production | Pilot does not guarantee production |
| Evaluation | Adoption | Evaluation is not commitment |
| Contribution | Implementation | Contributing to standard ≠ implementing it |
| Connected to | Built on | Connectivity layer ≠ native CDM |
| Working group member | Active contributor | Membership may be passive |

---

### Type C: Factual Contradiction

**Definition:** Genuine disagreement about current state — both cannot be true simultaneously.

**Example:**
- Source A: "Bank X went into CDM production in Q3 2024"
- Source B: "Bank X has no CDM in production"

**Resolution:** One source is wrong. Requires investigation.

**Classification Impact:** Cannot classify with confidence until resolved; reduce confidence by 15-25%.

---

## Step 3: Resolution Approach by Type

### For Temporal Contradictions

1. Order sources chronologically
2. Identify the most recent authoritative statement
3. Document the evolution (bank's position changed)
4. Use most recent status for classification
5. Note trajectory in assessment

**Template:**
```markdown
TEMPORAL CONTRADICTION RESOLUTION

Source A: [Summary] ([Date])
Source B: [Summary] ([Date])

Resolution: These sources describe different points in time.
Evolution: [Bank] [previous position] as of [earlier date], but [current position] as of [later date].

Classification basis: Using [later date] status: [Classification]
Trajectory note: [Accelerating/Decelerating/Stable]
```

---

### For Definitional Contradictions

1. Identify the precise claim of each source
2. Clarify terminology
3. Determine if claims can both be true
4. If yes, synthesize both into complete picture
5. If no, treat as factual contradiction

**Template:**
```markdown
DEFINITIONAL CONTRADICTION RESOLUTION

Source A claims: [Precise claim]
Source B claims: [Precise claim]

Terminology analysis:
- "[Term A]" means: [Definition]
- "[Term B]" means: [Definition]

Resolution: These claims [are/are not] actually contradictory because [explanation].

Synthesized understanding: [Bank] is [complete picture incorporating both claims].

Classification basis: [How this informs classification]
```

---

### For Factual Contradictions

1. Assess source reliability (use matrix above)
2. Search for additional sources that corroborate either claim
3. If one source clearly prevails, use it and document why
4. If neither prevails, reduce confidence and flag uncertainty
5. Consider whether both sources could be partially correct

**Template:**
```markdown
FACTUAL CONTRADICTION RESOLUTION

Source A claims: [Claim] (Tier [X], Date: [Y])
Source B claims: [Contradicting claim] (Tier [X], Date: [Y])

Reliability comparison:
- Source A: [Assessment]
- Source B: [Assessment]

Additional search for corroboration:
- Search: [Query]
- Result: [Corroborates A / Corroborates B / Neither]

Resolution:
[ ] Source A prevails because: [Reasoning]
[ ] Source B prevails because: [Reasoning]
[ ] Unresolved — both sources have merit

Confidence impact: [Reduced by X% due to unresolved/resolved contradiction]

Classification: [Classification] with caveat: [What we're uncertain about]
```

---

## Step 4: Document the Contradiction

All contradictions must be documented in the evidence inventory:

```markdown
## Contradiction Log: [BANK NAME]

### Contradiction 1
- **Type:** [Temporal / Definitional / Factual]
- **Source A:** [ID] - [Summary of claim]
- **Source B:** [ID] - [Summary of claim]
- **Resolution:** [How resolved]
- **Confidence Impact:** [Reduced by X% / No impact]
- **Lingering Uncertainty:** [What remains unclear]

### Contradiction 2
[Repeat as needed]
```

---

## Common Contradiction Patterns

### Pattern 1: Vendor vs. Bank Source

**Situation:** Vendor claims bank as client; bank sources don't confirm.

**Resolution Approach:**
- Vendors have incentive to overstate client engagement
- Bank official sources prevail unless vendor source is very specific
- Search for bank confirmation before accepting vendor claim
- If unconfirmed, note as "vendor-claimed only" with reduced weight

---

### Pattern 2: Old Announcement vs. Current Silence

**Situation:** Bank announced CDM initiative in past; no recent updates.

**Resolution Approach:**
- Old announcements are not automatically invalid
- Search for evidence initiative continued or was cancelled
- If no updates: could be (a) quietly proceeding, (b) stalled, (c) cancelled
- Classify as stalled if >18 months without update; flag for validation

---

### Pattern 3: Press Report vs. Official Source

**Situation:** Trade press reports engagement; official sources don't confirm.

**Resolution Approach:**
- Trade press may have inside information not publicly disclosed
- Or may have misinterpreted/overstated
- Tier 1 official sources prevail over Tier 2 press
- But press report from reputable source raises probability even without confirmation

---

### Pattern 4: Different Subsidiaries/Regions

**Situation:** Evidence of CDM work in one region, not others.

**Resolution Approach:**
- Large banks may have different approaches by region/subsidiary
- Identify which entity the evidence applies to
- Classification may need to be entity-specific or note regional variation
- Example: "HSBC EMEA: X, HSBC Asia: Y"

---

## Unresolvable Contradictions

Sometimes contradictions cannot be definitively resolved. In these cases:

1. **Document both positions** transparently
2. **Reduce confidence** by 15-25%
3. **Flag as key uncertainty** in final output
4. **Recommend validation path** (what would resolve it)
5. **Do NOT arbitrarily choose** one source without justification

**Template for Unresolved:**
```markdown
UNRESOLVED CONTRADICTION

The evidence contains a factual contradiction that cannot be definitively resolved:
- [Source A claim]
- [Source B claim]

Neither source clearly prevails because: [Explanation]

Classification: [Best assessment] with REDUCED confidence ([X]%, reduced from [Y]%)

This contradiction is flagged as a KEY UNCERTAINTY.

Resolution path: [What evidence or validation would resolve this]
```
