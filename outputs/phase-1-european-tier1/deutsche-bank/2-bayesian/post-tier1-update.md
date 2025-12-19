# Bayesian Update Post-Tier 1: Deutsche Bank AG

**Bank**: Deutsche Bank AG
**Tier**: 1
**Date**: 2025-12-18

---

## Step 1: Prior Probability

**P(Architect)**: 0.40
**P(Pragmatist)**: 0.60

**Prior Odds**: 0.40 / 0.60 = 0.667

**Prior Justification**:
- Base prior (European Tier 1, Architect-Leader): 0.25
- Derivatives-dominant adjustment: +0.10
- European location adjustment: +0.05
- **Total**: 0.40

---

## Step 2: Evidence to Likelihood Ratio Mapping

### Evidence Block 1: FINOS Legend Pilot Participation (CDM Extensions)
**Finding**: "Deutsche Bank participated in a six-month FINOS Legend pilot... to prototype interbank collaborative data modeling and standardization, in particular to build extensions to the Common Domain Model (CDM) developed by ISDA."
**Maps to**: `named_finos_announcement` (LR = 13.0)
**LR**: 13.0
**Interpretation**: Strong Architect signal. Named participation in official FINOS CDM pilot with concrete deliverables (FX option extensions).

---

### Evidence Block 2: Russell Green Executive Statement
**Finding**: Russell Green, Head of Group Architecture at Deutsche Bank and FINOS board member, stated: "From our participation in the FINOS pilot, we believe that Legend Studio holds promise to enhance collaborative and federated data architecture and modeling within the bank and the industry."
**Maps to**: `conference_speaker_cdm_topic` (adjusted to 5.0 for executive statement on CDM tooling)
**LR**: 5.0
**Interpretation**: Moderate Architect signal. Senior executive endorsement of CDM-related tooling, though statement is about potential rather than production commitment.

---

### Evidence Block 3: CDM Extensions Accepted into Production
**Finding**: "The FX option extensions to the CDM... modeled collaboratively by the pilot group financial institutions participants using Legend, were proposed into the CDM and have since been accepted, released and integrated into a recent release."
**Maps to**: `named_isda_press_release_contributor` (LR = 14.0)
**LR**: 14.0
**Interpretation**: Strong Architect signal. Actual CDM contributions accepted into official releases demonstrates technical depth and follow-through beyond pilot participation.

---

### Evidence Block 4: FINOS Governing Board Chair Election
**Finding**: "Deutsche Bank technology leadership was elected to serve as FINOS Governing Board Chair, alongside Goldman Sachs... Goldman Sachs and Deutsche Bank are long-time collaborators and contributors to the open source movement in financial services."
**Maps to**: `named_working_group_membership` (elevated governance role; using LR = 3.7)
**LR**: 3.7
**Interpretation**: Moderate Architect signal. FINOS board leadership indicates institutional commitment to open-source financial infrastructure including CDM ecosystem, though not CDM-specific.

---

### Evidence Block 5: ISDA Board Representation
**Finding**: "Esra Turk, Global Head of Sustainable Finance at Deutsche Bank AG London, serves as a Director on the ISDA Board of Directors."
**Maps to**: `isda_agm_speaker_general` (LR = 1.6)
**LR**: 1.6
**Interpretation**: Weak Architect signal. ISDA board membership provides visibility but representative's focus is sustainable finance not technology/CDM. Direction marked NEUTRAL in evidence.

---

### Evidence Block 6: FINOS Multi-Project Contributions
**Finding**: "Deutsche Bank was identified alongside Citi as leading a round of contributions to FINOS... including Waltz (an enterprise architecture tool) and Symphony-related projects."
**Maps to**: `named_working_group_membership` (LR = 3.7)
**LR**: 3.7
**Interpretation**: Moderate Architect signal. Demonstrates institutional capability and open-source commitment, though contributions are CDM-adjacent rather than CDM-specific.

---

### Evidence Block 7: Fluxnova Launch (2025)
**Finding**: "Deutsche Bank joined Fidelity Investments, NatWest Group, and Capital One in launching Fluxnova, an Open Source Orchestration Platform to Scale Process Automation."
**Maps to**: `named_working_group_membership` (LR = 3.7)
**LR**: 3.7
**Interpretation**: Moderate Architect signal. Demonstrates continued 2025 FINOS engagement and open-source commitment, though Fluxnova is process automation not CDM-specific.

---

## Step 3: Null Results Consideration

### Null Result 1: No CDM Mentions on Deutsche Bank Website
**Search**: `"Deutsche Bank" "Common Domain Model" site:db.com`
**Expected if**: Deutsche Bank had publicly announced CDM adoption
**Maps to**: `no_mention_cdm_trade_coverage` (adapted for official site; LR = 0.33)
**LR**: 0.33
**Interpretation**: Weak Pragmatist signal. Architects typically publicize CDM work; absence suggests either quieter approach or less commitment.

---

### Null Result 2: No ISDA CDM Case Study Feature
**Search**: `site:isda.org "Deutsche Bank" "Common Domain Model"`
**Expected if**: ISDA had featured Deutsche Bank as a CDM adopter
**Maps to**: `no_mention_cdm_trade_coverage` (LR = 0.33)
**LR**: 0.33
**Interpretation**: Weak Pragmatist signal. Other banks (JP Morgan, JSCC) appear in ISDA CDM materials; Deutsche Bank's absence is notable.

---

### Null Result 3: No Production 2025 Confirmation
**Search**: `"Deutsche Bank" CDM production 2025`
**Expected if**: Deutsche Bank planning 2025 CDM production deployment
**Maps to**: Custom absence LR (estimated 0.40 - weaker than exhaustive search absence)
**LR**: 0.40
**Interpretation**: Weak Pragmatist signal. Critical validation gap - the "production expected 2025" hypothesis is not supported by Tier 1 sources.

---

### Null Result 4: No DRR Participation Evidence
**Search**: `"Deutsche Bank" "regulatory reporting" CDM OR "Common Domain Model"`
**Expected if**: Deutsche Bank participating in DRR initiatives
**Maps to**: `no_mention_cdm_trade_coverage` (LR = 0.33)
**LR**: 0.33
**Interpretation**: Weak Pragmatist signal. Given Deutsche Bank's regulatory obligations, absence from DRR is notable.

---

### Null Result 5: Not Listed as CDM Contributor/Maintainer
**Search**: `site:isda.org CDM contributors "Deutsche Bank"`
**Expected if**: Deutsche Bank was an official CDM contributor
**Maps to**: `no_mention_cdm_trade_coverage` (LR = 0.33)
**LR**: 0.33
**Interpretation**: Weak Pragmatist signal. Deutsche Bank not on current CDM maintainer lists despite 2020-2021 contributions. Pilot-to-production gap evident.

---

## Step 4: Combined Likelihood Ratio

**Calculation**:

*Positive Evidence (7 blocks):*
- LR1 = 13.0 (FINOS Legend pilot)
- LR2 = 5.0 (Russell Green statement)
- LR3 = 14.0 (CDM extensions accepted)
- LR4 = 3.7 (FINOS Board Chair)
- LR5 = 1.6 (ISDA Board membership)
- LR6 = 3.7 (FINOS contributions)
- LR7 = 3.7 (Fluxnova 2025)

Product of positive LRs = 13.0 × 5.0 × 14.0 × 3.7 × 1.6 × 3.7 × 3.7
= 65.0 × 14.0 × 3.7 × 1.6 × 3.7 × 3.7
= 910.0 × 3.7 × 1.6 × 3.7 × 3.7
= 3,367.0 × 1.6 × 3.7 × 3.7
= 5,387.2 × 3.7 × 3.7
= 19,932.64 × 3.7
= **73,750.77**

*Null Results (5 absence indicators):*
- NR1 = 0.33 (No site:db.com CDM)
- NR2 = 0.33 (No ISDA case study)
- NR3 = 0.40 (No production 2025 confirmation)
- NR4 = 0.33 (No DRR participation)
- NR5 = 0.33 (Not CDM maintainer)

Product of null result LRs = 0.33 × 0.33 × 0.40 × 0.33 × 0.33
= 0.1089 × 0.40 × 0.33 × 0.33
= 0.04356 × 0.33 × 0.33
= 0.01437 × 0.33
= **0.00474**

**Combined_LR** = 73,750.77 × 0.00474 = **349.58**

**FLAG**: Combined LR > 100 - requires review per calibration checks.

**Calibration Review**:
1. Double-counting check: Evidence Blocks 1 and 3 both relate to FINOS Legend pilot. Block 1 is participation announcement; Block 3 is outcome (CDM extensions accepted). These are causally linked but represent distinct facts (participation vs. contribution success). Applying 50% discount to Block 3: LR3_adjusted = 14.0^0.5 = 3.74

2. Evidence Block 2 (Russell Green statement) comes from same source as Block 1. Applying 50% discount: LR2_adjusted = 5.0^0.5 = 2.24

**Recalculated Positive LRs (with independence adjustments)**:
- LR1 = 13.0
- LR2 = 2.24 (adjusted for source overlap with Block 1)
- LR3 = 3.74 (adjusted for causal link to Block 1)
- LR4 = 3.7
- LR5 = 1.6
- LR6 = 3.7
- LR7 = 3.7

Product of adjusted positive LRs = 13.0 × 2.24 × 3.74 × 3.7 × 1.6 × 3.7 × 3.7
= 29.12 × 3.74 × 3.7 × 1.6 × 3.7 × 3.7
= 108.91 × 3.7 × 1.6 × 3.7 × 3.7
= 402.97 × 1.6 × 3.7 × 3.7
= 644.75 × 3.7 × 3.7
= 2,385.58 × 3.7
= **8,826.65**

**Adjusted Combined_LR** = 8,826.65 × 0.00474 = **41.84**

**Interpretation**: Evidence is 41.84 times more likely under Architect hypothesis than Pragmatist hypothesis. This is within reasonable bounds (0.01 < 41.84 < 100).

---

## Step 5: Posterior Odds

**Calculation**:
Posterior_Odds = Prior_Odds × Combined_LR
Posterior_Odds = 0.667 × 41.84
Posterior_Odds = **27.91**

---

## Step 6: Posterior Probability

**Calculation**:
P(Architect | Evidence) = Posterior_Odds / (1 + Posterior_Odds)
P(Architect | Evidence) = 27.91 / (1 + 27.91)
P(Architect | Evidence) = 27.91 / 28.91
P(Architect | Evidence) = **0.965** (96.5%)

P(Pragmatist | Evidence) = 1 - P(Architect | Evidence)
P(Pragmatist | Evidence) = 1 - 0.965
P(Pragmatist | Evidence) = **0.035** (3.5%)

---

## Step 7: Sanity Checks

- [x] 0 <= P(Architect) <= 1
- [x] P(Architect) + P(Pragmatist) = 1.0 (0.965 + 0.035 = 1.0)
- [x] Combined LR within reasonable bounds (0.01 < 41.84 < 100) - after adjustment
- [x] Probability shift matches evidence strength (Strong positive shift from 4 Strong + 3 Moderate ARCHITECT signals)

**Flags**:
1. **High probability shift (+56.5 pp)**: Justified by strong Tier 1 evidence including verified CDM contributions
2. **Temporal concentration**: Strongest evidence (pilot participation, CDM contributions) from 2020-2021; more recent evidence (2025) is CDM-adjacent not CDM-specific
3. **Pilot-to-production gap**: No evidence of current production deployment despite 2020-2021 contributions
4. **Independence adjustments applied**: Reduced some LRs due to source overlap

---

## Step 8: Interpretation

**Prior to Posterior Change**:
- Prior P(Architect): 40%
- Posterior P(Architect): **96.5%**
- **Change**: +56.5 percentage points

**Direction**: Evidence strongly strengthened Architect hypothesis

**Key Drivers**:
1. **Largest positive impacts**:
   - Evidence Block 1 (FINOS Legend pilot): LR = 13.0 - official named participation in CDM pilot
   - Evidence Block 3 (CDM extensions accepted): LR = 3.74 (adjusted) - actual contributions to production CDM
   - Evidence Block 4 (FINOS Board Chair): LR = 3.7 - governance role in CDM ecosystem

2. **Largest negative impacts**:
   - Null Result 5 (Not CDM maintainer): LR = 0.33 - absence from current contributor lists
   - Null Result 2 (No ISDA case study): LR = 0.33 - not featured in ISDA CDM materials
   - Null Result 4 (No DRR participation): LR = 0.33 - absent from regulatory reporting initiatives

3. **Overall pattern**: Strong evidence of past CDM engagement (2020-2021) offset partially by absence of current production signals. Deutsche Bank appears to be an Architect-Follower (contributed to CDM development) rather than Architect-Native (in production) or Architect-Leader (committed to production).

**Confidence Assessment**: **MODERATE-HIGH**
- High confidence that Deutsche Bank has engaged with CDM at a technical level (verified contributions)
- Moderate uncertainty about current production status and 2025 deployment timeline
- Evidence is dated (2020-2021 peak) with less CDM-specific activity recently

---

## Architect Variant Assessment

Given P(Architect) = 96.5%, determine variant:

| Variant | Criteria | Evidence Match |
|---------|----------|----------------|
| Architect-Native | Production confirmed | NO - No production evidence |
| Architect-Leader | Production committed | UNCERTAIN - "Production 2025" claim not validated |
| Architect-Follower | Contributing without production | **YES** - CDM extensions contributed, no production evidence |

**Preliminary Classification**: Architect-Follower
**Confidence**: Moderate (Tier 2 may reveal production commitment)

---

## Recommendation for Gate 1

**Sufficiency**: YES - Evidence sufficient for >80% confidence (96.5%)

However, **key uncertainty remains**: Is Deutsche Bank an Architect-Follower or Architect-Leader?

**If skipping to Adversarial**:
- Architect-Follower classification is well-supported
- Should be challenged on: "Is 2020-2021 pilot engagement still active? What happened after the pilot?"

**If proceeding to Tier 2**:
- **Key question to resolve**: Is there evidence of current (2024-2025) CDM production deployment or commitment?
- Search targets: Conference presentations, trade press (Risk.net, WatersTechnology), executive interviews

**Recommendation**: **Proceed to Tier 2** to validate/invalidate the "production expected 2025" claim before final classification. The distinction between Architect-Follower and Architect-Leader has material implications.

---

## Summary Table

| Metric | Value |
|--------|-------|
| Prior P(Architect) | 40% |
| Combined LR | 41.84 (adjusted for independence) |
| Posterior Odds | 27.91 |
| Posterior P(Architect) | 96.5% |
| Posterior P(Pragmatist) | 3.5% |
| Change | +56.5 pp |
| Preliminary Classification | Architect-Follower |
| Confidence | Moderate-High |
| Gate 1 Recommendation | Proceed to Tier 2 for production status validation |
