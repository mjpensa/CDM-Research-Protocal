# NatWest Group - Post-Tier 1 Bayesian Update

## Prior Probabilities
| Classification | Prior |
|----------------|-------|
| ARCHITECT | 25% |
| PRAGMATIST | 65% |
| OBSERVER | 10% |

## Tier 1 Evidence Summary
| Evidence | LR(ARCHITECT) | LR(PRAGMATIST) | LR(OBSERVER) |
|----------|---------------|----------------|--------------|
| FINOS Gold Member | 0.9 | 1.4 | 0.4 |
| FCA/BOE DRR Pilot (historical) | 1.0 | 1.1 | 0.8 |
| Fluxnova Contribution | 1.2 | 1.3 | 0.3 |
| Git Proxy Engagement | 1.1 | 1.2 | 0.4 |

## Likelihood Ratio Analysis

### FINOS Gold Membership (LR_A=0.9, LR_P=1.4)
- ARCHITECT banks tend to have higher FINOS tiers (Platinum) or CDM contribution
- PRAGMATIST banks commonly hold Gold membership without CDM focus
- Favors PRAGMATIST

### Fluxnova Contribution (LR_A=1.2, LR_P=1.3)
- Shows active FINOS contributor capability
- However, contribution is NOT CDM-specific
- Process orchestration (Fluxnova) vs derivatives standardization (CDM)
- Slight uplift to both, more to PRAGMATIST

### Historical DRR Pilot (LR_A=1.0, LR_P=1.1)
- 2018-2019 participation shows awareness but no follow-through
- Neutral for ARCHITECT, slight positive for PRAGMATIST

## Posterior Calculation

### Combined LR
| Classification | Combined LR |
|----------------|-------------|
| ARCHITECT | 0.9 × 1.0 × 1.2 × 1.1 = 1.19 |
| PRAGMATIST | 1.4 × 1.1 × 1.3 × 1.2 = 2.40 |
| OBSERVER | 0.4 × 0.8 × 0.3 × 0.4 = 0.04 |

### Posterior (Unnormalized)
| Classification | Prior × LR |
|----------------|------------|
| ARCHITECT | 0.25 × 1.19 = 0.298 |
| PRAGMATIST | 0.65 × 2.40 = 1.560 |
| OBSERVER | 0.10 × 0.04 = 0.004 |

### Normalized Posterior
| Classification | Posterior |
|----------------|-----------|
| ARCHITECT | 16% |
| PRAGMATIST | 84% |
| OBSERVER | <1% |

## Key Update
Strong FINOS engagement (Fluxnova, Git Proxy) WITHOUT CDM contribution significantly increases PRAGMATIST probability. Active open source culture makes OBSERVER implausible.

---
*Generated: 2025-12-21*
