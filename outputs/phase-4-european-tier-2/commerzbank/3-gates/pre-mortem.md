# Pre-Mortem: Commerzbank AG

**Bank:** Commerzbank AG
**Phase:** 4 - European Tier 2
**Date:** 2025-12-20

---

## Research Question

What is Commerzbank's CDM adoption maturity level?

## Pre-Mortem Scenario

"Six months from now, we discover our Commerzbank assessment was completely wrong. What happened?"

## Failure Modes

### 1. Hidden CDM Adoption Behind Murex

**Probability:** 25%

**Scenario:** Commerzbank is actually using Murex's CDM capabilities but:
- Murex press release didn't emphasize CDM aspect
- CDM implementation is internal/confidential
- Bank requested low-profile rollout

**Mitigation:**
- Search for Murex CDM case studies mentioning Commerzbank
- Check Commerzbank regulatory filings for CDM references
- Monitor ISDA working group participation

### 2. CDM Pilot Parallel to Murex Migration

**Probability:** 15%

**Scenario:** Commerzbank is running a separate CDM pilot for regulatory reporting while using Murex MX.3 for trading platform.

**Mitigation:**
- Search for DRR/EMIR Refit initiatives at Commerzbank
- Check for CDM regulatory reporting partnerships
- Look for job postings mentioning CDM

### 3. Missed ISDA/FINOS Participation

**Probability:** 10%

**Scenario:** Commerzbank has representatives in CDM working groups but under different names or roles.

**Mitigation:**
- Cross-reference ISDA member lists with Commerzbank LinkedIn employees
- Check conference speaker lists
- Review FINOS contributor commits for Commerzbank domains

### 4. Future CDM Plans Not Yet Public

**Probability:** 20%

**Scenario:** Commerzbank has CDM adoption plans for 2025-2026 but hasn't announced yet.

**Mitigation:**
- This is acceptable uncertainty - classification reflects current state
- Recommend re-assessment in 12 months
- Monitor for announcements

### 5. False Confidence in Null Results

**Probability:** 5%

**Scenario:** Evidence exists but wasn't found due to:
- Paywall blocking access
- German-language sources not searched
- Internal communications not public

**Mitigation:**
- Note knowledge gaps explicitly
- Flag German-language search limitation
- Document confidence bounds clearly

## Null Hypothesis Defense

**Assumption:** Commerzbank is PRAGMATIST (Vendor-Dependent)

**Evidence Supporting:**
- Murex MX.3 migration (traditional platform)
- No FINOS membership
- No ISDA CDM working group participation
- No CDM-related announcements

**Evidence Needed to Overturn:**
- Tier 1: Official CDM adoption announcement
- Tier 1: FINOS membership or contribution
- Tier 1: ISDA working group participation
- Tier 2: Trade press coverage of CDM initiative

## Confidence Calibration

Given the pre-mortem analysis:
- **Base Confidence:** 50% (Tier 2 maximum)
- **Adjustment:** -5% for hidden CDM possibility
- **Final Confidence:** 45-50% range

**Recommendation:** Classify as PRAGMATIST (Vendor-Dependent) at 50% confidence, noting possible hidden CDM usage as caveat.
