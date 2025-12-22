# Bayesian Update: Post-Tier 2

**Bank**: Banco Santander S.A.
**Phase**: 5 (Spanish)
**Date**: 2025-12-21

---

## Prior (Post-Tier 1)

| Classification | Prior |
|---------------|-------|
| ARCHITECT | 1% |
| PRAGMATIST | 55% |
| OBSERVER | 36% |
| UNKNOWN | 8% |

---

## Tier 2 Evidence Summary

| Evidence ID | Claim | Direction |
|-------------|-------|-----------|
| SANT-E001 | UK DRR pilot participation (2022) | Positive (CDM ecosystem engagement) |
| SANT-E004 | ISDA protocol adherence (2013) | Neutral (standard compliance) |
| Null | No trade press CDM coverage | Neutral/Negative |
| Null | No vendor CDM relationship | Negative for Vendor-Pragmatist |
| Null | No conference presentations | Negative |

---

## Key Evidence: UK DRR Pilot Participation

**Finding**: Santander participated in UK DRR Phase 2 (Feb 2022) alongside Barclays, Credit Suisse, HSBC, NatWest, and Lloyds.

**Significance**:
- Direct exposure to ISDA CDM 2.0 technology
- Collaboration with FCA/BOE regulatory bodies
- Peer cohort included known ARCHITECT (Barclays) and PRAGMATIST banks

**Limitations**:
- Evidence is **dated** (35 months old)
- No visible follow-through or sustained engagement
- Freshness weight: 0.5

---

## Likelihood Ratios

### ARCHITECT Hypothesis
- P(DRR pilot | ARCHITECT) = 0.8 (ARCHITECTs likely to participate)
- P(No trade press | ARCHITECT) = 0.3 (Would expect some coverage)
- P(No vendor CDM | ARCHITECT) = 0.5 (May build internally)
- **Combined**: 0.12

### PRAGMATIST Hypothesis
- P(DRR pilot | PRAGMATIST) = 0.4 (Some pragmatists in pilots)
- P(No trade press | PRAGMATIST) = 0.7 (Less newsworthy)
- P(No vendor CDM | PRAGMATIST) = 0.5 (May not be vendor-dependent type)
- **Combined**: 0.14

### OBSERVER Hypothesis
- P(DRR pilot | OBSERVER) = 0.1 (Observers rarely in pilots)
- P(No trade press | OBSERVER) = 0.9 (Expected)
- P(No vendor CDM | OBSERVER) = 0.9 (Expected)
- **Combined**: 0.081

---

## Posterior Calculation

| Classification | Prior | Likelihood | Unnormalized | Posterior |
|---------------|-------|------------|--------------|-----------|
| ARCHITECT | 0.01 | 0.12 | 0.0012 | 2% |
| PRAGMATIST | 0.55 | 0.14 | 0.077 | 67% |
| OBSERVER | 0.36 | 0.081 | 0.029 | 26% |
| UNKNOWN | 0.08 | 0.05 | 0.004 | 5% |

**Total**: 0.1112
**Normalization Factor**: 8.99

---

## Post-Tier 2 Posterior

| Classification | Posterior |
|---------------|-----------|
| ARCHITECT | 2% |
| **PRAGMATIST** | **67%** |
| OBSERVER | 26% |
| UNKNOWN | 5% |

---

## Key Insights

1. **DRR pilot shifts probability toward PRAGMATIST**: The UK DRR participation is strong evidence of CDM ecosystem engagement, differentiating Santander from OBSERVER status.

2. **ARCHITECT remains unlikely**: Despite pilot participation, the lack of FINOS contribution, ongoing engagement, and CFTC enforcement action make ARCHITECT classification improbable.

3. **PRAGMATIST (Ecosystem) best fit**: Santander fits the "Ecosystem" subtype - participated in CDM pilot but without internal build or vendor relationship.

4. **Freshness concern**: The dated nature of the DRR evidence (2022) limits confidence. Need to check for recent signals in Tier 3.

---

## Subtype Analysis

| PRAGMATIST Subtype | Fit |
|-------------------|-----|
| ISDA Governance | No - not on ISDA Board/CDM Steering |
| Ecosystem | **Yes** - DRR pilot participant |
| Vendor-Dependent | No - no vendor CDM relationship found |
| Traditional | Partial - active derivatives but dated CDM engagement |

**Recommended Subtype**: PRAGMATIST (Ecosystem)

---

## Decision

**Proceed to Tier 3**: Confirm no recent CDM signals before finalizing classification.
