# NatWest Group - Pre-Mortem Analysis

## Bank Profile
| Attribute | Value |
|-----------|-------|
| **Bank** | NatWest Group (formerly Royal Bank of Scotland) |
| **Headquarters** | Edinburgh, UK |
| **Type** | Universal bank (retail/commercial focus) |
| **Prior P(ARCHITECT)** | 25% |

## Pre-Mortem: Why Classification Might Fail

### Scenario 1: False Positive (ARCHITECT when actually PRAGMATIST)
**Risk**: NatWest's legacy RBS investment banking unit (scaled down post-2008) may show historical CDM involvement that no longer reflects current state.
**Mitigation**: Verify recency of any CDM evidence; post-restructuring focus is retail/commercial.

### Scenario 2: False Negative (PRAGMATIST when actually ARCHITECT)
**Risk**: NatWest may have quiet CDM adoption through UK regulatory compliance (EMIR Refit) without public announcement.
**Mitigation**: Search for FCA/BOE regulatory sandboxes, DRR pilot participation.

### Scenario 3: Missing Evidence
**Risk**: UK domestic focus may mean less visibility in international CDM coverage.
**Mitigation**: Focus on UK-specific sources (FCA, BOE, UK fintech press).

## Key Search Hypotheses

### H1: FCA/BOE DRR Engagement
NatWest may have participated in UK digital regulatory reporting pilots alongside other UK banks.

### H2: FINOS Membership
Check for FINOS membership status similar to Lloyds.

### H3: ISDA Working Groups
Check for ISDA working group participation despite lower derivatives exposure.

### H4: Technology Partners
NatWest has partnerships with various technology vendors; check for CDM-related implementations.

## Prediction
| Classification | Probability |
|----------------|-------------|
| ARCHITECT | 25% |
| PRAGMATIST | 65% |
| OBSERVER | 10% |

**Reasoning**: Lower derivatives exposure than Lloyds, less likely to have FINOS membership given retail focus post-RBS restructuring.

---
*Pre-mortem generated: 2025-12-21*
