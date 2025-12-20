# Phase 2 Synthesis: UK Regional Banks
## CDM/DRR Research Protocol

**Date**: 2025-12-19
**Phase**: 2 - UK Regional
**Protocol**: Tier B (Abbreviated)
**Banks Assessed**: 2

---

## Executive Summary

Phase 2 assessed UK regional banks with medium derivatives exposure. Both banks were classified as **PRAGMATIST** with CDM architecture, consistent with their retail/commercial banking focus and limited derivatives operations.

| Bank | Classification | P(Architect) | Confidence | Key Finding |
|------|---------------|--------------|------------|-------------|
| NatWest Group PLC | PRAGMATIST | 5% | 95% | No evidence; retail/commercial focus |
| Lloyds Banking Group PLC | PRAGMATIST | 5% | 95% | Retail-focused; no ISDA CDM involvement |

---

## Phase 2 Distribution

```
ARCHITECT:     0 (0%)
PRAGMATIST:    0 (0%)
PRAGMATIST:   2 (100%)
```

**Total Banks**: 2
**Total Classified as CDM-Involved**: 0

---

## Cross-Bank Patterns

### Pattern 1: UK Regional = PRAGMATIST

Both UK regional banks show identical classification patterns:
- **No direct CDM evidence** found
- **Business model mismatch**: Retail/commercial focus ≠ CDM Architect profile
- **Technology investments** directed toward consumer digital, not derivatives infrastructure
- **EMIR compliance** achieved through standard vendor solutions, not proprietary CDM

### Pattern 2: Clear Differentiation from Phase 1 UK Banks

| Phase | Bank | Classification | Derivatives Focus |
|-------|------|---------------|-------------------|
| 1 | Barclays | ARCHITECT (Follower) | Investment Banking |
| 1 | HSBC | PRAGMATIST (Vendor-Dependent) | Global Markets |
| 2 | NatWest | PRAGMATIST | UK Retail/Commercial |
| 2 | Lloyds | PRAGMATIST | UK Retail/Commercial |

**Insight**: CDM engagement strongly correlates with investment banking activity and global derivatives operations. UK regional banks without significant investment banking divisions show no CDM architectural involvement.

### Pattern 3: Vendor-Mediated Future Adoption

Both banks classified as "Potential Future Adopter (via vendors)":
- CDM exposure may come through vendor platform upgrades
- No immediate strategic investment expected
- Passive consumption rather than active architecture

---

## Research Questions Summary

### Q1: Following Larger UK Banks?

**Answer**: NO

Neither NatWest nor Lloyds shows evidence of following Barclays or HSBC on CDM. The fundamental business model difference (retail vs. investment banking) creates different strategic priorities.

### Q2: UK EMIR (Sept 2024) Impact?

**Answer**: COMPLIANCE-DRIVEN, NOT CDM-DRIVEN

- UK EMIR Refit mandates ISO 20022 XML format
- CDM is NOT required for compliance
- Both banks likely use standard trade repository solutions
- Regulatory compliance does not drive CDM architecture investment

### Q3: Vendor Reliance?

**Answer**: YES (Almost Certainly)

Both banks expected to use vendor solutions for derivatives operations:
- NatWest: Standard vendor infrastructure (DTCC, MarkitServ)
- Lloyds: Limited derivatives operations via treasury systems

---

## Probability Evolution (Phase 2)

| Bank | Prior | Post-Evidence | Post-Adversarial | Change |
|------|-------|---------------|------------------|--------|
| NatWest | 20% | 3% | 5% | -15% |
| Lloyds | 20% | 5% | 5% | -15% |

**Phase Average Movement**: -15 percentage points

---

## Tier B Protocol Effectiveness

Tier B (Abbreviated) protocol proved appropriate for UK regional banks:
- **2 failure modes** sufficient for low-complexity assessment
- **6 searches** adequate given limited derivatives exposure
- **Single-tier adversarial** confirmed classifications without extended analysis
- **Condensed synthesis** appropriate for PRAGMATIST outcomes

---

## Phase 2 Files Generated

### NatWest (7 files)
- status.json
- pre-mortem.md
- evidence-gathering.md
- bayesian-update.md
- gate-1-decision.md
- adversarial-analysis.md
- synthesis.md

### Lloyds (6 files)
- status.json
- pre-mortem.md
- evidence-gathering.md
- bayesian-update.md
- adversarial-analysis.md
- synthesis.md

---

## Cumulative Progress (Phases 1-2)

| Classification | Phase 1 | Phase 2 | Total |
|----------------|---------|---------|-------|
| ARCHITECT | 2 | 0 | 2 |
| PRAGMATIST | 3 | 0 | 3 |
| PRAGMATIST | 0 | 2 | 2 |
| **Total** | **5** | **2** | **7** |

### Distribution After 7 Banks
```
ARCHITECT:     29% (2/7)
PRAGMATIST:    43% (3/7)
PRAGMATIST:   29% (2/7)
```

---

## Key Insights from Phase 2

1. **Business Model = CDM Engagement**: Investment banking activity is the primary predictor of CDM involvement. Retail banks have no strategic motivation for CDM architecture.

2. **UK Market Segmentation**: UK banking sector shows clear segmentation:
   - Tier 1 (Barclays, HSBC): CDM-engaged (varying degrees)
   - Regional (NatWest, Lloyds): CDM PRAGMATIST

3. **EMIR Refit ≠ CDM Adoption**: Regulatory compliance can be achieved without CDM. Regional banks use standard vendor/TR solutions.

4. **Tier B Protocol Validated**: Abbreviated protocol effective for banks with low expected CDM engagement. No extended investigation required.

---

## Recommendations

### For Phase 3+ Protocol Selection
- **Japanese banks**: Consider Tier B for regional (Mizuho, SMBC) and Tier A for investment bank-focused (Nomura)
- **MUFG**: May warrant Tier A given scale and international presence

### For Cross-Phase Analysis
- Track correlation between derivatives volume and CDM classification
- Monitor vendor-mediated CDM adoption as potential future pathway
- Compare US/EU regulatory drivers vs. UK EMIR impact

---

## Phase 2 Status: COMPLETE

All assessments validated. Ready to proceed to Phase 3 (Japanese Banks).
