# Pre-Mortem Analysis - Standard Chartered

**Bank:** Standard Chartered
**Phase:** 6 (Deep Dive)
**Date:** 2025-12-21

---

## Exercise Premise

*"It is now March 2026. Our research concluded that Standard Chartered is an ARCHITECT (Leader) at 80% confidence. However, new evidence has emerged proving this classification was WRONG. What went wrong?"*

---

## Failure Scenario 1: Vendor Dependency Misclassified as Native Capability

**What Happened:**
Standard Chartered's "production CDM usage" was actually a vendor-managed solution (e.g., Regnosys, Bloomberg, or ISDA tech vendor). The bank lacked internal CDM expertise and was effectively a PRAGMATIST relying on outsourced implementation.

**How We Missed It:**
- We took ISDA announcements at face value without investigating vendor involvement
- Absence of GitHub contributions should have been a stronger red flag
- Conference presentations could have been describing vendor-led implementations
- DRR consortium participation may have been governance-level, not technical

**Warning Signs We Ignored:**
- No open source contributions (SC negative search)
- All evidence from ISDA sources (potential reporting bias)
- No independent trade press validation
- No specific technical details in evidence excerpts

**Probability:** 25%

**Mitigation:**
- Search for vendor announcements mentioning Standard Chartered
- Investigate partnership disclosures in annual reports
- Seek independent corroboration from non-ISDA sources

---

## Failure Scenario 2: Pilot/POC Misclassified as Production

**What Happened:**
What we interpreted as "production usage" was actually a limited pilot or proof-of-concept that never scaled. Standard Chartered participated in DRR consortium development but didn't deploy CDM in production trading systems.

**How We Missed It:**
- ISDA language was aspirational ("supporting development") not confirmatory ("in production")
- We assumed consortium participation implied production deployment
- No evidence of scale, transaction volumes, or business impact
- Rune "deployment" may have been sandbox/testing only

**Warning Signs We Ignored:**
- Evidence from 2023-2024 with no recent updates (possible stalled project)
- Vague language in ISDA announcements (no specific metrics)
- No case study or detailed implementation description
- Absence of regulatory filing mentions (suggests non-material impact)

**Probability:** 15%

**Mitigation:**
- Search for "Standard Chartered CDM production scale volumes"
- Look for evidence of ongoing usage post-2024
- Seek specific use case descriptions beyond generic "derivatives processing"

---

## Failure Scenario 3: Asia-Pacific Regional Divergence

**What Happened:**
Standard Chartered's European operations adopted CDM for EMIR Refit compliance, but Asia-Pacific operations (majority of business) did not. We over-generalized limited regional adoption to bank-wide classification.

**How We Missed It:**
- We didn't distinguish between regional implementations
- ISDA participation driven by European regulatory requirements
- Asia-Pacific has different regulatory landscape (no EMIR equivalent)
- Evidence sources were Europe-focused

**Warning Signs We Ignored:**
- Limited Asia-Pacific press coverage (not just reporting bias)
- No evidence of MAS (Singapore) or HKMA (Hong Kong) regulatory filings
- Standard Chartered's business weighted toward Asia where CDM less relevant

**Probability:** 20%

**Mitigation:**
- Search for region-specific CDM evidence
- Check MAS/HKMA regulatory announcements
- Investigate whether DRR consortium is EU-only initiative

---

## Failure Scenario 4: Discontinued Implementation

**What Happened:**
Standard Chartered did implement CDM in 2023-2024 but discontinued the initiative due to cost, complexity, or strategic shift. We're looking at historical evidence of a program that no longer exists.

**How We Missed It:**
- No evidence from last 12 months (all 18-24 months old)
- We assumed continuity without verification
- No negative press coverage (because discontinued quietly)
- Staff may have moved on (would explain absence of recent LinkedIn activity)

**Warning Signs We Ignored:**
- **All evidence >12 months old** (significant red flag)
- No 2025 ISDA event participation found
- No recent job postings (could indicate completed or cancelled program)
- Dr. Milan Dragaš presentation in May 2024 (8 months ago, no followup)

**Probability:** 15%

**Mitigation:**
- Search for Standard Chartered staff changes (LinkedIn departures)
- Look for 2025 ISDA participation
- Check if Emmanuel Ramambason still on ISDA Board
- Search for "Standard Chartered CDM 2025" explicitly

---

## Failure Scenario 5: Governance Engagement Without Implementation

**What Happened:**
Standard Chartered participated in ISDA governance and DRR development as strategic intelligence gathering, not because they were implementing CDM. Board membership and working group participation were about influencing standards, not adopting them.

**How We Missed It:**
- We conflated governance participation with technical implementation
- Assumed DRR consortium membership required production usage
- Didn't distinguish between advisory roles and implementation roles

**Warning Signs We Ignored:**
- Board membership (SC004) is governance, not technical
- Working group participation (SC005) could be observational
- No evidence of actual code commits or technical artifacts
- Senior analytics leader presenting could be thought leadership, not implementation case study

**Probability:** 10%

**Mitigation:**
- Re-read evidence for specific technical details vs. generic participation
- Distinguish between "contributing to development" and "using in production"
- Verify if Rune deployment claim (SC002) has technical substance

---

## Composite Risk Assessment

**Highest Risk Failure Mode:** Vendor Dependency (25%)

**Combined Probability of Misclassification:** ~60%
- (Calculated as: 1 - [(1-0.25) × (1-0.15) × (1-0.20) × (1-0.15) × (1-0.10)] = 59.5%)

**Interpretation:**
There's a ~60% chance one of these failure modes applies, which aligns with our 80% confidence (implying 20% error rate from random factors + 60% from systematic errors = need for caution).

---

## Mitigation Strategy

**Before Finalizing Classification:**

1. **Vendor Verification Search:**
   - "Standard Chartered Regnosys partnership CDM"
   - "Standard Chartered Bloomberg CDM implementation"
   - Check vendor case study pages for Standard Chartered mentions

2. **Production Confirmation Search:**
   - "Standard Chartered CDM production volumes"
   - "Standard Chartered CDM live trading"
   - Look for specific use cases beyond generic "derivatives processing"

3. **Recency Verification:**
   - "Standard Chartered CDM 2025"
   - Check 2025 ISDA event speaker lists
   - Verify Emmanuel Ramambason still on ISDA Board

4. **Regional Scope Verification:**
   - "Standard Chartered CDM Asia Pacific"
   - Check MAS/HKMA regulatory announcements
   - Distinguish European vs. global rollout

**If mitigations reveal concerns:** Downgrade to PRAGMATIST or reduce confidence to 60-65%.

---

## Adversarial Questions for Synthesis

1. What specific evidence proves production usage beyond pilot/POC?
2. Is the absence of vendor announcements evidence of native capability or evidence gap?
3. Why is all our evidence 12-24 months old with nothing recent?
4. Could Standard Chartered be classified as OBSERVER with unusually high governance engagement?
5. Are we over-indexing on ISDA sources and under-indexing on absence of independent verification?

---

## Conclusion

**Pre-Mortem Verdict:** Proceed with caution.

**Recommended Actions:**
1. Execute mitigation searches before finalizing
2. Re-examine evidence excerpts for specificity vs. vagueness
3. Consider confidence reduction to 70-75% if mitigations fail
4. Flag temporal staleness (no 2025 evidence) as key risk factor

**Gate Status:** PROCEED TO TIER 1 with heightened scrutiny on production vs. pilot distinction.
