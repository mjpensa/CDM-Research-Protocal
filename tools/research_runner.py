"""
CDM Research Protocol - Research Runner v1.0

End-to-end research execution and validation for banks.
Orchestrates all tools and validates at each stage.

Usage:
    python research_runner.py --bank barclays --phase 1
    python research_runner.py --phase 1 --all
    python research_runner.py --validate-only outputs/phase-1/barclays/
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import load_bank_manifest, get_bank_config
from markdown_parser import validate_bank_outputs, parse_evidence_file, parse_bayesian_file
from bayesian_calculator import BayesianCalculator
from url_validator import URLValidator, validate_evidence_urls
from trust_audit import run_trust_audit
from cross_bank_validator import run_checks
from orchestrate import Stage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class StageResult:
    """Result of executing a stage."""
    stage: str
    success: bool
    duration_seconds: float
    outputs: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class BankResult:
    """Result of researching a bank."""
    bank_id: str
    phase: int
    success: bool
    classification: Optional[str] = None
    confidence: Optional[float] = None
    stages: List[StageResult] = field(default_factory=list)
    total_duration: float = 0.0


class ResearchRunner:
    """
    Orchestrates end-to-end research validation for banks.
    """

    def __init__(self, outputs_dir: Path = None):
        self.outputs_dir = outputs_dir or PROJECT_ROOT / "outputs"
        self.bayesian_calc = BayesianCalculator()
        self.url_validator = URLValidator()

    def get_bank_dir(self, bank_id: str, phase: int) -> Path:
        """Get output directory for a bank."""
        # Find the phase directory
        for phase_dir in self.outputs_dir.iterdir():
            if phase_dir.is_dir() and f"phase-{phase}" in phase_dir.name:
                bank_dir = phase_dir / bank_id
                return bank_dir

        # Create if doesn't exist
        phase_name = f"phase-{phase}"
        try:
            manifest = load_bank_manifest()
            for phase_info in manifest.get('phases', []):
                if phase_info.get('number') == phase:
                    phase_name = f"phase-{phase}-{phase_info.get('name', '')}"
                    break
        except Exception:
            pass

        bank_dir = self.outputs_dir / phase_name / bank_id
        bank_dir.mkdir(parents=True, exist_ok=True)
        return bank_dir

    def validate_stage(self, bank_dir: Path, stage: str) -> StageResult:
        """Validate outputs for a completed stage."""
        start_time = datetime.now()
        result = StageResult(stage=stage, success=True, duration_seconds=0)

        if stage.startswith('tier') and stage.endswith('_evidence'):
            # Validate evidence file
            tier = stage.replace('tier', '').replace('_evidence', '')
            evidence_file = bank_dir / "1-evidence" / f"tier{tier}-evidence.md"

            if not evidence_file.exists():
                result.errors.append(f"Missing: {evidence_file.name}")
                result.success = False
            else:
                blocks, validation = parse_evidence_file(str(evidence_file))

                if not validation.valid:
                    result.errors.extend(validation.errors)
                    result.success = False
                result.warnings.extend(validation.warnings)
                result.outputs.append(str(evidence_file))

        elif stage.startswith('bayesian_'):
            # Validate Bayesian file
            tier = stage.replace('bayesian_', '')
            bayesian_file = bank_dir / "2-bayesian" / f"post-tier{tier}-update.md"

            if not bayesian_file.exists():
                result.errors.append(f"Missing: {bayesian_file.name}")
                result.success = False
            else:
                update, validation = parse_bayesian_file(str(bayesian_file))

                if not validation.valid:
                    result.errors.extend(validation.errors)
                    result.success = False
                result.warnings.extend(validation.warnings)
                result.outputs.append(str(bayesian_file))

        elif stage.startswith('gate_'):
            # Validate gate file
            gate_name = stage.replace('gate_', '')
            gate_file = bank_dir / "3-gates" / f"{gate_name}.md"

            if not gate_file.exists():
                result.errors.append(f"Missing: {gate_file.name}")
                result.success = False
            else:
                result.outputs.append(str(gate_file))

        result.duration_seconds = (datetime.now() - start_time).total_seconds()
        return result

    def run_validation_pipeline(self, bank_dir: Path) -> dict:
        """
        Run full validation pipeline on existing bank outputs.

        Returns:
            Dict with validation results
        """
        logger.info(f"Running validation pipeline for {bank_dir.name}")

        results = {
            'bank': bank_dir.name,
            'valid': True,
            'stages': {}
        }

        # 1. Validate markdown structure
        logger.info("  [1/4] Validating markdown structure...")
        try:
            md_results = validate_bank_outputs(str(bank_dir))
            results['stages']['markdown'] = md_results

            md_errors = sum(len(r.get('errors', [])) for r in md_results.values() if isinstance(r, dict))
            if md_errors > 0:
                results['valid'] = False
        except Exception as e:
            logger.warning(f"Markdown validation error: {e}")
            results['stages']['markdown'] = {'error': str(e)}

        # 2. Validate URLs
        logger.info("  [2/4] Validating URLs...")
        evidence_dir = bank_dir / "1-evidence"
        url_results = {'alive': 0, 'dead': 0, 'checked': 0}

        if evidence_dir.exists():
            for tier_file in evidence_dir.glob("tier*-evidence.md"):
                try:
                    tier_urls = validate_evidence_urls(str(tier_file))
                    url_results['alive'] += tier_urls.get('alive', 0)
                    url_results['dead'] += tier_urls.get('dead', 0)
                    url_results['checked'] += tier_urls.get('total', 0)
                except Exception as e:
                    logger.warning(f"URL validation error for {tier_file.name}: {e}")

        results['stages']['urls'] = url_results

        # 3. Run trust audit
        logger.info("  [3/4] Running trust audit...")
        evidence_json = bank_dir / "evidence.json"

        if evidence_json.exists():
            try:
                trust_results = run_trust_audit(str(evidence_json))
                results['stages']['trust'] = trust_results.get('trust_metrics', {})
                results['confidence'] = trust_results.get('trust_metrics', {}).get('overall_confidence')
            except Exception as e:
                logger.warning(f"Trust audit error: {e}")
                results['stages']['trust'] = {'error': str(e)}
        else:
            results['stages']['trust'] = {'skipped': 'No evidence.json found'}

        # 4. Validate status.json
        logger.info("  [4/4] Validating status...")
        status_file = bank_dir / "status.json"

        if status_file.exists():
            try:
                status = json.loads(status_file.read_text(encoding='utf-8'))
                results['classification'] = status.get('classification')
                results['stages']['status'] = {
                    'classification': status.get('classification'),
                    'sub_classification': status.get('sub_classification'),
                    'confidence': status.get('confidence'),
                    'stages_completed': status.get('stages_completed', [])
                }
            except Exception as e:
                logger.warning(f"Status validation error: {e}")
                results['stages']['status'] = {'error': str(e)}
        else:
            results['stages']['status'] = {'skipped': 'No status.json found'}

        return results

    def run_bank(self, bank_id: str, phase: int) -> BankResult:
        """
        Execute full validation pipeline for a bank.

        Args:
            bank_id: Bank identifier
            phase: Phase number

        Returns:
            BankResult with validation details
        """
        start_time = datetime.now()
        bank_dir = self.get_bank_dir(bank_id, phase)

        result = BankResult(
            bank_id=bank_id,
            phase=phase,
            success=True
        )

        logger.info(f"Starting validation for {bank_id} (Phase {phase})")
        logger.info(f"Output directory: {bank_dir}")

        if not bank_dir.exists():
            result.success = False
            result.stages.append(StageResult(
                stage="init",
                success=False,
                duration_seconds=0,
                errors=[f"Bank directory not found: {bank_dir}"]
            ))
            return result

        # Get current status
        status_file = bank_dir / "status.json"
        stages_completed = []

        if status_file.exists():
            try:
                status = json.loads(status_file.read_text(encoding='utf-8'))
                stages_completed = status.get('stages_completed', [])
            except Exception:
                pass

        logger.info(f"Stages completed: {stages_completed}")

        # Validate completed stages
        for stage in stages_completed:
            stage_result = self.validate_stage(bank_dir, stage)
            result.stages.append(stage_result)

            if not stage_result.success:
                result.success = False
                logger.error(f"Stage {stage} validation failed")
                for err in stage_result.errors:
                    logger.error(f"  - {err}")

        # Run full validation pipeline
        validation = self.run_validation_pipeline(bank_dir)
        result.classification = validation.get('classification')
        result.confidence = validation.get('confidence')

        if not validation.get('valid', True):
            result.success = False

        result.total_duration = (datetime.now() - start_time).total_seconds()

        logger.info(f"Validation complete for {bank_id}")
        logger.info(f"  Classification: {result.classification}")
        logger.info(f"  Confidence: {result.confidence}%")
        logger.info(f"  Duration: {result.total_duration:.1f}s")

        return result

    def run_phase(self, phase: int) -> List[BankResult]:
        """
        Run validation for all banks in a phase.

        Args:
            phase: Phase number

        Returns:
            List of BankResult for each bank
        """
        results = []

        # Find phase directory
        phase_dir = None
        for d in self.outputs_dir.iterdir():
            if d.is_dir() and f"phase-{phase}" in d.name:
                phase_dir = d
                break

        if not phase_dir:
            logger.error(f"Phase {phase} directory not found")
            return results

        # Process each bank
        for bank_dir in sorted(phase_dir.iterdir()):
            if bank_dir.is_dir() and not bank_dir.name.startswith('.'):
                result = self.run_bank(bank_dir.name, phase)
                results.append(result)

        # Run cross-bank validation
        logger.info(f"\nRunning cross-bank validation for Phase {phase}...")
        cross_results = run_checks(phase_dir)

        if not cross_results['passed']:
            logger.warning("Cross-bank validation found issues:")
            for issue in cross_results.get('critical', []):
                logger.error(f"  CRITICAL: {issue['issue']}")

        return results


def main():
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="CDM Research Protocol - Research Runner"
    )
    parser.add_argument('--bank', help="Bank ID to process")
    parser.add_argument('--phase', type=int, help="Phase number")
    parser.add_argument('--all', action='store_true', help="Process all banks in phase")
    parser.add_argument('--validate-only', help="Validate existing outputs (path to bank dir)")
    parser.add_argument('--output', help="Output results to JSON file")

    args = parser.parse_args()
    runner = ResearchRunner()

    if args.validate_only:
        # Validate existing outputs
        bank_dir = Path(args.validate_only)
        results = runner.run_validation_pipeline(bank_dir)

        print(f"\n{'='*60}")
        print(f"VALIDATION RESULTS: {bank_dir.name}")
        print(f"{'='*60}")
        print(f"Valid: {results['valid']}")
        print(f"Classification: {results.get('classification')}")
        print(f"Confidence: {results.get('confidence')}%")

        # Show stage details
        print(f"\nStage Results:")
        for stage, data in results.get('stages', {}).items():
            if isinstance(data, dict):
                if 'error' in data:
                    print(f"  [{stage}] ERROR: {data['error']}")
                elif 'skipped' in data:
                    print(f"  [{stage}] SKIPPED: {data['skipped']}")
                else:
                    print(f"  [{stage}] OK")
            else:
                print(f"  [{stage}] {data}")

        if args.output:
            Path(args.output).write_text(json.dumps(results, indent=2, default=str), encoding='utf-8')
            print(f"\nResults saved to: {args.output}")

    elif args.bank and args.phase:
        # Single bank
        result = runner.run_bank(args.bank, args.phase)

        print(f"\n{'='*60}")
        print(f"BANK RESULT: {result.bank_id}")
        print(f"{'='*60}")
        print(f"Success: {result.success}")
        print(f"Classification: {result.classification}")
        print(f"Confidence: {result.confidence}%")
        print(f"Duration: {result.total_duration:.1f}s")

        if result.stages:
            print(f"\nStage Results:")
            for stage in result.stages:
                status = "OK" if stage.success else "FAIL"
                print(f"  [{status}] {stage.stage}")
                for err in stage.errors:
                    print(f"    ERROR: {err}")
                for warn in stage.warnings[:3]:
                    print(f"    WARN: {warn}")

        if args.output:
            Path(args.output).write_text(json.dumps(asdict(result), indent=2, default=str), encoding='utf-8')
            print(f"\nResults saved to: {args.output}")

    elif args.phase and args.all:
        # All banks in phase
        results = runner.run_phase(args.phase)

        print(f"\n{'='*60}")
        print(f"PHASE {args.phase} RESULTS")
        print(f"{'='*60}")

        passed = sum(1 for r in results if r.success)
        failed = len(results) - passed

        print(f"Total: {len(results)} banks | Passed: {passed} | Failed: {failed}")
        print()

        for r in results:
            status = "OK" if r.success else "FAIL"
            conf = f"{r.confidence}%" if r.confidence else "N/A"
            print(f"[{status:4}] {r.bank_id:25} {r.classification or 'UNKNOWN':15} {conf}")

        if args.output:
            Path(args.output).write_text(
                json.dumps([asdict(r) for r in results], indent=2, default=str),
                encoding='utf-8'
            )
            print(f"\nResults saved to: {args.output}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
