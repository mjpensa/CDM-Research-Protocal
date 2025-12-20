# Contradiction Resolution Output Template

## Purpose

This template provides a structured format for documenting contradiction resolution when `trust_audit.py` sets the `CONTRADICTIONS_DETECTED` flag. It creates an audit trail showing how conflicting evidence was analyzed and resolved.

**Trigger**: This file is created when `evidence.json` contains contradictory evidence items (identified by trust_audit).

**Workflow Stage**: Stage 5.5 (after Gate 1, before continuing evidence gathering)

---

## Template: contradiction-resolution.md

**Location**: `outputs/phase-[N]/[bank_id]/3-gates/contradiction-resolution.md`

---

```markdown
# Contradiction Resolution Log: [BANK NAME]

**Date**: [YYYY-MM-DD]
**Analyst**: [Name/ID]
**Trigger**: CONTRADICTIONS_DETECTED flag from trust_audit

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Contradictions Identified** | [N] |
| **Resolved** | [N] |
| **Unresolved** | [N] |
| **Total Confidence Impact** | [+/-X]% |

---

## Contradiction 1: [Brief Description]

### Identification

| Field | Source A | Source B |
|-------|----------|----------|
| **Evidence ID** | [E001] | [E003] |
| **Claim** | "[Claim A text]" | "[Claim B text]" |
| **Tier** | [1/2/3] | [1/2/3] |
| **Date** | [YYYY-MM-DD] | [YYYY-MM-DD] |
| **Source URL** | [URL A] | [URL B] |

### Contradiction Type

- [ ] **Temporal** — Both claims true at different points in time
- [ ] **Definitional** — Terms used differently, creating apparent conflict
- [ ] **Factual** — Genuine disagreement; both cannot be true simultaneously

### Source Reliability Analysis

| Criterion | Source A | Source B | Assessment |
|-----------|----------|----------|------------|
| **Authority** | [HIGH/MEDIUM/LOW] | [HIGH/MEDIUM/LOW] | [Which is more authoritative] |
| **Recency** | [Current/Recent/Dated] | [Current/Recent/Dated] | [Which is more recent] |
| **Specificity** | [Specific/Moderate/Vague] | [Specific/Moderate/Vague] | [Which is more specific] |
| **Independence** | [Independent/Derived] | [Independent/Derived] | [Are they truly independent?] |
| **Motivation** | [Assessment] | [Assessment] | [Any bias concerns?] |

### Resolution

**Resolution Method Applied**: [From appendices/contradiction-resolution.md]

- [ ] Temporal: Use most recent source, document evolution
- [ ] Definitional: Both valid under different definitions
- [ ] Factual - Source A Prevails: [Reason]
- [ ] Factual - Source B Prevails: [Reason]
- [ ] Unresolved: Neither source clearly prevails

**Resolution Rationale**:
[2-3 sentences explaining why this resolution is justified]

**Source that Prevails**: [Evidence ID or "Both Valid" or "Unresolved"]

### Impact Assessment

| Impact Type | Value | Notes |
|-------------|-------|-------|
| **Confidence Reduction** | [X]% | [Why this reduction] |
| **LR Adjustment Applied** | [None / 0.5× for superseded / 0.7 penalty] | [Applied to which evidence] |
| **Evidence Excluded** | [Evidence ID or None] | [Why excluded if applicable] |

### Lingering Uncertainty

[Description of what remains uncertain after resolution. If resolved cleanly, state "None - contradiction fully resolved."]

---

## Contradiction 2: [Brief Description]

[Repeat structure above for each contradiction]

---

## Aggregate Impact Summary

### Total Adjustments Applied

| Adjustment Type | Count | Net Impact |
|-----------------|-------|------------|
| Temporal resolutions (no adjustment) | [N] | 0% |
| Definitional resolutions (no adjustment) | [N] | 0% |
| Factual - source prevailed (superseded LR ×0.5) | [N] | [Applied to specific evidence] |
| Unresolved (penalty LR = 0.7) | [N] | [LR factor applied] |

### Confidence Impact Calculation

```
Base confidence before contradictions:     [X]%
- Minor contradiction penalty (-5% each):  [N] × -5% = -[X]%
- Significant contradiction penalty:       [N] × -10% = -[X]%
- Unresolved contradiction penalty:        [N] × -15% = -[X]%
------------------------------------------------
Net confidence adjustment:                 -[X]%
```

### Residual Uncertainties

List all uncertainties that remain after contradiction resolution:

1. [Uncertainty 1]: [Description] — Resolution path: [What would resolve this]
2. [Uncertainty 2]: [Description] — Resolution path: [What would resolve this]

---

## Validation Recommendations

Based on unresolved contradictions, the following validation is recommended:

| Priority | Validation Action | Expected Resolution |
|----------|-------------------|---------------------|
| [High/Medium/Low] | [Specific action to take] | [What this would confirm] |
| [High/Medium/Low] | [Specific action to take] | [What this would confirm] |

---

## Checkpoint Decision

Based on contradiction resolution:

- [ ] **PROCEED** — All contradictions resolved, confidence impact acceptable
- [ ] **BLOCK** — Unresolved contradictions require human review before proceeding

If BLOCK, specify:
- Which contradiction(s) require human review: [List]
- What decision is needed: [Describe]

---

## Integration Instructions

### For Bayesian Analyst

When reading this file, apply the following adjustments:

1. For each "Factual - Source Prevailed" resolution:
   - Reduce LR of superseded source by ×0.5

2. For each "Unresolved" contradiction:
   - Apply penalty LR of 0.7 to combined LR

3. Document adjustments in `post-tier*-update.md` under "Contradiction Adjustments" section

### For Synthesis Agent

When reading this file for confidence-calibration.md:

1. Sum all confidence penalties from this log
2. Apply to Step 3 (Contradiction Adjustment) of calibration
3. Reference this file in calibration documentation

---

## Metadata

| Field | Value |
|-------|-------|
| Template Version | 1.0 |
| Created | [YYYY-MM-DD] |
| Methodology Reference | appendices/contradiction-resolution.md |
| Trust Audit Run | [Timestamp from evidence.json meta] |
```

---

## Usage Notes

1. **Trigger**: Only create this file when `CONTRADICTIONS_DETECTED` flag is present in trust_audit results
2. **Timing**: Create during Stage 5.5 (after Gate 1, before continuing to Tier 2)
3. **Agent**: Reasoning Gate Agent in contradiction resolution mode
4. **Inputs Required**:
   - `evidence.json` with contradiction details from trust_audit
   - `appendices/contradiction-resolution.md` (methodology)

---

## Workflow Integration

### Stage 5.5: Contradiction Resolution (Conditional)

**Trigger**: `trust_audit.py` returns `CONTRADICTIONS_DETECTED` flag

**Process**:
1. Orchestrator detects CONTRADICTIONS_DETECTED in trust_metrics
2. Spawns Reasoning Gate Agent in contradiction resolution mode
3. Agent reads contradiction details from evidence.json
4. Agent applies resolution methodology from appendices/contradiction-resolution.md
5. Agent produces this file
6. If unresolved contradictions remain → BLOCK for human review
7. If all resolved → PROCEED to next stage

**Checkpoint**: BLOCK if unresolved contradictions remain

---

_Template Version: 1.0_
_Last Updated: 2025-12-20_
