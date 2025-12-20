#!/usr/bin/env python3
"""
CDM Research Protocol - Unified CLI v1.0

Single entry point for all CDM research protocol tools.
Replaces 19 separate tools with one unified interface.

Usage:
    python tools/cdm.py research --bank deutsche-bank --phase 1
    python tools/cdm.py validate --bank deutsche-bank
    python tools/cdm.py checkpoint approve final_classification
    python tools/cdm.py status --phase 1
    python tools/cdm.py pipeline --batch outputs/phase-1-european-tier1/
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))


def cmd_research(args):
    """Run automated research on banks."""
    from auto_orchestrate import run_bank_auto, run_phase_auto

    if args.bank and args.phase:
        result = run_bank_auto(args.bank, args.phase, resume=not args.fresh)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2), encoding='utf-8')
        return 0 if result['status'] == 'complete' else 1

    elif args.phase and args.all:
        results = run_phase_auto(args.phase, args.parallel)
        if args.output:
            Path(args.output).write_text(json.dumps(results, indent=2), encoding='utf-8')
        failed = sum(1 for r in results if r['status'] not in ['complete'])
        return 1 if failed > 0 else 0

    else:
        print("Error: Specify --bank and --phase, or --phase and --all")
        return 1


def cmd_validate(args):
    """Run validation on bank outputs."""
    from research_runner import ResearchRunner

    runner = ResearchRunner()

    if args.bank:
        # Find bank directory
        outputs_dir = PROJECT_ROOT / "outputs"
        bank_dir = None
        for phase_dir in outputs_dir.iterdir():
            if phase_dir.is_dir():
                candidate = phase_dir / args.bank
                if candidate.exists():
                    bank_dir = candidate
                    break

        if not bank_dir:
            print(f"Error: Bank directory not found: {args.bank}")
            return 1

        results = runner.run_validation_pipeline(bank_dir)

        print(f"\n{'='*60}")
        print(f"VALIDATION: {args.bank}")
        print(f"{'='*60}")
        print(f"Valid: {results['valid']}")
        print(f"Classification: {results.get('classification')}")
        print(f"Confidence: {results.get('confidence')}%")

        for stage, data in results.get('stages', {}).items():
            if isinstance(data, dict):
                if 'error' in data:
                    print(f"  [{stage}] ERROR: {data['error']}")
                elif 'skipped' in data:
                    print(f"  [{stage}] SKIPPED")
                else:
                    print(f"  [{stage}] OK")

        return 0 if results['valid'] else 1

    elif args.phase:
        results = runner.run_phase(args.phase)
        passed = sum(1 for r in results if r.success)
        print(f"\nPhase {args.phase}: {passed}/{len(results)} passed")
        return 0 if passed == len(results) else 1

    elif args.cross_bank:
        from cross_bank_validator import run_checks
        results = run_checks(args.cross_bank)

        if results['passed']:
            print("Cross-bank validation: PASSED")
            return 0
        else:
            print("Cross-bank validation: FAILED")
            for issue in results.get('critical', []):
                print(f"  CRITICAL: {issue.get('issue', 'Unknown')}")
            return 1

    else:
        print("Error: Specify --bank, --phase, or --cross-bank")
        return 1


def cmd_checkpoint(args):
    """Manage workflow checkpoints."""
    from orchestrate import Orchestrator

    if args.action == 'list':
        # List all pending checkpoints
        outputs_dir = PROJECT_ROOT / "outputs"
        pending = []

        for phase_dir in outputs_dir.iterdir():
            if phase_dir.is_dir() and 'phase-' in phase_dir.name:
                for bank_dir in phase_dir.iterdir():
                    if bank_dir.is_dir():
                        status_file = bank_dir / "status.json"
                        if status_file.exists():
                            try:
                                status = json.loads(status_file.read_text(encoding='utf-8'))
                                if status.get('checkpoints_pending'):
                                    pending.append({
                                        'bank': bank_dir.name,
                                        'checkpoints': status['checkpoints_pending'],
                                        'stage': status.get('current_stage')
                                    })
                            except Exception:
                                pass

        if not pending:
            print("No pending checkpoints.")
        else:
            print(f"\n{'='*60}")
            print("PENDING CHECKPOINTS")
            print(f"{'='*60}")
            for p in pending:
                print(f"\n{p['bank']} (stage: {p['stage']})")
                for cp in p['checkpoints']:
                    print(f"  - {cp}")
            print(f"\nTotal: {sum(len(p['checkpoints']) for p in pending)} checkpoints")

        return 0

    elif args.action == 'approve':
        if not args.bank:
            print("Error: --bank required for approve action")
            return 1

        # Find bank directory
        outputs_dir = PROJECT_ROOT / "outputs"
        bank_dir = None
        for phase_dir in outputs_dir.iterdir():
            if phase_dir.is_dir():
                candidate = phase_dir / args.bank
                if candidate.exists():
                    bank_dir = candidate
                    break

        if not bank_dir:
            print(f"Error: Bank directory not found: {args.bank}")
            return 1

        orchestrator = Orchestrator(bank_dir)

        if args.checkpoint_id:
            success = orchestrator.approve_checkpoint(args.checkpoint_id, approver="cdm-cli")
            if success:
                print(f"Approved: {args.checkpoint_id}")

                # Try to advance
                if orchestrator.advance():
                    print(f"Advanced to: {orchestrator.get_current_stage().value}")
            else:
                print(f"Failed to approve: {args.checkpoint_id}")
            return 0 if success else 1
        else:
            print("Error: checkpoint_id required")
            return 1

    elif args.action == 'approve-all-clear':
        # Auto-approve all checkpoints that meet criteria
        from auto_orchestrate import check_auto_approval, log_auto_approval

        outputs_dir = PROJECT_ROOT / "outputs"
        approved_count = 0

        for phase_dir in outputs_dir.iterdir():
            if phase_dir.is_dir() and 'phase-' in phase_dir.name:
                for bank_dir in phase_dir.iterdir():
                    if bank_dir.is_dir():
                        try:
                            orchestrator = Orchestrator(bank_dir)
                            for cp in list(orchestrator.state.checkpoints_pending):
                                auto_result = check_auto_approval(orchestrator, cp)
                                if auto_result.approved:
                                    orchestrator.approve_checkpoint(cp, approver="cdm-cli-auto")
                                    log_auto_approval(bank_dir, cp, auto_result)
                                    approved_count += 1
                                    print(f"Auto-approved: {bank_dir.name}/{cp}")
                        except Exception as e:
                            print(f"Error processing {bank_dir.name}: {e}")

        print(f"\nTotal auto-approved: {approved_count}")
        return 0

    else:
        print(f"Unknown action: {args.action}")
        return 1


def cmd_status(args):
    """Show status of banks/phases."""
    outputs_dir = PROJECT_ROOT / "outputs"

    if args.bank:
        # Find and show single bank status
        bank_dir = None
        for phase_dir in outputs_dir.iterdir():
            if phase_dir.is_dir():
                candidate = phase_dir / args.bank
                if candidate.exists():
                    bank_dir = candidate
                    break

        if not bank_dir:
            print(f"Bank not found: {args.bank}")
            return 1

        from orchestrate import Orchestrator
        orchestrator = Orchestrator(bank_dir)
        status = orchestrator.get_status()

        print(f"\n{'='*60}")
        print(f"BANK STATUS: {args.bank}")
        print(f"{'='*60}")
        print(f"Stage: {status['current_stage']}")
        print(f"P(Architect): {status['probability_architect']}%")
        print(f"Classification: {status['classification'] or 'Not set'}")
        print(f"Confidence: {status['confidence']}%")
        print(f"Blocked: {status['is_blocked']}")
        if status['block_reason']:
            print(f"Reason: {status['block_reason']}")
        print(f"Stages completed: {len(status['stages_completed'])}")
        return 0

    elif args.phase:
        # Show phase summary
        phase_dir = None
        for d in outputs_dir.iterdir():
            if d.is_dir() and f"phase-{args.phase}" in d.name:
                phase_dir = d
                break

        if not phase_dir:
            print(f"Phase {args.phase} not found")
            return 1

        print(f"\n{'='*60}")
        print(f"PHASE {args.phase} STATUS")
        print(f"{'='*60}")

        banks = []
        for bank_dir in sorted(phase_dir.iterdir()):
            if bank_dir.is_dir() and not bank_dir.name.startswith('.'):
                status_file = bank_dir / "status.json"
                if status_file.exists():
                    try:
                        status = json.loads(status_file.read_text(encoding='utf-8'))
                        banks.append({
                            'name': bank_dir.name,
                            'stage': status.get('current_stage', 'init'),
                            'classification': status.get('classification'),
                            'confidence': status.get('confidence', 0),
                            'pending': len(status.get('checkpoints_pending', []))
                        })
                    except Exception:
                        banks.append({'name': bank_dir.name, 'stage': 'error'})
                else:
                    banks.append({'name': bank_dir.name, 'stage': 'not started'})

        print(f"{'Bank':<25} {'Stage':<15} {'Class':<12} {'Conf':>5} {'Pending':>7}")
        print("-" * 70)
        for b in banks:
            cls = b.get('classification', '-') or '-'
            conf = f"{b.get('confidence', 0):.0f}%" if b.get('confidence') else '-'
            pend = b.get('pending', 0)
            print(f"{b['name']:<25} {b['stage']:<15} {cls:<12} {conf:>5} {pend:>7}")

        return 0

    elif args.all:
        # Show all phases
        phases = {}
        for d in outputs_dir.iterdir():
            if d.is_dir() and 'phase-' in d.name:
                banks = list(d.iterdir())
                bank_count = len([b for b in banks if b.is_dir() and not b.name.startswith('.')])
                phases[d.name] = bank_count

        print(f"\n{'='*60}")
        print("ALL PHASES STATUS")
        print(f"{'='*60}")
        for phase_name, count in sorted(phases.items()):
            print(f"{phase_name}: {count} banks")

        return 0

    else:
        print("Error: Specify --bank, --phase, or --all")
        return 1


def cmd_pipeline(args):
    """Run verification pipeline."""
    from run_pipeline import run_pipeline, run_batch

    if args.batch:
        results = run_batch(args.batch, args.skip_verification)
        failed = sum(1 for r in results if r['status'] == 'failed')
        return 1 if failed > 0 else 0

    elif args.bank:
        # Find bank directory
        outputs_dir = PROJECT_ROOT / "outputs"
        bank_dir = None
        for phase_dir in outputs_dir.iterdir():
            if phase_dir.is_dir():
                candidate = phase_dir / args.bank
                if candidate.exists():
                    bank_dir = candidate
                    break

        if not bank_dir:
            print(f"Bank not found: {args.bank}")
            return 1

        result = run_pipeline(str(bank_dir), args.skip_verification)
        return 0 if result['status'] == 'complete' else 1

    else:
        print("Error: Specify --bank or --batch")
        return 1


def cmd_watch(args):
    """Watch for changes and auto-process."""
    from run_pipeline import watch_directory

    watch_directory(args.path, args.interval)
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="CDM Research Protocol - Unified CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  research    Run automated research on banks
  validate    Run validation on bank outputs
  checkpoint  Manage workflow checkpoints
  status      Show status of banks/phases
  pipeline    Run verification pipeline
  watch       Watch for changes and auto-process

Examples:
  cdm research --bank deutsche-bank --phase 1
  cdm validate --bank deutsche-bank
  cdm checkpoint list
  cdm checkpoint approve --bank deutsche-bank final_classification
  cdm status --phase 1
  cdm pipeline --batch outputs/phase-1-european-tier1/
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Research command
    p_research = subparsers.add_parser('research', help='Run automated research')
    p_research.add_argument('--bank', help='Bank ID')
    p_research.add_argument('--phase', type=int, help='Phase number')
    p_research.add_argument('--all', action='store_true', help='Process all banks in phase')
    p_research.add_argument('--parallel', type=int, default=1, help='Parallel workers')
    p_research.add_argument('--fresh', action='store_true', help='Start fresh')
    p_research.add_argument('--output', help='Output JSON file')

    # Validate command
    p_validate = subparsers.add_parser('validate', help='Run validation')
    p_validate.add_argument('--bank', help='Bank ID')
    p_validate.add_argument('--phase', type=int, help='Phase number')
    p_validate.add_argument('--cross-bank', help='Directory for cross-bank validation')

    # Checkpoint command
    p_checkpoint = subparsers.add_parser('checkpoint', help='Manage checkpoints')
    p_checkpoint.add_argument('action', choices=['list', 'approve', 'approve-all-clear'],
                               help='Action to perform')
    p_checkpoint.add_argument('checkpoint_id', nargs='?', help='Checkpoint ID to approve')
    p_checkpoint.add_argument('--bank', help='Bank ID')

    # Status command
    p_status = subparsers.add_parser('status', help='Show status')
    p_status.add_argument('--bank', help='Bank ID')
    p_status.add_argument('--phase', type=int, help='Phase number')
    p_status.add_argument('--all', action='store_true', help='Show all phases')

    # Pipeline command
    p_pipeline = subparsers.add_parser('pipeline', help='Run verification pipeline')
    p_pipeline.add_argument('--bank', help='Bank ID')
    p_pipeline.add_argument('--batch', help='Directory for batch processing')
    p_pipeline.add_argument('--skip-verification', action='store_true', help='Skip URL verification')

    # Watch command
    p_watch = subparsers.add_parser('watch', help='Watch for changes')
    p_watch.add_argument('path', help='Directory to watch')
    p_watch.add_argument('--interval', type=int, default=30, help='Check interval (seconds)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Dispatch to command handler
    handlers = {
        'research': cmd_research,
        'validate': cmd_validate,
        'checkpoint': cmd_checkpoint,
        'status': cmd_status,
        'pipeline': cmd_pipeline,
        'watch': cmd_watch,
    }

    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
