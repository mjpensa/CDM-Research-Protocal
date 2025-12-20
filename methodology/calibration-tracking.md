# Calibration Tracking

## Purpose

Track prediction accuracy over time using Brier scores to validate that confidence levels are well-calibrated. This enables continuous improvement of the assessment methodology by comparing predictions against actual outcomes.

**Reference**: Tetlock's superforecasting research demonstrates that the best forecasters achieve Brier scores around 0.14, while random guessing yields 0.25 for binary predictions.

---

## Brier Score Formula

The Brier score measures the accuracy of probabilistic predictions:

```
Brier Score = (1/N) × Σ(forecast_probability - actual_outcome)²
```

Where:
- `forecast_probability` = Your predicted probability (0 to 1)
- `actual_outcome` = What actually happened (1 = ARCHITECT confirmed, 0 = PRAGMATIST confirmed)
- `N` = Number of predictions validated

### Interpretation Scale

| Brier Score | Interpretation | Action |
|-------------|----------------|--------|
| 0.00 - 0.10 | Excellent calibration | Maintain current methodology |
| 0.10 - 0.15 | Very good (superforecaster level) | Minor refinements only |
| 0.15 - 0.20 | Good calibration | Review edge cases |
| 0.20 - 0.25 | Marginal (approaching random) | Systematic review needed |
| > 0.25 | Poor (worse than random) | Major methodology revision required |

---

## Outcome Recording

### When to Record Outcomes

Record a validation event when any of the following occurs:

1. **Official Production Announcement**: Bank announces CDM deployment
   - Outcome: 1 (ARCHITECT confirmed)

2. **Official Rejection Statement**: Bank explicitly states no CDM plans
   - Outcome: 0 (PRAGMATIST confirmed)

3. **Vendor-Only Confirmation**: Bank confirms vendor-dependent regulatory reporting
   - Outcome: 0 (PRAGMATIST confirmed)

4. **FINOS/ISDA Contribution**: Bank appears as CDM contributor
   - Outcome: 1 (ARCHITECT confirmed)

5. **Time-Based Confirmation**: 24+ months elapsed with no CDM activity
   - Outcome: 0 (PRAGMATIST confirmed, with caveat)

### Recording Process

1. Locate original assessment in `outputs/phase-X/{bank}/`
2. Create validation file using `templates/outcome-validation.md`
3. Calculate squared error: `(predicted_probability - actual_outcome)²`
4. Update running Brier score in `outputs/state/calibration-scores.json`

---

## Calibration Targets

Based on Tetlock's superforecasting research and ENFSI forensic standards:

| Metric | Target | Warning | Failure |
|--------|--------|---------|---------|
| Brier Score | < 0.20 | 0.20 - 0.25 | > 0.25 |
| Minimum Validations | 10 | 5-9 | < 5 |
| Calibration Curve R² | > 0.85 | 0.70 - 0.85 | < 0.70 |

**Note**: Fewer than 10 validations is insufficient for reliable calibration assessment.

---

## Calibration Curve Analysis

Beyond Brier scores, plot a calibration curve to visualize accuracy:

### Expected Pattern (Well-Calibrated)

```
Actual Outcome Rate
    100% |                    *
         |                 *
     80% |              *
         |           *
     60% |        *
         |     *
     40% |  *
         |*
     20% +------------------------
         20%  40%  60%  80%  100%
              Predicted Probability
```

A well-calibrated forecaster shows predictions falling along the diagonal.

### Common Miscalibration Patterns

| Pattern | Meaning | Fix |
|---------|---------|-----|
| Below diagonal | Overconfident | Lower confidence caps |
| Above diagonal | Underconfident | Allow higher confidence |
| S-curve | Extreme predictions too confident | Moderate extreme probabilities |
| Flat line | Predictions not discriminating | Improve evidence weighting |

---

## Periodic Calibration Review

### Quarterly Review Checklist

- [ ] Calculate current Brier score across all validated predictions
- [ ] Plot calibration curve
- [ ] Identify banks where prediction was most wrong
- [ ] Analyze systematic errors (e.g., always overconfident on European banks)
- [ ] Propose methodology adjustments if Brier > 0.20

### Review Template

```markdown
## Calibration Review: [QUARTER YEAR]

### Summary Statistics
- Predictions validated this quarter: [N]
- Cumulative predictions validated: [N]
- Current Brier Score: [X.XX]
- Previous Brier Score: [X.XX]
- Trend: [Improving / Stable / Declining]

### Largest Errors

| Bank | Predicted | Actual | Squared Error | Root Cause |
|------|-----------|--------|---------------|------------|
| [Bank 1] | [X]% ARCHITECT | [Outcome] | [Error] | [Analysis] |
| [Bank 2] | [X]% ARCHITECT | [Outcome] | [Error] | [Analysis] |

### Systematic Patterns Identified
[Describe any patterns in errors]

### Recommended Adjustments
[List specific methodology changes]
```

---

## Integration with Decision Thresholds

The calibration tracking system informs threshold adjustments in `config/decision-thresholds.json`:

### Automatic Threshold Review Triggers

| Condition | Trigger |
|-----------|---------|
| Brier score > 0.25 | Review all confidence caps |
| 3+ consecutive overconfident errors | Lower maximum confidence by 5% |
| 3+ consecutive underconfident errors | Raise minimum confidence by 5% |
| Tier-specific miscalibration | Adjust tier-specific LR values |

---

## Data Storage

### Calibration Scores File

Location: `outputs/state/calibration-scores.json`

```json
{
  "last_updated": "2025-12-20",
  "total_validations": 0,
  "current_brier_score": null,
  "validations": [],
  "quarterly_reviews": []
}
```

### Validation Entry Format

```json
{
  "bank_id": "deutsche-bank",
  "assessment_date": "2025-12-18",
  "validation_date": "2026-06-15",
  "predicted_probability": 0.85,
  "actual_outcome": 1,
  "squared_error": 0.0225,
  "validation_source": "https://example.com/announcement",
  "notes": "Production deployment announced"
}
```

---

## References

- Tetlock, P. E., & Gardner, D. (2015). *Superforecasting: The Art and Science of Prediction*
- Dawid, A. P. (1982). "The Well-Calibrated Bayesian." *Journal of the American Statistical Association*, 77(379), 605-610
- Good Judgment Project calibration standards: https://goodjudgment.com

---

_Last Updated: 2025-12-20_
