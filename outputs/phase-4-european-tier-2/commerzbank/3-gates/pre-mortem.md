# Pre-Mortem Analysis: Commerzbank AG

**Bank:** Commerzbank AG
**Phase:** 4 - Other European
**Date:** 2025-12-21

---

## Research Objective

Assess Commerzbank AG's CDM/DRR adoption maturity.

## Potential Failure Modes

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

## Search Strategy

### Tier 1 (Official Sources)
- Bank official website, annual reports
- ISDA.org, FINOS.org
- Regulatory filings

### Tier 2 (Industry Sources)
- Risk.net, Waters Technology
- Trade press coverage
- Vendor announcements

### Tier 3 (Signal Sources)
- Job postings
- LinkedIn profiles
- Conference presentations

## Key Hypotheses to Test

N/A

## Decision Points

1. After Tier 1: If P(ARCHITECT) < 20% or > 80%, consider early classification
2. After Tier 2: Assess if Tier 3 signals will add value
3. After Tier 3: Proceed to adversarial challenge

## Null Hypothesis Reminder

Assume Commerzbank AG is PRAGMATIST until evidence proves otherwise.

---
