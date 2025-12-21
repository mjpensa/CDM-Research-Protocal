# Tier 1 Evidence: Deutsche Bank AG

**Bank:** Deutsche Bank AG
**Phase:** 1 - European Tier 1
**Date:** 2025-12-21

---

## Search Execution Summary

| Metric | Value |
|--------|-------|
| Date | 2025-12-21 |
| Evidence Items Found | 3 |
| Schema Version | 4.3 |
| Sources Searched | FINOS, Official Bank Website, Annual Reports, ISDA |

## Evidence Inventory

### DB-002: FINOS Contributor (Non-CDM)

| Field | Value |
|-------|-------|
| Source | [finos.org/common-domain-model](https://www.finos.org/common-domain-model) |
| Date | 2025-12-20 |
| Tier | 1 |
| Claim Type | open_source_contribution |
| Direction | NEUTRAL |
| LR | 0.8 |

**Claim:** Deutsche Bank is an active FINOS contributor to Fluxnova, Spring Bot, and Waltz projects - but NOT to the Common Domain Model

**Excerpt:** "Fluxnova is co-maintained by Fidelity, NatWest Group, Deutsche Bank, Capital One and BMO. Rob Moffat built Spring Bot while at Deutsche Bank. David Watkins from Deutsche Bank is Waltz Lead Maintainer."

**Analysis:** This is a critical "informative absence" finding. Deutsche Bank has demonstrated clear open-source capability and willingness to contribute to FINOS projects. Their absence from CDM contributions is therefore a revealed preference, not a capability limitation. This suggests CDM is not a strategic priority.

**Quality Assessment:**
- Authority: HIGH (official FINOS source)
- Recency: Current (verified 2025-12-20)
- Specificity: Specific (named individuals and projects)

**Caveats:** Deutsche Bank's non-participation in CDM could change. This evidence tells us about current priorities, not permanent strategy.

---

### DB-003: DTCC EMIR Reporting (Traditional Approach)

| Field | Value |
|-------|-------|
| Source | [db.com/legal-resources/european-market-infrastructure-regulation/transaction-reporting](https://www.db.com/legal-resources/european-market-infrastructure-regulation/transaction-reporting) |
| Date | 2024-04-29 |
| Tier | 1 |
| Claim Type | vendor_proxy_signal |
| Direction | SUPPORTS_PRAGMATIST |
| LR | 0.7 |

**Claim:** Deutsche Bank offers EMIR reporting service via DTCC Data Repository - traditional approach without CDM/DRR

**Excerpt:** "Deutsche Bank is offering a reporting service to the DTCC Data Repository (Ireland) Plc, an EU TR, to help NFC+ and FC clients comply with their EMIR reporting obligations."

**Analysis:** This confirms Deutsche Bank is using traditional infrastructure for EMIR compliance rather than a CDM-based approach. DTCC is a well-established utility provider, and this represents the "traditional" compliance path. No mention of CDM or DRR in their EMIR compliance documentation.

**Quality Assessment:**
- Authority: HIGH (official Deutsche Bank source)
- Recency: Current (EMIR Refit deadline was April 2024)
- Specificity: Specific (product scope: IRS, CDS, FX Forwards, FX Options)

**Caveats:** DTCC is building CDM capabilities. It's possible Deutsche Bank could transition to CDM through DTCC without public announcement.

---

### DB-005: Annual Report Silence on CDM

| Field | Value |
|-------|-------|
| Source | [investor-relations.db.com/files/documents/annual-reports/2024/Annual-Report-2023.pdf](https://investor-relations.db.com/files/documents/annual-reports/2024/Annual-Report-2023.pdf) |
| Date | 2024-03-14 |
| Tier | 1 |
| Claim Type | membership_or_participation |
| Direction | NEUTRAL |
| LR | 0.9 |

**Claim:** Deutsche Bank annual reports 2023-2024 mention investments in technology and regulatory compliance but no specific CDM/DRR references

**Excerpt:** "Work on their most important regulatory programmes is now nearing completion. Investments in technology, processes and controls will increasingly translate into savings."

**Analysis:** Deutsche Bank's annual reports discuss regulatory technology investment in general terms but make no mention of CDM, DRR, or ISDA standards adoption. For a G-SIB with significant derivatives operations, this absence is informative. If CDM were a major strategic initiative, it would likely warrant mention.

**Quality Assessment:**
- Authority: HIGH (official annual report to investors)
- Recency: Current (2023 annual report published March 2024)
- Specificity: Vague (generic regulatory investment language)

**Caveats:** Annual reports may not detail specific technology initiatives. Absence does not prove non-adoption, only that it's not a highlighted strategic priority.

---

## Combined Tier 1 Assessment

| Evidence ID | Direction | LR | Key Signal |
|-------------|-----------|-----|------------|
| DB-002 | NEUTRAL | 0.8 | FINOS paradox - capability without CDM focus |
| DB-003 | SUPPORTS_PRAGMATIST | 0.7 | Traditional DTCC approach |
| DB-005 | NEUTRAL | 0.9 | Annual report silence |

**Combined Tier 1 LR:** 0.8 x 0.7 x 0.9 = **0.504**

**Interpretation:** Tier 1 evidence shifts probability toward PRAGMATIST. The FINOS paradox (DB-002) is particularly informative - Deutsche Bank has demonstrated they CAN and DO contribute to open source, but choose NOT to contribute to CDM.

---
