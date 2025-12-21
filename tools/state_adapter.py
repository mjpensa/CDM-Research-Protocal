"""
CDM Research Protocol - State Adapter v1.1

Adapters for converting between legacy state formats and the unified BankState schema.
Enables gradual migration from research_executor.py's ResearchState and
orchestrate.py's WorkflowState to the unified state_schema.py types.

NOTE: As of v1.1, all probability values use 0-1 scale internally.
Legacy 0-100 scale values are automatically converted on load.

Usage:
    from state_adapter import convert_research_state_to_bank_state

    # After research_executor completes:
    bank_state = convert_research_state_to_bank_state(research_state)
    state_manager.save_bank_state(bank_state)
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from state_schema import (
    BankState, ProbabilityUpdate, normalize_stage, STAGE_SEQUENCE
)


def convert_research_state_to_bank_state(
    research_state: Any,
    prior_probability: float = 0.30,
    execution_tier: str = "B"
) -> BankState:
    """
    Convert ResearchState from research_executor.py to unified BankState.

    Args:
        research_state: ResearchState instance or dict from research_executor.py
        prior_probability: Prior probability to use (default 30%)
        execution_tier: Execution tier A/B/C (default B)

    Returns:
        BankState instance

    Note:
        ResearchState fields:
        - bank_id, bank_name, phase
        - probability_architect (0-100 scale), probability_pragmatist
        - classification, sub_classification, confidence
        - current_stage, stages_completed, evidence_items
        - highest_tier, adversarial_verdict, trust_flags
        - errors, started_at, completed_at
    """
    # Handle both object and dict inputs
    if hasattr(research_state, '__dict__'):
        data = research_state.__dict__
    elif hasattr(research_state, 'bank_id'):
        # Dataclass - access attributes directly
        data = {
            'bank_id': research_state.bank_id,
            'bank_name': research_state.bank_name,
            'phase': research_state.phase,
            'probability_architect': research_state.probability_architect,
            'probability_pragmatist': getattr(research_state, 'probability_pragmatist', None),
            'classification': research_state.classification,
            'sub_classification': getattr(research_state, 'sub_classification', None),
            'confidence': research_state.confidence,
            'current_stage': research_state.current_stage,
            'stages_completed': research_state.stages_completed,
            'highest_tier': research_state.highest_tier,
            'adversarial_verdict': getattr(research_state, 'adversarial_verdict', None),
            'trust_flags': getattr(research_state, 'trust_flags', []),
            'errors': getattr(research_state, 'errors', []),
            'started_at': getattr(research_state, 'started_at', None),
            'completed_at': getattr(research_state, 'completed_at', None),
        }
    else:
        data = research_state

    # Handle legacy 0-100 scale (convert to 0-1 if needed)
    prob_architect = data.get('probability_architect', 0.30)
    if prob_architect > 1.0:
        prob_architect = prob_architect / 100.0

    # Normalize stage names
    current_stage = normalize_stage(data.get('current_stage', 'initialize'))
    stages_completed = [
        normalize_stage(s) for s in data.get('stages_completed', [])
    ]

    # Build evidence counts from evidence_items if available
    evidence_counts = {"tier1": 0, "tier2": 0, "tier3": 0, "null": 0}
    evidence_items = data.get('evidence_items', [])
    if evidence_items:
        for item in evidence_items:
            if hasattr(item, 'tier'):
                tier = item.tier
            elif isinstance(item, dict):
                tier = item.get('tier', 0)
            else:
                continue

            if tier == 1:
                evidence_counts["tier1"] += 1
            elif tier == 2:
                evidence_counts["tier2"] += 1
            elif tier == 3:
                evidence_counts["tier3"] += 1

    # Create BankState
    bank_state = BankState(
        bank_id=data.get('bank_id', 'unknown'),
        bank_name=data.get('bank_name', data.get('bank_id', 'Unknown')),
        phase=data.get('phase', 1),
        execution_tier=execution_tier,
        prior_probability=prior_probability,
        current_probability=prob_architect,
        probability_history=[],  # Will be populated by state manager
        stages_completed=stages_completed,
        current_stage=current_stage,
        skipped_stages=[],
        classification=data.get('classification'),
        classification_variant=data.get('sub_classification'),
        confidence=data.get('confidence'),
        adversarial_verdict=data.get('adversarial_verdict'),
        started_at=data.get('started_at', datetime.now(timezone.utc).isoformat()),
        completed_at=data.get('completed_at'),
        evidence_counts=evidence_counts,
        highest_tier=data.get('highest_tier', 0),
        trust_flags=data.get('trust_flags', []),
        errors=data.get('errors', []),
    )

    # Initialize stage timing for timeout detection (Phase 3 migration)
    if bank_state.current_stage != "complete":
        bank_state.start_stage(bank_state.current_stage)

    return bank_state


def convert_orchestrate_state_to_bank_state(
    workflow_state: Any,
    bank_name: Optional[str] = None,
    phase: int = 1
) -> BankState:
    """
    Convert WorkflowState from orchestrate.py to unified BankState.

    Args:
        workflow_state: WorkflowState instance or dict from orchestrate.py
        bank_name: Bank display name (optional, derived from bank_id)
        phase: Phase number

    Returns:
        BankState instance

    Note:
        orchestrate.py WorkflowState fields:
        - bank_id, current_stage
        - probability_architect (0-100 scale)
        - classification, sub_classification, confidence
        - stages_completed, checkpoints_pending, checkpoints_approved
        - created_at, updated_at, errors, provenance
    """
    # Handle both object and dict inputs
    if hasattr(workflow_state, '__dict__'):
        data = workflow_state.__dict__
    elif hasattr(workflow_state, 'bank_id'):
        data = {
            'bank_id': workflow_state.bank_id,
            'current_stage': workflow_state.current_stage,
            'probability_architect': workflow_state.probability_architect,
            'classification': getattr(workflow_state, 'classification', None),
            'sub_classification': getattr(workflow_state, 'sub_classification', None),
            'confidence': getattr(workflow_state, 'confidence', 0.0),
            'stages_completed': getattr(workflow_state, 'stages_completed', []),
            'created_at': getattr(workflow_state, 'created_at', None),
            'updated_at': getattr(workflow_state, 'updated_at', None),
            'errors': getattr(workflow_state, 'errors', []),
        }
    else:
        data = workflow_state

    bank_id = data.get('bank_id', 'unknown')

    # Convert probability from 0-100 scale to 0-1 scale
    prob_architect = data.get('probability_architect', 30.0)
    if prob_architect > 1.0:
        prob_architect = prob_architect / 100.0

    # Normalize stage names
    current_stage = normalize_stage(data.get('current_stage', 'initialize'))
    stages_completed = [
        normalize_stage(s) for s in data.get('stages_completed', [])
    ]

    # Determine blocked status from checkpoints_pending
    blocked_checkpoint = None
    blocked_reason = None
    blocked_at = None
    checkpoints_pending = data.get('checkpoints_pending', [])
    if checkpoints_pending:
        blocked_checkpoint = checkpoints_pending[0] if isinstance(checkpoints_pending[0], str) else checkpoints_pending[0].get('id')
        blocked_reason = "Pending checkpoint approval"
        blocked_at = datetime.now(timezone.utc).isoformat()

    # Create BankState
    bank_state = BankState(
        bank_id=bank_id,
        bank_name=bank_name or bank_id.replace('-', ' ').title(),
        phase=phase,
        execution_tier="B",
        prior_probability=0.30,
        current_probability=prob_architect,
        probability_history=[],
        stages_completed=stages_completed,
        current_stage=current_stage,
        skipped_stages=[],
        classification=data.get('classification'),
        classification_variant=data.get('sub_classification'),
        confidence=data.get('confidence'),
        adversarial_verdict=None,
        started_at=data.get('created_at', datetime.now(timezone.utc).isoformat()),
        last_updated=data.get('updated_at', datetime.now(timezone.utc).isoformat()),
        completed_at=None,
        blocked_at=blocked_at,
        blocked_checkpoint=blocked_checkpoint,
        blocked_reason=blocked_reason,
        evidence_counts={"tier1": 0, "tier2": 0, "tier3": 0, "null": 0},
        highest_tier=0,
        trust_flags=[],
        errors=data.get('errors', []),
    )

    # Initialize stage timing for timeout detection (Phase 3 migration)
    if bank_state.current_stage != "complete":
        bank_state.start_stage(bank_state.current_stage)

    return bank_state


def sync_research_state_to_bank_state(
    research_state: Any,
    existing_bank_state: Optional[BankState] = None,
    stage: Optional[str] = None
) -> BankState:
    """
    Sync fields from ResearchState to an existing or new BankState.

    Preserves probability_history and other fields not in ResearchState.
    Used for incremental updates during research execution.

    Args:
        research_state: Current ResearchState from research_executor.py
        existing_bank_state: Existing BankState to update (or None to create new)
        stage: Current stage name for probability history tracking

    Returns:
        Updated BankState
    """
    if existing_bank_state is None:
        return convert_research_state_to_bank_state(research_state)

    # Handle both object and dict inputs
    if hasattr(research_state, 'probability_architect'):
        prob_architect = research_state.probability_architect
        classification = research_state.classification
        sub_classification = getattr(research_state, 'sub_classification', None)
        confidence = research_state.confidence
        current_stage = research_state.current_stage
        stages_completed = research_state.stages_completed
        highest_tier = research_state.highest_tier
        adversarial_verdict = getattr(research_state, 'adversarial_verdict', None)
        trust_flags = getattr(research_state, 'trust_flags', [])
        errors = getattr(research_state, 'errors', [])
        completed_at = getattr(research_state, 'completed_at', None)
    else:
        data = research_state
        prob_architect = data.get('probability_architect', 30.0)
        classification = data.get('classification')
        sub_classification = data.get('sub_classification')
        confidence = data.get('confidence')
        current_stage = data.get('current_stage', 'initialize')
        stages_completed = data.get('stages_completed', [])
        highest_tier = data.get('highest_tier', 0)
        adversarial_verdict = data.get('adversarial_verdict')
        trust_flags = data.get('trust_flags', [])
        errors = data.get('errors', [])
        completed_at = data.get('completed_at')

    # Convert probability from 0-100 scale to 0-1 scale
    if prob_architect > 1.0:
        prob_architect = prob_architect / 100.0

    # Track probability change if there's a significant difference
    if stage and abs(existing_bank_state.current_probability - prob_architect) > 0.001:
        update = ProbabilityUpdate(
            stage=normalize_stage(stage),
            prior=existing_bank_state.current_probability,
            posterior=prob_architect,
            combined_lr=1.0,  # Will be set by caller if known
            evidence_count=0,  # Will be set by caller if known
        )
        existing_bank_state.probability_history.append(update)

    # Update fields
    existing_bank_state.current_probability = prob_architect
    existing_bank_state.classification = classification
    existing_bank_state.classification_variant = sub_classification
    existing_bank_state.confidence = confidence
    existing_bank_state.current_stage = normalize_stage(current_stage)
    existing_bank_state.stages_completed = [normalize_stage(s) for s in stages_completed]
    existing_bank_state.highest_tier = highest_tier
    existing_bank_state.adversarial_verdict = adversarial_verdict
    existing_bank_state.trust_flags = trust_flags
    existing_bank_state.errors = errors
    existing_bank_state.last_updated = datetime.now(timezone.utc).isoformat()

    if completed_at:
        existing_bank_state.completed_at = completed_at

    return existing_bank_state


def extract_legacy_fields(bank_state: BankState) -> Dict[str, Any]:
    """
    Extract fields in legacy ResearchState format for backward compatibility.

    Useful when existing code expects the old format.

    Args:
        bank_state: BankState instance

    Returns:
        Dictionary with ResearchState-compatible fields
    """
    return {
        'bank_id': bank_state.bank_id,
        'bank_name': bank_state.bank_name,
        'phase': bank_state.phase,
        'probability_architect': bank_state.current_probability * 100,  # 0-100 scale
        'probability_pragmatist': (1.0 - bank_state.current_probability) * 100,
        'classification': bank_state.classification,
        'sub_classification': bank_state.classification_variant,
        'confidence': bank_state.confidence,
        'current_stage': bank_state.current_stage,
        'stages_completed': bank_state.stages_completed,
        'highest_tier': bank_state.highest_tier,
        'adversarial_verdict': bank_state.adversarial_verdict,
        'trust_flags': bank_state.trust_flags,
        'errors': bank_state.errors,
        'started_at': bank_state.started_at,
        'completed_at': bank_state.completed_at,
    }
