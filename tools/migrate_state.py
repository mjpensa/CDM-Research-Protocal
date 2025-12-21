"""
CDM Research Protocol - State Migration Script v1.0

Migrates existing state files to unified schema format.

Features:
- Applies stage name normalization (bayesian_t1 -> bayesian_1)
- Adds missing required fields (execution_tier, prior_probability)
- Validates migrated files with BankState.from_dict()
- Supports --dry-run and --execute modes

Usage:
    # Preview changes (no modifications)
    python tools/migrate_state.py --dry-run

    # Apply migration
    python tools/migrate_state.py --execute

    # Migrate specific phase
    python tools/migrate_state.py --execute --phase 1
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple, Optional

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from state_schema import (
    BankState, normalize_stage, STAGE_ALIASES, STAGE_SEQUENCE
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def find_status_files(outputs_dir: Path, phase: Optional[int] = None) -> List[Path]:
    """
    Find all status.json files in outputs directory.

    Args:
        outputs_dir: Path to outputs directory
        phase: Optional phase number to filter

    Returns:
        List of status.json file paths
    """
    if phase:
        pattern = f"phase-{phase}-*/*/status.json"
    else:
        pattern = "phase-*/*/status.json"

    return sorted(outputs_dir.glob(pattern))


def analyze_status_file(file_path: Path) -> Dict[str, Any]:
    """
    Analyze a status.json file for migration needs.

    Args:
        file_path: Path to status.json

    Returns:
        Analysis result with issues found
    """
    result = {
        "path": str(file_path),
        "bank_id": file_path.parent.name,
        "issues": [],
        "changes": [],
        "valid": True,
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        result["valid"] = False
        result["issues"].append(f"Failed to read: {e}")
        return result

    # Check for legacy stage names
    current_stage = data.get("current_stage", "")
    if current_stage in STAGE_ALIASES:
        result["issues"].append(f"Legacy current_stage: {current_stage}")
        result["changes"].append(f"current_stage: {current_stage} -> {STAGE_ALIASES[current_stage]}")

    # Check stages_completed for legacy names
    stages_completed = data.get("stages_completed", [])
    for stage in stages_completed:
        if stage in STAGE_ALIASES:
            result["issues"].append(f"Legacy stage in stages_completed: {stage}")
            result["changes"].append(f"stages_completed: {stage} -> {STAGE_ALIASES[stage]}")

    # Check for missing fields
    if "execution_tier" not in data:
        result["issues"].append("Missing execution_tier")
        result["changes"].append("Add execution_tier: 'B'")

    if "prior_probability" not in data:
        result["issues"].append("Missing prior_probability")
        result["changes"].append("Add prior_probability: 0.30")

    if "probability_history" not in data:
        result["issues"].append("Missing probability_history")
        result["changes"].append("Add probability_history: []")

    if "skipped_stages" not in data:
        result["issues"].append("Missing skipped_stages")
        result["changes"].append("Add skipped_stages: []")

    if "evidence_counts" not in data:
        result["issues"].append("Missing evidence_counts")
        result["changes"].append("Add evidence_counts: {tier1: 0, tier2: 0, tier3: 0, null: 0}")

    # Check for unknown fields
    try:
        # Try to load with BankState.from_dict to catch issues
        BankState.from_dict(data)
    except Exception as e:
        result["valid"] = False
        result["issues"].append(f"Schema validation error: {e}")

    return result


def migrate_status_file(file_path: Path, dry_run: bool = True) -> Tuple[bool, str]:
    """
    Migrate a status.json file to unified schema.

    Args:
        file_path: Path to status.json
        dry_run: If True, only report changes without modifying

    Returns:
        Tuple of (success, message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return False, f"Failed to read: {e}"

    original_data = json.dumps(data, sort_keys=True)
    changes_made = []

    # Normalize current_stage
    current_stage = data.get("current_stage", "")
    if current_stage in STAGE_ALIASES:
        data["current_stage"] = normalize_stage(current_stage)
        changes_made.append(f"current_stage: {current_stage} -> {data['current_stage']}")

    # Normalize stages_completed
    stages_completed = data.get("stages_completed", [])
    normalized_stages = [normalize_stage(s) for s in stages_completed]
    if normalized_stages != stages_completed:
        data["stages_completed"] = normalized_stages
        changes_made.append("Normalized stages_completed")

    # Normalize skipped_stages
    skipped_stages = data.get("skipped_stages", [])
    normalized_skipped = [normalize_stage(s) for s in skipped_stages]
    if normalized_skipped != skipped_stages:
        data["skipped_stages"] = normalized_skipped
        changes_made.append("Normalized skipped_stages")

    # Add missing fields with defaults
    if "execution_tier" not in data:
        data["execution_tier"] = "B"
        changes_made.append("Added execution_tier: B")

    if "prior_probability" not in data:
        data["prior_probability"] = 0.30
        changes_made.append("Added prior_probability: 0.30")

    if "probability_history" not in data:
        data["probability_history"] = []
        changes_made.append("Added probability_history: []")

    if "skipped_stages" not in data:
        data["skipped_stages"] = []
        changes_made.append("Added skipped_stages: []")

    if "evidence_counts" not in data:
        data["evidence_counts"] = {"tier1": 0, "tier2": 0, "tier3": 0, "null": 0}
        changes_made.append("Added evidence_counts")

    if "trust_flags" not in data:
        data["trust_flags"] = []
        changes_made.append("Added trust_flags: []")

    if "errors" not in data:
        data["errors"] = []
        changes_made.append("Added errors: []")

    # Convert probability scales if needed (0-100 to 0-1)
    prob = data.get("current_probability")
    if prob is not None and prob > 1.0:
        data["current_probability"] = prob / 100.0
        changes_made.append(f"Converted current_probability: {prob} -> {prob/100.0}")

    prior = data.get("prior_probability")
    if prior is not None and prior > 1.0:
        data["prior_probability"] = prior / 100.0
        changes_made.append(f"Converted prior_probability: {prior} -> {prior/100.0}")

    # Validate with BankState.from_dict
    try:
        bank_state = BankState.from_dict(data)
    except Exception as e:
        return False, f"Schema validation failed: {e}"

    # Check if changes were made
    new_data = json.dumps(data, sort_keys=True)
    if new_data == original_data:
        return True, "No changes needed"

    if not dry_run:
        # Create backup
        backup_path = file_path.with_suffix('.json.bak')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_data)

        # Write migrated file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)

        return True, f"Migrated ({len(changes_made)} changes): {', '.join(changes_made)}"
    else:
        return True, f"Would make {len(changes_made)} changes: {', '.join(changes_made)}"


def run_migration(outputs_dir: Path, phase: Optional[int] = None, dry_run: bool = True) -> Dict[str, Any]:
    """
    Run migration on all status files.

    Args:
        outputs_dir: Path to outputs directory
        phase: Optional phase to filter
        dry_run: If True, only preview changes

    Returns:
        Migration results summary
    """
    status_files = find_status_files(outputs_dir, phase)

    results = {
        "total": len(status_files),
        "success": 0,
        "skipped": 0,
        "failed": 0,
        "changes": 0,
        "files": [],
        "dry_run": dry_run,
    }

    logger.info(f"{'DRY RUN: ' if dry_run else ''}Found {len(status_files)} status files to process")

    for file_path in status_files:
        bank_id = file_path.parent.name
        success, message = migrate_status_file(file_path, dry_run=dry_run)

        file_result = {
            "bank_id": bank_id,
            "path": str(file_path),
            "success": success,
            "message": message,
        }
        results["files"].append(file_result)

        if not success:
            results["failed"] += 1
            logger.error(f"  FAILED: {bank_id}: {message}")
        elif "No changes needed" in message:
            results["skipped"] += 1
            logger.debug(f"  SKIP: {bank_id}: {message}")
        else:
            results["success"] += 1
            results["changes"] += 1
            logger.info(f"  {'WOULD CHANGE' if dry_run else 'CHANGED'}: {bank_id}: {message}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Migrate state files to unified schema format"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Preview changes without modifying files (default)"
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help="Apply migration changes"
    )
    parser.add_argument(
        '--phase',
        type=int,
        help="Migrate only specific phase"
    )
    parser.add_argument(
        '--outputs-dir',
        type=Path,
        default=PROJECT_ROOT / "outputs",
        help="Path to outputs directory"
    )
    parser.add_argument(
        '--analyze-only',
        action='store_true',
        help="Only analyze files, don't attempt migration"
    )

    args = parser.parse_args()

    # Default to dry-run if --execute not specified
    dry_run = not args.execute

    if dry_run:
        logger.info("=" * 60)
        logger.info("DRY RUN MODE - No files will be modified")
        logger.info("Use --execute to apply changes")
        logger.info("=" * 60)

    outputs_dir = args.outputs_dir

    if not outputs_dir.exists():
        logger.error(f"Outputs directory not found: {outputs_dir}")
        sys.exit(1)

    if args.analyze_only:
        # Just analyze and report
        status_files = find_status_files(outputs_dir, args.phase)
        logger.info(f"Analyzing {len(status_files)} status files...")

        total_issues = 0
        for file_path in status_files:
            analysis = analyze_status_file(file_path)
            if analysis["issues"]:
                total_issues += len(analysis["issues"])
                logger.info(f"\n{analysis['bank_id']}:")
                for issue in analysis["issues"]:
                    logger.info(f"  - {issue}")

        logger.info(f"\nTotal issues found: {total_issues}")
        return

    # Run migration
    results = run_migration(outputs_dir, args.phase, dry_run=dry_run)

    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("MIGRATION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total files:    {results['total']}")
    logger.info(f"{'Would change' if dry_run else 'Changed'}:   {results['changes']}")
    logger.info(f"Skipped:        {results['skipped']}")
    logger.info(f"Failed:         {results['failed']}")

    if dry_run and results['changes'] > 0:
        logger.info("\nTo apply these changes, run with --execute")

    if results['failed'] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
