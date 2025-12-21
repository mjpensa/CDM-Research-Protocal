# Bayesian Update: Post-Tier 1 Evidence

**Bank:** UniCredit
**Phase:** 4 - European Tier 2
**Update Date:** 2025-12-20

---

## Prior Probabilities (Phase 4 Baseline)

| Classification | Prior P(H) | Rationale |
|---------------|-----------|-----------|
| ARCHITECT | 5% | European Tier 2 banks rarely lead CDM adoption |
| PRAGMATIST | 70% | Default assumption for major banks |
| OBSERVER | 20% | Some ecosystem engagement expected |
| UNKNOWN | 5% | Minimal evidence scenario |

---

## Tier 1 Evidence Summary

| ID | Claim | Type | Freshness | LR |
|----|-------|------|-----------|-----|
| UC-001 | TJ Lim ISDA Board 2011-2016 | membership_or_participation | Historical (9 years old) | 1.5 |

**Evidence Characteristics:**
- Single Tier 1 evidence item
- Historical engagement (ended 2016)
- Pre-CDM era (CDM development began 2017)
- No current engagement signals

---

## Likelihood Ratios

### UC-001: Historical ISDA Board Membership

**Given:**
- P(E|ARCHITECT) = 0.15 (historical board membership has weak correlation with current technical CDM work)
- P(E|PRAGMATIST) = 0.10 (board membership doesn't distinguish pragmatist from architect in historical context)
- P(E|OBSERVER) = 0.20 (board membership is classic observer behavior)
- P(E|UNKNOWN) = 0.01 (having any ISDA evidence contradicts unknown status)

**Likelihood Ratios:**
- LR(ARCHITECT) = 0.15 / 0.10 = 1.5
- LR(PRAGMATIST) = 0.10 / 0.10 = 1.0 (baseline)
- LR(OBSERVER) = 0.20 / 0.10 = 2.0
- LR(UNKNOWN) = 0.01 / 0.10 = 0.1

**Interpretation:**
- Historical board membership is 2x more likely under OBSERVER hypothesis
- Evidence only weakly supports ARCHITECT (LR=1.5)
- UNKNOWN becomes less likely (LR=0.1)

---

## Bayesian Calculation

### Step 1: Multiply Priors by LRs

| Classification | Prior | LR | Prior × LR |
|---------------|-------|-----|-----------|
| ARCHITECT | 0.05 | 1.5 | 0.075 |
| PRAGMATIST | 0.70 | 1.0 | 0.700 |
| OBSERVER | 0.20 | 2.0 | 0.400 |
| UNKNOWN | 0.05 | 0.1 | 0.005 |
| **Sum** | | | **1.180** |

### Step 2: Normalize

| Classification | Unnormalized | Normalized P(H|E) |
|---------------|-------------|------------------|
| ARCHITECT | 0.075 | 0.075 / 1.180 = **6.4%** |
| PRAGMATIST | 0.700 | 0.700 / 1.180 = **59.3%** |
| OBSERVER | 0.400 | 0.400 / 1.180 = **33.9%** |
| UNKNOWN | 0.005 | 0.005 / 1.180 = **0.4%** |

---

## Post-Tier 1 Probabilities

| Classification | Prior | Posterior | Change |
|---------------|-------|-----------|--------|
| ARCHITECT | 5.0% | 6.4% | +1.4% |
| PRAGMATIST | 70.0% | 59.3% | -10.7% |
| OBSERVER | 20.0% | 33.9% | +13.9% |
| UNKNOWN | 5.0% | 0.4% | -4.6% |

**Key Movement:**
- OBSERVER probability increased from 20% to 33.9%
- PRAGMATIST decreased from 70% to 59.3%
- Evidence shifts probability toward OBSERVER but not decisively

---

## Comparison to Credit Agricole

| Bank | Evidence | Age | OBSERVER Posterior |
|------|----------|-----|-------------------|
| Credit Agricole | Current ISDA Board | <1 year | 65% |
| UniCredit | Historical ISDA Board | 9 years | 34% |

UniCredit's historical evidence provides weaker signal strength than Credit Agricole's current engagement.

---

## Gate 1 Decision

| Metric | Value |
|--------|-------|
| **Leading Hypothesis** | PRAGMATIST (59.3%) |
| **Second Hypothesis** | OBSERVER (33.9%) |
| **Separation** | 25.4 percentage points |
| **Decision** | PROCEED TO TIER 2 |

**Rationale:**
- Single historical evidence item is insufficient
- Need to check for more recent signals in trade press
- Historical evidence alone cannot definitively classify
- Tier 2 may reveal vendor relationships or recent initiatives

---

## Next Steps

1. Search Risk.net for UniCredit CDM coverage (2020-2025)
2. Check Waters Technology for vendor announcements
3. Look for analyst reports on UniCredit derivatives modernization
4. If Tier 2 yields no results, proceed to Tier 3 for hiring signals
