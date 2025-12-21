# Post-Tier 1 Bayesian Update - Standard Chartered

**Bank:** Standard Chartered
**Phase:** 6 (Deep Dive)
**Date:** 2025-12-21

---

## Prior Probability (Pre-Research)

**Starting Classification:** UNKNOWN
**Prior Probability:**
- ARCHITECT: 15% (base rate for Tier 1 banks)
- PRAGMATIST: 60% (most common classification)
- OBSERVER: 20%
- UNKNOWN: 5%

**Rationale:**
Standard Chartered is a large international bank with significant derivatives operations, particularly in Asia-Pacific markets. As a Tier 1 institution, there's a moderate prior probability of CDM adoption, but no specific evidence before research began.

---

## Tier 1 Evidence Summary

**Evidence Items Collected:** 4

1. **SC001** - DRR consortium participation (production_usage)
2. **SC002** - Rune-powered CDM production deployment (production_usage)
3. **SC004** - ISDA Board membership (membership_or_participation)
4. **SC005** - CDM working group participation (membership_or_participation)

---

## Likelihood Ratios

### Evidence: Production DRR Consortium (SC001)

**Likelihood Ratio Calculation:**

P(DRR consortium participation | ARCHITECT) = 0.90
- DRR development requires production-grade CDM capability
- Consortium participation indicates leadership commitment

P(DRR consortium participation | PRAGMATIST) = 0.15
- Pragmatists may observe but rarely join development consortia
- Requires significant resource commitment

P(DRR consortium participation | OBSERVER) = 0.02
- Observers don't typically contribute to development

**Likelihood Ratio:** 6.0 in favor of ARCHITECT

---

### Evidence: Rune Production Deployment (SC002)

**Likelihood Ratio Calculation:**

P(Rune production | ARCHITECT) = 0.85
- Rune is the CDM runtime - production usage indicates full adoption
- Strong technical signal

P(Rune production | PRAGMATIST) = 0.10
- Pragmatists might use CDM but typically via vendors, not native Rune

P(Rune production | OBSERVER) = 0.01
- Observers don't deploy production systems

**Likelihood Ratio:** 8.5 in favor of ARCHITECT

---

### Evidence: ISDA Board Membership (SC004)

**Likelihood Ratio Calculation:**

P(ISDA Board | ARCHITECT) = 0.70
- Board membership indicates strategic commitment
- Governance influence often precedes or accompanies implementation

P(ISDA Board | PRAGMATIST) = 0.30
- Some pragmatists serve on boards for market intelligence
- Board membership alone doesn't confirm implementation

P(ISDA Board | OBSERVER) = 0.15
- Observers can participate in governance

**Likelihood Ratio:** 2.3 in favor of ARCHITECT

---

### Evidence: Working Group Participation (SC005)

**Likelihood Ratio Calculation:**

P(Working groups | ARCHITECT) = 0.80
- Active technical participation typical of implementers
- Multiple workgroups suggests depth of engagement

P(Working groups | PRAGMATIST) = 0.40
- Pragmatists may participate for awareness

P(Working groups | OBSERVER) = 0.25
- Observers often join workgroups

**Likelihood Ratio:** 2.0 in favor of ARCHITECT

---

## Bayesian Update Calculation

**Combined Likelihood Ratio:**
LR_total = 6.0 × 8.5 × 2.3 × 2.0 = 234.6

**Posterior Odds:**
Prior odds (ARCHITECT) = 0.15 / (1 - 0.15) = 0.176
Posterior odds = 0.176 × 234.6 = 41.3

**Posterior Probability:**
P(ARCHITECT | Evidence) = 41.3 / (1 + 41.3) = 97.6%

---

## Confidence Calibration

**Raw Posterior:** 97.6%
**Calibrated Confidence:** 80%

**Calibration Factors:**

1. **Evidence Diversity (−5%):**
   - All evidence from ISDA sources
   - Limited independent corroboration
   - Reduction: 5%

2. **Temporal Uncertainty (−3%):**
   - Evidence ranges from 18-24 months old
   - No evidence from last 6 months
   - Reduction: 3%

3. **Absence of Open Source Activity (−5%):**
   - No GitHub contributions found
   - No FINOS participation
   - Suggests possible vendor dependency
   - Reduction: 5%

4. **Geographic Coverage Concern (−4.6%):**
   - Limited Western media coverage
   - May reflect reporting bias rather than implementation status
   - Reduction: 4.6%

**Final Calibrated Confidence:** 97.6% - 17.6% = 80%

---

## Classification After Tier 1

**Classification:** ARCHITECT (Leader)
**Confidence:** 80%

**Rationale:**
- Strong production usage signals (DRR consortium + Rune deployment)
- Governance-level commitment (ISDA Board)
- Technical engagement (working groups)
- Calibrated downward due to source concentration and temporal factors

**Justification for "Leader" Sub-Classification:**
- Consortium participation indicates industry leadership
- Board membership suggests strategic influence
- Not "Native" due to absence of open source contributions
- Not "Active" because evidence exceeds pilot/POC level

---

## Next Steps

**Proceed to Tier 2 Research:** Yes

**Focus Areas for Tier 2:**
1. Conference presentations by Standard Chartered staff
2. Trade press coverage of CDM implementation
3. Vendor partnerships that might explain absence of GitHub activity
4. Regional press (Asia-Pacific) for additional coverage

**Questions to Resolve:**
- Is the absence of GitHub activity due to vendor partnership or internal capability?
- Are there more recent (< 12 months) signals of continued CDM usage?
- How does Standard Chartered's implementation compare to peer banks?
