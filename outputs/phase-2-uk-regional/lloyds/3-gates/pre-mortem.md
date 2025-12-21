# Pre-Mortem Analysis: Lloyds Banking Group PLC

**Bank:** Lloyds Banking Group PLC
**Phase:** 2 - UK Regional
**Date:** 2025-12-21

---

## Research Objective

**Primary Goal**: Assess Lloyds Banking Group's CDM adoption status for UK Regional bank classification

**Key Questions**:
1. Did Lloyds continue CDM work after 2018-2019 FCA/BoE DRR pilot?
2. How is Lloyds addressing EMIR Refit compliance?
3. Does Lloyds' retail/commercial focus reduce CDM priority?
4. Is there any derivatives technology strategy involving CDM?

## Potential Failure Modes

| Risk | Description | Mitigation |
|------|-------------|------------|
| False Positive | Overstating CDM engagement | Require Tier 1 corroboration |
| False Negative | Missing silent implementation | Check job postings, LinkedIn |
| Stale Evidence | Outdated information | Apply temporal weighting |

## Search Strategy

### Tier 1 (Official Sources)
- Lloyds official news/press releases
- FCA DRR pilot documentation
- FINOS contributor searches
- Annual reports

### Tier 2 (Industry Sources)
- Risk.net, Waters Technology coverage
- Vendor announcements
- Conference participation

### Tier 3 (Signal Sources)
- LinkedIn job postings
- Employee profiles
- GitHub activity

## Key Hypotheses to Test

### H1: Lloyds continued CDM work after 2019 pilot
- **Disconfirming evidence**: Complete absence of post-2019 activity

### H2: Retail banking focus reduces CDM priority
- **Supporting evidence**: Small derivatives book, limited CIB operations
- **Disconfirming evidence**: Significant derivatives business

## Decision Points

1. After Tier 1: If P(ARCHITECT) < 20% or > 80%, consider early classification
2. After Tier 2: Assess if Tier 3 signals will add value
3. After Tier 3: Proceed to adversarial challenge

## Null Hypothesis Reminder

Assume Lloyds Banking Group PLC is PRAGMATIST until evidence proves otherwise.

---
