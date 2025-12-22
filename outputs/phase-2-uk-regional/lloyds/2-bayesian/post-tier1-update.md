# Lloyds Banking Group - Bayesian Update: Post-Tier 1

## Prior State
| Metric | Value |
|--------|-------|
| P(Architect) | 30% |
| P(Pragmatist) | 70% |

## Tier 1 Evidence
| ID | Claim | LR | Temporal Weight |
|----|-------|-----|-----------------|
| LBG-001 | FINOS Gold member | 4.0 | 0.8 |
| LBG-002 | Active OSPO | 2.5 | 1.0 |
| LBG-003 | FCA DRR pilot | 3.0 | 0.3 |

## Calculation
```
LR_weighted = (4.0^0.8) × (2.5^1.0) × (3.0^0.3) = 2.64 × 2.5 × 1.39 = 9.18
Prior odds = 0.30 / 0.70 = 0.43
Posterior odds = 0.43 × 9.18 = 3.95
P(Architect) = 3.95 / (1 + 3.95) = 79.8%
```

Cap at 75% (no production evidence)

## Posterior State
| Metric | Before | After |
|--------|--------|-------|
| P(Architect) | 30% | 75% |

---
*Generated: 2025-12-21*
