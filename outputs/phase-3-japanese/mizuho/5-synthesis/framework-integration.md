# Mizuho Financial Group - Framework Integration

## Classification Output

```json
{
  "bank_id": "mizuho",
  "classification": "PRAGMATIST",
  "sub_classification": "ISDA Governance (Board Member)",
  "confidence": 0.70,
  "maturity_score": 2,
  "engagement_type": "isda_governance"
}
```

## Peer Cohort

### Japanese Banks (Complete)
| Bank | FINOS Status | ISDA Board | Classification |
|------|--------------|------------|----------------|
| Nomura | Not Member | Yes | PRAGMATIST (Governance) |
| MUFG | Not Member | Yes (2025) | PRAGMATIST (Governance) |
| Mizuho | Not Member | Yes (2023) | PRAGMATIST (Governance) |
| SMBC | TBD | TBD | TBD |

### Japanese CCPs
| Entity | FINOS Status | CDM Status |
|--------|--------------|------------|
| JSCC | Member (2024) | Production |

## Key Finding
Japanese mega-banks uniformly exhibit "ISDA Governance" pattern - strong ISDA Board presence without FINOS membership or CDM adoption. Infrastructure providers (JSCC) are driving CDM adoption in Japan, not banks.

---
*Framework integration: 2025-12-21*
