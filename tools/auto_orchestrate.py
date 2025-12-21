"""
CDM Research Protocol - Auto Orchestrator v1.0

Fully automated bank research pipeline with smart checkpoints.
Runs complete bank research end-to-end with minimal human intervention.

Usage:
    python tools/auto_orchestrate.py --bank deutsche-bank --phase 1
    python tools/auto_orchestrate.py --phase 1 --all
    python tools/auto_orchestrate.py --bank deutsche-bank --resume
    python tools/auto_orchestrate.py --phase 1 --parallel 3

Features:
    - Auto-generates prompts from templates and bank config
    - Runs validation between stages
    - Auto-approves checkpoints that meet criteria
    - Generates decision reports for blocked checkpoints
    - Supports parallel processing of multiple banks
    - Auto-resumes from last completed stage
"""

import sys
import json
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import load_bank_manifest, get_bank_config, get_confidence_caps
from orchestrate import Orchestrator, Stage, WorkflowState
from run_pipeline import run_pipeline
from markdown_parser import validate_bank_outputs

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AutoApprovalResult:
    """Result of auto-approval check."""
    approved: bool
    reason: str
    checkpoint_id: str
    conditions_met: Dict[str, bool] = field(default_factory=dict)


def load_auto_approval_rules() -> dict:
    """Load auto-approval rules from config."""
    rules_path = PROJECT_ROOT / "config" / "auto-approval-rules.json"
    if rules_path.exists():
        return json.loads(rules_path.read_text(encoding='utf-8'))
    return {"auto_approve_conditions": {}, "force_block_checkpoints": []}


def check_auto_approval(orchestrator: Orchestrator, checkpoint_id: str) -> AutoApprovalResult:
    """
    Check if a checkpoint can be auto-approved based on rules.

    Args:
        orchestrator: Current orchestrator instance
        checkpoint_id: ID of checkpoint to check

    Returns:
        AutoApprovalResult with approval decision and reasoning
    """
    rules = load_auto_approval_rules()
    state = orchestrator.state

    # Check force-block list
    if checkpoint_id in rules.get('force_block_checkpoints', []):
        return AutoApprovalResult(
            approved=False,
            reason=f"Checkpoint '{checkpoint_id}' is in force-block list",
            checkpoint_id=checkpoint_id
        )

    conditions = rules.get('auto_approve_conditions', {}).get(checkpoint_id, {})
    if not conditions:
        # No rules defined - default to manual
        return AutoApprovalResult(
            approved=False,
            reason="No auto-approval rules defined for this checkpoint",
            checkpoint_id=checkpoint_id
        )

    # Check explicit auto_approve: false
    if conditions.get('auto_approve') is False:
        return AutoApprovalResult(
            approved=False,
            reason=conditions.get('reason', 'Auto-approval disabled'),
            checkpoint_id=checkpoint_id
        )

    # Check conditions for final_classification
    if checkpoint_id == 'final_classification':
        conds = conditions.get('conditions', {})
        met = {}

        # Min confidence
        if 'min_confidence' in conds:
            met['min_confidence'] = state.confidence >= conds['min_confidence']

        # Probability-classification alignment
        if conds.get('probability_classification_aligned'):
            alignment = conditions.get('alignment_rules', {})
            p = state.probability_architect

            if state.classification == 'ARCHITECT':
                met['alignment'] = p >= alignment.get('architect_if_probability_above', 70)
            elif state.classification == 'PRAGMATIST':
                met['alignment'] = p <= alignment.get('pragmatist_if_probability_below', 30)
            else:
                met['alignment'] = True  # OBSERVER/UNKNOWN don't need alignment

        # No contradictions
        if conds.get('no_contradictions'):
            met['no_contradictions'] = 'contradiction' not in state.checkpoints_pending

        # No anchor violations
        if conds.get('no_anchor_violations'):
            violation, _ = orchestrator.check_anchor_violation()
            met['no_anchor_violations'] = not violation

        # All conditions met?
        all_met = all(met.values())

        return AutoApprovalResult(
            approved=all_met,
            reason="All auto-approval conditions met" if all_met else "Some conditions not met",
            checkpoint_id=checkpoint_id,
            conditions_met=met
        )

    # Check conditions for adversarial_verdict
    if checkpoint_id == 'adversarial_revised':
        # Never auto-approve revised verdicts
        return AutoApprovalResult(
            approved=False,
            reason="Revised adversarial verdicts require human review",
            checkpoint_id=checkpoint_id
        )

    # Default: gates auto-approve unless blocked
    if checkpoint_id.startswith('gate_'):
        return AutoApprovalResult(
            approved=True,
            reason="Gate checkpoints auto-proceed by default",
            checkpoint_id=checkpoint_id
        )

    return AutoApprovalResult(
        approved=False,
        reason="Unknown checkpoint type - defaulting to manual review",
        checkpoint_id=checkpoint_id
    )


def generate_decision_report(orchestrator: Orchestrator, bank_dir: Path) -> Path:
    """
    Generate a decision report for human review when blocked.

    Args:
        orchestrator: Current orchestrator instance
        bank_dir: Path to bank directory

    Returns:
        Path to generated decision report
    """
    state = orchestrator.state
    status = orchestrator.get_status()

    report_path = bank_dir / f"checkpoint-decision-{status['checkpoints_pending'][0] if status['checkpoints_pending'] else 'review'}.md"

    # Count evidence
    evidence_dir = bank_dir / "1-evidence"
    evidence_count = {1: 0, 2: 0, 3: 0}
    if evidence_dir.exists():
        for tier in [1, 2, 3]:
            tier_file = evidence_dir / f"tier{tier}-evidence.md"
            if tier_file.exists():
                content = tier_file.read_text(encoding='utf-8')
                # Count evidence blocks
                evidence_count[tier] = content.count('[BANK-')

    # Build report
    report = f"""# Checkpoint Decision Report

## Bank: {state.bank_id}
## Blocked At: {status['block_reason']}
## Generated: {datetime.utcnow().isoformat()}

---

## Current State

| Metric | Value |
|--------|-------|
| Classification | {state.classification or 'Not set'} |
| Sub-classification | {state.sub_classification or 'Not set'} |
| Confidence | {state.confidence}% |
| P(Architect) | {state.probability_architect}% |
| Current Stage | {state.current_stage} |

---

## Evidence Summary

| Tier | Evidence Items |
|------|----------------|
| Tier 1 | {evidence_count[1]} items |
| Tier 2 | {evidence_count[2]} items |
| Tier 3 | {evidence_count[3]} items |
| **Total** | **{sum(evidence_count.values())} items** |

---

## Pending Checkpoints

"""
    for cp in status['checkpoints_pending']:
        report += f"- [ ] {cp}\n"

    report += """
---

## Quick Actions

To approve and continue:
```bash
python tools/orchestrate.py {bank_dir} --approve {checkpoint_id}
python tools/orchestrate.py {bank_dir} --advance
```

To adjust classification:
```bash
python tools/orchestrate.py {bank_dir} --set-classification PRAGMATIST Vendor-Dependent 70
```

To re-run validation:
```bash
python tools/run_pipeline.py {bank_dir}
```

---

## Recommendation

""".format(
        bank_dir=bank_dir,
        checkpoint_id=status['checkpoints_pending'][0] if status['checkpoints_pending'] else 'final_classification'
    )

    # Add recommendation based on state
    if state.confidence >= 70 and not status['checkpoints_pending']:
        report += "**APPROVE** - High confidence classification with no pending issues.\n"
    elif state.confidence >= 50:
        report += "**REVIEW** - Moderate confidence. Review evidence chain before approving.\n"
    else:
        report += "**INVESTIGATE** - Low confidence. Consider gathering additional evidence.\n"

    report_path.write_text(report, encoding='utf-8')
    logger.info(f"Generated decision report: {report_path}")

    return report_path


def run_stage_validation(bank_dir: Path, stage: str) -> dict:
    """
    Run validation for a completed stage.

    Args:
        bank_dir: Path to bank directory
        stage: Stage that was just completed

    Returns:
        Validation results dict
    """
    results = {'valid': True, 'errors': [], 'warnings': []}

    try:
        md_results = validate_bank_outputs(str(bank_dir))

        for file_type, result in md_results.items():
            if isinstance(result, dict):
                results['errors'].extend(result.get('errors', []))
                results['warnings'].extend(result.get('warnings', []))

        results['valid'] = len(results['errors']) == 0

    except Exception as e:
        results['warnings'].append(f"Validation error: {e}")

    return results


def run_bank_auto(bank_id: str, phase: int, resume: bool = True) -> dict:
    """
    Run complete bank research pipeline automatically.

    Args:
        bank_id: Bank identifier
        phase: Phase number
        resume: Whether to resume from last stage

    Returns:
        Result dict with status and details
    """
    result = {
        'bank_id': bank_id,
        'phase': phase,
        'status': 'pending',
        'stages_completed': [],
        'blocked_at': None,
        'decision_report': None,
        'errors': []
    }

    # Find bank directory
    outputs_dir = PROJECT_ROOT / "outputs"
    bank_dir = None

    # Check directory exists before iterating (batch safety)
    if not outputs_dir.exists():
        outputs_dir.mkdir(parents=True, exist_ok=True)

    for phase_dir in outputs_dir.iterdir():
        if phase_dir.is_dir() and f"phase-{phase}" in phase_dir.name:
            candidate = phase_dir / bank_id
            if candidate.exists():
                bank_dir = candidate
                break

    if not bank_dir:
        # Create directory structure
        manifest = load_bank_manifest()
        phase_name = f"phase-{phase}"
        for p in manifest.get('phases', {}).values():
            if p.get('number') == phase:
                phase_name = f"phase-{phase}-{p.get('name', '').lower().replace(' ', '-')}"
                break

        bank_dir = outputs_dir / phase_name / bank_id
        bank_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        for subdir in ['1-evidence', '2-bayesian', '3-gates', '4-adversarial', '5-synthesis', 'snapshots']:
            (bank_dir / subdir).mkdir(exist_ok=True)

    logger.info(f"\n{'='*60}")
    logger.info(f"AUTO-ORCHESTRATE: {bank_id} (Phase {phase})")
    logger.info(f"{'='*60}")
    logger.info(f"Directory: {bank_dir}")

    # Initialize orchestrator
    orchestrator = Orchestrator(bank_dir)

    if resume:
        logger.info(f"Resuming from stage: {orchestrator.state.current_stage}")
        logger.info(f"Stages completed: {orchestrator.state.stages_completed}")

    # Main loop - advance through stages
    max_iterations = 20  # Safety limit
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        current_stage = orchestrator.get_current_stage()

        if current_stage == Stage.COMPLETE:
            result['status'] = 'complete'
            logger.info("Bank research COMPLETE")
            break

        logger.info(f"\n[Stage] {current_stage.value}")

        # Check if blocked
        should_block, reason, checkpoint_id = orchestrator.should_block()

        if should_block:
            # Try auto-approval
            auto_result = check_auto_approval(orchestrator, checkpoint_id)

            if auto_result.approved:
                logger.info(f"AUTO-APPROVED: {checkpoint_id} - {auto_result.reason}")
                orchestrator.approve_checkpoint(checkpoint_id, approver="auto_orchestrate")

                # Log auto-approval
                log_auto_approval(bank_dir, checkpoint_id, auto_result)

            else:
                # Generate decision report and block
                logger.warning(f"BLOCKED: {reason}")
                logger.warning(f"Auto-approval failed: {auto_result.reason}")

                decision_report = generate_decision_report(orchestrator, bank_dir)

                result['status'] = 'blocked'
                result['blocked_at'] = checkpoint_id
                result['decision_report'] = str(decision_report)
                result['stages_completed'] = orchestrator.state.stages_completed

                logger.info(f"Decision report: {decision_report}")
                logger.info("Run with --approve to continue after review")
                break

        # Try to advance
        success = orchestrator.advance()

        if success:
            # Run validation after stage
            new_stage = orchestrator.get_current_stage()
            validation = run_stage_validation(bank_dir, current_stage.value)

            if validation['errors']:
                logger.warning(f"Validation errors: {validation['errors'][:3]}")
            if validation['warnings']:
                logger.info(f"Validation warnings: {validation['warnings'][:3]}")

            result['stages_completed'] = orchestrator.state.stages_completed
        else:
            # Blocked - should have been caught above
            break

    # Run final pipeline if complete
    if result['status'] == 'complete':
        logger.info("\nRunning final verification pipeline...")
        try:
            pipeline_result = run_pipeline(str(bank_dir))
            result['pipeline'] = pipeline_result
            result['confidence'] = pipeline_result.get('confidence')
        except Exception as e:
            result['errors'].append(f"Pipeline error: {e}")

    return result


def log_auto_approval(bank_dir: Path, checkpoint_id: str, auto_result: AutoApprovalResult):
    """Log auto-approval decision."""
    log_path = PROJECT_ROOT / "outputs" / "state" / "auto-approval-log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    if log_path.exists():
        try:
            entries = json.loads(log_path.read_text(encoding='utf-8'))
        except Exception:
            entries = []

    entries.append({
        'timestamp': datetime.utcnow().isoformat(),
        'bank_id': bank_dir.name,
        'checkpoint_id': checkpoint_id,
        'approved': auto_result.approved,
        'reason': auto_result.reason,
        'conditions_met': auto_result.conditions_met
    })

    log_path.write_text(json.dumps(entries, indent=2), encoding='utf-8')


def run_phase_auto(phase: int, parallel: int = 1) -> List[dict]:
    """
    Run all banks in a phase, optionally in parallel.

    Args:
        phase: Phase number
        parallel: Number of parallel workers

    Returns:
        List of results for each bank
    """
    manifest = load_bank_manifest()
    banks = [b for b in manifest.get('banks', []) if b.get('phase') == phase]

    if not banks:
        logger.error(f"No banks found for phase {phase}")
        return []

    logger.info(f"Phase {phase}: {len(banks)} banks, {parallel} parallel workers")

    results = []

    if parallel == 1:
        # Sequential execution
        for bank in banks:
            result = run_bank_auto(bank['bank_id'], phase)
            results.append(result)
    else:
        # Parallel execution
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {
                executor.submit(run_bank_auto, bank['bank_id'], phase): bank
                for bank in banks
            }

            for future in as_completed(futures):
                bank = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error processing {bank['bank_id']}: {e}")
                    results.append({
                        'bank_id': bank['bank_id'],
                        'phase': phase,
                        'status': 'error',
                        'error': str(e)
                    })

    # Summary
    print(f"\n{'='*70}")
    print(f"PHASE {phase} SUMMARY")
    print(f"{'='*70}")

    complete = sum(1 for r in results if r['status'] == 'complete')
    blocked = sum(1 for r in results if r['status'] == 'blocked')
    errors = sum(1 for r in results if r['status'] == 'error')

    print(f"Complete: {complete} | Blocked: {blocked} | Errors: {errors}")
    print()

    for r in results:
        status_icon = {'complete': 'OK', 'blocked': 'BLOCK', 'error': 'ERR'}.get(r['status'], '?')
        conf = f"{r.get('confidence', 0):.0f}%" if r.get('confidence') else 'N/A'
        print(f"[{status_icon:5}] {r['bank_id']:25} {conf:>6}")

        if r.get('decision_report'):
            print(f"        └─ Decision report: {Path(r['decision_report']).name}")

    print(f"{'='*70}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="CDM Research Protocol - Auto Orchestrator"
    )
    parser.add_argument('--bank', help="Bank ID to process")
    parser.add_argument('--phase', type=int, help="Phase number")
    parser.add_argument('--all', action='store_true', help="Process all banks in phase")
    parser.add_argument('--parallel', type=int, default=1, help="Parallel workers (default: 1)")
    parser.add_argument('--resume', action='store_true', default=True, help="Resume from last stage (default)")
    parser.add_argument('--fresh', action='store_true', help="Start fresh, ignore previous state")
    parser.add_argument('--approve-all', action='store_true', help="Auto-approve all pending checkpoints")
    parser.add_argument('--output', help="Output results to JSON file")

    args = parser.parse_args()

    if args.bank and args.phase:
        # Single bank
        result = run_bank_auto(args.bank, args.phase, resume=not args.fresh)

        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2), encoding='utf-8')

        sys.exit(0 if result['status'] == 'complete' else 1)

    elif args.phase and args.all:
        # All banks in phase
        results = run_phase_auto(args.phase, args.parallel)

        if args.output:
            Path(args.output).write_text(json.dumps(results, indent=2), encoding='utf-8')

        failed = sum(1 for r in results if r['status'] not in ['complete'])
        sys.exit(1 if failed > 0 else 0)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
