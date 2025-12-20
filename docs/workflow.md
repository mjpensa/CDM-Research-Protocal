# CDM/DRR Research Protocol - Master Orchestration Workflow

> **This is the canonical workflow reference.** See also:
> - [hybrid-workflow.md](hybrid-workflow.md) - Deep Research + Claude Standard hybrid approach
> - [execution-checklist.md](execution-checklist.md) - Quick reference checklist

## Overview

This is the MASTER WORKFLOW for executing the CDM/DRR research protocol on 24 international banks across 7 phases. This workflow coordinates all specialized agents, manages state, enforces checkpoints, and produces deliverables.

**Estimated Total Time**: 8-9 hours (vs 20 hours manual)
**Banks**: 24 across 7 phases
**Deliverables**: 24 complete assessments + 7 phase syntheses + final cross-bank analysis

---

## Execution Modes

### Mode 1: Single Bank Test (Recommended First)
Test the entire system on one bank before full rollout.
- **Bank**: Deutsche Bank (Tier A - most rigorous)
- **Purpose**: Validate all agents, templates, and workflows
- **Time**: ~1.5 hours
- **Proceed if**: All outputs generated correctly, checkpoints work

### Mode 2: Phase Pilot
Execute one complete phase to validate cross-bank logic.
- **Phase**: Phase 1 (5 European Tier 1 banks)
- **Purpose**: Test phase synthesis and consistency validation
- **Time**: ~4-5 hours
- **Proceed if**: Phase synthesis complete, QA tests pass

### Mode 3: Full Rollout
Execute all 7 phases, all 24 banks.
- **Phases**: 1 → 2 → 3 → 4 → 5 → 6 → 7
- **Purpose**: Complete research for all banks
- **Time**: ~8-9 hours
- **Result**: All deliverables produced

---

## State Files

**Primary State**: `outputs/state/workflow-state.json`
**Checkpoint Log**: `outputs/state/checkpoint-log.json`
**Error Log**: `outputs/state/error-log.json`
**Per-Bank Status**: `outputs/phase-[N]/[bank]/status.json`

**Before starting**: Initialize workflow-state.json (see section below)

---

## Single Bank Workflow (Per Bank)

For each bank, execute this sequence using Task tool to spawn agents:

### Stage 1: Initialize Bank

**Action**: Create bank status.json and load configuration

**From**: `config/bank-manifest.json`

**Create**: `outputs/phase-[N]/[bank]/status.json`

```json
{
  "bank_id": "deutsche-bank",
  "bank_name": "Deutsche Bank AG",
  "phase": 1,
  "execution_tier": "A",
  "current_probability": {
    "architect": 0.40,
    "pragmatist": 0.60
  },
  "stages_completed": [],
  "current_stage": "pre-mortem",
  "classification": null,
  "confidence": null,
  "blocked_at": null,
  "started_at": "2025-12-18T10:00:00Z",
  "errors": []
}
```

### Stage 2: Pre-Mortem Gate

**Agent**: Reasoning Gate Agent
**Input**: Bank configuration, execution tier
**Output**: `outputs/phase-[N]/[bank]/3-gates/pre-mortem.md`

**Spawn**:
```
Task tool, subagent_type="general-purpose", model="opus"
Read: config/agent-prompts/reasoning-gate.md
Read: config/bank-manifest.json (for bank context)
Prompt: "Complete Pre-Mortem Gate for [bank-name]. Use execution tier [A/B/C] template..."
```

**Checkpoint**: AUTO-PROCEED (log to checkpoint-log.json)

**Update**: status.json stages_completed += "pre-mortem"

### Stage 3: Tier 1 Evidence Gathering

**Agent**: Evidence Gatherer Agent
**Input**: Bank configuration, tier=1, execution tier
**Output**: `outputs/phase-[N]/[bank]/1-evidence/tier1-evidence.md`, `null-results.md`

**Spawn**:
```
Task tool, subagent_type="general-purpose", model="opus"
Read: config/agent-prompts/evidence-gatherer.md
Read: config/bank-manifest.json (bank context)
Prompt: "Execute Tier 1 evidence gathering for [bank-name]..."
Include: Bank-specific search questions, known evidence, hypothesis
```

**Validation After**:
- Verify tier1-evidence.md exists
- Count evidence blocks (warn if < 3)
- Verify null-results.md exists (warn if empty)

**Update**: status.json stages_completed += "tier1-evidence"

### Stage 4: Bayesian Update T1

**Agent**: Bayesian Analyst Agent
**Input**: Prior (from status.json), tier1-evidence.md, bayesian-lr-tables.json
**Output**: `outputs/phase-[N]/[bank]/2-bayesian/post-tier1-update.md`

**Spawn**:
```
Task tool, subagent_type="general-purpose", model="opus"
Read: config/agent-prompts/bayesian-analyst.md
Read: config/bayesian-lr-tables.json
Read: outputs/phase-[N]/[bank]/1-evidence/tier1-evidence.md
Read: outputs/phase-[N]/[bank]/status.json (for prior)
Prompt: "Perform Bayesian update after Tier 1 for [bank-name]..."
Enable thinking mode: YES
```

**Validation After**:
- Verify 0 <= P(Architect) <= 1
- Verify P(Architect) + P(Pragmatist) ≈ 1.0 (±0.02)
- If combined LR > 100 or < 0.01 → BLOCK

**Update**: status.json current_probability, stages_completed += "bayesian-t1"

### Stage 5: Reasoning Gate 1

**Agent**: Reasoning Gate Agent
**Input**: All evidence so far, current probability, execution tier
**Output**: `outputs/phase-[N]/[bank]/3-gates/gate-1.md`

**Spawn**:
```
Task tool, subagent_type="general-purpose", model="opus"
Read: config/agent-prompts/reasoning-gate.md
Read: outputs/phase-[N]/[bank]/1-evidence/tier1-evidence.md
Read: outputs/phase-[N]/[bank]/2-bayesian/post-tier1-update.md
Prompt: "Complete Reasoning Gate 1 for [bank-name]..."
Enable thinking mode: YES
```

**Checkpoint**: AUTO-PROCEED

**Decision Point**:
- Read gate-1.md for proceeding decision
- If P(Architect) > 80% OR P(Pragmatist) > 80%: **SKIP to Stage 12 (Adversarial)**
- Else: Continue to Stage 6

**Update**: status.json stages_completed += "gate-1"

### Stage 6-8: Tier 2 (If Not Skipped)

Repeat pattern:
- Evidence Gathering (Tier 2)
- Bayesian Update T2
- Reasoning Gate 2

**Decision Point after Gate 2**:
- If P > 80%: SKIP to Adversarial
- Else: Continue to Tier 3

### Stage 9-11: Tier 3 (If Not Skipped)

Repeat pattern:
- Evidence Gathering (Tier 3)
- Bayesian Update T3
- Reasoning Gate 3

**After Gate 3**: Always proceed to Adversarial (no more evidence tiers)

### Stage 12: Adversarial Challenge

**Agent**: Adversarial Challenger Agent
**Input**: All evidence, current probability, execution tier
**Output**: `outputs/phase-[N]/[bank]/4-adversarial/` (counter-case.md, verdict.md, etc.)

**Spawn**:
```
Task tool, subagent_type="general-purpose", model="opus"
Read: config/agent-prompts/adversarial-challenger.md
Read: All evidence files
Read: All bayesian update files
Read: All gate files
Prompt: "Execute [Tier A/B/C] adversarial challenge for [bank-name]..."
Enable thinking mode: YES
```

**Checkpoint Decision**:
- Read verdict.md for verdict type
- If verdict = "REVISED" → **BLOCK** for human review
- If major contradiction detected → **BLOCK**
- Else: AUTO-PROCEED

**Update**: status.json stages_completed += "adversarial", apply confidence adjustment from verdict

### Stage 13: CHECKPOINT - Final Classification

**BLOCK for Human Approval** (Always)

**Prompt User**:
```
Bank: [bank-name]
Classification: [ARCHITECT/PRAGMATIST] ([variant])
Confidence: [X]%
Current Probability: P(Architect) = [Y]%

Please review the complete reasoning chain and approve classification.

Options:
1. Approve classification and confidence
2. Approve classification but adjust confidence
3. Change classification
4. Request additional evidence gathering
```

**Wait for User Decision**

**Actions Based on Decision**:
- Option 1: Proceed to synthesis
- Option 2: Update confidence in status.json, proceed
- Option 3: Update classification in status.json, proceed
- Option 4: Return to evidence gathering stage specified

**Log**: checkpoint-log.json with decision

### Stage 14: Synthesis

**Agent**: Synthesis Agent
**Input**: All files from stages 1-13, approved classification
**Output**: `outputs/phase-[N]/[bank]/5-synthesis/assessment.md`, `framework-integration.md`

**Spawn**:
```
Task tool, subagent_type="general-purpose", model="opus"
Read: config/agent-prompts/synthesis.md
Read: templates/per-bank-output.md (597-line template)
Read: templates/framework-integration.md
Read: All evidence files
Read: All bayesian files
Read: All gate files
Read: Adversarial files
Read: status.json (approved classification)
Prompt: "Complete final synthesis for [bank-name]..."
Enable thinking mode: YES
```

**Validation After**:
- Verify assessment.md matches template structure (19 sections)
- Verify framework-integration.md created
- Verify all mandatory sections complete

**Update**: status.json stages_completed += "synthesis", mark bank complete

### Stage 15: Bank Complete

**Action**: Mark bank complete in workflow-state.json

**Update**:
- workflow-state.json: banks_completed += bank-id
- workflow-state.json: current_bank = next bank in queue
- status.json: completed_at timestamp

**Log**: Completion to checkpoint-log.json

---

## Phase-Level Workflow

After all banks in phase complete:

### Phase Synthesis & QA

**Agent**: QA Validator Agent
**Input**: All bank assessments from phase
**Output**: `outputs/qa/phase-[N]-consistency.md`, `outputs/phase-[N]/phase-synthesis.md`

**Spawn**:
```
Task tool, subagent_type="general-purpose", model="opus"
Read: config/agent-prompts/qa-validator.md
Read: All assessment.md files from phase
Read: config/bank-manifest.json (anchor points)
Prompt: "Execute cross-bank QA validation for Phase [N]..."
Enable thinking mode: YES
```

**Checkpoint Decision**:
- Read phase-[N]-consistency.md
- If any test FAILED → **BLOCK** for human review
- Provide: List of inconsistencies, recommended actions
- Wait for resolution
- Else: AUTO-PROCEED

**Update**: workflow-state.json phase-[N] status = "complete"

**Proceed**: To next phase

---

## Full Rollout Sequence

**Execute phases sequentially**:

```
Phase 1: European Tier 1 (5 banks, Tier A)
  → Execute banks: Barclays, HSBC, Société Générale, Deutsche Bank, UBS
  → Phase synthesis + QA validation
  → Checkpoint: Review consistency

Phase 2: UK Regional (2 banks, Tier B)
  → Execute banks: NatWest, Lloyds
  → Phase synthesis + QA validation

Phase 3: Japanese (4 banks, Tier B)
  → Execute banks: Nomura, MUFG, Mizuho, SMBC
  → Phase synthesis + QA validation

Phase 4: Other European (4 banks, Tier C)
  → Execute banks: ING, Crédit Agricole, UniCredit, Commerzbank
  → Phase synthesis + QA validation

Phase 5: Spanish (2 banks, Tier C)
  → Execute banks: Santander, BBVA
  → Phase synthesis + QA validation

Phase 6: Deep Dives (2 banks, Tier B)
  → Execute banks: Standard Chartered, Pictet
  → Phase synthesis + QA validation

Phase 7: Emerging Markets (5 banks, Tier C)
  → Execute banks: DBS, ICBC, Bank of China, CCB, ABC
  → Phase synthesis + QA validation
```

**After All Phases**:

### Final Cross-Bank Analysis

**Agent**: QA Validator Agent
**Input**: All 24 bank assessments, all 7 phase syntheses
**Output**: `outputs/final/cross-bank-patterns.md`

**Spawn**:
```
Task tool, subagent_type="general-purpose", model="opus"
Read: config/agent-prompts/qa-validator.md
Read: templates/cross-bank-patterns.md (8-part template)
Read: All assessment.md files (24 banks)
Read: All phase synthesis files
Prompt: "Execute final cross-bank pattern analysis for all 24 banks..."
Enable thinking mode: YES
```

**Output**: 8-part analysis with hypothesis tests, confidence gaps, framework insights

**Also Generate**:
- `outputs/final/classification-table.md` - Summary table of all banks
- `outputs/final/validation-priorities.md` - Banks flagged for validation
- `outputs/final/framework-narrative.md` - Framework update recommendations

---

## State Management

### Initialize Workflow State

**Before starting**, create `outputs/state/workflow-state.json`:

```json
{
  "execution_mode": "single_bank_test",
  "current_phase": 1,
  "current_bank": "deutsche-bank",
  "current_stage": "initialize",
  "banks_completed": [],
  "banks_in_progress": [],
  "banks_pending": ["societe-generale", "ubs", "barclays", "hsbc"],
  "phase_status": {
    "1": "in_progress",
    "2": "pending",
    "3": "pending",
    "4": "pending",
    "5": "pending",
    "6": "pending",
    "7": "pending"
  },
  "blocked_checkpoints": [],
  "last_updated": "2025-12-18T10:00:00Z",
  "started_at": "2025-12-18T10:00:00Z",
  "execution_log": []
}
```

### Update After Each Stage

**Pattern**:
1. Read workflow-state.json
2. Update relevant fields
3. Append to execution_log
4. Update last_updated timestamp
5. Write back to file

### Checkpoint Logging

**File**: `outputs/state/checkpoint-log.json`

**Entry Format**:
```json
{
  "timestamp": "2025-12-18T10:30:00Z",
  "bank_id": "deutsche-bank",
  "checkpoint_id": "final_classification",
  "checkpoint_name": "Final Classification Approval",
  "action": "BLOCK",
  "condition_met": "always",
  "human_decision": "approved",
  "classification": "PRAGMATIST",
  "confidence": 85,
  "rationale": "User approved classification after review"
}
```

### Error Logging

**File**: `outputs/state/error-log.json`

**Entry Format**:
```json
{
  "timestamp": "2025-12-18T11:00:00Z",
  "bank_id": "deutsche-bank",
  "stage": "bayesian-t1",
  "error_type": "agent_failure",
  "error_message": "Agent failed to produce post-tier1-update.md",
  "retry_attempted": true,
  "retry_successful": false,
  "resolution": "Manual intervention required"
}
```

---

## Error Handling

### Agent Failure

If agent fails to produce expected output:
1. Log error to error-log.json
2. Retry once with same parameters
3. If retry fails → BLOCK and alert user
4. User options: Skip stage, Manual completion, Modify parameters

### Interruption Recovery

If execution interrupted:
1. Read workflow-state.json
2. Read status.json for current bank
3. Resume from current_stage
4. If stage partially complete → retry stage

### State Corruption

Before each write:
1. Backup current state → workflow-state.backup.json
2. Write new state
3. Verify write succeeded
4. If failed → restore from backup

---

## Validation Checks

**Before advancing from any stage**:

1. **File Existence**: Verify expected output file exists
2. **File Completeness**: Check required sections present
3. **Probability Sanity**: Verify 0 <= P <= 1, sum ≈ 1
4. **Evidence Count**: Warn if < 3 evidence blocks
5. **Null Documentation**: Warn if no null results
6. **Gate Completeness**: All required sections filled

**If validation fails**: BLOCK and require resolution

---

## Human Checkpoints Summary

**AUTO-PROCEED** (log but don't wait):
- Pre-Mortem Gate
- Reasoning Gates 1, 2, 3
- Bayesian Updates
- Adversarial Verdict (unless REVISED)

**BLOCK** (wait for human decision):
- Major contradictions
- Classification changes from adversarial
- **Final classification** (always)
- Low confidence (< 50%)
- Cross-bank consistency failures
- Anchor point violations
- Extreme LRs (>100 or <0.01)

---

## Execution Commands

### Single Bank Test

**Command**: Start with Deutsche Bank only

**Execution**:
1. Set workflow-state.json: execution_mode = "single_bank_test"
2. Set current_bank = "deutsche-bank"
3. Set banks_pending = []
4. Execute stages 1-15 for Deutsche Bank
5. Stop after synthesis complete
6. Validate all outputs
7. If successful → proceed to phase pilot

### Phase Pilot

**Command**: Execute Phase 1 (5 banks)

**Execution**:
1. Set workflow-state.json: execution_mode = "phase_pilot"
2. Set banks_pending = ["barclays", "hsbc", "societe-generale", "deutsche-bank", "ubs"]
3. Execute stages 1-15 for each bank sequentially
4. Execute phase synthesis + QA validation
5. Stop after phase complete
6. If successful → proceed to full rollout

### Full Rollout

**Command**: Execute all 7 phases

**Execution**:
1. Set workflow-state.json: execution_mode = "full_rollout"
2. Load all 24 banks from bank-manifest.json
3. Execute phases 1-7 sequentially
4. Execute phase synthesis after each phase
5. Execute final cross-bank analysis
6. Generate all deliverables

---

## Success Criteria

**Single Bank Test Passes If**:
- [ ] All 14+ output files generated for Deutsche Bank
- [ ] assessment.md matches 597-line template
- [ ] Bayesian calculations correct (spot-check)
- [ ] All gates completed
- [ ] Adversarial protocol executed
- [ ] Checkpoints worked correctly

**Phase Pilot Passes If**:
- [ ] All 5 banks completed
- [ ] Phase synthesis generated
- [ ] QA validation: all tests PASS
- [ ] Cross-bank consistency verified

**Full Rollout Succeeds If**:
- [ ] All 24 banks completed
- [ ] All 7 phase syntheses generated
- [ ] Final cross-bank analysis complete
- [ ] All deliverables in outputs/final/

---

## Time Tracking

| Phase | Banks | Estimated Time | Actual Time |
|-------|-------|----------------|-------------|
| Test (Deutsche Bank) | 1 | 1.5 hours | ___ |
| Phase 1 | 5 | 4.5 hours | ___ |
| Phase 2 | 2 | 1.75 hours | ___ |
| Phase 3 | 4 | 3.25 hours | ___ |
| Phase 4 | 4 | 2.25 hours | ___ |
| Phase 5 | 2 | 1.2 hours | ___ |
| Phase 6 | 2 | 1.75 hours | ___ |
| Phase 7 | 5 | 1.75 hours | ___ |
| Final Analysis | - | 1 hour | ___ |
| **Total** | **24** | **~18-20 hours** | ___ |

*Includes human review time at checkpoints*

---

## Next Step

**Execute Single Bank Test** using this workflow to validate the complete system before full rollout.

Bank: Deutsche Bank (Tier A)
Expected Time: 1.5 hours
Validation Criteria: All outputs complete, checkpoints functional
