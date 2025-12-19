# Bayesian Update Post-Tier 1: Societe Generale

**Bank**: Societe Generale
**Tier**: 1
**Date**: 2025-12-19

---

## Step 1: Prior Probability

**P(Architect)**: 0.45
**P(Pragmatist)**: 0.55

**Prior Odds**: 0.45 / 0.55 = 0.818

**Prior Justification**:
- Base prior (European Tier 1, derivatives-dominant): 0.30
- Regional peer BNP Paribas is confirmed Architect-Native: +0.10
- Eric Litvack ISDA chairmanship (governance proximity): +0.05
- **Total**: 0.45

---

## Step 2: Evidence to Likelihood Ratio Mapping

### Positive Evidence

---

### Evidence Block 2: Eric Litvack ISDA CDM Panel Moderation
**Finding**: Eric Litvack from Societe Generale moderated ISDA AGM sessions discussing "the potential application of the Common Domain Model (CDM) to facilitate reporting and compliance." As ISDA Chair for 10 years during CDM's development and launch.
**Maps to**: `isda_agm_speaker_general` (LR = 1.6) - elevated slightly for CDM topic moderation
**Assigned LR**: 1.8
**Interpretation**: Weak-to-moderate Architect signal. Moderating a CDM discussion demonstrates awareness and governance proximity, but moderation ≠ implementation commitment. Litvack's role was industry-level governance, not a signal of SocGen firm-level technical adoption.
**Direction**: NEUTRAL-ARCHITECT

**Rationale for LR = 1.8**:
- Base ISDA AGM speaker LR = 1.6
- Slight uplift to 1.8 for specific CDM topic (vs. general ISDA involvement)
- Capped below 2.0 because moderator role does not indicate presenter/implementer status

---

### Negative Evidence (Absence/Null Signals)

---

### Null Result 1: No Direct CDM/DRR Announcement
**Finding**: No official CDM or DRR adoption announcement from SocGen despite BNP Paribas announcing CDM production in November 2022. Expected announcement window (12-24 month lag hypothesis: Nov 2023 - Nov 2024) passed without any SocGen announcement.
**Maps to**: `no_evidence_after_exhaustive_tier1_search` (LR = 0.21) - applying partial weight for Tier 1 only
**Assigned LR**: 0.30
**Interpretation**: Moderate Pragmatist signal. If SocGen were pursuing CDM at scale, we would expect some public announcement similar to BNP Paribas. The silence is informative.
**Direction**: PRAGMATIST

**Rationale for LR = 0.30**:
- Base "no evidence after exhaustive Tier 1" LR = 0.21
- Raised to 0.30 because search was thorough but not fully exhaustive
- Absence of announcement is notable given BNP benchmark and Litvack's ISDA proximity

---

### Null Result 2: No FINOS Presence
**Finding**: SocGen does not appear in any FINOS public listings, member directories, or contributor acknowledgments. FINOS is the home of CDM open source project.
**Maps to**: Custom absence indicator (no_finos_participation)
**Assigned LR**: 0.40
**Interpretation**: Moderate Pragmatist signal. FINOS membership and contribution are public. Absence suggests either no CDM community engagement or consuming via vendors without contributing.
**Direction**: PRAGMATIST

**Rationale for LR = 0.40**:
- Architects typically appear in FINOS listings (JP Morgan, Goldman Sachs, Deutsche Bank all visible)
- Absence is more likely for Pragmatists (~70%) than Architects (~30%)
- LR = 0.30 / 0.70 ≈ 0.43, rounded to 0.40

---

### Evidence Block 4: EMIR Compliance Without CDM Mention
**Finding**: SocGen's official EMIR page describes compliance with EU EMIR Refit (April 2024) and UK EMIR Refit (September 2024) but contains no mention of implementation technology, CDM, DRR, or any vendor reference.
**Maps to**: Custom absence indicator (regulatory_compliance_without_cdm_attribution)
**Assigned LR**: 0.50
**Interpretation**: Weak Pragmatist signal. EMIR Refit was an ideal use case for CDM/DRR. BNP Paribas explicitly announced CDM usage for CFTC rules. SocGen's silence on technology approach suggests either traditional implementation or deliberate non-disclosure.
**Direction**: PRAGMATIST

**Rationale for LR = 0.50**:
- Architects using CDM for regulatory reporting often publicize this (e.g., BNP, JP Morgan)
- Silence is more common among Pragmatists but not definitive
- P(silence | Architect) ≈ 0.35; P(silence | Pragmatist) ≈ 0.70
- LR = 0.35 / 0.70 = 0.50

---

### Evidence Block 5: SG-FORGE Alternative Innovation Focus
**Finding**: SocGen heavily invested in SG-FORGE, a fully regulated digital assets subsidiary focusing on blockchain tokenization, stablecoins (EUR CoinVertible, USD CoinVertible), and security token issuance. This represents a differentiated innovation strategy.
**Maps to**: Custom indicator (alternative_innovation_priority)
**Assigned LR**: 0.60
**Interpretation**: Weak Pragmatist signal. Strategic resources allocated to digital assets rather than derivatives standardization suggests different priorities. Innovation capacity is finite; heavy SG-FORGE investment may compete with CDM initiatives.
**Direction**: PRAGMATIST

**Rationale for LR = 0.60**:
- Alternative innovation focus is slightly more likely for Pragmatists
- Architects can also have parallel innovation streams, so this is weak evidence
- P(alt_innovation | Architect) ≈ 0.45; P(alt_innovation | Pragmatist) ≈ 0.75
- LR = 0.45 / 0.75 = 0.60

---

### Evidence Block 6: Capitolis Vendor Partnership
**Finding**: SocGen was "a key driver" of Capitolis's STP novations platform for FX derivatives automation. Solution is in production. Capitolis uses proprietary algorithms, not industry standards like CDM.
**Maps to**: `announced_vendor_only_approach` (partial match; LR = 0.25 base)
**Assigned LR**: 0.70
**Interpretation**: Very weak Pragmatist signal. Pursuing vendor-based automation over open standards suggests Pragmatist tendencies. However, this is for novations/compression (not regulatory reporting), so signal is weaker.
**Direction**: PRAGMATIST

**Rationale for LR = 0.70**:
- Base "announced vendor only approach" LR = 0.25 is too strong for adjacent use case
- Capitolis partnership is for operational efficiency (novations), not regulatory reporting
- Architects can use vendors alongside CDM; this is not mutually exclusive
- Raised to 0.70 to reflect weak signal for non-reporting use case

---

### Evidence Block 7: AI/Cloud Digital Strategy Priority
**Finding**: SocGen's official digital transformation strategy emphasizes AI (330+ AI solutions, SocGen AI entity) and cloud (multi-cloud migration target by 2025-2026). No mention of industry data standards (CDM, FpML) on digital strategy pages.
**Maps to**: Custom indicator (alternative_technology_priority)
**Assigned LR**: 0.70
**Interpretation**: Very weak Pragmatist signal. AI and cloud are mainstream priorities across all banks. Absence of data standardization mention suggests it is not a strategic communication priority, but this is common.
**Direction**: PRAGMATIST

**Rationale for LR = 0.70**:
- Almost all banks emphasize AI/cloud; this is not discriminating
- Absence of CDM mention is slightly more common for Pragmatists
- P(AI_focus_no_CDM | Architect) ≈ 0.60; P(AI_focus_no_CDM | Pragmatist) ≈ 0.85
- LR = 0.60 / 0.85 = 0.71, rounded to 0.70

---

### Neutral Evidence (Non-Discriminating)

The following evidence blocks are classified as NEUTRAL (LR ≈ 1.0) and do not significantly update probabilities:

- **Block 1**: Eric Litvack 10-year ISDA chairmanship - governance role, not implementation signal
- **Block 3**: Historical ISDA Resolution Stay Protocol adoption (2014) - predates CDM
- **Block 8**: Derivatives awards (2025) - business success, technology approach unclear
- **Block 9**: BNP CDM benchmark (comparative reference only)
- **Block 10**: Historical competitive dynamics with BNP - context only

These are excluded from LR calculation to avoid noise.

---

## Step 3: Combined Likelihood Ratio

**Positive Evidence**:
- LR_positive = 1.8 (Eric Litvack CDM panel moderation)

**Negative Evidence**:
- LR1 = 0.30 (No CDM/DRR announcement)
- LR2 = 0.40 (No FINOS presence)
- LR3 = 0.50 (EMIR compliance without CDM)
- LR4 = 0.60 (SG-FORGE alternative innovation)
- LR5 = 0.70 (Capitolis vendor partnership)
- LR6 = 0.70 (AI/cloud priority, no CDM mention)

**Product of Negative LRs**:
0.30 × 0.40 × 0.50 × 0.60 × 0.70 × 0.70
= 0.12 × 0.50 × 0.60 × 0.70 × 0.70
= 0.06 × 0.60 × 0.70 × 0.70
= 0.036 × 0.70 × 0.70
= 0.0252 × 0.70
= **0.01764**

**Combined LR (All Evidence)**:
Combined_LR = 1.8 × 0.01764 = **0.0318**

**Interpretation**: Evidence is approximately **31 times more likely** under the Pragmatist hypothesis than under the Architect hypothesis. This is a strong evidential shift toward Pragmatist.

---

## Step 4: Calibration Check

**Flag**: Combined LR < 0.01 threshold NOT triggered (0.0318 > 0.01)

**Independence Review**:
1. **Double-counting check**:
   - SG-FORGE (Block 5) and AI/cloud strategy (Block 7) both reflect "alternative priorities" - some overlap
   - Apply 50% discount to Block 7: LR6_adjusted = sqrt(0.70) = 0.84

2. **Absence evidence clustering**:
   - Null results (no announcement, no FINOS, no EMIR CDM) are partially correlated (same underlying cause: no CDM activity)
   - These remain distinct observable outcomes, so no further adjustment

**Recalculated Combined LR (with adjustment)**:
Positive: 1.8
Negative: 0.30 × 0.40 × 0.50 × 0.60 × 0.70 × 0.84
= 0.12 × 0.50 × 0.60 × 0.70 × 0.84
= 0.06 × 0.60 × 0.70 × 0.84
= 0.036 × 0.70 × 0.84
= 0.0252 × 0.84
= **0.02117**

**Adjusted Combined_LR** = 1.8 × 0.02117 = **0.0381**

This represents evidence approximately **26 times more likely** under Pragmatist than Architect. This is within reasonable bounds.

---

## Step 5: Posterior Odds

**Calculation**:
Posterior_Odds = Prior_Odds × Combined_LR
Posterior_Odds = 0.818 × 0.0381
Posterior_Odds = **0.0312**

---

## Step 6: Posterior Probability

**Calculation**:
P(Architect | Evidence) = Posterior_Odds / (1 + Posterior_Odds)
P(Architect | Evidence) = 0.0312 / (1 + 0.0312)
P(Architect | Evidence) = 0.0312 / 1.0312
P(Architect | Evidence) = **0.0303** (3.0%)

P(Pragmatist | Evidence) = 1 - P(Architect | Evidence)
P(Pragmatist | Evidence) = 1 - 0.0303
P(Pragmatist | Evidence) = **0.9697** (97.0%)

---

## Step 7: Sanity Checks

- [x] 0 <= P(Architect) <= 1
- [x] P(Architect) + P(Pragmatist) = 1.0 (0.030 + 0.970 = 1.0)
- [x] Combined LR within reasonable bounds (0.01 < 0.0381 < 100)
- [x] Probability shift matches evidence pattern (Strong shift from multiple Pragmatist signals + absence evidence)

**Flags**:
1. **Large probability shift (-42.0 pp)**: Justified by consistent null results across multiple search domains
2. **High posterior certainty (97%)**: Unusual after single tier, but evidence is consistently one-directional
3. **Single weak positive**: Only one positive signal (Eric Litvack moderation) insufficient to counter multiple null results
4. **"BNP follower" hypothesis rejected**: Evidence does not support lag-following behavior

---

## Step 8: Interpretation

**Prior to Posterior Change**:
- Prior P(Architect): 45%
- Posterior P(Architect): **3.0%**
- **Change**: -42.0 percentage points

**Direction**: Evidence strongly weakened Architect hypothesis

**Key Drivers**:

1. **Largest negative impacts**:
   - Null Result 1 (No CDM/DRR announcement): LR = 0.30 - strongest single piece of absence evidence
   - Null Result 2 (No FINOS presence): LR = 0.40 - absence from CDM community
   - Evidence Block 4 (EMIR without CDM): LR = 0.50 - missed opportunity to attribute compliance to CDM

2. **Largest positive impact**:
   - Evidence Block 2 (Litvack CDM panel): LR = 1.8 - insufficient to counter multiple negatives

3. **Overall pattern**: Consistent absence of CDM activity signals across official sources, ISDA, FINOS, and regulatory compliance communications. The only CDM-proximate evidence (Litvack moderation) reflects governance role rather than firm implementation. Alternative innovation paths (SG-FORGE, Capitolis) suggest differentiated strategy.

**Confidence Assessment**: **HIGH**
- High confidence that SocGen is NOT actively pursuing CDM adoption
- Evidence is consistently one-directional with no contradictions
- The 45% prior was overly optimistic; adjustment to 3% reflects reality of zero CDM signals

---

## Step 9: Pragmatist Variant Assessment

Given P(Pragmatist) = 97.0%, determine variant:

| Variant | Criteria | Evidence Match |
|---------|----------|----------------|
| Pragmatist-Regulatory-Compliant | Compliance focus, no standardization | **PARTIAL** - EMIR compliance evident |
| Pragmatist-Vendor-Dependent | Using vendors for derivatives tech | **YES** - Capitolis partnership confirmed |
| Pragmatist-Network-Accelerant | Passive ISDA/industry participation | **PARTIAL** - Litvack ISDA role but no CDM action |
| Pragmatist-Capacity-Constrained | Resources consumed elsewhere | **POSSIBLE** - SG-FORGE investment may compete |

**Preliminary Classification**: **Pragmatist-Vendor-Dependent** (primary) with **Pragmatist-Network-Accelerant** characteristics

**Rationale**:
- Active Capitolis partnership demonstrates vendor-based automation preference
- Historical ISDA leadership (Litvack) suggests network participation without CDM commitment
- SG-FORGE investment indicates innovation capacity directed elsewhere

**Confidence**: **High** (97%)

---

## Recommendation for Gate 1

**Sufficiency**: **POTENTIAL YES** - Evidence sufficient for >80% Pragmatist confidence (97%)

**Key Considerations**:

1. **For SKIP TO ADVERSARIAL**:
   - P(Pragmatist) = 97% greatly exceeds 80% threshold
   - Null results are comprehensive across multiple domains
   - No contradictory Architect signals found
   - Single positive (Litvack moderation) is weak and fully incorporated

2. **For CONTINUE TO TIER 2**:
   - Could SocGen be doing quiet CDM work without public announcement?
   - LinkedIn personnel search might reveal internal CDM activity
   - French-language sources not fully explored

**Recommendation**: **Consider SKIP TO ADVERSARIAL** pending Gate 1 analysis

The consistent null results across ISDA, FINOS, official sources, and regulatory communications, combined with clear alternative innovation signals (SG-FORGE, Capitolis), suggest Tier 2 is unlikely to reveal hidden Architect activity. However, the Gate 1 adversarial challenge should test whether "quiet CDM adoption" is a plausible explanation.

---

## Summary Table

| Metric | Value |
|--------|-------|
| Prior P(Architect) | 45% |
| Combined LR | 0.0381 (adjusted for independence) |
| Posterior Odds | 0.0312 |
| Posterior P(Architect) | 3.0% |
| Posterior P(Pragmatist) | 97.0% |
| Change | -42.0 pp |
| Preliminary Classification | Pragmatist-Vendor-Dependent |
| Confidence | High |
| Gate 1 Recommendation | Consider SKIP TO ADVERSARIAL |
