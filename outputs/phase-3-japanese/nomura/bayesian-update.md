# Bayesian Update: Nomura Holdings, Inc.

**Bank**: Nomura Holdings, Inc.
**Date**: 2025-12-19
**Protocol**: Tier B (Abbreviated)
**Prior Probability**: P(Architect) = 35%

---

## Prior Probability Justification

**P(ARCHITECT) = 35%**

Justification:
- Japan's largest investment bank with global derivatives operations
- JSCC clearing member with mandatory CDM connectivity (confirmed June 2025)
- Post-Lehman acquisition gives global footprint (Americas + EMEA)
- Historical pattern of following industry standards rather than leading
- Higher prior than other Japanese banks due to investment banking focus

**P(PRAGMATIST) = 45%**

Justification:
- Investment bank profile suggests engagement with derivatives standards
- Likely to adopt industry solutions for regulatory compliance
- Global operations create multi-jurisdictional compliance needs
- Vendor relationships expected for operational efficiency

**P(NOT ENGAGED) = 20%**

Justification:
- Low probability given JSCC CDM go-live requirement
- Global derivatives operations require some level of standards engagement
- However, could be minimal compliance-only approach

---

## Evidence Evaluation

### Evidence Item 1: JSCC CDM Connectivity (NOM-001)

**Type**: Infrastructure Requirement (Tier 1)
**Quality**: HIGH

**Likelihood Ratios**:
- P(JSCC connectivity | ARCHITECT) = 1.0
  - *Architects would definitely connect to JSCC*
- P(JSCC connectivity | PRAGMATIST) = 1.0
  - *Pragmatists would comply with CCP requirements*
- P(JSCC connectivity | NOT ENGAGED) = 0.2
  - *Difficult to maintain clearing membership without connectivity*

**Bayes Factor**:
- BF(PRAGMATIST / ARCHITECT) = 1.0 / 1.0 = 1.0 (neutral)
- BF(NOT ENGAGED / ARCHITECT) = 0.2 / 1.0 = 0.2 (disfavors Not Engaged)

**Impact**: Eliminates "Not Engaged" but neutral between Architect and Pragmatist

### Evidence Item 2: Absence of CDM Contribution Evidence (NOM-003)

**Type**: Informative Absence (Tier 1)
**Quality**: MEDIUM (limited by search constraints)

**Likelihood Ratios**:
- P(No contribution evidence | ARCHITECT) = 0.15
  - *True architects have visible contribution footprints*
  - *Nomura-level institution would be cited in ISDA materials*
- P(No contribution evidence | PRAGMATIST) = 0.80
  - *Pragmatists don't contribute to standard development*
  - *Consistent with follower/adopter pattern*
- P(No contribution evidence | NOT ENGAGED) = 0.90
  - *Would expect no contribution evidence if not engaged*

**Bayes Factor**:
- BF(PRAGMATIST / ARCHITECT) = 0.80 / 0.15 = 5.33 (strongly favors Pragmatist)
- BF(NOT ENGAGED / ARCHITECT) = 0.90 / 0.15 = 6.0 (strongly favors Not Engaged)

**Impact**: Strong evidence against Architect classification

### Evidence Item 3: Business Model Analysis (NOM-002)

**Type**: Structural/Contextual (Tier 4)
**Quality**: LOW (inference, not direct evidence)

**Likelihood Ratios**:
- P(Global investment bank profile | ARCHITECT) = 0.60
  - *Investment banks are more likely to engage with derivatives standards*
- P(Global investment bank profile | PRAGMATIST) = 0.70
  - *Investment banks need efficient derivatives operations*
- P(Global investment bank profile | NOT ENGAGED) = 0.30
  - *Less likely for investment bank to be completely disengaged*

**Bayes Factor**:
- BF(PRAGMATIST / ARCHITECT) = 0.70 / 0.60 = 1.17 (slight favor to Pragmatist)
- BF(NOT ENGAGED / ARCHITECT) = 0.30 / 0.60 = 0.50 (disfavors Not Engaged)

**Impact**: Weak evidence, slight favor to Pragmatist

### Evidence Item 4: Japanese Bank Cohort Pattern (NOM-004)

**Type**: Comparative Inference (Tier 3)
**Quality**: LOW

**Likelihood Ratios**:
- P(Japanese cohort pattern | ARCHITECT) = 0.30
  - *If architect, would expect differentiation from cohort*
- P(Japanese cohort pattern | PRAGMATIST) = 0.75
  - *Consistent with Japanese collective adoption approach*
- P(Japanese cohort pattern | NOT ENGAGED) = 0.60
  - *Japanese banks may collectively be non-engaged*

**Bayes Factor**:
- BF(PRAGMATIST / ARCHITECT) = 0.75 / 0.30 = 2.5 (favors Pragmatist)
- BF(NOT ENGAGED / ARCHITECT) = 0.60 / 0.30 = 2.0 (favors Not Engaged)

**Impact**: Moderate evidence for Pragmatist

### Evidence Item 5: Vendor Mediation Pattern (NOM-005)

**Type**: Industry Pattern Analysis (Tier 2)
**Quality**: MEDIUM

**Likelihood Ratios**:
- P(Vendor-mediated approach | ARCHITECT) = 0.35
  - *Architects use vendors but lead strategy themselves*
- P(Vendor-mediated approach | PRAGMATIST) = 0.85
  - *Defining characteristic of pragmatist approach*
- P(Vendor-mediated approach | NOT ENGAGED) = 0.50
  - *May use legacy vendor systems without CDM*

**Bayes Factor**:
- BF(PRAGMATIST / ARCHITECT) = 0.85 / 0.35 = 2.43 (favors Pragmatist)
- BF(NOT ENGAGED / ARCHITECT) = 0.50 / 0.35 = 1.43 (slight favor to Not Engaged)

**Impact**: Moderate evidence for Pragmatist

---

## Bayesian Calculation

### Combined Bayes Factors

**Odds Ratio (PRAGMATIST / ARCHITECT)**:
Combined BF = 1.0 x 5.33 x 1.17 x 2.5 x 2.43 = **37.86**

Evidence quality discount (0.4 weight due to simulated searches):
Adjusted BF = 37.86^0.4 = **4.77**

**Odds Ratio (NOT ENGAGED / ARCHITECT)**:
Combined BF = 0.2 x 6.0 x 0.50 x 2.0 x 1.43 = **1.72**

Evidence quality discount (0.4 weight):
Adjusted BF = 1.72^0.4 = **1.25**

### Posterior Calculation

**Starting Odds**:
- Odds(ARCHITECT) = 35/65 = 0.538
- Odds(PRAGMATIST) = 45/55 = 0.818
- Odds(NOT ENGAGED) = 20/80 = 0.25

**Updated Odds**:
- Prior Odds(PRAGMATIST / ARCHITECT) = 0.818 / 0.538 = 1.52
- Posterior Odds(PRAGMATIST / ARCHITECT) = 1.52 x 4.77 = **7.25**

- Prior Odds(NOT ENGAGED / ARCHITECT) = 0.25 / 0.538 = 0.465
- Posterior Odds(NOT ENGAGED / ARCHITECT) = 0.465 x 1.25 = **0.58**

**Converting to Probabilities**:

Let P(A) = P(Architect), P(P) = P(Pragmatist), P(N) = P(Not Engaged)

From odds:
- P(P) / P(A) = 7.25
- P(N) / P(A) = 0.58
- P(A) + P(P) + P(N) = 1

Solving:
- P(P) = 7.25 x P(A)
- P(N) = 0.58 x P(A)
- P(A) x (1 + 7.25 + 0.58) = 1
- P(A) x 8.83 = 1
- **P(ARCHITECT) = 11.3%**
- **P(PRAGMATIST) = 82.1%**
- **P(NOT ENGAGED) = 6.6%**

---

## Posterior Probability Summary

| Classification | Prior | Posterior | Change |
|---------------|-------|-----------|--------|
| ARCHITECT | 35.0% | 11.3% | -23.7% |
| PRAGMATIST | 45.0% | 82.1% | +37.1% |
| NOT ENGAGED | 20.0% | 6.6% | -13.4% |

---

## Analysis

### ARCHITECT: 35% -> 11.3% (Strong Decrease)

**Key Drivers**:
1. Complete absence of CDM contribution evidence (strongest signal)
2. Japanese cohort pattern suggests follower rather than leader
3. Vendor mediation pattern inconsistent with Architect role
4. JSCC connectivity alone does not indicate strategic CDM commitment

### PRAGMATIST: 45% -> 82.1% (Strong Increase)

**Key Drivers**:
1. JSCC connectivity confirms engagement (not "Not Engaged")
2. Absence of leadership signals fits Pragmatist profile
3. Vendor-mediated implementation pattern
4. Japanese collective adoption approach
5. Global operations drive standards adoption for efficiency

### NOT ENGAGED: 20% -> 6.6% (Moderate Decrease)

**Key Drivers**:
1. JSCC CDM connectivity requirement eliminates non-engagement
2. Global derivatives operations require some standards engagement
3. Investment bank profile inconsistent with complete disengagement

---

## Gate 1 Decision

**Threshold for Architect Classification**: P(Architect) > 60%
**Current Posterior**: P(Architect) = 11.3%

**Decision: FAIL Architect Threshold**

**Proceed to Abbreviated Adversarial Analysis**:
- Classification: PRAGMATIST (82.1%)
- Sub-classification: Vendor-Dependent (based on vendor mediation pattern)
- Adversarial focus: Challenge assumption of non-Architect status

---

## Confidence Assessment

**Overall Confidence in PRAGMATIST Classification**: MODERATE-HIGH (70%)

**Supporting Factors**:
- Strong Bayesian signal (82.1% posterior)
- Evidence pattern consistent with Pragmatist profile
- JSCC connectivity confirms engagement
- Vendor mediation pattern well-established for Japanese institutions

**Limiting Factors**:
- Evidence based on simulated searches
- Japanese-language sources not accessed
- Possible hidden Architect activity not visible in English sources
- Timing uncertainty (current snapshot only)

---

## Next Steps

**Proceed to**: Abbreviated Adversarial Analysis (Tier B)

**Focus Areas**:
1. Challenge "hidden Architect" hypothesis
2. Verify absence of contribution evidence is informative
3. Consider timing effects (evaluation phase)
4. Test Pragmatist vs Not Engaged boundary
