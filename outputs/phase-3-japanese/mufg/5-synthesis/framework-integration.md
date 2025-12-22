# MUFG - Framework Integration

## Classification Output

```json
{
  "bank_id": "mufg",
  "classification": "PRAGMATIST",
  "sub_classification": "ISDA Governance (Board Member)",
  "confidence": 0.70,
  "maturity_score": 2,
  "engagement_type": "isda_governance"
}
```

## Evidence Integration

### Claim Type Summary
| Claim Type | Count | Highest Tier |
|------------|-------|--------------|
| membership_or_participation | 2 | 1 |
| vendor_proxy_signal | 3 | 2 |

## Peer Cohort

### Japanese Banks
| Bank | FINOS Status | ISDA Board | Classification |
|------|--------------|------------|----------------|
| MUFG | Not Member | Yes (2025) | PRAGMATIST (Governance) |
| Nomura | Not Member | Yes | PRAGMATIST (Governance) |
| Mizuho | TBD | TBD | TBD |
| SMBC | TBD | TBD | TBD |

### Japanese CCPs
| Entity | FINOS Status | CDM Status |
|--------|--------------|------------|
| JSCC | Member (2024) | Production |

### Similar Pattern Banks
| Bank | Pattern Match | Classification |
|------|---------------|----------------|
| Nomura | ISDA governance, no FINOS | PRAGMATIST (Governance) |
| HSBC | ISDA governance, no FINOS | PRAGMATIST (Governance) |

---
*Framework integration: 2025-12-21*
