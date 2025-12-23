# HSBC - Bayesian Update: Post-Tier 2

## Prior State (Post-Tier 1)
| Metric | Value |
|--------|-------|
| P(Architect) | 64% |
| P(Pragmatist) | 36% |

## Tier 2 Evidence

| ID | Claim | LR | Direction |
|----|-------|-----|-----------|
| HSBC-004 | ISDA Future Leaders participation | 1.5 | SUPPORTS (weak) |

## Bayesian Calculation

### Step 1: Combined Likelihood Ratio
```
LR_combined = 1.5
```

### Step 2: Update Probability
```
Prior odds = 0.64 / 0.36 = 1.78
Posterior odds = 1.78 × 1.5 = 2.67
P(Architect) = 2.67 / (1 + 2.67) = 72.7%
```

### Step 3: Apply Confidence Cap
Maximum: 75% (no production evidence)
Current: 72.7% < 75% → No cap needed

## Posterior State

| Metric | Before | After |
|--------|--------|-------|
| P(Architect) | 64% | 73% |
| P(Pragmatist) | 36% | 27% |

## Analysis

Tier 2 provided weak supporting evidence. The ISDA Future Leaders participation reinforces ISDA engagement but is not CDM-specific.

---
*Bayesian Update Complete*
*P(Architect) = 73%*
*Generated: 2025-12-21*
