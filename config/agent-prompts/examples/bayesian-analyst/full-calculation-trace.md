# Example: Full Bayesian Calculation Trace

## Context

Post-Tier 2 probability update for Credit Suisse (now UBS). Demonstrating complete calculation methodology with multiple evidence items.

## Input State

- **Bank**: Credit Suisse (pre-merger research)
- **Prior P(Architect)**: 40% (default)
- **Post-Tier 1 P(Architect)**: 52%
- **Current Stage**: Post-Tier 2

---

## Evidence Summary

### Tier 1 Evidence

| ID | Finding | LR | Direction |
|----|---------|-----|-----------|
| CS-001 | No official CDM announcement on cs.com | 0.33 | PRAGMATIST |
| CS-002 | Listed as ISDA member (not CDM working group) | 1.2 | WEAK ARCHITECT |

### Tier 2 Evidence

| ID | Finding | LR | Direction |
|----|---------|-----|-----------|
| CS-003 | Risk.net: "Credit Suisse exploring CDM pilot" | 5.0 | ARCHITECT |
| CS-004 | ISDA AGM 2023: CS speaker on "CDM Implementation Challenges" | 4.0 | ARCHITECT |
| CS-005 | No Waters Technology coverage of CS CDM | 0.8 | WEAK PRAGMATIST |
| CS-006 | Delta Capita partnership for EMIR reporting | 2.0 | ARCHITECT (vendor) |

---

## Bayesian Calculation (8-Step Process)

### Step 1: Establish Prior

```
Prior P(Architect) = 0.40
Prior P(Pragmatist) = 0.60
Prior Odds = P(A) / P(P) = 0.40 / 0.60 = 0.667
```

### Step 2: Identify Evidence Items and LRs

| Evidence | LR | Source of LR |
|----------|-----|--------------|
| CS-001: No official announcement | 0.33 | no_evidence_after_exhaustive_tier1_search |
| CS-002: ISDA member only | 1.2 | general_membership_no_cdm_specific |
| CS-003: Risk.net pilot report | 5.0 | trade_press_pilot_mention |
| CS-004: ISDA AGM speaker | 4.0 | conference_speaker_cdm_topic |
| CS-005: No Waters coverage | 0.8 | no_trade_press_coverage |
| CS-006: Delta Capita partnership | 2.0 | vendor_partnership_confirmed |

### Step 3: Calculate Combined LR

```
Combined LR = 0.33 x 1.2 x 5.0 x 4.0 x 0.8 x 2.0
            = 0.33 x 1.2 x 5.0 x 4.0 x 0.8 x 2.0
            = 12.672
```

### Step 4: Apply Dampening (if needed)

```
Combined LR = 12.672
Threshold for dampening: LR > 100 or LR < 0.01

12.672 is within normal range. No dampening required.
```

### Step 5: Calculate Posterior Odds

```
Posterior Odds = Prior Odds x Combined LR
               = 0.667 x 12.672
               = 8.45
```

### Step 6: Convert to Probability

```
P(Architect | Evidence) = Posterior Odds / (1 + Posterior Odds)
                        = 8.45 / (1 + 8.45)
                        = 8.45 / 9.45
                        = 0.894 = 89.4%
```

### Step 7: Apply Confidence Caps

```
Highest tier with evidence: Tier 2
Tier 2 cap: 75%

Bayesian posterior: 89.4%
Capped posterior: 75% (cap applied)

Reason: Evidence is primarily Tier 2 (trade press, conferences).
No official Tier 1 confirmation limits maximum confidence.
```

### Step 8: Sanity Checks

**Check 1: Direction Consistency**
- 4 items support ARCHITECT (CS-002, CS-003, CS-004, CS-006)
- 2 items support PRAGMATIST (CS-001, CS-005)
- Net direction: ARCHITECT consistent with posterior

**Check 2: Extreme LR Flag**
- No individual LR > 50 or < 0.02
- Combined LR = 12.67 (reasonable)
- CHECK PASSED

**Check 3: Belief Reversal Detection**
- Prior: 40% Architect
- Posterior: 75% Architect
- Shift: +35 percentage points
- Threshold for flag: >40 points
- CHECK PASSED (no flag needed)

**Check 4: Evidence Quality Match**
- Posterior capped at 75% (Tier 2 only)
- Highest evidence is trade press, not official
- Confidence appropriately limited
- CHECK PASSED

---

## Thinking Trace

```
<thinking>
Starting with prior P(Architect) = 0.40, P(Pragmatist) = 0.60
Prior odds = 0.40 / 0.60 = 0.667

Evidence CS-001: No official CDM announcement found
- This is an informative absence from Tier 1 search
- Maps to "no_evidence_after_exhaustive_tier1_search" in tier1_evidence
- LR = 0.33 (moderate Pragmatist evidence)

Evidence CS-002: ISDA member but not CDM working group
- General membership without specific CDM participation
- Maps to "general_membership_no_cdm_specific"
- LR = 1.2 (very weak Architect evidence)

Evidence CS-003: Risk.net reports pilot exploration
- Trade press mentioning pilot is informative
- Maps to "trade_press_pilot_mention"
- LR = 5.0 (moderate Architect evidence)

Evidence CS-004: ISDA AGM speaker on CDM topic
- Conference speaking engagement shows engagement
- Maps to "conference_speaker_cdm_topic"
- LR = 4.0 (moderate Architect evidence)

Evidence CS-005: No Waters Technology coverage
- Absence from another trade press is weak signal
- Maps to "no_trade_press_coverage"
- LR = 0.8 (very weak Pragmatist evidence)

Evidence CS-006: Delta Capita partnership
- Vendor partnership confirmed for EMIR
- Maps to "vendor_partnership_confirmed"
- LR = 2.0 (weak Architect evidence, could be vendor-dependent)

Combined LR = 0.33 x 1.2 x 5.0 x 4.0 x 0.8 x 2.0 = 12.672

Posterior odds = 0.667 x 12.672 = 8.45
P(Architect | Evidence) = 8.45 / 9.45 = 89.4%

Applying Tier 2 cap: 75%

Final P(Architect) = 75%

Sanity check: Moved from 40% to 75%. Shift of 35 points is justified by Risk.net pilot report and ISDA speaking engagement. The Tier 2 cap appropriately limits confidence given lack of official confirmation.

Classification leaning: ARCHITECT (likely Follower variant given vendor partnership)
</thinking>
```

---

## Output File

**File**: `outputs/phase-[N]/credit-suisse/2-bayesian/post-tier2-update.md`

```markdown
## Post-Tier 2 Bayesian Update

### Summary
- Prior P(Architect): 40%
- Post-Tier 1 P(Architect): 52%
- Post-Tier 2 P(Architect): 75% (capped)

### Calculation
| Evidence | LR | Cumulative |
|----------|-----|-----------|
| CS-001 | 0.33 | 0.33 |
| CS-002 | 1.2 | 0.40 |
| CS-003 | 5.0 | 1.98 |
| CS-004 | 4.0 | 7.92 |
| CS-005 | 0.8 | 6.34 |
| CS-006 | 2.0 | 12.67 |

Combined LR: 12.67
Raw Posterior: 89.4%
Applied Cap: Tier 2 (75%)
Final Posterior: 75%

### Classification Signal
ARCHITECT-Follower (75% confidence)
Variant: Vendor-Dependent (Delta Capita partnership)

### Proceed Decision
P(Architect) = 75% < 80% threshold
CONTINUE TO TIER 3
```
