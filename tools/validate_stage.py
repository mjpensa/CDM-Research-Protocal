"""
CDM Research Protocol - Stage Validation CLI v1.0

Command-line tool for validating stage outputs.
Called by Claude Code after completing each stage.

Usage:
    python tools/validate_stage.py --bank deutsche-bank --phase 1 --stage tier1_evidence
    python tools/validate_stage.py --bank deutsche-bank --phase 1 --auto
    python tools/validate_stage.py --bank deutsche-bank --phase 1 --advance

The --auto flag validates the current stage from state.
The --advance flag advances to the next stage after successful validation.
"""

import argparse
import sys
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from claude_code_bridge import ClaudeCodeBridge, StageResult


def main():
    parser = argparse.ArgumentParser(
        description="Validate stage outputs for CDM Research Protocol",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Validate specific stage
    python tools/validate_stage.py --bank deutsche-bank --phase 1 --stage tier1_evidence

    # Auto-detect and validate current stage
    python tools/validate_stage.py --bank deutsche-bank --phase 1 --auto

    # Validate and advance to next stage
    python tools/validate_stage.py --bank deutsche-bank --phase 1 --auto --advance

    # Get JSON output for parsing
    python tools/validate_stage.py --bank deutsche-bank --phase 1 --auto --json
        """
    )

    parser.add_argument("--bank", required=True, help="Bank ID (e.g., deutsche-bank)")
    parser.add_argument("--phase", type=int, default=1, help="Phase number (default: 1)")
    parser.add_argument("--stage", help="Stage to validate (e.g., tier1_evidence)")
    parser.add_argument("--auto", action="store_true",
                        help="Auto-detect current stage from state")
    parser.add_argument("--advance", action="store_true",
                        help="Advance to next stage after successful validation")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")
    parser.add_argument("--quiet", action="store_true",
                        help="Minimal output (exit code only)")

    args = parser.parse_args()

    # Validate arguments
    if not args.stage and not args.auto:
        parser.error("Either --stage or --auto must be specified")

    try:
        # Initialize bridge
        bridge = ClaudeCodeBridge(args.bank, args.phase)

        # Determine stage to validate
        if args.auto:
            stage = bridge.get_current_stage()
        else:
            stage = args.stage

        # Validate
        result: StageResult = bridge.validate_stage_output(stage)

        # Advance if requested and successful
        if args.advance and result.success:
            next_stage, _ = bridge.advance_to_next_stage()
            if next_stage:
                result = StageResult(
                    success=True,
                    stage=stage,
                    errors=result.errors,
                    warnings=result.warnings,
                    next_stage=next_stage,
                    recommendation=result.recommendation,
                    details={**(result.details or {}), "advanced": True}
                )

        # Output
        if args.json:
            output = result.to_dict()
            output['bank_id'] = args.bank
            output['phase'] = args.phase
            print(json.dumps(output, indent=2))

        elif not args.quiet:
            print(f"\n{'='*60}")
            print(f"VALIDATION: {args.bank} (Phase {args.phase})")
            print(f"{'='*60}")
            print(f"Stage: {result.stage}")
            print(f"Status: {'PASS' if result.success else 'FAIL'}")

            if result.errors:
                print(f"\nErrors ({len(result.errors)}):")
                for err in result.errors:
                    print(f"  - {err}")

            if result.warnings:
                print(f"\nWarnings ({len(result.warnings)}):")
                for warn in result.warnings:
                    print(f"  - {warn}")

            print(f"\nNext Stage: {result.next_stage or 'N/A'}")
            print(f"Recommendation: {result.recommendation}")

            if result.details:
                print(f"\nDetails:")
                for key, value in result.details.items():
                    if key not in ['errors', 'warnings']:
                        print(f"  {key}: {value}")

            print(f"{'='*60}\n")

        # Exit code
        return 0 if result.success else 1

    except Exception as e:
        if args.json:
            print(json.dumps({
                "success": False,
                "error": str(e),
                "bank_id": args.bank,
                "phase": args.phase
            }, indent=2))
        elif not args.quiet:
            print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
