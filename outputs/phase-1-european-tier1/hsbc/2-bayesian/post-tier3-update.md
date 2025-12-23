# HSBC - Bayesian Update: Post-Tier 3

## Prior State (Post-Tier 2)
| Metric | Value |
|--------|-------|
| P(Architect) | 73% |
| P(Pragmatist) | 27% |

## Tier 3 Evidence

| ID | Claim | LR | Direction |
|----|-------|-----|-----------|
| (null) | No CDM-specific job postings | 1.0 | NEUTRAL |

## Bayesian Calculation

### Step 1: Combined Likelihood Ratio
```
LR_combined = 1.0 (neutral)
```

### Step 2: Update Probability
```
P(Architect) = 73% (unchanged)
```

## Posterior State

| Metric | Before | After |
|--------|--------|-------|
| P(Architect) | 73% | 73% |
| P(Pragmatist) | 27% | 27% |

## Classification Decision

At P(Architect) = 73%, HSBC is borderline between PRAGMATIST and ARCHITECT.

Given:
- No FINOS membership
- No CDM contribution evidence
- No production DRR announcement
- Historical pilot only (5+ years ago)

**Decision**: Classify as **PRAGMATIST** with governance engagement.

## Final Pre-Adversarial State

| Metric | Value |
|--------|-------|
| **Classification** | PRAGMATIST |
| **Sub-Classification** | Governance (ISDA Board) |
| **Confidence** | 70% |
| **Maturity Score** | 2 (historical pilot + governance) |
| **Engagement Type** | Governance-focused |

---
*Bayesian Update Complete*
*Classification: PRAGMATIST @ 70%*
*Generated: 2025-12-21*
