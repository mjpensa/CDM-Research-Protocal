"""
CDM Research Protocol - Centralized Configuration Loader v1.0

Single source of truth for all configuration values.
All tools must import thresholds from here, not define their own.

This module provides:
- Cached loading of JSON configuration files
- Convenience accessors for common threshold values
- Validation functions for classification taxonomy
"""

import json
from pathlib import Path
from functools import lru_cache
from typing import Optional

# --- PROJECT PATHS ---
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_ROOT / "config"


# --- CORE LOADERS (cached) ---

@lru_cache(maxsize=1)
def load_decision_thresholds() -> dict:
    """Load decision-thresholds.json with caching."""
    path = CONFIG_DIR / "decision-thresholds.json"
    if not path.exists():
        raise FileNotFoundError(f"Decision thresholds config not found: {path}")
    return json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def load_bayesian_tables() -> dict:
    """Load bayesian-lr-tables.json with caching."""
    path = CONFIG_DIR / "bayesian-lr-tables.json"
    if not path.exists():
        raise FileNotFoundError(f"Bayesian LR tables not found: {path}")
    return json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def load_classification_taxonomy() -> dict:
    """Load classification-taxonomy.json with caching."""
    path = CONFIG_DIR / "classification-taxonomy.json"
    if not path.exists():
        raise FileNotFoundError(f"Classification taxonomy not found: {path}")
    return json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def load_vendor_matrix() -> dict:
    """Load vendor-matrix.json with caching."""
    path = CONFIG_DIR / "vendor-matrix.json"
    if not path.exists():
        raise FileNotFoundError(f"Vendor matrix not found: {path}")
    return json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def load_bank_manifest() -> dict:
    """Load bank-manifest.json with caching."""
    path = CONFIG_DIR / "bank-manifest.json"
    if not path.exists():
        raise FileNotFoundError(f"Bank manifest not found: {path}")
    return json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def load_source_authority() -> dict:
    """Load source-authority.json with caching."""
    path = CONFIG_DIR / "source-authority.json"
    if not path.exists():
        raise FileNotFoundError(f"Source authority config not found: {path}")
    return json.loads(path.read_text(encoding='utf-8'))


# --- CONVENIENCE ACCESSORS ---

def get_confidence_caps() -> dict:
    """
    Returns tier-to-max-confidence mapping.
    Example: {1: 95, 2: 75, 3: 50, 4: 35}
    """
    thresholds = load_decision_thresholds()
    caps = thresholds['confidence_caps']
    return {
        1: caps['tier1_only'],
        2: caps['tier2_only'],
        3: caps['tier3_only'],
        4: caps.get('tier4_inference_only', 35),
        None: caps.get('tier4_inference_only', 35)  # Fallback for missing tier
    }


def get_skip_threshold() -> int:
    """
    Returns the threshold for skipping to adversarial (default: 80%).
    If P(Architect) > 80% OR P(Architect) < 20%, skip remaining evidence tiers.
    """
    thresholds = load_decision_thresholds()
    return thresholds['workflow_decisions']['skip_to_adversarial']['threshold']


def get_low_confidence_block_threshold() -> int:
    """
    Returns the threshold below which we BLOCK for human review (default: 50%).
    """
    thresholds = load_decision_thresholds()
    return thresholds['workflow_decisions']['low_confidence_block']['threshold']


def get_uncertainty_range() -> tuple[int, int]:
    """
    Returns (lower, upper) for the uncertainty range (default: 40-60%).
    Probabilities in this range warrant careful analysis.
    """
    thresholds = load_decision_thresholds()
    ur = thresholds['workflow_decisions']['uncertainty_range']
    return (ur['lower'], ur['upper'])


def get_early_termination_threshold() -> int:
    """
    Returns threshold for early termination after Tier 1 (default: 95%).
    """
    thresholds = load_decision_thresholds()
    return thresholds['workflow_decisions']['early_termination']['threshold']


def get_extreme_lr_bounds() -> tuple[float, float]:
    """
    Returns (lower, upper) bounds for extreme likelihood ratio flagging.
    Default: (0.01, 100) - flag if combined LR outside this range.
    """
    thresholds = load_decision_thresholds()
    elr = thresholds['workflow_decisions']['extreme_lr_flag']
    return (elr['lower'], elr['upper'])


def get_temporal_thresholds() -> dict:
    """
    Returns temporal threshold values for evidence freshness.
    Returns: {'current_days': 548, 'dated_days': 1095}
    - current_days: Evidence < this age gets full weight (18 months)
    - dated_days: Evidence > this age is historical only (3 years)
    """
    thresholds = load_decision_thresholds()
    return thresholds.get('temporal_thresholds', {
        'current_days': 548,   # 18 months
        'dated_days': 1095     # 3 years
    })


def get_default_priors() -> dict:
    """
    Returns default prior probabilities for classifications.
    Example: {'architect_native': 0.05, 'architect_leader': 0.10, ...}
    """
    tables = load_bayesian_tables()
    return tables['default_priors']


def get_valid_claim_types() -> list[str]:
    """
    Returns list of valid claim_type enum values.
    """
    return [
        'production_usage',
        'pilot_or_poc',
        'membership_or_participation',
        'open_source_contribution',
        'vendor_proxy_signal',
        'hiring_signal'
    ]


def get_lr_for_evidence_type(tier: int, evidence_type: str) -> Optional[dict]:
    """
    Look up likelihood ratio for a specific evidence type.

    Args:
        tier: 1, 2, 3, or 4
        evidence_type: The type key (e.g., 'official_production_announcement')

    Returns:
        dict with 'p_e_given_architect', 'p_e_given_pragmatist', 'lr', 'interpretation'
        or None if not found
    """
    tables = load_bayesian_tables()
    tier_key = f"tier{tier}_evidence"

    if tier_key not in tables:
        # Handle tier4 which may be called 'absence_evidence' or 'tier4_evidence'
        if tier == 4:
            tier_key = tables.get('tier4_evidence') or tables.get('absence_evidence')
            if tier_key is None:
                return None
        else:
            return None

    tier_data = tables.get(tier_key, {})
    evidence_types = tier_data.get('evidence_types', {})
    return evidence_types.get(evidence_type)


def get_source_authority_mapping() -> dict:
    """
    Returns domain to (authority, tier) mapping.
    Example: {'isda.org': ('HIGH', 1), 'linkedin.com': ('VERY_LOW', 3)}
    """
    cfg = load_source_authority()
    return {
        domain: (info['authority'], info['tier'])
        for domain, info in cfg.get('domain_mappings', {}).items()
    }


def get_authority_levels() -> dict:
    """
    Returns authority level to weight mapping.
    Example: {'HIGH': 1.0, 'MEDIUM_HIGH': 0.8, ...}
    """
    cfg = load_source_authority()
    return cfg.get('authority_levels', {
        'HIGH': 1.0, 'MEDIUM_HIGH': 0.8, 'MEDIUM': 0.6, 'LOW': 0.3, 'VERY_LOW': 0.1
    })


def get_vendor_domains() -> list:
    """Returns list of known vendor domains."""
    cfg = load_source_authority()
    return cfg.get('vendor_domains', [])


def get_maturity_weights() -> dict:
    """
    Returns claim_type to maturity weight mapping.
    Example: {'production_usage': 5, 'pilot_or_poc': 3, ...}
    """
    thresholds = load_decision_thresholds()
    return thresholds.get('maturity_weights', {
        'production_usage': 5,
        'pilot_or_poc': 3,
        'open_source_contribution': 2,
        'membership_or_participation': 1,
        'vendor_proxy_signal': 2,
        'hiring_signal': 1
    })


# --- VALIDATION FUNCTIONS ---

def validate_classification(classification: str, variant: str) -> bool:
    """
    Validate that a classification/variant pair is valid per taxonomy.

    Args:
        classification: Main classification (ARCHITECT, PRAGMATIST, OBSERVER, UNKNOWN)
        variant: Sub-classification variant

    Returns:
        True if valid, False otherwise
    """
    try:
        taxonomy = load_classification_taxonomy()
        classifications = taxonomy.get('classifications', {})
        valid_variants = classifications.get(classification, {}).get('variants', [])
        return variant in valid_variants
    except (FileNotFoundError, KeyError):
        # If taxonomy file doesn't exist or is malformed, allow any value
        return True


def get_vendor_relationship(bank_id: str) -> Optional[dict]:
    """
    Look up known vendor relationships for a bank.

    Args:
        bank_id: Bank identifier (e.g., 'barclays', 'hsbc')

    Returns:
        dict with vendor relationship info, or None if not found
    """
    try:
        matrix = load_vendor_matrix()
        return matrix.get('banks', {}).get(bank_id)
    except FileNotFoundError:
        return None


def get_bank_config(bank_id: str) -> Optional[dict]:
    """
    Look up configuration for a specific bank from the manifest.

    Args:
        bank_id: Bank identifier

    Returns:
        dict with bank configuration, or None if not found
    """
    try:
        manifest = load_bank_manifest()
        banks = manifest.get('banks', [])
        for bank in banks:
            if bank.get('id') == bank_id:
                return bank
        return None
    except FileNotFoundError:
        return None


# --- CACHE MANAGEMENT ---

def clear_config_cache():
    """
    Clear all cached configuration data.
    Use after modifying config files to pick up changes.
    """
    load_decision_thresholds.cache_clear()
    load_bayesian_tables.cache_clear()
    load_classification_taxonomy.cache_clear()
    load_source_authority.cache_clear()
    load_vendor_matrix.cache_clear()
    load_bank_manifest.cache_clear()


# --- MAIN (for testing) ---

if __name__ == "__main__":
    print("CDM Research Protocol - Configuration Loader Test")
    print("=" * 50)

    try:
        print("\n1. Decision Thresholds:")
        print(f"   Skip threshold: {get_skip_threshold()}%")
        print(f"   Low confidence block: {get_low_confidence_block_threshold()}%")
        print(f"   Uncertainty range: {get_uncertainty_range()}")
        print(f"   Early termination: {get_early_termination_threshold()}%")
        print(f"   Extreme LR bounds: {get_extreme_lr_bounds()}")

        print("\n2. Confidence Caps:")
        caps = get_confidence_caps()
        for tier, cap in caps.items():
            print(f"   Tier {tier}: {cap}%")

        print("\n3. Temporal Thresholds:")
        temporal = get_temporal_thresholds()
        print(f"   Current (full weight): <{temporal['current_days']} days")
        print(f"   Historical (context only): >{temporal['dated_days']} days")

        print("\n4. Default Priors:")
        priors = get_default_priors()
        for key, value in priors.items():
            if key != 'rationale' and isinstance(value, (int, float)):
                print(f"   {key}: {value*100:.0f}%")

        print("\n5. Valid Claim Types:")
        for ct in get_valid_claim_types():
            print(f"   - {ct}")

        print("\n[OK] All configuration loaded successfully!")

    except FileNotFoundError as e:
        print(f"\n[ERROR] Configuration error: {e}")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
