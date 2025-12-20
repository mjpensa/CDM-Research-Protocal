"""
CDM Research Protocol - Structured Audit Logger v1.0

Comprehensive audit logging for CDM research workflow.
Creates machine-readable audit trail of all decisions.

This tool logs:
- Stage transitions
- Evidence findings (and informative absences)
- Bayesian probability updates with calculation details
- Gate decisions and reasoning
- Adversarial verdicts
- Checkpoint blocks and approvals
- Search queries executed
- Errors and warnings

Usage:
    from audit_logger import AuditLogger, EventType

    logger = AuditLogger(Path("outputs/bank"))
    logger.log_stage_start("tier1_evidence")
    logger.log_search("tier1_evidence", "site:isda.org bank CDM", 3, ["E001", "E002"])
    logger.log_bayesian_update("bayesian_1", 30.0, [...], 14.7, 86.4)
    logger.log_gate_decision("gate_1", 86.4, "skip_to_adversarial", "P > 80%")
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Optional, Any
from enum import Enum

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
module_logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of audit events."""
    # Stage lifecycle
    STAGE_START = "stage_start"
    STAGE_COMPLETE = "stage_complete"
    STAGE_SKIPPED = "stage_skipped"

    # Evidence events
    EVIDENCE_FOUND = "evidence_found"
    EVIDENCE_ABSENT = "evidence_absent"
    EVIDENCE_VERIFIED = "evidence_verified"
    EVIDENCE_FAILED = "evidence_failed"

    # Bayesian events
    BAYESIAN_UPDATE = "bayesian_update"
    LR_CALCULATED = "lr_calculated"

    # Gate events
    GATE_DECISION = "gate_decision"
    OBSERVABLE_IMPLICATION_CHECK = "observable_implication_check"

    # Adversarial events
    ADVERSARIAL_VERDICT = "adversarial_verdict"
    DISCONFIRMING_SEARCH = "disconfirming_search"
    STEELMAN_ARGUMENT = "steelman_argument"

    # Checkpoint events
    CHECKPOINT_BLOCK = "checkpoint_block"
    CHECKPOINT_APPROVED = "checkpoint_approved"
    CHECKPOINT_OVERRIDE = "checkpoint_override"

    # Search events
    SEARCH_EXECUTED = "search_executed"
    SEARCH_NO_RESULTS = "search_no_results"
    DEAD_END_AVOIDED = "dead_end_avoided"

    # Classification events
    CLASSIFICATION_SET = "classification_set"
    CLASSIFICATION_CHANGED = "classification_changed"
    CONFIDENCE_UPDATED = "confidence_updated"

    # Error events
    ERROR = "error"
    WARNING = "warning"

    # Verification events
    URL_VERIFIED = "url_verified"
    URL_FAILED = "url_failed"
    CONTENT_DRIFT = "content_drift"


@dataclass
class AuditEvent:
    """A single audit event."""
    timestamp: str
    bank_id: str
    event_type: str
    stage: str
    details: dict = field(default_factory=dict)
    severity: str = "info"  # info, warning, error

    def to_dict(self) -> dict:
        return asdict(self)


class AuditLogger:
    """
    Comprehensive audit logging for CDM research workflow.

    Creates machine-readable audit trail stored in audit-log.json.
    """

    def __init__(self, bank_dir: Path):
        """
        Initialize audit logger for a bank.

        Args:
            bank_dir: Path to bank output directory
        """
        self.bank_dir = Path(bank_dir)
        self.log_path = self.bank_dir / "audit-log.json"
        self.bank_id = self.bank_dir.name
        self.events: list[AuditEvent] = []
        self._load_existing()

    def _load_existing(self):
        """Load existing audit log if present."""
        if self.log_path.exists():
            try:
                data = json.loads(self.log_path.read_text(encoding='utf-8'))
                self.events = [
                    AuditEvent(**e) for e in data.get('events', [])
                ]
                module_logger.debug(f"Loaded {len(self.events)} existing events")
            except (json.JSONDecodeError, KeyError) as e:
                module_logger.warning(f"Failed to load existing audit log: {e}")
                self.events = []

    def _save(self):
        """Save audit log to file."""
        # Ensure directory exists
        self.bank_dir.mkdir(parents=True, exist_ok=True)

        data = {
            "bank_id": self.bank_id,
            "event_count": len(self.events),
            "first_event": self.events[0].timestamp if self.events else None,
            "last_updated": datetime.utcnow().isoformat(),
            "events": [e.to_dict() for e in self.events]
        }
        self.log_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def log(self, event_type: EventType, stage: str, details: dict,
            severity: str = "info"):
        """
        Log an audit event.

        Args:
            event_type: Type of event (from EventType enum)
            stage: Current workflow stage
            details: Event-specific details dict
            severity: Event severity (info, warning, error)
        """
        event = AuditEvent(
            timestamp=datetime.utcnow().isoformat(),
            bank_id=self.bank_id,
            event_type=event_type.value,
            stage=stage,
            details=details,
            severity=severity
        )
        self.events.append(event)
        self._save()

        # Also log to console
        msg = f"[{event_type.value}] {stage}: {details.get('summary', str(details)[:100])}"
        if severity == "error":
            module_logger.error(msg)
        elif severity == "warning":
            module_logger.warning(msg)
        else:
            module_logger.debug(msg)

    # --- CONVENIENCE METHODS ---

    def log_stage_start(self, stage: str):
        """Log the start of a workflow stage."""
        self.log(EventType.STAGE_START, stage, {
            "summary": f"Started {stage}"
        })

    def log_stage_complete(self, stage: str, duration_seconds: Optional[float] = None):
        """Log completion of a workflow stage."""
        self.log(EventType.STAGE_COMPLETE, stage, {
            "summary": f"Completed {stage}",
            "duration_seconds": duration_seconds
        })

    def log_stage_skipped(self, stage: str, reason: str):
        """Log that a stage was skipped."""
        self.log(EventType.STAGE_SKIPPED, stage, {
            "summary": f"Skipped {stage}",
            "reason": reason
        })

    def log_search(self, stage: str, query: str, results_count: int,
                   evidence_ids: list[str]):
        """
        Log a search execution for reproducibility.

        Args:
            stage: Current stage
            query: Search query executed
            results_count: Number of results found
            evidence_ids: IDs of evidence items created
        """
        self.log(EventType.SEARCH_EXECUTED, stage, {
            "summary": f"Search: {query[:50]}... -> {results_count} results",
            "query": query,
            "results_count": results_count,
            "evidence_ids_created": evidence_ids
        })

    def log_no_results(self, stage: str, query: str, interpretation: str):
        """Log a search that returned no results (informative absence)."""
        self.log(EventType.SEARCH_NO_RESULTS, stage, {
            "summary": f"No results for: {query[:50]}...",
            "query": query,
            "interpretation": interpretation
        })

    def log_dead_end_avoided(self, stage: str, query: str, reason: str):
        """Log that a known dead-end search was avoided."""
        self.log(EventType.DEAD_END_AVOIDED, stage, {
            "summary": f"Avoided dead end: {query[:50]}...",
            "query": query,
            "reason": reason
        }, severity="info")

    def log_evidence_found(self, stage: str, evidence_id: str, claim: str,
                          tier: int, source_url: str):
        """Log discovery of evidence."""
        self.log(EventType.EVIDENCE_FOUND, stage, {
            "summary": f"Found T{tier} evidence: {claim[:50]}...",
            "evidence_id": evidence_id,
            "claim": claim,
            "tier": tier,
            "source_url": source_url
        })

    def log_evidence_verified(self, stage: str, evidence_id: str,
                             status: str, content_hash: Optional[str] = None):
        """Log URL verification result."""
        self.log(EventType.EVIDENCE_VERIFIED, stage, {
            "summary": f"Verified {evidence_id}: {status}",
            "evidence_id": evidence_id,
            "status": status,
            "content_hash": content_hash
        })

    def log_bayesian_update(self, stage: str, prior: float, lr_items: list[dict],
                           combined_lr: float, posterior: float):
        """
        Log detailed Bayesian calculation.

        Args:
            stage: Current stage (e.g., "bayesian_1")
            prior: Prior P(Architect) percentage
            lr_items: List of {evidence_id, evidence_type, lr} dicts
            combined_lr: Product of all likelihood ratios
            posterior: Posterior P(Architect) percentage
        """
        self.log(EventType.BAYESIAN_UPDATE, stage, {
            "summary": f"P(Architect): {prior:.1f}% -> {posterior:.1f}%",
            "prior_probability": prior,
            "likelihood_ratios": lr_items,
            "combined_lr": combined_lr,
            "posterior_probability": posterior,
            "calculation": f"Prior odds = {prior/(100-prior):.3f}, "
                          f"Combined LR = {combined_lr:.2f}, "
                          f"Posterior = {posterior:.1f}%"
        })

    def log_gate_decision(self, gate: str, probability: float,
                         decision: str, reason: str):
        """
        Log reasoning gate decision.

        Args:
            gate: Gate identifier (e.g., "gate_1")
            probability: Current P(Architect) percentage
            decision: Decision made (continue, skip_to_adversarial)
            reason: Reason for decision
        """
        self.log(EventType.GATE_DECISION, gate, {
            "summary": f"Gate decision: {decision}",
            "probability_architect": probability,
            "decision": decision,
            "reason": reason
        })

    def log_adversarial_verdict(self, stage: str, verdict: str,
                               confidence_adjustment: float, rationale: str):
        """
        Log adversarial challenge verdict.

        Args:
            stage: Should be "adversarial"
            verdict: STRENGTHENED, UNCHANGED, WEAKENED, or REVISED
            confidence_adjustment: Change to confidence (e.g., +5, -10)
            rationale: Why this verdict was reached
        """
        severity = "warning" if verdict == "REVISED" else "info"
        self.log(EventType.ADVERSARIAL_VERDICT, stage, {
            "summary": f"Adversarial verdict: {verdict} ({confidence_adjustment:+.1f}%)",
            "verdict": verdict,
            "confidence_adjustment": confidence_adjustment,
            "rationale": rationale
        }, severity=severity)

    def log_checkpoint_block(self, stage: str, checkpoint_id: str, reason: str):
        """Log that a checkpoint has blocked the workflow."""
        self.log(EventType.CHECKPOINT_BLOCK, stage, {
            "summary": f"BLOCKED: {reason}",
            "checkpoint_id": checkpoint_id,
            "reason": reason
        }, severity="warning")

    def log_checkpoint_approved(self, stage: str, checkpoint_id: str,
                               approver: str, notes: Optional[str] = None):
        """Log approval of a checkpoint."""
        self.log(EventType.CHECKPOINT_APPROVED, stage, {
            "summary": f"Approved: {checkpoint_id} by {approver}",
            "checkpoint_id": checkpoint_id,
            "approver": approver,
            "notes": notes
        })

    def log_classification(self, stage: str, classification: str,
                          sub_classification: str, confidence: float):
        """Log final classification."""
        self.log(EventType.CLASSIFICATION_SET, stage, {
            "summary": f"{classification} ({sub_classification}) at {confidence:.1f}%",
            "classification": classification,
            "sub_classification": sub_classification,
            "confidence": confidence
        })

    def log_error(self, stage: str, error: str, details: Optional[dict] = None):
        """Log an error."""
        self.log(EventType.ERROR, stage, {
            "summary": error,
            "error": error,
            **(details or {})
        }, severity="error")

    def log_warning(self, stage: str, warning: str, details: Optional[dict] = None):
        """Log a warning."""
        self.log(EventType.WARNING, stage, {
            "summary": warning,
            "warning": warning,
            **(details or {})
        }, severity="warning")

    def log_content_drift(self, stage: str, evidence_id: str,
                         old_hash: str, new_hash: str):
        """Log content drift detection."""
        self.log(EventType.CONTENT_DRIFT, stage, {
            "summary": f"Content changed for {evidence_id}",
            "evidence_id": evidence_id,
            "old_hash": old_hash[:16] + "...",
            "new_hash": new_hash[:16] + "..."
        }, severity="warning")

    # --- QUERY METHODS ---

    def get_timeline(self) -> list[dict]:
        """Return chronological event timeline."""
        return [e.to_dict() for e in sorted(self.events, key=lambda e: e.timestamp)]

    def get_events_by_type(self, event_type: EventType) -> list[dict]:
        """Get all events of a specific type."""
        return [
            e.to_dict() for e in self.events
            if e.event_type == event_type.value
        ]

    def get_events_by_stage(self, stage: str) -> list[dict]:
        """Get all events for a specific stage."""
        return [
            e.to_dict() for e in self.events
            if e.stage == stage
        ]

    def get_errors_and_warnings(self) -> list[dict]:
        """Get all error and warning events."""
        return [
            e.to_dict() for e in self.events
            if e.severity in ("error", "warning")
        ]

    def get_search_history(self) -> list[dict]:
        """Get all search queries executed."""
        return self.get_events_by_type(EventType.SEARCH_EXECUTED)

    def get_bayesian_history(self) -> list[dict]:
        """Get all Bayesian updates."""
        return self.get_events_by_type(EventType.BAYESIAN_UPDATE)

    def get_summary(self) -> dict:
        """Get summary statistics of the audit log."""
        type_counts = {}
        for e in self.events:
            type_counts[e.event_type] = type_counts.get(e.event_type, 0) + 1

        return {
            "bank_id": self.bank_id,
            "total_events": len(self.events),
            "events_by_type": type_counts,
            "error_count": len([e for e in self.events if e.severity == "error"]),
            "warning_count": len([e for e in self.events if e.severity == "warning"]),
            "first_event": self.events[0].timestamp if self.events else None,
            "last_event": self.events[-1].timestamp if self.events else None
        }


# --- CLI ---

def main():
    """CLI entry point for viewing audit logs."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python audit_logger.py <bank_directory> [--summary|--timeline|--errors]")
        sys.exit(1)

    bank_dir = Path(sys.argv[1])
    logger = AuditLogger(bank_dir)

    if '--summary' in sys.argv or len(sys.argv) == 2:
        summary = logger.get_summary()
        print(f"\nAudit Log Summary: {summary['bank_id']}")
        print(f"{'='*50}")
        print(f"Total events: {summary['total_events']}")
        print(f"Errors: {summary['error_count']}")
        print(f"Warnings: {summary['warning_count']}")
        print(f"\nEvents by type:")
        for etype, count in sorted(summary['events_by_type'].items()):
            print(f"  {etype}: {count}")

    elif '--timeline' in sys.argv:
        timeline = logger.get_timeline()
        for event in timeline:
            print(f"[{event['timestamp']}] [{event['event_type']}] {event['stage']}")
            print(f"  {event['details'].get('summary', '')}")

    elif '--errors' in sys.argv:
        issues = logger.get_errors_and_warnings()
        if not issues:
            print("No errors or warnings found.")
        else:
            for event in issues:
                print(f"[{event['severity'].upper()}] [{event['stage']}] {event['details'].get('summary', '')}")

    elif '--searches' in sys.argv:
        searches = logger.get_search_history()
        print(f"\nSearch History ({len(searches)} queries):")
        for s in searches:
            print(f"  [{s['stage']}] {s['details'].get('query', 'N/A')[:60]}...")
            print(f"    Results: {s['details'].get('results_count', 0)}")


if __name__ == "__main__":
    main()
