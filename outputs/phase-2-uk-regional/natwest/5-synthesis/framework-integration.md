# NatWest Group - Framework Integration

## Classification Output

```json
{
  "bank_id": "natwest",
  "classification": "PRAGMATIST",
  "sub_classification": "Ecosystem (Active FINOS Contributor)",
  "confidence": 0.78,
  "maturity_score": 2,
  "engagement_type": "ecosystem_active_contributor"
}
```

## Evidence Integration

### Claim Type Summary
| Claim Type | Count | Highest Tier |
|------------|-------|--------------|
| open_source_contribution | 2 | 1 |
| membership_or_participation | 2 | 1 |
| pilot_or_poc | 1 | 1 (historical) |
| vendor_proxy_signal | 2 | 2 |
| hiring_signal | 1 | 3 |

### Tier Distribution
| Tier | Items | Weight |
|------|-------|--------|
| 1 | 4 | 1.0 / 0.8 / 0.3 |
| 2 | 3 | 1.0 |
| 3 | 1 | 0.8 |

## Bayesian Integration

### Prior → Posterior
| Stage | P(ARCHITECT) | P(PRAGMATIST) | P(OBSERVER) |
|-------|--------------|---------------|-------------|
| Prior | 25% | 65% | 10% |
| Post-Tier1 | 16% | 84% | <1% |
| Post-Tier2 | 7% | 93% | <1% |
| Post-Tier3 | 10% | 88% | 2% |

### Key Likelihood Ratios
| Evidence | LR(ARCHITECT) | LR(PRAGMATIST) |
|----------|---------------|----------------|
| FINOS Gold | 0.9 | 1.4 |
| Fluxnova Contribution | 1.2 | 1.3 |
| No CDM contribution | 0.3 | 1.2 |
| Traditional EMIR reporting | 0.6 | 1.1 |

## Vendor Matrix Integration

### Vendor Dependencies
| Vendor | Relationship | CDM Relevance |
|--------|--------------|---------------|
| No CDM vendor identified | - | - |

### Platform Status
- **Primary Systems**: NatWest Markets platforms
- **CDM Layer**: None identified
- **Reporting**: Traditional EMIR Trade Reporting Service

## Peer Cohort

### UK Regional Banks
| Bank | FINOS Status | FINOS Contributions | Classification |
|------|--------------|---------------------|----------------|
| NatWest | Gold | Active (Fluxnova, Git Proxy) | PRAGMATIST (Active) |
| Lloyds | Gold | None (passive) | PRAGMATIST (Ecosystem) |

### Similar Pattern Banks
| Bank | Pattern Match | Classification |
|------|---------------|----------------|
| Société Générale | FINOS member, no CDM | PRAGMATIST (Ecosystem) |
| HSBC | Governance role, no FINOS CDM | PRAGMATIST (Governance) |

### Differentiation
NatWest is unique in exhibiting:
- Strongest FINOS engagement without CDM
- "Active Contributor" vs "Passive Member" pattern
- Clear capability but deliberate non-adoption

## Confidence Framework

### Tier-Based Maximum
- Highest tier present: Tier 1 (FINOS membership + contributions)
- Tier 1 maximum: 95%
- Applied confidence: 78% (well below maximum)

### Evidence Freshness
| Source | Age | Weight |
|--------|-----|--------|
| Fluxnova (2025) | <2 months | 1.0 |
| Git Proxy (2024) | ~12 months | 1.0 |
| FINOS Gold (2021) | ~4 years | 0.8 |
| DRR Pilot (2018-2019) | ~6 years | 0.3 |

### Corroboration Status
- FINOS membership: Corroborated (official + press + presentations)
- FINOS contributions: Corroborated (FINOS press + project pages)
- CDM absence: Corroborated (multiple searches)

## Risk Assessment

### Overconfidence Risk: LOW
- Clear positive evidence (FINOS contributions)
- Clear negative evidence (no CDM)
- Pattern is coherent and distinctive

### Future Movement Indicators
| Indicator | Current | Watch For |
|-----------|---------|-----------|
| FINOS tier | Gold | Platinum upgrade |
| CDM working group | None | Participation announced |
| Job postings | General quant | CDM-specific roles |
| Fluxnova scope | Process orchestration | Financial standardization |

---
*Framework integration: 2025-12-21*
*Schema version: 3.1*
