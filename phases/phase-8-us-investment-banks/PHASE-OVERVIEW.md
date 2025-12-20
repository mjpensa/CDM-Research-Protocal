# Phase 8: US Investment Banks

## Overview

Phase 8 assesses the five major US investment banks/universal banks for CDM adoption posture. This is a critical phase as JPMorgan is a **confirmed ARCHITECT** (production October 2024), establishing a US anchor point for comparison.

---

## Banks in Phase

| Bank | Execution Tier | Time Budget | Known Status |
|------|---------------|-------------|--------------|
| JPMorgan Chase | B (Deep Dive) | 3.0 hours | **ARCHITECT-Native (confirmed)** |
| Goldman Sachs | A (Full) | 4.5 hours | High potential ARCHITECT |
| Morgan Stanley | A (Full) | 4.5 hours | High potential ARCHITECT |
| Citigroup | B (Abbreviated) | 3.0 hours | Universal bank |
| Bank of America | B (Abbreviated) | 3.0 hours | Retail focus |

**Total Time Budget**: 18.0 hours

---

## Regulatory Context

### CFTC Rewrite
The Commodity Futures Trading Commission has been modernizing derivatives reporting requirements:
- **Part 43**: Real-time swap data reporting
- **Part 45**: Swap data recordkeeping and reporting
- **Part 46**: Swap data reporting (legacy swaps)
- Various effective dates throughout 2022-2024

US banks must address CFTC requirements, creating potential CDM adoption pressure similar to EMIR Refit in Europe.

### SEC Involvement
- Securities-based swaps regulated separately by SEC
- Additional reporting requirements for US G-SIBs

### Dodd-Frank Legacy
- US was early mover on derivatives reform post-2008
- Established derivatives reporting infrastructure before CDM existed
- Question: Are US banks modernizing to CDM or maintaining legacy systems?

---

## Phase Hypothesis

**Primary Hypothesis**: JPMorgan production creates peer pressure for other US derivatives dealers (Goldman Sachs, Morgan Stanley) to pursue ARCHITECT path.

**Alternative Hypothesis**: US derivatives infrastructure (DTCC) may provide CDM connectivity, allowing vendor-dependent path for non-JPMorgan banks.

---

## Prior Probability Framework

### JPMorgan Chase
- **P(ARCHITECT) = 90%** (confirmed production)
- Research focus: Scope and depth of production deployment

### Goldman Sachs
- **P(ARCHITECT) = 40%** (high derivatives relevance + JPMorgan peer pressure)
- Derivatives dominant business model
- Strong technology culture
- Research focus: Evidence of CDM investment or contribution

### Morgan Stanley
- **P(ARCHITECT) = 35%** (high derivatives relevance + JPMorgan peer pressure)
- Derivatives + wealth management hybrid
- Research focus: Evidence of CDM investment or contribution

### Citigroup
- **P(ARCHITECT) = 25%** (universal bank, JPMorgan peer pressure partially offset by broader business model)
- Global universal bank with significant derivatives
- Research focus: CDM vs vendor path decision

### Bank of America
- **P(ARCHITECT) = 20%** (retail focus reduces CDM priority)
- Retail-heavy universal bank
- Merrill Lynch integration considerations
- Research focus: CDM relevance given retail focus

---

## Key Research Questions

1. **JPMorgan Deep Dive**
   - What products/workflows are in CDM production?
   - Is JPMorgan contributing to CDM governance?
   - What was the timeline from pilot to production?

2. **Goldman Sachs / Morgan Stanley**
   - Are they building internal CDM capability?
   - ISDA/FINOS contribution evidence?
   - Pilot or production announcements?

3. **Citigroup / Bank of America**
   - Vendor vs build decision indicators?
   - CFTC Rewrite response strategy?

4. **Cross-Bank**
   - Is there a "US derivatives dealer cohort" behavior?
   - How does DTCC involvement affect bank strategies?

---

## Execution Order

1. **JPMorgan** (Deep Dive) - Establish US ARCHITECT benchmark
2. **Goldman Sachs** (Full) - Highest potential ARCHITECT after JPMorgan
3. **Morgan Stanley** (Full) - Second derivatives dealer assessment
4. **Citigroup** (Abbreviated) - Universal bank comparison
5. **Bank of America** (Abbreviated) - Retail-focused comparison

---

## Success Criteria

1. [ ] JPMorgan production scope documented
2. [ ] Goldman Sachs CDM posture determined (ARCHITECT vs PRAGMATIST)
3. [ ] Morgan Stanley CDM posture determined
4. [ ] US G-SIB cohort behavior pattern identified (or refuted)
5. [ ] CFTC Rewrite impact on CDM adoption assessed
6. [ ] DTCC role in US CDM ecosystem understood

---

## Output Structure

Each bank assessment follows standard protocol structure:
- `outputs/phase-8-us-investment-banks/{bank}/1-evidence/`
- `outputs/phase-8-us-investment-banks/{bank}/2-bayesian/`
- `outputs/phase-8-us-investment-banks/{bank}/3-gates/`
- `outputs/phase-8-us-investment-banks/{bank}/4-adversarial/`
- `outputs/phase-8-us-investment-banks/{bank}/5-synthesis/`

---

## Dependencies

- **JPMorgan anchor point** is already established in the protocol
- Phase 8 provides US benchmark for comparison with European banks
- Patterns discovered here inform Phase 9 (US Custody Banks)

---

*Phase 8: US Investment Banks*
*5 Banks | 18.0 Hours Total*
