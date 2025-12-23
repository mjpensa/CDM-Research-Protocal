# Société Générale - Bayesian Update 2 (Post-Tier 2)

## Prior Probability
P(Architect) = 48% (from post-Tier 1 update)

## New Evidence (Tier 2)

### Evidence Item: SG-T2-001 (Derivatives Industry Recognition)
**Claim**: Risk.net Derivatives Client Clearer of Year 2024
**Direction**: NEUTRAL
**Likelihood Ratio**: 1.0 (derivatives capability without CDM specificity)

### Null Results

| Search | Implication | LR |
|--------|-------------|-----|
| No Regnosys partnership | Not using CDM vendors | 0.5 |
| No CDM conference speaking | No community engagement | 0.6 |
| Clearing/post-trade focus | Different priorities than CDM | 0.8 |

**Combined Null Result LR**: 0.5 x 0.6 x 0.8 = 0.24

## Bayesian Calculation

### Combined Tier 2 LR
- Evidence LR: 1.0 (neutral)
- Null Results LR: 0.24
- **Combined LR**: 1.0 x 0.24 = 0.24

### Posterior Calculation
```
Prior Odds = 0.48 / 0.52 = 0.923
Posterior Odds = 0.923 x 0.24 = 0.222
P(Architect) = 0.222 / (1 + 0.222) = 18.1%
```

## Updated Probability

| Metric | Value |
|--------|-------|
| Prior P(Architect) | 48% |
| Tier 2 Combined LR | 0.24 |
| **Posterior P(Architect)** | **18%** |
| P(Pragmatist) | 82% |

## Interpretation

Tier 2 evidence substantially reduced P(Architect) from 48% to 18%:

1. **Technology Focus Clarity**: SG's derivatives technology investments are in clearing and post-trade operations, not CDM standardization.

2. **Vendor Gap**: Unlike Barclays or Credit Suisse, no Regnosys partnership indicating CDM tooling adoption.

3. **Community Absence**: No speakers at CDM Showcase despite active FINOS membership suggests FINOS engagement is infrastructure-focused (CCC), not CDM-focused.

4. **BNP Paribas Contrast**: BNP has visible CDM engagement; SG's silence is informative given they operate in the same French market.

## Trajectory

```
35% (prior) → 48% (post-Tier 1) → 18% (post-Tier 2)
```

The FINOS membership created uplift, but Tier 2 null results corrected this as we found no CDM-specific engagement.

---
*Generated: 2024-12-21*
*Prior: 48% | LR: 0.24 | Posterior: 18%*
