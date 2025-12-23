# Bayesian Update: Post-Tier 1 Evidence

**Bank**: Deutsche Bank AG
**Date**: 2025-12-21
**Stage**: Post-Tier 1 Evidence

---

## Prior Probability

| Classification | Probability | Rationale |
|----------------|-------------|-----------|
| ARCHITECT | 35% | Base prior for European G-SIB with derivatives focus |
| PRAGMATIST | 65% | Null hypothesis |

---

## Tier 1 Evidence Summary

### Positive Evidence

| ID | Claim Type | Raw LR | Temporal Weight | Adjusted LR |
|----|------------|--------|-----------------|-------------|
| DB-001 | pilot_or_poc | 10.0 | 0.3 (historical) | 2.0 |
| DB-002 | open_source_contribution | 14.0 | 0.3 (historical) | 2.2 |
| DB-003 | membership_or_participation | 6.0 | 0.3 (historical) | 1.7 |

**Combined Positive LR**: 2.0 × 2.2 × 1.7 = **7.5**

### Null Results (Informative Absence)

| Category | Implication | LR Adjustment |
|----------|-------------|---------------|
| No production deployment | Pilot did not lead to adoption | 0.5 |
| No post-2021 activity | 3+ year gap suggests abandonment | 0.6 |
| No EMIR Refit CDM | Traditional methods used | 0.9 |

**Combined Null LR**: 0.5 × 0.6 × 0.9 = **0.27**

---

## Probability Calculation

### Step 1: Total Likelihood Ratio
```
Total LR = Positive LR × Null LR
Total LR = 7.5 × 0.27 = 2.03
```

### Step 2: Convert Prior to Odds
```
Prior Odds = P(A) / P(~A) = 0.35 / 0.65 = 0.538
```

### Step 3: Calculate Posterior Odds
```
Posterior Odds = Prior Odds × Total LR
Posterior Odds = 0.538 × 2.03 = 1.09
```

### Step 4: Convert to Probability
```
P(Architect | Tier 1) = Posterior Odds / (1 + Posterior Odds)
P(Architect | Tier 1) = 1.09 / (1 + 1.09) = 1.09 / 2.09 = 0.52
```

---

## Post-Tier 1 Probability

| Classification | Probability | Change from Prior |
|----------------|-------------|-------------------|
| **ARCHITECT** | **52%** | +17% |
| PRAGMATIST | 48% | -17% |

---

## Interpretation

The Tier 1 evidence shows a modest shift toward ARCHITECT (from 35% to 52%), but the posterior is barely above the 50% threshold. Key factors:

### Why Not Higher?
1. **Temporal Decay**: All evidence is >3 years old (2020-2021), applying 0.3 weight multiplier
2. **Informative Null Results**: No production deployment, no post-pilot activity, no EMIR Refit CDM approach
3. **Pilot ≠ Production**: FINOS Legend pilot was exploratory, not operational

### Current Assessment
Deutsche Bank demonstrated genuine CDM engagement in 2020-2021 through:
- Pilot participation
- Accepted code contribution (FX Options Averaging Model)
- FINOS board leadership (Russell Green)

However, the 3+ year gap with no visible continuation suggests the pilot did not lead to strategic CDM adoption. The bank may have evaluated CDM and decided not to proceed.

---

## Next Steps

Proceed to Tier 2 Evidence to search for:
1. Trade press coverage of Deutsche Bank derivatives technology
2. Conference presentations on CDM/DRR
3. Vendor partnerships that might indicate CDM direction
4. Named individual updates (Russell Green recent activity)

---

## Confidence Assessment

- **Evidence Quality**: HIGH (official FINOS sources)
- **Temporal Relevance**: LOW (all evidence >3 years old)
- **Corroboration**: MODERATE (multiple independent sources for same pilot)
- **Informative Absence**: HIGH (well-searched null results)
