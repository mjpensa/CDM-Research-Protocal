# UBS - Bayesian Update 2 (Post-Tier 2)

## Prior Probability
P(Architect) = 95% (from post-Tier 1 update, capped)

## New Evidence (Tier 2)

### Evidence Item: UBS-T2-001 (Derivatives House of Year)
**Direction**: NEUTRAL
**Likelihood Ratio**: 1.5

### Null Results
- No CDM Showcase speaking: LR = 0.9 (mild negative)
- No vendor partnerships: LR = 0.95 (very mild negative)

## Bayesian Calculation

### Combined Tier 2 LR
```
LR = 1.5 x 0.9 x 0.95 = 1.28
```

### Posterior Calculation
```
Prior Odds = 0.95 / 0.05 = 19.0
Posterior Odds = 19.0 x 1.28 = 24.3
P(Architect) = 24.3 / (1 + 24.3) = 96%

Applying 95% ceiling:
P(Architect) = 95% (unchanged)
```

## Updated Probability

| Metric | Value |
|--------|-------|
| Prior P(Architect) | 95% |
| Tier 2 Combined LR | 1.28 |
| **Posterior P(Architect)** | **95%** (at ceiling) |
| P(Pragmatist) | 5% |

## Interpretation

Tier 2 evidence is essentially neutral - it doesn't significantly change the classification. The strong Tier 1 evidence (CDM contributions, FINOS Platinum) drives the classification.

## Key Observation

The absence of CDM Showcase speaking is notable but not disqualifying. UBS's CDM engagement appears to be:
- Technical contributions (code)
- Governance participation (TOC)
- Rather than: public speaking/evangelism

This is a valid form of ARCHITECT engagement - contributing to the standard rather than promoting it.

---
*Generated: 2024-12-21*
*Prior: 95% | LR: 1.28 | Posterior: 95%*
