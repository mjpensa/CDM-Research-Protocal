"""
CDM Research Protocol - Bayesian Validator v1.0

Validates agent Bayesian calculations by recomputing posteriors
and comparing against claimed values.

Usage:
    from bayesian_validator import BayesianValidator

    validator = BayesianValidator()
    violations = validator.validate_bayesian_update(bank_dir, tier=1, state=state)
"""

import re
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

# Project imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config_loader import (
        load_bayesian_tables,
        load_validation_rules,
        get_validation_tolerances
    )
    from orchestrator.violation_queue import ProtocolViolation
except ImportError:
    from tools.config_loader import (
        load_bayesian_tables,
        load_validation_rules,
        get_validation_tolerances
    )
    from tools.orchestrator.violation_queue import ProtocolViolation


class BayesianValidator:
    """
    Validates Bayesian calculations in agent outputs.

    Parses Bayesian update markdown files, extracts claimed values,
    recomputes expected values, and flags discrepancies.
    """

    def __init__(self):
        """Initialize the validator."""
        self.tolerances = get_validation_tolerances()
        self.lr_tables = load_bayesian_tables()

    def validate_bayesian_update(
        self,
        bank_dir: Path,
        tier: int,
        prior_probability: float
    ) -> List[ProtocolViolation]:
        """
        Validate a Bayesian update for a specific tier.

        Args:
            bank_dir: Path to bank output directory
            tier: Tier number (1, 2, or 3)
            prior_probability: Prior P(Architect) before this tier's evidence

        Returns:
            List of violations found
        """
        violations = []

        # Locate Bayesian update file
        bayesian_path = bank_dir / "2-bayesian" / f"post-tier{tier}-update.md"
        if not bayesian_path.exists():
            violations.append(ProtocolViolation(
                violation_type="MISSING_BAYESIAN_OUTPUT",
                severity="ERROR",
                description=f"Bayesian update file not found: {bayesian_path.name}",
                stage=f"bayesian_{tier}",
                remediation="Generate Bayesian update file per protocol"
            ))
            return violations

        # Parse agent's claimed values
        content = bayesian_path.read_text(encoding='utf-8')
        agent_claims = self._extract_agent_claims(content)

        if not agent_claims.get("posterior"):
            violations.append(ProtocolViolation(
                violation_type="UNPARSEABLE_BAYESIAN_OUTPUT",
                severity="WARNING",
                description="Could not parse posterior probability from Bayesian update",
                stage=f"bayesian_{tier}",
                remediation="Ensure Bayesian update follows template format"
            ))
            return violations

        # Load evidence and map to LRs
        evidence_path = bank_dir / "evidence.json"
        if evidence_path.exists():
            evidence_data = json.loads(evidence_path.read_text(encoding='utf-8'))
            tier_evidence = [
                e for e in evidence_data.get("evidence_items", [])
                if e.get("tier") == tier
            ]
        else:
            tier_evidence = []

        # Recompute expected values
        expected = self._compute_expected_values(prior_probability, tier_evidence, tier)

        # Compare values
        violations.extend(self._compare_values(agent_claims, expected, tier))

        return violations

    def _extract_agent_claims(self, content: str) -> Dict[str, Any]:
        """
        Extract claimed values from Bayesian update markdown.

        Args:
            content: Markdown content of Bayesian update file

        Returns:
            Dict with 'prior', 'posterior', 'combined_lr', 'evidence_items'
        """
        claims = {
            "prior": None,
            "posterior": None,
            "combined_lr": None,
            "evidence_items": []
        }

        # Extract prior probability
        prior_patterns = [
            r'Prior\s*(?:probability|P\(Architect\))?\s*[=:]\s*(\d+(?:\.\d+)?)\s*%?',
            r'P\(Architect\)\s*=\s*(\d+(?:\.\d+)?)\s*%?',
            r'prior\s+of\s+(\d+(?:\.\d+)?)\s*%'
        ]
        for pattern in prior_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                claims["prior"] = value / 100 if value > 1 else value
                break

        # Extract posterior probability
        posterior_patterns = [
            r'Posterior\s*(?:probability|P\(Architect\))?\s*[=:]\s*(\d+(?:\.\d+)?)\s*%?',
            r'Updated\s*P\(Architect\)\s*[=:]\s*(\d+(?:\.\d+)?)\s*%?',
            r'(?:Final|New)\s*probability\s*[=:]\s*(\d+(?:\.\d+)?)\s*%?',
            r'P\(Architect\|E\)\s*[=≈]\s*(\d+(?:\.\d+)?)\s*%?'
        ]
        for pattern in posterior_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                claims["posterior"] = value / 100 if value > 1 else value
                break

        # Extract combined LR
        lr_patterns = [
            r'Combined\s*(?:LR|likelihood ratio)\s*[=:]\s*(\d+(?:\.\d+)?)',
            r'LR_combined\s*[=:]\s*(\d+(?:\.\d+)?)',
            r'Product\s*of\s*LRs?\s*[=:]\s*(\d+(?:\.\d+)?)'
        ]
        for pattern in lr_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                claims["combined_lr"] = float(match.group(1))
                break

        # Extract individual LR claims
        lr_item_pattern = r'(?:LR|likelihood ratio)\s*[=:]\s*(\d+(?:\.\d+)?)'
        claims["evidence_items"] = [
            float(m) for m in re.findall(lr_item_pattern, content, re.IGNORECASE)
        ]

        return claims

    def _compute_expected_values(
        self,
        prior: float,
        evidence_items: List[Dict],
        tier: int
    ) -> Dict[str, Any]:
        """
        Compute expected Bayesian values from evidence.

        Args:
            prior: Prior P(Architect)
            evidence_items: List of evidence items from evidence.json
            tier: Tier number

        Returns:
            Dict with 'posterior', 'combined_lr', 'lr_assignments'
        """
        lr_assignments = []
        combined_lr = 1.0

        tier_key = f"tier{tier}_evidence"
        tier_data = self.lr_tables.get(tier_key, {})
        evidence_types = tier_data.get("evidence_types", {})

        for item in evidence_items:
            claim_type = item.get("claim_type", "")
            lr = self._lookup_lr_for_claim_type(claim_type, tier)
            lr_assignments.append({
                "claim_type": claim_type,
                "lr": lr
            })
            combined_lr *= lr

        # Compute posterior using Bayes' theorem
        prior_odds = prior / (1 - prior) if prior < 1 else float('inf')
        posterior_odds = prior_odds * combined_lr
        posterior = posterior_odds / (1 + posterior_odds) if posterior_odds != float('inf') else 1.0

        return {
            "prior": prior,
            "posterior": posterior,
            "combined_lr": combined_lr,
            "lr_assignments": lr_assignments
        }

    def _lookup_lr_for_claim_type(self, claim_type: str, tier: int) -> float:
        """
        Look up LR for a claim type from the LR tables.

        Args:
            claim_type: Claim type (e.g., 'production_usage', 'membership_or_participation')
            tier: Tier number

        Returns:
            Likelihood ratio (defaults to 1.0 if not found)
        """
        # Map claim types to evidence type keys
        claim_to_evidence = {
            "production_usage": "official_production_announcement",
            "pilot_or_poc": "official_pilot_with_timeline",
            "membership_or_participation": "working_group_membership",
            "open_source_contribution": "cdm_code_commits",
            "vendor_proxy_signal": "vendor_claims_bank_as_client",
            "hiring_signal": "job_posting_mentioning_cdm"
        }

        evidence_type = claim_to_evidence.get(claim_type, claim_type)
        tier_key = f"tier{tier}_evidence"
        tier_data = self.lr_tables.get(tier_key, {})
        evidence_types = tier_data.get("evidence_types", {})

        if evidence_type in evidence_types:
            return evidence_types[evidence_type].get("lr", 1.0)

        # Try direct lookup
        for et_key, et_data in evidence_types.items():
            if claim_type.lower() in et_key.lower():
                return et_data.get("lr", 1.0)

        return 1.0  # Neutral LR if not found

    def _compare_values(
        self,
        agent_claims: Dict[str, Any],
        expected: Dict[str, Any],
        tier: int
    ) -> List[ProtocolViolation]:
        """
        Compare agent claims against expected values.

        Args:
            agent_claims: Values extracted from agent output
            expected: Computed expected values
            tier: Tier number

        Returns:
            List of violations for discrepancies
        """
        violations = []
        stage = f"bayesian_{tier}"

        # Get tolerance thresholds
        posterior_tolerance = self.tolerances.get("posterior_tolerance_absolute", 0.05)
        lr_tolerance = self.tolerances.get("lr_tolerance_relative", 0.15)

        rules = load_validation_rules()
        escalation = rules.get("bayesian_validation", {}).get("severity_escalation", {})
        posterior_error_threshold = escalation.get("posterior_mismatch_error", 0.10)
        lr_error_threshold = escalation.get("lr_mismatch_error", 0.25)

        # Compare posterior probability
        if agent_claims.get("posterior") is not None and expected.get("posterior") is not None:
            diff = abs(agent_claims["posterior"] - expected["posterior"])

            if diff > posterior_error_threshold:
                violations.append(ProtocolViolation(
                    violation_type="BAYESIAN_POSTERIOR_MISMATCH",
                    severity="ERROR",
                    description=f"Posterior probability mismatch exceeds error threshold",
                    stage=stage,
                    expected_value=f"{expected['posterior']:.1%}",
                    actual_value=f"{agent_claims['posterior']:.1%}",
                    remediation="Recalculate posterior using standard Bayesian formula: P(A|E) = P(E|A)P(A) / P(E)"
                ))
            elif diff > posterior_tolerance:
                violations.append(ProtocolViolation(
                    violation_type="BAYESIAN_POSTERIOR_MISMATCH",
                    severity="WARNING",
                    description=f"Posterior probability differs from expected by {diff:.1%}",
                    stage=stage,
                    expected_value=f"{expected['posterior']:.1%}",
                    actual_value=f"{agent_claims['posterior']:.1%}",
                    remediation="Review calculation for potential rounding or LR mapping errors"
                ))

        # Compare combined LR
        if agent_claims.get("combined_lr") is not None and expected.get("combined_lr") is not None:
            expected_lr = expected["combined_lr"]
            agent_lr = agent_claims["combined_lr"]

            if expected_lr > 0:
                relative_diff = abs(agent_lr - expected_lr) / expected_lr

                if relative_diff > lr_error_threshold:
                    violations.append(ProtocolViolation(
                        violation_type="BAYESIAN_LR_MISMATCH",
                        severity="ERROR",
                        description=f"Combined LR mismatch ({relative_diff:.0%} relative difference)",
                        stage=stage,
                        expected_value=f"{expected_lr:.3f}",
                        actual_value=f"{agent_lr:.3f}",
                        remediation="Review LR assignments and check for double-counting or missing evidence"
                    ))
                elif relative_diff > lr_tolerance:
                    violations.append(ProtocolViolation(
                        violation_type="BAYESIAN_LR_MISMATCH",
                        severity="WARNING",
                        description=f"Combined LR differs from expected by {relative_diff:.0%}",
                        stage=stage,
                        expected_value=f"{expected_lr:.3f}",
                        actual_value=f"{agent_lr:.3f}",
                        remediation="Review LR mappings against bayesian-lr-tables.json"
                    ))

        # Check for extreme LR values
        extreme_upper = self.tolerances.get("extreme_lr_upper", 100)
        extreme_lower = self.tolerances.get("extreme_lr_lower", 0.01)

        if agent_claims.get("combined_lr") is not None:
            lr = agent_claims["combined_lr"]
            if lr > extreme_upper or lr < extreme_lower:
                violations.append(ProtocolViolation(
                    violation_type="EXTREME_COMBINED_LR",
                    severity="WARNING",
                    description=f"Combined LR ({lr:.3f}) outside normal range ({extreme_lower}-{extreme_upper})",
                    stage=stage,
                    expected_value=f"{extreme_lower}-{extreme_upper}",
                    actual_value=f"{lr:.3f}",
                    remediation="Review for potential calculation error or extraordinary evidence"
                ))

        return violations

    def validate_independence(
        self,
        evidence_items: List[Dict]
    ) -> List[ProtocolViolation]:
        """
        Check for independence violations in evidence.

        Detects:
        - Duplicate URLs
        - Domain concentration (>2 from same domain)
        - Causal linking (vendor claim + vendor confirmation)

        Args:
            evidence_items: List of evidence items

        Returns:
            List of violations for independence issues
        """
        violations = []

        # Check for duplicate URLs
        urls = [e.get("source_url", "") for e in evidence_items]
        seen_urls = set()
        for url in urls:
            if url and url in seen_urls:
                violations.append(ProtocolViolation(
                    violation_type="DUPLICATE_EVIDENCE_URL",
                    severity="WARNING",
                    description=f"Same URL used for multiple evidence items",
                    stage="evidence",
                    actual_value=url,
                    remediation="Remove duplicate or ensure claims are truly independent"
                ))
            seen_urls.add(url)

        # Check domain concentration
        from urllib.parse import urlparse
        domains = {}
        for e in evidence_items:
            url = e.get("source_url", "")
            if url:
                domain = urlparse(url).netloc
                domains[domain] = domains.get(domain, 0) + 1

        for domain, count in domains.items():
            if count > 2:
                violations.append(ProtocolViolation(
                    violation_type="DOMAIN_CONCENTRATION",
                    severity="WARNING",
                    description=f"High concentration from single domain: {count} items from {domain}",
                    stage="evidence",
                    actual_value=f"{domain}: {count} items",
                    remediation="Consider evidence dependence when calculating combined LR"
                ))

        # Check for vendor claim + bank confirmation patterns
        vendor_claims = [e for e in evidence_items if e.get("claim_type") == "vendor_proxy_signal"]
        if len(vendor_claims) > 1:
            violations.append(ProtocolViolation(
                violation_type="POTENTIAL_DOUBLE_COUNTING",
                severity="INFO",
                description=f"Multiple vendor proxy signals ({len(vendor_claims)}) may be causally linked",
                stage="evidence",
                remediation="Verify vendor claims are from independent sources"
            ))

        return violations


# --- CLI INTERFACE ---

def main():
    """CLI interface for Bayesian validator."""
    import argparse

    parser = argparse.ArgumentParser(description="CDM Research Protocol - Bayesian Validator")
    parser.add_argument("bank_dir", type=Path, help="Path to bank output directory")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3], required=True,
                        help="Tier to validate")
    parser.add_argument("--prior", type=float, default=0.30,
                        help="Prior P(Architect) (default: 0.30)")

    args = parser.parse_args()

    validator = BayesianValidator()
    violations = validator.validate_bayesian_update(
        bank_dir=args.bank_dir,
        tier=args.tier,
        prior_probability=args.prior
    )

    if violations:
        print(f"Found {len(violations)} violation(s):")
        for v in violations:
            print(f"  [{v.severity}] {v.violation_type}: {v.description}")
            if v.expected_value and v.actual_value:
                print(f"         Expected: {v.expected_value}, Actual: {v.actual_value}")
    else:
        print("No violations found. Bayesian calculations appear valid.")


if __name__ == "__main__":
    main()
