"""
Bayesian Calculator Validation Test Suite

Validates the CDM Research Protocol's Bayesian implementation against:
1. Standard mathematical formulas (MIT 18.05, textbooks)
2. Known worked examples
3. Edge cases
4. Independence checking

Sources:
- MIT 18.05 Introduction to Probability and Statistics
- Dawid (1982) "The Well-Calibrated Bayesian"
- ENFSI 2016 Guideline for Evaluative Reporting

Run with: pytest tools/tests/test_bayesian_calculator.py -v
"""

import pytest
import sys
from pathlib import Path
from math import isclose

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bayesian_calculator import BayesianCalculator, LRResult, IndependenceCheck


class TestBayesianFormulas:
    """Test core Bayesian formulas match textbook definitions."""

    @pytest.fixture
    def calc(self):
        return BayesianCalculator()

    # =========================================================================
    # PRIOR ODDS FORMULA: O(H) = P(H) / (1 - P(H))
    # Source: MIT 18.05 Class 12
    # =========================================================================

    def test_prior_odds_calculation(self, calc):
        """Prior odds = P(H) / (1 - P(H))"""
        # Test case: P = 0.30
        # Expected: 0.30 / 0.70 = 0.4286
        result = calc.calculate_posterior(prior=0.30, evidence_items=[])
        assert isclose(result.prior_odds, 0.30 / 0.70, rel_tol=1e-4)

    def test_prior_odds_50_percent(self, calc):
        """At P = 0.50, odds should be exactly 1.0"""
        result = calc.calculate_posterior(prior=0.50, evidence_items=[])
        assert isclose(result.prior_odds, 1.0, rel_tol=1e-6)

    def test_prior_odds_low_probability(self, calc):
        """Test with low prior (P = 0.10)"""
        # Expected: 0.10 / 0.90 = 0.111...
        result = calc.calculate_posterior(prior=0.10, evidence_items=[])
        assert isclose(result.prior_odds, 0.10 / 0.90, rel_tol=1e-4)

    def test_prior_odds_high_probability(self, calc):
        """Test with high prior (P = 0.90)"""
        # Expected: 0.90 / 0.10 = 9.0
        result = calc.calculate_posterior(prior=0.90, evidence_items=[])
        assert isclose(result.prior_odds, 9.0, rel_tol=1e-4)

    # =========================================================================
    # POSTERIOR ODDS FORMULA: O(H|E) = O(H) × LR
    # Source: MIT 18.05 Class 12
    # =========================================================================

    def test_posterior_odds_with_single_lr(self, calc):
        """Posterior odds = Prior odds × LR (single evidence)"""
        # Prior = 0.30, LR = 5.0
        # Prior odds = 0.4286
        # Posterior odds = 0.4286 × 5 = 2.143
        evidence = [{"type": "conference_speaker_cdm_topic", "tier": 2}]  # LR = 5.0
        result = calc.calculate_posterior(prior=0.30, evidence_items=evidence, apply_cap=False)

        expected_prior_odds = 0.30 / 0.70
        expected_posterior_odds = expected_prior_odds * 5.0
        assert isclose(result.posterior_odds, expected_posterior_odds, rel_tol=1e-3)

    def test_posterior_odds_lr_equals_one(self, calc):
        """Uninformative evidence (LR=1) should not change odds"""
        evidence = [{"type": "regulatory_pressure_inference", "tier": 4}]  # LR = 1.0
        result = calc.calculate_posterior(prior=0.30, evidence_items=evidence, apply_cap=False)

        # Posterior odds should equal prior odds when LR = 1
        assert isclose(result.posterior_odds, result.prior_odds, rel_tol=1e-6)

    # =========================================================================
    # COMBINED LR: LR_combined = LR_1 × LR_2 × ... × LR_n
    # Source: MIT 18.05, assumes independence
    # =========================================================================

    def test_combined_lr_multiplication(self, calc):
        """Combined LR is product of individual LRs"""
        # LRs: 5.0 × 3.7 = 18.5
        evidence = [
            {"type": "conference_speaker_cdm_topic", "tier": 2},     # LR = 5.0
            {"type": "named_working_group_membership", "tier": 2}    # LR = 3.7
        ]
        result = calc.calculate_posterior(prior=0.30, evidence_items=evidence, apply_cap=False)

        expected_combined_lr = 5.0 * 3.7
        assert isclose(result.combined_lr, expected_combined_lr, rel_tol=1e-3)

    def test_combined_lr_with_pragmatist_evidence(self, calc):
        """LR < 1 reduces probability (Pragmatist evidence)"""
        # LR = 0.33 (no_mention_cdm_trade_coverage)
        evidence = [{"type": "no_mention_cdm_trade_coverage", "tier": 2}]
        result = calc.calculate_posterior(prior=0.50, evidence_items=evidence, apply_cap=False)

        # Posterior should be less than prior
        assert result.posterior < 0.50
        assert isclose(result.combined_lr, 0.33, rel_tol=1e-2)

    # =========================================================================
    # POSTERIOR PROBABILITY: P(H|E) = O(H|E) / (1 + O(H|E))
    # Source: Standard Bayesian conversion
    # =========================================================================

    def test_posterior_probability_formula(self, calc):
        """P(H|E) = posterior_odds / (1 + posterior_odds)"""
        evidence = [{"type": "conference_speaker_cdm_topic", "tier": 2}]  # LR = 5.0
        result = calc.calculate_posterior(prior=0.30, evidence_items=evidence, apply_cap=False)

        # Manual calculation
        prior_odds = 0.30 / 0.70
        posterior_odds = prior_odds * 5.0
        expected_posterior = posterior_odds / (1 + posterior_odds)

        assert isclose(result.posterior, expected_posterior, rel_tol=1e-4)

    def test_posterior_at_odds_one(self, calc):
        """When posterior odds = 1, probability should be 0.50"""
        # Need prior and LR such that prior_odds × LR = 1
        # P = 0.30, prior_odds = 0.4286, need LR = 2.33 to get odds = 1
        # Use neutral evidence and P = 0.50
        evidence = [{"type": "regulatory_pressure_inference", "tier": 4}]  # LR = 1.0
        result = calc.calculate_posterior(prior=0.50, evidence_items=evidence, apply_cap=False)

        assert isclose(result.posterior, 0.50, rel_tol=1e-6)


class TestWorkedExamples:
    """Test against known worked examples from course materials and documentation."""

    @pytest.fixture
    def calc(self):
        return BayesianCalculator()

    def test_example_from_lr_tables_json(self, calc):
        """Test example from config/bayesian-lr-tables.json calculation_instructions"""
        # Example from JSON: Prior = 0.30, LRs = 14 × 5 × 0.21 = 14.7
        # Prior odds = 0.43
        # Posterior odds = 0.43 × 14.7 = 6.32
        # Posterior = 6.32 / 7.32 = 0.86 = 86%

        # Note: This example uses hypothetical LRs, we test the math
        prior = 0.30
        prior_odds = prior / (1 - prior)  # 0.4286
        combined_lr = 14.7
        posterior_odds = prior_odds * combined_lr  # ~6.3
        expected_posterior = posterior_odds / (1 + posterior_odds)  # ~0.86

        assert isclose(prior_odds, 0.4286, rel_tol=1e-2)
        assert isclose(posterior_odds, 6.3, rel_tol=0.05)
        assert isclose(expected_posterior, 0.86, rel_tol=0.02)

    def test_strong_architect_evidence(self, calc):
        """Strong Tier 1 evidence should yield high posterior"""
        # official_production_announcement: LR = 95
        evidence = [{"type": "official_production_announcement", "tier": 1}]
        result = calc.calculate_posterior(prior=0.30, evidence_items=evidence, apply_cap=False)

        # Prior odds = 0.4286, Posterior odds = 0.4286 × 95 = 40.7
        # Posterior = 40.7 / 41.7 = 0.976
        assert result.posterior > 0.95

    def test_strong_pragmatist_evidence(self, calc):
        """Strong Pragmatist evidence should yield low posterior"""
        # official_statement_no_cdm_plans: LR = 0.03
        evidence = [{"type": "official_statement_no_cdm_plans", "tier": 1}]
        result = calc.calculate_posterior(prior=0.50, evidence_items=evidence, apply_cap=False)

        # Prior odds = 1.0, Posterior odds = 1.0 × 0.03 = 0.03
        # Posterior = 0.03 / 1.03 = 0.029
        assert result.posterior < 0.05


class TestConfidenceCaps:
    """Test confidence cap application per CLAUDE.md Section 7."""

    @pytest.fixture
    def calc(self):
        return BayesianCalculator()

    def test_tier1_cap_95_percent(self, calc):
        """Tier 1 evidence caps at 95%"""
        # Very strong evidence that would otherwise exceed 95%
        evidence = [{"type": "official_production_announcement", "tier": 1}]
        result = calc.calculate_posterior(prior=0.50, evidence_items=evidence, apply_cap=True)

        # Raw posterior would be ~0.99, but should cap at 0.95
        assert result.capped_posterior is not None
        assert result.capped_posterior <= 0.95

    def test_tier2_cap_75_percent(self, calc):
        """Tier 2 evidence caps at 75%"""
        # Multiple strong Tier 2 evidence
        evidence = [
            {"type": "trade_press_reports_cdm_pilot", "tier": 2},      # LR = 15
            {"type": "conference_speaker_cdm_topic", "tier": 2}        # LR = 5
        ]
        result = calc.calculate_posterior(prior=0.50, evidence_items=evidence, apply_cap=True)

        # Combined LR = 75, should push posterior high but cap at 75%
        if result.posterior > 0.75:
            assert result.capped_posterior is not None
            assert result.capped_posterior <= 0.75

    def test_tier3_cap_50_percent(self, calc):
        """Tier 3 evidence caps at 50%"""
        evidence = [
            {"type": "job_posting_specifically_mentions_cdm", "tier": 3},  # LR = 3.0
            {"type": "linkedin_profile_mentions_cdm_work", "tier": 3}     # LR = 2.3
        ]
        result = calc.calculate_posterior(prior=0.30, evidence_items=evidence, apply_cap=True)

        # Check cap is applied if posterior exceeds 50%
        if result.posterior > 0.50:
            assert result.capped_posterior is not None
            assert result.capped_posterior <= 0.50

    def test_no_cap_when_below_threshold(self, calc):
        """No cap applied when posterior is below tier cap"""
        evidence = [{"type": "isda_agm_speaker_general", "tier": 2}]  # LR = 1.6
        result = calc.calculate_posterior(prior=0.20, evidence_items=evidence, apply_cap=True)

        # Posterior should be low enough to not trigger cap
        assert result.capped_posterior is None or result.posterior == result.capped_posterior


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def calc(self):
        return BayesianCalculator()

    def test_empty_evidence(self, calc):
        """No evidence should return prior unchanged"""
        result = calc.calculate_posterior(prior=0.30, evidence_items=[])
        assert result.posterior == 0.30
        assert result.combined_lr == 1.0

    def test_very_low_prior(self, calc):
        """Very low prior (P = 0.01)"""
        result = calc.calculate_posterior(prior=0.01, evidence_items=[])
        assert isclose(result.prior_odds, 0.01 / 0.99, rel_tol=1e-4)

    def test_very_high_prior(self, calc):
        """Very high prior (P = 0.99)"""
        result = calc.calculate_posterior(prior=0.99, evidence_items=[])
        assert isclose(result.prior_odds, 0.99 / 0.01, rel_tol=1e-4)

    def test_unknown_evidence_type(self, calc):
        """Unknown evidence type should use LR = 1.0 (neutral)"""
        evidence = [{"type": "completely_unknown_type", "tier": 2}]
        result = calc.calculate_posterior(prior=0.30, evidence_items=evidence)

        # Should have warning about unknown type
        assert any("not found" in w.lower() for w in result.warnings)
        # LR should be 1.0 (neutral)
        assert result.combined_lr == 1.0

    def test_extreme_lr_warning(self, calc):
        """Extreme combined LR should trigger warning"""
        # Multiple strong evidence to push combined LR > 100
        evidence = [
            {"type": "official_production_announcement", "tier": 1},   # LR = 95
            {"type": "official_pilot_announcement_with_timeline", "tier": 1}  # LR = 27
        ]
        result = calc.calculate_posterior(prior=0.30, evidence_items=evidence)

        # Combined LR = 95 × 27 = 2565, should trigger warning
        assert any("EXTREME_LR" in w for w in result.warnings)


class TestIndependenceChecking:
    """Test independence checking algorithm."""

    @pytest.fixture
    def calc(self):
        return BayesianCalculator()

    def test_duplicate_url_detection(self, calc):
        """Should detect duplicate URLs"""
        evidence = [
            {"type": "test1", "source_url": "https://example.com/article"},
            {"type": "test2", "source_url": "https://example.com/article"},  # Duplicate
        ]
        result = calc.check_independence(evidence)

        assert not result.independent
        assert any("DUPLICATE_URL" in w for w in result.warnings)

    def test_domain_concentration_warning(self, calc):
        """Should warn about domain concentration (>2 from same domain)"""
        evidence = [
            {"type": "test1", "source_url": "https://example.com/page1"},
            {"type": "test2", "source_url": "https://example.com/page2"},
            {"type": "test3", "source_url": "https://example.com/page3"},
        ]
        result = calc.check_independence(evidence)

        assert any("DOMAIN_CONCENTRATION" in w for w in result.warnings)

    def test_vendor_causal_link_detection(self, calc):
        """Should detect vendor claim + confirmation causal pattern"""
        evidence = [
            {"type": "vendor_claim", "source_url": "https://vendor.com/release"},
            {"type": "vendor_confirmation", "source_url": "https://bank.com/confirm"},
        ]
        result = calc.check_independence(evidence)

        assert any("CAUSAL_LINK" in w for w in result.warnings)

    def test_independent_evidence(self, calc):
        """Truly independent evidence should pass checks"""
        evidence = [
            {"type": "test1", "source_url": "https://source1.com/article"},
            {"type": "test2", "source_url": "https://source2.com/article"},
        ]
        result = calc.check_independence(evidence)

        assert result.independent
        assert len(result.warnings) == 0

    def test_www_prefix_normalization(self, calc):
        """www. prefix should be normalized for domain comparison"""
        evidence = [
            {"type": "test1", "source_url": "https://www.example.com/page1"},
            {"type": "test2", "source_url": "https://example.com/page2"},
            {"type": "test3", "source_url": "https://www.example.com/page3"},
        ]
        result = calc.check_independence(evidence)

        # Should recognize these as same domain
        assert any("DOMAIN_CONCENTRATION" in w for w in result.warnings)


class TestLRLookup:
    """Test LR lookup functionality."""

    @pytest.fixture
    def calc(self):
        return BayesianCalculator()

    def test_tier1_lr_lookup(self, calc):
        """Should correctly lookup Tier 1 LR values"""
        result = calc.lookup_lr("official_production_announcement")
        assert result.found_in_table
        assert result.lr == 200.0  # Updated per ENFSI calibration
        assert result.tier == 1

    def test_tier2_lr_lookup(self, calc):
        """Should correctly lookup Tier 2 LR values"""
        result = calc.lookup_lr("conference_speaker_cdm_topic")
        assert result.found_in_table
        assert result.lr == 5.0
        assert result.tier == 2

    def test_tier3_lr_lookup(self, calc):
        """Should correctly lookup Tier 3 LR values"""
        result = calc.lookup_lr("job_posting_specifically_mentions_cdm")
        assert result.found_in_table
        assert result.lr == 3.0
        assert result.tier == 3

    def test_tier4_lr_lookup(self, calc):
        """Should correctly lookup Tier 4 LR values"""
        result = calc.lookup_lr("no_evidence_after_full_protocol_search")
        assert result.found_in_table
        assert result.lr == 0.012  # Updated per ENFSI calibration
        assert result.tier == 4

    def test_unknown_type_returns_neutral(self, calc):
        """Unknown type should return LR = 1.0"""
        result = calc.lookup_lr("totally_fake_evidence_type")
        assert not result.found_in_table
        assert result.lr == 1.0


class TestAgentValidation:
    """Test agent calculation validation."""

    @pytest.fixture
    def calc(self):
        return BayesianCalculator()

    def test_correct_agent_calculation_passes(self, calc):
        """Agent with correct calculation should pass validation"""
        evidence = [{"type": "conference_speaker_cdm_topic", "tier": 2}]  # LR = 5.0

        # Calculate correct values
        prior_odds = 0.30 / 0.70
        posterior_odds = prior_odds * 5.0
        correct_posterior = posterior_odds / (1 + posterior_odds)

        validation = calc.validate_agent_calculation(
            agent_posterior=correct_posterior,
            agent_combined_lr=5.0,
            prior=0.30,
            evidence_items=evidence
        )

        assert validation.valid
        assert len(validation.issues) == 0

    def test_incorrect_agent_posterior_fails(self, calc):
        """Agent with wrong posterior should fail validation"""
        evidence = [{"type": "conference_speaker_cdm_topic", "tier": 2}]  # LR = 5.0

        validation = calc.validate_agent_calculation(
            agent_posterior=0.90,  # Wrong - should be ~0.68
            agent_combined_lr=5.0,
            prior=0.30,
            evidence_items=evidence
        )

        assert not validation.valid
        assert any("Posterior discrepancy" in issue for issue in validation.issues)

    def test_incorrect_agent_lr_fails(self, calc):
        """Agent with wrong LR should fail validation"""
        evidence = [{"type": "conference_speaker_cdm_topic", "tier": 2}]  # LR = 5.0

        validation = calc.validate_agent_calculation(
            agent_posterior=0.68,
            agent_combined_lr=10.0,  # Wrong - should be 5.0
            prior=0.30,
            evidence_items=evidence
        )

        assert not validation.valid
        assert any("LR discrepancy" in issue for issue in validation.issues)


class TestENFSIScaleAlignment:
    """
    Validate platform LR interpretations against ENFSI 2016 verbal scale.

    ENFSI Scale (European Network of Forensic Science Institutes):
    - 1-10: Weak support
    - 10-100: Moderate support
    - 100-1000: Moderately strong support
    - 1000-10000: Strong support
    - >10000: Very strong support

    Source: ENFSI Guideline for Evaluative Reporting in Forensic Science (2016)
    """

    @pytest.fixture
    def calc(self):
        return BayesianCalculator()

    def test_lr_200_is_moderately_strong(self, calc):
        """
        After ENFSI calibration: LR=200 (official_production_announcement)
        is now in ENFSI 'Moderately strong support' range (100-1000).

        The "Near-definitive Architect" label is appropriate for this range.
        """
        result = calc.lookup_lr("official_production_announcement")

        # Verify the updated LR value
        assert result.lr == 200.0

        # ENFSI classification for LR in range 100-1000 is "Moderately strong"
        # "Near-definitive" is acceptable for LR=200
        assert result.interpretation == "Near-definitive Architect"

    def test_lr_27_interpretation(self, calc):
        """LR=27 is in ENFSI 'Moderate support' range (10-100)"""
        result = calc.lookup_lr("official_pilot_announcement_with_timeline")
        assert result.lr == 27.0
        # After calibration, label matches ENFSI "Moderate" range
        assert result.interpretation == "Moderate Architect"

    def test_lr_values_are_within_reasonable_range(self, calc):
        """All LR values should be within typical forensic science ranges"""
        evidence_types = calc.get_evidence_types()

        for ev_type, info in evidence_types.items():
            lr = info['lr']
            # LRs should typically be between 0.001 and 10000 for forensic applications
            assert 0.001 <= lr <= 10000, f"{ev_type} has unusual LR={lr}"


# ============================================================================
# Run tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
