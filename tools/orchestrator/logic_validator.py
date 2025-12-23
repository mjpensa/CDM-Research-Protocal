"""
CDM Research Protocol - Logic Validator v1.0

Main orchestrator for all logic validation of agent outputs.
Coordinates Bayesian validation, protocol compliance, and adjustment consistency.

Usage:
    from logic_validator import LogicValidator

    validator = LogicValidator()
    result = validator.validate_stage(
        bank_id="deutsche-bank",
        phase=1,
        stage="bayesian_1",
        bank_dir=Path("outputs/phase-1-european-tier1/deutsche-bank"),
        state=bank_state
    )

    if not result.valid:
        for violation in result.violations:
            print(f"[{violation.severity}] {violation.violation_type}")
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

# Project imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config_loader import load_validation_rules
    from orchestrator.violation_queue import (
        ViolationQueue,
        ProtocolViolation,
        LogicValidationResult
    )
    from orchestrator.bayesian_validator import BayesianValidator
    from orchestrator.protocol_compliance import ProtocolComplianceChecker
except ImportError:
    from tools.config_loader import load_validation_rules
    from tools.orchestrator.violation_queue import (
        ViolationQueue,
        ProtocolViolation,
        LogicValidationResult
    )
    from tools.orchestrator.bayesian_validator import BayesianValidator
    from tools.orchestrator.protocol_compliance import ProtocolComplianceChecker


# Stage to validation type mapping
STAGE_VALIDATION_MAP = {
    "bayesian_1": ["bayesian"],
    "bayesian_2": ["bayesian"],
    "bayesian_3": ["bayesian"],
    "gate_1": ["gate_sections"],
    "gate_2": ["gate_sections", "observable_implications"],
    "gate_3": ["gate_sections"],
    "adversarial_challenge": ["disconfirmation", "steelman", "adversarial_sections"],
    "synthesis": ["confidence_calibration"]
}


class LogicValidator:
    """
    Main orchestrator for logic validation.

    Coordinates validation across stages and manages the violation queue.
    """

    def __init__(self, queue_path: Optional[Path] = None):
        """
        Initialize the logic validator.

        Args:
            queue_path: Custom path for violation queue (optional)
        """
        self.violation_queue = ViolationQueue(queue_path)
        self.bayesian_validator = BayesianValidator()
        self.protocol_checker = ProtocolComplianceChecker()
        self.rules = load_validation_rules()

    def validate_stage(
        self,
        bank_id: str,
        phase: int,
        stage: str,
        bank_dir: Path,
        prior_probability: float = 0.30,
        current_probability: float = 0.50
    ) -> LogicValidationResult:
        """
        Validate a completed stage.

        Args:
            bank_id: Bank identifier
            phase: Research phase
            stage: Stage name (e.g., "bayesian_1", "gate_2")
            bank_dir: Path to bank output directory
            prior_probability: Prior P(Architect) before current tier
            current_probability: Current P(Architect)

        Returns:
            LogicValidationResult with violations and metrics
        """
        violations = []
        warnings = []
        metrics = {}

        # Get validation types for this stage
        validation_types = STAGE_VALIDATION_MAP.get(stage, [])

        if not validation_types:
            # No specific validations for this stage
            return LogicValidationResult(
                valid=True,
                stage=stage,
                bank_id=bank_id,
                phase=phase,
                violations=[],
                warnings=[f"No validations defined for stage: {stage}"],
                metrics={"skipped": True}
            )

        # Run appropriate validations
        for val_type in validation_types:
            stage_violations = self._run_validation(
                val_type=val_type,
                bank_dir=bank_dir,
                stage=stage,
                prior_probability=prior_probability,
                current_probability=current_probability
            )
            violations.extend(stage_violations)

        # Queue violations (non-blocking)
        if violations:
            self.violation_queue.add_violations(violations, bank_id, phase)

        # Count by severity
        error_count = sum(1 for v in violations if v.severity == "ERROR")
        warning_count = sum(1 for v in violations if v.severity == "WARNING")

        metrics = {
            "validation_types": validation_types,
            "total_violations": len(violations),
            "errors": error_count,
            "warnings": warning_count
        }

        # Determine overall validity
        # By default, we don't block on violations (non-blocking mode)
        # But we flag if there are ERROR-level violations
        settings = self.rules.get("validation_settings", {})
        blocking_mode = settings.get("blocking_mode", False)

        if blocking_mode and error_count > 0:
            valid = False
        else:
            valid = True  # Non-blocking: always proceed

        return LogicValidationResult(
            valid=valid,
            stage=stage,
            bank_id=bank_id,
            phase=phase,
            violations=violations,
            warnings=[v.description for v in violations if v.severity == "WARNING"],
            metrics=metrics
        )

    def _run_validation(
        self,
        val_type: str,
        bank_dir: Path,
        stage: str,
        prior_probability: float,
        current_probability: float
    ) -> List[ProtocolViolation]:
        """
        Run a specific type of validation.

        Args:
            val_type: Type of validation to run
            bank_dir: Path to bank output directory
            stage: Current stage name
            prior_probability: Prior P(Architect)
            current_probability: Current P(Architect)

        Returns:
            List of violations found
        """
        violations = []

        try:
            if val_type == "bayesian":
                # Extract tier number from stage name
                tier = int(stage.split("_")[1]) if "_" in stage else 1
                violations = self.bayesian_validator.validate_bayesian_update(
                    bank_dir=bank_dir,
                    tier=tier,
                    prior_probability=prior_probability
                )

            elif val_type == "gate_sections":
                gate_num = int(stage.split("_")[1]) if "_" in stage else 1
                violations = self.protocol_checker.verify_gate_sections(bank_dir, gate_num)

            elif val_type == "observable_implications":
                leading = "ARCHITECT" if current_probability > 0.5 else "PRAGMATIST"
                violations = self.protocol_checker.verify_observable_implications(
                    bank_dir, leading
                )

            elif val_type == "disconfirmation":
                violations = self.protocol_checker.verify_disconfirmation_testing(bank_dir)

            elif val_type == "steelman":
                violations = self.protocol_checker.verify_steelman_quality(bank_dir)

            elif val_type == "adversarial_sections":
                violations = self.protocol_checker.verify_adversarial_sections(bank_dir)

            elif val_type == "confidence_calibration":
                violations = self.protocol_checker.verify_synthesis(bank_dir)

        except Exception as e:
            # Log error but don't fail validation
            violations.append(ProtocolViolation(
                violation_type="VALIDATION_ERROR",
                severity="WARNING",
                description=f"Error during {val_type} validation: {str(e)}",
                stage=stage,
                remediation="Check validation configuration and file paths"
            ))

        return violations

    def validate_bank_complete(
        self,
        bank_id: str,
        phase: int,
        bank_dir: Path,
        state: Any
    ) -> LogicValidationResult:
        """
        Run comprehensive validation on a completed bank assessment.

        Args:
            bank_id: Bank identifier
            phase: Research phase
            bank_dir: Path to bank output directory
            state: BankState object

        Returns:
            Comprehensive LogicValidationResult
        """
        all_violations = []
        all_metrics = {}

        # Get probability history for prior lookups
        prob_history = getattr(state, 'probability_history', [])
        prior = getattr(state, 'prior_probability', 0.30)
        current = getattr(state, 'current_probability', 0.50)

        # Validate each stage
        stages_to_validate = [
            "bayesian_1", "gate_1",
            "bayesian_2", "gate_2",
            "adversarial_challenge",
            "synthesis"
        ]

        # Add tier 3 if it was executed
        completed_stages = getattr(state, 'stages_completed', [])
        if "tier3_evidence" in completed_stages or "bayesian_3" in completed_stages:
            stages_to_validate.insert(4, "bayesian_3")
            stages_to_validate.insert(5, "gate_3")

        for stage in stages_to_validate:
            # Determine prior for this stage
            stage_prior = prior
            if stage.startswith("bayesian_"):
                tier = int(stage.split("_")[1])
                if tier > 1 and prob_history:
                    # Use posterior from previous tier as prior
                    for update in reversed(prob_history):
                        if f"tier{tier-1}" in update.get("stage", "") or f"bayesian_{tier-1}" in update.get("stage", ""):
                            stage_prior = update.get("posterior", prior)
                            break

            result = self.validate_stage(
                bank_id=bank_id,
                phase=phase,
                stage=stage,
                bank_dir=bank_dir,
                prior_probability=stage_prior,
                current_probability=current
            )

            all_violations.extend(result.violations)
            all_metrics[stage] = result.metrics

        # Also check evidence independence
        evidence_path = bank_dir / "evidence.json"
        if evidence_path.exists():
            evidence_data = json.loads(evidence_path.read_text(encoding='utf-8'))
            independence_violations = self.bayesian_validator.validate_independence(
                evidence_data.get("evidence_items", [])
            )
            all_violations.extend(independence_violations)

        # Summary metrics
        error_count = sum(1 for v in all_violations if v.severity == "ERROR")
        warning_count = sum(1 for v in all_violations if v.severity == "WARNING")

        return LogicValidationResult(
            valid=error_count == 0,
            stage="complete",
            bank_id=bank_id,
            phase=phase,
            violations=all_violations,
            warnings=[v.description for v in all_violations if v.severity == "WARNING"],
            metrics={
                "stages_validated": len(stages_to_validate),
                "total_violations": len(all_violations),
                "errors": error_count,
                "warnings": warning_count,
                "stage_metrics": all_metrics
            }
        )

    def get_violation_summary(self, bank_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get summary of violations.

        Args:
            bank_id: Filter by bank ID (optional)

        Returns:
            Summary statistics
        """
        if bank_id:
            violations = self.violation_queue.get_violations_for_bank(bank_id)
        else:
            violations = self.violation_queue.get_pending_violations()

        by_type = {}
        by_severity = {"ERROR": 0, "WARNING": 0, "INFO": 0}
        by_stage = {}

        for v in violations:
            by_type[v.violation_type] = by_type.get(v.violation_type, 0) + 1
            by_severity[v.severity] = by_severity.get(v.severity, 0) + 1
            by_stage[v.stage] = by_stage.get(v.stage, 0) + 1

        return {
            "total": len(violations),
            "by_type": by_type,
            "by_severity": by_severity,
            "by_stage": by_stage
        }

    def generate_report(self, bank_id: Optional[str] = None) -> str:
        """
        Generate validation report.

        Args:
            bank_id: Filter by bank ID (optional)

        Returns:
            Markdown report
        """
        return self.violation_queue.generate_report(format="markdown")


# --- CLI INTERFACE ---

def main():
    """CLI interface for logic validator."""
    import argparse

    parser = argparse.ArgumentParser(description="CDM Research Protocol - Logic Validator")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Validate stage command
    stage_parser = subparsers.add_parser("validate-stage", help="Validate a specific stage")
    stage_parser.add_argument("bank_dir", type=Path, help="Path to bank output directory")
    stage_parser.add_argument("--stage", required=True, help="Stage to validate")
    stage_parser.add_argument("--bank-id", required=True, help="Bank identifier")
    stage_parser.add_argument("--phase", type=int, default=1, help="Research phase")
    stage_parser.add_argument("--prior", type=float, default=0.30, help="Prior P(Architect)")
    stage_parser.add_argument("--current", type=float, default=0.50, help="Current P(Architect)")

    # Validate complete command
    complete_parser = subparsers.add_parser("validate-complete", help="Validate complete bank assessment")
    complete_parser.add_argument("bank_dir", type=Path, help="Path to bank output directory")
    complete_parser.add_argument("--bank-id", required=True, help="Bank identifier")
    complete_parser.add_argument("--phase", type=int, default=1, help="Research phase")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show violation summary")
    summary_parser.add_argument("--bank-id", help="Filter by bank ID")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate violation report")
    report_parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    validator = LogicValidator()

    if args.command == "validate-stage":
        result = validator.validate_stage(
            bank_id=args.bank_id,
            phase=args.phase,
            stage=args.stage,
            bank_dir=args.bank_dir,
            prior_probability=args.prior,
            current_probability=args.current
        )
        print(f"Validation result: {'VALID' if result.valid else 'INVALID'}")
        print(f"Violations: {len(result.violations)}")
        for v in result.violations:
            print(f"  [{v.severity}] {v.violation_type}: {v.description}")

    elif args.command == "validate-complete":
        # Create a minimal state object for testing
        class MinimalState:
            prior_probability = 0.30
            current_probability = 0.50
            probability_history = []
            stages_completed = []

        result = validator.validate_bank_complete(
            bank_id=args.bank_id,
            phase=args.phase,
            bank_dir=args.bank_dir,
            state=MinimalState()
        )
        print(f"Complete validation: {'VALID' if result.valid else 'INVALID'}")
        print(f"Total violations: {len(result.violations)}")
        print(f"Metrics: {json.dumps(result.metrics, indent=2)}")

    elif args.command == "summary":
        summary = validator.get_violation_summary(args.bank_id)
        print(json.dumps(summary, indent=2))

    elif args.command == "report":
        report = validator.generate_report()
        if args.output:
            Path(args.output).write_text(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
