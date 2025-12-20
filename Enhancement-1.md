# Enhancement 1: Operationalize CDM Research Protocol

## Overview

**Goal:** Complete the CDM/DRR research tool so it can execute end-to-end on all 31 banks across 9 phases.

**Current State:** 40% automated, 60% manual. Strong methodology, incomplete execution layer.

**Target State:** Fully operational tool that can process banks with minimal human intervention (only at mandatory BLOCK checkpoints).

**Estimated Effort:** 10-14 days

**Implementation Approach:** Full implementation - complete all phases before testing

**Checkpoint Handling:** Queue for batch review - log blocks to `review-queue.json`, continue processing other banks, review all blocks in batch session

---

## Critical Gaps to Fix

| Gap | Severity | Root Cause | Impact |
|-----|----------|------------|--------|
| Missing `anthropic` dependency | CRITICAL | Not in requirements.txt | Import crash on line 47 of research_executor.py |
| No master orchestration loop | CRITICAL | 5 separate orchestrators don't coordinate | State conflicts, gates ignored |
| State not persisted across tiers | CRITICAL | Each module creates own state | Loses probability updates between tiers |
| Gate enforcement missing | HIGH | Skip logic defined but not wired | Runs all tiers regardless of probability |
| Resume/retry logic missing | HIGH | No checkpoint recovery | Fails mid-batch require full restart |
| Markdown/JSON reconciliation | MEDIUM | Two formats, no sync | Evidence drift between formats |

---

## Implementation Tasks

### Phase 1: Fix Critical Dependencies (Day 1)

#### Task 1.1: Update requirements.txt
**File:** `requirements.txt`

```
requests>=2.28.0
jsonschema>=4.0.0
anthropic>=0.40.0
pytest>=7.0.0
```

**Validation:** `pip install -r requirements.txt` succeeds

---

#### Task 1.2: Add API configuration
**File:** `config/api-config.json` (NEW)

```json
{
  "model": "claude-opus-4-5-20250101",
  "fallback_model": "claude-sonnet-4-20250514",
  "max_retries": 3,
  "retry_delay_seconds": 5,
  "timeout_seconds": 300,
  "rate_limit_requests_per_minute": 50
}
```

**Update:** `research_executor.py` lines 105, 121 to load from config instead of hardcoding

---

### Phase 2: Unify State Management (Days 2-4)

#### Task 2.1: Create unified state manager
**File:** `tools/state_manager.py` (NEW, ~250 lines)

```python
class UnifiedStateManager:
    """Single source of truth for all workflow state."""

    def __init__(self, outputs_dir: Path):
        self.workflow_state_path = outputs_dir / "state" / "workflow-state.json"
        self.checkpoint_log_path = outputs_dir / "state" / "checkpoint-log.json"
        self.error_log_path = outputs_dir / "state" / "error-log.json"

    def load_bank_state(self, bank_id: str, phase: int) -> BankState
    def save_bank_state(self, state: BankState) -> None
    def update_probability(self, bank_id: str, p_architect: float, stage: str) -> None
    def mark_stage_complete(self, bank_id: str, stage: str) -> None
    def get_next_stage(self, bank_id: str) -> str
    def should_skip_to_adversarial(self, bank_id: str) -> bool
    def log_checkpoint(self, checkpoint: CheckpointEvent) -> None
    def log_error(self, error: ErrorEvent) -> None
    def get_incomplete_banks(self) -> List[str]
    def get_blocked_banks(self) -> List[str]
```

**Key Design:**
- Atomic writes (write to temp, rename)
- Lock file for concurrent access
- State validation on load/save
- Provenance tracking built-in

---

#### Task 2.2: Define unified state schema
**File:** `tools/state_schema.py` (NEW, ~100 lines)

```python
@dataclass
class BankState:
    bank_id: str
    bank_name: str
    phase: int
    execution_tier: str  # A, B, C

    # Probability tracking
    prior_probability: float
    current_probability: float
    probability_history: List[ProbabilityUpdate]

    # Stage tracking
    stages_completed: List[str]
    current_stage: str
    skipped_stages: List[str]

    # Classification
    classification: Optional[str]
    classification_variant: Optional[str]
    confidence: Optional[float]

    # Timestamps
    started_at: datetime
    last_updated: datetime
    completed_at: Optional[datetime]

    # Blocking
    blocked_at: Optional[str]
    blocked_reason: Optional[str]

    # Evidence tracking
    evidence_counts: Dict[str, int]  # tier1: 5, tier2: 3, tier3: 0, null: 7

    # Errors
    errors: List[str]

@dataclass
class ProbabilityUpdate:
    stage: str
    prior: float
    posterior: float
    combined_lr: float
    evidence_count: int
    timestamp: datetime
```

---

#### Task 2.3: Integrate state manager into existing tools

**Files to modify:**

| File | Changes |
|------|---------|
| `research_executor.py` | Replace `ResearchState` with `UnifiedStateManager` calls |
| `batch_orchestrate.py` | Remove local state, use `UnifiedStateManager` |
| `orchestrate.py` | Deprecate `WorkflowState`, delegate to `UnifiedStateManager` |
| `auto_orchestrate.py` | Use `UnifiedStateManager` for state reads |
| `run_pipeline.py` | Add state validation calls |

**Critical changes in `research_executor.py`:**
- Line 81-100: Remove `ResearchState` dataclass
- Line 518: Initialize via `UnifiedStateManager.load_bank_state()`
- Line 632-636: Call `state_manager.update_probability()` after parsing
- Line 703-704: Call `state_manager.save_bank_state()` instead of direct write

---

### Phase 3: Implement Gate Enforcement (Days 5-6)

#### Task 3.1: Create gate enforcer
**File:** `tools/gate_enforcer.py` (NEW, ~150 lines)

```python
class GateEnforcer:
    """Enforces reasoning gate decisions and skip logic."""

    def __init__(self, thresholds: dict, state_manager: UnifiedStateManager):
        self.skip_threshold = thresholds["skip_to_adversarial_threshold"]  # 80
        self.low_confidence_block = thresholds["low_confidence_block"]  # 50
        self.uncertainty_range = (40, 60)

    def should_skip_tier(self, current_probability: float, tier: int) -> bool:
        """Returns True if probability exceeds skip threshold."""
        return current_probability > self.skip_threshold or \
               current_probability < (100 - self.skip_threshold)

    def get_next_stage(self, bank_state: BankState) -> str:
        """Determines next stage respecting skip logic."""
        current = bank_state.current_stage
        prob = bank_state.current_probability

        # After any gate, check skip condition
        if current.startswith("gate_") and self.should_skip_tier(prob, ...):
            return "adversarial_challenge"

        return STAGE_SEQUENCE[STAGE_SEQUENCE.index(current) + 1]

    def check_block_condition(self, bank_state: BankState, checkpoint: str) -> Optional[str]:
        """Returns block reason if checkpoint should block, None otherwise."""
        if checkpoint == "final_classification":
            return "Final classification requires human approval"
        if checkpoint == "low_confidence" and bank_state.confidence < self.low_confidence_block:
            return f"Confidence {bank_state.confidence}% below threshold {self.low_confidence_block}%"
        # ... other block conditions
        return None
```

---

#### Task 3.2: Wire gate enforcer into research flow

**File:** `research_executor.py`

**Changes at lines 589-621 (tier loop):**

```python
# BEFORE (current):
for tier in [1, 2, 3]:
    # Always executes all tiers

# AFTER (with gate enforcement):
for tier in [1, 2, 3]:
    # Check skip condition before each tier
    if tier > 1 and gate_enforcer.should_skip_tier(state.current_probability, tier):
        state_manager.mark_stage_skipped(bank_id, f"tier{tier}_evidence")
        state_manager.mark_stage_skipped(bank_id, f"bayesian_t{tier}")
        state_manager.mark_stage_skipped(bank_id, f"gate_{tier}")
        continue

    # Execute tier...
```

---

### Phase 4: Build Master Orchestration Loop (Days 7-9)

#### Task 4.1: Create master orchestrator
**File:** `tools/master_orchestrator.py` (NEW, ~400 lines)

```python
class MasterOrchestrator:
    """
    Single entry point for all research execution.
    Coordinates all agents, manages state, enforces checkpoints.
    """

    def __init__(self, config_dir: Path, outputs_dir: Path):
        self.state_manager = UnifiedStateManager(outputs_dir)
        self.gate_enforcer = GateEnforcer(load_thresholds(config_dir), self.state_manager)
        self.bank_manifest = load_bank_manifest(config_dir)
        self.checkpoint_rules = load_checkpoint_rules(config_dir)
        self.api_config = load_api_config(config_dir)

    def run_single_bank(self, bank_id: str, resume: bool = False) -> BankResult:
        """Execute full research protocol for one bank."""
        state = self._initialize_or_resume(bank_id, resume)

        while not self._is_complete(state):
            next_stage = self.gate_enforcer.get_next_stage(state)

            # Check for block before executing
            block_reason = self.gate_enforcer.check_block_condition(state, next_stage)
            if block_reason:
                self._handle_block(state, next_stage, block_reason)
                return BankResult(status="blocked", state=state)

            # Execute stage
            try:
                self._execute_stage(state, next_stage)
                self.state_manager.mark_stage_complete(bank_id, next_stage)
            except Exception as e:
                self._handle_error(state, next_stage, e)
                return BankResult(status="error", state=state)

        return BankResult(status="complete", state=state)

    def run_phase(self, phase: int, parallel: bool = False) -> PhaseResult:
        """Execute all banks in a phase."""
        banks = [b for b in self.bank_manifest if b["phase"] == phase]

        if parallel:
            with ThreadPoolExecutor(max_workers=3) as executor:
                results = list(executor.map(self.run_single_bank,
                                           [b["bank_id"] for b in banks]))
        else:
            results = [self.run_single_bank(b["bank_id"]) for b in banks]

        # Run phase synthesis if all complete
        if all(r.status == "complete" for r in results):
            self._run_phase_synthesis(phase)

        return PhaseResult(phase=phase, bank_results=results)

    def run_full_protocol(self) -> FullResult:
        """Execute all phases in sequence."""
        for phase in range(1, 10):
            result = self.run_phase(phase)
            if not result.all_complete:
                return FullResult(status="incomplete", completed_through=phase-1)

        self._run_cross_bank_analysis()
        return FullResult(status="complete")

    def resume_from_checkpoint(self) -> None:
        """Resume execution from last checkpoint."""
        incomplete = self.state_manager.get_incomplete_banks()
        blocked = self.state_manager.get_blocked_banks()

        # Handle blocked banks first (require user input)
        for bank_id in blocked:
            self._prompt_user_for_block_resolution(bank_id)

        # Resume incomplete banks
        for bank_id in incomplete:
            self.run_single_bank(bank_id, resume=True)
```

---

#### Task 4.2: Implement stage executors
**File:** `tools/stage_executors.py` (NEW, ~300 lines)

```python
class StageExecutor:
    """Executes individual stages and validates outputs."""

    def execute_pre_mortem(self, bank_id: str, bank_config: dict) -> Path:
        """Execute pre-mortem gate analysis."""
        prompt = self._load_agent_prompt("reasoning-gate.md")
        # ... call Claude API with pre-mortem template
        output_path = self._get_output_path(bank_id, "3-gates/pre-mortem.md")
        self._validate_gate_output(output_path)
        return output_path

    def execute_evidence_gathering(self, bank_id: str, tier: int) -> Path:
        """Execute evidence gathering for specified tier."""
        prompt = self._load_agent_prompt("evidence-gatherer.md")
        # ... call Claude API with tier-specific search strategy
        output_path = self._get_output_path(bank_id, f"1-evidence/tier{tier}-evidence.md")
        self._validate_evidence_output(output_path, tier)
        return output_path

    def execute_bayesian_update(self, bank_id: str, tier: int, prior: float) -> Tuple[Path, float]:
        """Execute Bayesian update and return new probability."""
        prompt = self._load_agent_prompt("bayesian-analyst.md")
        # ... call Claude API with evidence and LR tables
        output_path = self._get_output_path(bank_id, f"2-bayesian/post-tier{tier}-update.md")
        posterior = self._extract_probability(output_path)
        self._validate_bayesian_output(output_path, prior, posterior)
        return output_path, posterior

    def execute_reasoning_gate(self, bank_id: str, gate_num: int) -> Tuple[Path, str]:
        """Execute reasoning gate and return decision."""
        prompt = self._load_agent_prompt("reasoning-gate.md")
        # ... call Claude API with gate template
        output_path = self._get_output_path(bank_id, f"3-gates/gate-{gate_num}.md")
        decision = self._extract_gate_decision(output_path)
        return output_path, decision

    def execute_adversarial_challenge(self, bank_id: str) -> Tuple[List[Path], str]:
        """Execute full adversarial challenge protocol."""
        prompt = self._load_agent_prompt("adversarial-challenger.md")
        # ... call Claude API with adversarial template
        outputs = [
            self._get_output_path(bank_id, "4-adversarial/counter-case.md"),
            self._get_output_path(bank_id, "4-adversarial/disconfirming-searches.md"),
            self._get_output_path(bank_id, "4-adversarial/steelman.md"),
            self._get_output_path(bank_id, "4-adversarial/verdict.md"),
        ]
        verdict = self._extract_verdict(outputs[3])
        return outputs, verdict

    def execute_synthesis(self, bank_id: str, approved_classification: str) -> Path:
        """Execute synthesis agent to produce final assessment."""
        prompt = self._load_agent_prompt("synthesis.md")
        # ... call Claude API with all evidence and approved classification
        output_path = self._get_output_path(bank_id, "5-synthesis/assessment.md")
        self._validate_synthesis_output(output_path)
        return output_path
```

---

### Phase 5: Implement Resume/Retry Logic (Days 10-11)

#### Task 5.1: Add checkpoint recovery
**File:** `tools/checkpoint_recovery.py` (NEW, ~150 lines)

```python
class CheckpointRecovery:
    """Handles recovery from failures and resumption."""

    def __init__(self, state_manager: UnifiedStateManager):
        self.state_manager = state_manager

    def get_resume_point(self, bank_id: str) -> str:
        """Determine where to resume for a bank."""
        state = self.state_manager.load_bank_state(bank_id)

        if state.blocked_at:
            return state.blocked_at  # Resume at block point

        if state.errors:
            # Resume at last successful stage
            return state.stages_completed[-1] if state.stages_completed else "initialize"

        return state.current_stage

    def can_resume(self, bank_id: str) -> bool:
        """Check if bank has valid state to resume from."""
        try:
            state = self.state_manager.load_bank_state(bank_id)
            return state is not None and len(state.stages_completed) > 0
        except:
            return False

    def retry_failed_stage(self, bank_id: str, max_retries: int = 3) -> bool:
        """Retry the last failed stage with exponential backoff."""
        state = self.state_manager.load_bank_state(bank_id)
        failed_stage = state.current_stage

        for attempt in range(max_retries):
            try:
                # Re-execute failed stage
                self._execute_stage(bank_id, failed_stage)
                self.state_manager.clear_error(bank_id)
                return True
            except Exception as e:
                delay = 2 ** attempt * 5  # 5, 10, 20 seconds
                time.sleep(delay)
                self.state_manager.log_error(ErrorEvent(
                    bank_id=bank_id,
                    stage=failed_stage,
                    error=str(e),
                    attempt=attempt + 1
                ))

        return False
```

---

#### Task 5.2: Add batch review queue system
**File:** `tools/review_queue.py` (NEW, ~200 lines)

```python
class ReviewQueue:
    """
    Manages BLOCK checkpoints in batch mode.
    Banks continue processing; blocks queued for later review.
    """

    def __init__(self, state_manager: UnifiedStateManager):
        self.state_manager = state_manager
        self.queue_path = Path("outputs/state/review-queue.json")

    def add_block(self, bank_id: str, checkpoint: str, reason: str,
                  provisional_classification: str, confidence: float) -> None:
        """Queue a block for later batch review."""
        item = ReviewItem(
            bank_id=bank_id,
            checkpoint=checkpoint,
            reason=reason,
            provisional_classification=provisional_classification,
            provisional_confidence=confidence,
            timestamp=datetime.now().isoformat(),
            status="pending"
        )
        self._append_to_queue(item)

    def get_pending_reviews(self) -> List[ReviewItem]:
        """Get all pending review items."""
        queue = self._load_queue()
        return [item for item in queue["items"] if item["status"] == "pending"]

    def run_batch_review(self) -> None:
        """Interactive batch review session."""
        pending = self.get_pending_reviews()
        print(f"\n{'='*60}")
        print(f"BATCH REVIEW SESSION: {len(pending)} items pending")
        print(f"{'='*60}\n")

        for i, item in enumerate(pending, 1):
            print(f"\n[{i}/{len(pending)}] {item['bank_id']}")
            print(f"  Checkpoint: {item['checkpoint']}")
            print(f"  Reason: {item['reason']}")
            print(f"  Provisional: {item['provisional_classification']} "
                  f"({item['provisional_confidence']}%)")
            print(f"\n  Options:")
            print(f"    [A] Approve as-is")
            print(f"    [M] Modify classification/confidence")
            print(f"    [R] Request more research")
            print(f"    [S] Skip (keep pending)")

            choice = input("\n  Decision: ").strip().upper()
            self._process_decision(item, choice)

    def generate_review_report(self) -> str:
        """Generate markdown report of all pending reviews."""
        pending = self.get_pending_reviews()
        # Returns formatted markdown for review
```

---

#### Task 5.3: Add batch recovery CLI
**File:** `tools/recovery_cli.py` (NEW, ~100 lines)

```python
def main():
    parser = argparse.ArgumentParser(description="Recovery CLI for CDM Research")
    parser.add_argument("command", choices=["status", "resume", "retry", "review"])
    parser.add_argument("--bank", help="Specific bank to operate on")
    parser.add_argument("--phase", type=int, help="Phase to operate on")
    parser.add_argument("--force", action="store_true", help="Force operation")

    args = parser.parse_args()

    if args.command == "status":
        show_workflow_status()
    elif args.command == "resume":
        resume_incomplete_banks(args.bank, args.phase)
    elif args.command == "retry":
        retry_failed_banks(args.bank)
    elif args.command == "review":
        # Launch batch review session for all pending blocks
        ReviewQueue(UnifiedStateManager()).run_batch_review()
```

---

### Phase 6: Integration & Testing (Days 12-14)

#### Task 6.1: Create integration test suite
**File:** `tools/tests/test_integration.py` (NEW, ~200 lines)

```python
class TestFullPipeline:
    """Integration tests for complete pipeline."""

    def test_single_bank_happy_path(self):
        """Test complete execution for one bank (Deutsche Bank)."""
        orchestrator = MasterOrchestrator(CONFIG_DIR, TEST_OUTPUTS_DIR)
        result = orchestrator.run_single_bank("deutsche-bank")

        assert result.status == "complete"
        assert result.state.classification in ["ARCHITECT", "PRAGMATIST"]
        assert 0 < result.state.confidence <= 100
        assert len(result.state.stages_completed) >= 10

    def test_gate_skip_logic(self):
        """Test that high probability triggers skip to adversarial."""
        # Mock probability > 80% after Tier 1
        # Verify Tier 2 and 3 are skipped

    def test_block_checkpoint_triggers(self):
        """Test that BLOCK checkpoints halt execution."""
        # Verify final_classification always blocks
        # Verify low_confidence blocks when < 50%

    def test_resume_from_checkpoint(self):
        """Test resumption after interruption."""
        # Start bank, interrupt mid-tier
        # Resume and verify continues from correct point

    def test_state_persistence(self):
        """Test that state survives process restart."""
        # Execute partial, kill process
        # Restart and verify state intact
```

---

#### Task 6.2: Create end-to-end validation script
**File:** `tools/validate_e2e.py` (NEW, ~100 lines)

```python
def validate_bank_outputs(bank_id: str) -> ValidationResult:
    """Validate all outputs for a completed bank."""
    checks = [
        check_all_required_files_exist(bank_id),
        check_evidence_schema_compliance(bank_id),
        check_bayesian_math_correct(bank_id),
        check_gates_complete(bank_id),
        check_adversarial_complete(bank_id),
        check_synthesis_sections(bank_id),
        check_state_consistency(bank_id),
    ]

    return ValidationResult(
        bank_id=bank_id,
        passed=all(c.passed for c in checks),
        checks=checks
    )
```

---

## Files to Create (Summary)

| File | Lines | Purpose |
|------|-------|---------|
| `tools/state_manager.py` | ~250 | Unified state management |
| `tools/state_schema.py` | ~100 | State dataclasses |
| `tools/gate_enforcer.py` | ~150 | Gate decision logic |
| `tools/master_orchestrator.py` | ~400 | Main execution loop |
| `tools/stage_executors.py` | ~300 | Individual stage execution |
| `tools/checkpoint_recovery.py` | ~150 | Resume/retry logic |
| `tools/review_queue.py` | ~200 | Batch review queue system |
| `tools/recovery_cli.py` | ~100 | CLI for recovery operations |
| `config/api-config.json` | ~15 | API configuration |
| `tools/tests/test_integration.py` | ~200 | Integration tests |
| `tools/validate_e2e.py` | ~100 | E2E validation |
| **TOTAL** | **~1,965** | |

---

## Files to Modify (Summary)

| File | Changes |
|------|---------|
| `requirements.txt` | Add `anthropic>=0.40.0`, `pytest>=7.0.0` |
| `research_executor.py` | Replace local state with UnifiedStateManager, add gate checks |
| `batch_orchestrate.py` | Delegate to MasterOrchestrator |
| `orchestrate.py` | Deprecate in favor of MasterOrchestrator |
| `run_pipeline.py` | Add state validation, integrate gate enforcer |

---

## Validation Criteria

### Must Pass Before Complete:

1. **Single Bank Test (Deutsche Bank)**
   - [ ] All 15+ output files generated
   - [ ] assessment.md has all 19 sections
   - [ ] Bayesian math validates (P(A) + P(P) = 1.0 +/-0.02)
   - [ ] State persists across stages
   - [ ] Gates enforce skip logic correctly

2. **Phase 1 Pilot (5 banks)**
   - [ ] All 5 banks complete without manual intervention (except final classification)
   - [ ] Phase synthesis generated
   - [ ] Cross-bank consistency tests pass
   - [ ] No state conflicts between banks

3. **Resume Test**
   - [ ] Interrupt mid-execution, resume successfully
   - [ ] State intact after process kill
   - [ ] Retry logic handles transient API failures

---

## Execution Order

```
Day 1:    Phase 1 (dependencies)
Days 2-4: Phase 2 (state management)
Days 5-6: Phase 3 (gate enforcement)
Days 7-9: Phase 4 (master orchestrator)
Days 10-11: Phase 5 (resume/retry)
Days 12-14: Phase 6 (integration testing)
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| API rate limits | Implement exponential backoff, configurable rate limiting |
| State corruption | Atomic writes, backup before modify, validation on load |
| Long execution time | Parallel bank processing, skip logic, checkpointing |
| Claude response format changes | Robust parsing with fallbacks, validation checks |

---

## Success Criteria

**Enhancement 1 is complete when:**

1. `python -m tools.master_orchestrator --bank deutsche-bank` produces all required outputs
2. `python -m tools.master_orchestrator --phase 1` completes all 5 banks
3. `python -m tools.recovery_cli status` shows accurate workflow state
4. `python -m tools.recovery_cli resume` successfully continues interrupted work
5. All integration tests pass
6. Cross-bank consistency validation passes for Phase 1
