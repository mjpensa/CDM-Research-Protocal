"""
CDM Research Protocol - Terminology Migration Tool v1.0

Migrates deprecated classification terms to current taxonomy.

Deprecated terms:
- NOT ENGAGED -> PRAGMATIST
- NON-ARCHITECT -> PRAGMATIST
- NOT_ENGAGED -> PRAGMATIST
- NON_ARCHITECT -> PRAGMATIST

Usage:
    python migrate_terminology.py <path>              # Preview changes (dry run)
    python migrate_terminology.py <path> --apply     # Apply changes
"""

import re
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Migration patterns: (regex, replacement)
MIGRATIONS = [
    # JSON string values (quoted)
    (re.compile(r'"NOT ENGAGED"', re.IGNORECASE), '"PRAGMATIST"'),
    (re.compile(r'"NON-ARCHITECT"', re.IGNORECASE), '"PRAGMATIST"'),
    (re.compile(r'"NOT_ENGAGED"', re.IGNORECASE), '"PRAGMATIST"'),
    (re.compile(r'"NON_ARCHITECT"', re.IGNORECASE), '"PRAGMATIST"'),
    # Markdown/prose (word boundaries)
    (re.compile(r'\bNOT ENGAGED\b', re.IGNORECASE), 'PRAGMATIST'),
    (re.compile(r'\bNON-ARCHITECT\b', re.IGNORECASE), 'PRAGMATIST'),
    (re.compile(r'\bNOT_ENGAGED\b', re.IGNORECASE), 'PRAGMATIST'),
    (re.compile(r'\bNON_ARCHITECT\b', re.IGNORECASE), 'PRAGMATIST'),
]


def migrate_file(path: Path, dry_run: bool = True) -> dict:
    """
    Migrate deprecated terms in a single file.

    Args:
        path: Path to file
        dry_run: If True, don't modify file

    Returns:
        dict with file path and list of changes made
    """
    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return {'file': str(path), 'changes': [], 'error': 'Binary file skipped'}

    original = content
    changes = []

    for pattern, replacement in MIGRATIONS:
        matches = pattern.findall(content)
        if matches:
            changes.append(f"{pattern.pattern} -> {replacement} ({len(matches)} occurrences)")
            content = pattern.sub(replacement, content)

    if changes and not dry_run:
        # Create backup
        backup_path = path.with_suffix(path.suffix + '.bak')
        backup_path.write_text(original, encoding='utf-8')
        # Write updated content
        path.write_text(content, encoding='utf-8')

    return {'file': str(path), 'changes': changes}


def migrate_all(directory: Path, dry_run: bool = True) -> list:
    """
    Migrate all JSON and Markdown files in directory tree.

    Args:
        directory: Root directory to scan
        dry_run: If True, don't modify files

    Returns:
        List of results for files with changes
    """
    results = []

    for ext in ['*.json', '*.md']:
        for path in directory.rglob(ext):
            # Skip backup files
            if '.bak' in path.suffixes:
                continue
            # Skip node_modules, .git, etc.
            if any(part.startswith('.') or part == 'node_modules' for part in path.parts):
                continue

            result = migrate_file(path, dry_run)
            if result['changes']:
                results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Migrate deprecated classification terms to current taxonomy"
    )
    parser.add_argument(
        'path',
        help="File or directory to process"
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help="Apply changes (default is dry run)"
    )

    args = parser.parse_args()
    path = Path(args.path).resolve()

    if not path.exists():
        print(f"Error: Path not found: {path}")
        sys.exit(1)

    dry_run = not args.apply

    if path.is_file():
        results = [migrate_file(path, dry_run)]
        results = [r for r in results if r['changes']]
    else:
        results = migrate_all(path, dry_run)

    # Print results
    mode = "DRY RUN - " if dry_run else ""
    print(f"\n{mode}Found {len(results)} files with deprecated terms\n")

    for r in results:
        print(f"  {r['file']}:")
        for change in r['changes']:
            print(f"    - {change}")
        print()

    if dry_run and results:
        print("Run with --apply to make changes (backups will be created)")
    elif not dry_run and results:
        print(f"Applied changes to {len(results)} files (backups created with .bak extension)")


if __name__ == "__main__":
    main()
