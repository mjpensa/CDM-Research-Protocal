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
from markdown_parser import validate_bank_outputs, parse_bayesian_file, parse_evidence_file
from bayesian_calculator import BayesianCalculator
from url_validator import validate_bank_urls

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


def validate_bayesian_calculations(bank_dir: Path) -> dict:
    """
    Validate Bayesian calculations against Python implementation.

    Args:
        bank_dir: Path to bank directory

    Returns:
        dict with 'valid', 'issues', and 'warnings'
    """
    calc = BayesianCalculator()
    results = {'valid': True, 'issues': [], 'warnings': []}

    evidence_dir = bank_dir / "1-evidence"
    bayesian_dir = bank_dir / "2-bayesian"

    if not bayesian_dir.exists():
        return results

    # For each tier, check independence and extreme LRs
    for tier in [1, 2, 3]:
        bayesian_file = bayesian_dir / f"post-tier{tier}-update.md"
        evidence_file = evidence_dir / f"tier{tier}-evidence.md"

        if not bayesian_file.exists():
            continue

        # Parse agent's output
        try:
            agent_update, parse_result = parse_bayesian_file(str(bayesian_file))
        except Exception as e:
            results['issues'].append(f"Tier {tier}: Could not parse Bayesian file: {e}")
            continue

        if not agent_update:
            results['issues'].append(f"Tier {tier}: Empty Bayesian update")
            continue

        # Parse evidence
        evidence_blocks = []
        if evidence_file.exists():
            try:
                evidence_blocks, _ = parse_evidence_file(str(evidence_file))
            except Exception:
                pass

        # Convert evidence blocks to calculator format for independence check
        evidence_items = []
        for block in evidence_blocks:
            evidence_items.append({
                'type': 'unknown',
                'tier': block.tier,
                'source_url': block.source_url
            })

        # Check independence
        if evidence_items:
            independence = calc.check_independence(evidence_items)
            if not independence.independent:
                results['valid'] = False
                for warning in independence.warnings:
                    results['issues'].append(f"Tier {tier} Independence: {warning}")

        # Check extreme LR (if combined LR is available and not placeholder)
        if agent_update.combined_lr > 0 and agent_update.combined_lr != 1.0:
            lower_bound, upper_bound = calc.extreme_lr_bounds
            if agent_update.combined_lr > upper_bound:
                results['warnings'].append(
                    f"Tier {tier}: Extreme LR ({agent_update.combined_lr:.2f}) exceeds {upper_bound}"
                )
            elif agent_update.combined_lr < lower_bound:
                results['warnings'].append(
                    f"Tier {tier}: Extreme LR ({agent_update.combined_lr:.4f}) below {lower_bound}"
                )

        # Check probability validity
        if agent_update.posterior_architect > 0:
            if agent_update.posterior_architect > 0.95:
                results['warnings'].append(
                    f"Tier {tier}: Posterior ({agent_update.posterior_architect:.1%}) exceeds confidence cap"
                )

    return results


def run_pipeline(path_input: str, skip_verification: bool = False, validate_urls_first: bool = False) -> dict:
    """
    Run complete pipeline on a bank directory or evidence.json file.
    Automatically converts Markdown to JSON if needed.

    Args:
        path_input: Path to bank directory or evidence.json file
        skip_verification: Skip URL verification step
        validate_urls_first: Validate URLs before processing

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

    # Step 0.5: Validate Markdown structure
    logger.info("\n[0.5/3] Validating markdown structure...")
    try:
        md_results = validate_bank_outputs(str(bank_dir))
        md_errors = []
        md_warnings = []

        for file_type, md_result in md_results.items():
            md_errors.extend([f"{file_type}: {e}" for e in md_result.get('errors', [])])
            md_warnings.extend([f"{file_type}: {w}" for w in md_result.get('warnings', [])])

        if md_errors:
            logger.error(f"  Markdown validation: {len(md_errors)} errors")
            for err in md_errors[:5]:  # Show first 5
                logger.error(f"    {err}")
            result["steps"]["markdown_validation"] = "errors"
            result["markdown_errors"] = md_errors
        elif md_warnings:
            logger.warning(f"  Markdown validation: {len(md_warnings)} warnings")
            for warn in md_warnings[:3]:  # Show first 3
                logger.warning(f"    {warn}")
            result["steps"]["markdown_validation"] = "warnings"
        else:
            logger.info("  Markdown validation: PASSED")
            result["steps"]["markdown_validation"] = "success"

    except Exception as e:
        logger.warning(f"  Markdown validation skipped: {e}")
        result["steps"]["markdown_validation"] = f"skipped: {e}"

    # Step 0.6: Validate Bayesian calculations
    logger.info("\n[0.6/3] Validating Bayesian calculations...")
    try:
        bayes_results = validate_bayesian_calculations(bank_dir)

        if bayes_results['issues']:
            logger.error(f"  Bayesian validation: {len(bayes_results['issues'])} issues")
            for issue in bayes_results['issues'][:3]:
                logger.error(f"    {issue}")
            result["steps"]["bayesian_validation"] = "issues"
            result["bayesian_issues"] = bayes_results['issues']
        elif bayes_results['warnings']:
            logger.warning(f"  Bayesian validation: {len(bayes_results['warnings'])} warnings")
            for warn in bayes_results['warnings'][:3]:
                logger.warning(f"    {warn}")
            result["steps"]["bayesian_validation"] = "warnings"
        else:
            logger.info("  Bayesian validation: PASSED")
            result["steps"]["bayesian_validation"] = "success"

    except Exception as e:
        logger.warning(f"  Bayesian validation skipped: {e}")
        result["steps"]["bayesian_validation"] = f"skipped: {e}"

    # Step 0.7: Pre-validate URLs (optional)
    if validate_urls_first:
        logger.info("\n[0.7/3] Pre-validating URLs...")
        try:
            url_results = validate_bank_urls(str(bank_dir))

            if url_results.get('dead', 0) > 0:
                logger.warning(f"  URL validation: {url_results['dead']} dead URLs detected")
                for dead_url in url_results.get('dead_urls', [])[:3]:
                    logger.warning(f"    {dead_url['url'][:50]}...")
                result["steps"]["url_validation"] = "dead_urls"
                result["flags"].append("DEAD_URLS_DETECTED")
            elif url_results.get('total', 0) == 0:
                logger.info("  URL validation: No URLs to check")
                result["steps"]["url_validation"] = "no_urls"
            else:
                logger.info(f"  URL validation: {url_results['alive']}/{url_results['total']} alive")
                result["steps"]["url_validation"] = "success"

        except Exception as e:
            logger.warning(f"  URL pre-validation skipped: {e}")
            result["steps"]["url_validation"] = f"skipped: {e}"

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


def run_batch(directory: str, skip_verification: bool = False, validate_urls_first: bool = False) -> list:
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
        result = run_pipeline(str(bank_dir), skip_verification, validate_urls_first)
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
    parser.add_argument(
        "--validate-urls-first",
        action="store_true",
        help="Validate URLs before processing (catches dead links early)"
    )
    parser.add_argument(
        "--full-validation",
        action="store_true",
        help="Run full validation pipeline including all Phase 1-6 checks"
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
        results = run_batch(str(path), args.skip_verification, args.validate_urls_first)
        failed = sum(1 for r in results if r['status'] == 'failed')
        sys.exit(1 if failed > 0 else 0)

    else:
        if not path.exists():
            print(f"Error: File not found: {path}")
            sys.exit(1)
        result = run_pipeline(str(path), args.skip_verification, args.validate_urls_first)

        # Run full validation if requested
        if args.full_validation:
            try:
                from research_runner import ResearchRunner

                # Determine bank directory
                if path.suffix == '.json':
                    bank_dir = path.parent
                else:
                    bank_dir = path

                runner = ResearchRunner()
                validation = runner.run_validation_pipeline(bank_dir)

                result["full_validation"] = validation

                if not validation.get('valid', True):
                    result["status"] = "validation_failed"
                    logger.warning("Full validation found issues")
                else:
                    logger.info("Full validation passed")

            except ImportError as e:
                logger.warning(f"Could not run full validation: {e}")
            except Exception as e:
                logger.error(f"Full validation error: {e}")
                result["full_validation"] = {"error": str(e)}

        sys.exit(0 if result['status'] == 'complete' else 1)


if __name__ == "__main__":
    main()
