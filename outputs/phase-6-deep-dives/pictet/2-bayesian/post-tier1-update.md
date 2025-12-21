# Post-Tier 1 Bayesian Update - Pictet Group

**Bank:** Pictet Group
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
Pictet is a Swiss private banking group with significant wealth management and derivatives operations. As a Tier 1 institution with European regulatory exposure (EMIR Refit), there's a moderate prior probability of CDM adoption. However, private banks typically have lower CDM adoption rates than universal banks due to smaller derivatives desks.

---

## Tier 1 Evidence Summary

**Evidence Items Collected:** 4

1. **PIC001** - CDM and DRR production deployment confirmed (production_usage)
2. **PIC002** - DRR development consortium participation (production_usage)
3. **PIC005** - CDM for EMIR Refit compliance automation (production_usage)
4. **PIC006** - ISDA CDM working group participation (membership_or_participation)

---

## Likelihood Ratios

### Evidence: Production DRR Deployment (PIC001)

**Likelihood Ratio Calculation:**

P(Production DRR deployment | ARCHITECT) = 0.95
- Explicit ISDA confirmation: "Pictet Group has successfully deployed CDM and Digital Regulatory Reporting in production"
- "Successfully deployed" indicates completed implementation, not pilot
- Production environment specified explicitly

P(Production DRR deployment | PRAGMATIST) = 0.10
- Pragmatists may use DRR but typically via vendors, not direct deployment
- "Successfully deployed" suggests hands-on implementation

P(Production DRR deployment | OBSERVER) = 0.01
- Observers don't deploy production systems

**Likelihood Ratio:** 9.5 in favor of ARCHITECT

---

### Evidence: DRR Development Consortium (PIC002)

**Likelihood Ratio Calculation:**

P(DRR consortium | ARCHITECT) = 0.90
- "Core consortium" language indicates leadership role
- "Developing and implementing" suggests both governance and technical engagement
- Named alongside BNP Paribas, JPMorgan, Standard Chartered (confirmed ARCHITECTs)

P(DRR consortium | PRAGMATIST) = 0.15
- Pragmatists may observe consortia but rarely join development leadership
- Requires significant technical resource commitment

P(DRR consortium | OBSERVER) = 0.02
- Observers don't typically contribute to development consortia

**Likelihood Ratio:** 6.0 in favor of ARCHITECT

---

### Evidence: EMIR Refit CDM Automation (PIC005)

**Likelihood Ratio Calculation:**

P(EMIR Refit automation | ARCHITECT) = 0.85
- Specific use case (EMIR Refit compliance) confirms real-world production application
- "Deployed CDM-based automation" indicates active system integration
- Regulatory compliance focus suggests mission-critical usage

P(EMIR Refit automation | PRAGMATIST) = 0.25
- Pragmatists might automate EMIR Refit via vendor solutions
- Could be vendor-provided automation rather than native build

P(EMIR Refit automation | OBSERVER) = 0.02
- Observers don't deploy automation systems

**Likelihood Ratio:** 3.4 in favor of ARCHITECT

---

### Evidence: Working Group Participation (PIC006)

**Likelihood Ratio Calculation:**

P(Working groups | ARCHITECT) = 0.80
- "Active membership" suggests ongoing engagement
- "Focused on derivatives standardization" indicates technical participation
- Recent date (June 2024) shows sustained commitment

P(Working groups | PRAGMATIST) = 0.40
- Pragmatists may participate for awareness and influence

P(Working groups | OBSERVER) = 0.30
- Observers commonly join working groups

**Likelihood Ratio:** 2.0 in favor of ARCHITECT

---

## Bayesian Update Calculation

**Combined Likelihood Ratio:**
LR_total = 9.5 × 6.0 × 3.4 × 2.0 = 387.6

**Posterior Odds:**
Prior odds (ARCHITECT) = 0.15 / (1 - 0.15) = 0.176
Posterior odds = 0.176 × 387.6 = 68.2

**Posterior Probability:**
P(ARCHITECT | Evidence) = 68.2 / (1 + 68.2) = 98.6%

---

## Confidence Calibration

**Raw Posterior:** 98.6%
**Calibrated Confidence:** 90%

**Calibration Factors:**

1. **Evidence Diversity (−3%):**
   - All Tier 1 evidence from ISDA sources
   - No regulatory filing corroboration (SEC, FCA, BaFin)
   - Limited independent verification at Tier 1
   - Reduction: 3%

2. **Temporal Uncertainty (−2%):**
   - Evidence ranges from 6-25 months old
   - Most recent: PIC006 (June 2024, 18 months = borderline Recent/Dated)
   - Oldest: PIC001, PIC002 (Nov 2023, 25 months = Dated)
   - Better than Standard Chartered (all >18 months) but not optimal
   - Reduction: 2%

3. **Absence of Open Source Activity (−2%):**
   - No GitHub contributions found (NR001)
   - No FINOS participation found (NR002)
   - Suggests possible vendor components or internal fork
   - Less concerning than Standard Chartered (due to private bank profile)
   - Reduction: 2%

4. **Swiss Discretion Discount (−1.6%):**
   - Swiss private banks have limited public technology disclosures
   - Expected reporting bias (undercounting evidence)
   - May have additional unreported production usage
   - Modest reduction due to cultural factor
   - Reduction: 1.6%

**Final Calibrated Confidence:** 98.6% - 8.6% = 90%

---

## Classification After Tier 1

**Classification:** ARCHITECT (Native)
**Confidence:** 90%

**Rationale:**
- Multiple explicit production usage confirmations (PIC001, PIC002, PIC005)
- Consortium participation alongside confirmed ARCHITECT banks
- Specific use case documented (EMIR Refit automation)
- Recent working group participation (continuity signal)
- Stronger than Standard Chartered due to more explicit production language

**Justification for "Native" Sub-Classification:**
- "Successfully deployed" language suggests internal capability
- DRR development consortium role indicates technical depth
- EMIR Refit automation suggests integration with core systems
- However, absence of GitHub activity creates minor uncertainty
- "Native (with possible vendor components)" is most accurate characterization

---

## Comparison to Standard Chartered

**Standard Chartered Post-Tier 1:** 80% ARCHITECT
**Pictet Post-Tier 1:** 90% ARCHITECT

**Why Pictet Scores Higher (+10%):**
1. **More explicit production language:** "Successfully deployed" vs. "developing with production implementation"
2. **Specific use case documented:** EMIR Refit automation (PIC005) vs. generic Rune deployment
3. **More recent evidence:** PIC006 at 18 months vs. all StanChart evidence >18 months
4. **Stronger consortium language:** "Core consortium" vs. participation mention
5. **Lower source diversity penalty:** Swiss discretion expected vs. global bank should have more sources

---

## Next Steps

**Proceed to Tier 2 Research:** Yes

**Focus Areas for Tier 2:**
1. Trade press coverage (Risk.net, Waters Technology, FT)
2. Conference presentations by Emmanuel Geinoz or Pictet derivatives team
3. Independent corroboration of early adopter status
4. Peer comparisons (vs. BNP Paribas, JPMorgan, Standard Chartered)

**Questions to Resolve:**
1. Is there independent (non-ISDA) confirmation of production status?
2. How does Pictet's implementation timeline compare to other early adopters?
3. Are there more recent (<12 months) signals of continued CDM usage?
4. What is the scope of deployment (Europe only vs. global)?
5. Is the absence of GitHub activity due to vendor partnership or internal development?

---

## Preliminary Verdict

**After Tier 1:** Pictet demonstrates strong ARCHITECT characteristics with 90% confidence. Production usage is well-established through multiple Tier 1 sources. Tier 2 research should focus on:
- Independent corroboration (reducing ISDA source concentration)
- Recent evidence (addressing temporal staleness)
- Scope clarification (geographic and business unit coverage)

**Expected Tier 2 Impact:** Likely to maintain or slightly increase confidence (90-95% range) if independent corroboration found. Unlikely to decrease unless contradictory evidence emerges.
