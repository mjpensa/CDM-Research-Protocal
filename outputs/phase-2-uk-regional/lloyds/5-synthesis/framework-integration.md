# Lloyds Banking Group - Framework Integration

## Classification Output

```json
{
  "bank_id": "lloyds",
  "classification": "PRAGMATIST",
  "sub_classification": "Ecosystem (FINOS + OSPO)",
  "confidence": 0.75,
  "maturity_score": 2,
  "engagement_type": "ecosystem_ospo"
}
```

## Evidence Integration

### Claim Type Summary
| Claim Type | Count | Highest Tier |
|------------|-------|--------------|
| membership_or_participation | 1 | 1 |
| pilot_or_poc | 1 | 1 (historical) |
| hiring_signal | 1 | 3 |

### Tier Distribution
| Tier | Items | Weight |
|------|-------|--------|
| 1 | 2 | 1.0 / 0.3 |
| 2 | 2 | 1.0 |
| 3 | 1 | 0.8 |

## Bayesian Integration

### Prior → Posterior
| Stage | P(ARCHITECT) | P(PRAGMATIST) | P(OBSERVER) |
|-------|--------------|---------------|-------------|
| Prior | 25% | 50% | 25% |
| Post-Tier1 | 30% | 55% | 15% |
| Post-Tier2 | 25% | 65% | 10% |
| Post-Tier3 | 20% | 75% | 5% |

### Key Likelihood Ratios
| Evidence | LR(ARCHITECT) | LR(PRAGMATIST) |
|----------|---------------|----------------|
| FINOS Gold | 0.8 | 1.5 |
| No CDM contribution | 0.3 | 1.2 |
| OSPO active | 0.6 | 1.3 |
| DRR pilot (historical) | 1.0 | 1.1 |

## Vendor Matrix Integration

### Vendor Dependencies
| Vendor | Relationship | CDM Relevance |
|--------|--------------|---------------|
| Red Hat | OSPO partnership | Low (general open source) |

### Platform Status
- **Primary Systems**: Traditional banking platforms
- **CDM Layer**: None identified
- **Reporting**: Standard regulatory reporting

## Peer Cohort

### UK Regional Banks
| Bank | FINOS Status | CDM Activity | Classification |
|------|--------------|--------------|----------------|
| Lloyds | Gold | None | PRAGMATIST (Ecosystem) |
| NatWest | TBD | TBD | TBD |

### Similar Pattern Banks
| Bank | Pattern Match | Classification |
|------|---------------|----------------|
| Société Générale | FINOS member, no CDM contribution | PRAGMATIST (Ecosystem) |
| HSBC | ISDA governance, no FINOS | PRAGMATIST (Governance Gap) |

## Confidence Framework

### Tier-Based Maximum
- Highest tier present: Tier 1 (FINOS membership)
- Tier 1 maximum: 95%
- Applied confidence: 75% (well below maximum)

### Evidence Freshness
| Source | Age | Weight |
|--------|-----|--------|
| FINOS Gold (2023) | ~20 months | 0.8 |
| OSPO (2024) | ~7 months | 1.0 |
| DRR Pilot (2018-2019) | ~6 years | 0.3 |

### Corroboration Status
- FINOS membership: Corroborated (official + press)
- OSPO activity: Corroborated (vendor + press)
- CDM absence: Corroborated (multiple searches)

## Risk Assessment

### Overconfidence Risk: LOW
- Classification based on clear positive and negative evidence
- No contradictory signals
- Pattern matches peer cohort

### Future Movement Indicators
| Indicator | Current | Watch For |
|-----------|---------|-----------|
| FINOS tier upgrade | Gold | Platinum |
| CDM commits | None | Any contribution |
| Job postings | General open source | CDM-specific roles |

---
*Framework integration: 2025-12-21*
*Schema version: 3.1*
