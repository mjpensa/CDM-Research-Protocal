# Framework Integration: BBVA

**Bank**: Banco Bilbao Vizcaya Argentaria S.A.
**Phase**: 5 (Spanish)
**Date**: 2025-12-21

---

## Classification Summary

| Field | Value |
|-------|-------|
| Bank ID | bbva |
| Classification | PRAGMATIST |
| Subtype | Traditional |
| Confidence | 45% |
| Maturity Score | 1 |
| Evidence Count | 4 |
| CDM Evidence | 0 |

---

## Framework Mapping

```
PRAGMATIST ─────────────────────────────────────────────────────────┐
  │                                                                  │
  ├── ISDA Governance          : Nomura, MUFG, Credit Agricole       │
  ├── Ecosystem                : NatWest, Lloyds, Santander          │
  ├── Vendor-Dependent         : HSBC                                │
  └── Traditional              : ING, SMBC, Commerzbank, [BBVA]      │ ◄── HERE
                                                                     │
OBSERVER ───────────────────────────────────────────────────────────┤
  │                                                                  │
  └── Membership Only          : (Near-boundary: BBVA 47%)           │
```

---

## Phase 5 Summary

| Bank | Classification | Subtype | Confidence | Key Evidence |
|------|---------------|---------|------------|--------------|
| Santander | PRAGMATIST | Ecosystem | 55% | DRR Pilot 2022 |
| BBVA | PRAGMATIST | Traditional | 45% | None (swap dealer) |

**Spanish Cohort Pattern**: Divergent CDM strategies between peers. Santander engaged with UK DRR pilot; BBVA did not.

---

## Integration Data

```json
{
  "bank_id": "bbva",
  "classification": "PRAGMATIST",
  "subtype": "Traditional",
  "confidence": 0.45,
  "maturity_score": 1,
  "region": "Europe",
  "subregion": "Spain",
  "derivatives_relevance": "Medium",
  "key_evidence": "None (classification based on derivatives operations)",
  "evidence_freshness": "N/A",
  "flags": ["LOW_CONFIDENCE", "OBSERVER_BOUNDARY", "NO_CDM_EVIDENCE"],
  "alternative": {"classification": "OBSERVER", "probability": 0.47}
}
```

---

## Export Data

```csv
bank_id,bank_name,phase,classification,subtype,confidence,maturity,region,evidence_count
bbva,Banco Bilbao Vizcaya Argentaria S.A.,5,PRAGMATIST,Traditional,45,1,Europe,4
```

---

*Framework integration completed under CDM Research Protocol v2.3*
