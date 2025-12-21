# Bayesian Update: Post-Tier 1 Evidence

**Bank**: UBS Group AG
**Date**: 2025-12-20
**Prior P(ARCHITECT)**: 10%

---

## Tier 1 Evidence Summary

| ID | Evidence | Direction | LR |
|----|----------|-----------|-----|
| UBS-001 | ISDA/Digital Asset CDM clearing pilot (Oct 2020) with Vinay Srinivas endorsement | SUPPORTS_ARCHITECT | 1.8 |
| UBS-003 | Credit Suisse integration: largest data migration in financial services, consuming all tech capacity through 2026 | SUPPORTS_PRAGMATIST | 0.5 |

## Likelihood Ratio Calculation

**Combined LR (Tier 1)** = 1.8 × 0.5 = **0.9**

## Posterior Calculation

```
Prior odds = 0.10 / 0.90 = 0.111
Posterior odds = 0.111 × 0.9 = 0.100
Posterior P(ARCHITECT) = 0.100 / (1 + 0.100) = 0.091 = 9.1%
```

## Updated Probability

| Metric | Value |
|--------|-------|
| **P(ARCHITECT)** | 9% |
| **P(PRAGMATIST)** | 91% |
| **Direction of Movement** | Decreased (10% → 9%) |

## Key Insights

1. **Historical but Not Current**: 2020 DAML pilot with Vinay Srinivas shows past CDM engagement, but it was 5+ years ago
2. **Integration Constraint Dominates**: UBS-003 (Tier 1, current, specific) weighs heavily - integration consuming ALL technology capacity through 2026
3. **Hypothesis Confirmed**: The research hypothesis that "Credit Suisse integration consuming CDM investment capacity" is validated by current evidence
4. **Temporal Decay**: 2020 evidence has aged considerably; with no follow-up signals, past pilot interest does not indicate current adoption

## Confidence Assessment

- **Tier 1 Evidence Quality**: Moderate (mixed signals: historical positive + current constraint)
- **Highest Tier Cap**: 95% (Tier 1 present)
- **Applied Confidence**: 40% (integration constraint dominates; historical pilot too stale)

---

*Proceeding to Tier 2 evidence gathering.*
