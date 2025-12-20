"""
CDM Forensic Research Engine v2.3 - Unified Pipeline
Runs the complete verification pipeline in one command:
  1. process_evidence.py → URL verification, content hashing
  2. trust_audit.py → Trust metrics calculation
  3. render_report.py → Final report generation

Usage:
  python tools/run_pipeline.py outputs/{Bank}/evidence.json
  python tools/run_pipeline.py --batch outputs/phase-1-european-tier1/
  python tools/run_pipeline.py --watch outputs/  # Monitor for new evidence.json files
"""

import sys
import json
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime

# Add tools directory to path for imports
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from process_evidence import process_bank_evidence
from trust_audit import run_trust_audit
from render_report import render_report
from markdown_to_json import convert_bank_directory

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_negative_facts(bank_id: str) -> list:
    """
    Check if bank is mentioned in knowledge_base/negative_facts.md.

    These are known dead ends that should be reviewed before proceeding.

    Args:
        bank_id: Bank identifier

    Returns:
        List of warnings if bank found in negative facts
    """
    nf_path = SCRIPT_DIR.parent / 'knowledge_base' / 'negative_facts.md'
    if not nf_path.exists():
        return []

    try:
        content = nf_path.read_text(encoding='utf-8').lower()
        bank_variants = [
            bank_id.lower(),
            bank_id.replace('-', ' '),
            bank_id.replace('-', ''),
        ]

        for variant in bank_variants:
            if variant in content:
                return [f"Bank '{bank_id}' mentioned in negative_facts.md - review known dead ends"]

    except Exception as e:
        logger.debug(f"Could not check negative facts: {e}")

    return []


def ensure_evidence_json(bank_dir: Path) -> Path:
    """
    Ensure evidence.json exists for a bank. Convert from Markdown if needed.

    Args:
        bank_dir: Path to bank directory (e.g., outputs/phase-1/deutsche-bank)

    Returns:
        Path to evidence.json file
    """
    json_path = bank_dir / 'evidence.json'
    evidence_dir = bank_dir / '1-evidence'

    # Check if Markdown evidence files exist
    md_exists = evidence_dir.exists() and any(evidence_dir.glob('tier*-evidence.md'))

    # Determine if we need to create or refresh JSON
    needs_create = not json_path.exists()

    if json_path.exists() and md_exists:
        # Check if any Markdown file is newer than the JSON
        json_mtime = json_path.stat().st_mtime
        md_files = list(evidence_dir.glob('tier*-evidence.md'))
        if md_files:
            md_mtime = max(f.stat().st_mtime for f in md_files)
            needs_create = md_mtime > json_mtime

    if md_exists and needs_create:
        logger.info(f"Converting Markdown to JSON for {bank_dir.name}")
        try:
            result = convert_bank_directory(bank_dir)
            json_path.write_text(json.dumps(result, indent=2), encoding='utf-8')
            logger.info(f"  Created evidence.json with {len(result['evidence_items'])} items")
        except Exception as e:
            logger.error(f"Failed to convert Markdown: {e}")

    return json_path


def run_pipeline(path_input: str, skip_verification: bool = False) -> dict:
    """
    Run complete pipeline on a bank directory or evidence.json file.
    Automatically converts Markdown to JSON if needed.

    Args:
        path_input: Path to bank directory or evidence.json file
        skip_verification: Skip URL verification step

    Returns:
        dict with status and metrics
    """
    path = Path(path_input).resolve()

    # Handle directory input - find or create evidence.json
    if path.is_dir():
        bank_dir = path
        json_path = ensure_evidence_json(bank_dir)
    elif path.name == 'evidence.json':
        json_path = path
        bank_dir = path.parent
    elif path.suffix == '.json':
        json_path = path
        bank_dir = path.parent
    else:
        # Assume it's a bank directory
        bank_dir = path
        json_path = ensure_evidence_json(bank_dir)

    if not json_path.exists():
        return {
            "file": str(json_path),
            "status": "failed",
            "error": "No evidence.json found and no Markdown files to convert",
            "steps": {},
            "confidence": None,
            "flags": []
        }

    result = {
        "file": str(json_path),
        "status": "pending",
        "steps": {},
        "confidence": None,
        "flags": []
    }

    logger.info(f"\n{'='*60}")
    logger.info(f"PIPELINE: {bank_dir.name}")
    logger.info(f"{'='*60}")

    # Check negative facts for known dead ends
    negative_warnings = check_negative_facts(bank_dir.name)
    for warning in negative_warnings:
        logger.warning(f"KNOWLEDGE BASE: {warning}")
        result["flags"].append("NEGATIVE_FACTS_WARNING")

    # Step 1: Process Evidence (URL verification)
    if not skip_verification:
        logger.info("\n[1/3] Processing evidence (URL verification)...")
        try:
            success = process_bank_evidence(str(json_path))
            result["steps"]["process_evidence"] = "success" if success else "failed"
            if not success:
                result["status"] = "failed"
                logger.error("Pipeline failed at step 1: process_evidence")
                return result
        except Exception as e:
            result["steps"]["process_evidence"] = f"error: {e}"
            result["status"] = "failed"
            logger.error(f"Pipeline failed at step 1: {e}")
            return result
    else:
        logger.info("\n[1/3] Skipping URL verification (--skip-verification)")
        result["steps"]["process_evidence"] = "skipped"

    # Step 2: Trust Audit
    logger.info("\n[2/3] Running trust audit...")
    try:
        audit_result = run_trust_audit(str(json_path))
        result["steps"]["trust_audit"] = "success"
        result["confidence"] = audit_result.get("trust_metrics", {}).get("overall_confidence")
        result["flags"] = audit_result.get("trust_metrics", {}).get("flags", [])
    except Exception as e:
        result["steps"]["trust_audit"] = f"error: {e}"
        result["status"] = "failed"
        logger.error(f"Pipeline failed at step 2: {e}")
        return result

    # Step 3: Render Report
    logger.info("\n[3/3] Rendering report...")
    try:
        success = render_report(str(json_path))
        result["steps"]["render_report"] = "success" if success else "failed"
        if not success:
            result["status"] = "failed"
            logger.error("Pipeline failed at step 3: render_report")
            return result
    except Exception as e:
        result["steps"]["render_report"] = f"error: {e}"
        result["status"] = "failed"
        logger.error(f"Pipeline failed at step 3: {e}")
        return result

    result["status"] = "complete"

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info(f"PIPELINE COMPLETE: {json_path.parent.name}")
    logger.info(f"  Confidence: {result['confidence']}%")
    if result["flags"]:
        logger.info(f"  Flags: {', '.join(result['flags'][:5])}")
    logger.info(f"  Report: {json_path.parent / 'Final_Report.md'}")
    logger.info(f"{'='*60}\n")

    return result


def run_batch(directory: str, skip_verification: bool = False) -> list:
    """
    Run pipeline on all bank directories in a directory tree.
    Automatically converts Markdown to JSON if needed.
    """
    directory = Path(directory).resolve()

    # Find all bank directories (those with 1-evidence subdirectory)
    bank_dirs = []
    for path in directory.rglob('1-evidence'):
        if path.is_dir():
            bank_dirs.append(path.parent)

    # Also include directories with existing evidence.json
    for json_file in directory.rglob('evidence.json'):
        bank_dir = json_file.parent
        if bank_dir not in bank_dirs:
            bank_dirs.append(bank_dir)

    # Sort for consistent ordering
    bank_dirs = sorted(set(bank_dirs))

    logger.info(f"Found {len(bank_dirs)} bank directories")

    results = []
    for i, bank_dir in enumerate(bank_dirs, 1):
        logger.info(f"\n[{i}/{len(bank_dirs)}] Processing {bank_dir.name}...")
        result = run_pipeline(str(bank_dir), skip_verification)
        results.append(result)

    # Summary table
    print("\n" + "=" * 70)
    print("BATCH PIPELINE SUMMARY")
    print("=" * 70)
    print(f"{'Bank':<25} {'Status':<10} {'Conf':<6} {'Flags'}")
    print("-" * 70)

    for r in sorted(results, key=lambda x: x.get('confidence') or 0, reverse=True):
        bank = Path(r['file']).parent.name
        status = r['status']
        conf = f"{r['confidence']}%" if r['confidence'] else "N/A"
        flags = ', '.join(r['flags'][:3]) if r['flags'] else '-'
        print(f"{bank:<25} {status:<10} {conf:<6} {flags}")

    print("=" * 70)

    return results


def watch_directory(directory: str, interval: int = 30):
    """
    Watch a directory for new or modified evidence.json files.
    Automatically runs pipeline when changes detected.
    """
    directory = Path(directory).resolve()
    logger.info(f"Watching {directory} for changes (interval: {interval}s)")
    logger.info("Press Ctrl+C to stop\n")

    processed = {}  # file -> mtime

    try:
        while True:
            json_files = list(directory.rglob("evidence.json"))

            for json_file in json_files:
                mtime = json_file.stat().st_mtime
                last_mtime = processed.get(str(json_file))

                if last_mtime is None or mtime > last_mtime:
                    # New or modified file
                    logger.info(f"Change detected: {json_file}")
                    run_pipeline(str(json_file))
                    processed[str(json_file)] = mtime

            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("\nWatch stopped")


def main():
    parser = argparse.ArgumentParser(
        description="CDM Forensic Research Pipeline - Run complete verification in one command"
    )
    parser.add_argument(
        "path",
        help="Path to evidence.json file or directory for batch processing"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all evidence.json files in directory tree"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch directory for changes and auto-process"
    )
    parser.add_argument(
        "--watch-interval",
        type=int,
        default=30,
        help="Watch interval in seconds (default: 30)"
    )
    parser.add_argument(
        "--skip-verification",
        action="store_true",
        help="Skip URL verification step (use existing verification data)"
    )

    args = parser.parse_args()
    path = Path(args.path)

    if args.watch:
        if not path.is_dir():
            print("Error: --watch requires a directory path")
            sys.exit(1)
        watch_directory(str(path), args.watch_interval)

    elif args.batch or path.is_dir():
        if not path.is_dir():
            print("Error: --batch requires a directory path")
            sys.exit(1)
        results = run_batch(str(path), args.skip_verification)
        failed = sum(1 for r in results if r['status'] == 'failed')
        sys.exit(1 if failed > 0 else 0)

    else:
        if not path.exists():
            print(f"Error: File not found: {path}")
            sys.exit(1)
        result = run_pipeline(str(path), args.skip_verification)
        sys.exit(0 if result['status'] == 'complete' else 1)


if __name__ == "__main__":
    main()
