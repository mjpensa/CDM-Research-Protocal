# HSBC - Bayesian Update: Post-Tier 1

## Prior State
| Metric | Value |
|--------|-------|
| P(Architect) | 35% |
| P(Pragmatist) | 65% |
| Reasoning | UK G-SIB, global derivatives presence |

## Tier 1 Evidence

| ID | Claim | LR | Direction |
|----|-------|-----|-----------|
| HSBC-001 | FCA/BOE DRR pilot (2018-2019) | 3.0 | SUPPORTS |
| HSBC-002 | ISDA Board Chair (Jeroen Krens) | 4.0 | SUPPORTS |
| HSBC-003 | NOT a FINOS member | 0.6 | CONTRADICTS |

## Bayesian Calculation

### Step 1: Calculate Combined Likelihood Ratio
```
LR_combined = 3.0 × 4.0 × 0.6 = 7.2
```

### Step 2: Apply Temporal Weighting
| Evidence | Age | Weight |
|----------|-----|--------|
| HSBC-001 | Historical (2018-2019) | 0.3 |
| HSBC-002 | Current (2024) | 1.0 |
| HSBC-003 | Current (2024) | 1.0 |

```
LR_weighted = (3.0^0.3) × (4.0^1.0) × (0.6^1.0)
LR_weighted = 1.39 × 4.0 × 0.6
LR_weighted = 3.34
```

### Step 3: Update Probability
```
Prior odds = 0.35 / 0.65 = 0.538
Posterior odds = 0.538 × 3.34 = 1.80
P(Architect) = 1.80 / (1 + 1.80) = 64.3%
```

### Step 4: Apply Confidence Cap
No production evidence → Cap at 75% (Tier 2 level)
Current: 64% < 75% → No cap needed

## Posterior State

| Metric | Before | After |
|--------|--------|-------|
| P(Architect) | 35% | 64% |
| P(Pragmatist) | 65% | 36% |

## Key Finding: "Governance Leadership" Pattern

HSBC exhibits:
- ISDA Board Chair role (highest governance position)
- Historical DRR pilot participation
- No FINOS membership (contradicting signal)
- No CDM technical engagement

This suggests governance-focused engagement rather than technical adoption.

---
*Bayesian Update Complete*
*P(Architect) = 64%*
*Generated: 2025-12-21*
