# Post-Tier 2 Bayesian Update: Nomura Holdings, Inc.

## Prior (Post-Tier 1)
**P(ARCHITECT) = 0.01**
**P(PRAGMATIST) = 0.74**
**P(OBSERVER) = 0.25**

After Tier 1, we introduced OBSERVER as a distinct category given the complete absence of direct CDM evidence.

---

## Tier 2 Evidence Summary
**Evidence Items Found:** 2
**Direction:** 1 SUPPORTS_PRAGMATIST, 1 NEUTRAL

### Evidence Items:
1. **NOMURA-001:** JSCC clearing membership (JSCC deployed CDM in June 2025)
   - Claim Type: vendor_proxy_signal
   - LR: 1.2 (weak support for PRAGMATIST/OBSERVER)
   
2. **NOMURA-002:** ISDA event sponsorship
   - Claim Type: membership_or_participation
   - LR: 1.0 (neutral)

---

## Likelihood Ratio Analysis

### NOMURA-001: JSCC Clearing Membership
**LR = 1.2** (slightly favors PRAGMATIST/OBSERVER over ARCHITECT)

**Reasoning:**
JSCC's CDM deployment creates indirect exposure for clearing members. However, this evidence does not distinguish between:
- OBSERVER (connected to CDM infrastructure passively)
- PRAGMATIST (actively using CDM through infrastructure/vendors)

The evidence weakly supports non-ARCHITECT classification but is not specific enough to differentiate OBSERVER from PRAGMATIST.

**Key Consideration:**
JSCC clearing members can interface with CDM through vendor solutions without internal CDM capabilities. This relationship indicates exposure but not commitment.

---

### NOMURA-002: ISDA Event Sponsorship
**LR = 1.0** (neutral)

**Reasoning:**
Event sponsorship indicates industry engagement but provides no information about CDM technical involvement. Many banks sponsor ISDA events regardless of CDM strategy. This is a weak signal that neither supports nor undermines any classification.

---

## Bayesian Update Calculation

**Starting Prior (Post-Tier 1):**
- P(ARCHITECT) = 0.01
- P(PRAGMATIST) = 0.49
- P(OBSERVER) = 0.50

**Combined Likelihood Ratio for Tier 2 Evidence:**
LR_JSCC = 1.2 (for OBSERVER/PRAGMATIST vs ARCHITECT)
LR_ISDA = 1.0 (neutral)

**Posterior Calculation:**
The JSCC evidence slightly increases the probability of OBSERVER (infrastructure-connected) relative to PRAGMATIST (strategic vendor adoption).

Assigning:
- LR for OBSERVER: 1.3 (infrastructure connection is most consistent with passive observation)
- LR for PRAGMATIST: 1.1 (slightly less consistent than OBSERVER)
- LR for ARCHITECT: 0.8 (weakly inconsistent with ARCHITECT)

**Post-Tier 2 Posterior:**
- P(ARCHITECT) = **0.01 (1%)**
- P(PRAGMATIST) = **0.30 (30%)**
- P(OBSERVER) = **0.69 (69%)**

---

## Interpretation

Tier 2 evidence confirms that Nomura is not pursuing ARCHITECT strategy and provides weak support for OBSERVER classification. The JSCC clearing relationship is the only substantive finding, and it indicates infrastructure connectivity rather than strategic CDM adoption.

**Classification Emerging:** OBSERVER (CCP-Connected)

**Confidence:** MODERATE (45%)

**Rationale:**
- No direct CDM evidence (Tier 1 null results)
- Single indirect infrastructure connection (JSCC)
- No vendor partnerships, trade press coverage, or strategic signals
- Infrastructure connection is passive (required for clearing operations)

---

## Proceeding to Tier 3

**Key Questions for Tier 3:**
1. Are there hiring signals for CDM roles?
2. Do LinkedIn profiles indicate internal CDM expertise?
3. Are there any indirect technical signals (patents, blog posts, GitHub activity)?

**Expected Impact:**
Tier 3 signals will either:
1. Reveal hidden CDM capability building (would upgrade to PRAGMATIST)
2. Confirm absence of capability building (would strengthen OBSERVER classification)

Given the pattern of null results in Tiers 1-2, we expect Tier 3 to also show null results, which would increase confidence in OBSERVER classification to 55-60%.
