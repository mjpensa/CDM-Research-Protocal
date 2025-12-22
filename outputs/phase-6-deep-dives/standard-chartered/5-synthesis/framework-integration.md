# Framework Integration: Standard Chartered

**Bank**: Standard Chartered PLC
**Phase**: 6 (Deep Dives)
**Date**: 2025-12-21

---

## Classification Summary

| Field | Value |
|-------|-------|
| Bank ID | standard-chartered |
| Classification | ARCHITECT |
| Subtype | Follower |
| Confidence | 80% |
| Maturity Score | 3 |
| Evidence Count | 4 |

---

## Framework Mapping

```
ARCHITECT ──────────────────────────────────────────────────────────┐
  │                                                                  │
  ├── Native (Production)      : BNP Paribas, JPMorgan, Pictet       │
  ├── Active (Pilot + Build)   : Deutsche Bank (expected)            │
  └── Follower (Contribution)  : Barclays, [STANDARD CHARTERED]      │ ◄── HERE
```

---

## Integration Data

```json
{
  "bank_id": "standard-chartered",
  "classification": "ARCHITECT",
  "subtype": "Follower",
  "confidence": 0.80,
  "maturity_score": 3,
  "region": "Asia",
  "subregion": "Emerging Markets Focus",
  "derivatives_relevance": "Medium",
  "key_evidence": "DRR contributor with BNP/JPMorgan/Pictet; ISDA Board member",
  "evidence_freshness": "current",
  "flags": []
}
```

---

## Export Data

```csv
bank_id,bank_name,phase,classification,subtype,confidence,maturity,region,evidence_count
standard-chartered,Standard Chartered PLC,6,ARCHITECT,Follower,80,3,Asia,4
```

---

*Framework integration completed under CDM Research Protocol v2.3*
