# Lloyds Banking Group - Bayesian Update: Post-Tier 2

## Prior State (Post-Tier 1)
| Metric | Value |
|--------|-------|
| P(Architect) | 75% |

## Tier 2 Evidence
| ID | Claim | LR |
|----|-------|-----|
| LBG-004 | FINOS event hosting | 1.5 |

## Calculation
```
P(Architect) = 75% × 1.5 / (75% × 1.5 + 25% × 1) = 81.8%
Cap at 75% (no production evidence)
```

## Posterior State
| Metric | Before | After |
|--------|--------|-------|
| P(Architect) | 75% | 75% (capped) |

---
*Generated: 2025-12-21*
