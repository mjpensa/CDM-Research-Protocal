"""
CDM Research Protocol - Output Validator

Validates that Claude Code produced correct outputs for each stage.
Runs automatically after each stage to ensure data quality before proceeding.

Usage:
    validator = OutputValidator()
    result = validator.validate(bank_id, phase, stage, bank_dir)
    if not result.valid:
        print(result.errors)
"""

import json
import re
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of output validation."""
    valid: bool
    stage: str
    files_found: List[str] = field(default_factory=list)
    files_missing: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    parsed_outputs: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "stage": self.stage,
            "files_found": self.files_found,
            "files_missing": self.files_missing,
            "errors": self.errors,
            "warnings": self.warnings
        }


class OutputValidator:
    """
    Validates outputs from each research stage.

    Checks:
    - Required files exist
    - JSON schemas are valid
    - Required sections present in markdown
    - Probability calculations are sane
    """

    # Expected outputs per stage
    STAGE_OUTPUTS = {
        "initialize": [],
        "pre_mortem": ["3-gates/pre-mortem.md"],
        "tier1_evidence": ["evidence.json", "1-evidence/tier1-evidence.md"],
        "bayesian_1": ["2-bayesian/post-tier1-update.md"],
        "gate_1": ["3-gates/gate-1.md"],
        "tier2_evidence": ["evidence.json", "1-evidence/tier2-evidence.md"],
        "bayesian_2": ["2-bayesian/post-tier2-update.md"],
        "gate_2": ["3-gates/gate-2.md"],
        "tier3_evidence": ["evidence.json", "1-evidence/tier3-evidence.md"],
        "bayesian_3": ["2-bayesian/post-tier3-update.md"],
        "gate_3": ["3-gates/gate-3.md"],
        "adversarial_challenge": [
            "4-adversarial/counter-case.md",
            "4-adversarial/disconfirming-searches.md",
            "4-adversarial/steelman.md",
            "4-adversarial/verdict.md"
        ],
        "final_classification": [],  # Classification set in state
        "synthesis": [
            "5-synthesis/confidence-calibration.md",
            "5-synthesis/assessment.md",
            "5-synthesis/framework-integration.md"
        ],
        "complete": []
    }

    # Required sections per markdown file
    REQUIRED_SECTIONS = {
        "pre-mortem.md": [
            "failure mode 1", "failure mode 2", "failure mode 3", "failure mode 4",
            "difficulty assessment"
        ],
        "gate-1.md": [
            "evidence delta", "probability update", "sufficiency"
        ],
        "gate-2.md": [
            "evidence delta", "probability update", "observable implications"
        ],
        "gate-3.md": [
            "evidence delta", "probability", "trajectory"
        ],
        "verdict.md": [
            "verdict", "confidence"
        ],
        "confidence-calibration.md": [
            "classification", "confidence", "calibration"
        ],
        "assessment.md": [
            "executive summary", "evidence summary", "classification"
        ]
    }

    def __init__(self, outputs_dir: Path = None):
        self.outputs_dir = outputs_dir or Path(__file__).parent.parent.parent / "outputs"

    def validate(self, bank_id: str, phase: int, stage: str, bank_dir: Path = None) -> ValidationResult:
        """
        Validate outputs for a stage.

        Args:
            bank_id: Bank identifier
            phase: Phase number
            stage: Stage name
            bank_dir: Bank output directory (optional, will be resolved)

        Returns:
            ValidationResult with validity status and any issues
        """
        if bank_dir is None:
            bank_dir = self._get_bank_dir(bank_id, phase)

        expected_outputs = self.STAGE_OUTPUTS.get(stage, [])

        if not expected_outputs:
            # No specific outputs required for this stage
            return ValidationResult(valid=True, stage=stage)

        errors = []
        warnings = []
        files_found = []
        files_missing = []
        parsed = {}

        for rel_path in expected_outputs:
            full_path = bank_dir / rel_path

            if not full_path.exists():
                files_missing.append(rel_path)
                errors.append(f"Missing output: {rel_path}")
                continue

            files_found.append(rel_path)

            # Validate content based on file type
            if rel_path.endswith('.json'):
                result = self._validate_json(full_path, stage)
            else:
                result = self._validate_markdown(full_path, stage)

            errors.extend(result.get("errors", []))
            warnings.extend(result.get("warnings", []))
            if result.get("parsed"):
                parsed[rel_path] = result["parsed"]

        return ValidationResult(
            valid=len(errors) == 0,
            stage=stage,
            files_found=files_found,
            files_missing=files_missing,
            errors=errors,
            warnings=warnings,
            parsed_outputs=parsed
        )

    def _get_bank_dir(self, bank_id: str, phase: int) -> Path:
        """Resolve bank directory path."""
        # Try with phase name suffix first
        phase_dirs = sorted(self.outputs_dir.glob(f"phase-{phase}-*"))
        if phase_dirs:
            return phase_dirs[0] / bank_id

        # Fall back to simple phase number
        return self.outputs_dir / f"phase-{phase}" / bank_id

    def _validate_json(self, path: Path, stage: str) -> Dict[str, Any]:
        """Validate JSON file content."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "evidence.json" in str(path):
                return self._validate_evidence_json(data)

            return {"parsed": data}

        except json.JSONDecodeError as e:
            return {"errors": [f"Invalid JSON in {path.name}: {e}"]}
        except Exception as e:
            return {"errors": [f"Error reading {path.name}: {e}"]}

    def _validate_evidence_json(self, data: dict) -> Dict[str, Any]:
        """Validate evidence.json schema."""
        errors = []
        warnings = []

        if "evidence_items" not in data:
            errors.append("Missing 'evidence_items' array in evidence.json")
            return {"errors": errors, "warnings": warnings, "parsed": data}

        items = data.get("evidence_items", [])

        if len(items) == 0:
            warnings.append("No evidence items found in evidence.json")

        # Validate each evidence item
        for i, item in enumerate(items):
            required_fields = ["id", "claim", "source_url", "tier", "claim_type"]
            for field in required_fields:
                if field not in item:
                    errors.append(f"Evidence item {i}: missing required field '{field}'")

            # Validate tier
            tier = item.get("tier")
            if tier is not None and tier not in [1, 2, 3, 4]:
                errors.append(f"Evidence item {i}: invalid tier '{tier}' (must be 1-4)")

            # Validate claim_type
            valid_claim_types = [
                "production_usage", "pilot_or_poc", "membership_or_participation",
                "open_source_contribution", "vendor_proxy_signal", "hiring_signal"
            ]
            claim_type = item.get("claim_type")
            if claim_type and claim_type not in valid_claim_types:
                warnings.append(f"Evidence item {i}: unrecognized claim_type '{claim_type}'")

            # Validate URL format
            url = item.get("source_url", "")
            if url and not url.startswith(("http://", "https://")):
                errors.append(f"Evidence item {i}: invalid URL format '{url}'")

        # Check for duplicate IDs
        ids = [item.get("id") for item in items if item.get("id")]
        if len(ids) != len(set(ids)):
            errors.append("Duplicate evidence IDs detected")

        return {"errors": errors, "warnings": warnings, "parsed": data}

    def _validate_markdown(self, path: Path, stage: str) -> Dict[str, Any]:
        """Validate markdown file content."""
        errors = []
        warnings = []

        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {"errors": [f"Error reading {path.name}: {e}"]}

        if not content.strip():
            errors.append(f"File {path.name} is empty")
            return {"errors": errors, "warnings": warnings}

        # Check for required sections
        filename = path.name
        required_sections = self.REQUIRED_SECTIONS.get(filename, [])

        content_lower = content.lower()
        for section in required_sections:
            if section.lower() not in content_lower:
                warnings.append(f"{filename}: missing expected section '{section}'")

        # Extract structured data from markdown
        parsed = self._extract_markdown_data(content, filename)

        return {"errors": errors, "warnings": warnings, "parsed": parsed}

    def _extract_markdown_data(self, content: str, filename: str) -> Dict[str, Any]:
        """Extract structured data from markdown content."""
        data = {"raw_content": content}

        # Extract probability values
        prob_patterns = [
            r'P\(Architect\)[:\s]+(\d+(?:\.\d+)?)\s*%',
            r'P\(A\)[:\s]+(\d+(?:\.\d+)?)\s*%',
            r'Probability[:\s]+(\d+(?:\.\d+)?)\s*%',
            r'(\d+(?:\.\d+)?)\s*%\s*P\(Architect\)',
        ]
        for pattern in prob_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    data["probability"] = float(match.group(1))
                    break
                except ValueError:
                    pass

        # Extract confidence
        conf_patterns = [
            r'[Cc]onfidence[:\s]+(\d+(?:\.\d+)?)\s*%',
            r'(\d+(?:\.\d+)?)\s*%\s*confidence',
        ]
        for pattern in conf_patterns:
            match = re.search(pattern, content)
            if match:
                try:
                    data["confidence"] = float(match.group(1))
                    break
                except ValueError:
                    pass

        # Extract classification
        class_patterns = [
            r'[Cc]lassification[:\s]+(ARCHITECT|PRAGMATIST|UNKNOWN)',
            r'(ARCHITECT|PRAGMATIST|UNKNOWN)\s*[-–]\s*(Native|Leader|Follower|Vendor|Integration)',
        ]
        for pattern in class_patterns:
            match = re.search(pattern, content)
            if match:
                data["classification"] = match.group(1)
                if len(match.groups()) > 1 and match.group(2):
                    data["variant"] = match.group(2)
                break

        # Extract verdict from adversarial
        if "verdict" in filename.lower():
            verdict_patterns = [
                r'[Vv]erdict[:\s]+(STRENGTHENED|WEAKENED|UNCHANGED|REVISED)',
                r'(STRENGTHENED|WEAKENED|UNCHANGED|REVISED)',
            ]
            for pattern in verdict_patterns:
                match = re.search(pattern, content)
                if match:
                    data["verdict"] = match.group(1)
                    break

        # Extract likelihood ratio
        lr_patterns = [
            r'[Cc]ombined\s+LR[:\s]+(\d+(?:\.\d+)?)',
            r'LR[:\s]+(\d+(?:\.\d+)?)',
        ]
        for pattern in lr_patterns:
            match = re.search(pattern, content)
            if match:
                try:
                    data["combined_lr"] = float(match.group(1))
                    break
                except ValueError:
                    pass

        return data

    def validate_probability_sanity(self, prob_architect: float) -> ValidationResult:
        """
        Validate probability is sane.

        Args:
            prob_architect: P(Architect) value (0.0 to 1.0 or 0 to 100)

        Returns:
            ValidationResult
        """
        errors = []
        warnings = []

        # Normalize to 0-1 if given as percentage
        if prob_architect > 1:
            prob_architect = prob_architect / 100

        # Check bounds
        if not 0.0 <= prob_architect <= 1.0:
            errors.append(f"Invalid probability: {prob_architect} (must be 0-100%)")

        # Check for extreme values
        if prob_architect > 0.95:
            warnings.append(f"Very high P(Architect): {prob_architect:.1%}")
        elif prob_architect < 0.05:
            warnings.append(f"Very low P(Architect): {prob_architect:.1%}")

        return ValidationResult(
            valid=len(errors) == 0,
            stage="probability_check",
            errors=errors,
            warnings=warnings
        )

    def count_evidence_by_tier(self, bank_dir: Path) -> Dict[str, int]:
        """
        Count evidence items by tier from evidence.json.

        Returns:
            Dict with tier counts: {"tier1": N, "tier2": N, "tier3": N, "null": N}
        """
        counts = {"tier1": 0, "tier2": 0, "tier3": 0, "null": 0}

        evidence_path = bank_dir / "evidence.json"
        if not evidence_path.exists():
            return counts

        try:
            with open(evidence_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for item in data.get("evidence_items", []):
                tier = item.get("tier")
                if tier == 1:
                    counts["tier1"] += 1
                elif tier == 2:
                    counts["tier2"] += 1
                elif tier == 3:
                    counts["tier3"] += 1

            # Count null results
            null_path = bank_dir / "1-evidence" / "null-results.md"
            if null_path.exists():
                content = null_path.read_text(encoding='utf-8')
                # Count "Null Result" or "No evidence found" patterns
                counts["null"] = len(re.findall(
                    r'(null result|no evidence found|no results)',
                    content, re.IGNORECASE
                ))

        except Exception as e:
            logger.warning(f"Error counting evidence: {e}")

        return counts

    def get_highest_tier(self, bank_dir: Path) -> int:
        """
        Get the highest evidence tier present.

        Returns:
            1, 2, 3, or 4 (4 means no direct evidence)
        """
        counts = self.count_evidence_by_tier(bank_dir)

        if counts["tier1"] > 0:
            return 1
        elif counts["tier2"] > 0:
            return 2
        elif counts["tier3"] > 0:
            return 3
        else:
            return 4

    def validate_all_stages(self, bank_id: str, phase: int, bank_dir: Path = None) -> Dict[str, ValidationResult]:
        """
        Validate all stages for a bank.

        Returns:
            Dict mapping stage name to ValidationResult
        """
        if bank_dir is None:
            bank_dir = self._get_bank_dir(bank_id, phase)

        results = {}
        for stage in self.STAGE_OUTPUTS.keys():
            results[stage] = self.validate(bank_id, phase, stage, bank_dir)

        return results
