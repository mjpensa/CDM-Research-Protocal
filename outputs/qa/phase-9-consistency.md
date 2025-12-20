# QA Consistency Report: Phase 9 (US Custody Banks)

**Phase**: 9 - US Custody Banks
**Banks**: State Street, BNY Mellon
**Date**: 2025-12-19
**Protocol**: Tier C (Rapid Assessment)

---

## Test 1: Ordinal Ranking Consistency

**Test**: Do probability rankings align with evidence quality?

| Bank | P(Architect) | Evidence Quality | Rank Consistent? |
|------|--------------|------------------|------------------|
| State Street | 5% | Tier 4 only | YES |
| BNY Mellon | 5% | Tier 3-4 | YES |

**Result**: PASS

Both banks have identical P(Architect) = 5% with similar evidence quality. BNY Mellon's Tier 3 infrastructure evidence doesn't significantly differentiate.

---

## Test 2: Similar Profile Consistency

**Test**: Do banks with similar profiles receive similar classifications?

### US Custody Banks

| Bank | Business Model | P(Pragmatist) | Confidence |
|------|---------------|---------------|------------|
| State Street | Custody | 95% | 85% |
| BNY Mellon | Custody | 95% | 85% |

**Analysis**: Identical classification, probability, and confidence. Custody bank profile produces consistent results.

### Custody vs Investment Banks

| Bank Type | Representative | P(Pragmatist) |
|-----------|---------------|---------------|
| Custody | State Street | 95% |
| Investment (no signals) | Goldman Sachs | 83% |
| Investment (confirmed) | JPMorgan | 1% |

**Analysis**: Custody banks have higher P(Pragmatist) than investment banks without CDM signals. This reflects lower CDM relevance for custody business model.

**Result**: PASS

---

## Test 3: Evidence-Confidence Alignment

**Test**: Does confidence correlate with evidence tier and quantity?

| Bank | Highest Tier | Evidence Count | Confidence | Aligned? |
|------|--------------|----------------|------------|----------|
| State Street | 4 | 3 evidence, 3 null | 85% | YES |
| BNY Mellon | 3 | 3 evidence, 3 null | 85% | YES |

**Analysis**:
- Both banks have limited evidence (expected for custody banks)
- Confidence at 85% reflects certainty about PRAGMATIST but acknowledges limited evidence depth
- Identical confidence appropriate given similar evidence profiles

**Result**: PASS

---

## Test 4: Distribution Sanity

**Test**: Is the phase distribution reasonable given bank profiles?

**Phase 9 Distribution**:
- ARCHITECT: 0 (0%)
- PRAGMATIST: 2 (100%)

**Expected Distribution** based on bank profiles:
- Custody banks have low CDM relevance
- Neither bank has CDM production or pilot evidence
- Expected: 0 ARCHITECT, 2 PRAGMATIST

**Analysis**: 100% PRAGMATIST is consistent with:
1. Custody business model
2. No CDM evidence for either bank
3. Different CDM dynamics than investment banks

**Result**: PASS

---

## Test 5: Anchor Coherence

**Test**: Are classifications coherent with established anchor points?

### Anchor Points
1. **JPMorgan**: Production CDM (Oct 2024) - ARCHITECT
2. **BNP Paribas**: Production CDM (Q3 2022) - ARCHITECT
3. **Total in production**: ~5 firms globally

### Phase 9 vs Anchors

| Bank | vs JPMorgan | Coherent? |
|------|-------------|-----------|
| State Street | No CDM evidence, different business | YES |
| BNY Mellon | No CDM evidence, different business | YES |

**Analysis**: Custody banks appropriately differentiated from JPMorgan anchor. Different business model = different CDM relevance. Gap between ARCHITECT investment banks and PRAGMATIST custody banks is appropriate.

**Result**: PASS

---

## Cross-Phase Consistency Check

### Business Model Comparison

| Business Model | Banks | Avg P(Pragmatist) | Consistent? |
|----------------|-------|-------------------|-------------|
| Pure Derivatives | Goldman, Morgan Stanley | 88% | YES |
| Universal (restructuring) | Deutsche Bank, Citigroup | 87% | YES |
| Universal (retail) | BofA, Lloyds | 96% | YES |
| Custody | State Street, BNY Mellon | 95% | YES |

Custody banks have P(Pragmatist) similar to retail-focused universal banks - both business models have low CDM relevance.

### Regional Consistency

| Region | Custody Example | Classification |
|--------|-----------------|----------------|
| USA | State Street | PRAGMATIST |
| USA | BNY Mellon | PRAGMATIST |

No European custody banks in study for direct comparison, but custody bank pattern should be region-independent.

---

## Summary

| Test | Result |
|------|--------|
| 1. Ordinal Ranking | PASS |
| 2. Similar Profile | PASS |
| 3. Evidence-Confidence | PASS |
| 4. Distribution Sanity | PASS |
| 5. Anchor Coherence | PASS |

**Overall**: ALL TESTS PASS

---

## Notes

- Phase 9 represents final phase of the research protocol
- Custody bank pattern clearly established
- All 31 banks now assessed across 9 phases
- Custody banks represent distinct category with different CDM dynamics

---

*QA Consistency Report Complete*
*Phase 9: 5/5 Tests Passed*
*Protocol Complete: 31 Banks Assessed*
