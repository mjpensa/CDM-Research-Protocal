#!/usr/bin/env python3
"""
CDM Research Orchestrator - Fully Automated Workflow Manager

Orchestrates the research protocol for banks with fully automated execution.
Human review happens only at the end of overnight runs, not during execution.

Usage:
    # See current status for a bank
    python tools/run_research.py status --bank deutsche-bank --phase 1

    # Get the full research prompt for a bank (for Claude Code execution)
    python tools/run_research.py prompt --bank deutsche-bank --phase 1

    # Get status for all banks in a phase
    python tools/run_research.py phase-status --phase 1

    # View deferred review queue
    python tools/run_research.py review-queue --phase 1

    # Initialize a bank for research
    python tools/run_research.py init --bank deutsche-bank --phase 1

    # Validate outputs for a bank
    python tools/run_research.py validate --bank deutsche-bank --phase 1

    # Clear state for re-running a bank
    python tools/run_research.py clear --bank deutsche-bank --phase 1

Examples:
    # Start research on Deutsche Bank
    python tools/run_research.py init --bank deutsche-bank --phase 1
    python tools/run_research.py prompt --bank deutsche-bank --phase 1 > prompt.md
    # Paste prompt.md contents into Claude Code

    # After Claude Code completes, validate and finalize
    python tools/run_research.py validate --bank deutsche-bank --phase 1
    python tools/run_research.py status --bank deutsche-bank --phase 1
"""

import sys
import json
import logging
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

import click

from orchestrator import (
    WorkflowOrchestrator,
    OutputValidator,
    CheckpointEngine,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(debug: bool):
    """CDM Research Orchestrator - Fully Automated Workflow Manager"""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)


@cli.command()
@click.option('--bank', required=True, help='Bank ID (e.g., deutsche-bank)')
@click.option('--phase', type=int, default=1, help='Phase number')
def status(bank: str, phase: int):
    """Show current research status for a bank."""
    orch = WorkflowOrchestrator()
    state = orch.get_status(bank, phase)

    if state is None:
        click.echo(f"\nNo research state found for {bank} (Phase {phase})")
        click.echo(f"Run 'run_research.py init --bank {bank} --phase {phase}' to initialize")
        return

    click.echo(f"\n{'='*60}")
    click.echo(f"Bank: {state.bank_name} ({state.bank_id})")
    click.echo(f"Phase: {phase}")
    click.echo(f"Execution Tier: {state.execution_tier}")
    click.echo(f"{'='*60}")
    click.echo(f"Current Stage: {state.current_stage}")
    click.echo(f"P(Architect): {state.current_probability:.1%}")
    click.echo(f"Stages Completed: {len(state.stages_completed)}/{len(state.stages_completed) + 1}")
    click.echo(f"Stages Skipped: {len(state.skipped_stages)}")

    if state.classification:
        click.echo(f"\nClassification: {state.classification}")
        if state.classification_variant:
            click.echo(f"Variant: {state.classification_variant}")
        if state.confidence:
            click.echo(f"Confidence: {state.confidence:.0f}%")

    if state.is_blocked():
        click.echo(f"\n[BLOCKED] {state.blocked_reason}")
        click.echo(f"   Checkpoint: {state.blocked_checkpoint}")

    if state.is_complete():
        click.echo(f"\n[OK] Research Complete")
        click.echo(f"  Completed: {state.completed_at}")

    # Evidence summary
    click.echo(f"\nEvidence Counts:")
    for tier, count in state.evidence_counts.items():
        click.echo(f"  {tier}: {count}")

    if state.trust_flags:
        click.echo(f"\nTrust Flags: {', '.join(state.trust_flags)}")

    if state.errors:
        click.echo(f"\nErrors: {len(state.errors)}")
        for err in state.errors[-3:]:  # Last 3 errors
            click.echo(f"  - {err}")

    click.echo(f"{'='*60}\n")


@cli.command()
@click.option('--bank', required=True, help='Bank ID')
@click.option('--phase', type=int, default=1, help='Phase number')
@click.option('--output', '-o', type=click.Path(), help='Output file (default: stdout)')
def prompt(bank: str, phase: int, output: str):
    """Generate the full research prompt for a bank."""
    orch = WorkflowOrchestrator()

    try:
        prompt_text = orch.get_full_research_prompt(bank, phase)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if output:
        Path(output).write_text(prompt_text, encoding='utf-8')
        click.echo(f"Prompt written to: {output}")
    else:
        click.echo(prompt_text)


@cli.command('phase-status')
@click.option('--phase', type=int, required=True, help='Phase number')
def phase_status(phase: int):
    """Show status for all banks in a phase."""
    orch = WorkflowOrchestrator()
    summary = orch.get_phase_summary(phase)

    click.echo(f"\n{'='*60}")
    click.echo(f"Phase {phase} Summary")
    click.echo(f"{'='*60}")
    click.echo(f"Total Banks: {summary['total_banks']}")
    click.echo(f"Completed: {summary['completed']}")
    click.echo(f"In Progress: {summary['in_progress']}")
    click.echo(f"Pending: {summary['pending']}")
    click.echo(f"Blocked: {summary['blocked']}")

    if summary['banks_completed']:
        click.echo(f"\n[COMPLETED]")
        for b in summary['banks_completed']:
            click.echo(f"  {b['bank_id']}: {b['classification']} @ {b['confidence']:.0f}%")

    if summary['banks_in_progress']:
        click.echo(f"\n[IN PROGRESS]")
        for b in summary['banks_in_progress']:
            click.echo(f"  {b['bank_id']}: {b['stage']} (P(A)={b['probability']:.1%})")

    if summary['banks_blocked']:
        click.echo(f"\n[BLOCKED]")
        for b in summary['banks_blocked']:
            click.echo(f"  {b['bank_id']}: {b['reason']}")

    if summary['banks_pending']:
        click.echo(f"\n[PENDING] {', '.join(summary['banks_pending'])}")

    # Review queue
    rq = summary['review_queue']
    if rq.get('total_items', 0) > 0:
        click.echo(f"\n[REVIEW QUEUE] {rq['total_items']} items")
        click.echo(f"   Critical: {rq.get('critical_count', 0)}")
        click.echo(f"   Warning: {rq.get('warning_count', 0)}")
        click.echo(f"   Info: {rq.get('info_count', 0)}")

    click.echo(f"{'='*60}\n")


@cli.command('review-queue')
@click.option('--phase', type=int, help='Filter by phase')
@click.option('--severity', type=click.Choice(['CRITICAL', 'WARNING', 'INFO']), help='Filter by severity')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def review_queue(phase: int, severity: str, json_output: bool):
    """View the deferred review queue."""
    engine = CheckpointEngine()
    items = engine.get_review_queue(phase)

    if severity:
        items = [i for i in items if i.severity == severity]

    if json_output:
        click.echo(json.dumps([i.to_dict() for i in items], indent=2))
        return

    if not items:
        click.echo("\n[OK] No items in review queue")
        return

    click.echo(f"\n{'='*60}")
    click.echo(f"Deferred Review Queue: {len(items)} items")
    click.echo(f"{'='*60}")

    for item in items:
        icon = {"CRITICAL": "[!!!]", "WARNING": "[!]", "INFO": "[i]"}.get(item.severity, "[?]")
        click.echo(f"\n{icon} {item.bank_name} ({item.bank_id})")
        click.echo(f"   Phase: {item.phase} | Stage: {item.stage}")
        click.echo(f"   Checkpoint: {item.checkpoint_name}")
        click.echo(f"   Reason: {item.review_reason}")
        click.echo(f"   P(A): {item.current_probability:.1%}")
        if item.current_classification:
            click.echo(f"   Classification: {item.current_classification} @ {item.current_confidence:.0f}%")
        click.echo(f"   Auto-resolution: {item.auto_resolution}")
        click.echo(f"   Options: {', '.join(item.options)}")
        click.echo(f"   Timestamp: {item.timestamp}")

    click.echo(f"\n{'='*60}\n")


@cli.command()
@click.option('--bank', required=True, help='Bank ID')
@click.option('--phase', type=int, default=1, help='Phase number')
@click.option('--prior', type=float, default=0.30, help='Prior P(Architect) (default: 0.30)')
def init(bank: str, phase: int, prior: float):
    """Initialize a bank for research."""
    orch = WorkflowOrchestrator()

    # Check if already exists
    existing = orch.get_status(bank, phase)
    if existing:
        click.echo(f"Bank {bank} already initialized. Current stage: {existing.current_stage}")
        if not click.confirm("Reinitialize?"):
            return

    try:
        state = orch.initialize_bank(bank, phase, prior)
        click.echo(f"\n[OK] Initialized {state.bank_name}")
        click.echo(f"  Phase: {phase}")
        click.echo(f"  Execution Tier: {state.execution_tier}")
        click.echo(f"  Prior P(Architect): {prior:.0%}")
        click.echo(f"\nNext: Run 'run_research.py prompt --bank {bank} --phase {phase}' to get the research prompt")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--bank', required=True, help='Bank ID')
@click.option('--phase', type=int, default=1, help='Phase number')
@click.option('--stage', help='Validate specific stage (default: all completed)')
def validate(bank: str, phase: int, stage: str):
    """Validate outputs for a bank."""
    orch = WorkflowOrchestrator()
    validator = OutputValidator()

    state = orch.get_status(bank, phase)
    if state is None:
        click.echo(f"No state found for {bank}. Initialize first.")
        sys.exit(1)

    bank_dir = orch._get_bank_dir(bank, phase)

    if stage:
        # Validate single stage
        result = validator.validate(bank, phase, stage, bank_dir)
        _print_validation_result(result)
    else:
        # Validate all stages
        results = validator.validate_all_stages(bank, phase, bank_dir)
        total_errors = 0
        total_warnings = 0

        click.echo(f"\n{'='*60}")
        click.echo(f"Validation Results: {state.bank_name}")
        click.echo(f"{'='*60}")

        for stage_name, result in results.items():
            if result.files_found or result.files_missing or result.errors:
                icon = "[OK]" if result.valid else "[ERR]"
                click.echo(f"\n{icon} {stage_name}")

                if result.files_found:
                    click.echo(f"   Files: {', '.join(result.files_found)}")

                if result.errors:
                    total_errors += len(result.errors)
                    for err in result.errors:
                        click.echo(f"   [ERR] {err}")

                if result.warnings:
                    total_warnings += len(result.warnings)
                    for warn in result.warnings:
                        click.echo(f"   [WARN] {warn}")

        click.echo(f"\n{'='*60}")
        click.echo(f"Total Errors: {total_errors}")
        click.echo(f"Total Warnings: {total_warnings}")
        click.echo(f"{'='*60}\n")


def _print_validation_result(result):
    """Print a single validation result."""
    icon = "[OK]" if result.valid else "[ERR]"
    click.echo(f"\n{icon} Stage: {result.stage}")

    if result.files_found:
        click.echo(f"Files found: {', '.join(result.files_found)}")

    if result.files_missing:
        click.echo(f"Files missing: {', '.join(result.files_missing)}")

    for err in result.errors:
        click.echo(f"[ERR] {err}")

    for warn in result.warnings:
        click.echo(f"[WARN] {warn}")


@cli.command()
@click.option('--bank', required=True, help='Bank ID')
@click.option('--phase', type=int, default=1, help='Phase number')
@click.option('--force', is_flag=True, help='Skip confirmation')
def clear(bank: str, phase: int, force: bool):
    """Clear state for a bank (for re-running research)."""
    orch = WorkflowOrchestrator()

    state = orch.get_status(bank, phase)
    if state is None:
        click.echo(f"No state found for {bank}")
        return

    if not force:
        click.echo(f"\nThis will clear state for {state.bank_name} (Phase {phase})")
        click.echo(f"Current stage: {state.current_stage}")
        click.echo(f"Stages completed: {len(state.stages_completed)}")
        if not click.confirm("Continue?"):
            return

    orch.clear_bank_state(bank, phase)
    click.echo(f"[OK] Cleared state for {bank}")


@cli.command('list-banks')
@click.option('--phase', type=int, help='Filter by phase')
def list_banks(phase: int):
    """List all banks in the manifest."""
    orch = WorkflowOrchestrator()

    if phase:
        banks = orch.get_banks_for_phase(phase)
        click.echo(f"\nBanks in Phase {phase}:")
    else:
        banks = orch.bank_manifest.get("banks", [])
        click.echo(f"\nAll Banks ({len(banks)} total):")

    for bank in banks:
        click.echo(f"  {bank['bank_id']}: {bank['bank_name']} (Phase {bank['phase']})")


@cli.command('finalize')
@click.option('--bank', required=True, help='Bank ID')
@click.option('--phase', type=int, default=1, help='Phase number')
def finalize(bank: str, phase: int):
    """Finalize research for a bank and generate result."""
    orch = WorkflowOrchestrator()

    state = orch.get_status(bank, phase)
    if state is None:
        click.echo(f"No state found for {bank}")
        sys.exit(1)

    # Validate first
    validator = OutputValidator()
    bank_dir = orch._get_bank_dir(bank, phase)
    results = validator.validate_all_stages(bank, phase, bank_dir)

    errors = sum(len(r.errors) for r in results.values())
    if errors > 0:
        click.echo(f"[WARN] {errors} validation errors found. Run 'validate' command for details.")
        if not click.confirm("Finalize anyway?"):
            return

    result = orch.finalize_bank(state)

    click.echo(f"\n{'='*60}")
    click.echo(f"Research Finalized: {result.bank_name}")
    click.echo(f"{'='*60}")
    click.echo(f"Classification: {result.classification or 'UNKNOWN'}")
    if result.classification_variant:
        click.echo(f"Variant: {result.classification_variant}")
    click.echo(f"Confidence: {result.confidence:.0f}%" if result.confidence else "Confidence: N/A")
    click.echo(f"P(Architect): {result.final_probability:.1%}")
    click.echo(f"Stages Completed: {len(result.stages_completed)}")
    click.echo(f"Stages Skipped: {len(result.stages_skipped)}")

    if result.review_items:
        click.echo(f"\n[WARN] {len(result.review_items)} items flagged for review")

    if result.errors:
        click.echo(f"\n[ERR] {len(result.errors)} errors during research")

    click.echo(f"\nCompleted: {result.completed_at}")
    click.echo(f"{'='*60}\n")


if __name__ == '__main__':
    cli()
