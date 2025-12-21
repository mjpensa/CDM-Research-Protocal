# Example: Confidence Calibration (6-Step Process)

## Context

Synthesis stage for HSBC. Calculating final calibrated confidence before writing assessment.

## Input State

- **Bank**: HSBC Holdings
- **Bayesian Posterior**: 72%
- **Adversarial Verdict**: UNCHANGED
- **Classification**: ARCHITECT-Follower

---

## Required Inputs

### From evidence.json (trust_metrics)

```json
{
  "trust_metrics": {
    "total_evidence_items": 8,
    "tier1_count": 2,
    "tier2_count": 4,
    "tier3_count": 2,
    "corroboration_rate": 0.75,
    "contradiction_count": 0,
    "flags": []
  }
}
```

### From 4-adversarial/verdict.md

```
Verdict: UNCHANGED
Confidence Adjustment: 0%
Steelman Strength: 5/10
Classification Survives: YES
```

---

## 6-Step Confidence Calibration

### Step 1: Maximum by Tier Cap

**Question**: What is the highest tier of evidence we have?

| Tier | Count | Present? |
|------|-------|----------|
| Tier 1 | 2 | YES |
| Tier 2 | 4 | YES |
| Tier 3 | 2 | YES |

**Highest Tier**: Tier 1
**Maximum Allowed**: 95%
**Bayesian Posterior**: 72%

```
Step 1 Result: 72% (within Tier 1 cap of 95%)
```

### Step 2: Corroboration Adjustment

**Corroboration Rate**: 75% (6/8 items corroborated)

| Rate | Adjustment |
|------|------------|
| ≥80% | +5% |
| 60-79% | +0% (neutral) |
| 40-59% | -5% |
| <40% | -10% |

**Rate**: 75% falls in 60-79% range
**Adjustment**: +0%

```
Step 2 Result: 72% + 0% = 72%
```

### Step 3: Contradiction Adjustment

**Contradictions Detected**: 0

| Status | Adjustment |
|--------|------------|
| No contradictions | +0% |
| All resolved | -5% |
| Some unresolved | -10% to -15% |
| Major unresolved | -20% to -25% |

**Adjustment**: +0%

```
Step 3 Result: 72% + 0% = 72%
```

### Step 4: Adversarial Survival Adjustment

**Adversarial Verdict**: UNCHANGED
**Steelman Strength**: 5/10 (moderate)

| Verdict | Adjustment |
|---------|------------|
| STRENGTHENED | +5% to +10% |
| UNCHANGED | +0% |
| WEAKENED | -5% to -15% |
| REVISED | N/A (classification changes) |

**Adjustment**: +0%

```
Step 4 Result: 72% + 0% = 72%
```

### Step 5: Coherence Check Adjustment

**Anchor Comparison**:
- BNP Paribas (ARCHITECT-Active, 85%) - stronger evidence, higher confidence
- Deutsche Bank (ARCHITECT-Follower, 68%) - similar evidence, similar confidence
- Standard Chartered (PRAGMATIST, 35%) - weaker evidence, lower confidence

**Ordinal Check**:
- HSBC at 72% is between BNP (85%) and Deutsche (68%)
- HSBC evidence is stronger than Deutsche (more Tier 1)
- HSBC confidence should be ≥ Deutsche

**Coherence**: PASSED (no adjustment needed)

| Coherence Status | Adjustment |
|------------------|------------|
| Fully coherent | +0% |
| Minor anomaly | -5% |
| Significant anomaly | -10% |
| Major violation | -15% |

**Adjustment**: +0%

```
Step 5 Result: 72% + 0% = 72%
```

### Step 6: Final Calculation with Floor/Ceiling

**Pre-Final Confidence**: 72%

**Floor**: 20% (minimum for any classification)
**Ceiling**: 95% (maximum allowed)

```
Step 6 Check: 20% ≤ 72% ≤ 95%
Final Confidence: 72%
```

---

## Betting Test

**Question**: Would you bet at the implied odds?

Implied odds for 72% confidence:
- Odds of ARCHITECT: 72:28 = 2.57:1
- If someone offered 2.5:1 that HSBC is ARCHITECT, would you take the bet?

**Assessment**:
- HSBC has 2 Tier 1 evidence items (ISDA participation, Risk.net coverage)
- 4 corroborating Tier 2 items
- Adversarial challenge found no major weaknesses
- No contradictions

**Verdict**: YES, would take 2.5:1 bet on ARCHITECT classification.

**Betting Test**: PASSED

---

## Cross-Bank Consistency Check

| Bank | Classification | Confidence | Evidence Profile |
|------|---------------|------------|------------------|
| BNP Paribas | ARCHITECT-Active | 85% | Production confirmed |
| HSBC | ARCHITECT-Follower | 72% | Pilot + participation |
| Deutsche Bank | ARCHITECT-Follower | 68% | Similar to HSBC |
| Standard Chartered | PRAGMATIST | 35% | No CDM evidence |

**Check**: Does HSBC's 72% fit the ordinal pattern?
- Higher than Deutsche (68%) - YES (slightly stronger evidence)
- Lower than BNP (85%) - YES (no production confirmation)
- Higher than Standard Chartered (35%) - YES (has CDM evidence)

**Cross-Bank Check**: PASSED

---

## Confidence Calibration Summary

| Step | Description | Adjustment | Running Total |
|------|-------------|------------|---------------|
| 1 | Tier cap | 0% | 72% |
| 2 | Corroboration | 0% | 72% |
| 3 | Contradictions | 0% | 72% |
| 4 | Adversarial | 0% | 72% |
| 5 | Coherence | 0% | 72% |
| 6 | Floor/ceiling | 0% | 72% |

**Final Calibrated Confidence**: 72%

---

## Output

**File**: `outputs/phase-1-european-tier1/hsbc/5-synthesis/confidence-calibration.md`

```markdown
# Confidence Calibration: HSBC

## Final Confidence: 72%

### Calibration Breakdown
| Step | Adjustment | Result |
|------|------------|--------|
| Base (Bayesian) | - | 72% |
| Tier cap (95%) | +0% | 72% |
| Corroboration (75%) | +0% | 72% |
| Contradictions (0) | +0% | 72% |
| Adversarial (UNCHANGED) | +0% | 72% |
| Coherence check | +0% | 72% |
| **Final** | - | **72%** |

### Validation
- [x] Betting test passed
- [x] Cross-bank consistency passed
- [x] Within floor/ceiling bounds

### Classification
**ARCHITECT-Follower at 72% confidence**
```
