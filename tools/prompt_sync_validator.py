"""
Prompt Sync Validator - Detects prompt content duplication in prompt_assembler.py.

This tool ensures that prompt_assembler.py doesn't contain inline prompt content
that should live in the static prompt files. It prevents "prompt drift" where
the assembler and static prompts diverge.

Usage:
    python prompt_sync_validator.py                    # Check default path
    python prompt_sync_validator.py --assembler path   # Check specific file
    python prompt_sync_validator.py --fix              # Show suggested fixes
"""

import re
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


@dataclass
class DriftViolation:
    """Represents a detected prompt drift violation."""
    line_number: int
    violation_type: str
    content_preview: str
    severity: str  # 'error', 'warning', 'info'
    suggestion: str


class PromptSyncValidator:
    """
    Detects prompt content duplication in the assembler.

    Violations include:
    - Inline role definitions (should be in static prompts)
    - Hardcoded section headers (should be loaded via section tags)
    - Duplicate instruction text (should use get_section())
    - Inline search templates (should be in search-templates.json)
    """

    # Patterns that indicate inline prompt content (violations)
    VIOLATION_PATTERNS = [
        # Role definitions in f-strings or docstrings
        (
            r'(f?["\']{{3}}).*?(You are the|Your role is|## Role).*?\1',
            'inline_role',
            'error',
            'Role definitions should be loaded via get_section("agent", "role")'
        ),
        # Section headers suggesting inline content
        (
            r'["\']## (Evidence|Bayesian|Gate|Adversarial|Synthesis|Reasoning)',
            'inline_section_header',
            'warning',
            'Section headers suggest inline content - use get_section()'
        ),
        # Inline search query templates
        (
            r'site:(isda\.org|finos\.org|risk\.net|github\.com/finos)',
            'inline_search_template',
            'warning',
            'Search templates should be loaded from search-templates.json'
        ),
        # Inline LR values
        (
            r'LR\s*[=:]\s*\d+\.\d+',
            'inline_lr_value',
            'info',
            'LR values should reference config/bayesian-lr-tables.json'
        ),
        # Inline threshold values (that should come from config)
        (
            r'(threshold|cap|maximum)\s*[=:]\s*(80|75|50|35|95)%?',
            'inline_threshold',
            'warning',
            'Thresholds should be loaded from config/decision-thresholds.json'
        ),
        # Long instruction strings (>300 chars in f-strings)
        (
            r"f['\"]{{3}}[^'\"]{300,}['\"]{{3}}",
            'long_inline_content',
            'warning',
            'Long inline content should be externalized to static prompts'
        ),
    ]

    # Patterns that are ALLOWED (false positive filters)
    ALLOWED_PATTERNS = [
        r'# .*(comment|docstring|documentation)',  # Comments about the code
        r'logger\.(info|debug|warning|error)',     # Logging statements
        r'raise \w+Error',                          # Exception messages
        r'description\s*[=:]',                      # Description fields
    ]

    def __init__(self, assembler_path: Path = None):
        """
        Initialize the validator.

        Args:
            assembler_path: Path to prompt_assembler.py
        """
        if assembler_path is None:
            # Default path
            script_dir = Path(__file__).parent
            assembler_path = script_dir / "orchestrator" / "prompt_assembler.py"

        self.assembler_path = Path(assembler_path)

    def validate(self) -> List[DriftViolation]:
        """
        Validate the assembler for prompt drift.

        Returns:
            List of DriftViolation objects
        """
        if not self.assembler_path.exists():
            logger.error(f"Assembler not found: {self.assembler_path}")
            return [DriftViolation(
                line_number=0,
                violation_type='file_not_found',
                content_preview=str(self.assembler_path),
                severity='error',
                suggestion='Ensure prompt_assembler.py exists'
            )]

        content = self.assembler_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        violations = []

        for pattern, vtype, severity, suggestion in self.VIOLATION_PATTERNS:
            for match in re.finditer(pattern, content, re.DOTALL | re.IGNORECASE):
                # Find line number
                line_num = content[:match.start()].count('\n') + 1

                # Check if this is an allowed pattern (false positive)
                context_start = max(0, match.start() - 100)
                context = content[context_start:match.end() + 100]

                if any(re.search(ap, context, re.IGNORECASE) for ap in self.ALLOWED_PATTERNS):
                    continue

                # Get content preview
                matched_text = match.group(0)
                preview = matched_text[:100] + ('...' if len(matched_text) > 100 else '')

                # Check for significant content (not just short strings)
                if vtype in ('inline_role', 'long_inline_content') and len(matched_text) < 200:
                    continue

                violations.append(DriftViolation(
                    line_number=line_num,
                    violation_type=vtype,
                    content_preview=preview.replace('\n', '\\n'),
                    severity=severity,
                    suggestion=suggestion
                ))

        return violations

    def validate_no_hardcoded_agents(self) -> List[DriftViolation]:
        """
        Check for hardcoded agent prompt content.

        Returns:
            List of violations for hardcoded agent prompts
        """
        content = self.assembler_path.read_text(encoding='utf-8')
        violations = []

        # Agent names that should use section loading
        agents = [
            'evidence-gatherer', 'bayesian-analyst', 'reasoning-gate',
            'adversarial-challenger', 'synthesis', 'orchestrator', 'qa-validator'
        ]

        # Check for inline content that matches agent prompt sections
        agent_content_patterns = [
            (r'Evidence Gatherer.*Execute web searches', 'evidence-gatherer'),
            (r'Bayesian Analyst.*probability updates?', 'bayesian-analyst'),
            (r'Reasoning Gate.*quality checkpoint', 'reasoning-gate'),
            (r'Adversarial Challenger.*counter-argument', 'adversarial-challenger'),
            (r'Synthesis Agent.*comprehensive assessment', 'synthesis'),
            (r'Orchestrator Agent.*workflow', 'orchestrator'),
            (r'QA Validator.*consistency', 'qa-validator'),
        ]

        for pattern, agent in agent_content_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE | re.DOTALL))
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1

                # Check context to see if it's in a docstring or comment
                line_start = content.rfind('\n', 0, match.start()) + 1
                line = content[line_start:match.start() + 100]

                if '"""' in line or "'''" in line or line.strip().startswith('#'):
                    # This is legitimate documentation
                    continue

                violations.append(DriftViolation(
                    line_number=line_num,
                    violation_type='hardcoded_agent_content',
                    content_preview=match.group(0)[:80] + '...',
                    severity='warning',
                    suggestion=f'Use section_loader.get_section("{agent}", "role") instead'
                ))

        return violations

    def generate_report(self, violations: List[DriftViolation] = None) -> str:
        """
        Generate a human-readable validation report.

        Args:
            violations: List of violations (if None, runs validation)

        Returns:
            Formatted report string
        """
        if violations is None:
            violations = self.validate()
            violations.extend(self.validate_no_hardcoded_agents())

        if not violations:
            return "✓ No prompt drift detected in prompt_assembler.py"

        lines = [
            "⚠ Prompt Drift Detection Report",
            "=" * 50,
            f"File: {self.assembler_path}",
            f"Violations: {len(violations)}",
            "",
        ]

        # Group by severity
        errors = [v for v in violations if v.severity == 'error']
        warnings = [v for v in violations if v.severity == 'warning']
        infos = [v for v in violations if v.severity == 'info']

        if errors:
            lines.append("ERRORS (must fix):")
            for v in errors:
                lines.append(f"  Line {v.line_number}: [{v.violation_type}]")
                lines.append(f"    {v.content_preview}")
                lines.append(f"    → {v.suggestion}")
                lines.append("")

        if warnings:
            lines.append("WARNINGS (should fix):")
            for v in warnings:
                lines.append(f"  Line {v.line_number}: [{v.violation_type}]")
                lines.append(f"    {v.content_preview}")
                lines.append(f"    → {v.suggestion}")
                lines.append("")

        if infos:
            lines.append("INFO (consider fixing):")
            for v in infos:
                lines.append(f"  Line {v.line_number}: [{v.violation_type}]")
                lines.append(f"    → {v.suggestion}")
                lines.append("")

        lines.append("=" * 50)
        lines.append(f"Total: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")

        return "\n".join(lines)

    def get_exit_code(self, violations: List[DriftViolation] = None) -> int:
        """
        Get appropriate exit code for CI/pre-commit.

        Args:
            violations: List of violations

        Returns:
            0 if no errors/warnings, 1 if errors, 2 if warnings only
        """
        if violations is None:
            violations = self.validate()
            violations.extend(self.validate_no_hardcoded_agents())

        errors = [v for v in violations if v.severity == 'error']
        warnings = [v for v in violations if v.severity == 'warning']

        if errors:
            return 1
        if warnings:
            return 2
        return 0


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate prompt_assembler.py for prompt drift"
    )
    parser.add_argument(
        "--assembler",
        type=Path,
        help="Path to prompt_assembler.py"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run validation (default action)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )

    args = parser.parse_args()

    validator = PromptSyncValidator(args.assembler)
    violations = validator.validate()
    violations.extend(validator.validate_no_hardcoded_agents())

    if args.json:
        import json
        output = [
            {
                "line": v.line_number,
                "type": v.violation_type,
                "severity": v.severity,
                "preview": v.content_preview,
                "suggestion": v.suggestion
            }
            for v in violations
        ]
        print(json.dumps(output, indent=2))
    else:
        print(validator.generate_report(violations))

    if args.strict:
        # Treat warnings as errors
        exit_code = 1 if violations else 0
    else:
        exit_code = validator.get_exit_code(violations)

    return exit_code


if __name__ == "__main__":
    exit(main())
