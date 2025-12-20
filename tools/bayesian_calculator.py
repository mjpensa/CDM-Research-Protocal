"""
CDM Research Protocol - Bayesian Calculator v1.0

Python implementation of Bayesian probability updates.
Used to validate agent calculations and detect errors.

Features:
- Prior to posterior calculation
- LR table lookups
- Independence checking
- Extreme LR detection
- Agent calculation validation

Usage:
    from bayesian_calculator import BayesianCalculator

    calc = BayesianCalculator()
    result = calc.calculate_posterior(
        prior=0.30,
        evidence_items=[
            {"type": "official_pilot_announcement_with_timeline", "tier": 1},
            {"type": "named_working_group_membership", "tier": 2}
        ]
    )
    print(f"Posterior: {result.posterior:.1%}")
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from collections import Counter
from urllib.parse import urlparse

# Import config loader
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import (
    load_bayesian_tables,
    get_confidence_caps,
    get_extreme_lr_bounds
)


@dataclass
class LRResult:
    """Result of looking up a likelihood ratio."""
    evidence_type: str
    tier: int
    lr: float
    interpretation: str
    found_in_table: bool
    notes: str = ""


@dataclass
class IndependenceCheck:
    """Result of checking evidence independence."""
    independent: bool
    warnings: List[str] = field(default_factory=list)
    adjustments: Dict[str, str] = field(default_factory=dict)


@dataclass
class BayesianResult:
    """Result of a Bayesian calculation."""
    prior: float
    posterior: float
    prior_odds: float
    posterior_odds: float
    combined_lr: float
    individual_lrs: List[LRResult]
    independence_check: IndependenceCheck
    confidence_cap: Optional[float]
    capped_posterior: Optional[float]
    warnings: List[str] = field(default_factory=list)
    calculation_trace: str = ""


@dataclass
class ValidationResult:
    """Result of validating agent calculation."""
    valid: bool
    agent_posterior: float
    calculated_posterior: float
    discrepancy: float
    agent_lr: float
    calculated_lr: float
    lr_discrepancy: float
    issues: List[str] = field(default_factory=list)


class BayesianCalculator:
    """
    Performs Bayesian probability calculations for CDM research.
    """

    def __init__(self):
        """Initialize with LR tables from config."""
        self.lr_tables = load_bayesian_tables()
        self.confidence_caps = get_confidence_caps()
        self.extreme_lr_bounds = get_extreme_lr_bounds()

        # Build flat lookup of all evidence types
        self._build_lr_lookup()

    def _build_lr_lookup(self):
        """Build a flat dictionary of evidence_type -> LR info."""
        self.lr_lookup = {}

        for tier_key in ['tier1_evidence', 'tier2_evidence', 'tier3_evidence', 'tier4_evidence']:
            tier_data = self.lr_tables.get(tier_key, {})
            tier_num = int(tier_key[4])  # Extract number from 'tierN_evidence'

            evidence_types = tier_data.get('evidence_types', {})
            for ev_type, ev_info in evidence_types.items():
                self.lr_lookup[ev_type] = {
                    'tier': tier_num,
                    'lr': ev_info.get('lr', 1.0),
                    'interpretation': ev_info.get('interpretation', ''),
                    'p_e_given_architect': ev_info.get('p_e_given_architect', 0.5),
                    'p_e_given_pragmatist': ev_info.get('p_e_given_pragmatist', 0.5)
                }

    def lookup_lr(self, evidence_type: str, tier: int = None) -> LRResult:
        """
        Look up likelihood ratio for an evidence type.

        Args:
            evidence_type: Type of evidence (e.g., 'official_pilot_announcement_with_timeline')
            tier: Optional tier hint

        Returns:
            LRResult with LR value and metadata
        """
        if evidence_type in self.lr_lookup:
            info = self.lr_lookup[evidence_type]
            return LRResult(
                evidence_type=evidence_type,
                tier=info['tier'],
                lr=info['lr'],
                interpretation=info['interpretation'],
                found_in_table=True
            )

        # Not found - return neutral LR with warning
        return LRResult(
            evidence_type=evidence_type,
            tier=tier or 3,
            lr=1.0,
            interpretation="Unknown - using neutral LR",
            found_in_table=False,
            notes=f"Evidence type '{evidence_type}' not found in LR tables"
        )

    def check_independence(self, evidence_items: List[Dict]) -> IndependenceCheck:
        """
        Check if evidence items are independent.

        Flags:
        - Same URL appearing multiple times
        - Multiple items from same domain
        - Causally linked evidence (e.g., vendor + vendor confirmation)

        Args:
            evidence_items: List of dicts with 'source_url' field

        Returns:
            IndependenceCheck with warnings and suggested adjustments
        """
        result = IndependenceCheck(independent=True)

        if not evidence_items:
            return result

        # Check 1: Duplicate URLs
        urls = [item.get('source_url', '') for item in evidence_items if item.get('source_url')]
        url_counts = Counter(urls)

        for url, count in url_counts.items():
            if count > 1:
                result.independent = False
                result.warnings.append(f"DUPLICATE_URL: '{url[:50]}...' appears {count} times")
                result.adjustments[url] = f"Count only once (not {count}x)"

        # Check 2: Domain concentration
        def extract_domain(url):
            try:
                parsed = urlparse(url)
                domain = parsed.netloc.lower()
                if domain.startswith('www.'):
                    domain = domain[4:]
                return domain
            except:
                return 'unknown'

        domains = [extract_domain(item.get('source_url', '')) for item in evidence_items]
        domain_counts = Counter(d for d in domains if d and d != 'unknown')

        for domain, count in domain_counts.items():
            if count > 2:
                result.warnings.append(
                    f"DOMAIN_CONCENTRATION: {count} items from {domain} - consider if independent"
                )

        # Check 3: Vendor + vendor confirmation pattern
        evidence_types = [item.get('type', '') for item in evidence_items]
        has_vendor_claim = any('vendor' in t.lower() for t in evidence_types)
        has_vendor_confirmation = any('confirm' in t.lower() for t in evidence_types)

        if has_vendor_claim and has_vendor_confirmation:
            result.warnings.append(
                "CAUSAL_LINK: Vendor claim and confirmation may not be independent"
            )

        return result

    def calculate_posterior(
        self,
        prior: float,
        evidence_items: List[Dict],
        apply_cap: bool = True
    ) -> BayesianResult:
        """
        Calculate posterior probability from prior and evidence.

        Args:
            prior: Prior probability of Architect (0.0 to 1.0)
            evidence_items: List of dicts with 'type' and optionally 'tier', 'source_url'
            apply_cap: Whether to apply confidence caps

        Returns:
            BayesianResult with full calculation details
        """
        warnings = []
        calculation_lines = []

        # Step 1: Calculate prior odds
        prior_odds = prior / (1 - prior) if prior < 1 else float('inf')
        calculation_lines.append(f"Prior: P(Architect) = {prior:.2%}")
        calculation_lines.append(f"Prior Odds = {prior:.2f} / {1-prior:.2f} = {prior_odds:.3f}")

        # Step 2: Look up LRs for each evidence item
        individual_lrs = []
        for item in evidence_items:
            ev_type = item.get('type', item.get('evidence_type', 'unknown'))
            tier = item.get('tier')

            lr_result = self.lookup_lr(ev_type, tier)
            individual_lrs.append(lr_result)

            if not lr_result.found_in_table:
                warnings.append(lr_result.notes)

            calculation_lines.append(
                f"  {ev_type}: LR = {lr_result.lr} ({lr_result.interpretation})"
            )

        # Step 3: Check independence
        independence = self.check_independence(evidence_items)
        if not independence.independent:
            warnings.extend(independence.warnings)

        # Step 4: Calculate combined LR
        combined_lr = 1.0
        for lr_result in individual_lrs:
            combined_lr *= lr_result.lr

        if individual_lrs:
            calculation_lines.append(f"\nCombined LR = {' x '.join(str(lr.lr) for lr in individual_lrs)}")
            calculation_lines.append(f"           = {combined_lr:.4f}")

        # Check for extreme LR
        lower_bound, upper_bound = self.extreme_lr_bounds
        if combined_lr > upper_bound:
            warnings.append(f"EXTREME_LR: Combined LR ({combined_lr:.2f}) exceeds {upper_bound}")
        elif combined_lr < lower_bound:
            warnings.append(f"EXTREME_LR: Combined LR ({combined_lr:.4f}) below {lower_bound}")

        # Step 5: Calculate posterior odds
        posterior_odds = prior_odds * combined_lr
        calculation_lines.append(f"\nPosterior Odds = {prior_odds:.3f} x {combined_lr:.4f} = {posterior_odds:.4f}")

        # Step 6: Convert to probability
        posterior = posterior_odds / (1 + posterior_odds) if posterior_odds < float('inf') else 1.0
        calculation_lines.append(f"\nP(Architect | Evidence) = {posterior_odds:.4f} / (1 + {posterior_odds:.4f})")
        calculation_lines.append(f"                        = {posterior:.2%}")

        # Step 7: Apply confidence cap if needed
        confidence_cap = None
        capped_posterior = None

        if apply_cap and individual_lrs:
            highest_tier = min(lr.tier for lr in individual_lrs)
            cap = self.confidence_caps.get(highest_tier, 0.35)
            confidence_cap = cap

            if posterior > cap:
                capped_posterior = cap
                calculation_lines.append(f"\nConfidence cap (Tier {highest_tier}): {cap:.0%}")
                calculation_lines.append(f"Capped posterior: {capped_posterior:.2%}")
                warnings.append(f"Posterior capped from {posterior:.1%} to {cap:.0%} (Tier {highest_tier} evidence)")

        return BayesianResult(
            prior=prior,
            posterior=posterior,
            prior_odds=prior_odds,
            posterior_odds=posterior_odds,
            combined_lr=combined_lr,
            individual_lrs=individual_lrs,
            independence_check=independence,
            confidence_cap=confidence_cap,
            capped_posterior=capped_posterior,
            warnings=warnings,
            calculation_trace='\n'.join(calculation_lines)
        )

    def validate_agent_calculation(
        self,
        agent_posterior: float,
        agent_combined_lr: float,
        prior: float,
        evidence_items: List[Dict],
        tolerance: float = 0.05
    ) -> ValidationResult:
        """
        Validate an agent's Bayesian calculation against Python calculation.

        Args:
            agent_posterior: Agent's reported posterior probability
            agent_combined_lr: Agent's reported combined LR
            prior: Prior probability used
            evidence_items: Evidence items used
            tolerance: Acceptable discrepancy (default 5%)

        Returns:
            ValidationResult with comparison details
        """
        # Calculate using Python
        result = self.calculate_posterior(prior, evidence_items, apply_cap=False)

        # Compare
        posterior_discrepancy = abs(agent_posterior - result.posterior)
        lr_discrepancy = abs(agent_combined_lr - result.combined_lr) / max(agent_combined_lr, result.combined_lr, 0.001)

        issues = []

        if posterior_discrepancy > tolerance:
            issues.append(
                f"Posterior discrepancy: agent={agent_posterior:.1%}, calculated={result.posterior:.1%}, diff={posterior_discrepancy:.1%}"
            )

        if lr_discrepancy > tolerance:
            issues.append(
                f"LR discrepancy: agent={agent_combined_lr:.2f}, calculated={result.combined_lr:.2f}, diff={lr_discrepancy:.1%}"
            )

        # Check for independence issues
        if result.independence_check.warnings:
            issues.extend([f"Independence: {w}" for w in result.independence_check.warnings])

        return ValidationResult(
            valid=len(issues) == 0,
            agent_posterior=agent_posterior,
            calculated_posterior=result.posterior,
            discrepancy=posterior_discrepancy,
            agent_lr=agent_combined_lr,
            calculated_lr=result.combined_lr,
            lr_discrepancy=lr_discrepancy,
            issues=issues
        )

    def get_evidence_types(self) -> Dict[str, Dict]:
        """Get all available evidence types and their LRs."""
        return self.lr_lookup


# --- CLI ---

def main():
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    print("CDM Research Protocol - Bayesian Calculator Test\n")

    calc = BayesianCalculator()

    # Show available evidence types
    print("=== Available Evidence Types ===")
    for ev_type, info in list(calc.lr_lookup.items())[:5]:
        print(f"  Tier {info['tier']}: {ev_type} (LR={info['lr']})")
    print(f"  ... and {len(calc.lr_lookup) - 5} more\n")

    # Example calculation
    evidence = [
        {"type": "official_pilot_announcement_with_timeline", "tier": 1, "source_url": "https://example.com/pilot"},
        {"type": "named_working_group_membership", "tier": 2, "source_url": "https://isda.org/members"},
    ]

    # Check if evidence types exist
    for item in evidence:
        if item['type'] not in calc.lr_lookup:
            print(f"Note: '{item['type']}' not in LR tables - using neutral LR")

    result = calc.calculate_posterior(prior=0.30, evidence_items=evidence)

    print("=== Calculation Trace ===")
    print(result.calculation_trace)

    print("\n=== Summary ===")
    print(f"Prior: {result.prior:.1%}")
    print(f"Posterior: {result.posterior:.1%}")
    print(f"Combined LR: {result.combined_lr:.2f}")

    if result.capped_posterior:
        print(f"Capped Posterior: {result.capped_posterior:.1%}")

    if result.warnings:
        print(f"\nWarnings:")
        for w in result.warnings:
            print(f"  - {w}")

    # Test independence checking
    print("\n=== Independence Check Test ===")
    duplicate_evidence = [
        {"type": "test1", "source_url": "https://example.com/article"},
        {"type": "test2", "source_url": "https://example.com/article"},  # Duplicate
        {"type": "test3", "source_url": "https://example.com/other"},  # Same domain
        {"type": "vendor_claim", "source_url": "https://vendor.com/release"},
        {"type": "vendor_confirmation", "source_url": "https://bank.com/confirm"},
    ]

    independence = calc.check_independence(duplicate_evidence)
    print(f"Independent: {independence.independent}")
    if independence.warnings:
        print("Warnings:")
        for w in independence.warnings:
            print(f"  - {w}")

    # Test validation
    print("\n=== Validation Test ===")
    validation = calc.validate_agent_calculation(
        agent_posterior=0.75,
        agent_combined_lr=20.0,
        prior=0.30,
        evidence_items=evidence
    )

    print(f"Agent posterior: {validation.agent_posterior:.1%}")
    print(f"Calculated posterior: {validation.calculated_posterior:.1%}")
    print(f"Discrepancy: {validation.discrepancy:.1%}")
    print(f"Valid: {validation.valid}")

    if validation.issues:
        print("Issues:")
        for issue in validation.issues:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()
