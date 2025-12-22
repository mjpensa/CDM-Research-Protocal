# NatWest Group - Post-Tier 3 Bayesian Update

## Prior (from Tier 2)
| Classification | Prior |
|----------------|-------|
| ARCHITECT | 7% |
| PRAGMATIST | 93% |
| OBSERVER | <1% |

## Tier 3 Evidence Summary
| Evidence | LR(ARCHITECT) | LR(PRAGMATIST) |
|----------|---------------|----------------|
| Quant Analyst Hiring (Python/C++) | 1.0 | 1.0 |

## Likelihood Ratio Analysis

### Quant Analyst Hiring (LR_A=1.0, LR_P=1.0)
- Standard derivatives technology roles
- Python and C++ are common in financial services
- No CDM-specific requirements in postings
- Neutral evidence - doesn't distinguish classifications

## Posterior Calculation

### Combined LR (Tier 3)
| Classification | Combined LR |
|----------------|-------------|
| ARCHITECT | 1.0 |
| PRAGMATIST | 1.0 |

### Normalized Posterior (unchanged)
| Classification | Posterior |
|----------------|-----------|
| ARCHITECT | 7% |
| PRAGMATIST | 93% |
| OBSERVER | <1% |

## Final Probability Assessment

Given the limited Tier 3 signal, apply confidence adjustment:

| Classification | Raw Posterior | Adjusted |
|----------------|---------------|----------|
| ARCHITECT | 7% | 10% |
| PRAGMATIST | 93% | 88% |
| OBSERVER | <1% | 2% |

**Reasoning**: Slight regression toward mean due to:
1. Active FINOS engagement suggests above-average awareness
2. Could pivot to CDM if business case emerges
3. But no current CDM signals

## Summary
| Metric | Value |
|--------|-------|
| P(ARCHITECT) | 10% |
| P(PRAGMATIST) | 88% |
| Classification | PRAGMATIST |
| Sub-Classification | Ecosystem (Active Contributor) |

---
*Generated: 2025-12-21*
