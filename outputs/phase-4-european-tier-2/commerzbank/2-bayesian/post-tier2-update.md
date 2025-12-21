# Bayesian Update: Post-Tier 2 - Commerzbank AG

**Bank:** Commerzbank AG
**Phase:** 4 - European Tier 2
**Update Date:** 2025-12-20

---

## Prior Probability (Post-Tier 1)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| P(ARCHITECT) | 0.15 | No Tier 1 evidence found |
| P(PRAGMATIST) | 0.85 | Default assumption maintained |

## Tier 2 Evidence Summary

| Evidence ID | Description | Direction | Likelihood Ratio |
|-------------|-------------|-----------|------------------|
| CBK-001 | Murex MX.3 platform migration (May 2024) | SUPPORTS_PRAGMATIST | 0.3 |

## Posterior Calculation

```
P(ARCHITECT|E) = P(E|ARCHITECT) × P(ARCHITECT) / P(E)

Where:
- P(E|ARCHITECT) = 0.1 (Architects unlikely to migrate to traditional platforms)
- P(E|PRAGMATIST) = 0.35 (Pragmatists commonly use vendor platforms)
- LR = 0.1 / 0.35 = 0.29 ≈ 0.3

Prior odds = 0.15 / 0.85 = 0.176
Posterior odds = 0.176 × 0.3 = 0.053

P(ARCHITECT|E) = 0.053 / (1 + 0.053) = 0.050 ≈ 5.0%
P(PRAGMATIST|E) = 0.95 ≈ 95.0%
```

## Updated Probabilities

| Parameter | Prior | Posterior | Change |
|-----------|-------|-----------|--------|
| P(ARCHITECT) | 0.15 | 0.05 | -0.10 |
| P(PRAGMATIST) | 0.85 | 0.95 | +0.10 |

## Analysis

The Murex MX.3 migration is strong evidence for PRAGMATIST classification:
- Traditional vendor platform migration
- No CDM layer mentioned despite Murex having CDM capabilities
- Partnership with Murex, TeamTek, and Infosys (full outsource model)
- Covers FX, FX derivatives, equities, commodities

Key insight: Murex MX.3 **has** CDM capabilities, but Commerzbank announcement makes no mention of CDM adoption, suggesting traditional platform usage.

## Decision

**Classification determined: PRAGMATIST (Vendor-Dependent)** at 50% confidence (Tier 2 maximum for vendor proxy signal).

Tier 3 searches not necessary - classification is clear from vendor migration evidence.
