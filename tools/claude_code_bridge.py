"""
CDM Research Protocol - Claude Code Bridge v1.0

Main orchestration interface for Claude Code extension execution.
NO Anthropic API calls - designed for Claude Code's built-in tools.

This module provides:
- Stage instruction generation
- Stage output validation
- State management integration
- Skip decision logic

Usage:
    from claude_code_bridge import ClaudeCodeBridge

    bridge = ClaudeCodeBridge("deutsche-bank", phase=1)

    # Get current stage instruction
    instruction = bridge.get_current_instruction()

    # After Claude Code completes, validate
    result = bridge.validate_stage_output()

    # Advance to next stage
    next_stage = bridge.advance_to_next_stage()
"""

import json
import sys
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass, asdict
from enum import Enum

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import (
    load_bank_manifest, get_bank_config, load_decision_thresholds,
    load_bayesian_tables
)
from state_manager import UnifiedStateManager
from state_schema import BankState, STAGE_SEQUENCE, normalize_stage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class StageStatus(Enum):
    """Status of a research stage."""
    PENDING = "pending"
    READY = "ready"  # Instruction generated
    IN_PROGRESS = "in_progress"
    AWAITING_VALIDATION = "awaiting_validation"
    VALIDATED = "validated"
    BLOCKED = "blocked"
    COMPLETE = "complete"
    SKIPPED = "skipped"


@dataclass
class StageResult:
    """Result of stage validation."""
    success: bool
    stage: str
    errors: List[str]
    warnings: List[str]
    next_stage: Optional[str]
    recommendation: str  # "continue", "skip_to_adversarial", "block_for_review"
    details: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Phase 2 fix: Use canonical STAGE_SEQUENCE from state_schema.py
# instead of maintaining a separate list. This ensures consistency
# across all orchestration tools. The canonical sequence includes:
# initialize, pre_mortem, tier1_evidence, bayesian_1, gate_1,
# tier2_evidence, bayesian_2, gate_2, tier3_evidence, bayesian_3,
# gate_3, adversarial_challenge, final_classification, synthesis, complete


class ClaudeCodeBridge:
    """
    Orchestration interface between Claude Code and Python validation.

    This class manages:
    - Stage instruction generation
    - Output validation
    - State transitions
    - Skip decision logic
    """

    def __init__(self, bank_id: str, phase: int, outputs_dir: Path = None):
        """
        Initialize bridge for a specific bank.

        Args:
            bank_id: Bank identifier (e.g., "deutsche-bank")
            phase: Research phase number
            outputs_dir: Path to outputs directory
        """
        self.bank_id = bank_id
        self.phase = phase
        self.outputs_dir = outputs_dir or PROJECT_ROOT / "outputs"

        # Track parsing errors for propagation (Phase 1 fix: no silent failures)
        self._parsing_errors: List[str] = []

        # Initialize state manager
        self.state_manager = UnifiedStateManager(self.outputs_dir)

        # Load bank configuration
        self.bank_config = get_bank_config(bank_id)
        if not self.bank_config:
            raise ValueError(f"Bank '{bank_id}' not found in manifest")

        self.bank_name = self.bank_config.get('bank_name', bank_id)

        # Determine bank directory
        self._init_bank_directory()

        # Load decision thresholds
        self.thresholds = load_decision_thresholds()

    def _init_bank_directory(self) -> None:
        """Initialize the bank output directory."""
        # Try to find existing phase directory
        phase_dirs = [
            self.outputs_dir / f"phase-{self.phase}",
            self.outputs_dir / f"phase-{self.phase}-european-tier1",
            self.outputs_dir / f"phase-{self.phase}-us-tier1",
            self.outputs_dir / f"phase-{self.phase}-apac-tier1",
        ]

        for phase_dir in phase_dirs:
            bank_dir = phase_dir / self.bank_id
            if bank_dir.exists():
                self.bank_dir = bank_dir
                return

        # Create new directory if none exists
        self.bank_dir = self.outputs_dir / f"phase-{self.phase}" / self.bank_id
        self.bank_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        for subdir in ["1-evidence", "2-bayesian", "3-gates", "4-adversarial", "5-synthesis", "snapshots"]:
            (self.bank_dir / subdir).mkdir(exist_ok=True)

    def get_current_stage(self) -> str:
        """Get the current workflow stage from state."""
        state = self.state_manager.load_bank_state(self.bank_id, self.phase)
        if state:
            return state.current_stage
        return "initialize"

    def get_stage_status(self) -> StageStatus:
        """Get status of current stage."""
        state = self.state_manager.load_bank_state(self.bank_id, self.phase)
        if not state:
            return StageStatus.PENDING

        # Fix: Use is_blocked() method instead of non-existent .blocked attribute
        if state.is_blocked():
            return StageStatus.BLOCKED

        current_stage = state.current_stage
        if current_stage in state.stages_completed:
            return StageStatus.COMPLETE

        return StageStatus.IN_PROGRESS

    def load_bank_context(self) -> Dict[str, Any]:
        """
        Load full context for instruction generation.

        Returns:
            Dictionary with bank config, state, and stage parameters
        """
        state = self.state_manager.load_bank_state(self.bank_id, self.phase)

        # Get prior probability
        if state and state.probability_history:
            current_prob = state.probability_history[-1].posterior
        elif state:
            current_prob = state.current_probability
        else:
            # Use base rate from config or default
            current_prob = self.bank_config.get('prior_adjustment', {}).get('adjusted_prior', 0.40)

        # Count existing evidence
        evidence_file = self.bank_dir / "evidence.json"
        evidence_count = 0
        if evidence_file.exists():
            try:
                data = json.loads(evidence_file.read_text(encoding='utf-8'))
                evidence_count = len(data.get('evidence_items', []))
            except json.JSONDecodeError as e:
                # Phase 1 fix: Log and track parsing errors instead of silent failure
                error_msg = f"evidence.json parse error: {e}"
                logger.error(f"Failed to parse evidence.json for {self.bank_id}: {e}")
                self._parsing_errors.append(error_msg)
            except Exception as e:
                # Phase 1 fix: Log and track unexpected errors
                error_msg = f"evidence.json read error: {e}"
                logger.error(f"Unexpected error reading evidence.json for {self.bank_id}: {e}")
                self._parsing_errors.append(error_msg)

        return {
            "bank_id": self.bank_id,
            "bank_name": self.bank_name,
            "phase": self.phase,
            "bank_dir": str(self.bank_dir),
            "headquarters": self.bank_config.get('headquarters', 'Unknown'),
            "primary_regulator": self.bank_config.get('primary_regulator', 'Unknown'),
            "derivatives_relevance": self.bank_config.get('derivatives_relevance', 'Unknown'),
            "business_model": self.bank_config.get('business_model', 'Unknown'),
            "research_objective": self.bank_config.get('research_objective', {}),
            "known_evidence": self.bank_config.get('known_evidence', []),
            "current_stage": self.get_current_stage(),
            "probability_architect": current_prob,
            "probability_pragmatist": 1.0 - current_prob,
            "evidence_count": evidence_count,
            "stages_completed": state.stages_completed if state else [],
            "thresholds": self.thresholds,
            "parsing_errors": self._parsing_errors,  # Phase 1 fix: expose errors
        }

    def get_skip_decision(self) -> Optional[str]:
        """
        Check if current probability warrants skipping to adversarial.

        Returns:
            "skip_to_adversarial" if probability exceeds threshold, None otherwise
        """
        context = self.load_bank_context()
        prob = context['probability_architect']

        skip_threshold = self.thresholds.get('skip_to_adversarial', 80) / 100.0

        # Skip if very high or very low probability
        if prob >= skip_threshold or prob <= (1 - skip_threshold):
            return "skip_to_adversarial"

        return None

    def validate_stage_output(self, stage: str = None) -> StageResult:
        """
        Validate the outputs produced by Claude Code for a stage.

        Args:
            stage: Stage to validate (defaults to current stage)

        Returns:
            StageResult with validation details
        """
        if stage is None:
            stage = self.get_current_stage()

        errors = []
        warnings = []
        details = {}

        # Phase 1 fix: Include any parsing errors from earlier operations
        if self._parsing_errors:
            errors.extend(self._parsing_errors)

        # Stage-specific validation
        if stage.startswith("tier") and stage.endswith("_evidence"):
            tier = int(stage.replace("tier", "").replace("_evidence", ""))
            result = self._validate_tier_evidence(tier)
            errors.extend(result.get('errors', []))
            warnings.extend(result.get('warnings', []))
            details = result

        elif stage.startswith("bayesian_"):
            tier = int(stage.replace("bayesian_", ""))
            result = self._validate_bayesian(tier)
            errors.extend(result.get('errors', []))
            warnings.extend(result.get('warnings', []))
            details = result

        elif stage.startswith("gate_"):
            gate_num = int(stage.replace("gate_", ""))
            result = self._validate_gate(gate_num)
            errors.extend(result.get('errors', []))
            warnings.extend(result.get('warnings', []))
            details = result

        elif stage == "adversarial" or stage == "adversarial_challenge":
            # Phase 2 fix: Handle both legacy and canonical stage names
            result = self._validate_adversarial()
            errors.extend(result.get('errors', []))
            warnings.extend(result.get('warnings', []))
            details = result

        elif stage == "synthesis":
            result = self._validate_synthesis()
            errors.extend(result.get('errors', []))
            warnings.extend(result.get('warnings', []))
            details = result

        # Determine next stage
        success = len(errors) == 0
        next_stage = self._get_next_stage(stage) if success else None

        # Check for skip condition
        skip_decision = self.get_skip_decision() if success else None
        recommendation = skip_decision if skip_decision else ("continue" if success else "fix_errors")

        return StageResult(
            success=success,
            stage=stage,
            errors=errors,
            warnings=warnings,
            next_stage=next_stage,
            recommendation=recommendation,
            details=details
        )

    def validate_evidence_before_write(self, new_evidence: Dict[str, Any]) -> List[str]:
        """
        Phase 4: Validate new evidence item before writing to evidence.json.

        Args:
            new_evidence: Dict with at least 'id' key

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Check ID format
        item_id = new_evidence.get('id', '')
        if not item_id:
            errors.append("Evidence item missing 'id' field")
        elif not re.match(r'^[A-Za-z0-9_-]+$', item_id):
            errors.append(f"Invalid ID format: {item_id} (must be alphanumeric with _ and -)")

        # Check for duplicate against existing evidence
        evidence_file = self.bank_dir / "evidence.json"
        if evidence_file.exists() and item_id:
            try:
                existing = json.loads(evidence_file.read_text(encoding='utf-8'))
                existing_ids = {e.get('id') for e in existing.get('evidence_items', [])}
                if item_id in existing_ids:
                    errors.append(f"Duplicate ID would be created: {item_id}")
            except Exception as e:
                logger.warning(f"Could not check for duplicates: {e}")

        return errors

    def _validate_tier_evidence(self, tier: int) -> Dict[str, Any]:
        """Validate tier evidence output."""
        errors = []
        warnings = []

        # Check evidence.json exists
        evidence_file = self.bank_dir / "evidence.json"
        if not evidence_file.exists():
            errors.append("evidence.json not found")
            return {"errors": errors, "warnings": warnings}

        try:
            data = json.loads(evidence_file.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            errors.append(f"evidence.json is not valid JSON: {e}")
            return {"errors": errors, "warnings": warnings}

        # Check required fields
        if 'evidence_items' not in data:
            errors.append("evidence.json missing 'evidence_items' array")
        else:
            items = data['evidence_items']
            tier_items = [i for i in items if i.get('tier') == tier]

            if len(tier_items) == 0:
                warnings.append(f"No Tier {tier} evidence items found")

            # Phase 4: Check for duplicate IDs across ALL items
            seen_ids = set()
            for item in items:
                item_id = item.get('id')
                if item_id:
                    if item_id in seen_ids:
                        errors.append(f"Duplicate evidence ID: {item_id}")
                    seen_ids.add(item_id)

            # Validate each item
            required_fields = ['id', 'claim', 'source_url', 'tier', 'claim_type']
            for item in tier_items:
                for field in required_fields:
                    if field not in item:
                        errors.append(f"Evidence item missing required field: {field}")

        # Check tier evidence markdown exists
        md_file = self.bank_dir / "1-evidence" / f"tier{tier}-evidence.md"
        if not md_file.exists():
            warnings.append(f"tier{tier}-evidence.md not created (optional)")

        return {
            "errors": errors,
            "warnings": warnings,
            "evidence_count": len(data.get('evidence_items', [])) if 'evidence_items' in data else 0,
            "tier": tier
        }

    def _validate_bayesian(self, tier: int) -> Dict[str, Any]:
        """Validate Bayesian update output."""
        errors = []
        warnings = []

        # Check bayesian file exists
        bayesian_file = self.bank_dir / "2-bayesian" / f"post-tier{tier}-update.md"
        if not bayesian_file.exists():
            errors.append(f"post-tier{tier}-update.md not found")
            return {"errors": errors, "warnings": warnings}

        content = bayesian_file.read_text(encoding='utf-8')

        # Check for probability value
        import re
        prob_pattern = r'P\s*\(\s*ARCHITECT\s*\)\s*[=:]\s*(\d+(?:\.\d+)?)\s*%'
        match = re.search(prob_pattern, content, re.IGNORECASE)

        if not match:
            warnings.append("Could not find P(ARCHITECT) value in output")
            posterior = None
        else:
            posterior = float(match.group(1)) / 100.0

            # Sanity check
            if posterior < 0 or posterior > 1:
                errors.append(f"Invalid probability: {posterior}")

        return {
            "errors": errors,
            "warnings": warnings,
            "posterior_probability": posterior,
            "tier": tier
        }

    def _validate_gate(self, gate_num: int) -> Dict[str, Any]:
        """Validate reasoning gate output."""
        errors = []
        warnings = []

        gate_file = self.bank_dir / "3-gates" / f"gate-{gate_num}.md"
        if not gate_file.exists():
            errors.append(f"gate-{gate_num}.md not found")
            return {"errors": errors, "warnings": warnings}

        content = gate_file.read_text(encoding='utf-8')

        # Check for decision keywords
        has_decision = any(kw in content.upper() for kw in ['PROCEED', 'SKIP', 'BLOCK', 'CONTINUE'])
        if not has_decision:
            warnings.append("No clear decision (PROCEED/SKIP/BLOCK) found in gate output")

        return {
            "errors": errors,
            "warnings": warnings,
            "gate_number": gate_num
        }

    def _validate_adversarial(self) -> Dict[str, Any]:
        """Validate adversarial challenge output."""
        errors = []
        warnings = []

        required_files = [
            "4-adversarial/counter-case.md",
            "4-adversarial/disconfirming-searches.md",
            "4-adversarial/steelman.md",
            "4-adversarial/verdict.md"
        ]

        for file_path in required_files:
            full_path = self.bank_dir / file_path
            if not full_path.exists():
                errors.append(f"{file_path} not found")

        # Check verdict for decision
        verdict_file = self.bank_dir / "4-adversarial" / "verdict.md"
        verdict_type = None
        if verdict_file.exists():
            content = verdict_file.read_text(encoding='utf-8')
            if "REVISED" in content.upper():
                verdict_type = "REVISED"
            elif "WEAKENED" in content.upper():
                verdict_type = "WEAKENED"
            elif "SUSTAINED" in content.upper() or "STRENGTHENED" in content.upper():
                verdict_type = "SUSTAINED"
            else:
                warnings.append("No clear verdict (SUSTAINED/WEAKENED/REVISED) found")

        return {
            "errors": errors,
            "warnings": warnings,
            "verdict_type": verdict_type
        }

    def _validate_synthesis(self) -> Dict[str, Any]:
        """Validate synthesis output."""
        errors = []
        warnings = []

        # Check confidence calibration FIRST (must exist before assessment)
        calib_file = self.bank_dir / "5-synthesis" / "confidence-calibration.md"
        if not calib_file.exists():
            errors.append("confidence-calibration.md must be created FIRST")

        # Check assessment
        assessment_file = self.bank_dir / "5-synthesis" / "assessment.md"
        if not assessment_file.exists():
            errors.append("assessment.md not found")

        # Check framework integration
        framework_file = self.bank_dir / "5-synthesis" / "framework-integration.md"
        if not framework_file.exists():
            warnings.append("framework-integration.md not found (optional)")

        return {
            "errors": errors,
            "warnings": warnings
        }

    def _get_next_stage(self, current_stage: str) -> Optional[str]:
        """Get the next stage in sequence using canonical STAGE_SEQUENCE."""
        # Phase 2 fix: Use canonical sequence with normalization
        normalized = normalize_stage(current_stage)

        try:
            idx = STAGE_SEQUENCE.index(normalized)
            if idx < len(STAGE_SEQUENCE) - 1:
                return STAGE_SEQUENCE[idx + 1]
        except ValueError:
            logger.warning(f"Stage '{current_stage}' (normalized: '{normalized}') not in STAGE_SEQUENCE")
        return None

    def advance_to_next_stage(self) -> Tuple[Optional[str], Optional[Path]]:
        """
        Advance to next stage after successful validation.

        Returns:
            Tuple of (next_stage_name, instruction_file_path)
        """
        current = self.get_current_stage()
        next_stage = self._get_next_stage(current)

        if not next_stage:
            return None, None

        # Update state
        state = self.state_manager.load_bank_state(self.bank_id, self.phase)
        if state:
            if current not in state.stages_completed:
                state.stages_completed.append(current)
            # CRITICAL: Use start_stage() to initialize stage timing for timeout detection
            state.start_stage(next_stage)
            self.state_manager.save_bank_state(state)

        return next_stage, None  # Instruction files handled separately

    # Phase 3: Resume context methods for batch recovery
    def get_resume_context(self) -> Dict[str, Any]:
        """Get context for resuming interrupted research."""
        state = self.state_manager.load_bank_state(self.bank_id, self.phase)
        if not state:
            return {"can_resume": False, "reason": "No state file found"}

        return {
            "can_resume": True,
            "current_stage": state.current_stage,
            "stage_started_at": state.stage_started_at,
            "files_already_written": state.stage_outputs_written,
            "retry_count": state.retry_count,
            "max_retries": state.max_retries,
            "last_checkpoint": state.last_checkpoint_at,
            "probability": state.current_probability,
            "evidence_counts": state.evidence_counts,
            "stages_completed": state.stages_completed,
            "instruction": self._generate_resume_instruction(state)
        }

    def _generate_resume_instruction(self, state) -> str:
        """Generate human-readable resume instruction for Claude Code."""
        if state.current_stage == "complete":
            return "Research is complete. No action needed."

        if state.is_blocked():
            return f"Research is BLOCKED at {state.blocked_checkpoint}: {state.blocked_reason}"

        if state.stage_outputs_written:
            files = ", ".join(state.stage_outputs_written)
            return f"Resume stage '{state.current_stage}'. Already written: {files}. Continue from where you left off."

        if state.stage_started_at:
            return f"Stage '{state.current_stage}' was started but no files written yet. Restart the stage."

        return f"Start stage '{state.current_stage}' from the beginning."

    def checkpoint_progress(self, files_written: List[str] = None) -> bool:
        """Record a checkpoint for the current stage."""
        state = self.state_manager.load_bank_state(self.bank_id, self.phase)
        if not state:
            return False

        state.checkpoint_stage_progress(files_written)
        self.state_manager.save_bank_state(state)
        logger.info(f"Checkpoint recorded for {self.bank_id} stage {state.current_stage}")
        return True

    def mark_complete(self) -> None:
        """Mark bank research as complete."""
        state = self.state_manager.load_bank_state(self.bank_id, self.phase)
        if state:
            state.current_stage = "complete"
            state.completed_at = datetime.now(timezone.utc).isoformat()
            self.state_manager.save_bank_state(state)

    def is_complete(self) -> bool:
        """Check if bank research is complete."""
        state = self.state_manager.load_bank_state(self.bank_id, self.phase)
        return state and state.current_stage == "complete"

    # Phase 8: Review queue resolution methods
    def get_pending_reviews(self) -> List[Dict[str, Any]]:
        """Get pending review items for this bank."""
        all_reviews = self.state_manager.get_pending_reviews()
        return [r.to_dict() for r in all_reviews if r.bank_id == self.bank_id]

    def resolve_review(self, resolution: str, resolved_by: str = "claude_code") -> bool:
        """Resolve pending review for this bank."""
        try:
            self.state_manager.resolve_review(self.bank_id, resolution, resolved_by)
            logger.info(f"Resolved review for {self.bank_id}: {resolution}")
            return True
        except Exception as e:
            logger.error(f"Failed to resolve review: {e}")
            return False


def main():
    """CLI interface for the bridge."""
    import argparse

    parser = argparse.ArgumentParser(description="Claude Code Bridge for CDM Research")
    parser.add_argument("--bank", required=True, help="Bank ID")
    parser.add_argument("--phase", type=int, default=1, help="Phase number")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--validate", help="Validate a specific stage")
    parser.add_argument("--context", action="store_true", help="Show bank context")
    parser.add_argument("--test", action="store_true", help="Run self-test")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--resume", action="store_true", help="Show resume context for interrupted research")
    parser.add_argument("--checkpoint", nargs="*", metavar="FILE", help="Record checkpoint with optional files written")
    parser.add_argument("--reviews", action="store_true", help="Show pending review items for this bank (Phase 8)")
    parser.add_argument("--resolve", type=str, metavar="RESOLUTION", help="Resolve pending review with given resolution (Phase 8)")
    parser.add_argument("--check-timeouts", action="store_true",
                        help="Check all banks in phase for stage timeouts and auto-block")

    args = parser.parse_args()

    try:
        bridge = ClaudeCodeBridge(args.bank, args.phase)

        if args.test:
            # Self-test
            print("Bridge initialized successfully")
            print(f"Bank: {bridge.bank_name}")
            print(f"Directory: {bridge.bank_dir}")
            print("Test PASSED")
            return 0

        if args.status:
            context = bridge.load_bank_context()
            if args.json:
                print(json.dumps(context, indent=2))
            else:
                print(f"Bank: {context['bank_name']}")
                print(f"Current Stage: {context['current_stage']}")
                print(f"P(ARCHITECT): {context['probability_architect']*100:.1f}%")
                print(f"Evidence Count: {context['evidence_count']}")
            return 0

        if args.validate:
            result = bridge.validate_stage_output(args.validate)
            if args.json:
                print(json.dumps(result.to_dict(), indent=2))
            else:
                print(f"Stage: {result.stage}")
                print(f"Success: {result.success}")
                if result.errors:
                    print(f"Errors: {result.errors}")
                if result.warnings:
                    print(f"Warnings: {result.warnings}")
                print(f"Next Stage: {result.next_stage}")
                print(f"Recommendation: {result.recommendation}")
            return 0 if result.success else 1

        if args.context:
            context = bridge.load_bank_context()
            print(json.dumps(context, indent=2))
            return 0

        # Phase 3: Resume context handler
        if args.resume:
            resume = bridge.get_resume_context()
            if args.json:
                print(json.dumps(resume, indent=2))
            else:
                if resume["can_resume"]:
                    print(f"Current Stage: {resume['current_stage']}")
                    print(f"Stages Completed: {', '.join(resume['stages_completed']) or 'None'}")
                    print(f"P(ARCHITECT): {resume['probability']*100:.1f}%")
                    if resume['files_already_written']:
                        print(f"Files Written: {', '.join(resume['files_already_written'])}")
                    print(f"Retry Count: {resume['retry_count']}/{resume['max_retries']}")
                    print(f"\nInstruction: {resume['instruction']}")
                else:
                    print(f"Cannot resume: {resume['reason']}")
            return 0

        # Phase 3: Checkpoint handler
        if args.checkpoint is not None:
            files = args.checkpoint if args.checkpoint else None
            success = bridge.checkpoint_progress(files)
            if args.json:
                print(json.dumps({"success": success, "files": files}))
            else:
                if success:
                    print(f"Checkpoint recorded" + (f" with files: {files}" if files else ""))
                else:
                    print("Failed to record checkpoint")
            return 0 if success else 1

        # Phase 8: Reviews handler
        if args.reviews:
            reviews = bridge.get_pending_reviews()
            if args.json:
                print(json.dumps(reviews, indent=2))
            else:
                if reviews:
                    print(f"\nPending Reviews for {args.bank}:")
                    for r in reviews:
                        print(f"  - Stage: {r.get('stage', 'N/A')}")
                        print(f"    Reason: {r.get('reason', 'N/A')}")
                        print(f"    Created: {r.get('created_at', 'N/A')}")
                        print()
                else:
                    print(f"No pending reviews for {args.bank}")
            return 0

        # Phase 8: Resolve handler
        if args.resolve:
            success = bridge.resolve_review(args.resolve)
            if args.json:
                print(json.dumps({"success": success, "resolution": args.resolve}))
            else:
                if success:
                    print(f"Review resolved: {args.resolve}")
                else:
                    print("Failed to resolve review")
            return 0 if success else 1

        # Stage timeout check handler (operates on all banks in phase)
        if getattr(args, 'check_timeouts', False):
            stage_timeouts, default_timeout = bridge.state_manager.get_stage_timeouts_from_config()
            timed_out = bridge.state_manager.check_and_handle_timeouts(
                phase=args.phase,
                stage_timeouts=stage_timeouts,
                default_timeout=default_timeout
            )
            if args.json:
                print(json.dumps({"timed_out": timed_out, "count": len(timed_out)}))
            else:
                if timed_out:
                    print(f"\nTimed out banks ({len(timed_out)}):")
                    for t in timed_out:
                        print(f"  - {t['bank_id']}: {t['stage']} ({t['elapsed_minutes']:.1f} min)")
                else:
                    print("No timed-out banks found")
            return 0

        # Default: show status
        context = bridge.load_bank_context()
        print(f"Bank: {context['bank_name']}")
        print(f"Current Stage: {context['current_stage']}")
        print(f"P(ARCHITECT): {context['probability_architect']*100:.1f}%")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
