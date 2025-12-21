"""
Prompt Version Validator - Validates prompt versions, dependencies, and compatibility.

Ensures all prompts have:
- Valid YAML frontmatter with version information
- Matching versions between file and registry
- All declared dependencies exist
- Compatible versions across the system

Usage:
    python prompt_version_validator.py --check          # Validate all prompts
    python prompt_version_validator.py --changelog X    # Show changelog for prompt
    python prompt_version_validator.py --compatibility  # Check compatibility matrix
"""

import json
import re
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class VersionInfo:
    """Parsed version information."""
    major: int
    minor: int
    date: str  # YYYYMMDD format

    @classmethod
    def parse(cls, version_str: str) -> 'VersionInfo':
        """
        Parse version string in X.Y-YYYYMMDD format.

        Args:
            version_str: Version string like "2.0-20251221"

        Returns:
            VersionInfo object
        """
        # Handle different formats
        if '-' in version_str:
            # Hybrid format: X.Y-YYYYMMDD
            parts = version_str.split('-')
            version_part = parts[0]
            date_part = parts[1] if len(parts) > 1 else ''
        else:
            # Simple format: X.Y.Z or X.Y
            version_part = version_str
            date_part = ''

        version_nums = version_part.split('.')
        return cls(
            major=int(version_nums[0]) if version_nums else 0,
            minor=int(version_nums[1]) if len(version_nums) > 1 else 0,
            date=date_part
        )

    def __str__(self) -> str:
        if self.date:
            return f"{self.major}.{self.minor}-{self.date}"
        return f"{self.major}.{self.minor}"

    def __ge__(self, other: 'VersionInfo') -> bool:
        if self.major != other.major:
            return self.major >= other.major
        if self.minor != other.minor:
            return self.minor >= other.minor
        return self.date >= other.date

    def __gt__(self, other: 'VersionInfo') -> bool:
        if self.major != other.major:
            return self.major > other.major
        if self.minor != other.minor:
            return self.minor > other.minor
        return self.date > other.date


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    prompt_id: str
    issue_type: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    details: Optional[str] = None


class PromptVersionValidator:
    """
    Validates prompt versions and dependencies.

    Checks:
    - Frontmatter presence and validity
    - Version match between file and registry
    - Dependency existence
    - Compatibility matrix compliance
    """

    FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

    def __init__(self, config_dir: Path = None):
        """
        Initialize the validator.

        Args:
            config_dir: Path to config/ directory
        """
        if config_dir is None:
            script_dir = Path(__file__).parent
            config_dir = script_dir.parent / "config"

        self.config_dir = Path(config_dir)
        self.prompts_dir = self.config_dir / "agent-prompts"
        self.registry = self._load_registry()

    def _load_registry(self) -> dict:
        """Load the prompt registry."""
        registry_path = self.config_dir / "prompt-registry.json"
        if registry_path.exists():
            with open(registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        logger.warning(f"Registry not found: {registry_path}")
        return {"prompts": {}, "config_files": {}}

    def _load_json(self, path: Path) -> dict:
        """Load a JSON file."""
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def extract_frontmatter(self, prompt_path: Path) -> Optional[dict]:
        """
        Extract YAML frontmatter from a prompt file.

        Args:
            prompt_path: Path to the prompt file

        Returns:
            Parsed frontmatter dict or None
        """
        if not YAML_AVAILABLE:
            logger.warning("PyYAML not available")
            return None

        content = prompt_path.read_text(encoding='utf-8')
        match = self.FRONTMATTER_PATTERN.match(content)

        if not match:
            return None

        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse frontmatter in {prompt_path}: {e}")
            return None

    def validate_all(self) -> List[ValidationIssue]:
        """
        Validate all prompts against the registry.

        Returns:
            List of ValidationIssue objects
        """
        issues = []

        # Check each registered prompt
        for prompt_id, info in self.registry.get("prompts", {}).items():
            prompt_issues = self.validate_prompt(prompt_id, info)
            issues.extend(prompt_issues)

        # Check for unregistered prompt files
        for prompt_file in self.prompts_dir.glob("*.md"):
            prompt_id = prompt_file.stem
            if prompt_id not in self.registry.get("prompts", {}):
                issues.append(ValidationIssue(
                    prompt_id=prompt_id,
                    issue_type='unregistered',
                    severity='warning',
                    message=f"Prompt file not in registry: {prompt_file.name}"
                ))

        # Check config file versions
        config_issues = self._validate_config_files()
        issues.extend(config_issues)

        return issues

    def validate_prompt(self, prompt_id: str, info: dict) -> List[ValidationIssue]:
        """
        Validate a single prompt.

        Args:
            prompt_id: Prompt identifier
            info: Registry info for the prompt

        Returns:
            List of ValidationIssue objects
        """
        issues = []
        prompt_path = self.config_dir.parent / info["path"]

        # Check file exists
        if not prompt_path.exists():
            issues.append(ValidationIssue(
                prompt_id=prompt_id,
                issue_type='missing_file',
                severity='error',
                message=f"Prompt file not found: {info['path']}"
            ))
            return issues

        # Check frontmatter
        frontmatter = self.extract_frontmatter(prompt_path)
        if not frontmatter:
            issues.append(ValidationIssue(
                prompt_id=prompt_id,
                issue_type='missing_frontmatter',
                severity='warning',
                message="No YAML frontmatter found",
                details="Add frontmatter with version, prompt_id, dependencies"
            ))
        else:
            # Version mismatch check
            file_version = frontmatter.get("version", "")
            registry_version = info.get("current_version", "")

            if file_version and registry_version and file_version != registry_version:
                issues.append(ValidationIssue(
                    prompt_id=prompt_id,
                    issue_type='version_mismatch',
                    severity='error',
                    message=f"Version mismatch: file={file_version}, registry={registry_version}"
                ))

            # Prompt ID mismatch
            file_prompt_id = frontmatter.get("prompt_id", "")
            if file_prompt_id and file_prompt_id != prompt_id:
                issues.append(ValidationIssue(
                    prompt_id=prompt_id,
                    issue_type='id_mismatch',
                    severity='warning',
                    message=f"Prompt ID mismatch: file={file_prompt_id}, registry={prompt_id}"
                ))

        # Check dependencies
        for dep in info.get("dependencies", []):
            if not self._check_dependency(dep):
                issues.append(ValidationIssue(
                    prompt_id=prompt_id,
                    issue_type='missing_dependency',
                    severity='error',
                    message=f"Missing dependency: {dep}"
                ))

        # Check for section tags if sections are declared
        declared_sections = info.get("sections", [])
        if declared_sections:
            content = prompt_path.read_text(encoding='utf-8')
            missing_sections = self._check_section_tags(content, declared_sections)
            for section in missing_sections:
                issues.append(ValidationIssue(
                    prompt_id=prompt_id,
                    issue_type='missing_section',
                    severity='warning',
                    message=f"Declared section not found: {section}",
                    details="Add <!-- @section:name --> ... <!-- @endsection --> tags"
                ))

        return issues

    def _check_dependency(self, dep: str) -> bool:
        """Check if a dependency exists."""
        # Check as file path relative to config_dir
        dep_path = self.config_dir / dep
        if dep_path.exists():
            return True

        # Check in registry config_files
        if dep in self.registry.get("config_files", {}):
            config_info = self.registry["config_files"][dep]
            config_path = self.config_dir.parent / config_info.get("path", dep)
            return config_path.exists()

        # Check as reference file
        ref_path = self.prompts_dir / "references" / dep
        if ref_path.exists():
            return True

        return False

    def _check_section_tags(self, content: str, sections: List[str]) -> List[str]:
        """Check which declared sections are missing tags."""
        missing = []
        for section in sections:
            pattern = rf'<!-- @section:{section} -->'
            if not re.search(pattern, content):
                missing.append(section)
        return missing

    def _validate_config_files(self) -> List[ValidationIssue]:
        """Validate config file existence and versions."""
        issues = []

        for config_id, info in self.registry.get("config_files", {}).items():
            config_path = self.config_dir.parent / info["path"]

            if not config_path.exists():
                # Check if it's marked as planned
                if info.get("status") == "planned":
                    issues.append(ValidationIssue(
                        prompt_id=config_id,
                        issue_type='planned_file',
                        severity='info',
                        message=f"Planned config file not yet created: {info['path']}"
                    ))
                else:
                    issues.append(ValidationIssue(
                        prompt_id=config_id,
                        issue_type='missing_config',
                        severity='error',
                        message=f"Config file not found: {info['path']}"
                    ))

        return issues

    def check_compatibility(self, target_version: str = None) -> Tuple[bool, List[str]]:
        """
        Check system-wide version compatibility.

        Args:
            target_version: Target version to check against (defaults to latest)

        Returns:
            Tuple of (is_compatible, list of issues)
        """
        issues = []

        if target_version is None:
            # Use latest from compatibility matrix
            matrix = self.registry.get("compatibility_matrix", {})
            if matrix:
                target_version = max(matrix.keys())
            else:
                return True, []

        compat = self.registry.get("compatibility_matrix", {}).get(target_version, {})

        # Check orchestrator version
        if "minimum_orchestrator" in compat:
            orch_info = self.registry.get("prompts", {}).get("orchestrator", {})
            current = VersionInfo.parse(orch_info.get("current_version", "0.0-00000000"))
            required = VersionInfo.parse(compat["minimum_orchestrator"])

            if not current >= required:
                issues.append(
                    f"Orchestrator version {current} < required {required}"
                )

        # Check for breaking changes
        if compat.get("breaking_changes"):
            migration_notes = compat.get("migration_notes", [])
            if migration_notes:
                issues.append("Breaking changes detected. Migration notes:")
                issues.extend([f"  - {note}" for note in migration_notes])

        return len([i for i in issues if not i.startswith("  ")]) == 0, issues

    def generate_changelog(self, prompt_id: str, from_version: str = None) -> str:
        """
        Generate changelog for a prompt.

        Args:
            prompt_id: Prompt identifier
            from_version: Show changes since this version (optional)

        Returns:
            Formatted changelog string
        """
        info = self.registry.get("prompts", {}).get(prompt_id, {})
        changelog = info.get("changelog", [])

        if not changelog:
            return f"No changelog available for {prompt_id}"

        if from_version:
            from_v = VersionInfo.parse(from_version)
            changelog = [
                c for c in changelog
                if VersionInfo.parse(c["version"]) > from_v
            ]

        if not changelog:
            return f"No changes since version {from_version}"

        lines = [
            f"# Changelog: {prompt_id}",
            f"Current version: {info.get('current_version', 'unknown')}",
            ""
        ]

        for entry in changelog:
            lines.append(f"## [{entry['version']}] - {entry['date']}")
            lines.append(f"**Type**: {entry.get('type', 'unknown')}")
            lines.append("")

            for change in entry.get("changes", []):
                lines.append(f"- {change}")

            if "migration" in entry:
                lines.append("")
                lines.append(f"**Migration**: {entry['migration']}")

            lines.append("")

        return "\n".join(lines)

    def generate_report(self, issues: List[ValidationIssue] = None) -> str:
        """
        Generate a validation report.

        Args:
            issues: List of issues (runs validation if None)

        Returns:
            Formatted report string
        """
        if issues is None:
            issues = self.validate_all()

        if not issues:
            return "✓ All prompts validated successfully"

        lines = [
            "Prompt Version Validation Report",
            "=" * 50,
            f"Registry: {self.config_dir / 'prompt-registry.json'}",
            f"Issues: {len(issues)}",
            ""
        ]

        # Group by severity
        errors = [i for i in issues if i.severity == 'error']
        warnings = [i for i in issues if i.severity == 'warning']
        infos = [i for i in issues if i.severity == 'info']

        if errors:
            lines.append("ERRORS:")
            for issue in errors:
                lines.append(f"  [{issue.prompt_id}] {issue.issue_type}")
                lines.append(f"    {issue.message}")
                if issue.details:
                    lines.append(f"    → {issue.details}")
            lines.append("")

        if warnings:
            lines.append("WARNINGS:")
            for issue in warnings:
                lines.append(f"  [{issue.prompt_id}] {issue.issue_type}")
                lines.append(f"    {issue.message}")
            lines.append("")

        if infos:
            lines.append("INFO:")
            for issue in infos:
                lines.append(f"  [{issue.prompt_id}] {issue.message}")
            lines.append("")

        lines.append("=" * 50)
        lines.append(f"Total: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")

        return "\n".join(lines)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate prompt versions and dependencies"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate all prompts (default action)"
    )
    parser.add_argument(
        "--changelog",
        type=str,
        help="Show changelog for specified prompt"
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Show changelog since version (use with --changelog)"
    )
    parser.add_argument(
        "--compatibility",
        action="store_true",
        help="Check version compatibility"
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        help="Path to config directory"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    validator = PromptVersionValidator(args.config_dir)

    if args.changelog:
        print(validator.generate_changelog(args.changelog, args.since))
        return 0

    if args.compatibility:
        is_compat, issues = validator.check_compatibility()
        if is_compat:
            print("✓ All versions are compatible")
        else:
            print("⚠ Compatibility issues detected:")
            for issue in issues:
                print(f"  {issue}")
        return 0 if is_compat else 1

    # Default: run validation
    issues = validator.validate_all()

    if args.json:
        output = [
            {
                "prompt_id": i.prompt_id,
                "type": i.issue_type,
                "severity": i.severity,
                "message": i.message,
                "details": i.details
            }
            for i in issues
        ]
        print(json.dumps(output, indent=2))
    else:
        print(validator.generate_report(issues))

    # Return appropriate exit code
    errors = [i for i in issues if i.severity == 'error']
    return 1 if errors else 0


if __name__ == "__main__":
    exit(main())
