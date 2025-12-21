# Bayesian Update: Post-Tier 2 Evidence

**Bank:** UniCredit
**Phase:** 4 - European Tier 2
**Update Date:** 2025-12-20

---

## Prior Probabilities (Post-Tier 1)

| Classification | Prior P(H) |
|---------------|-----------|
| ARCHITECT | 6.4% |
| PRAGMATIST | 59.3% |
| OBSERVER | 33.9% |
| UNKNOWN | 0.4% |

---

## Tier 2 Evidence Summary

**No Tier 2 evidence found.**

**Sources Searched:**
- Risk.net (no UniCredit CDM articles)
- Waters Technology (no UniCredit CDM coverage)
- DerivSource (no UniCredit CDM mentions)
- Financial News London (no UniCredit CDM reports)

---

## Impact of Null Results

### Likelihood Ratios for Absence of Tier 2 Evidence

**Given:**
- P(No T2 Evidence|ARCHITECT) = 0.05 (architects usually have trade press coverage)
- P(No T2 Evidence|PRAGMATIST) = 0.50 (pragmatists often lack CDM-specific coverage)
- P(No T2 Evidence|OBSERVER) = 0.70 (observers rarely generate trade press attention)
- P(No T2 Evidence|UNKNOWN) = 0.90 (no evidence is consistent with unknown status)

**Likelihood Ratios:**
- LR(ARCHITECT) = 0.05 / 0.50 = 0.1
- LR(PRAGMATIST) = 0.50 / 0.50 = 1.0 (baseline)
- LR(OBSERVER) = 0.70 / 0.50 = 1.4
- LR(UNKNOWN) = 0.90 / 0.50 = 1.8

---

## Bayesian Calculation

### Step 1: Multiply Priors by LRs

| Classification | Prior | LR | Prior × LR |
|---------------|-------|-----|-----------|
| ARCHITECT | 0.064 | 0.1 | 0.0064 |
| PRAGMATIST | 0.593 | 1.0 | 0.5930 |
| OBSERVER | 0.339 | 1.4 | 0.4746 |
| UNKNOWN | 0.004 | 1.8 | 0.0072 |
| **Sum** | | | **1.0812** |

### Step 2: Normalize

| Classification | Unnormalized | Normalized P(H|E) |
|---------------|-------------|------------------|
| ARCHITECT | 0.0064 | 0.0064 / 1.0812 = **0.6%** |
| PRAGMATIST | 0.5930 | 0.5930 / 1.0812 = **54.8%** |
| OBSERVER | 0.4746 | 0.4746 / 1.0812 = **43.9%** |
| UNKNOWN | 0.0072 | 0.0072 / 1.0812 = **0.7%** |

---

## Post-Tier 2 Probabilities

| Classification | Post-Tier 1 | Post-Tier 2 | Change |
|---------------|------------|-------------|--------|
| ARCHITECT | 6.4% | 0.6% | -5.8% |
| PRAGMATIST | 59.3% | 54.8% | -4.5% |
| OBSERVER | 33.9% | 43.9% | +10.0% |
| UNKNOWN | 0.4% | 0.7% | +0.3% |

**Key Movement:**
- OBSERVER increased from 33.9% to 43.9%
- ARCHITECT collapsed from 6.4% to 0.6%
- Null results push toward OBSERVER classification

---

## Gate 2 Decision

| Metric | Value |
|--------|-------|
| **Leading Hypothesis** | PRAGMATIST (54.8%) |
| **Second Hypothesis** | OBSERVER (43.9%) |
| **Separation** | 10.9 percentage points |
| **Decision** | PROCEED TO TIER 3 |

**Rationale:**
- PRAGMATIST and OBSERVER probabilities are converging
- Need additional evidence to resolve classification
- Tier 3 hiring signals may break the tie
- Historical evidence + null results suggests limited engagement

---

## Next Steps

Search Tier 3 sources for:
1. LinkedIn job postings for CDM/ISDA roles
2. LinkedIn posts from UniCredit staff about CDM
3. Indeed/Glassdoor postings mentioning FINOS or DRR
