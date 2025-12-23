# Bayesian Update: Post-Tier 3

**Bank**: Banco Bilbao Vizcaya Argentaria S.A.
**Phase**: 5 (Spanish)
**Date**: 2025-12-21

---

## Prior (Post-Tier 2)

| Classification | Prior |
|---------------|-------|
| ARCHITECT | 0% |
| PRAGMATIST | 51% |
| OBSERVER | 44% |
| UNKNOWN | 5% |

---

## Tier 3 Evidence Summary

| Search Target | Result | Direction |
|--------------|--------|-----------|
| CDM job postings | None found | Neutral/Negative |
| LinkedIn CDM activity | None found | Neutral |
| Employee blogs | None found | Neutral |
| GitHub personal | None found | Negative |

---

## Tier 3 Null Analysis

Complete absence of Tier 3 signals:

1. **No CDM job postings**: Not building CDM team
2. **No LinkedIn advocacy**: No visible CDM interest
3. **No personal contributions**: No employee CDM activity

This is consistent with both PRAGMATIST (Traditional) and OBSERVER classifications.

---

## Likelihood Ratios

### PRAGMATIST Hypothesis
- P(No CDM jobs | PRAGMATIST) = 0.7 (traditional pragmatists don't hire for CDM)
- P(No LinkedIn | PRAGMATIST) = 0.7
- **Combined**: 0.49

### OBSERVER Hypothesis
- P(No CDM jobs | OBSERVER) = 0.95
- P(No LinkedIn | OBSERVER) = 0.9
- **Combined**: 0.855

---

## Posterior Calculation

| Classification | Prior | Likelihood | Unnormalized | Posterior |
|---------------|-------|------------|--------------|-----------|
| ARCHITECT | 0.00 | 0.05 | 0.000 | 0% |
| PRAGMATIST | 0.51 | 0.49 | 0.250 | 48% |
| OBSERVER | 0.44 | 0.855 | 0.376 | 47% |
| UNKNOWN | 0.05 | 0.5 | 0.025 | 5% |

---

## Final Posterior

| Classification | Posterior |
|---------------|-----------|
| ARCHITECT | 0% |
| **PRAGMATIST** | **48%** |
| OBSERVER | 47% |
| UNKNOWN | 5% |

---

## Classification Decision

This is a **close call** between PRAGMATIST and OBSERVER.

### Arguments for PRAGMATIST (Traditional)
- Active derivatives operations (CFTC/SEC swap dealer)
- Vendor relationship with Murex/Calypso ecosystem
- ISDA protocol adherence demonstrates engagement
- Business need for derivatives reporting exists

### Arguments for OBSERVER
- No CDM-specific evidence whatsoever
- Did not participate in UK DRR pilot (unlike peer Santander)
- No FINOS membership or contribution
- No hiring or advocacy signals

### Decision Rationale
PRAGMATIST (Traditional) is selected because:
1. BBVA has **active derivatives operations** requiring regulatory reporting
2. The **vendor relationship** (Murex/Calypso via Accenture) indicates technology investment
3. OBSERVER would suggest minimal derivatives activity, which contradicts swap dealer status
4. "Traditional" subtype means derivatives-active but non-CDM approach

---

## Final Classification

| Field | Value |
|-------|-------|
| **Classification** | PRAGMATIST |
| **Subtype** | Traditional |
| **Confidence** | 45% |
| **Maturity Score** | 1 |

---

## Confidence Calculation

| Factor | Impact |
|--------|--------|
| No Tier 2 CDM evidence | Caps at 75% |
| Tier 4 inference only for CDM | -20% |
| Near OBSERVER boundary | -10% |
| Vendor relationship | +5% |
| Swap dealer status | +5% |
| **Final Confidence** | **45%** |

---

## Alternative Classification

| Classification | Probability |
|---------------|-------------|
| OBSERVER | 47% |

The OBSERVER alternative is nearly equally probable. The selection of PRAGMATIST over OBSERVER is a marginal call based on derivatives market presence.
