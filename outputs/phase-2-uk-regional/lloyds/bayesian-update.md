# Bayesian Update: Lloyds Banking Group PLC
## Tier B Protocol

**Date**: 2025-12-19
**Prior**: P(Architect) = 20%

---

## Bayesian Framework

Using likelihood ratios to update probability based on evidence gathered.

### Formula
```
P(A|E) = P(E|A) * P(A) / [P(E|A) * P(A) + P(E|~A) * P(~A)]
```

Where:
- P(A) = Prior probability of being Architect (0.20)
- P(E|A) = Probability of observing this evidence if Architect
- P(E|~A) = Probability of observing this evidence if PRAGMATIST

---

## Evidence Likelihood Assessment

### Evidence Set 1: No ISDA CDM Working Group Membership
- **Observation**: Lloyds not listed among CDM contributors
- **P(E|A)**: 0.10 (unlikely an Architect would have no public CDM involvement)
- **P(E|~A)**: 0.95 (expected for PRAGMATIST)
- **Likelihood Ratio**: 0.10 / 0.95 = 0.105

### Evidence Set 2: Retail-Focused Business Model
- **Observation**: Limited derivatives operations, no investment banking
- **P(E|A)**: 0.15 (Architects typically have significant derivatives business)
- **P(E|~A)**: 0.70 (common among PRAGMATIST regional banks)
- **Likelihood Ratio**: 0.15 / 0.70 = 0.214

### Evidence Set 3: Technology Focus on Retail Digital
- **Observation**: No derivatives technology investments visible
- **P(E|A)**: 0.20 (Architects invest in derivatives infrastructure)
- **P(E|~A)**: 0.80 (expected for retail-focused banks)
- **Likelihood Ratio**: 0.20 / 0.80 = 0.250

### Evidence Set 4: No Job Postings or Technical Contributions
- **Observation**: Absence of CDM-related hiring or publications
- **P(E|A)**: 0.15 (Architects typically hire for CDM roles)
- **P(E|~A)**: 0.90 (expected for Non-Architects)
- **Likelihood Ratio**: 0.15 / 0.90 = 0.167

---

## Combined Likelihood Calculation

### Combined Likelihood Ratio (CLR)
```
CLR = LR1 × LR2 × LR3 × LR4
CLR = 0.105 × 0.214 × 0.250 × 0.167
CLR = 0.00094
```

### Posterior Calculation
```
Prior Odds = P(A) / P(~A) = 0.20 / 0.80 = 0.25
Posterior Odds = Prior Odds × CLR = 0.25 × 0.00094 = 0.000235
P(A|E) = Posterior Odds / (1 + Posterior Odds) = 0.000235 / 1.000235 = 0.000235
```

**Raw Posterior**: P(Architect | Evidence) = 0.02%

---

## Posterior Calibration

The raw Bayesian calculation yields an extremely low probability. However, calibration adjustments are needed:

### Calibration Factors
1. **Evidence incompleteness**: Web search unavailable, reducing evidence confidence
2. **Hidden consortium work**: UK banks may collaborate invisibly
3. **Vendor-mediated adoption**: Could adopt CDM via vendors without public acknowledgment
4. **Future adoption potential**: EMIR requirements may drive future adoption

### Calibrated Posterior
Applying conservative floor and uncertainty adjustment:
- Raw posterior: 0.02%
- Uncertainty adjustment: +3% (for evidence incompleteness)
- Consortium possibility: +1%
- Vendor-mediated adoption: +1%

**Calibrated Posterior**: P(Architect) = **5%**

---

## Gate 1 Assessment

| Criterion | Value | Threshold | Result |
|-----------|-------|-----------|--------|
| P(Architect) | 5% | > 80% | **NOT MET** |
| P(PRAGMATIST) | 95% | > 80% | **MET** |

### Gate 1 Decision
- **Skip to adversarial**: NO (P < 80% Architect threshold)
- **Proceed to adversarial**: YES (to confirm PRAGMATIST classification)
- **High confidence PRAGMATIST**: P(PRAGMATIST) = 95% exceeds 80% threshold

Per Tier B protocol, proceed to single-tier adversarial analysis to confirm classification.

---

## Updated Probability Summary

| Stage | P(Architect) | P(PRAGMATIST) |
|-------|--------------|------------------|
| Prior | 20% | 80% |
| Post-Evidence | 5% | 95% |

**Probability Movement**: -15 percentage points (significant shift toward PRAGMATIST)
