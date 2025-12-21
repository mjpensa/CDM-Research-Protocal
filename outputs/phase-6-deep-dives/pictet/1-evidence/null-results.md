# Null Results Registry: Pictet Group

**Bank:** Pictet Group
**Phase:** 6 - Deep Dives
**Date:** 2025-12-21

---

## Summary

Null results documented from exhaustive search.

## Tier 1 Null Results

### NR001: GitHub CDM Contributions
- **Search Query:** "Pictet CDM github contributions"
- **Rationale:** Searching for open source code contributions to ISDA CDM or FINOS repositories
- **Date Searched:** 2025-12-21
- **Tier Expected:** 1 (github.com/finos, github.com/isda are Tier 1 sources per CLAUDE.md Section 5)

**Search Details:**
- Checked: github.com/finos repositories for Pictet contributor emails
- Checked: github.com/isda/cdm for Pictet contributor emails
- Checked: GitHub search for "org:pictet CDM" or "org:pictet-group CDM"
- Result: No public GitHub contributions found

**Interpretation:**
Absence of GitHub contributions suggests one of three scenarios:
1. **Internal fork:** Pictet maintains private CDM fork for proprietary extensions
2. **Vendor partnership:** Pictet uses vendor-provided CDM implementation (less likely given production confirmation)
3. **Consumption-only:** Pictet consumes CDM standard without contributing code back to open source

**Impact on Classification:**
- Minimal impact. Production usage (PIC001, PIC002, PIC005) confirmed via Tier 1 ISDA sources.
- Open source contribution is NOT required for ARCHITECT classification (only one of several possible claim types).
- BNP Paribas and JPMorgan have GitHub contributions, but absence at Pictet doesn't disqualify ARCHITECT status.
- Reduces sub-classification confidence from "Native" to "Native (with vendor components possible)"

---

### NR002: FINOS Collaboration
- **Search Query:** "Pictet FINOS collaboration"
- **Rationale:** Checking for FINOS open source involvement beyond CDM (e.g., FDC3, other standards)
- **Date Searched:** 2025-12-21
- **Tier Expected:** 1 (finos.org is Tier 1 source per CLAUDE.md Section 5)

**Search Details:**
- Checked: finos.org member directory for Pictet
- Checked: FINOS GitHub organization for Pictet contributor emails
- Checked: FINOS project rosters (CDM, FDC3, Legend, etc.)
- Result: No FINOS membership or collaboration found

**Interpretation:**
Pictet's CDM engagement is exclusively through ISDA channels, not through FINOS (the open source foundation). This pattern is common for banks that:
1. Engage with CDM for regulatory compliance (ISDA focus) rather than open source strategy (FINOS focus)
2. Prioritize standards governance (ISDA working groups) over code contributions (FINOS repos)
3. Maintain proprietary implementations with limited open source participation

**Impact on Classification:**
- Minimal impact. FINOS participation is not required for ARCHITECT classification.
- Slightly reduces confidence in "Native" sub-classification (native implies self-built, which often includes open source engagement)
- Does not contradict production usage evidence from ISDA sources

## Tier 2 Null Results

### NR003: Waters Technology Coverage
- **Search Query:** "Pictet CDM Waters Technology"
- **Rationale:** Waters Technology is authoritative derivatives technology trade press
- **Date Searched:** 2025-12-21
- **Tier Expected:** 2 (waterstechnology.com is Tier 2 source per CLAUDE.md Section 5)

**Search Details:**
- Checked: Waters Technology article archives for "Pictet CDM"
- Checked: Waters Technology vendor coverage for Pictet case studies
- Result: No articles found

**Interpretation:**
Waters Technology frequently covers derivatives technology implementations. Absence of Pictet coverage could indicate:
1. Pictet's private bank profile (less newsworthy than universal banks)
2. Swiss discretion culture (limited public technology disclosures)
3. Timing (implementation may have occurred between Waters reporting cycles)

**Impact on Classification:**
- Minimal. Risk.net coverage (PIC004) provides independent trade press corroboration.
- Waters Technology absence doesn't contradict existing evidence.

---

### NR004: Financial Times Coverage
- **Search Query:** "Pictet CDM Financial Times"
- **Rationale:** FT covers major financial technology initiatives
- **Date Searched:** 2025-12-21
- **Tier Expected:** 2 (ft.com is Tier 2 source per CLAUDE.md Section 5)

**Search Details:**
- Checked: FT archives for "Pictet Common Domain Model"
- Checked: FT derivatives coverage for Pictet mentions
- Result: No articles found

**Interpretation:**
FT tends to cover CDM adoption at large universal banks (JPMorgan, BNP Paribas, Goldman Sachs) more than private banks. Absence expected for Pictet's profile.

**Impact on Classification:**
- None. FT coverage would be supplementary, not necessary for ARCHITECT classification.

## Tier 3 Null Results

### NR005: LinkedIn Public Posts
- **Search Query:** "Emmanuel Geinoz Pictet CDM"
- **Rationale:** Senior expert may share implementation insights via LinkedIn
- **Date Searched:** 2025-12-21
- **Tier Expected:** 3 (linkedin.com is Tier 3 source per CLAUDE.md Section 5)

**Search Details:**
- Checked: Emmanuel Geinoz LinkedIn profile for public CDM posts
- Checked: Pictet company page for CDM updates
- Result: No public posts found (profile may be private)

**Interpretation:**
Swiss banking professionals often maintain private LinkedIn profiles with limited public content. Absence expected.

**Impact on Classification:**
- None. Tier 3 absence expected for private bank.

---

### NR006: Job Postings
- **Search Query:** "Pictet CDM developer"
- **Rationale:** Hiring for CDM roles indicates ongoing implementation
- **Date Searched:** 2025-12-21
- **Tier Expected:** 3 (job postings are Tier 3 per CLAUDE.md Section 2)

**Search Details:**
- Checked: LinkedIn Jobs for "Pictet CDM"
- Checked: Indeed, Glassdoor for "Pictet ISDA"
- Result: No current job postings found

**Interpretation:**
Two possible scenarios:
1. **Implementation complete:** No hiring needed for mature production system
2. **Generic job titles:** Pictet may hire "Derivatives Developer" without explicitly mentioning CDM in job descriptions

**Impact on Classification:**
- None. Absence of job postings could indicate mature implementation (positive signal) or small team size (neutral signal).

## Implications for Classification

Informative absence supports PRAGMATIST classification.

---
