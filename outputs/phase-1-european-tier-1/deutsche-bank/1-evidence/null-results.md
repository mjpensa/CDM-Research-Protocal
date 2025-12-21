# Null Results Registry: Deutsche Bank AG

**Bank:** Deutsche Bank AG
**Phase:** 1 - European Tier 1
**Date:** 2025-12-21

---

## Summary

| Metric | Value |
|--------|-------|
| Total Search Categories | 5 |
| Categories with Null Results | 5 |
| Informative Absences | 5 |

---

## Tier 1 Null Results

### ISDA CDM Contributor List

| Field | Value |
|-------|-------|
| Queries | `site:isda.org Deutsche Bank CDM`, `ISDA CDM contributors Deutsche Bank` |
| Results Reviewed | 10 |
| Null Type | NO_RESULTS |
| Informative Absence | Yes |

**Implication:** Deutsche Bank is not listed as an ISDA CDM contributor despite being a major G-SIB derivatives dealer.

---

### FINOS CDM Contributor

| Field | Value |
|-------|-------|
| Queries | `site:github.com/finos Deutsche Bank CDM`, `FINOS CDM Deutsche Bank contributor` |
| Results Reviewed | 10 |
| Null Type | NO_RESULTS |
| Informative Absence | Yes |

**Implication:** Deutsche Bank contributes to other FINOS projects (Fluxnova, Waltz, Spring Bot) but NOT to CDM - the "FINOS Paradox".

---

### Official CDM Announcements

| Field | Value |
|-------|-------|
| Queries | `site:db.com CDM`, `site:deutsche-bank.de common domain model` |
| Results Reviewed | 10 |
| Null Type | NO_RESULTS |
| Informative Absence | Yes |

**Implication:** No CDM announcements on official Deutsche Bank websites.

---

## Tier 2 Null Results

### Waters Technology Coverage

| Field | Value |
|-------|-------|
| Queries | `site:waterstechnology.com Deutsche Bank CDM` |
| Results Reviewed | 10 |
| Null Type | NO_RESULTS |
| Informative Absence | Partial |

**Implication:** No Waters Technology coverage of Deutsche Bank CDM initiatives.

---

## Tier 3 Null Results

### CDM Job Postings

| Field | Value |
|-------|-------|
| Queries | `Deutsche Bank CDM job`, `Deutsche Bank common domain model careers` |
| Results Reviewed | 10 |
| Null Type | NO_RESULTS |
| Informative Absence | Yes |

**Implication:** No CDM-specific hiring signals - suggests no active CDM build program.

---

### Production or Pilot Announcements

| Field | Value |
|-------|-------|
| Queries | `Deutsche Bank CDM production`, `Deutsche Bank CDM pilot 2024 2025` |
| Results Reviewed | 15 |
| Null Type | NO_RESULTS |
| Informative Absence | Yes |

**Implication:** Framework v20 claim of 'Pilot; production expected 2025' cannot be verified.

---

## Implications for Classification

The pattern of null results strongly supports **PRAGMATIST** classification:

| Signal Type | Expected if ARCHITECT | Found | Assessment |
|-------------|----------------------|-------|------------|
| ISDA/FINOS contribution | Yes | No | Informative absence |
| Official announcements | Yes | No | Informative absence |
| CDM job postings | Yes | No | Informative absence |
| Pilot/production news | Yes | No | Informative absence |
| Trade press coverage | Likely | No | Mild absence |

**Combined Null Result LR:** 0.808 (applied in Tier 3 Bayesian update)

---
