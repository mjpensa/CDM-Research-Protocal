"""
Tests for state_schema.py - State Management v1.1

Tests:
- from_dict() filtering of unknown fields
- Stage alias normalization
- Legacy 0-100 probability scale conversion to 0-1
- BankState and WorkflowState serialization
- Schema version handling
- Validation logic
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add tools directory to path
TOOLS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(TOOLS_DIR))

from state_schema import (
    BankState, WorkflowState, ProbabilityUpdate, CheckpointEvent,
    ErrorEvent, ReviewItem, STAGE_SEQUENCE, STAGE_ALIASES, normalize_stage
)
from state_manager import UnifiedStateManager


class TestStageAliases:
    """Test stage name normalization and aliases."""

    def test_normalize_stage_canonical_names(self):
        """Canonical names should pass through unchanged."""
        for stage in STAGE_SEQUENCE:
            assert normalize_stage(stage) == stage

    def test_normalize_stage_legacy_bayesian(self):
        """Legacy bayesian_t* names should normalize to bayesian_*."""
        assert normalize_stage("bayesian_t1") == "bayesian_1"
        assert normalize_stage("bayesian_t2") == "bayesian_2"
        assert normalize_stage("bayesian_t3") == "bayesian_3"

    def test_normalize_stage_legacy_init(self):
        """Legacy init/initialized should normalize to initialize."""
        assert normalize_stage("init") == "initialize"
        assert normalize_stage("initialized") == "initialize"

    def test_normalize_stage_legacy_adversarial(self):
        """Legacy 'adversarial' should normalize to 'adversarial_challenge'."""
        assert normalize_stage("adversarial") == "adversarial_challenge"

    def test_normalize_stage_unknown(self):
        """Unknown stages should pass through unchanged."""
        assert normalize_stage("unknown_stage") == "unknown_stage"
        assert normalize_stage("custom") == "custom"


class TestFromDictUnknownFields:
    """Test that from_dict filters unknown fields without crashing."""

    def test_probability_update_extra_fields(self):
        """ProbabilityUpdate.from_dict should ignore extra fields."""
        data = {
            "stage": "bayesian_1",
            "prior": 0.30,
            "posterior": 0.45,
            "combined_lr": 2.5,
            "evidence_count": 5,
            "timestamp": "2025-01-01T00:00:00+00:00",
            "extra_field": "should be ignored",
            "another_unknown": 123,
        }
        update = ProbabilityUpdate.from_dict(data)
        assert update.stage == "bayesian_1"
        assert update.prior == 0.30
        assert update.posterior == 0.45
        assert not hasattr(update, 'extra_field')

    def test_checkpoint_event_extra_fields(self):
        """CheckpointEvent.from_dict should ignore extra fields."""
        data = {
            "checkpoint_id": "gate_1",
            "checkpoint_name": "Gate 1",
            "bank_id": "test-bank",
            "stage": "gate_1",
            "action": "auto_proceed",
            "condition_met": "P > 80%",
            "unknown_field": "ignored",
        }
        event = CheckpointEvent.from_dict(data)
        assert event.checkpoint_id == "gate_1"
        assert not hasattr(event, 'unknown_field')

    def test_error_event_extra_fields(self):
        """ErrorEvent.from_dict should ignore extra fields."""
        data = {
            "bank_id": "test-bank",
            "stage": "tier1_evidence",
            "error_type": "APIError",
            "error_message": "Rate limit exceeded",
            "future_field": "v2.0 feature",
        }
        event = ErrorEvent.from_dict(data)
        assert event.bank_id == "test-bank"
        assert not hasattr(event, 'future_field')

    def test_review_item_extra_fields(self):
        """ReviewItem.from_dict should ignore extra fields."""
        data = {
            "bank_id": "test-bank",
            "bank_name": "Test Bank",
            "phase": 1,
            "checkpoint": "final",
            "reason": "Low confidence",
            "provisional_classification": "PRAGMATIST",
            "provisional_confidence": 45.0,
            "probability_architect": 0.45,
            "evidence_count": 10,
            "deprecated_field": "old format",
        }
        item = ReviewItem.from_dict(data)
        assert item.bank_id == "test-bank"
        assert not hasattr(item, 'deprecated_field')

    def test_bank_state_extra_fields(self):
        """BankState.from_dict should ignore extra fields."""
        data = {
            "bank_id": "test-bank",
            "bank_name": "Test Bank",
            "phase": 1,
            "current_probability": 0.45,
            "current_stage": "bayesian_1",
            "stages_completed": ["initialize", "tier1_evidence"],
            "legacy_field": "from old version",
            "removed_in_v2": True,
        }
        state = BankState.from_dict(data)
        assert state.bank_id == "test-bank"
        assert not hasattr(state, 'legacy_field')
        assert not hasattr(state, 'removed_in_v2')

    def test_workflow_state_extra_fields(self):
        """WorkflowState.from_dict should ignore extra fields."""
        data = {
            "execution_mode": "phase_pilot",
            "current_phase": 1,
            "banks_completed": ["bank-a"],
            "banks_pending": ["bank-b", "bank-c"],
            "obsolete_tracking": {"old": "data"},
        }
        state = WorkflowState.from_dict(data)
        assert state.execution_mode == "phase_pilot"
        assert not hasattr(state, 'obsolete_tracking')


class TestBankStateStageNormalization:
    """Test that BankState normalizes legacy stage names on load."""

    def test_current_stage_normalization(self):
        """current_stage should be normalized from legacy format."""
        data = {
            "bank_id": "test-bank",
            "bank_name": "Test Bank",
            "phase": 1,
            "current_stage": "bayesian_t1",  # Legacy format
        }
        state = BankState.from_dict(data)
        assert state.current_stage == "bayesian_1"  # Normalized

    def test_stages_completed_normalization(self):
        """stages_completed should have all stages normalized."""
        data = {
            "bank_id": "test-bank",
            "bank_name": "Test Bank",
            "phase": 1,
            "stages_completed": ["init", "tier1_evidence", "bayesian_t1"],
        }
        state = BankState.from_dict(data)
        assert state.stages_completed == ["initialize", "tier1_evidence", "bayesian_1"]

    def test_skipped_stages_normalization(self):
        """skipped_stages should have all stages normalized."""
        data = {
            "bank_id": "test-bank",
            "bank_name": "Test Bank",
            "phase": 1,
            "skipped_stages": ["bayesian_t2", "bayesian_t3"],
        }
        state = BankState.from_dict(data)
        assert state.skipped_stages == ["bayesian_2", "bayesian_3"]


class TestLegacyProbabilityConversion:
    """Test that legacy 0-100 probability scale is converted to 0-1."""

    def test_legacy_probability_conversion(self):
        """Legacy 0-100 probabilities should be converted to 0-1."""
        data = {
            "bank_id": "test-bank",
            "bank_name": "Test Bank",
            "phase": 1,
            "prior_probability": 30.0,  # Legacy 0-100
            "current_probability": 65.0,  # Legacy 0-100
        }
        state = BankState.from_dict(data)
        assert state.prior_probability == 0.30
        assert state.current_probability == 0.65

    def test_already_normalized_probability(self):
        """Probabilities already in 0-1 scale should not be changed."""
        data = {
            "bank_id": "test-bank",
            "bank_name": "Test Bank",
            "phase": 1,
            "prior_probability": 0.30,
            "current_probability": 0.65,
        }
        state = BankState.from_dict(data)
        assert state.prior_probability == 0.30
        assert state.current_probability == 0.65


class TestSchemaVersion:
    """Test schema version handling."""

    def test_schema_version_set_on_new_state(self):
        """New BankState should have schema_version set."""
        from state_schema import SCHEMA_VERSION
        state = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
        )
        assert state.schema_version == SCHEMA_VERSION

    def test_schema_version_preserved_on_load(self):
        """Schema version should be set even when loading old data."""
        from state_schema import SCHEMA_VERSION
        data = {
            "bank_id": "test-bank",
            "bank_name": "Test Bank",
            "phase": 1,
            # No schema_version in old data
        }
        state = BankState.from_dict(data)
        assert state.schema_version == SCHEMA_VERSION

    def test_schema_version_in_serialization(self):
        """Schema version should appear in to_dict output."""
        state = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
        )
        data = state.to_dict()
        assert "schema_version" in data


class TestWorkflowStateNormalization:
    """Test WorkflowState handles legacy formats."""

    def test_current_stage_normalization(self):
        """current_stage should be normalized."""
        data = {
            "current_stage": "adversarial",  # Legacy format
        }
        state = WorkflowState.from_dict(data)
        assert state.current_stage == "adversarial_challenge"

    def test_phase_status_key_conversion(self):
        """phase_status keys should be converted from strings to ints."""
        data = {
            "phase_status": {"1": "complete", "2": "in_progress"},
        }
        state = WorkflowState.from_dict(data)
        assert state.phase_status == {1: "complete", 2: "in_progress"}
        assert isinstance(list(state.phase_status.keys())[0], int)


class TestBankStateSerialization:
    """Test BankState round-trip serialization."""

    def test_to_dict_from_dict_roundtrip(self):
        """BankState should survive to_dict/from_dict roundtrip."""
        original = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
            current_probability=0.65,
            current_stage="gate_1",
            stages_completed=["initialize", "tier1_evidence", "bayesian_1"],
            classification="ARCHITECT",
            confidence=72,
        )

        # Add probability history
        original.probability_history.append(ProbabilityUpdate(
            stage="bayesian_1",
            prior=0.30,
            posterior=0.65,
            combined_lr=3.5,
            evidence_count=4,
        ))

        # Round-trip
        data = original.to_dict()
        restored = BankState.from_dict(data)

        assert restored.bank_id == original.bank_id
        assert restored.current_probability == original.current_probability
        assert restored.stages_completed == original.stages_completed
        assert len(restored.probability_history) == 1
        assert restored.probability_history[0].posterior == 0.65

    def test_probability_history_preserved(self):
        """Probability history should be properly serialized and deserialized."""
        state = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
        )

        # Add multiple updates
        state.update_probability(0.45, 1.5, 3, "bayesian_1")
        state.update_probability(0.60, 1.8, 4, "bayesian_2")

        data = state.to_dict()
        restored = BankState.from_dict(data)

        assert len(restored.probability_history) == 2
        assert restored.probability_history[0].posterior == 0.45
        assert restored.probability_history[1].posterior == 0.60
        assert restored.current_probability == 0.60


class TestBankStateValidation:
    """Test validation logic in state_manager."""

    @pytest.fixture
    def state_manager(self, tmp_path):
        """Create a state manager with temp directory."""
        return UnifiedStateManager(tmp_path)

    def test_valid_state_no_errors(self, state_manager):
        """Valid state should produce no validation errors."""
        state = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
            current_probability=0.65,
            current_stage="bayesian_1",
            stages_completed=["initialize", "tier1_evidence"],
        )
        errors = state_manager.validate_bank_state(state)
        assert errors == []

    def test_invalid_probability_detected(self, state_manager):
        """Invalid probability should be detected."""
        state = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
            current_probability=1.5,  # Invalid: > 1.0
            current_stage="initialize",
        )
        errors = state_manager.validate_bank_state(state)
        assert any("Invalid probability" in e for e in errors)

    def test_invalid_stage_detected(self, state_manager):
        """Invalid stage name should be detected."""
        state = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
            current_stage="nonexistent_stage",
        )
        errors = state_manager.validate_bank_state(state)
        assert any("Invalid stage" in e for e in errors)

    def test_invalid_confidence_detected(self, state_manager):
        """Invalid confidence should be detected."""
        state = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
            current_stage="initialize",
            confidence=150,  # Invalid: > 100
        )
        errors = state_manager.validate_bank_state(state)
        assert any("Invalid confidence" in e for e in errors)

    def test_blocked_state_consistency(self, state_manager):
        """Blocked state without checkpoint/reason should be detected."""
        state = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
            current_stage="initialize",
        )
        state.blocked_at = datetime.now(timezone.utc).isoformat()
        # Missing blocked_checkpoint and blocked_reason

        errors = state_manager.validate_bank_state(state)
        assert any("blocked_checkpoint is None" in e for e in errors)
        assert any("blocked_reason is None" in e for e in errors)

    def test_probability_history_consistency(self, state_manager):
        """Probability history mismatch should be detected."""
        state = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
            current_probability=0.65,
            current_stage="bayesian_1",
        )
        # Add update with different posterior
        state.probability_history.append(ProbabilityUpdate(
            stage="bayesian_1",
            prior=0.30,
            posterior=0.50,  # Doesn't match current_probability
            combined_lr=2.0,
            evidence_count=3,
        ))

        errors = state_manager.validate_bank_state(state)
        assert any("doesn't match" in e for e in errors)

    def test_invalid_classification_detected(self, state_manager):
        """Invalid classification should be detected."""
        state = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
            current_stage="initialize",
            classification="INVALID_TYPE",
        )
        errors = state_manager.validate_bank_state(state)
        assert any("Invalid classification" in e for e in errors)


class TestStateAdapter:
    """Test state_adapter.py conversion functions."""

    def test_convert_research_state_dict(self):
        """Test converting ResearchState-like dict to BankState."""
        from state_adapter import convert_research_state_to_bank_state

        research_data = {
            "bank_id": "deutsche-bank",
            "bank_name": "Deutsche Bank",
            "phase": 1,
            "probability_architect": 65.0,  # 0-100 scale
            "probability_pragmatist": 35.0,
            "classification": "ARCHITECT",
            "sub_classification": "Follower",
            "confidence": 72,
            "current_stage": "bayesian_t1",  # Legacy name
            "stages_completed": ["init", "tier1_evidence"],  # Legacy names
            "highest_tier": 1,
            "adversarial_verdict": "SUSTAINED",
            "trust_flags": ["SINGLE_SOURCE"],
            "errors": [],
        }

        bank_state = convert_research_state_to_bank_state(research_data)

        assert bank_state.bank_id == "deutsche-bank"
        assert bank_state.current_probability == 0.65  # Converted to 0-1 scale
        assert bank_state.current_stage == "bayesian_1"  # Normalized
        assert bank_state.stages_completed == ["initialize", "tier1_evidence"]  # Normalized
        assert bank_state.classification == "ARCHITECT"
        assert bank_state.classification_variant == "Follower"

    def test_sync_preserves_history(self):
        """Test that sync preserves probability history."""
        from state_adapter import sync_research_state_to_bank_state

        existing = BankState(
            bank_id="test-bank",
            bank_name="Test Bank",
            phase=1,
            current_probability=0.30,
            current_stage="initialize",
        )

        research_data = {
            "probability_architect": 45.0,
            "classification": None,
            "sub_classification": None,
            "confidence": None,
            "current_stage": "bayesian_1",
            "stages_completed": ["initialize", "tier1_evidence"],
            "highest_tier": 1,
        }

        updated = sync_research_state_to_bank_state(
            research_data,
            existing,
            stage="bayesian_1"
        )

        assert updated.current_probability == 0.45
        assert len(updated.probability_history) == 1
        assert updated.probability_history[0].prior == 0.30
        assert updated.probability_history[0].posterior == 0.45


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
