# Assessment: Citigroup Inc.

**Bank**: Citigroup Inc.
**Date**: 2025-12-19
**Protocol**: Tier B (Abbreviated)
**Phase**: 8 - US Investment Banks

---

## Bank Profile

| Attribute | Value |
|-----------|-------|
| Headquarters | New York, USA |
| Business Model | Global universal bank |
| Derivatives Relevance | High |
| Primary Regulator | OCC/Federal Reserve/SEC/CFTC |
| G-SIB Status | Yes |
| Strategic Context | Ongoing simplification/restructuring |

---

## Prior Probability

**P(ARCHITECT) = 25%**

Adjustments:
- +10% for significant derivatives business
- +5% for JPMorgan peer pressure
- -5% for strategic restructuring (competing priorities)
- -5% for universal bank complexity
- Base 25%

**P(PRAGMATIST) = 75%**

---

## Evidence Summary

Citigroup is a global universal bank undergoing strategic simplification. Key observations:

1. **No CDM production announcement** - No public CDM initiative
2. **Restructuring priority** - Simplification consuming technology capacity
3. **Markets business significant** - But part of broader universal bank
4. **CFTC compliance focus** - Regulatory requirements apply

---

## Evidence Blocks

### [CITI-001] TIER 4 - SUPPORTS PRAGMATIST (No CDM Announcement)
**Finding**: Citigroup has not announced CDM production or pilot. Universal bank model suggests vendor path more likely.
**Source**: Absence of announcement
**Confidence**: MEDIUM
**Implication**: Not pursuing internal CDM build

### [CITI-002] TIER 2 - SUPPORTS PRAGMATIST (Restructuring Priority)
**Finding**: Citigroup's strategic simplification (exit from consumer banking in multiple markets, management changes) consumes technology and management capacity. CDM investment unlikely during restructuring.
**Source**: Public announcements, earnings calls
**Confidence**: HIGH
**Implication**: Competing priorities reduce CDM probability

### [CITI-003] TIER 4 - SUPPORTS PRAGMATIST (Universal Bank Model)
**Finding**: Universal banks historically favor vendor solutions for derivatives technology rather than proprietary builds. Citigroup's broader business model suggests similar pattern.
**Source**: Industry analysis, peer comparisons (Deutsche Bank, HSBC)
**Confidence**: MEDIUM
**Implication**: Business model predicts vendor path

---

## Bayesian Update

### Prior
- P(Architect) = 25%
- P(Pragmatist) = 75%
- Prior Odds = 0.33

### Evidence Assessment
| Evidence | Likelihood Ratio | Direction |
|----------|-----------------|-----------|
| No CDM announcement | 0.3:1 | Supports PRAGMATIST |
| Restructuring priority | 0.4:1 | Supports PRAGMATIST |
| Universal bank model | 0.6:1 | Supports PRAGMATIST |

### Combined Likelihood Ratio
LR = 0.3 × 0.4 × 0.6 = 0.072

### Posterior Calculation
Posterior Odds = 0.33 × 0.072 = 0.024
**P(Architect | Evidence) = 2%**
**P(Pragmatist | Evidence) = 98%**

---

## Single Adversarial Question

**Question**: Does Citigroup's significant markets business justify CDM investment despite restructuring?

**Answer**: No. Restructuring priority is clear strategic direction. Markets business will address CFTC requirements through vendor solutions rather than internal CDM build. Classification is high confidence PRAGMATIST.

**Verdict**: **PRAGMATIST** - Restructuring + universal bank model

---

## Final Classification

| Classification | Probability | Confidence |
|---------------|-------------|------------|
| **PRAGMATIST** | 98% | 85% |
| Architect | 2% | - |

**Sub-classification**: Vendor-Dependent

---

## Key Findings

1. **No CDM announcement** - Expected for PRAGMATIST
2. **Restructuring priority** - Clear competing strategic focus
3. **Universal bank model** - Predicts vendor path (like Deutsche Bank, HSBC)
4. **High confidence classification** - Multiple confirming signals

---

*Assessment Complete*
*Protocol: Tier B (Abbreviated)*
*Classification: PRAGMATIST (98%, 85% confidence)*
