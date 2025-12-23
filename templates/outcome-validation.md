# Outcome Validation Template

## Purpose

Use this template to record when a prediction can be validated against an actual outcome. This enables Brier score calculation and calibration tracking per `methodology/calibration-tracking.md`.

---

## Outcome Validation: [BANK NAME]

### Original Assessment

| Field | Value |
|-------|-------|
| **Bank ID** | [e.g., deutsche-bank] |
| **Assessment Date** | [YYYY-MM-DD] |
| **Phase** | [e.g., phase-1-european-tier1] |
| **Classification** | [ARCHITECT-Native / ARCHITECT-Leader / ARCHITECT-Follower / PRAGMATIST] |
| **Confidence** | [X]% |
| **Implied Probability (ARCHITECT)** | [X/100] |
| **Assessment File** | [Path to original assessment] |

### Validation Event

| Field | Value |
|-------|-------|
| **Validation Date** | [YYYY-MM-DD] |
| **Days Since Assessment** | [X days] |
| **Validation Type** | [ ] Production Announcement / [ ] Rejection Statement / [ ] FINOS Contribution / [ ] Vendor Confirmation / [ ] Time-Based (24+ months) |
| **Actual Outcome** | [ ] 1 = ARCHITECT confirmed / [ ] 0 = PRAGMATIST confirmed |
| **Source URL** | [Full URL] |
| **Source Verification** | [ ] URL accessible / [ ] Content matches claim / [ ] Archived |

### Validation Evidence

**Summary of Validating Event:**

[2-3 sentences describing what happened that confirms or refutes the original assessment]

**Key Quote (if applicable):**

> "[Direct quote from source that confirms outcome]"

---

## Calibration Calculation

### Squared Error

```
Predicted Probability (P):     [X.XX]
Actual Outcome (O):            [0 or 1]
Squared Error = (P - O)²:      [X.XXXX]
```

### Worked Example

If original assessment was 85% ARCHITECT and bank confirmed CDM production:
- P = 0.85
- O = 1
- Squared Error = (0.85 - 1)² = 0.0225

If original assessment was 85% ARCHITECT but bank announced vendor-only approach:
- P = 0.85
- O = 0
- Squared Error = (0.85 - 0)² = 0.7225

---

## Calibration Analysis

### Was the Confidence Appropriate?

| Question | Answer |
|----------|--------|
| Did outcome match prediction direction? | [ ] Yes [ ] No |
| Was confidence level justified by evidence? | [ ] Yes [ ] No / [ ] Too High / [ ] Too Low |
| Were there warning signs we missed? | [ ] Yes (describe below) / [ ] No |
| Did any evidence mislead us? | [ ] Yes (describe below) / [ ] No |

### Root Cause Analysis (if squared error > 0.25)

**What went wrong:**

[Describe why the prediction was significantly off]

**Evidence we should have weighted differently:**

| Evidence | Original Weight | Should Have Been | Why |
|----------|-----------------|------------------|-----|
| [E001] | [LR] | [LR] | [Reason] |
| [E002] | [LR] | [LR] | [Reason] |

**Methodology improvements suggested:**

- [ ] Adjust LR for evidence type: ___________
- [ ] Adjust confidence caps for tier: ___________
- [ ] Add new evidence type to tables: ___________
- [ ] Other: ___________

---

## Data Entry

### For calibration-scores.json

Copy this entry to `outputs/state/calibration-scores.json`:

```json
{
  "bank_id": "[bank-id]",
  "assessment_date": "[YYYY-MM-DD]",
  "validation_date": "[YYYY-MM-DD]",
  "predicted_probability": [X.XX],
  "actual_outcome": [0 or 1],
  "squared_error": [X.XXXX],
  "validation_source": "[URL]",
  "validation_type": "[type]",
  "notes": "[brief notes]"
}
```

---

## Sign-Off

| Field | Value |
|-------|-------|
| **Validated By** | [Name/ID] |
| **Validation Date** | [YYYY-MM-DD] |
| **Review Status** | [ ] Pending / [ ] Reviewed / [ ] Incorporated into Brier score |

---

_Template Version: 1.0_
_Last Updated: 2025-12-20_
