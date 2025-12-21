"""
CDM Research Protocol - Protocol Compliance Checker v1.0

Verifies that agents followed required methodological steps:
- Disconfirmation testing
- Observable implications
- Steelman arguments
- Gate sections

Usage:
    from protocol_compliance import ProtocolComplianceChecker

    checker = ProtocolComplianceChecker()
    violations = checker.verify_adversarial(bank_dir)
"""

import re
from pathlib import Path
from typing import Optional, List, Dict, Any

# Project imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config_loader import load_validation_rules, get_protocol_compliance_rules
    from orchestrator.violation_queue import ProtocolViolation
except ImportError:
    from tools.config_loader import load_validation_rules, get_protocol_compliance_rules
    from tools.orchestrator.violation_queue import ProtocolViolation


class ProtocolComplianceChecker:
    """
    Verifies compliance with CDM Research Protocol methodology.

    Checks that agents actually executed required steps rather than
    just claiming to have done so.
    """

    def __init__(self):
        """Initialize the compliance checker."""
        self.rules = get_protocol_compliance_rules()
        self.full_rules = load_validation_rules()

    # --- DISCONFIRMATION TESTING ---

    def verify_disconfirmation_testing(
        self,
        bank_dir: Path
    ) -> List[ProtocolViolation]:
        """
        Verify agents actually executed disconfirming searches.

        Requirements per adversarial-challenger.md:
        - 3 disconfirming searches required for all banks
        - Each search must have: query, target, results, impact

        Args:
            bank_dir: Path to bank output directory

        Returns:
            List of violations found
        """
        violations = []
        stage = "adversarial_challenge"

        disconf_path = bank_dir / "4-adversarial" / "disconfirming-searches.md"
        if not disconf_path.exists():
            violations.append(ProtocolViolation(
                violation_type="MISSING_DISCONFIRMATION_FILE",
                severity="ERROR",
                description="Disconfirming searches file not found",
                stage=stage,
                remediation="Execute disconfirming searches per adversarial protocol"
            ))
            return violations

        content = disconf_path.read_text(encoding='utf-8')
        min_searches = self.rules.get("min_disconfirming_searches", 3)

        # Find search blocks
        search_patterns = [
            r'###?\s+(?:Disconfirming\s+)?Search\s+(\d+)',
            r'##?\s+Search\s+(\d+)',
            r'\*\*Search\s+(\d+)\*\*'
        ]

        searches_found = set()
        for pattern in search_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            searches_found.update(matches)

        if len(searches_found) < min_searches:
            violations.append(ProtocolViolation(
                violation_type="MISSING_DISCONFIRMATION_SEARCHES",
                severity="ERROR",
                description=f"Only {len(searches_found)}/{min_searches} required disconfirming searches found",
                stage=stage,
                expected_value=str(min_searches),
                actual_value=str(len(searches_found)),
                remediation="Execute additional disconfirming searches per adversarial protocol"
            ))

        # Verify each search has required components
        required_components = ["Query", "Result", "Finding", "Conclusion"]

        for i in range(1, min(4, len(searches_found) + 1)):
            search_block = self._extract_search_block(content, i)
            if search_block:
                missing_components = []
                for component in required_components:
                    if not re.search(rf'\*?\*?{component}\*?\*?[:\s]', search_block, re.IGNORECASE):
                        # Also check for common variations
                        variations = {
                            "Query": ["search query", "searched for", "query:"],
                            "Result": ["results:", "found:", "returned:"],
                            "Finding": ["finding:", "conclusion:", "impact:"],
                            "Conclusion": ["disconfirming value", "conclusion:", "impact:"]
                        }
                        found_variation = False
                        for var in variations.get(component, []):
                            if var.lower() in search_block.lower():
                                found_variation = True
                                break
                        if not found_variation:
                            missing_components.append(component)

                if missing_components:
                    violations.append(ProtocolViolation(
                        violation_type="INCOMPLETE_DISCONFIRMATION_SEARCH",
                        severity="WARNING",
                        description=f"Search {i} missing components: {', '.join(missing_components)}",
                        stage=stage,
                        remediation=f"Add {', '.join(missing_components)} documentation to search {i}"
                    ))

        return violations

    def _extract_search_block(self, content: str, search_num: int) -> Optional[str]:
        """Extract content for a specific search number."""
        patterns = [
            rf'###?\s+(?:Disconfirming\s+)?Search\s+{search_num}(.*?)(?=###?\s+(?:Disconfirming\s+)?Search\s+\d+|$)',
            rf'\*\*Search\s+{search_num}\*\*(.*?)(?=\*\*Search\s+\d+\*\*|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1)

        return None

    # --- OBSERVABLE IMPLICATIONS ---

    def verify_observable_implications(
        self,
        bank_dir: Path,
        leading_hypothesis: str = "ARCHITECT"
    ) -> List[ProtocolViolation]:
        """
        Verify observable implications testing at Gate 2.

        Per reasoning-gate.md Gate 2 requirements:
        - >=3/6 implications tested for leading hypothesis
        - Both hypotheses should be tested

        Args:
            bank_dir: Path to bank output directory
            leading_hypothesis: Current leading hypothesis (ARCHITECT or PRAGMATIST)

        Returns:
            List of violations found
        """
        violations = []
        stage = "gate_2"

        gate2_path = bank_dir / "3-gates" / "gate-2.md"
        if not gate2_path.exists():
            violations.append(ProtocolViolation(
                violation_type="MISSING_GATE_FILE",
                severity="WARNING",
                description="Gate 2 file not found - cannot verify observable implications",
                stage=stage
            ))
            return violations

        content = gate2_path.read_text(encoding='utf-8')
        obs_impl = self.full_rules.get("observable_implications", {})
        min_tested = obs_impl.get("minimum_tested_per_hypothesis", 3)

        # Architect implications
        architect_implications = obs_impl.get("architect_implications", {
            "A1": "Official Participation",
            "A2": "Named Individual Contributors",
            "A3": "Public Announcements",
            "A4": "Technical Investment",
            "A5": "Industry Recognition",
            "A6": "Ecosystem Relationships"
        })

        # Pragmatist implications
        pragmatist_implications = obs_impl.get("pragmatist_implications", {
            "P1": "Vendor Dependency",
            "P2": "Absence from CDM Forums",
            "P3": "Traditional Technology Focus",
            "P4": "Regulatory Compliance Focus",
            "P5": "Utility/Infrastructure Reliance",
            "P6": "Peer Differentiation"
        })

        # Count tested implications
        architect_tested = 0
        pragmatist_tested = 0

        for key, desc in architect_implications.items():
            # Look for the implication ID or description followed by a result indicator
            pattern = rf'{key}[:\s].*?(?:\[|\(|✓|✗|confirmed|refuted|tested|found|not found)'
            if re.search(pattern, content, re.IGNORECASE):
                architect_tested += 1
            elif desc.lower() in content.lower():
                # Check if there's a result near the description
                idx = content.lower().find(desc.lower())
                nearby = content[max(0, idx-50):min(len(content), idx+200)]
                if any(indicator in nearby.lower() for indicator in ['confirmed', 'refuted', 'found', 'tested', '✓', '✗', '[x]', '[ ]']):
                    architect_tested += 1

        for key, desc in pragmatist_implications.items():
            pattern = rf'{key}[:\s].*?(?:\[|\(|✓|✗|confirmed|refuted|tested|found|not found)'
            if re.search(pattern, content, re.IGNORECASE):
                pragmatist_tested += 1
            elif desc.lower() in content.lower():
                idx = content.lower().find(desc.lower())
                nearby = content[max(0, idx-50):min(len(content), idx+200)]
                if any(indicator in nearby.lower() for indicator in ['confirmed', 'refuted', 'found', 'tested', '✓', '✗', '[x]', '[ ]']):
                    pragmatist_tested += 1

        # Check leading hypothesis
        if leading_hypothesis == "ARCHITECT":
            if architect_tested < min_tested:
                violations.append(ProtocolViolation(
                    violation_type="INSUFFICIENT_OBSERVABLE_IMPLICATIONS",
                    severity="ERROR",
                    description=f"Only {architect_tested}/6 ARCHITECT implications tested (minimum {min_tested} required)",
                    stage=stage,
                    expected_value=f">={min_tested}",
                    actual_value=str(architect_tested),
                    remediation="Test additional ARCHITECT observable implications per templates/observable-implications.md"
                ))
        else:
            if pragmatist_tested < min_tested:
                violations.append(ProtocolViolation(
                    violation_type="INSUFFICIENT_OBSERVABLE_IMPLICATIONS",
                    severity="ERROR",
                    description=f"Only {pragmatist_tested}/6 PRAGMATIST implications tested (minimum {min_tested} required)",
                    stage=stage,
                    expected_value=f">={min_tested}",
                    actual_value=str(pragmatist_tested),
                    remediation="Test additional PRAGMATIST observable implications"
                ))

        # Check alternative hypothesis
        alt_tested = pragmatist_tested if leading_hypothesis == "ARCHITECT" else architect_tested
        if alt_tested == 0:
            alt_hyp = "PRAGMATIST" if leading_hypothesis == "ARCHITECT" else "ARCHITECT"
            violations.append(ProtocolViolation(
                violation_type="ALTERNATIVE_HYPOTHESIS_NOT_TESTED",
                severity="WARNING",
                description=f"Alternative hypothesis ({alt_hyp}) implications not tested",
                stage=stage,
                remediation="Test implications for BOTH hypotheses per reasoning-gate.md Gate 2 requirements"
            ))

        return violations

    # --- STEELMAN VERIFICATION ---

    def verify_steelman_quality(
        self,
        bank_dir: Path
    ) -> List[ProtocolViolation]:
        """
        Verify steelman argument meets quality requirements.

        Per adversarial-challenger.md: "2-3 paragraphs, genuinely persuasive"

        Args:
            bank_dir: Path to bank output directory

        Returns:
            List of violations found
        """
        violations = []
        stage = "adversarial_challenge"

        steelman_path = bank_dir / "4-adversarial" / "steelman.md"
        if not steelman_path.exists():
            violations.append(ProtocolViolation(
                violation_type="MISSING_STEELMAN_FILE",
                severity="ERROR",
                description="Steelman file not found",
                stage=stage,
                remediation="Create steelman.md with strongest argument for alternative hypothesis"
            ))
            return violations

        content = steelman_path.read_text(encoding='utf-8')
        min_words = self.rules.get("min_steelman_words", 150)

        # Check minimum length
        word_count = len(content.split())
        if word_count < min_words:
            violations.append(ProtocolViolation(
                violation_type="INSUFFICIENT_STEELMAN_DEPTH",
                severity="WARNING",
                description=f"Steelman argument appears superficial ({word_count} words)",
                stage=stage,
                expected_value=f">={min_words} words",
                actual_value=f"{word_count} words",
                remediation="Expand steelman to 2-3 paragraphs genuinely arguing for alternative hypothesis"
            ))

        # Check for dismissive patterns
        dismissive_patterns = self.full_rules.get("protocol_compliance", {}).get(
            "steelman_dismissive_patterns", [
                "there is no evidence",
                "cannot be argued",
                "impossible to steelman",
                "no basis for",
                "no case can be made"
            ]
        )

        for pattern in dismissive_patterns:
            if pattern.lower() in content.lower():
                violations.append(ProtocolViolation(
                    violation_type="STEELMAN_APPEARS_DISMISSIVE",
                    severity="WARNING",
                    description=f"Steelman contains dismissive language: '{pattern}'",
                    stage=stage,
                    actual_value=pattern,
                    remediation="Steelman should argue FOR the alternative, not dismiss it"
                ))
                break  # Only report first match

        return violations

    # --- GATE SECTIONS ---

    def verify_gate_sections(
        self,
        bank_dir: Path,
        gate_num: int
    ) -> List[ProtocolViolation]:
        """
        Verify gate file has required sections.

        Args:
            bank_dir: Path to bank output directory
            gate_num: Gate number (1, 2, or 3)

        Returns:
            List of violations found
        """
        violations = []
        stage = f"gate_{gate_num}"

        gate_path = bank_dir / "3-gates" / f"gate-{gate_num}.md"
        if not gate_path.exists():
            violations.append(ProtocolViolation(
                violation_type="MISSING_GATE_FILE",
                severity="ERROR",
                description=f"Gate {gate_num} file not found",
                stage=stage,
                remediation=f"Create gate-{gate_num}.md per reasoning-gate protocol"
            ))
            return violations

        content = gate_path.read_text(encoding='utf-8')

        protocol_compliance = self.full_rules.get("protocol_compliance", {})
        required_sections = protocol_compliance.get(
            "required_gate_sections", [
                "Evidence Delta Analysis",
                "Probability Update",
                "Evidence Sufficiency Check"
            ]
        )

        # Get section aliases for flexible matching
        section_aliases = protocol_compliance.get("section_aliases", {})

        missing_sections = []
        for section in required_sections:
            # Get all names to check: primary + aliases
            names_to_check = [section] + section_aliases.get(section, [])

            found = False
            for name in names_to_check:
                # Look for section header or key phrase
                patterns = [
                    rf'##?\s+{re.escape(name)}',
                    rf'\*\*{re.escape(name)}\*\*',
                    name.lower().replace(" ", ".*?")
                ]
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        found = True
                        break
                if found:
                    break

            if not found:
                missing_sections.append(section)

        if missing_sections:
            # Include aliases in the message for clarity
            aliases_hint = []
            for section in missing_sections:
                aliases = section_aliases.get(section, [])
                if aliases:
                    aliases_hint.append(f"{section} (aliases: {', '.join(aliases[:3])}...)")
                else:
                    aliases_hint.append(section)

            violations.append(ProtocolViolation(
                violation_type="MISSING_GATE_SECTION",
                severity="WARNING",
                description=f"Gate {gate_num} missing sections: {', '.join(aliases_hint)}",
                stage=stage,
                expected_value=str(required_sections),
                actual_value=f"Missing: {missing_sections}",
                remediation="Add missing sections per reasoning-gate template"
            ))

        return violations

    # --- ADVERSARIAL SECTIONS ---

    def verify_adversarial_sections(
        self,
        bank_dir: Path
    ) -> List[ProtocolViolation]:
        """
        Verify adversarial challenge has required components.

        Args:
            bank_dir: Path to bank output directory

        Returns:
            List of violations found
        """
        violations = []
        stage = "adversarial_challenge"
        adversarial_dir = bank_dir / "4-adversarial"

        required_files = {
            "counter-case.md": "Counter-Case analysis",
            "disconfirming-searches.md": "Disconfirming searches",
            "steelman.md": "Steelman argument",
            "verdict.md": "Adversarial verdict"
        }

        for filename, description in required_files.items():
            filepath = adversarial_dir / filename
            if not filepath.exists():
                violations.append(ProtocolViolation(
                    violation_type="MISSING_ADVERSARIAL_FILE",
                    severity="ERROR",
                    description=f"Missing adversarial component: {description}",
                    stage=stage,
                    expected_value=filename,
                    remediation=f"Create {filename} per adversarial-challenger protocol"
                ))

        # Verify verdict has required content
        verdict_path = adversarial_dir / "verdict.md"
        if verdict_path.exists():
            content = verdict_path.read_text(encoding='utf-8')

            # Check for verdict type
            verdict_types = ["STRENGTHENED", "UNCHANGED", "WEAKENED", "REVISED"]
            found_verdict = False
            for vtype in verdict_types:
                if vtype.lower() in content.lower():
                    found_verdict = True
                    break

            if not found_verdict:
                violations.append(ProtocolViolation(
                    violation_type="INVALID_ADVERSARIAL_VERDICT",
                    severity="WARNING",
                    description="Verdict file missing verdict type (STRENGTHENED/UNCHANGED/WEAKENED/REVISED)",
                    stage=stage,
                    remediation="Add explicit verdict type to verdict.md"
                ))

        return violations

    # --- SYNTHESIS VERIFICATION ---

    def verify_synthesis(
        self,
        bank_dir: Path
    ) -> List[ProtocolViolation]:
        """
        Verify synthesis stage compliance.

        Args:
            bank_dir: Path to bank output directory

        Returns:
            List of violations found
        """
        violations = []
        stage = "synthesis"
        synthesis_dir = bank_dir / "5-synthesis"

        # Check confidence calibration exists and was created first
        calibration_path = synthesis_dir / "confidence-calibration.md"
        assessment_path = synthesis_dir / "assessment.md"

        if not calibration_path.exists():
            violations.append(ProtocolViolation(
                violation_type="CONFIDENCE_CALIBRATION_MISSING",
                severity="ERROR",
                description="Confidence calibration file not found (must be created BEFORE assessment)",
                stage=stage,
                remediation="Create confidence-calibration.md following 6-step calibration process"
            ))
        elif assessment_path.exists():
            # Check calibration content
            calibration_content = calibration_path.read_text(encoding='utf-8')

            required_steps = [
                "tier maximum",
                "corroboration",
                "contradiction",
                "adversarial",
                "coherence",
                "final"
            ]

            steps_found = sum(1 for step in required_steps if step.lower() in calibration_content.lower())
            if steps_found < 4:
                violations.append(ProtocolViolation(
                    violation_type="INCOMPLETE_CONFIDENCE_CALIBRATION",
                    severity="WARNING",
                    description=f"Confidence calibration missing steps (found {steps_found}/6)",
                    stage=stage,
                    expected_value="6 calibration steps",
                    actual_value=f"{steps_found} steps found",
                    remediation="Complete all 6 steps of confidence calibration"
                ))

            # Check for betting test
            if "bet" not in calibration_content.lower() and "wager" not in calibration_content.lower():
                violations.append(ProtocolViolation(
                    violation_type="MISSING_BETTING_TEST",
                    severity="WARNING",
                    description="Betting test not found in confidence calibration",
                    stage=stage,
                    remediation="Add betting test: 'Would I bet at these odds?'"
                ))

        return violations

    # --- COMBINED VERIFICATION ---

    def verify_all(
        self,
        bank_dir: Path,
        current_probability: float = 0.5
    ) -> List[ProtocolViolation]:
        """
        Run all protocol compliance checks.

        Args:
            bank_dir: Path to bank output directory
            current_probability: Current P(Architect) for determining leading hypothesis

        Returns:
            List of all violations found
        """
        violations = []

        # Determine leading hypothesis
        leading = "ARCHITECT" if current_probability > 0.5 else "PRAGMATIST"

        # Gate checks
        for gate_num in [1, 2, 3]:
            violations.extend(self.verify_gate_sections(bank_dir, gate_num))

        # Observable implications (Gate 2)
        violations.extend(self.verify_observable_implications(bank_dir, leading))

        # Adversarial checks
        violations.extend(self.verify_adversarial_sections(bank_dir))
        violations.extend(self.verify_disconfirmation_testing(bank_dir))
        violations.extend(self.verify_steelman_quality(bank_dir))

        # Synthesis checks
        violations.extend(self.verify_synthesis(bank_dir))

        return violations


# --- CLI INTERFACE ---

def main():
    """CLI interface for protocol compliance checker."""
    import argparse

    parser = argparse.ArgumentParser(description="CDM Research Protocol - Protocol Compliance Checker")
    parser.add_argument("bank_dir", type=Path, help="Path to bank output directory")
    parser.add_argument("--check", choices=[
        "all", "disconfirmation", "implications", "steelman", "gates", "adversarial", "synthesis"
    ], default="all", help="Which checks to run")
    parser.add_argument("--probability", type=float, default=0.5,
                        help="Current P(Architect) for hypothesis determination")

    args = parser.parse_args()

    checker = ProtocolComplianceChecker()

    if args.check == "all":
        violations = checker.verify_all(args.bank_dir, args.probability)
    elif args.check == "disconfirmation":
        violations = checker.verify_disconfirmation_testing(args.bank_dir)
    elif args.check == "implications":
        leading = "ARCHITECT" if args.probability > 0.5 else "PRAGMATIST"
        violations = checker.verify_observable_implications(args.bank_dir, leading)
    elif args.check == "steelman":
        violations = checker.verify_steelman_quality(args.bank_dir)
    elif args.check == "gates":
        violations = []
        for gate_num in [1, 2, 3]:
            violations.extend(checker.verify_gate_sections(args.bank_dir, gate_num))
    elif args.check == "adversarial":
        violations = checker.verify_adversarial_sections(args.bank_dir)
    elif args.check == "synthesis":
        violations = checker.verify_synthesis(args.bank_dir)

    if violations:
        print(f"Found {len(violations)} violation(s):")
        for v in violations:
            print(f"  [{v.severity}] {v.violation_type}")
            print(f"         {v.description}")
            if v.remediation:
                print(f"         Fix: {v.remediation}")
    else:
        print("No violations found. Protocol compliance verified.")


if __name__ == "__main__":
    main()
