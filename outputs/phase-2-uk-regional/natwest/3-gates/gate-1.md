# Reasoning Gate 1: Post-Tier 1 Assessment

**Bank**: NatWest Group plc
**Date**: 2025-12-20

---

## Current Probability State

| Metric | Value |
|--------|-------|
| P(ARCHITECT) | 30% |
| P(PRAGMATIST) | 70% |
| Confidence | 40% |

## Gate Decision Criteria

Per `config/decision-thresholds.json`:
- Skip to adversarial if P(ARCHITECT) > 80% OR P(ARCHITECT) < 20%
- Current P(ARCHITECT) = 30% → **Between thresholds**

## Decision: PROCEED TO TIER 2

**Rationale**: While the historical pilot participation increased P(ARCHITECT) from 20% to 30%, this is insufficient for classification. The FINOS Paradox (capability without CDM application) creates uncertainty that requires Tier 2 investigation.

## Evidence Quality Assessment

### Strengths
- High-authority Tier 1 sources (FCA, FINOS)
- Clear historical pilot participation documented
- FINOS open-source capability demonstrated

### Weaknesses
- Evidence is 5+ years old
- FINOS capability NOT applied to CDM
- No recent CDM signals
- Reliance on one historical pilot + informative absences

## Key Questions for Tier 2

1. Did the 2019 FCA DRR pilot lead to any industry press coverage of continuation?
2. Are there vendor announcements linking NatWest to CDM solutions?
3. Has NatWest participated in ISDA or FINOS CDM conferences since 2019?
4. What is NatWest's EMIR Refit compliance approach?

---

*Gate 1 passed. Proceeding to Tier 2 evidence gathering.*
