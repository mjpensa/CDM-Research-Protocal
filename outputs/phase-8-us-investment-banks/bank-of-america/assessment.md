# Assessment: Bank of America Corporation

**Bank**: Bank of America Corporation
**Date**: 2025-12-19
**Protocol**: Tier B (Abbreviated)
**Phase**: 8 - US Investment Banks

---

## Bank Profile

| Attribute | Value |
|-----------|-------|
| Headquarters | Charlotte, USA |
| Business Model | Global universal bank with retail focus |
| Derivatives Relevance | High |
| Primary Regulator | OCC/Federal Reserve/SEC/CFTC |
| G-SIB Status | Yes |
| Business Focus | Retail and commercial banking primary |

---

## Prior Probability

**P(ARCHITECT) = 20%**

Adjustments:
- -10% for retail focus
- +5% for JPMorgan peer pressure
- +5% for Merrill Lynch trading capability
- Base 25%

**P(PRAGMATIST) = 80%**

---

## Evidence Summary

Bank of America is primarily a retail and commercial bank. Merrill Lynch provides investment banking but doesn't dominate business mix. Key observations:

1. **No CDM production announcement** - No public CDM initiative
2. **Retail banking primary focus** - Technology investment prioritizes consumer
3. **Merrill Lynch trading** - Derivatives capability exists but secondary
4. **Charlotte headquarters** - Different culture than NYC investment banks

---

## Evidence Blocks

### [BOFA-001] TIER 4 - SUPPORTS PRAGMATIST (No CDM Announcement)
**Finding**: Bank of America has not announced CDM production or pilot. Retail focus suggests CDM not technology priority.
**Source**: Absence of announcement
**Confidence**: MEDIUM
**Implication**: Not pursuing internal CDM build

### [BOFA-002] TIER 2 - STRONGLY SUPPORTS PRAGMATIST (Retail Focus)
**Finding**: Bank of America's strategic emphasis is retail and commercial banking. Technology investments prioritize consumer digital banking, mobile apps, and commercial services. Derivatives technology is secondary.
**Source**: Public strategy, earnings calls, technology announcements
**Confidence**: HIGH
**Implication**: Business model makes CDM low priority

### [BOFA-003] TIER 3 - WEAKLY SUPPORTS ARCHITECT (Merrill Lynch Trading)
**Finding**: Merrill Lynch provides significant trading capability including derivatives. This creates some CDM relevance but doesn't override retail focus.
**Source**: Business mix analysis
**Confidence**: MEDIUM
**Implication**: Merrill provides CDM relevance but not priority

---

## Bayesian Update

### Prior
- P(Architect) = 20%
- P(Pragmatist) = 80%
- Prior Odds = 0.25

### Evidence Assessment
| Evidence | Likelihood Ratio | Direction |
|----------|-----------------|-----------|
| No CDM announcement | 0.3:1 | Supports PRAGMATIST |
| Retail focus | 0.3:1 | Strongly supports PRAGMATIST |
| Merrill Lynch trading | 1.2:1 | Weakly supports ARCHITECT |

### Combined Likelihood Ratio
LR = 0.3 × 0.3 × 1.2 = 0.108

### Posterior Calculation
Posterior Odds = 0.25 × 0.108 = 0.027
**P(Architect | Evidence) = 3%**
**P(Pragmatist | Evidence) = 97%**

---

## Single Adversarial Question

**Question**: Does Merrill Lynch's derivatives business justify CDM investment despite Bank of America's retail focus?

**Answer**: No. Merrill Lynch derivatives business is significant but not dominant in Bank of America's overall strategy. Consumer banking technology receives priority investment. CDM will likely be addressed through vendor solutions for CFTC compliance.

**Verdict**: **PRAGMATIST** - Retail focus + no CDM signals

---

## Final Classification

| Classification | Probability | Confidence |
|---------------|-------------|------------|
| **PRAGMATIST** | 97% | 85% |
| Architect | 3% | - |

**Sub-classification**: Vendor-Dependent

---

## Key Findings

1. **No CDM announcement** - Expected for retail-focused bank
2. **Retail banking priority** - Clear strategic focus
3. **Merrill Lynch secondary** - Trading capability doesn't override retail focus
4. **Similar to Lloyds pattern** - Retail-focused universal banks = PRAGMATIST
5. **High confidence classification** - Business model provides clear signal

---

## Comparison to UK Retail Banks

| Bank | Region | Retail Focus | Classification | Confidence |
|------|--------|--------------|----------------|------------|
| Bank of America | USA | Primary | PRAGMATIST | 85% |
| Lloyds | UK | Primary | PRAGMATIST | 85% |
| NatWest | UK | Primary | PRAGMATIST | 80% |

Retail-focused universal banks consistently classify as PRAGMATIST regardless of region.

---

*Assessment Complete*
*Protocol: Tier B (Abbreviated)*
*Classification: PRAGMATIST (97%, 85% confidence)*
