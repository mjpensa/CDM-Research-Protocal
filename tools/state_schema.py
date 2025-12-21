"""
CDM Research Protocol - Unified State Schema v1.1

Dataclasses defining the structure of all workflow state.
Single source of truth for state across all orchestration tools.

IMPORTANT: This is the canonical state format for the CDM Research Protocol.
All probabilities use 0-1 scale internally. For display, format as percentage.

Usage:
    from state_schema import BankState, ProbabilityUpdate, CheckpointEvent, ErrorEvent

    # Probabilities are 0-1 scale
    state.current_probability = 0.65  # 65%

    # For display:
    print(f"P(ARCHITECT): {state.current_probability * 100:.1f}%")
"""

from dataclasses import dataclass, field, asdict, fields
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from enum import Enum
import json


# Schema version for migration support
SCHEMA_VERSION = "1.1"


class StageStatus(Enum):
    """Status of a workflow stage."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    ERROR = "error"


class CheckpointAction(Enum):
    """Action taken at a checkpoint."""
    AUTO_PROCEED = "auto_proceed"
    BLOCK = "block"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"


# Stage sequence for reference - canonical names matching orchestrate.py
STAGE_SEQUENCE = [
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
    "adversarial_challenge",
    "final_classification",
    "synthesis",
    "complete"
]

# Aliases for backward compatibility with legacy stage names
STAGE_ALIASES = {
    # Old research_executor.py names -> canonical names
    "bayesian_t1": "bayesian_1",
    "bayesian_t2": "bayesian_2",
    "bayesian_t3": "bayesian_3",
    # Other legacy aliases
    "initialized": "initialize",
    "init": "initialize",
    "adversarial": "adversarial_challenge",
}


def normalize_stage(stage: str) -> str:
    """
    Normalize a stage name to its canonical form.

    Args:
        stage: Stage name (may be legacy alias)

    Returns:
        Canonical stage name
    """
    return STAGE_ALIASES.get(stage, stage)


@dataclass
class ProbabilityUpdate:
    """Record of a probability update after evidence gathering."""
    stage: str
    prior: float
    posterior: float
    combined_lr: float
    evidence_count: int
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ProbabilityUpdate':
        """Create from dictionary, filtering unknown fields for forward compatibility."""
        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)


@dataclass
class CheckpointEvent:
    """Record of a checkpoint decision."""
    checkpoint_id: str
    checkpoint_name: str
    bank_id: str
    stage: str
    action: str  # CheckpointAction value
    condition_met: str
    classification: Optional[str] = None
    variant: Optional[str] = None
    confidence: Optional[float] = None
    rationale: Optional[str] = None
    human_decision: Optional[str] = None
    files_written: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'CheckpointEvent':
        """Create from dictionary, filtering unknown fields for forward compatibility."""
        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)


@dataclass
class ErrorEvent:
    """Record of an error during execution."""
    bank_id: str
    stage: str
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    recovery_action: Optional[str] = None
    attempt: int = 1
    resolved: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ErrorEvent':
        """Create from dictionary, filtering unknown fields for forward compatibility."""
        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)


@dataclass
class ReviewItem:
    """Item in the batch review queue."""
    bank_id: str
    bank_name: str
    phase: int
    checkpoint: str
    reason: str
    provisional_classification: str
    provisional_confidence: float
    probability_architect: float
    evidence_count: int
    status: str = "pending"  # pending, approved, rejected, modified
    resolution: Optional[str] = None
    resolved_at: Optional[str] = None
    resolved_by: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ReviewItem':
        """Create from dictionary, filtering unknown fields for forward compatibility."""
        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)


@dataclass
class BankState:
    """
    Complete state of research for a bank.

    All probability values use 0-1 scale (not 0-100).
    For display, multiply by 100: f"{prob * 100:.1f}%"
    """
    bank_id: str
    bank_name: str
    phase: int
    schema_version: str = SCHEMA_VERSION  # For migration support
    execution_tier: str = "B"  # A, B, or C

    # Probability tracking (0-1 scale)
    prior_probability: float = 0.30  # Default 30% Architect
    current_probability: float = 0.30
    probability_history: List[ProbabilityUpdate] = field(default_factory=list)

    # Stage tracking
    stages_completed: List[str] = field(default_factory=list)
    current_stage: str = "initialize"
    skipped_stages: List[str] = field(default_factory=list)

    # Classification (set after final approval)
    classification: Optional[str] = None
    classification_variant: Optional[str] = None
    confidence: Optional[float] = None
    adversarial_verdict: Optional[str] = None

    # Timestamps
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None

    # Blocking
    blocked_at: Optional[str] = None
    blocked_reason: Optional[str] = None
    blocked_checkpoint: Optional[str] = None

    # Evidence tracking
    evidence_counts: Dict[str, int] = field(default_factory=lambda: {
        "tier1": 0, "tier2": 0, "tier3": 0, "null": 0
    })
    highest_tier: int = 0

    # Trust flags
    trust_flags: List[str] = field(default_factory=list)

    # Errors
    errors: List[str] = field(default_factory=list)

    # Phase 3: Stage progress tracking for resumability
    stage_started_at: Optional[str] = None  # When current stage began
    stage_outputs_written: List[str] = field(default_factory=list)  # Files created this stage
    last_checkpoint_at: Optional[str] = None  # Last successful checkpoint
    retry_count: int = 0  # Number of retries for current stage
    max_retries: int = 3  # Maximum retries before blocking

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Convert ProbabilityUpdate objects to dicts
        data['probability_history'] = [
            p.to_dict() if isinstance(p, ProbabilityUpdate) else p
            for p in self.probability_history
        ]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'BankState':
        """
        Create from dictionary (e.g., loaded from JSON).

        Handles:
        - Unknown fields (filtered out for forward compatibility)
        - Legacy stage name aliases (normalized to canonical form)
        - Legacy probability scales (0-100 converted to 0-1)
        - Nested ProbabilityUpdate objects
        - Missing schema_version (defaults to current)
        """
        # Get valid field names
        valid_fields = {f.name for f in fields(cls)}

        # Filter to only known fields
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        # Ensure schema_version is set
        if 'schema_version' not in filtered_data:
            filtered_data['schema_version'] = SCHEMA_VERSION

        # Handle legacy 0-100 probability scale (convert to 0-1)
        for prob_field in ['prior_probability', 'current_probability']:
            if prob_field in filtered_data and filtered_data[prob_field] is not None:
                if filtered_data[prob_field] > 1.0:
                    filtered_data[prob_field] = filtered_data[prob_field] / 100.0

        # Convert probability_history dicts to ProbabilityUpdate objects
        if 'probability_history' in filtered_data:
            filtered_data['probability_history'] = [
                ProbabilityUpdate.from_dict(p) if isinstance(p, dict) else p
                for p in filtered_data['probability_history']
            ]

        # Normalize stage names for backward compatibility
        if 'current_stage' in filtered_data:
            filtered_data['current_stage'] = normalize_stage(filtered_data['current_stage'])

        if 'stages_completed' in filtered_data:
            filtered_data['stages_completed'] = [
                normalize_stage(s) for s in filtered_data['stages_completed']
            ]

        if 'skipped_stages' in filtered_data:
            filtered_data['skipped_stages'] = [
                normalize_stage(s) for s in filtered_data['skipped_stages']
            ]

        return cls(**filtered_data)

    def update_probability(self, posterior: float, combined_lr: float,
                          evidence_count: int, stage: str) -> None:
        """Record a probability update."""
        update = ProbabilityUpdate(
            stage=stage,
            prior=self.current_probability,
            posterior=posterior,
            combined_lr=combined_lr,
            evidence_count=evidence_count
        )
        self.probability_history.append(update)
        self.current_probability = posterior
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def mark_stage_complete(self, stage: str) -> None:
        """Mark a stage as completed."""
        if stage not in self.stages_completed:
            self.stages_completed.append(stage)
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def mark_stage_skipped(self, stage: str) -> None:
        """Mark a stage as skipped."""
        if stage not in self.skipped_stages:
            self.skipped_stages.append(stage)
        self.last_updated = datetime.now(timezone.utc).isoformat()

    # Phase 3: Checkpoint methods for resumability
    def start_stage(self, stage: str) -> None:
        """Mark the beginning of a new stage."""
        self.current_stage = stage
        self.stage_started_at = datetime.now(timezone.utc).isoformat()
        self.stage_outputs_written = []
        self.retry_count = 0
        self.last_updated = self.stage_started_at

    def checkpoint_stage_progress(self, files_written: List[str] = None) -> None:
        """Record a checkpoint within the current stage."""
        self.last_checkpoint_at = datetime.now(timezone.utc).isoformat()
        if files_written:
            self.stage_outputs_written.extend(files_written)
        self.last_updated = self.last_checkpoint_at

    def increment_retry(self) -> bool:
        """Increment retry count. Returns False if max retries exceeded."""
        self.retry_count += 1
        self.last_updated = datetime.now(timezone.utc).isoformat()
        return self.retry_count <= self.max_retries

    def is_stage_timed_out(self, timeout_minutes: int = 30) -> bool:
        """
        Check if current stage has exceeded timeout.

        Args:
            timeout_minutes: Maximum allowed time for stage (default 30 min)

        Returns:
            True if stage has timed out, False otherwise
        """
        if not self.stage_started_at:
            return False

        if self.current_stage == "complete":
            return False

        try:
            started = datetime.fromisoformat(self.stage_started_at.replace('Z', '+00:00'))
            elapsed = (datetime.now(timezone.utc) - started).total_seconds() / 60
            return elapsed > timeout_minutes
        except (ValueError, AttributeError):
            return False

    def get_stage_elapsed_minutes(self) -> Optional[float]:
        """Get elapsed time for current stage in minutes."""
        if not self.stage_started_at:
            return None
        try:
            started = datetime.fromisoformat(self.stage_started_at.replace('Z', '+00:00'))
            return (datetime.now(timezone.utc) - started).total_seconds() / 60
        except (ValueError, AttributeError):
            return None

    def set_blocked(self, checkpoint: str, reason: str) -> None:
        """Set the bank as blocked at a checkpoint."""
        self.blocked_at = datetime.now(timezone.utc).isoformat()
        self.blocked_checkpoint = checkpoint
        self.blocked_reason = reason
        self.last_updated = self.blocked_at

    def clear_block(self) -> None:
        """Clear the blocked status."""
        self.blocked_at = None
        self.blocked_checkpoint = None
        self.blocked_reason = None
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def add_error(self, error: str) -> None:
        """Add an error message."""
        self.errors.append(error)
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def is_complete(self) -> bool:
        """Check if research is complete."""
        return self.completed_at is not None or "complete" in self.stages_completed

    def is_blocked(self) -> bool:
        """Check if research is blocked."""
        return self.blocked_at is not None

    def get_next_stage(self) -> Optional[str]:
        """Get the next stage in sequence."""
        if self.current_stage == "complete":
            return None

        try:
            current_idx = STAGE_SEQUENCE.index(self.current_stage)
            if current_idx < len(STAGE_SEQUENCE) - 1:
                return STAGE_SEQUENCE[current_idx + 1]
        except ValueError:
            pass

        return None


@dataclass
class WorkflowState:
    """Master workflow state tracking all phases and banks."""
    schema_version: str = SCHEMA_VERSION  # For migration support
    execution_mode: str = "full_rollout"  # single_bank_test, phase_pilot, full_rollout
    current_phase: int = 1
    current_bank: Optional[str] = None
    current_stage: Optional[str] = None

    banks_completed: List[str] = field(default_factory=list)
    banks_in_progress: List[str] = field(default_factory=list)
    banks_pending: List[str] = field(default_factory=list)
    banks_blocked: List[str] = field(default_factory=list)

    phase_status: Dict[int, str] = field(default_factory=dict)  # phase: status

    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    execution_log: List[Dict[str, str]] = field(default_factory=list)

    notes: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'WorkflowState':
        """
        Create from dictionary, filtering unknown fields for forward compatibility.

        Handles:
        - Unknown fields (filtered out)
        - phase_status key conversion (JSON stringifies int keys)
        - Legacy stage name normalization
        """
        # Get valid field names
        valid_fields = {f.name for f in fields(cls)}

        # Filter to only known fields
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        # Convert phase_status keys back to int (JSON stringifies int keys)
        if 'phase_status' in filtered_data:
            filtered_data['phase_status'] = {
                int(k): v for k, v in filtered_data['phase_status'].items()
            }

        # Normalize current_stage if present
        if 'current_stage' in filtered_data and filtered_data['current_stage']:
            filtered_data['current_stage'] = normalize_stage(filtered_data['current_stage'])

        return cls(**filtered_data)

    def log_event(self, event: str, details: str) -> None:
        """Log a workflow event."""
        self.execution_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "details": details
        })
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def mark_bank_started(self, bank_id: str) -> None:
        """Mark a bank as in progress."""
        if bank_id in self.banks_pending:
            self.banks_pending.remove(bank_id)
        if bank_id not in self.banks_in_progress:
            self.banks_in_progress.append(bank_id)
        self.current_bank = bank_id
        self.log_event("bank_started", f"Started research for {bank_id}")

    def mark_bank_completed(self, bank_id: str) -> None:
        """Mark a bank as completed."""
        if bank_id in self.banks_in_progress:
            self.banks_in_progress.remove(bank_id)
        if bank_id in self.banks_blocked:
            self.banks_blocked.remove(bank_id)
        if bank_id not in self.banks_completed:
            self.banks_completed.append(bank_id)
        self.log_event("bank_completed", f"Completed research for {bank_id}")

    def mark_bank_blocked(self, bank_id: str) -> None:
        """Mark a bank as blocked."""
        if bank_id in self.banks_in_progress:
            self.banks_in_progress.remove(bank_id)
        if bank_id not in self.banks_blocked:
            self.banks_blocked.append(bank_id)
        self.log_event("bank_blocked", f"Bank {bank_id} blocked at checkpoint")

    def mark_bank_unblocked(self, bank_id: str) -> None:
        """Mark a bank as unblocked and return it to in-progress state."""
        if bank_id in self.banks_blocked:
            self.banks_blocked.remove(bank_id)
        if bank_id not in self.banks_in_progress:
            self.banks_in_progress.append(bank_id)
        self.log_event("bank_unblocked", f"Bank {bank_id} unblocked and resumed")


# Utility functions for JSON serialization
def state_to_json(state: BankState) -> str:
    """Convert BankState to JSON string."""
    return json.dumps(state.to_dict(), indent=2)


def state_from_json(json_str: str) -> BankState:
    """Load BankState from JSON string."""
    return BankState.from_dict(json.loads(json_str))


def workflow_to_json(state: WorkflowState) -> str:
    """Convert WorkflowState to JSON string."""
    return json.dumps(state.to_dict(), indent=2)


def workflow_from_json(json_str: str) -> WorkflowState:
    """Load WorkflowState from JSON string."""
    return WorkflowState.from_dict(json.loads(json_str))
