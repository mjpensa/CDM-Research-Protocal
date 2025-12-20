# Pre-Mortem Analysis: Lloyds Banking Group PLC
## Tier B Protocol (Abbreviated - 2 Failure Modes)

**Date**: 2025-12-19
**Prior Probability**: P(Architect) = 20%
**Derivatives Relevance**: Medium (UK-focused retail/commercial)

---

## Failure Mode 1: False Positive - Mistaking Vendor Adoption for CDM Architecture

### Scenario
Research incorrectly classifies Lloyds as CDM Architect based on:
- Vendor platform adoption (e.g., Murex, Calypso, Bloomberg) that happens to support CDM
- EMIR Refit compliance work that uses CDM-enabled reporting tools
- References to "digital transformation" or "standardization" without CDM specificity

### Why This Could Happen
- Lloyds has significant retail banking focus with limited derivatives trading desk
- UK EMIR Refit (Sept 2024) mandates may force CDM-adjacent tooling via vendors
- Vendor marketing materials may overstate client CDM involvement
- Bank's public communications focus on retail digital transformation, not wholesale derivatives

### Mitigation Strategy
- Distinguish between vendor-provided CDM capability and bank-architected CDM infrastructure
- Look for direct ISDA/CDM working group participation evidence
- Seek internal implementation evidence (job postings, technical papers, conference talks)
- Verify if CDM references are from Lloyds or their technology vendors

### Probability Assessment
- **High risk** given Lloyds' retail focus and medium derivatives relevance
- Likelihood of false positive: 35%

---

## Failure Mode 2: False Negative - Missing CDM Work Through UK Finance Consortium

### Scenario
Research incorrectly classifies Lloyds as PRAGMATIST because:
- CDM work is conducted through UK Finance industry body rather than publicly
- Collaborative efforts with other UK banks (Barclays, NatWest, HSBC) obscure individual contributions
- Regulatory-driven adoption via FCA/BoE coordination not visible in public sources

### Why This Could Happen
- UK banks often coordinate through UK Finance for industry standards
- EMIR Refit compliance may drive collective CDM adoption
- Lloyds may participate in ISDA working groups without public acknowledgment
- Internal technology modernization may include CDM without external announcement

### Mitigation Strategy
- Search for UK Finance CDM initiatives mentioning Lloyds
- Look for conference appearances at industry events (ISDA AGM, UK Finance events)
- Check for cross-bank collaborative announcements on derivatives standards
- Search for FCA/BoE regulatory coordination initiatives

### Probability Assessment
- **Moderate risk** - consortium approach is common in UK banking
- Likelihood of false negative: 25%

---

## Pre-Mortem Gate Decision

| Criterion | Assessment |
|-----------|------------|
| Failure modes identified | 2 (meets Tier B requirement) |
| Mitigation strategies defined | Yes |
| Search strategy informed | Yes |

**Gate Status**: PASSED - Proceed to Evidence Gathering

---

## Search Strategy Recommendations (Informed by Pre-Mortem)

1. **Direct CDM searches**: "Lloyds" + "CDM" + "ISDA"
2. **Vendor differentiation**: "Lloyds" + derivatives technology vendor names
3. **Consortium searches**: UK Finance + CDM + member banks
4. **EMIR Refit**: Lloyds + EMIR Refit + derivatives reporting
5. **Job postings**: Technical roles mentioning CDM/derivatives standards
6. **Conference participation**: ISDA events + UK bank participation
