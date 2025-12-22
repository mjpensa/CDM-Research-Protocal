# SMBC - Framework Integration

## Classification Output

```json
{
  "bank_id": "smbc",
  "classification": "PRAGMATIST",
  "sub_classification": "Traditional (Derivatives Active, Governance Absent)",
  "confidence": 0.65,
  "maturity_score": 1,
  "engagement_type": "traditional"
}
```

## Peer Cohort

### Japanese Banks (Complete)
| Bank | FINOS | ISDA Board | Pattern | Maturity |
|------|-------|------------|---------|----------|
| Nomura | No | Yes | Governance | 2 |
| MUFG | No | Yes | Governance | 2 |
| Mizuho | No | Yes | Governance | 2 |
| SMBC | No | **No** | **Traditional** | **1** |

### Japanese CCPs
| Entity | FINOS | CDM Status |
|--------|-------|------------|
| JSCC | Yes | Production |

## Key Finding
Japanese mega-banks split into two patterns:
1. **ISDA Governance** (Nomura, MUFG, Mizuho): Board representation without FINOS/CDM
2. **Traditional** (SMBC): Active business without governance role

Only JSCC (infrastructure) has adopted CDM. No Japanese bank has CDM deployment.

---
*Framework integration: 2025-12-21*
