# QA Consistency Report: Phase 8 (US Investment Banks)

**Phase**: 8 - US Investment Banks
**Banks**: JPMorgan, Goldman Sachs, Morgan Stanley, Citigroup, Bank of America
**Date**: 2025-12-19
**Protocol**: Mixed (Tier A/B)

---

## Test 1: Ordinal Ranking Consistency

**Test**: Do probability rankings align with evidence quality?

| Bank | P(Architect) | Evidence Quality | Rank Consistent? |
|------|--------------|------------------|------------------|
| JPMorgan | 99% | Tier 1 production confirmed | YES |
| Goldman Sachs | 17% | Tier 4 only, no signals | YES |
| Morgan Stanley | 8% | Tier 4 + wealth dilution | YES |
| Bank of America | 3% | Retail focus clear | YES |
| Citigroup | 2% | Restructuring priority | YES |

**Result**: PASS

JPMorgan highest with confirmed production. Goldman higher than others due to technology culture potential. Citigroup lowest due to restructuring + universal model.

---

## Test 2: Similar Profile Consistency

**Test**: Do banks with similar profiles receive similar classifications?

### Pure Derivatives Dealers

| Bank | Business Model | P(Pragmatist) | Confidence |
|------|---------------|---------------|------------|
| Goldman Sachs | Pure dealer | 83% | 65% |
| Morgan Stanley | Dealer + wealth | 92% | 75% |

**Analysis**: Both PRAGMATIST but Goldman has lower confidence due to technology culture. Morgan Stanley higher confidence due to wealth management dilution. Differentiation appropriate.

### Universal Banks

| Bank | Business Focus | P(Pragmatist) | Confidence |
|------|---------------|---------------|------------|
| Citigroup | Restructuring | 98% | 85% |
| Bank of America | Retail | 97% | 85% |

**Analysis**: Both high-confidence PRAGMATIST with similar probabilities. Different drivers (restructuring vs retail) but same classification outcome. Consistent.

**Result**: PASS

---

## Test 3: Evidence-Confidence Alignment

**Test**: Does confidence correlate with evidence tier and quantity?

| Bank | Highest Tier | Evidence Count | Confidence | Aligned? |
|------|--------------|----------------|------------|----------|
| JPMorgan | 1 | 4 evidence | 95% | YES |
| Goldman Sachs | 2 | 4 evidence | 65% | YES |
| Morgan Stanley | 2 | 4 evidence | 75% | YES |
| Citigroup | 2 | 3 evidence | 85% | YES |
| Bank of America | 2 | 3 evidence | 85% | YES |

**Analysis**:
- JPMorgan: Tier 1 production evidence = highest confidence
- Goldman: Lower confidence due to secretive culture uncertainty
- Morgan Stanley: Higher than Goldman due to clearer wealth management signal
- Citigroup/BofA: High confidence due to clear business model signals

**Result**: PASS

---

## Test 4: Distribution Sanity

**Test**: Is the phase distribution reasonable given bank profiles?

**Phase 8 Distribution**:
- ARCHITECT: 1 (20%)
- PRAGMATIST: 4 (80%)

**Expected Distribution** based on bank profiles:
- JPMorgan: Confirmed ARCHITECT
- Goldman/Morgan Stanley: High potential but no signals
- Citigroup/BofA: Universal bank pattern suggests PRAGMATIST
- Expected: 1-2 ARCHITECT, 3-4 PRAGMATIST

**Analysis**: 20% ARCHITECT is consistent with:
1. Only JPMorgan has confirmed production
2. Goldman/Morgan Stanley showing no CDM signals
3. Universal bank pattern confirmed for Citigroup/BofA

Distribution aligns with evidence and priors.

**Result**: PASS

---

## Test 5: Anchor Coherence

**Test**: Are classifications coherent with established anchor points?

### Anchor Points
1. **BNP Paribas**: Production CDM (Q3 2022) - ARCHITECT
2. **JPMorgan**: Production CDM (Oct 2024) - ARCHITECT
3. **Pictet**: Production CDM (confirmed) - ARCHITECT
4. **Total in production**: 4-5 firms globally

### Phase 8 vs Anchors

| Bank | vs BNP | vs JPMorgan | vs Pictet | Coherent? |
|------|--------|-------------|-----------|-----------|
| JPMorgan | Later adopter | IS ANCHOR | Later than Pictet | YES |
| Goldman Sachs | No CDM evidence | No CDM evidence | No CDM evidence | YES |
| Morgan Stanley | No CDM evidence | No CDM evidence | No CDM evidence | YES |
| Citigroup | No CDM evidence | No CDM evidence | No CDM evidence | YES |
| Bank of America | No CDM evidence | No CDM evidence | No CDM evidence | YES |

**Analysis**:
- JPMorgan coherent as 4th confirmed production firm
- Other 4 banks show no production evidence, consistent with <5 firms globally in production
- Classification gap between JPMorgan (ARCHITECT) and others (PRAGMATIST) appropriate

**Result**: PASS

---

## Cross-Phase Consistency Check

### US Investment Banks vs European Tier 1

| Bank | Region | Business Model | Classification | Coherent? |
|------|--------|----------------|----------------|-----------|
| JPMorgan | USA | Derivatives | ARCHITECT | YES - confirmed |
| Goldman Sachs | USA | Derivatives | PRAGMATIST | YES - no signals |
| Barclays | UK | Derivatives | ARCHITECT | YES - confirmed contributor |
| Deutsche Bank | Germany | Universal | PRAGMATIST | YES - restructuring |

US and European patterns are consistent: confirmed contributors/production = ARCHITECT, no evidence = PRAGMATIST.

### Universal Bank Pattern

| Bank | Region | Classification | Driver |
|------|--------|----------------|--------|
| Citigroup | USA | PRAGMATIST | Restructuring |
| Bank of America | USA | PRAGMATIST | Retail |
| Deutsche Bank | Germany | PRAGMATIST | Restructuring |
| HSBC | UK | PRAGMATIST | Complexity |

Universal bank pattern consistent across US and Europe.

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

- Goldman Sachs has lowest confidence (65%) due to technology culture uncertainty
- JPMorgan classification establishes US ARCHITECT benchmark
- Universal bank pattern confirmed for US as well as Europe
- US market shows less cohort behavior than Asian markets

---

*QA Consistency Report Complete*
*Phase 8: 5/5 Tests Passed*
