# Phase 1 QA Consistency Report: European Tier 1 Banks

**QA Execution Date**: 2025-12-19
**QA Agent**: Claude Opus 4.5
**Phase**: 1 (European Tier 1)
**Banks Validated**: 5

---

## Phase 1 Results Summary

| Bank | Classification | Variant | Confidence | P(Architect) |
|------|---------------|---------|------------|--------------|
| Deutsche Bank | PRAGMATIST | Strategic-Dormant | 80% | 19.6% |
| Societe Generale | PRAGMATIST | Vendor-Dependent | 95% | 5% |
| UBS | ARCHITECT | Adopter-Low | 54% | 54% |
| Barclays | ARCHITECT | Follower | 96% | 96% |
| HSBC | PRAGMATIST | Vendor-Dependent | 99% | 0.1% |

**Distribution**: 2 ARCHITECT (40%), 3 PRAGMATIST (60%)

---

## Test 1: Ordinal Ranking Consistency

**Rule**: If Bank A has stronger evidence than Bank B for the same classification, Bank A should have equal or higher confidence than Bank B.

### ARCHITECT Banks Ranking

| Bank | Confidence | Key Evidence Strength |
|------|------------|----------------------|
| Barclays | 96% | DerivHack series, DRR pilot, Lee Braine advocacy, FINOS participation, 8+ years engagement |
| UBS | 54% | 2020 ISDA pilot, 2025 FINOS contributions, integration constraints |

**Analysis**: Barclays has demonstrably stronger and more sustained evidence (hackathons, research publications, named advocates, continuous activity) compared to UBS (older pilot, unquantified contributions, integration disruption). The 42 percentage point gap (96% vs 54%) correctly reflects this evidence differential.

**Verdict**: PASS

### PRAGMATIST Banks Ranking

| Bank | Confidence | Key Evidence Strength |
|------|------------|----------------------|
| HSBC | 99% | Delta Capita outsourcing contract, 6-year gap, explicit vendor dependency |
| Societe Generale | 95% | Comprehensive null results, Litvack Paradox, alternative innovation (SG-FORGE) |
| Deutsche Bank | 80% | Historical pilot (2020-2021), 4-year gap, continued FINOS non-CDM engagement |

**Analysis**:
- HSBC has definitive PRAGMATIST evidence (signed outsourcing contract) justifying highest confidence
- Societe Generale has comprehensive null results with no positive CDM evidence, justifying very high confidence
- Deutsche Bank has mixed evidence (historical pilot activity) creating residual uncertainty, justifying lower confidence

The ranking correctly reflects evidence strength hierarchy.

**Verdict**: PASS

### Test 1 Overall Result: **PASS**

---

## Test 2: Similar Profile Test

**Rule**: Banks with similar profiles (region, size, derivatives exposure, regulatory environment) should have similar classifications unless specific differentiating evidence exists.

### Geographic/Regulatory Peer Groups

#### UK Banks: Barclays vs HSBC

| Dimension | Barclays | HSBC |
|-----------|----------|------|
| Classification | ARCHITECT-Follower | PRAGMATIST-Vendor-Dependent |
| Confidence | 96% | 99% |
| HQ | London | London |
| Primary Regulator | FCA/PRA | FCA/PRA |
| Derivatives Exposure | Major dealer | Major dealer |

**Classification Difference Explanation**:
1. **Barclays Evidence**:
   - DerivHack hackathon series (2018, 2019, 2023)
   - UK DRR pilot participation with follow-up activity
   - Lee Braine sustained CDM advocacy and publications
   - Internal CDM working group established
   - FINOS community participation

2. **HSBC Evidence**:
   - UK DRR pilot participation (2018-2019) with NO follow-up
   - Delta Capita outsourcing contract (2025) for complete CDM capability
   - 6-year gap between pilot and outsourcing with no internal activity
   - ISDA governance role without CDM technical contribution
   - Explicit vendor dependency strategy

**Key Differentiator**: Barclays demonstrates sustained internal engagement and advocacy over 8+ years. HSBC demonstrates pilot participation followed by explicit outsourcing decision. The divergence is explained by strategic technology choices, not regional factors.

**Verdict**: FLAG - Requires Explanation (Explanation Provided: Strategic Differentiation)

#### French Banks: Societe Generale (no Phase 1 peer)
Only one French bank in Phase 1. BNP Paribas (known ARCHITECT-Native) not in Phase 1 scope.

#### German Banks: Deutsche Bank (no Phase 1 peer)
Only one German bank in Phase 1.

#### Swiss Banks: UBS (no Phase 1 peer)
Only one Swiss bank in Phase 1.

### Test 2 Overall Result: **PASS WITH FLAG**

**Flag**: UK bank divergence (Barclays ARCHITECT vs HSBC PRAGMATIST) requires explanation.

**Resolution**: Divergence is explained by documented strategic technology choices, not methodology inconsistency. Barclays has 8+ years of sustained internal CDM engagement. HSBC has documented vendor outsourcing decision. Classification difference reflects real strategic divergence between UK Tier 1 banks.

---

## Test 3: Evidence-Confidence Correlation

**Rule**: Higher-tier evidence should correlate with higher confidence. Strong Tier 1 evidence should produce high confidence. Mixed or weak evidence should produce lower confidence.

### Bank-by-Bank Analysis

| Bank | Evidence Quality | Confidence | Correlation |
|------|-----------------|------------|-------------|
| Barclays | Strong Tier 1 (FINOS, DRR pilot, DerivHack, named advocate) | 96% | CORRECT |
| HSBC | Strong Tier 1 (Delta Capita contract, outsourcing announcement) | 99% | CORRECT |
| Societe Generale | Comprehensive null results + alternative innovation documentation | 95% | CORRECT |
| Deutsche Bank | Mixed (historical pilot + 4-year gap) | 80% | CORRECT |
| UBS | Mixed (2020 pilot, 2025 contributions, integration uncertainty) | 54% | CORRECT |

### Detailed Correlation Check

**Barclays (96%)**:
- Strong Tier 1: Named hackathon series, named advocate (Lee Braine), research publications
- Evidence quality justifies high confidence

**HSBC (99%)**:
- Strong Tier 1: Signed contract with Delta Capita, press announcement, explicit outsourcing scope
- Evidence quality justifies very high confidence

**Societe Generale (95%)**:
- Strong null results across all evidence tiers
- Clear alternative innovation path (SG-FORGE, Capitolis)
- Comprehensive absence evidence justifies high confidence in PRAGMATIST

**Deutsche Bank (80%)**:
- Mixed evidence: Historical pilot (positive) + 4-year gap (negative)
- Residual uncertainty from possible hidden work justifies moderate-high confidence

**UBS (54%)**:
- Mixed evidence: Pilot participation + contributions (positive) + integration constraints + evidence age (negative)
- Borderline probability justifies low confidence classification

### Test 3 Overall Result: **PASS**

All confidence levels appropriately reflect evidence quality.

---

## Test 4: Classification Distribution Sanity

**Rule**: Industry-wide distribution expected to be approximately 30% Architect, 70% Pragmatist. Phase-level deviation acceptable if explained.

### Phase 1 Distribution

| Classification | Count | Percentage |
|---------------|-------|------------|
| ARCHITECT | 2 | 40% |
| PRAGMATIST | 3 | 60% |

### Expected vs Observed

| Dimension | Expected | Observed | Deviation |
|-----------|----------|----------|-----------|
| ARCHITECT | ~30% | 40% | +10pp |
| PRAGMATIST | ~70% | 60% | -10pp |

### Deviation Explanation

Phase 1 contains European Tier 1 banks selected for:
1. **Derivatives-dominant business models**: Higher CDM incentive
2. **ISDA/FINOS proximity**: Greater standard awareness
3. **Regulatory pressure (EMIR Refit)**: Forcing function
4. **Tier 1 scale**: Resources for CDM investment

A 10 percentage point deviation toward ARCHITECT is expected for this cohort. The deviation is within acceptable range and explained by selection criteria.

### Sanity Check: Are Classifications Defensible?

| Bank | Classification | Defensibility |
|------|---------------|---------------|
| Barclays | ARCHITECT | STRONG - 8+ years sustained engagement, named advocate |
| UBS | ARCHITECT | MODERATE - Pilot + contributions, integration constraints |
| Deutsche Bank | PRAGMATIST | STRONG - 4-year gap, pilot-only history |
| Societe Generale | PRAGMATIST | STRONG - Comprehensive null results, Litvack Paradox |
| HSBC | PRAGMATIST | STRONG - Explicit outsourcing contract |

### Test 4 Overall Result: **PASS**

Distribution is within expected range for European Tier 1 cohort. 40% ARCHITECT rate is justified by selection criteria (derivatives-dominant, Tier 1 scale, ISDA/FINOS proximity).

---

## Test 5: Anchor Point Coherence

**Rule**: No classification may violate established framework anchor points (immutable facts).

### Anchor Point Checklist

| Anchor Point | Requirement | Phase 1 Status | Compliant |
|--------------|-------------|----------------|-----------|
| Only 4 firms globally in CDM production | No Phase 1 bank claimed as production | No production claims | YES |
| Production firms: JPM, Goldman, Citi, BNP | Phase 1 banks classified appropriately | No conflicting claims | YES |
| CDM Native requires production evidence | No Phase 1 bank classified Native | Barclays=Follower, UBS=Adopter | YES |
| JSCC first CCP production (June 2025) | No Phase 1 bank claimed earlier | No CCP claims | YES |
| BNP Paribas first major bank (Q3 2022) | No Phase 1 bank claimed earlier | No earlier claims | YES |
| FINOS governance (September 2022) | Correctly referenced | All assessments accurate | YES |
| EMIR Refit EU April 2024 / UK Sept 2024 | Correctly referenced | Timeline accurate | YES |

### Specific Bank Checks

**Deutsche Bank**:
- Classified PRAGMATIST - does not claim production
- Historical pilot acknowledged but not treated as current capability
- COMPLIANT

**Societe Generale**:
- Classified PRAGMATIST - does not claim production
- Litvack ISDA role acknowledged but not treated as CDM adoption
- COMPLIANT

**UBS**:
- Classified ARCHITECT-Adopter (Low) - does not claim production
- 2020 pilot acknowledged as pilot, not production
- COMPLIANT

**Barclays**:
- Classified ARCHITECT-Follower - does not claim production
- DRR pilot acknowledged but no production follow-through
- COMPLIANT

**HSBC**:
- Classified PRAGMATIST - does not claim production
- Vendor dependency via Delta Capita correctly assessed
- COMPLIANT

### Test 5 Overall Result: **PASS**

All classifications comply with established anchor points. No immutable facts violated.

---

## QA Summary

| Test | Result | Notes |
|------|--------|-------|
| Test 1: Ordinal Ranking | PASS | Confidence rankings correctly reflect evidence strength |
| Test 2: Similar Profile | PASS WITH FLAG | UK divergence explained by strategic differentiation |
| Test 3: Evidence-Confidence | PASS | All confidence levels appropriate for evidence quality |
| Test 4: Distribution Sanity | PASS | 40% ARCHITECT justified for Tier 1 cohort |
| Test 5: Anchor Coherence | PASS | No anchor point violations |

---

## Overall QA Verdict

### **ALL TESTS PASS**

### Flags Requiring Attention

| Flag | Description | Resolution Status |
|------|-------------|-------------------|
| UK Bank Divergence | Barclays (ARCHITECT) vs HSBC (PRAGMATIST) | RESOLVED - Strategic differentiation documented |

### Phase 1 Status: **COMPLETE - VALIDATED**

---

## Recommendations for Framework

1. **Document UK Bank Divergence Pattern**: Add case study on Barclays vs HSBC strategic divergence to framework examples.

2. **Establish "Litvack Paradox" as Named Pattern**: ISDA governance roles do not predict firm-level CDM adoption.

3. **Define "Strategic-Dormant" Variant**: Deutsche Bank case establishes new PRAGMATIST variant for banks with historical engagement but current inactivity.

4. **Validate Low-Confidence ARCHITECT Protocol**: UBS classification (54%) at ARCHITECT/MONITOR boundary demonstrates protocol handling of borderline cases.

5. **Confirm Vendor-Dependent Identification Criteria**: HSBC Delta Capita case provides definitive example of PRAGMATIST-Vendor-Dependent.

---

## Appendix: Evidence Summary by Bank

### Deutsche Bank - PRAGMATIST (Strategic-Dormant, 80%)
- Tier 1: 7 evidence blocks (historical pilot, FINOS leadership)
- Tier 2: 8 evidence blocks (industry coverage, null results)
- Null Results: 14 (5 Tier 1, 9 Tier 2)
- Key Finding: 4-year gap (2021-2025) without CDM activity

### Societe Generale - PRAGMATIST (Vendor-Dependent, 95%)
- Tier 1: 8 evidence blocks (governance, alternative innovation)
- Null Results: 5 (comprehensive absence)
- Key Finding: Litvack Paradox - 10 years ISDA Chair without adoption

### UBS - ARCHITECT (Adopter-Low, 54%)
- Tier 1: 5 positive evidence blocks (pilot, contributions)
- Null Results: 5 (production, showcase absence)
- Key Finding: Integration constraint partially refuted

### Barclays - ARCHITECT (Follower, 96%)
- Tier 1: 7 positive evidence blocks (hackathons, advocacy, publications)
- Tier 2: Multiple supporting sources
- Key Finding: FMI-first strategy = self-identified Follower

### HSBC - PRAGMATIST (Vendor-Dependent, 99%)
- Tier 1: 10 evidence blocks (outsourcing contract, gap analysis)
- Key Finding: Delta Capita comprehensive outsourcing confirms vendor dependency

---

**QA Report Complete**

*Generated: 2025-12-19*
*QA Agent: Claude Opus 4.5*
*Protocol Version: v2.0*
