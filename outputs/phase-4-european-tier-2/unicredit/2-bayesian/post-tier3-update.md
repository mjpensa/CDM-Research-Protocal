# Bayesian Update: Post-Tier 3 Evidence

**Bank:** UniCredit
**Phase:** 4 - European Tier 2
**Update Date:** 2025-12-20

---

## Prior Probabilities (Post-Tier 2)

| Classification | Prior P(H) |
|---------------|-----------|
| ARCHITECT | 0.6% |
| PRAGMATIST | 54.8% |
| OBSERVER | 43.9% |
| UNKNOWN | 0.7% |

---

## Tier 3 Evidence Summary

**No Tier 3 evidence found.**

**Sources Searched:**
- LinkedIn (no CDM/ISDA job postings)
- Indeed (no CDM-related roles)
- Glassdoor (no FINOS/CDM mentions)

---

## Impact of Null Results

### Likelihood Ratios for Absence of Tier 3 Evidence

**Given:**
- P(No T3 Evidence|ARCHITECT) = 0.10 (architects usually hire for CDM roles)
- P(No T3 Evidence|PRAGMATIST) = 0.60 (pragmatists may not signal CDM hiring)
- P(No T3 Evidence|OBSERVER) = 0.80 (observers rarely hire for CDM-specific roles)
- P(No T3 Evidence|UNKNOWN) = 0.95 (no hiring signals consistent with no engagement)

**Likelihood Ratios:**
- LR(ARCHITECT) = 0.10 / 0.60 = 0.17
- LR(PRAGMATIST) = 0.60 / 0.60 = 1.0 (baseline)
- LR(OBSERVER) = 0.80 / 0.60 = 1.33
- LR(UNKNOWN) = 0.95 / 0.60 = 1.58

---

## Bayesian Calculation

### Step 1: Multiply Priors by LRs

| Classification | Prior | LR | Prior × LR |
|---------------|-------|-----|-----------|
| ARCHITECT | 0.006 | 0.17 | 0.00102 |
| PRAGMATIST | 0.548 | 1.0 | 0.54800 |
| OBSERVER | 0.439 | 1.33 | 0.58387 |
| UNKNOWN | 0.007 | 1.58 | 0.01106 |
| **Sum** | | | **1.14395** |

### Step 2: Normalize

| Classification | Unnormalized | Normalized P(H|E) |
|---------------|-------------|------------------|
| ARCHITECT | 0.00102 | 0.00102 / 1.14395 = **0.1%** |
| PRAGMATIST | 0.54800 | 0.54800 / 1.14395 = **47.9%** |
| OBSERVER | 0.58387 | 0.58387 / 1.14395 = **51.0%** |
| UNKNOWN | 0.01106 | 0.01106 / 1.14395 = **1.0%** |

---

## Final Posterior Probabilities

| Classification | Post-Tier 2 | Post-Tier 3 | Change |
|---------------|------------|-------------|--------|
| ARCHITECT | 0.6% | 0.1% | -0.5% |
| PRAGMATIST | 54.8% | 47.9% | -6.9% |
| OBSERVER | 43.9% | 51.0% | +7.1% |
| UNKNOWN | 0.7% | 1.0% | +0.3% |

**Key Movement:**
- OBSERVER crossed 50% threshold, becoming leading hypothesis
- PRAGMATIST declined from 54.8% to 47.9%
- Complete absence of evidence across all tiers drives OBSERVER classification
- ARCHITECT effectively ruled out (<1%)

---

## Evidence Synthesis

### Total Evidence Collected

| Tier | Evidence Items | Null Results |
|------|---------------|--------------|
| 1 | 1 (historical) | 3 |
| 2 | 0 | 4 |
| 3 | 0 | 3 |
| **Total** | **1** | **10** |

### Evidence Characteristics

- **Single Evidence Item:** UC-001 (TJ Lim ISDA Board 2011-2016)
- **Evidence Age:** 9 years (historical category)
- **Freshness Multiplier:** 0.3
- **Null Result Ratio:** 10:1 (null to positive)

---

## Final Classification

| Element | Value |
|---------|-------|
| **Classification** | OBSERVER |
| **Sub-Classification** | Historical-Engagement |
| **Confidence** | 40% |
| **Bayesian Posterior** | 51.0% |

**Rationale for 40% Confidence (not 51%):**

1. **Historical Evidence Limitation:** Single evidence item from 2011-2016 (pre-CDM era)
2. **Temporal Decay:** 9-year gap reduces confidence per CLAUDE.md Section 6
3. **No Corroboration:** Zero supporting evidence across Tiers 2-3
4. **Informative Absence:** Comprehensive null results suggest no current engagement
5. **Confidence Calibration:** Bayesian 51% adjusted down to 40% due to evidence age

---

## Comparison to Phase 4 Peers

| Bank | Classification | Evidence | Age | Confidence | Bayesian |
|------|---------------|----------|-----|------------|----------|
| Credit Agricole | OBSERVER (Ecosystem) | Current Board | <1 year | 55% | 65% |
| UniCredit | OBSERVER (Historical) | Historical Board | 9 years | 40% | 51% |
| ING | UNKNOWN | None | N/A | 30% | 35% |

UniCredit falls between Credit Agricole (active engagement) and ING (no evidence).

---

## Key Insights

1. **Historical vs. Current:** UniCredit's engagement ended before CDM development began
2. **No Continuity:** 9-year gap with no replacement or sustained participation
3. **Pre-CDM Era:** TJ Lim's board tenure (2011-2016) predates ISDA CDM initiative
4. **Informative Absence:** Comprehensive searches yielded only historical evidence

---

## Confidence Calibration Notes

Final confidence of 40% reflects:
- Bayesian posterior of 51% for OBSERVER
- Downward adjustment for temporal decay (-8%)
- Downward adjustment for lack of corroboration (-3%)
- Historical evidence cannot support >40% per CLAUDE.md temporal thresholds
