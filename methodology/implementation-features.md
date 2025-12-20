# Implementation Features Reference

This document describes features implemented in the Python tools that extend beyond the core methodology documentation.

---

## Overview

The CDM/DRR Research Protocol has a two-layer architecture:

1. **Core Workflow (Markdown-based)**: Agent prompts, evidence gathering, Bayesian analysis, gates, adversarial challenges, and synthesis—all producing Markdown files
2. **Optional Tooling (JSON-based)**: Python tools for URL verification, content hashing, drift detection, and trust scoring

This document describes the optional tooling layer.

---

## 1. Evidence Verification (tools/process_evidence.py)

### Purpose

Validates evidence URLs are accessible and tracks changes over time.

### Fields Added to Evidence

When processing JSON evidence files, the tool adds:

```json
{
  "verification": {
    "status": "VERIFIED|ARCHIVED|PAYWALLED|DEAD|ERROR|PENDING",
    "live_ok": true,
    "archive_ok": false,
    "last_verified": "2025-12-19T12:00:00Z",
    "verification_count": 3
  }
}
```

### Status Definitions

| Status | Meaning |
|--------|---------|
| VERIFIED | URL accessible, content retrieved |
| ARCHIVED | Original dead, archive.org copy found |
| PAYWALLED | Content exists but behind paywall |
| DEAD | URL returns 404/error, no archive |
| ERROR | Verification failed (network, timeout) |
| PENDING | Not yet verified |

### Usage

```bash
python tools/process_evidence.py outputs/{Bank}/evidence.json
python tools/process_evidence.py --dry-run outputs/{Bank}/evidence.json
```

---

## 2. Content Hash and Drift Detection (tools/process_evidence.py)

### Purpose

Detects when source content changes after evidence was collected, which could invalidate quoted excerpts.

### Fields

```json
{
  "content": {
    "hash_sha256": "abc123def456...",
    "byte_length": 12345,
    "retrieved_at": "2025-12-19T12:00:00Z",
    "archive_url": "https://web.archive.org/web/...",
    "hash_history": [
      {"hash": "abc123", "timestamp": "2025-01-01T00:00:00Z", "byte_length": 12345}
    ],
    "content_changed": false,
    "excerpt_verified": true
  }
}
```

### Drift Detection Logic

1. On each verification, compute SHA256 of page content
2. Compare to stored hash
3. If different, set `content_changed: true` and append to `hash_history`
4. Flag `CONTENT_DRIFT_DETECTED` triggers review

### Excerpt Verification

If an `excerpt` field is provided:
1. Normalize both excerpt and retrieved content
2. Search for excerpt in content
3. Set `excerpt_verified: true` if found

---

## 3. Evidence Trust Flags (tools/trust_audit.py)

### Purpose

Automatically flags evidence quality issues for review before final classification.

### Available Flags

| Flag | Trigger Condition | Action Required |
|------|-------------------|-----------------|
| `SINGLE_SOURCE_CLAIM` | Claim supported by only 1 evidence item | Find corroborating source |
| `STALE_EVIDENCE` | Evidence >18 months old | Verify still current or find update |
| `UNVERIFIED_URLS` | URLs not yet verified | Run process_evidence.py |
| `CONTRADICTIONS_DETECTED` | Conflicting evidence found | Apply contradiction resolution |
| `LOW_TIER_ONLY` | Only Tier 3 evidence for key claim | Apply confidence cap, seek Tier 1/2 |
| `CONTENT_DRIFT_DETECTED` | Source content changed | Re-verify excerpt accuracy |
| `MISSING_CORROBORATION` | Key claim lacks triangulation | Find second independent source |
| `DUPLICATE_IDS` | Same evidence ID used twice | Fix ID collision |
| `EXCERPTS_NOT_VERIFIED` | Quoted text not confirmed in source | Verify quote accuracy |
| `TIER_AUTHORITY_MISMATCH` | Source doesn't match claimed tier | Reclassify evidence tier |

### Running Trust Audit

```bash
# Single bank
python tools/trust_audit.py outputs/{Bank}/evidence.json

# Batch (all banks in phase)
python tools/trust_audit.py --batch outputs/phase-1-european-tier1/

# Compare across banks
python tools/trust_audit.py --compare outputs/phase-1-european-tier1/*/evidence.json
```

---

## 4. Confidence Scoring (tools/trust_audit.py)

### Algorithm

```python
base_confidence = weighted_average(evidence_tiers)

# Apply adjustments
- Temporal decay: older evidence = lower weight
- Corroboration bonus: +5% per corroborating source
- Contradiction penalty: -10% per unresolved contradiction
- Tier cap: maximum confidence based on highest tier

# Clamp to valid range
final_confidence = clamp(base_confidence, 20, 95)
```

### Output

Trust audit produces a `trust_metrics` object:

```json
{
  "trust_metrics": {
    "overall_confidence": 75,
    "confidence_rationale": "Strong Tier 2 evidence with corroboration",
    "evidence_count": 12,
    "corroboration_rate": 0.83,
    "verification_rate": 0.92,
    "temporal_health_score": 0.78,
    "flags": ["STALE_EVIDENCE"],
    "authority_score": 0.72
  }
}
```

---

## 5. Domain Authority Scoring (tools/trust_audit.py)

### Purpose

Assigns authority scores to sources based on domain, used to weight evidence appropriately.

### Authority Tiers

| Domain Type | Examples | Authority Score |
|-------------|----------|-----------------|
| Standards Body | isda.org, finos.org | 1.0 |
| Regulator | sec.gov, fca.org.uk, esma.europa.eu | 1.0 |
| Bank Official | [bank].com investor relations | 0.95 |
| Trade Press | risk.net, waterstechnology.com | 0.8 |
| Business Press | ft.com, bloomberg.com, reuters.com | 0.75 |
| Consulting | mckinsey.com, oliverwyman.com | 0.6 |
| Social Media | linkedin.com | 0.3 |
| Blog Platform | medium.com, substack.com | 0.2 |

### Domain Matching

Uses safe domain matching (fixed in B4) to prevent substring attacks:

```python
# Correct: exact match or subdomain
is_trusted_domain("https://www.finos.org/page", "finos.org")  # True
is_trusted_domain("https://finos.org/page", "finos.org")     # True

# Correct: rejects malicious substrings
is_trusted_domain("https://malfinos.org/page", "finos.org")  # False
```

---

## 6. Batch Processing (tools/run_pipeline.py)

### Purpose

Orchestrates verification, trust audit, and report generation in sequence.

### Usage

```bash
# Full pipeline for single bank
python tools/run_pipeline.py outputs/{Bank}/evidence.json

# Batch processing for phase
python tools/run_pipeline.py --batch outputs/phase-1-european-tier1/

# Watch mode (auto-process on file changes)
python tools/run_pipeline.py --watch outputs/ --watch-interval 30
```

### Pipeline Stages

1. **Verify**: Run process_evidence.py to check URLs
2. **Audit**: Run trust_audit.py to calculate metrics
3. **Render**: Generate Final_Report.md from evidence

---

## Integration with Workflow

These tools are **optional enhancements**. The core workflow operates without them:

| Workflow Step | Core (Markdown) | Enhanced (JSON + Tools) |
|---------------|-----------------|-------------------------|
| Evidence Gathering | tier[N]-evidence.md | evidence.json |
| URL Verification | Manual check | Automated via process_evidence.py |
| Trust Assessment | Manual review | Automated via trust_audit.py |
| Confidence | Bayesian calculation | Bayesian + trust metrics |
| Final Report | synthesis/assessment.md | Final_Report.md (rendered) |

### To Enable Enhanced Processing

1. Output evidence in JSON format (not Markdown)
2. Run `tools/run_pipeline.py` after evidence gathering
3. Include trust_metrics in synthesis assessment

---

## File Locations

| Tool | Location | Purpose |
|------|----------|---------|
| process_evidence.py | tools/ | URL verification, content hashing |
| trust_audit.py | tools/ | Trust flags, confidence scoring |
| run_pipeline.py | tools/ | Orchestrate all tools |
| evidence-schema.json | templates/ | JSON schema documentation |

---

## Related Documentation

- [CLAUDE.md](../CLAUDE.md) - Central configuration and trust flag meanings
- [evidence-framework.md](evidence-framework.md) - Evidence tier definitions
- [evidence-schema.json](../templates/evidence-schema.json) - Schema documentation

---

_Last Updated: 2025-12-19_
