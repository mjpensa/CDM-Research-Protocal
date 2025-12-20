# Bayesian Update: NatWest Group PLC
## Tier B Protocol

**Bank**: NatWest Group PLC
**Date**: 2025-12-19

---

## Prior Probability

**P(Architect | Prior)** = 0.20 (20%)

Rationale for prior:
- Medium derivatives relevance (UK-focused retail/commercial)
- UK regional bank, not global investment bank
- Lower expected CDM involvement than Barclays/HSBC

---

## Evidence Assessment

### Likelihood Ratios from Evidence Gathering

| Evidence Category | P(E|Architect) | P(E|Not Architect) | Likelihood Ratio |
|-------------------|----------------|---------------------|------------------|
| No direct CDM evidence | 0.05 | 0.50 | 0.10 |
| ISDA member but no CDM groups | 0.15 | 0.50 | 0.30 |
| UK EMIR compliance focus | 0.30 | 0.60 | 0.50 |
| Standard vendor usage | 0.20 | 0.50 | 0.40 |
| No technical contributions | 0.05 | 0.50 | 0.10 |
| Industry participation, no CDM lead | 0.25 | 0.50 | 0.50 |

### Combined Likelihood Ratio

Using independence assumption (conservative):
**Combined LR** = 0.10 × 0.30 × 0.50 × 0.40 × 0.10 × 0.50 = **0.0003**

---

## Bayesian Calculation

### Formula
```
P(Architect | Evidence) = P(E|A) × P(A) / [P(E|A) × P(A) + P(E|¬A) × P(¬A)]
```

### Simplified using Likelihood Ratio
```
Posterior Odds = Prior Odds × Likelihood Ratio
Prior Odds = 0.20 / 0.80 = 0.25
Posterior Odds = 0.25 × 0.0003 = 0.000075
Posterior Probability = 0.000075 / (1 + 0.000075) = 0.000075 ≈ 0.0075%
```

### Adjusted Calculation (Conservative Floor)
Given data limitations and potential for hidden evidence, apply conservative floor:
- **Raw Posterior**: 0.0075%
- **Conservative Floor**: 3% (minimum uncertainty given incomplete web search)
- **Adjusted Posterior**: 3%

---

## Updated Probability

**P(Architect | Evidence)** = **3%** (down from 20% prior)

### Confidence Assessment
- **Confidence Level**: MEDIUM
- **Data Quality**: LIMITED (web search unavailable, relying on knowledge base)
- **Key Uncertainty**: Possible undisclosed vendor partnerships or quiet participation

---

## Summary

| Metric | Value |
|--------|-------|
| Prior Probability | 20% |
| Likelihood Ratio | 0.0003 |
| Raw Posterior | 0.0075% |
| Adjusted Posterior | 3% |
| Direction | Strong decrease |
| Confidence | Medium |

**Interpretation**: Evidence strongly suggests NatWest is NOT a CDM Architect. The absence of any direct CDM involvement, combined with the UK regional bank profile and vendor-dependent derivatives infrastructure, indicates NatWest is likely in the "PRAGMATIST" or "Potential Future Adopter" category rather than Architect.
