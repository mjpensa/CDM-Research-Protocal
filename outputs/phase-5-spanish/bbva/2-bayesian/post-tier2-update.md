# Bayesian Update: Post-Tier 2

**Bank**: Banco Bilbao Vizcaya Argentaria S.A.
**Phase**: 5 (Spanish)
**Date**: 2025-12-21

---

## Prior (Post-Tier 1)

| Classification | Prior |
|---------------|-------|
| ARCHITECT | 1% |
| PRAGMATIST | 48% |
| OBSERVER | 46% |
| UNKNOWN | 5% |

---

## Tier 2 Evidence Summary

| Evidence ID | Claim | Direction |
|-------------|-------|-----------|
| BBVA-E002 | ISDA 2012 FATCA Protocol | Neutral (standard) |
| BBVA-E003 | ISDA 2018 Resolution Stay | Neutral (standard) |
| BBVA-E004 | Accenture/Murex/Calypso | Weak positive (vendor) |
| **Null** | **NOT in UK DRR pilot** | **Negative (key finding)** |
| Null | No trade press CDM | Neutral |

---

## Key Finding: UK DRR Pilot Absence

**BBVA was confirmed NOT to be a participant in the UK DRR pilot.**

Pilot participants were: Barclays, Credit Suisse, HSBC, Lloyds, Nationwide, NatWest, and Santander.

### Implications
1. Unlike peer Santander, BBVA has no demonstrated CDM pilot experience
2. BBVA has not engaged with FCA/BOE on DRR initiatives
3. The key differentiator between Spanish banks is established

---

## Likelihood Ratios

### PRAGMATIST Hypothesis
- P(No DRR pilot | PRAGMATIST) = 0.6 (many pragmatists not in pilot)
- P(Murex/Calypso | PRAGMATIST) = 0.5 (common platform)
- **Combined**: 0.30

### OBSERVER Hypothesis
- P(No DRR pilot | OBSERVER) = 0.9 (observers typically not in pilots)
- P(Murex/Calypso | OBSERVER) = 0.3 (less likely to invest)
- **Combined**: 0.27

---

## Posterior Calculation

| Classification | Prior | Likelihood | Unnormalized | Posterior |
|---------------|-------|------------|--------------|-----------|
| ARCHITECT | 0.01 | 0.05 | 0.0005 | 0% |
| PRAGMATIST | 0.48 | 0.30 | 0.144 | 51% |
| OBSERVER | 0.46 | 0.27 | 0.124 | 44% |
| UNKNOWN | 0.05 | 0.05 | 0.0025 | 5% |

---

## Post-Tier 2 Posterior

| Classification | Posterior |
|---------------|-----------|
| ARCHITECT | 0% |
| **PRAGMATIST** | **51%** |
| OBSERVER | 44% |
| UNKNOWN | 5% |

---

## Key Insights

1. **Still near parity**: PRAGMATIST and OBSERVER remain close (51% vs 44%)

2. **DRR absence is informative**: Unlike Santander's DRR participation, BBVA's absence shifts probability slightly toward OBSERVER

3. **Vendor relationship provides minimal lift**: Murex/Calypso relationship is too common to be strongly informative

4. **PRAGMATIST (Traditional) subtype**: If PRAGMATIST, the "Traditional" subtype (active derivatives, no CDM) fits best

---

## Subtype Analysis

If PRAGMATIST:

| Subtype | Fit |
|---------|-----|
| ISDA Governance | No - not on Board/Steering |
| Ecosystem | No - not in DRR pilot |
| Vendor-Dependent | Weak - no CDM-specific vendor |
| **Traditional** | **Yes - active derivatives, no CDM** |

---

## Decision

**Proceed to Tier 3**: Need to check for hiring signals that might indicate hidden CDM activity.
