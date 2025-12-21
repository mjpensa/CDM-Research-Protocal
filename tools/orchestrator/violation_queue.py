"""
CDM Research Protocol - Violation Queue v1.0

Non-blocking queue for protocol violations.
Violations are queued for batch review rather than stopping workflow.

Usage:
    from violation_queue import ViolationQueue, ProtocolViolation

    queue = ViolationQueue()

    # Add a violation
    violation = ProtocolViolation(
        violation_type="BAYESIAN_POSTERIOR_MISMATCH",
        severity="ERROR",
        description="Posterior probability mismatch",
        expected_value="23%",
        actual_value="35%",
        stage="bayesian_1"
    )
    queue.add_violation(violation, bank_id="deutsche-bank")

    # Get violations for review
    violations = queue.get_pending_violations()

    # Generate report
    report = queue.generate_report()
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

# File locking for concurrent access safety
try:
    from orchestrator.file_lock import file_lock, atomic_write, load_json as _load_json
    FILE_LOCK_AVAILABLE = True
except ImportError:
    FILE_LOCK_AVAILABLE = False

# --- PATHS ---
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent
STATE_DIR = PROJECT_ROOT / "outputs" / "state"
VIOLATION_QUEUE_PATH = STATE_DIR / "violation-queue.json"


# --- DATA CLASSES ---

@dataclass
class ProtocolViolation:
    """Record of a protocol violation."""
    violation_type: str
    severity: str  # ERROR, WARNING, INFO
    description: str
    stage: str
    expected_value: Optional[Any] = None
    actual_value: Optional[Any] = None
    remediation: Optional[str] = None
    violation_id: Optional[str] = None
    bank_id: Optional[str] = None
    phase: Optional[int] = None
    status: str = "pending"  # pending, reviewed, resolved, dismissed
    resolution: Optional[str] = None
    resolved_at: Optional[str] = None
    resolved_by: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ProtocolViolation':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class LogicValidationResult:
    """Result of logic validation for a stage."""
    valid: bool
    stage: str
    bank_id: str
    phase: int
    violations: List[ProtocolViolation] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        result = asdict(self)
        result['violations'] = [v.to_dict() if isinstance(v, ProtocolViolation) else v
                                for v in self.violations]
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'LogicValidationResult':
        violations = [ProtocolViolation.from_dict(v) if isinstance(v, dict) else v
                      for v in data.get('violations', [])]
        data['violations'] = violations
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# --- VIOLATION QUEUE ---

class ViolationQueue:
    """
    Non-blocking queue for protocol violations.

    Violations are stored for batch review rather than blocking the workflow.
    """

    def __init__(self, queue_path: Optional[Path] = None):
        """
        Initialize the violation queue.

        Args:
            queue_path: Custom path for queue file (defaults to outputs/state/violation-queue.json)
        """
        self.queue_path = Path(queue_path) if queue_path else VIOLATION_QUEUE_PATH
        self.queue_path.parent.mkdir(parents=True, exist_ok=True)

    def add_violation(
        self,
        violation: ProtocolViolation,
        bank_id: str,
        phase: int = 1
    ) -> str:
        """
        Add a violation to the queue.

        Uses file locking to prevent concurrent access data loss.

        Args:
            violation: The violation to add
            bank_id: Bank identifier
            phase: Research phase

        Returns:
            violation_id: Unique identifier for the violation
        """
        def _do_add(data):
            # Generate violation ID if not set
            if not violation.violation_id:
                violation_count = len(data["violations"]) + 1
                violation.violation_id = f"VIO-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{violation_count:04d}"

            violation.bank_id = bank_id
            violation.phase = phase

            data["violations"].append(violation.to_dict())

            # Update summary
            self._update_summary(data)
            return data

        if FILE_LOCK_AVAILABLE:
            with file_lock(self.queue_path, operation="add_violation"):
                data = self._load_queue()
                data = _do_add(data)
                atomic_write(self.queue_path, data)
        else:
            # Fallback without locking
            data = self._load_queue()
            data = _do_add(data)
            self._save_queue(data)

        return violation.violation_id

    def add_violations(
        self,
        violations: List[ProtocolViolation],
        bank_id: str,
        phase: int = 1
    ) -> List[str]:
        """
        Add multiple violations to the queue.

        Args:
            violations: List of violations to add
            bank_id: Bank identifier
            phase: Research phase

        Returns:
            List of violation_ids
        """
        return [self.add_violation(v, bank_id, phase) for v in violations]

    def get_violations_for_bank(
        self,
        bank_id: str,
        status: Optional[str] = None
    ) -> List[ProtocolViolation]:
        """
        Get violations for a specific bank.

        Args:
            bank_id: Bank identifier
            status: Filter by status (optional)

        Returns:
            List of violations
        """
        data = self._load_queue()
        violations = [
            ProtocolViolation.from_dict(v) for v in data["violations"]
            if v.get("bank_id") == bank_id
        ]

        if status:
            violations = [v for v in violations if v.status == status]

        return violations

    def get_pending_violations(self) -> List[ProtocolViolation]:
        """Get all pending violations."""
        data = self._load_queue()
        return [
            ProtocolViolation.from_dict(v) for v in data["violations"]
            if v.get("status") == "pending"
        ]

    def get_violations_by_severity(self, severity: str) -> List[ProtocolViolation]:
        """Get violations by severity level."""
        data = self._load_queue()
        return [
            ProtocolViolation.from_dict(v) for v in data["violations"]
            if v.get("severity") == severity
        ]

    def resolve_violation(
        self,
        violation_id: str,
        resolution: str,
        resolved_by: str = "human_review"
    ) -> bool:
        """
        Mark a violation as resolved.

        Uses file locking to prevent concurrent access issues.

        Args:
            violation_id: ID of the violation to resolve
            resolution: Resolution description
            resolved_by: Who/what resolved it

        Returns:
            True if violation was found and updated
        """
        def _do_resolve(data):
            for v in data["violations"]:
                if v.get("violation_id") == violation_id:
                    v["status"] = "resolved"
                    v["resolution"] = resolution
                    v["resolved_at"] = datetime.now(timezone.utc).isoformat()
                    v["resolved_by"] = resolved_by
                    self._update_summary(data)
                    return data, True
            return data, False

        if FILE_LOCK_AVAILABLE:
            with file_lock(self.queue_path, operation="resolve_violation"):
                data = self._load_queue()
                data, found = _do_resolve(data)
                if found:
                    atomic_write(self.queue_path, data)
                return found
        else:
            # Fallback without locking
            data = self._load_queue()
            data, found = _do_resolve(data)
            if found:
                self._save_queue(data)
            return found

    def dismiss_violation(
        self,
        violation_id: str,
        reason: str
    ) -> bool:
        """
        Dismiss a violation (e.g., false positive).

        Uses file locking to prevent concurrent access issues.

        Args:
            violation_id: ID of the violation to dismiss
            reason: Reason for dismissal

        Returns:
            True if violation was found and updated
        """
        def _do_dismiss(data):
            for v in data["violations"]:
                if v.get("violation_id") == violation_id:
                    v["status"] = "dismissed"
                    v["resolution"] = f"Dismissed: {reason}"
                    v["resolved_at"] = datetime.now(timezone.utc).isoformat()
                    self._update_summary(data)
                    return data, True
            return data, False

        if FILE_LOCK_AVAILABLE:
            with file_lock(self.queue_path, operation="dismiss_violation"):
                data = self._load_queue()
                data, found = _do_dismiss(data)
                if found:
                    atomic_write(self.queue_path, data)
                return found
        else:
            # Fallback without locking
            data = self._load_queue()
            data, found = _do_dismiss(data)
            if found:
                self._save_queue(data)
            return found

    def get_summary(self) -> Dict[str, Any]:
        """Get queue summary statistics."""
        data = self._load_queue()
        return data.get("summary", {})

    def generate_report(self, format: str = "markdown") -> str:
        """
        Generate a report of violations.

        Args:
            format: Output format ("markdown" or "text")

        Returns:
            Report as string
        """
        data = self._load_queue()
        violations = data.get("violations", [])

        if format == "markdown":
            return self._generate_markdown_report(violations, data.get("summary", {}))
        else:
            return self._generate_text_report(violations, data.get("summary", {}))

    def _generate_markdown_report(
        self,
        violations: List[Dict],
        summary: Dict
    ) -> str:
        """Generate markdown report."""
        lines = [
            "# Violation Queue Report",
            "",
            f"**Generated**: {datetime.now(timezone.utc).isoformat()}",
            "",
            "## Summary",
            "",
            f"- Total violations: {summary.get('total', 0)}",
            f"- Errors: {summary.get('errors', 0)}",
            f"- Warnings: {summary.get('warnings', 0)}",
            f"- Pending: {summary.get('pending', 0)}",
            ""
        ]

        # Group by bank
        by_bank = {}
        for v in violations:
            bank_id = v.get("bank_id", "unknown")
            if bank_id not in by_bank:
                by_bank[bank_id] = []
            by_bank[bank_id].append(v)

        for bank_id, bank_violations in sorted(by_bank.items()):
            lines.append(f"## {bank_id}")
            lines.append("")

            pending = [v for v in bank_violations if v.get("status") == "pending"]
            if pending:
                lines.append("### Pending Violations")
                lines.append("")
                for v in pending:
                    severity_icon = "🔴" if v.get("severity") == "ERROR" else "🟡"
                    lines.append(f"- {severity_icon} **{v.get('violation_type')}** ({v.get('stage')})")
                    lines.append(f"  - {v.get('description')}")
                    if v.get("expected_value") and v.get("actual_value"):
                        lines.append(f"  - Expected: {v.get('expected_value')}, Actual: {v.get('actual_value')}")
                    if v.get("remediation"):
                        lines.append(f"  - Remediation: {v.get('remediation')}")
                    lines.append("")

            resolved = [v for v in bank_violations if v.get("status") in ("resolved", "dismissed")]
            if resolved:
                lines.append("### Resolved/Dismissed")
                lines.append("")
                for v in resolved:
                    lines.append(f"- ~~{v.get('violation_type')}~~: {v.get('resolution')}")
                lines.append("")

        return "\n".join(lines)

    def _generate_text_report(
        self,
        violations: List[Dict],
        summary: Dict
    ) -> str:
        """Generate plain text report."""
        lines = [
            "VIOLATION QUEUE REPORT",
            "=" * 50,
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "SUMMARY",
            "-" * 20,
            f"Total: {summary.get('total', 0)}",
            f"Errors: {summary.get('errors', 0)}",
            f"Warnings: {summary.get('warnings', 0)}",
            f"Pending: {summary.get('pending', 0)}",
            ""
        ]

        for v in violations:
            if v.get("status") == "pending":
                lines.append(f"[{v.get('severity')}] {v.get('violation_type')}")
                lines.append(f"  Bank: {v.get('bank_id')}")
                lines.append(f"  Stage: {v.get('stage')}")
                lines.append(f"  Description: {v.get('description')}")
                lines.append("")

        return "\n".join(lines)

    def clear_resolved(self) -> int:
        """
        Remove resolved and dismissed violations from queue.

        Uses file locking to prevent concurrent access issues.

        Returns:
            Number of violations removed
        """
        def _do_clear(data):
            original_count = len(data["violations"])
            data["violations"] = [
                v for v in data["violations"]
                if v.get("status") == "pending"
            ]
            removed = original_count - len(data["violations"])
            self._update_summary(data)
            return data, removed

        if FILE_LOCK_AVAILABLE:
            with file_lock(self.queue_path, operation="clear_resolved"):
                data = self._load_queue()
                data, removed = _do_clear(data)
                atomic_write(self.queue_path, data)
        else:
            # Fallback without locking
            data = self._load_queue()
            data, removed = _do_clear(data)
            self._save_queue(data)

        return removed

    # --- INTERNAL HELPERS ---

    def _load_queue(self) -> Dict:
        """Load queue from disk."""
        default = {
            "schema_version": "1.0",
            "violations": [],
            "summary": {
                "total": 0,
                "errors": 0,
                "warnings": 0,
                "pending": 0,
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
        }
        if FILE_LOCK_AVAILABLE:
            return _load_json(self.queue_path, default)
        if self.queue_path.exists():
            try:
                return json.loads(self.queue_path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, IOError):
                return default
        return default

    def _save_queue(self, data: Dict) -> None:
        """Save queue to disk (fallback when locking not available)."""
        if FILE_LOCK_AVAILABLE:
            atomic_write(self.queue_path, data)
        else:
            self.queue_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )

    def _update_summary(self, data: Dict) -> None:
        """Update summary statistics in data dict."""
        violations = data.get("violations", [])
        data["summary"] = {
            "total": len(violations),
            "errors": sum(1 for v in violations if v.get("severity") == "ERROR"),
            "warnings": sum(1 for v in violations if v.get("severity") == "WARNING"),
            "pending": sum(1 for v in violations if v.get("status") == "pending"),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }


# --- CLI INTERFACE ---

def main():
    """CLI interface for violation queue."""
    import argparse

    parser = argparse.ArgumentParser(description="CDM Research Protocol - Violation Queue")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show queue status")

    # List command
    list_parser = subparsers.add_parser("list", help="List violations")
    list_parser.add_argument("--bank", help="Filter by bank ID")
    list_parser.add_argument("--severity", choices=["ERROR", "WARNING", "INFO"],
                             help="Filter by severity")
    list_parser.add_argument("--pending-only", action="store_true",
                             help="Show only pending violations")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate report")
    report_parser.add_argument("--format", choices=["markdown", "text"],
                               default="markdown", help="Output format")
    report_parser.add_argument("--output", help="Output file path")

    # Resolve command
    resolve_parser = subparsers.add_parser("resolve", help="Resolve a violation")
    resolve_parser.add_argument("violation_id", help="Violation ID to resolve")
    resolve_parser.add_argument("resolution", help="Resolution description")

    # Dismiss command
    dismiss_parser = subparsers.add_parser("dismiss", help="Dismiss a violation")
    dismiss_parser.add_argument("violation_id", help="Violation ID to dismiss")
    dismiss_parser.add_argument("reason", help="Reason for dismissal")

    # Clear command
    clear_parser = subparsers.add_parser("clear-resolved", help="Remove resolved violations")

    args = parser.parse_args()

    queue = ViolationQueue()

    if args.command == "status":
        summary = queue.get_summary()
        print(json.dumps(summary, indent=2))

    elif args.command == "list":
        if args.bank:
            violations = queue.get_violations_for_bank(
                args.bank,
                status="pending" if args.pending_only else None
            )
        elif args.severity:
            violations = queue.get_violations_by_severity(args.severity)
        elif args.pending_only:
            violations = queue.get_pending_violations()
        else:
            data = queue._load_queue()
            violations = [ProtocolViolation.from_dict(v) for v in data["violations"]]

        for v in violations:
            print(f"[{v.severity}] {v.violation_id}: {v.violation_type} ({v.stage})")
            print(f"    {v.description}")

    elif args.command == "report":
        report = queue.generate_report(format=args.format)
        if args.output:
            Path(args.output).write_text(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)

    elif args.command == "resolve":
        if queue.resolve_violation(args.violation_id, args.resolution):
            print(f"Resolved: {args.violation_id}")
        else:
            print(f"Violation not found: {args.violation_id}")

    elif args.command == "dismiss":
        if queue.dismiss_violation(args.violation_id, args.reason):
            print(f"Dismissed: {args.violation_id}")
        else:
            print(f"Violation not found: {args.violation_id}")

    elif args.command == "clear-resolved":
        removed = queue.clear_resolved()
        print(f"Removed {removed} resolved/dismissed violations")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
