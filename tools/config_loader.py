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


@lru_cache(maxsize=1)
def load_calibration_config() -> dict:
    """Load calibration-config.json with caching."""
    path = CONFIG_DIR / "calibration-config.json"
    if not path.exists():
        raise FileNotFoundError(f"Calibration config not found: {path}")
    return json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def load_validation_rules() -> dict:
    """Load validation-rules.json with caching."""
    path = CONFIG_DIR / "validation-rules.json"
    if not path.exists():
        # Return defaults if file doesn't exist
        return get_default_validation_rules()
    return json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def load_ground_truth() -> dict:
    """Load ground-truth.json with caching."""
    path = CONFIG_DIR / "ground-truth.json"
    if not path.exists():
        return {"validated_outcomes": [], "pending_validations": [], "lr_accuracy_tracking": {}}
    return json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def load_regulatory_calendar() -> dict:
    """Load regulatory-calendar.json with caching."""
    path = CONFIG_DIR / "regulatory-calendar.json"
    if not path.exists():
        return {"active_mandates": [], "upcoming_mandates": [], "temporal_weighting_rules": {}}
    return json.loads(path.read_text(encoding='utf-8'))


def get_default_validation_rules() -> dict:
    """Return default validation rules if config file is missing."""
    return {
        "bayesian_validation": {
            "posterior_tolerance_absolute": 0.05,
            "lr_tolerance_relative": 0.15,
            "extreme_lr_upper": 100,
            "extreme_lr_lower": 0.01
        },
        "protocol_compliance": {
            "min_disconfirming_searches": 3,
            "min_observable_implications": 3,
            "min_steelman_words": 150,
            "min_robustness_questions": 5
        },
        "adjustment_consistency": {
            "std_threshold": 2.0,
            "min_precedents_for_check": 3
        }
    }


# NOTE: load_api_config() removed in v2.0 - API config no longer needed
# Platform now uses Claude Code extension (VS Code) for execution


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


# --- CALIBRATION ACCESSORS ---

def get_brier_thresholds() -> dict:
    """
    Returns Brier score thresholds for calibration assessment.
    Example: {'excellent': 0.10, 'good': 0.15, ...}
    """
    cfg = load_calibration_config()
    return cfg.get('brier_score_thresholds', {
        'excellent': 0.10,
        'good': 0.15,
        'acceptable': 0.20,
        'marginal': 0.25,
        'poor': 0.30
    })


def get_drift_detection_params() -> dict:
    """
    Returns drift detection parameters.
    Example: {'window_size': 10, 'direction_threshold': 0.60, ...}
    """
    cfg = load_calibration_config()
    return cfg.get('drift_detection', {
        'window_size': 10,
        'direction_threshold': 0.60,
        'significance_level': 0.05,
        'severity_thresholds': {'low': 0.05, 'medium': 0.10, 'high': 0.15}
    })


def get_minimum_validations() -> dict:
    """
    Returns minimum sample sizes for calibration assessments.
    Example: {'overall_assessment': 10, 'tier_level_assessment': 5, ...}
    """
    cfg = load_calibration_config()
    return cfg.get('minimum_validations', {
        'overall_assessment': 10,
        'tier_level_assessment': 5,
        'evidence_type_assessment': 5,
        'adjustment_recommendation': 8
    })


def get_lr_adjustment_rules() -> dict:
    """
    Returns rules for LR table update recommendations.
    """
    cfg = load_calibration_config()
    return cfg.get('lr_adjustment_rules', {
        'divergence_threshold_for_flag': 0.20,
        'divergence_threshold_for_recommendation': 0.30,
        'minimum_sample_for_empirical_lr': 5,
        'maximum_recommended_lr_change': 2.0
    })


def get_validation_tolerances() -> dict:
    """
    Returns tolerance thresholds for logic validation.
    """
    rules = load_validation_rules()
    return rules.get('bayesian_validation', {
        'posterior_tolerance_absolute': 0.05,
        'lr_tolerance_relative': 0.15
    })


def get_protocol_compliance_rules() -> dict:
    """
    Returns protocol compliance requirements.
    """
    rules = load_validation_rules()
    return rules.get('protocol_compliance', {
        'min_disconfirming_searches': 3,
        'min_observable_implications': 3,
        'min_steelman_words': 150
    })


def get_state_validation_config() -> dict:
    """
    Returns state validation configuration (Gap 5 fix).

    Includes validation mode (strict/warn/off) and specific
    error handling rules.

    Returns:
        dict with 'mode', 'fail_on_errors', etc.
    """
    rules = load_validation_rules()
    return rules.get('state_validation', {
        'mode': 'strict',
        'mode_override_env_var': 'CDM_VALIDATION_MODE',
        'fail_on_errors': {
            'probability_out_of_range': True,
            'history_mismatch': True,
            'invalid_stage': True,
            'schema_version_mismatch': False,
            'missing_required_fields': True,
            'duplicate_history_entries': True
        }
    })


def get_state_management_config() -> dict:
    """
    Returns state management timing configuration (Gaps 3, 8, 10 fixes).

    Includes lock timeouts, stale lock age, and retry config.

    Returns:
        dict with timing constants
    """
    thresholds = load_decision_thresholds()
    return thresholds.get('state_management', {
        'lock_timeout_seconds': 30,
        'stale_lock_age_seconds': 300,
        'workflow_staleness_hours': 1,
        'phase_scan_range': {'min': 1, 'max': 9},
        'retry_config': {
            'max_retries': 5,
            'base_delay_seconds': 0.1,
            'max_delay_seconds': 2.0
        }
    })


def get_log_rotation_config() -> dict:
    """
    Returns log rotation configuration (Gap 4 fix).

    Includes thresholds per log type, archive settings.

    Returns:
        dict with rotation settings
    """
    thresholds = load_decision_thresholds()
    return thresholds.get('log_rotation', {
        'enabled': True,
        'thresholds': {
            'checkpoint_log': {'max_entries': 1000, 'archive_threshold': 800},
            'error_log': {'max_entries': 500, 'archive_threshold': 400},
            'review_queue': {'max_entries': 200, 'archive_threshold': 150}
        },
        'archive_directory': 'archives',
        'retention_days': 90,
        'compress_archives': True,
        'check_interval': 100
    })


def get_state_versioning_config() -> dict:
    """
    Returns state versioning configuration (Gap 6 fix).

    Includes version limits, compression settings.

    Returns:
        dict with versioning settings
    """
    thresholds = load_decision_thresholds()
    return thresholds.get('state_versioning', {
        'enabled': True,
        'max_versions': 5,
        'version_directory': 'versions',
        'compress_old_versions': True,
        'version_triggers': ['stage_complete', 'probability_update', 'blocked', 'manual']
    })


# --- GROUND TRUTH ACCESSORS ---

def get_validated_banks() -> list[str]:
    """
    Return list of bank_ids with validated outcomes (confirmed classifications).
    These are banks where we know the actual classification result.
    """
    gt = load_ground_truth()
    return [v['bank_id'] for v in gt.get('validated_outcomes', [])]


def get_validated_outcome(bank_id: str) -> Optional[dict]:
    """
    Get validated outcome for a specific bank.

    Args:
        bank_id: Bank identifier

    Returns:
        dict with outcome details, or None if not validated
    """
    gt = load_ground_truth()
    for outcome in gt.get('validated_outcomes', []):
        if outcome.get('bank_id') == bank_id:
            return outcome
    return None


def get_pending_validations() -> list[dict]:
    """
    Return list of predictions awaiting validation.
    """
    gt = load_ground_truth()
    return gt.get('pending_validations', [])


# --- REGULATORY CALENDAR ACCESSORS ---

def get_active_mandates(jurisdiction: str = None) -> list[dict]:
    """
    Return active regulatory mandates, optionally filtered by jurisdiction.

    Args:
        jurisdiction: Optional filter (e.g., 'EU', 'UK', 'US', 'Japan')

    Returns:
        List of active mandate dicts
    """
    calendar = load_regulatory_calendar()
    mandates = calendar.get('active_mandates', [])
    if jurisdiction:
        mandates = [m for m in mandates if m.get('jurisdiction') == jurisdiction]
    return mandates


def get_mandate_by_id(mandate_id: str) -> Optional[dict]:
    """
    Get a specific mandate by ID.

    Args:
        mandate_id: Mandate identifier (e.g., 'EMIR_REFIT_EU', 'JSCC_CDM')

    Returns:
        Mandate dict or None if not found
    """
    calendar = load_regulatory_calendar()
    for mandate in calendar.get('active_mandates', []):
        if mandate.get('mandate_id') == mandate_id:
            return mandate
    for mandate in calendar.get('upcoming_mandates', []):
        if mandate.get('mandate_id') == mandate_id:
            return mandate
    return None


def get_temporal_weighting_rules() -> dict:
    """
    Get temporal weighting rules for evidence near regulatory deadlines.
    """
    calendar = load_regulatory_calendar()
    return calendar.get('temporal_weighting_rules', {})


# NOTE: API accessor functions removed in v2.0
# - get_api_model()
# - get_api_fallback_model()
# - get_api_retry_config()
# - get_api_timeout()
# - get_api_rate_limits()
# Platform now uses Claude Code extension (VS Code) for execution


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


def get_vendor_cdm_depth(vendor_id: str) -> Optional[str]:
    """
    Get vendor's CDM capability depth level (L0-L4).

    Args:
        vendor_id: Vendor identifier (e.g., 'murex', 'delta-capita')

    Returns:
        Depth level string (e.g., 'L2_translation', 'L4_workflow_native'),
        or None if vendor not found
    """
    try:
        matrix = load_vendor_matrix()
        mappings = matrix.get('vendor_depth_mapping', {}).get('mappings', {})
        return mappings.get(vendor_id)
    except FileNotFoundError:
        return None


def get_depth_classification_impact(depth_level: str) -> dict:
    """
    Get classification impact details for a CDM depth level.

    Args:
        depth_level: Depth level string (e.g., 'L2_translation')

    Returns:
        dict with classification_impact, pressure_direction, pressure_strength,
        and evidence_implication. Returns defaults if depth level not found.
    """
    default = {
        "classification_impact": "UNKNOWN",
        "pressure_direction": "neutral",
        "pressure_strength": 0.0,
        "evidence_implication": "Unknown depth level"
    }

    try:
        matrix = load_vendor_matrix()
        depth_config = matrix.get('cdm_capability_depth', {})
        level_info = depth_config.get(depth_level)

        if level_info:
            return {
                "classification_impact": level_info.get('classification_impact', 'UNKNOWN'),
                "pressure_direction": level_info.get('pressure_direction', 'neutral'),
                "pressure_strength": level_info.get('pressure_strength', 0.0),
                "evidence_implication": level_info.get('evidence_implication', '')
            }
        return default
    except FileNotFoundError:
        return default


def get_bank_vendor_depth(bank_id: str) -> Optional[dict]:
    """
    Get CDM depth information for a bank's vendor relationship.

    Args:
        bank_id: Bank identifier

    Returns:
        dict with vendor_id, depth_level, and classification_impact,
        or None if no vendor relationship found
    """
    try:
        matrix = load_vendor_matrix()
        relationships = matrix.get('bank_vendor_relationships', [])

        for rel in relationships:
            if rel.get('bank_id') == bank_id:
                vendor_id = rel.get('vendor_id')
                depth = get_vendor_cdm_depth(vendor_id)
                impact = get_depth_classification_impact(depth) if depth else {}

                return {
                    "bank_id": bank_id,
                    "vendor_id": vendor_id,
                    "vendor_name": rel.get('vendor_name', vendor_id),
                    "depth_level": depth,
                    "relationship_type": rel.get('relationship_type'),
                    "classification_impact": impact.get('classification_impact'),
                    "pressure_direction": impact.get('pressure_direction'),
                    "pressure_strength": impact.get('pressure_strength')
                }
        return None
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
            # Support both 'id' and 'bank_id' keys for compatibility
            if bank.get('bank_id') == bank_id or bank.get('id') == bank_id:
                return bank
        return None
    except FileNotFoundError:
        return None


def get_prior_for_bank(bank_id: str) -> float:
    """
    Calculate adjusted prior P(ARCHITECT) for a bank based on manifest metadata.

    Applies adjustments from prior_adjustments in bank-manifest.json:
    - derivatives_dominant: +adjustment_pct (typically 10%)
    - confirmed_contributor: +contributor_adjustment_pct (typically 15-20%)
    - confirmed_production: +production_adjustment_pct (typically 30%)
    - regional_peer_architect: +peer_adjustment_pct (typically 10%)
    - active_ma_integration with net_direction="pragmatist": -integration_adjustment_pct
    - us_gsib: +5% (default)
    - european_regulatory_pressure: +5% (default)

    Args:
        bank_id: Bank identifier

    Returns:
        Prior probability P(ARCHITECT) as float 0-1 scale (e.g., 0.50 for 50%)
        Default is 0.50 (null hypothesis: PRAGMATIST until proven otherwise)
    """
    BASE_PRIOR = 0.50  # Null hypothesis: equal probability
    MIN_PRIOR = 0.10   # Floor to leave room for evidence
    MAX_PRIOR = 0.90   # Cap to leave room for evidence

    bank_config = get_bank_config(bank_id)
    if not bank_config:
        return BASE_PRIOR

    adjustments = bank_config.get('prior_adjustments', {})
    if not adjustments:
        return BASE_PRIOR

    prior = BASE_PRIOR
    adjustment_log = []

    # Positive adjustments (increase P(ARCHITECT))
    if adjustments.get('derivatives_dominant'):
        adj = adjustments.get('adjustment_pct', 10) / 100
        prior += adj
        adjustment_log.append(f"derivatives_dominant: +{adj*100:.0f}%")

    if adjustments.get('confirmed_contributor'):
        adj = adjustments.get('contributor_adjustment_pct', 15) / 100
        prior += adj
        adjustment_log.append(f"confirmed_contributor: +{adj*100:.0f}%")

    if adjustments.get('confirmed_production'):
        adj = adjustments.get('production_adjustment_pct', 30) / 100
        prior += adj
        adjustment_log.append(f"confirmed_production: +{adj*100:.0f}%")

    if adjustments.get('regional_peer_architect'):
        adj = adjustments.get('peer_adjustment_pct', 10) / 100
        prior += adj
        adjustment_log.append(f"regional_peer_architect: +{adj*100:.0f}%")

    if adjustments.get('us_gsib'):
        adj = 0.05  # Default 5% for US G-SIBs
        prior += adj
        adjustment_log.append(f"us_gsib: +{adj*100:.0f}%")

    if adjustments.get('european_regulatory_pressure'):
        adj = 0.05  # Default 5% for European regulatory pressure
        prior += adj
        adjustment_log.append(f"european_regulatory_pressure: +{adj*100:.0f}%")

    # Negative adjustments (decrease P(ARCHITECT))
    if adjustments.get('active_ma_integration'):
        net_direction = adjustments.get('net_direction', 'neutral')
        if net_direction == 'pragmatist':
            adj = adjustments.get('integration_adjustment_pct', 15) / 100
            prior -= adj
            adjustment_log.append(f"active_ma_integration (pragmatist): -{adj*100:.0f}%")

    # Apply floor and cap
    prior = max(MIN_PRIOR, min(MAX_PRIOR, prior))

    return prior


def get_prior_for_bank_with_details(bank_id: str) -> dict:
    """
    Calculate adjusted prior with full details for logging/debugging.

    Args:
        bank_id: Bank identifier

    Returns:
        dict with 'prior', 'base_prior', 'adjustments_applied', 'bank_name'
    """
    BASE_PRIOR = 0.50
    MIN_PRIOR = 0.10
    MAX_PRIOR = 0.90

    bank_config = get_bank_config(bank_id)
    if not bank_config:
        return {
            'prior': BASE_PRIOR,
            'base_prior': BASE_PRIOR,
            'adjustments_applied': [],
            'bank_name': bank_id,
            'capped': False
        }

    adjustments = bank_config.get('prior_adjustments', {})
    prior = BASE_PRIOR
    applied = []

    # Apply all adjustments (same logic as get_prior_for_bank)
    if adjustments.get('derivatives_dominant'):
        adj = adjustments.get('adjustment_pct', 10) / 100
        prior += adj
        applied.append({'type': 'derivatives_dominant', 'adjustment': adj})

    if adjustments.get('confirmed_contributor'):
        adj = adjustments.get('contributor_adjustment_pct', 15) / 100
        prior += adj
        applied.append({'type': 'confirmed_contributor', 'adjustment': adj})

    if adjustments.get('confirmed_production'):
        adj = adjustments.get('production_adjustment_pct', 30) / 100
        prior += adj
        applied.append({'type': 'confirmed_production', 'adjustment': adj})

    if adjustments.get('regional_peer_architect'):
        adj = adjustments.get('peer_adjustment_pct', 10) / 100
        prior += adj
        applied.append({'type': 'regional_peer_architect', 'adjustment': adj})

    if adjustments.get('us_gsib'):
        adj = 0.05
        prior += adj
        applied.append({'type': 'us_gsib', 'adjustment': adj})

    if adjustments.get('european_regulatory_pressure'):
        adj = 0.05
        prior += adj
        applied.append({'type': 'european_regulatory_pressure', 'adjustment': adj})

    if adjustments.get('active_ma_integration'):
        net_direction = adjustments.get('net_direction', 'neutral')
        if net_direction == 'pragmatist':
            adj = adjustments.get('integration_adjustment_pct', 15) / 100
            prior -= adj
            applied.append({'type': 'active_ma_integration', 'adjustment': -adj})

    uncapped_prior = prior
    prior = max(MIN_PRIOR, min(MAX_PRIOR, prior))

    return {
        'prior': prior,
        'base_prior': BASE_PRIOR,
        'adjustments_applied': applied,
        'bank_name': bank_config.get('bank_name', bank_id),
        'capped': uncapped_prior != prior,
        'uncapped_prior': uncapped_prior if uncapped_prior != prior else None
    }


# --- RELATIONSHIPS KNOWLEDGE BASE ---

KB_DIR = PROJECT_ROOT / "knowledge_base"


@lru_cache(maxsize=1)
def load_relationships() -> dict:
    """Load relationships.json from knowledge base with caching."""
    path = KB_DIR / "relationships.json"
    if not path.exists():
        return {"relationships": [], "entities": {}, "relationship_types": {}}
    return json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def load_source_credibility() -> dict:
    """Load source_credibility.json from knowledge base with caching."""
    path = KB_DIR / "source_credibility.json"
    if not path.exists():
        return {"domain_credibility": {}, "author_credibility": {}}
    return json.loads(path.read_text(encoding='utf-8'))


def get_bank_relationships(bank_id: str) -> list[dict]:
    """
    Get all relationships for a specific bank.

    Args:
        bank_id: Bank identifier

    Returns:
        List of relationship dicts where bank is source or target
    """
    rels = load_relationships()
    relationships = rels.get('relationships', [])
    return [
        r for r in relationships
        if r.get('source_entity') == bank_id or r.get('target_entity') == bank_id
    ]


def get_relationship_by_id(rel_id: str) -> Optional[dict]:
    """
    Get a specific relationship by ID.

    Args:
        rel_id: Relationship identifier (e.g., 'REL-001')

    Returns:
        Relationship dict or None if not found
    """
    rels = load_relationships()
    for rel in rels.get('relationships', []):
        if rel.get('id') == rel_id:
            return rel
    return None


def get_entity_info(entity_id: str, entity_type: str) -> Optional[dict]:
    """
    Get information about an entity (vendor, CCP, working group, etc.).

    Args:
        entity_id: Entity identifier
        entity_type: 'vendors', 'ccps', 'working_groups', 'regulators'

    Returns:
        Entity info dict or None
    """
    rels = load_relationships()
    entities = rels.get('entities', {})
    type_entities = entities.get(entity_type, {})
    return type_entities.get(entity_id)


def get_domain_credibility(domain: str) -> Optional[dict]:
    """
    Get credibility information for a domain.

    Args:
        domain: Domain name (e.g., 'risk.net', 'linkedin.com')

    Returns:
        Credibility info dict or None
    """
    cred = load_source_credibility()
    return cred.get('domain_credibility', {}).get(domain)


def get_author_credibility(author_name: str) -> Optional[dict]:
    """
    Get credibility information for a specific author.

    Args:
        author_name: Author name

    Returns:
        Author credibility dict or None
    """
    cred = load_source_credibility()
    authors = cred.get('author_credibility', {}).get('authors', [])
    for author in authors:
        if author.get('name', '').lower() == author_name.lower():
            return author
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
    load_calibration_config.cache_clear()
    load_validation_rules.cache_clear()
    load_ground_truth.cache_clear()
    load_regulatory_calendar.cache_clear()
    load_relationships.cache_clear()
    load_source_credibility.cache_clear()
    # NOTE: load_api_config removed in v2.0


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
