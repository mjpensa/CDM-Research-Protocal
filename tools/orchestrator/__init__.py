"""
CDM Research Protocol - Python Orchestrator

Fully automated workflow orchestrator for bank research.
Works with Claude Code in VS Code to execute research stages.

Usage:
    from orchestrator import WorkflowOrchestrator

    orch = WorkflowOrchestrator()
    orch.run_bank("deutsche-bank", phase=1)
"""

from .workflow import WorkflowOrchestrator
from .prompt_assembler import PromptAssembler
from .output_validator import OutputValidator, ValidationResult
from .checkpoint_engine import CheckpointEngine, CheckpointDecision

__all__ = [
    'WorkflowOrchestrator',
    'PromptAssembler',
    'OutputValidator',
    'ValidationResult',
    'CheckpointEngine',
    'CheckpointDecision',
]
