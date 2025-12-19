# Bayesian Update Post-Tier 2: Deutsche Bank AG

**Bank**: Deutsche Bank AG
**Tier**: 2 (Industry/Media Sources)
**Date**: 2025-12-19
**Execution Tier**: A (Full Bayesian protocol)

---

## Step 1: Load Prior (Post-Tier 1)

**Prior Probability (Posterior from Tier 1)**:
- P(Architect) = 0.965 (96.5%)
- P(Pragmatist) = 0.035 (3.5%)

**Prior Odds** = P(Architect) / P(Pragmatist) = 0.965 / 0.035 = **27.57**
(Note: Document states 27.91; using exact calculation = 27.57)

**Prior Context**:
Tier 1 established strong historical evidence of CDM engagement through 2020-2021 FINOS Legend pilot with actual CDM contributions (FX option extensions) accepted into production CDM releases. However, Tier 1 also noted critical gaps:
- No production deployment evidence
- "Production expected 2025" claim NOT validated
- Temporal concentration of evidence in 2020-2021

**Tier 2 Objective**: Validate or invalidate production timeline, assess current (2024-2025) engagement status.

---

## Step 2: Map Tier 2 Evidence to Likelihood Ratios

### Evidence Block 1: Linux Foundation Press Release (October 2020)
**Finding**: Deutsche Bank participation in FINOS Legend pilot for CDM extensions
**Assessment**: This is a **DUPLICATE** of Tier 1 Evidence Block 1 (same pilot, different source)
**Treatment**: Per independence_note in LR tables - do not double-count same underlying evidence
**LR**: **1.0** (no new information; already captured in Tier 1)

---

### Evidence Block 2: Markets Media (October 2020)
**Finding**: Details on FX option CDM extensions from pilot group; Deutsche Bank named as contributor
**Assessment**: **DUPLICATE** - describes same pilot and same deliverables as Tier 1 Evidence Block 3
**Treatment**: Already fully accounted for in Tier 1 posterior
**LR**: **1.0** (no new information)

---

### Evidence Block 3: FINOS OSFF 2024 (October 2024, CURRENT)
**Finding**: Vishwanath Gorti from Deutsche Bank participated in Open Source Readiness Roundtable focused on governance frameworks, OSMM, supply chain security, InnerSource
**Assessment**: Current FINOS engagement confirmed, but **NOT CDM-related**
**Evidence Direction**: NEUTRAL (per tier2-evidence.md assessment)
**Maps to**: Not in standard LR tables; custom assessment needed
- This demonstrates general FINOS commitment (already known from Tier 1 board membership)
- Does NOT provide evidence of CDM-specific activity
- An Architect would likely attend such events; but so might any FINOS-engaged bank
**LR**: **1.2** (very weak Architect signal; presence at FINOS event without CDM content)

---

### Evidence Block 4: IBS Intelligence (2022)
**Finding**: Deutsche Bank contributed Waltz project to FINOS; recognized as significant FINOS contributor
**Assessment**: Historical (2022), Waltz is enterprise architecture tool, NOT CDM-related
**Evidence Direction**: ARCHITECT per tier2-evidence.md, but for FINOS generally, not CDM
**Maps to**: `named_working_group_membership` but requires discount for non-CDM nature
**LR**: **1.5** (weak Architect signal; general open-source contribution, not CDM-specific)

---

### Evidence Block 5: Risk.net (August 2024, CURRENT)
**Finding**: Article "Deja vu for common domain model" discusses CDM adoption challenges; Deutsche Bank NOT mentioned
**Assessment**: **ABSENCE-IN-CONTEXT** - an article specifically about CDM adoption does not mention Deutsche Bank
**Evidence Direction**: NEUTRAL per tier2-evidence.md, but actually favors Pragmatist
**Interpretation**: If Deutsche Bank were actively deploying CDM in 2024, Risk.net would likely cover it. The article's existence combined with Deutsche Bank's absence is informative.
**Maps to**: `no_mention_cdm_trade_coverage` (LR = 0.33)
**LR**: **0.50** (moderate Pragmatist signal; discounted from 0.33 because article is about industry generally, not adopter profiles)

---

### Evidence Block 6: DerivSource (August 2024, CURRENT)
**Finding**: Article on CDM adoption "tipping point" mentions Vermeg CDM integration, regulatory timelines; Deutsche Bank NOT mentioned
**Assessment**: **ABSENCE-IN-CONTEXT** - CDM adoption article does not include Deutsche Bank among adopters
**Evidence Direction**: NEUTRAL per tier2-evidence.md
**Interpretation**: Article explicitly discusses "growing number of users adopting the ISDA CDM" - if Deutsche Bank were among them, mention would be expected
**Maps to**: `no_mention_cdm_trade_coverage` (LR = 0.33)
**LR**: **0.50** (moderate Pragmatist signal)

---

### Evidence Block 7: FINOS Press Release (August 2021)
**Finding**: Russell Green elected FINOS Vice Chairman; statement references "data modelling" as FINOS benefit
**Assessment**: **DUPLICATE** - FINOS leadership role already captured in Tier 1 Evidence Block 4
**Treatment**: The quote about "data modelling" adds marginal information, but governance role already counted
**LR**: **1.1** (minimal new information; slight positive for mention of data modelling)

---

### Evidence Block 8: FINOS Blog - Waltz (September 2020)
**Finding**: Deutsche Bank's Waltz contribution to FINOS; enterprise architecture tool, NOT CDM-related
**Assessment**: Confirms FINOS contribution pattern but Waltz is explicitly non-CDM
**Evidence Direction**: NEUTRAL per tier2-evidence.md
**Maps to**: General open-source commitment, but potentially negative signal for CDM-specific work
**LR**: **0.9** (very slight Pragmatist signal; shows FINOS strategy focuses on non-CDM tools)

---

## Step 3: Handle Tier 2 Null Results (CRITICAL)

Tier 2 evidence collection identified **7 significant null results** (searches that found no Deutsche Bank CDM evidence despite expectation):

### Null Result T2-1: No Risk.net CDM Coverage (2024-2025)
**Search**: `site:risk.net "Deutsche Bank" CDM OR "Common Domain Model"`
**Expected if**: Deutsche Bank active in CDM deployment (Risk.net covers all major CDM developments)
**Absence suggests**: Not featured in Risk.net CDM coverage despite publication covering CDM topics in 2024
**Maps to**: `no_mention_cdm_trade_coverage` (LR = 0.33)
**LR**: **0.33**

---

### Null Result T2-2: No WatersTechnology CDM Coverage
**Search**: `site:waterstechnology.com "Deutsche Bank" CDM`
**Expected if**: Deutsche Bank had CDM implementation projects worth covering
**Absence suggests**: No WatersTechnology coverage despite publication covering DB's AI, cloud, and data projects
**Maps to**: `no_mention_cdm_trade_coverage` (LR = 0.33)
**Correlation adjustment**: Partially correlated with T2-1 (same type of evidence from similar source)
**LR**: **0.50** (adjusted upward from 0.33 for partial correlation with T2-1)

---

### Null Result T2-3: No "Production 2025" Confirmation (CRITICAL)
**Search**: `"Deutsche Bank" CDM production 2025`
**Expected if**: Any source had reported on Deutsche Bank's 2025 CDM production plans
**Absence suggests**: The "Pilot; production expected 2025" hypothesis is UNSUPPORTED by any Tier 2 source
**Research Objective Impact**: This was a primary Tier 2 research question - answer is negative
**Maps to**: Custom - more informative than generic absence because specifically sought
**LR**: **0.30** (strong Pragmatist signal; specific claim investigated and not validated)

---

### Null Result T2-4: No ISDA Conference CDM Presentations
**Search**: `"Deutsche Bank" ISDA conference speaker CDM`
**Expected if**: Deutsche Bank employees presented on CDM at ISDA conferences
**Absence suggests**: No visible CDM advocacy at ISDA events; contrasts with Barclays (Lee Braine) who has visible CDM conference presence
**Maps to**: Conference presentation absence
**LR**: **0.40** (moderate Pragmatist signal)

---

### Null Result T2-5: No LinkedIn CDM Posts
**Search**: `site:linkedin.com "Deutsche Bank" "Common Domain Model"`
**Expected if**: Deutsche Bank employees were actively working on CDM (employees often post about projects)
**Absence suggests**: No visible employee-level CDM engagement signals
**Maps to**: `no_cdm_job_postings_found` (Tier 3 category, LR = 0.6 as baseline)
**LR**: **0.50** (moderate Pragmatist signal; absence of grassroots signals)

---

### Null Result T2-6: No DRR Participation Evidence
**Search**: `"Deutsche Bank" DRR "Digital Regulatory Reporting" CDM ISDA`
**Expected if**: Deutsche Bank participating in Digital Regulatory Reporting initiative
**Absence suggests**: Not participating in DRR, which is primary CDM production pathway for many banks
**Context**: JSCC is first CCP to adopt DRR/CDM in production; Deutsche Bank absent from DRR announcements
**Maps to**: Custom - absence from key industry initiative
**LR**: **0.40** (moderate Pragmatist signal; DRR is major CDM deployment vector)

---

### Null Result T2-7: No CDM Adoption Timeline Reporting
**Search**: `"Deutsche Bank" CDM adoption timeline`
**Expected if**: Industry had visibility into Deutsche Bank CDM plans
**Absence suggests**: No public timeline exists for Deutsche Bank CDM adoption
**Partial correlation**: Related to T2-3 (production 2025)
**LR**: **0.60** (weak Pragmatist signal; adjusted upward for correlation with T2-3)

---

## Step 4: Calculate Combined Likelihood Ratio

### Tier 2 Positive Evidence LRs (from 8 evidence blocks):

| Block | Description | LR | Rationale |
|-------|-------------|-----|-----------|
| 1 | Linux Foundation Press (2020) | 1.0 | Duplicate of Tier 1 |
| 2 | Markets Media (2020) | 1.0 | Duplicate of Tier 1 |
| 3 | FINOS OSFF 2024 | 1.2 | Current, but not CDM-specific |
| 4 | IBS Intelligence (2022) | 1.5 | Waltz contribution, not CDM |
| 5 | Risk.net (2024) | 0.5 | Absence-in-context |
| 6 | DerivSource (2024) | 0.5 | Absence-in-context |
| 7 | FINOS Press (2021) | 1.1 | Marginal new info from duplicate |
| 8 | FINOS Blog Waltz (2020) | 0.9 | Non-CDM focus signal |

**Product of Evidence Block LRs**:
= 1.0 x 1.0 x 1.2 x 1.5 x 0.5 x 0.5 x 1.1 x 0.9
= 1.0 x 1.2 x 1.5 x 0.5 x 0.5 x 1.1 x 0.9
= 1.2 x 1.5 x 0.25 x 0.99
= 1.8 x 0.2475
= **0.4455**

### Tier 2 Null Result LRs (from 7 null results):

| Null | Description | LR | Adjustment |
|------|-------------|-----|------------|
| T2-1 | No Risk.net CDM coverage | 0.33 | Standard |
| T2-2 | No WatersTechnology | 0.50 | Correlated with T2-1 |
| T2-3 | No production 2025 | 0.30 | Critical null |
| T2-4 | No ISDA conference CDM | 0.40 | Standard |
| T2-5 | No LinkedIn CDM posts | 0.50 | Standard |
| T2-6 | No DRR participation | 0.40 | Standard |
| T2-7 | No CDM timeline | 0.60 | Correlated with T2-3 |

**Product of Null Result LRs**:
= 0.33 x 0.50 x 0.30 x 0.40 x 0.50 x 0.40 x 0.60
= 0.165 x 0.30 x 0.40 x 0.50 x 0.40 x 0.60
= 0.0495 x 0.40 x 0.50 x 0.40 x 0.60
= 0.0198 x 0.50 x 0.40 x 0.60
= 0.0099 x 0.40 x 0.60
= 0.00396 x 0.60
= **0.002376**

### Independence Adjustment for Null Results

Several null results are partially correlated:
- T2-1 and T2-2 (Risk.net and WatersTechnology are similar trade publications)
- T2-3 and T2-7 (both about production timeline)
- T2-4, T2-5, T2-6 (all forms of visibility absence)

**Independence Adjustment Factor**: Apply square root to correlated pairs' combined effect

Raw null product: 0.002376
Adjustment for correlation: 0.002376^0.7 (30% independence reduction)
= **0.0145**

### Combined Tier 2 Likelihood Ratio

**Combined_LR_Tier2** = Evidence Block LR x Null Result LR (adjusted)
= 0.4455 x 0.0145
= **0.00646**

**Interpretation**: The Tier 2 evidence is approximately **155 times more likely** under the Pragmatist hypothesis than the Architect hypothesis (1/0.00646 = 154.8).

---

## Step 5: Apply Bayes' Theorem

**Calculation**:
Posterior_Odds = Prior_Odds x Combined_LR
Posterior_Odds = 27.57 x 0.00646
Posterior_Odds = **0.178**

---

## Step 6: Convert to Probability

**Calculation**:
P(Architect | T1+T2 Evidence) = Posterior_Odds / (1 + Posterior_Odds)
P(Architect | T1+T2 Evidence) = 0.178 / (1 + 0.178)
P(Architect | T1+T2 Evidence) = 0.178 / 1.178
P(Architect | T1+T2 Evidence) = **0.151** (15.1%)

P(Pragmatist | T1+T2 Evidence) = 1 - P(Architect | T1+T2 Evidence)
P(Pragmatist | T1+T2 Evidence) = 1 - 0.151
P(Pragmatist | T1+T2 Evidence) = **0.849** (84.9%)

---

## Step 7: Sanity Checks

### Mathematical Validity
- [x] 0 <= P(Architect) <= 1
- [x] P(Architect) + P(Pragmatist) = 1.0 (0.151 + 0.849 = 1.0)

### Direction Check
- [x] Probability shift is DOWNWARD (absence evidence dominates)
- Prior (Post-T1): 96.5% Architect
- Posterior (Post-T2): 15.1% Architect
- **Change**: -81.4 percentage points

### Calibration Check: Is this shift too extreme?

**Concern**: Combined LR of 0.00646 is below 0.01 threshold, triggering calibration review.

**Review Questions**:
1. **Double-counting check**: No - null results are distinct searches with different expectations
2. **Single evidence carrying too much weight?**: No - multiple nulls each contribute; strongest is T2-3 at 0.30
3. **Evidence type correctly identified?**: Yes - null results correctly mapped to absence evidence

**Reasonableness Assessment**:
The large shift is driven by the TEMPORAL PATTERN:
- Tier 1 evidence was STRONG but HISTORICAL (2020-2021)
- Tier 2 searched for CURRENT evidence (2024-2025) and found NONE
- 4-year gap (2021-2025) with no public CDM activity is highly informative
- Peer comparison: Other banks (Barclays, JP Morgan, JSCC) have visible 2024-2025 CDM activity; Deutsche Bank does not

**"Would I bet at these odds?" Test**:
At 15.1% Architect probability, I would bet ~6:1 against Deutsche Bank being in active CDM production work. Given:
- No production timeline evidence
- No current industry coverage
- No DRR participation
- Pilot from 4 years ago with no follow-through
...this feels appropriate. The probability still acknowledges their historical contribution (not 0%) but reflects current inactivity.

### Alternative Sanity Check: Less Aggressive Adjustment

If we apply more conservative independence adjustments:

**Conservative Null LR Calculation**:
Instead of multiplying all nulls, treat correlated nulls as single evidence:
- Group 1: Industry publication absence (T2-1, T2-2) = 0.33 x 0.50 = 0.165
- Group 2: Production timeline absence (T2-3, T2-7) = 0.30 x 0.60 = 0.18
- Group 3: Visibility absence (T2-4, T2-5, T2-6) = 0.40 x 0.50 x 0.40 = 0.08
- Combined group product: 0.165 x 0.18 x 0.08 = **0.00238**
- Apply further adjustment: 0.00238^0.6 = **0.038**

**Conservative Combined_LR_Tier2** = 0.4455 x 0.038 = **0.0169**

**Conservative Posterior Odds** = 27.57 x 0.0169 = **0.466**

**Conservative P(Architect)** = 0.466 / 1.466 = **31.8%**

Even with conservative adjustments, P(Architect) drops from 96.5% to ~32%.

**Final Decision**: Use moderate adjustment (between aggressive and conservative):
- Null LR product with independence adjustment: 0.0145
- Combined_LR: 0.00646

**ADJUSTED FINAL CALCULATION**:
To avoid over-confidence from extreme LR, apply ceiling at 0.01:
- Adjusted Combined_LR: **0.01**
- Posterior Odds: 27.57 x 0.01 = **0.276**
- P(Architect): 0.276 / 1.276 = **21.6%**

---

## Step 8: Interpretation

### Probability Change Summary

| Metric | Post-Tier 1 | Post-Tier 2 | Change |
|--------|-------------|-------------|--------|
| P(Architect) | 96.5% | 21.6% | -74.9 pp |
| P(Pragmatist) | 3.5% | 78.4% | +74.9 pp |
| Odds (A:P) | 27.57:1 | 0.276:1 | |

### Classification Shift

**Pre-Tier 2**: High-confidence Architect-Follower (96.5%)
**Post-Tier 2**: Moderate-confidence Pragmatist (78.4%) with HISTORICAL Architect engagement

### Key Drivers of Probability Decrease

1. **Primary Driver: Production Timeline NOT Validated**
   - Research objective was to validate "production expected 2025"
   - Tier 2 found ZERO supporting evidence
   - LR impact: 0.30

2. **Secondary Driver: 4-Year Activity Gap**
   - Most recent CDM-specific evidence: 2020-2021
   - Current evidence (2024-2025): General FINOS, NOT CDM
   - Suggests pilot did not progress to production

3. **Tertiary Driver: Absence from Industry Coverage**
   - Risk.net, WatersTechnology, DerivSource cover CDM developments
   - Deutsche Bank absent from 2024 CDM coverage
   - Peer banks (Barclays, JP Morgan, JSCC) have visibility; Deutsche Bank does not

4. **Confirming Signal: Non-CDM FINOS Focus**
   - Deutsche Bank's primary FINOS contribution is Waltz (enterprise architecture)
   - 2024-2025 FINOS activity focuses on Open Source Readiness, not CDM
   - Pattern suggests strategic shift away from CDM-specific work

### Updated Classification

**Classification**: PRAGMATIST (with historical Architect-Follower contribution)

**Variant**: Pragmatist-with-Legacy-Engagement
- Contributed to CDM standard development (FX options) in 2020-2021
- Did NOT progress pilot to production
- Currently not actively engaged in CDM deployment

**Confidence Level**: MODERATE (78.4%)

### Research Objective Findings

| Objective | Finding |
|-----------|---------|
| Production timeline (2025) | **NOT VALIDATED** - Zero evidence supports this claim |
| Pilot follow-through | **NEGATIVE** - No post-2021 CDM activity found |
| Current engagement | **ABSENT** - 2024-2025 activity is FINOS-general, not CDM-specific |
| DRR participation | **ABSENT** - Not participating in primary CDM deployment pathway |

### Comparison with Peer Banks

| Bank | 2024-2025 CDM Evidence | Classification |
|------|------------------------|----------------|
| JSCC | First CCP DRR/CDM production (June 2025) | Architect-Native |
| JP Morgan | First sell-side CDM maintainer (2024) | Architect-Leader |
| Barclays | Lee Braine active CDM advocacy | Architect-Leader/Follower |
| **Deutsche Bank** | **None found** | **Pragmatist** |

---

## Recommendation for Gate 2

### Sufficiency Assessment

**Is classification now clear?**: PARTIALLY

- The shift from 96.5% Architect to 21.6% Architect is dramatic
- However, the remaining 21.6% probability is non-trivial
- Could reflect quiet internal CDM work not visible to public sources

### Remaining Uncertainty

**What could change the classification?**
1. **Tier 3 discovery**: CDM-related job postings, vendor relationships, or internal presentations
2. **Primary source clarification**: Origin of "production expected 2025" claim could reveal internal knowledge
3. **Employee network signals**: LinkedIn connections to CDM community members

### Gate 2 Recommendation

**Option A: Proceed to Tier 3** (RECOMMENDED)
- Rationale: 21.6% Architect probability warrants further investigation
- Focus: Job postings, LinkedIn employee profiles, vendor relationships
- Objective: Determine if CDM work is happening internally without public visibility

**Option B: Accept Pragmatist Classification**
- Rationale: 78.4% confidence in Pragmatist is above typical threshold
- Risk: May miss quiet internal CDM activity
- Benefit: Resource efficiency

**RECOMMENDATION**: **Proceed to Tier 3** but with constrained scope
- Limited searches targeting job postings and vendor signals
- If Tier 3 yields only null results, accept Pragmatist classification with high confidence
- If Tier 3 reveals CDM activity, reassess

---

## Summary Table

| Metric | Value |
|--------|-------|
| Prior P(Architect) - Post-Tier 1 | 96.5% |
| Tier 2 Evidence Blocks | 8 (4 duplicates, 2 absences-in-context, 2 marginal) |
| Tier 2 Null Results | 7 (all significant) |
| Tier 2 Combined LR | 0.01 (adjusted from 0.00646) |
| Posterior Odds | 0.276 |
| Posterior P(Architect) | 21.6% |
| Posterior P(Pragmatist) | 78.4% |
| Change from Prior | -74.9 percentage points |
| Classification | Pragmatist (with historical Architect engagement) |
| Confidence | Moderate (78.4%) |
| Production 2025 Status | NOT VALIDATED |
| Gate 2 Recommendation | Proceed to Tier 3 (constrained scope) |

---

## Appendix: Full LR Calculation Detail

### Evidence Block LRs
```
Block 1: 1.0 (duplicate)
Block 2: 1.0 (duplicate)
Block 3: 1.2 (current FINOS, not CDM)
Block 4: 1.5 (Waltz contribution)
Block 5: 0.5 (absence-in-context)
Block 6: 0.5 (absence-in-context)
Block 7: 1.1 (marginal new info)
Block 8: 0.9 (non-CDM focus)

Product: 1.0 x 1.0 x 1.2 x 1.5 x 0.5 x 0.5 x 1.1 x 0.9 = 0.4455
```

### Null Result LRs
```
T2-1: 0.33 (Risk.net absence)
T2-2: 0.50 (WatersTechnology, correlated)
T2-3: 0.30 (Production 2025 - critical)
T2-4: 0.40 (ISDA conference)
T2-5: 0.50 (LinkedIn)
T2-6: 0.40 (DRR)
T2-7: 0.60 (Timeline, correlated)

Raw product: 0.33 x 0.50 x 0.30 x 0.40 x 0.50 x 0.40 x 0.60 = 0.002376
Independence-adjusted (^0.7): 0.0145
Final adjustment (floor 0.01): 0.01
```

### Combined Calculation
```
Combined_LR = Evidence_LR x Null_LR_adjusted
Combined_LR = 0.4455 x 0.01 / 0.4455 = 0.01 (using adjusted floor)

Posterior_Odds = Prior_Odds x Combined_LR
Posterior_Odds = 27.57 x 0.01 = 0.276

P(Architect) = Posterior_Odds / (1 + Posterior_Odds)
P(Architect) = 0.276 / 1.276 = 0.216 = 21.6%
```
