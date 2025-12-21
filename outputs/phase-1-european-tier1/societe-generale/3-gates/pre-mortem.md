# Pre-Mortem Analysis: Société Générale

**Bank**: Société Générale
**Date**: 2025-12-21
**Researcher**: Claude Code (Sonnet 4.5)
**Phase**: 1 (European Tier 1)

---

## 1. Research Objective

**Primary Goal**: Assess whether Société Générale is following BNP Paribas CDM path with 12-24 month lag

**Hypothesis**: Société Générale is following BNP Paribas CDM path with 12-24 month lag

**Key Questions**:
1. Has Société Générale announced any CDM/DRR initiatives?
2. Is there evidence of BNP → SocGen knowledge transfer or pattern following?
3. How did SocGen address EMIR Refit (April 2024)?
4. Are there named individuals at SocGen involved in CDM/ISDA working groups?
5. What is SocGen's derivatives technology direction?

---

## 2. Prior Probability & Adjustments

**Base Prior**: 30% (null hypothesis: PRAGMATIST)

**Adjustments**:
- Derivatives dominant business (+10%): 40%
- BNP Paribas (French peer) in CDM production Q3 2022 (+10%): 50%
- Regional peer pressure (+5%): 45% (adjusted downward for lag effect)

**Final Prior P(Architect)**: 45%

**Rationale**:
- Société Générale operates in the same regulatory environment as BNP Paribas (AMF/ACPR)
- Strong derivatives franchise creates business case for CDM
- French banking culture may show cohort behavior patterns
- However, as a follower rather than leader, lag time is expected
- EMIR Refit (April 2024) is key inflection point

---

## 3. Failure Modes Analysis

### 3.1 Evidence Collection Failures

**Failure Mode 1**: Missing French-language evidence
- **Risk**: SocGen may communicate CDM initiatives primarily in French
- **Mitigation**: Include French search terms: "Société Générale CDM", "Modèle de Domaine Commun", "ISDA France"
- **Detection**: If only English sources found, explicitly search French trade press

**Failure Mode 2**: Assuming BNP pattern automatically applies
- **Risk**: Overfitting to BNP Paribas precedent without independent verification
- **Mitigation**: Require independent evidence; do not infer SocGen actions from BNP's path
- **Detection**: Check if evidence explicitly mentions SocGen vs. inferred from BNP

**Failure Mode 3**: Missing vendor relationships
- **Risk**: SocGen may have outsourced CDM capability without public announcement
- **Mitigation**: Search vendor press releases (Murex, Calypso, Delta Capita) for SocGen mentions
- **Detection**: Check vendor-matrix.json for known relationships

**Failure Mode 4**: Swiss banking discretion assumption
- **Risk**: Treating French bank like Swiss bank (low disclosure norms)
- **Mitigation**: French banks more transparent than Swiss; expect reasonable disclosure
- **Detection**: Compare evidence volume to Deutsche Bank (similar size/scope)

### 3.2 Interpretation Failures

**Failure Mode 5**: Conflating EMIR compliance with CDM adoption
- **Risk**: EMIR Refit can be addressed without CDM; compliance ≠ CDM
- **Mitigation**: Require explicit CDM mention in EMIR reporting context
- **Detection**: Check if "EMIR" evidence includes "CDM" or "ISDA Common Domain Model"

**Failure Mode 6**: Overweighting peer pressure
- **Risk**: Assuming French peer behavior guarantees SocGen follows
- **Mitigation**: Peer pressure is a prior adjustment, not evidence; require independent verification
- **Detection**: Distinguish prior adjustments from observed evidence

**Failure Mode 7**: Timing misinterpretation
- **Risk**: Assuming 12-24 month lag is automatic without checking dates
- **Mitigation**: If BNP went production Q3 2022, SocGen lag would be Q3 2023 - Q3 2024
- **Detection**: Check evidence timestamps carefully; current date is Dec 2025

**Failure Mode 8**: Working group membership overweighting
- **Risk**: ISDA CDM working group membership classified as production evidence
- **Mitigation**: Membership = `membership_or_participation` (Tier 2), not production
- **Detection**: Apply claim_type taxonomy strictly

### 3.3 Classification Failures

**Failure Mode 9**: Insufficient evidence for confidence level
- **Risk**: Reaching high confidence on thin evidence
- **Mitigation**: Apply confidence caps (Tier 1 = 95%, Tier 2 = 75%, Tier 3 = 50%)
- **Detection**: Count evidence items per tier; require corroboration for >75% confidence

**Failure Mode 10**: Missing null results documentation
- **Risk**: Absence of evidence not documented (informative absence ignored)
- **Mitigation**: Document exhaustive Tier 1 searches even if yielding nothing
- **Detection**: Check if null-results.md exists and is substantive

---

## 4. Search Strategy Design

### 4.1 Tier 1 Searches (Official Sources)

**Strategy**: Prioritize French regulatory/official sources given headquarters in Paris

1. **ISDA/FINOS Official**:
   - `"Société Générale" site:isda.org`
   - `"Société Générale" site:finos.org`
   - `"Société Générale" site:github.com/finos/common-domain-model`
   - `"SocGen" site:github.com/finos` (common abbreviation)

2. **Regulatory Filings**:
   - `"Société Générale" EMIR CDM 2024`
   - `"Société Générale" "regulatory reporting" "Common Domain Model"`
   - `"Société Générale" AMF derivatives reporting 2024`

3. **Bank Official Domain**:
   - `"CDM" OR "Common Domain Model" site:societegenerale.com`
   - `"ISDA CDM" site:societegenerale.com`
   - `"regulatory reporting" derivatives site:societegenerale.com`

**Expected Yield**: Low (banks rarely publicize on corporate sites)
**Informative Absence**: If exhaustive Tier 1 search yields nothing, suggests not in ARCHITECT-Native or Leader tiers

### 4.2 Tier 2 Searches (Trade Press & Partners)

**Strategy**: Target European/French derivatives trade press

1. **Trade Press**:
   - `"Société Générale" CDM ISDA site:risk.net`
   - `"Société Générale" "Common Domain Model" site:waterstechnology.com`
   - `"Société Générale" derivatives reporting 2024 site:fnlondon.com`
   - `"SocGen" CDM pilot production`

2. **French Trade Press**:
   - `"Société Générale" CDM 2024 France`
   - `"Société Générale" EMIR Refit 2024`
   - `"Société Générale" transformation dérivés` (French: derivatives transformation)

3. **Business Press**:
   - `"Société Générale" ISDA CDM site:ft.com`
   - `"Société Générale" derivatives technology 2024 site:bloomberg.com`
   - `"Société Générale" regulatory reporting site:reuters.com`

4. **Conferences/Events**:
   - `"Société Générale" ISDA conference 2023 2024`
   - `"Société Générale" FINOS summit`
   - `"Société Générale" derivatives technology conference`

**Expected Yield**: Medium (French banks appear in European derivatives press)

### 4.3 Tier 3 Searches (Signals)

**Strategy**: LinkedIn and job postings for hiring signals

1. **Job Postings**:
   - `"Société Générale" "ISDA CDM" job`
   - `"Société Générale" "Common Domain Model" careers`
   - `"Société Générale" derivatives reporting engineer`

2. **LinkedIn**:
   - `"Société Générale" CDM ISDA site:linkedin.com`
   - `"Société Générale" "Common Domain Model" site:linkedin.com`

**Expected Yield**: Low-Medium
**Risk**: LinkedIn signals are Tier 3 only (max 50% confidence)

### 4.4 Vendor Searches (Proxy Signals)

**Strategy**: Check known derivatives vendors for SocGen relationships

1. **Vendor Press**:
   - `"Société Générale" Murex CDM`
   - `"Société Générale" Delta Capita`
   - `"Société Générale" Calypso CDM`
   - `"Société Générale" REGnosys`

**Expected Yield**: Medium
**Classification Impact**: If vendor-only, may suggest PRAGMATIST (Vendor-dependent)

---

## 5. Disconfirming Evidence Search

To avoid confirmation bias, explicitly search for evidence that would disconfirm the hypothesis:

1. **Alternative Technology Paths**:
   - `"Société Générale" derivatives reporting modernization -CDM`
   - `"Société Générale" EMIR compliance 2024 -CDM`
   - `"Société Générale" Murex upgrade 2024` (check if traditional path without CDM)

2. **Vendor Dependency Signals**:
   - `"Société Générale" outsourcing derivatives operations`
   - `"Société Générale" vendor derivatives reporting`

3. **Capacity Constraints**:
   - `"Société Générale" restructuring 2024`
   - `"Société Générale" cost cutting technology`
   - `"Société Générale" regulatory fines 2024` (capacity diverted to remediation)

**Purpose**: If SocGen addressed EMIR Refit without CDM, or if capacity constraints exist, classification shifts to PRAGMATIST

---

## 6. Decision Thresholds

### 6.1 Classification Criteria

**ARCHITECT (Native)** requires:
- Tier 1 evidence of `production_usage` OR
- Multiple Tier 2 sources confirming production timeline with 75%+ confidence

**ARCHITECT (Active)** requires:
- Tier 1/2 evidence of `pilot_or_poc` OR
- `open_source_contribution` verified in FINOS/ISDA repos

**PRAGMATIST (Ecosystem)** requires:
- `membership_or_participation` evidence OR
- Tier 2 working group confirmation

**PRAGMATIST (Vendor)** requires:
- Vendor relationship without internal capability evidence

**OBSERVER** requires:
- `hiring_signal` only OR
- Single Tier 3 source

**UNKNOWN**:
- No verified evidence after exhaustive search

### 6.2 Confidence Calibration

- **>80% confidence**: Requires Tier 1 evidence + Tier 2 corroboration
- **60-80% confidence**: Requires multiple Tier 2 sources
- **40-60% confidence**: Single Tier 2 or multiple Tier 3 sources
- **<40% confidence**: Inference only or single Tier 3 source

---

## 7. Temporal Context

**Key Dates**:
- BNP Paribas production: Q3 2022
- EMIR Refit effective (EU): April 29, 2024
- Current date: December 21, 2025
- Expected SocGen timeline if 12-24 month lag: Q3 2023 - Q3 2024

**Implication**: We are now 15-27 months post-BNP production. If hypothesis is correct, evidence should exist by now.

**Freshness Thresholds**:
- Evidence <12 months (since Dec 2024): Current (1.0 weight)
- Evidence 12-18 months (Jun 2024 - Dec 2024): Recent (0.8 weight)
- Evidence 18 months - 3 years (Dec 2022 - Jun 2024): Dated (0.5 weight)
- Evidence >3 years (pre-Dec 2022): Historical (0.3 weight, context only)

**Search Recency**: Prioritize 2024-2025 evidence for current state assessment

---

## 8. Success Criteria

This research will be considered successful if:

1. **Evidence Completeness**: All three tiers searched exhaustively
2. **Null Results Documented**: Informative absences explicitly recorded
3. **Vendor Relationships Mapped**: All major derivatives vendors checked
4. **French Sources Included**: French-language evidence considered
5. **BNP Comparison Made**: Explicit comparison to BNP Paribas timeline
6. **Confidence Justified**: Final confidence score traceable to evidence tier mix
7. **Contradictions Resolved**: Any conflicting evidence explicitly addressed
8. **Disconfirming Evidence Sought**: Alternative hypotheses tested

---

## 9. Expected Outcome Distributions

Based on prior (45%) and failure modes analysis:

**Most Likely Outcomes** (ordered by probability):

1. **PRAGMATIST (Ecosystem)** [35% prior probability]
   - Scenario: SocGen in ISDA CDM working groups but no production commitment
   - Evidence: Tier 2 membership confirmation, no Tier 1 production evidence
   - Why: Conservative follower posture; observing BNP's success before committing

2. **ARCHITECT (Active)** [25% prior probability]
   - Scenario: SocGen launched CDM pilot in 2023-2024 following BNP path
   - Evidence: Tier 2 pilot announcements, job postings, conference mentions
   - Why: Hypothesis is partially correct; pilot stage confirming 12-24 month lag

3. **OBSERVER** [20% prior probability]
   - Scenario: SocGen aware of CDM but no active initiatives
   - Evidence: Tier 3 only (job postings, LinkedIn mentions)
   - Why: Derivatives business insufficient to justify investment despite BNP precedent

4. **PRAGMATIST (Vendor)** [15% prior probability]
   - Scenario: SocGen outsourced EMIR compliance to vendor without internal CDM
   - Evidence: Vendor press release (Murex, Calypso) without SocGen confirmation
   - Why: Cost optimization; treating regulatory reporting as vendor-managed

5. **ARCHITECT (Native)** [5% prior probability]
   - Scenario: SocGen in CDM production, announcement missed
   - Evidence: Tier 1 production confirmation
   - Why: Low probability; major production would be publicized

---

## 10. Known Risks

1. **French Language Barrier**: May miss French-only announcements
2. **European Press Bias**: Risk.net/Waters may under-cover French banks vs UK/German
3. **BNP Anchoring**: May over-infer from BNP precedent
4. **Vendor Opacity**: Vendor relationships may not be public
5. **EMIR Compliance Noise**: May confuse EMIR compliance with CDM adoption

**Mitigation**: Acknowledged in search strategy design; French terms included

---

## 11. Pre-Mortem Conclusion

**Readiness Assessment**: ✅ READY TO PROCEED

**Search Strategy**: Validated with failure modes considered
**Decision Thresholds**: Defined and aligned with CLAUDE.md
**Expected Challenges**: French language barrier, BNP anchoring bias
**Success Metrics**: 8 criteria defined above

**Next Step**: Execute Tier 1 searches (ISDA, FINOS, regulatory sources)

---

_Pre-Mortem completed: 2025-12-21_
_Estimated research duration: 90-120 minutes_
_Confidence in methodology: 85%_
