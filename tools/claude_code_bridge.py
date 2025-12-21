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
from state_schema import BankState, STAGE_SEQUENCE

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


# Stage sequence for Claude Code execution
CLAUDE_CODE_STAGES = [
    "initialize",
    "pre_mortem",
    "tier1_evidence",
    "bayesian_1",
    "gate_1",
    "tier2_evidence",
    "bayesian_2",
    "gate_2",
    "tier3_evidence",
    "bayesian_3",
    "gate_3",
    "adversarial",
    "synthesis",
    "complete"
]


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

        if state.blocked:
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

        elif stage == "adversarial":
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
        """Get the next stage in sequence."""
        try:
            idx = CLAUDE_CODE_STAGES.index(current_stage)
            if idx < len(CLAUDE_CODE_STAGES) - 1:
                return CLAUDE_CODE_STAGES[idx + 1]
        except ValueError:
            pass
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
            state.current_stage = next_stage
            state.last_updated = datetime.now(timezone.utc).isoformat()
            self.state_manager.save_bank_state(state)

        return next_stage, None  # Instruction files handled separately

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
