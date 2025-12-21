#!/usr/bin/env python3
"""
CDM Research Protocol - State Migration Script v2.0

Migrates state files from pre-Gap-fix format to v2.0 format with:
- Schema version tracking
- Idempotency keys for probability_history entries
- Version metadata for state files
- Rotation metadata for log files

Usage:
    # Dry run - show what would change
    python tools/migrate_state_v2.py --dry-run outputs/

    # Execute migration with backup
    python tools/migrate_state_v2.py outputs/ --backup-dir migrations/backup/

    # Migrate specific bank
    python tools/migrate_state_v2.py outputs/phase-1-european-tier-1/deutsche-bank/

    # Show migration summary
    python tools/migrate_state_v2.py outputs/ --summary-only
"""

import argparse
import gzip
import hashlib
import json
import logging
import shutil
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Add tools directory to path for imports
TOOLS_DIR = Path(__file__).parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Migration constants
TARGET_SCHEMA_VERSION = "2.0"
SOURCE_SCHEMA_VERSIONS = ["1.0", "1.1", "1.2", None]  # None = no version field


@dataclass
class MigrationResult:
    """Result of a single file migration."""
    file_path: str
    file_type: str  # status, log, workflow
    action: str  # migrated, skipped, error
    changes: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class MigrationSummary:
    """Summary of migration run."""
    total_files_scanned: int = 0
    files_migrated: int = 0
    files_skipped: int = 0
    files_errored: int = 0
    backup_created: bool = False
    backup_path: Optional[str] = None
    results: List[MigrationResult] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class StateMigrator:
    """
    Handles migration of state files to v2.0 format.

    Migration tasks:
    1. Add schema_version field to status.json files
    2. Add idempotency_key to probability_history entries
    3. Add _version_meta to status.json for version tracking
    4. Add rotation_metadata to log files
    """

    def __init__(self, outputs_dir: Path, dry_run: bool = False,
                 backup_dir: Optional[Path] = None):
        self.outputs_dir = Path(outputs_dir)
        self.dry_run = dry_run
        self.backup_dir = Path(backup_dir) if backup_dir else None
        self.summary = MigrationSummary()

    def run(self) -> MigrationSummary:
        """Execute the full migration."""
        logger.info(f"Starting migration {'(DRY RUN)' if self.dry_run else ''}")
        logger.info(f"Target directory: {self.outputs_dir}")

        # Create backup if requested
        if self.backup_dir and not self.dry_run:
            self._create_backup()

        # Find and migrate status.json files
        status_files = list(self.outputs_dir.glob("**/status.json"))
        logger.info(f"Found {len(status_files)} status.json files")

        for status_file in status_files:
            self.summary.total_files_scanned += 1
            result = self._migrate_status_file(status_file)
            self.summary.results.append(result)
            self._update_summary_counts(result)

        # Find and migrate log files
        log_patterns = [
            "**/checkpoint-log.json",
            "**/error-log.json",
            "**/deferred-review-queue.json",
            "**/violation-queue.json"
        ]
        for pattern in log_patterns:
            for log_file in self.outputs_dir.glob(pattern):
                self.summary.total_files_scanned += 1
                result = self._migrate_log_file(log_file)
                self.summary.results.append(result)
                self._update_summary_counts(result)

        # Find and migrate workflow-state.json
        workflow_files = list(self.outputs_dir.glob("**/workflow-state.json"))
        for wf_file in workflow_files:
            self.summary.total_files_scanned += 1
            result = self._migrate_workflow_file(wf_file)
            self.summary.results.append(result)
            self._update_summary_counts(result)

        self.summary.completed_at = datetime.now(timezone.utc).isoformat()
        return self.summary

    def _create_backup(self) -> None:
        """Create backup of outputs directory."""
        if not self.backup_dir:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"pre_migration_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)

        # Copy status.json files to backup
        for status_file in self.outputs_dir.glob("**/status.json"):
            relative_path = status_file.relative_to(self.outputs_dir)
            dest = backup_path / relative_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(status_file, dest)

        self.summary.backup_created = True
        self.summary.backup_path = str(backup_path)
        logger.info(f"Created backup at: {backup_path}")

    def _migrate_status_file(self, file_path: Path) -> MigrationResult:
        """Migrate a status.json file to v2.0 format."""
        result = MigrationResult(
            file_path=str(file_path),
            file_type="status",
            action="skipped"
        )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            changes = []

            # 1. Check/add schema_version
            current_version = data.get('schema_version')
            if current_version == TARGET_SCHEMA_VERSION:
                result.action = "skipped"
                result.changes.append(f"Already at schema version {TARGET_SCHEMA_VERSION}")
                return result

            if current_version not in SOURCE_SCHEMA_VERSIONS:
                result.action = "error"
                result.error = f"Unknown schema version: {current_version}"
                return result

            data['schema_version'] = TARGET_SCHEMA_VERSION
            changes.append(f"Updated schema_version: {current_version} -> {TARGET_SCHEMA_VERSION}")

            # 2. Add idempotency keys to probability_history
            if 'probability_history' in data and isinstance(data['probability_history'], list):
                bank_id = data.get('bank_id', 'unknown')
                for i, entry in enumerate(data['probability_history']):
                    if isinstance(entry, dict) and 'idempotency_key' not in entry:
                        # Generate idempotency key from existing data
                        stage = entry.get('stage', f'stage_{i}')
                        timestamp = entry.get('timestamp', datetime.now(timezone.utc).isoformat())
                        key = self._generate_idempotency_key(stage, bank_id, timestamp)
                        entry['idempotency_key'] = key
                        changes.append(f"Added idempotency_key to probability_history[{i}]")

            # 3. Add version metadata if not present
            if '_version_meta' not in data:
                data['_version_meta'] = {
                    'version': 1,
                    'created_at': datetime.now(timezone.utc).isoformat(),
                    'trigger': 'migration_v2',
                    'checksum': self._compute_checksum(data)
                }
                changes.append("Added _version_meta")

            # 4. Normalize probability scale if needed (0-100 -> 0-1)
            prob_fields = ['prior_probability', 'current_probability', 'probability_architect']
            for pf in prob_fields:
                if pf in data and data[pf] is not None:
                    if data[pf] > 1.0 and data[pf] <= 100.0:
                        old_val = data[pf]
                        data[pf] = data[pf] / 100.0
                        changes.append(f"Normalized {pf}: {old_val} -> {data[pf]}")

            # 5. Add probability_pragmatist if probability_architect exists
            if 'probability_architect' in data and 'probability_pragmatist' not in data:
                data['probability_pragmatist'] = 1.0 - data['probability_architect']
                changes.append("Added calculated probability_pragmatist")

            # Save if not dry run
            if not self.dry_run and changes:
                self._atomic_write(file_path, data)
                result.action = "migrated"
            elif changes:
                result.action = "would_migrate"

            result.changes = changes

        except json.JSONDecodeError as e:
            result.action = "error"
            result.error = f"JSON parse error: {e}"
        except Exception as e:
            result.action = "error"
            result.error = str(e)

        return result

    def _migrate_log_file(self, file_path: Path) -> MigrationResult:
        """Migrate a log file to include rotation metadata."""
        result = MigrationResult(
            file_path=str(file_path),
            file_type="log",
            action="skipped"
        )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            changes = []

            # Add rotation_metadata if not present
            if 'rotation_metadata' not in data:
                data['rotation_metadata'] = {
                    'last_rotation': None,
                    'total_entries_archived': 0,
                    'archive_count': 0,
                    'migrated_at': datetime.now(timezone.utc).isoformat()
                }
                changes.append("Added rotation_metadata")

            # Add schema_version if not present
            if 'schema_version' not in data:
                data['schema_version'] = TARGET_SCHEMA_VERSION
                changes.append(f"Added schema_version: {TARGET_SCHEMA_VERSION}")

            # Ensure entries array exists
            if 'entries' not in data and isinstance(data.get('items'), list):
                # Rename 'items' to 'entries' for consistency
                data['entries'] = data.pop('items')
                changes.append("Renamed 'items' to 'entries'")
            elif 'entries' not in data and isinstance(data.get('queue'), list):
                # Keep queue for review/violation queues
                pass
            elif 'entries' not in data and isinstance(data.get('events'), list):
                # Keep events for checkpoint logs
                pass

            # Save if not dry run
            if not self.dry_run and changes:
                self._atomic_write(file_path, data)
                result.action = "migrated"
            elif changes:
                result.action = "would_migrate"
            else:
                result.action = "skipped"
                result.changes.append("No changes needed")

            result.changes = changes

        except json.JSONDecodeError as e:
            result.action = "error"
            result.error = f"JSON parse error: {e}"
        except Exception as e:
            result.action = "error"
            result.error = str(e)

        return result

    def _migrate_workflow_file(self, file_path: Path) -> MigrationResult:
        """Migrate workflow-state.json file."""
        result = MigrationResult(
            file_path=str(file_path),
            file_type="workflow",
            action="skipped"
        )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            changes = []

            # Add schema_version if not present
            current_version = data.get('schema_version')
            if current_version != TARGET_SCHEMA_VERSION:
                data['schema_version'] = TARGET_SCHEMA_VERSION
                changes.append(f"Updated schema_version: {current_version} -> {TARGET_SCHEMA_VERSION}")

            # Add migration marker
            if '_migration_info' not in data:
                data['_migration_info'] = {
                    'migrated_at': datetime.now(timezone.utc).isoformat(),
                    'from_version': current_version,
                    'to_version': TARGET_SCHEMA_VERSION
                }
                changes.append("Added _migration_info")

            # Save if not dry run
            if not self.dry_run and changes:
                self._atomic_write(file_path, data)
                result.action = "migrated"
            elif changes:
                result.action = "would_migrate"
            else:
                result.action = "skipped"
                result.changes.append("No changes needed")

            result.changes = changes

        except json.JSONDecodeError as e:
            result.action = "error"
            result.error = f"JSON parse error: {e}"
        except Exception as e:
            result.action = "error"
            result.error = str(e)

        return result

    def _generate_idempotency_key(self, stage: str, bank_id: str, timestamp: str) -> str:
        """Generate idempotency key for probability history entry."""
        # Truncate timestamp to minute precision
        ts_minute = timestamp[:16] if len(timestamp) >= 16 else timestamp
        raw = f"{stage}_{bank_id}_{ts_minute}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _compute_checksum(self, data: dict) -> str:
        """Compute checksum of data for version tracking."""
        # Exclude _version_meta from checksum
        data_copy = {k: v for k, v in data.items() if k != '_version_meta'}
        content = json.dumps(data_copy, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def _atomic_write(self, path: Path, data: dict) -> None:
        """Write data atomically using temp file + rename."""
        temp_path = path.with_suffix('.tmp')
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            temp_path.replace(path)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def _update_summary_counts(self, result: MigrationResult) -> None:
        """Update summary counts based on result."""
        if result.action in ("migrated", "would_migrate"):
            self.summary.files_migrated += 1
        elif result.action == "skipped":
            self.summary.files_skipped += 1
        elif result.action == "error":
            self.summary.files_errored += 1


def create_version_backups(outputs_dir: Path, dry_run: bool = False) -> int:
    """
    Create version backups for all status.json files.

    This sets up the versioning directory structure for existing files.

    Returns:
        Number of version backups created
    """
    count = 0
    for status_file in outputs_dir.glob("**/status.json"):
        versions_dir = status_file.parent / "versions"

        if dry_run:
            logger.info(f"Would create versions directory: {versions_dir}")
            count += 1
            continue

        versions_dir.mkdir(exist_ok=True)

        # Check if version 1 already exists
        v1_file = versions_dir / "status.1.json.gz"
        if v1_file.exists():
            logger.debug(f"Version backup already exists: {v1_file}")
            continue

        # Create compressed backup
        try:
            with open(status_file, 'rb') as f_in:
                with gzip.open(v1_file, 'wb') as f_out:
                    f_out.write(f_in.read())
            logger.info(f"Created version backup: {v1_file}")
            count += 1
        except Exception as e:
            logger.error(f"Failed to create backup {v1_file}: {e}")

    return count


def print_summary(summary: MigrationSummary, verbose: bool = False) -> None:
    """Print migration summary to console."""
    print("\n" + "=" * 60)
    print("MIGRATION SUMMARY")
    print("=" * 60)
    print(f"Total files scanned:  {summary.total_files_scanned}")
    print(f"Files migrated:       {summary.files_migrated}")
    print(f"Files skipped:        {summary.files_skipped}")
    print(f"Files with errors:    {summary.files_errored}")
    print(f"Backup created:       {'Yes' if summary.backup_created else 'No'}")
    if summary.backup_path:
        print(f"Backup location:      {summary.backup_path}")
    print(f"Started at:           {summary.started_at}")
    print(f"Completed at:         {summary.completed_at}")
    print("=" * 60)

    if verbose or summary.files_errored > 0:
        print("\nDETAILED RESULTS:")
        for result in summary.results:
            status_icon = {
                'migrated': '✓',
                'would_migrate': '~',
                'skipped': '-',
                'error': '✗'
            }.get(result.action, '?')

            print(f"\n{status_icon} [{result.file_type}] {result.file_path}")
            print(f"  Action: {result.action}")

            if result.changes:
                for change in result.changes:
                    print(f"    - {change}")

            if result.error:
                print(f"  ERROR: {result.error}")


def main():
    parser = argparse.ArgumentParser(
        description="Migrate CDM state files to v2.0 format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run to see what would change
  python migrate_state_v2.py --dry-run outputs/

  # Execute migration with backup
  python migrate_state_v2.py outputs/ --backup-dir migrations/backup/

  # Migrate specific bank folder
  python migrate_state_v2.py outputs/phase-1-european-tier-1/deutsche-bank/

  # Create version backups for existing files
  python migrate_state_v2.py outputs/ --create-version-backups
        """
    )

    parser.add_argument(
        'outputs_dir',
        type=Path,
        help='Path to outputs directory or specific bank folder'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '--backup-dir',
        type=Path,
        help='Directory to store pre-migration backup'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output for all files'
    )
    parser.add_argument(
        '--summary-only',
        action='store_true',
        help='Only show summary, do not migrate'
    )
    parser.add_argument(
        '--create-version-backups',
        action='store_true',
        help='Create initial version backups for versioning system'
    )
    parser.add_argument(
        '--output-json',
        type=Path,
        help='Write migration summary to JSON file'
    )

    args = parser.parse_args()

    if not args.outputs_dir.exists():
        print(f"Error: Directory not found: {args.outputs_dir}")
        sys.exit(1)

    # Handle version backup creation
    if args.create_version_backups:
        print("Creating version backups for existing status.json files...")
        count = create_version_backups(args.outputs_dir, args.dry_run)
        print(f"{'Would create' if args.dry_run else 'Created'} {count} version backups")
        sys.exit(0)

    # Run migration
    migrator = StateMigrator(
        outputs_dir=args.outputs_dir,
        dry_run=args.dry_run or args.summary_only,
        backup_dir=args.backup_dir
    )

    summary = migrator.run()

    # Print summary
    print_summary(summary, verbose=args.verbose)

    # Write JSON summary if requested
    if args.output_json:
        with open(args.output_json, 'w') as f:
            json.dump(summary.to_dict(), f, indent=2)
        print(f"\nMigration summary written to: {args.output_json}")

    # Exit with error code if there were errors
    if summary.files_errored > 0:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
