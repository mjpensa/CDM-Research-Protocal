# Optimized Prompt for Critical Break Detection

## Context Summary

Based on exploration of your research platform, I've identified the key systems and their potential failure points. The prompt below is engineered to systematically validate these systems for autonomous overnight batch execution.

---

## Engineered Prompt

```
You are auditing a research platform designed for autonomous overnight batch runs. Your task is to identify CRITICAL BREAKS that would prevent unattended execution across all 31 banks.

## CONTEXT
- Platform: CDM/DRR Bank Research Protocol
- Runtime: Claude Code Opus 4.5 in VS Code (Max plan with web search)
- Mode: Autonomous overnight batch processing, human reviews output next morning
- Requirement: All banks must receive identical analytical rigor

## CRITICAL BREAK CATEGORIES (Check in Order)

### 1. BATCH RESUMABILITY (HIGHEST PRIORITY)
Verify the platform can resume mid-batch after crash/restart:

- [ ] Does `batch_orchestrate.py` check if a bank is already completed before processing?
- [ ] Is there a global completion registry that survives process restart?
- [ ] Can the system identify which bank was in-progress when a crash occurred?
- [ ] After restart, does it skip completed banks and resume the in-progress bank at the correct stage?

**Files to check**: `tools/batch_orchestrate.py`, `tools/state_manager.py`, `outputs/state/workflow-state.json` schema

### 2. SILENT ERROR PROPAGATION
Verify errors surface properly and don't create phantom "success":

- [ ] When a bank fails mid-processing, is this surfaced in the batch summary?
- [ ] Does `execute_bank_research()` in batch_orchestrate.py propagate errors or swallow them?
- [ ] Is there a failure count threshold that halts the batch (e.g., 3+ consecutive failures)?
- [ ] Are API errors (rate limits, timeouts) logged AND cause the bank to be marked for retry?

**Files to check**: `tools/batch_orchestrate.py` (error handling in execute_bank_research), `tools/research_executor.py`

### 3. INTRA-STAGE CHECKPOINTING
Verify work isn't lost during long-running stages:

- [ ] Does evidence gathering checkpoint after each search, or only after the entire tier?
- [ ] If process crashes during search 12 of 20, are searches 1-11 preserved?
- [ ] Is `evidence.json` written incrementally or only at stage completion?

**Files to check**: `tools/research_executor.py`, evidence gathering flow

### 4. STATE CONSISTENCY
Verify no state divergence between the three state systems:

- [ ] Do `orchestrate.py`, `batch_orchestrate.py`, and `workflow.py` read/write the same state files?
- [ ] Is there a single source of truth for "is bank X complete"?
- [ ] After a crash, which state file determines resumption point?
- [ ] Are `status.json` (per-bank) and `workflow-state.json` (global) kept in sync?

**Files to check**: `tools/orchestrate.py`, `tools/batch_orchestrate.py`, `tools/orchestrator/workflow.py`, `tools/state_manager.py`

### 5. LOCK CONTENTION & DEADLOCKS
Verify parallel workers don't block each other:

- [ ] Is the 10-minute stale lock threshold appropriate for overnight runs?
- [ ] Can parallel workers (default: 3) all access `workflow-state.json` without contention?
- [ ] If worker A holds a lock and crashes, can worker B recover within reasonable time?
- [ ] Is there a maximum retry count for lock acquisition?

**Files to check**: `tools/state_manager.py` (_file_lock, _handle_stale_lock)

### 6. IDEMPOTENCY
Verify re-runs don't corrupt data:

- [ ] If the same stage runs twice (due to crash before completion marker), are evidence IDs duplicated?
- [ ] Does evidence gathering check for existing IDs before appending?
- [ ] Is there deduplication logic in `evidence.json` processing?

**Files to check**: Evidence gatherer logic, `tools/process_evidence.py`

### 7. EQUAL RIGOR GUARANTEE
Verify all banks receive identical treatment:

- [ ] Are the same prompts used for all banks (check prompt_assembler.py)?
- [ ] Are decision thresholds loaded from config (not hardcoded)?
- [ ] Is skip logic (P>80%) applied uniformly?
- [ ] Do errors in one bank affect processing of subsequent banks?

**Files to check**: `tools/orchestrator/prompt_assembler.py`, `config/decision-thresholds.json` loading

### 8. HUMAN REVIEW QUEUE INTEGRITY
Verify edge cases are properly queued for morning review:

- [ ] Is `review-queue.json` written atomically?
- [ ] If batch crashes after queuing items but before completion, is queue preserved?
- [ ] Are all 8 review triggers evaluated for every bank?
- [ ] Does the queue contain enough context for human to review without re-running?

**Files to check**: `tools/batch_orchestrate.py` (ReviewQueue class), `outputs/state/review-queue.json` schema

## OUTPUT FORMAT

For each category, report:
1. **STATUS**: PASS / FAIL / PARTIAL
2. **EVIDENCE**: Specific file:line references
3. **BREAK SEVERITY**: CRITICAL (blocks overnight run) / HIGH (causes data issues) / MEDIUM (degrades quality)
4. **RECOMMENDED FIX**: One-line description if FAIL

## PRIORITY ORDER
Execute checks in order 1-8. Stop and report if you find a CRITICAL break in categories 1-4.

## VERIFICATION METHOD
- Read the actual code, don't assume from function names
- Check both happy path and error paths
- Look for try/except blocks that swallow exceptions
- Verify config values are loaded dynamically, not hardcoded
```

---

## Key Vulnerabilities Identified During Exploration

| Category | Vulnerability | Severity | Current State |
|----------|--------------|----------|---------------|
| Batch Resumability | No global completion tracking | CRITICAL | batch_orchestrate.py processes all banks, doesn't skip completed |
| Silent Errors | Exception caught but only logged | CRITICAL | Batch shows success even with failed banks |
| Intra-stage Checkpoints | State saved only after stage complete | HIGH | Multi-hour tier collection lost on crash |
| State Consistency | 3 separate state systems | HIGH | No clear source of truth on recovery |
| Lock Contention | 10-min stale lock threshold | MEDIUM | Could cause hangs on restart |
| Idempotency | No duplicate ID prevention | HIGH | Re-running stage creates duplicate evidence |

---

## Usage Instructions

1. Copy the prompt above into a new Claude Code session
2. Execute with: "Run this audit on the codebase"
3. Claude will systematically check each category
4. Focus first on any CRITICAL findings in categories 1-4
5. Address those before running overnight batch

---

## Quick Reference: Files to Audit

| File | Critical Checks |
|------|-----------------|
| `tools/batch_orchestrate.py` | Bank completion check, error handling, review queue |
| `tools/state_manager.py` | Lock handling, atomic writes, state validation |
| `tools/research_executor.py` | Intra-stage checkpointing, evidence persistence |
| `tools/orchestrate.py` | Stage progression, state file writes |
| `tools/orchestrator/workflow.py` | State integration, skip logic |
| `config/decision-thresholds.json` | Threshold values are loaded (not hardcoded) |
