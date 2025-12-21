# Reasoning Gate 2: Post-Tier 2 Assessment

**Bank**: HSBC Holdings plc
**Date**: 2025-12-20

---

## Current Probability State

| Metric | Value |
|--------|-------|
| P(ARCHITECT) | 27% |
| P(PRAGMATIST) | 73% |
| Confidence | 50% |

## Gate Decision Criteria

Per `config/decision-thresholds.json`:
- Skip to adversarial if P(ARCHITECT) > 80% OR P(ARCHITECT) < 20%
- Current P(ARCHITECT) = 27% → **Above 20% threshold but below 80%**

## Decision: PROCEED TO TIER 3

**Rationale**: Per instructions to process all 3 tiers for every bank, we proceed to Tier 3 despite P(ARCHITECT) not hitting extreme thresholds.

## Evidence Trajectory Analysis

| Stage | P(ARCHITECT) | Direction |
|-------|--------------|-----------|
| Prior | 25% | - |
| Post-Tier 1 | 32% | Increased (DRR pilot boost) |
| Post-Tier 2 | 27% | Decreased (traditional platform signals) |

**Pattern**: Initial boost from DRR pilot offset by evidence of traditional platform commitment (Calypso) and absence of CDM in derivatives coverage.

## Remaining Questions for Tier 3

1. Are there CDM-related job postings at HSBC?
2. Do LinkedIn profiles of HSBC derivatives technology staff mention CDM work?
3. Is HSBC listed as FINOS CDM contributor or GitHub contributor?
4. Are there any CDM signals in broader employment searches?

## Framework Claim Assessment

**Framework v20 Claim** (if applicable): Not documented for HSBC

**Current Evidence Status**:
- DRR pilot ended 2019 - no evidence of production deployment
- DTCC Trade Repository approach dominates official documentation
- No vendor partnerships claiming HSBC CDM involvement
- €22.2T derivatives clearing activity uses traditional platforms, not CDM

---

*Gate 2 passed. Proceeding to Tier 3 evidence gathering.*
