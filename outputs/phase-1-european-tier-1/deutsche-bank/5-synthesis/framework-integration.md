# Framework Integration: Deutsche Bank AG

**Bank:** Deutsche Bank AG
**Phase:** 1 - European Tier 1
**Date:** 2025-12-21

---

## Framework v20 Claim Assessment

### Original Claim

| Field | Value |
|-------|-------|
| Bank | Deutsche Bank |
| Claim | "Pilot; production expected 2025" |
| Classification | ARCHITECT (implied) |

### Verification Status

| Aspect | Evidence Found | Status |
|--------|---------------|--------|
| Pilot announcement | None | **UNVERIFIED** |
| Production timeline | None | **UNVERIFIED** |
| CDM contribution | None (contributes to other FINOS) | **CONTRADICTED** |
| Vendor CDM partnership | None | **UNVERIFIED** |

**Overall Status:** CLAIM CANNOT BE VERIFIED

---

## Recommended Framework Update

### Remove Original Claim

The "Pilot; production expected 2025" claim should be **removed** from framework v21 because:

1. No pilot announcement found in any evidence tier
2. No production timeline evidence found
3. 2022 conference participation is insufficient basis for pilot claim
4. Claim provenance is unknown (no source URL)

### Replacement Entry

```json
{
  "bank": "Deutsche Bank AG",
  "classification": "PRAGMATIST",
  "sub_classification": "Regulatory-Driven",
  "confidence": 55,
  "key_findings": [
    "Active FINOS contributor (Fluxnova, Waltz, Spring Bot) but NOT CDM",
    "EMIR Refit compliance via traditional DTCC reporting",
    "No CDM hiring signals or production announcements",
    "Framework v20 pilot claim UNVERIFIED"
  ],
  "last_verified": "2025-12-21"
}
```

---

## Integration with Peer Banks

### European G-SIB Comparison

| Bank | Classification | Confidence | CDM Evidence |
|------|---------------|------------|--------------|
| BNP Paribas | ARCHITECT-Native | 90% | Production Q3 2022 |
| Barclays | ARCHITECT-Follower | 75% | FINOS CDM contributor |
| **Deutsche Bank** | **PRAGMATIST** | **55%** | **FINOS contributor but NOT CDM** |

---

## Knowledge Gap Recommendations

### For Framework Maintenance

| Gap ID | Priority | Resolution Source |
|--------|----------|------------------|
| GAP-001 | 78/100 | Insider interview - CDM strategy |
| GAP-002 | 55/100 | DTCC relationship inquiry - CDM component |

---

## Reassessment Triggers

Framework should reassess Deutsche Bank if any of the following occur:

| Trigger | Source | Impact |
|---------|--------|--------|
| Official CDM announcement | db.com press release | Reclassify to ARCHITECT |
| FINOS CDM contribution | github.com/finos/common-domain-model | Reclassify to ARCHITECT |
| CDM job postings appear | Deutsche Bank careers site | Increase P(ARCHITECT) |
| Vendor CDM partnership | Vendor press release | Shift to PRAGMATIST (Vendor-Dependent) |

### Recommended Reassessment Date

**Q2 2025**

---
