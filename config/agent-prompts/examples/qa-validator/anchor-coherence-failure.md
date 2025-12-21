# Example: Anchor Coherence Failure Detection

## Context

Phase-end QA validation for Phase 1 (European Tier 1). Testing anchor coherence across 5 banks.

## Input State

- **Phase**: 1 (European Tier 1)
- **Banks Completed**: 5 (Deutsche Bank, HSBC, Barclays, BNP Paribas, UBS)
- **Anchor Points**: BNP Paribas (known ARCHITECT-Active)

---

## Bank Assessments Summary

| Bank | Classification | Confidence | Key Evidence |
|------|---------------|------------|--------------|
| BNP Paribas | ARCHITECT-Active | 85% | Production confirmed, FINOS contributor |
| Deutsche Bank | ARCHITECT-Follower | 78% | Risk.net pilot, ISDA speaker |
| HSBC | ARCHITECT-Follower | 72% | Pilot report, vendor partnership |
| **Barclays** | **ARCHITECT-Follower** | **82%** | Risk.net coverage, job postings |
| UBS | PRAGMATIST | 45% | Vendor-only, no direct evidence |

---

## Anchor Coherence Test

### Anchor Definition

**BNP Paribas** is designated as anchor point because:
1. Official production announcement (verified Tier 1)
2. Named FINOS contributors (3+ individuals)
3. Highest evidence quality in cohort

**Anchor Classification**: ARCHITECT-Active at 85%

### Coherence Rule

> No bank with WEAKER evidence than the anchor should have HIGHER confidence than the anchor.

### Test Execution

| Bank | vs Anchor | Evidence Comparison | Confidence Comparison | Coherent? |
|------|-----------|---------------------|----------------------|-----------|
| Deutsche Bank | Follower < Active | Weaker (no production) | 78% < 85% | YES |
| HSBC | Follower < Active | Weaker (no production) | 72% < 85% | YES |
| **Barclays** | **Follower < Active** | **Weaker (no production)** | **82% < 85%** | **BORDERLINE** |
| UBS | Pragmatist << Active | Much weaker | 45% << 85% | YES |

---

## Barclays Detailed Analysis

### Evidence Inventory

| ID | Finding | Tier | Direction |
|----|---------|------|-----------|
| BAR-001 | Risk.net: "Barclays CDM pilot underway" | 2 | ARCHITECT |
| BAR-002 | ISDA AGM 2024 speaker on CDM | 2 | ARCHITECT |
| BAR-003 | Job posting: "CDM Developer" | 3 | ARCHITECT |
| BAR-004 | Job posting: "CDM Integration Lead" | 3 | ARCHITECT |
| BAR-005 | Delta Capita partnership | 2 | ARCHITECT |
| NULL-1 | No official bank announcement | 1 | PRAGMATIST |

### BNP Paribas Evidence (Anchor)

| ID | Finding | Tier | Direction |
|----|---------|------|-----------|
| BNP-001 | Official press release: production | 1 | ARCHITECT |
| BNP-002 | 3 named FINOS contributors | 1 | ARCHITECT |
| BNP-003 | Annual report CDM mention | 1 | ARCHITECT |
| BNP-004 | Risk.net production confirmation | 2 | ARCHITECT |
| BNP-005 | ISDA CDM working group chair | 2 | ARCHITECT |

### Evidence Quality Comparison

| Dimension | Barclays | BNP Paribas | Winner |
|-----------|----------|-------------|--------|
| Tier 1 evidence | 0 items | 3 items | BNP |
| Tier 2 evidence | 3 items | 2 items | Barclays (count) |
| Official confirmation | NO | YES | BNP |
| Production status | Pilot | Production | BNP |
| FINOS contribution | NO | YES (3 people) | BNP |

**Verdict**: BNP Paribas has definitively stronger evidence.

---

## Coherence Violation Detection

### Issue Identified

**Barclays at 82% is too close to BNP Paribas at 85%** given the evidence gap.

| Metric | Barclays | BNP Paribas | Gap |
|--------|----------|-------------|-----|
| Confidence | 82% | 85% | 3 points |
| Tier 1 items | 0 | 3 | -3 |
| Official confirmation | No | Yes | Major |
| Classification | Follower | Active | 1 level |

**Expected Gap**: Given BNP has production confirmed and Barclays has pilot only, confidence gap should be ~15-20 points, not 3 points.

### Root Cause Analysis

Reviewing Barclays Bayesian calculation:

```
Evidence: 5 ARCHITECT items, 1 PRAGMATIST item
Combined LR: Overcounted job postings
BAR-003 and BAR-004 are similar job postings
Should apply dependency discount: 2 similar items = 1.5x, not 2x
```

**Issue**: Job postings BAR-003 and BAR-004 were treated as independent, but they're from the same source (Barclays careers) at similar time. This inflated the LR.

---

## Violation Report

```markdown
## COHERENCE VIOLATION DETECTED

### Violation Type: ANCHOR_COHERENCE_FAILURE

### Banks Involved
- Anchor: BNP Paribas (ARCHITECT-Active, 85%)
- Violator: Barclays (ARCHITECT-Follower, 82%)

### Issue Description
Barclays confidence (82%) is within 3 points of anchor (85%) despite:
- No Tier 1 evidence (anchor has 3 items)
- No production confirmation (anchor has production)
- Pilot status only (anchor is in production)

### Evidence of Violation
| Criterion | Expectation | Actual |
|-----------|-------------|--------|
| Confidence gap | ≥15 points | 3 points |
| Classification gap | Follower < Active | Correct |
| Evidence gap | Barclays << BNP | Correct |

### Root Cause
Job posting evidence (BAR-003, BAR-004) treated as independent when they should have dependency discount applied.

### Recommended Correction
1. Apply dependency discount to BAR-003/BAR-004 (LR = 1.5x, not 2x)
2. Recalculate Barclays posterior
3. Expected corrected confidence: ~70-72%

### Action Required
- [ ] Recalculate Barclays Bayesian update
- [ ] Apply job posting dependency discount
- [ ] Verify corrected confidence is coherent with anchor
```

---

## Corrected Calculation

### Original Barclays LR Calculation

```
BAR-001 (Risk.net pilot): LR = 5.0
BAR-002 (ISDA speaker): LR = 4.0
BAR-003 (Job posting 1): LR = 2.5
BAR-004 (Job posting 2): LR = 2.5
BAR-005 (Delta Capita): LR = 2.0
NULL-1 (No announcement): LR = 0.33

Combined LR = 5.0 x 4.0 x 2.5 x 2.5 x 2.0 x 0.33 = 82.5
```

### Corrected Calculation (with dependency)

```
BAR-001 (Risk.net pilot): LR = 5.0
BAR-002 (ISDA speaker): LR = 4.0
BAR-003+004 (Job postings, dependent): LR = 3.0 (not 6.25)
BAR-005 (Delta Capita): LR = 2.0
NULL-1 (No announcement): LR = 0.33

Corrected LR = 5.0 x 4.0 x 3.0 x 2.0 x 0.33 = 39.6
Prior odds = 0.667
Posterior odds = 0.667 x 39.6 = 26.4
P(Architect) = 26.4 / 27.4 = 96.4%
Capped at Tier 2: 75%
```

### Corrected Confidence

| Metric | Original | Corrected |
|--------|----------|-----------|
| Combined LR | 82.5 | 39.6 |
| Raw posterior | 98.2% | 96.4% |
| After Tier 2 cap | 82%* | 75% |
| Gap from anchor | 3 points | 10 points |

*Original calculation had error in cap application

---

## Resolution

After applying correction:
- Barclays: ARCHITECT-Follower at 72% (down from 82%)
- Anchor gap: 13 points (acceptable)
- Coherence: RESTORED

**Phase 1 Validation**: PASSED (after correction)
