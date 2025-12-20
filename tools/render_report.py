"""
CDM Forensic Research Engine v2.3 - Report Renderer
Generates a formatted Markdown report from verified evidence.
Uses trust_metrics from trust_audit.py when available.
"""

import json
import sys
import logging
from pathlib import Path
from datetime import datetime

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def render_report(json_path: str) -> bool:
    """
    Render a Markdown report from processed evidence.
    Returns True on success, False on failure.
    """
    json_path = Path(json_path).resolve()

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {json_path}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return False

    items = data.get('evidence_items', [])
    valid_items = [
        i for i in items
        if i.get('verification', {}).get('status') in ['verified', 'archived']
    ]

    # 1. Get Confidence from trust_metrics if available, otherwise calculate
    trust_metrics = data.get('trust_metrics', {})
    if trust_metrics.get('overall_confidence') is not None:
        # Use pre-calculated confidence from trust_audit.py
        confidence_pct = trust_metrics['overall_confidence']
        if confidence_pct >= 70:
            confidence = "HIGH"
        elif confidence_pct >= 50:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        confidence_detail = f"{confidence} ({confidence_pct}%)"
    else:
        # Fallback: calculate locally (legacy mode)
        tier_weights = {1: 3, 2: 2, 3: 1}
        tier_scores = sum(tier_weights.get(i.get('tier', 3), 0) for i in valid_items)

        if tier_scores > 6:
            confidence = "HIGH"
        elif tier_scores > 3:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        confidence_detail = confidence

    # 2. Calculate Maturity (Strategic Advancement)
    maturity_map = {
        "production_usage": 5,
        "pilot_or_poc": 3,
        "open_source_contribution": 2,
        "membership_or_participation": 1,
        "hiring_signal": 1,
        "vendor_proxy_signal": 2
    }

    max_maturity = 0
    for i in valid_items:
        val = maturity_map.get(i.get('claim_type'), 0)
        if val > max_maturity:
            max_maturity = val

    maturity_labels = {
        5: "ARCHITECT (Native)",
        4: "ARCHITECT (Native)",
        3: "PRAGMATIST (Pilot)",
        2: "PRAGMATIST (Vendor/Signal)",
        1: "OBSERVER",
        0: "UNKNOWN"
    }
    maturity_label = maturity_labels.get(max_maturity, "UNKNOWN")

    # 3. Calculate statistics
    total_items = len(items)
    verified_count = sum(1 for i in items if i.get('verification', {}).get('status') == 'verified')
    archived_count = sum(1 for i in items if i.get('verification', {}).get('status') == 'archived')
    dead_count = sum(1 for i in items if i.get('verification', {}).get('status') == 'dead')
    error_count = sum(1 for i in items if i.get('verification', {}).get('status') in ['error', 'pending'])

    # 4. Render Markdown
    bank_name = data.get('bank_name', 'Unknown Bank')
    run_id = data.get('meta', {}).get('run_id', 'N/A')
    run_timestamp = data.get('meta', {}).get('timestamp', 'N/A')

    # Build trust flags section if available
    flags = trust_metrics.get('flags', [])
    flags_section = ""
    if flags:
        flags_section = "\n**Trust Flags:** " + ", ".join(f"`{f}`" for f in flags[:5])
        if len(flags) > 5:
            flags_section += f" (+{len(flags) - 5} more)"

    md = f"""# Forensic CDM Research: {bank_name}

**Run ID:** `{run_id}` | **Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
**Confidence:** {confidence_detail} | **Maturity:** {maturity_label}{flags_section}

---

## 1. Strategic Verdict

{data.get('analysis_summary', '_No analysis summary provided._')}

---

## 2. Evidence Statistics

| Metric | Count |
|--------|-------|
| Total Evidence Items | {total_items} |
| Verified (Live) | {verified_count} |
| Archived (Wayback) | {archived_count} |
| Dead Links | {dead_count} |
| Errors/Pending | {error_count} |

---

## 3. Evidence Ledger

| ID | Tier | Type | Claim | Status | Source |
|----|------|------|-------|--------|--------|
"""

    for item in items:
        status = item.get('verification', {}).get('status', 'unknown').upper()

        # Status icons
        icon_map = {
            "VERIFIED": "![check](https://img.shields.io/badge/-verified-green)",
            "ARCHIVED": "![archive](https://img.shields.io/badge/-archived-blue)",
            "PAYWALLED": "![lock](https://img.shields.io/badge/-paywalled-yellow)",
            "DEAD": "![x](https://img.shields.io/badge/-dead-red)",
            "ERROR": "![error](https://img.shields.io/badge/-error-red)",
            "PENDING": "![pending](https://img.shields.io/badge/-pending-gray)"
        }
        # Fallback to text icons for simpler rendering
        text_icons = {
            "VERIFIED": "VERIFIED",
            "ARCHIVED": "ARCHIVED",
            "PAYWALLED": "PAYWALLED",
            "DEAD": "DEAD",
            "ERROR": "ERROR",
            "PENDING": "PENDING"
        }
        status_display = text_icons.get(status, status)

        # Link handling - prefer archive URL for archived items
        link = item.get('source_url', '#')
        if status == "ARCHIVED":
            link = item.get('content', {}).get('archive_url', link)

        # Escape pipe characters in claim text
        claim_text = item.get('claim', '').replace('|', '\\|')

        md += f"| {item.get('id', 'N/A')} | T{item.get('tier', '?')} | `{item.get('claim_type', 'unknown')}` | {claim_text} | {status_display} | [Link]({link}) |\n"

    # 5. Add trust metrics section if available
    trust_section = ""
    if trust_metrics:
        trust_section = f"""
## 4. Trust Metrics

| Metric | Score |
|--------|-------|
| Overall Confidence | {trust_metrics.get('overall_confidence', 'N/A')}% |
| Source Diversity | {trust_metrics.get('source_diversity_score', 'N/A')} |
| Temporal Health | {trust_metrics.get('temporal_health_score', 'N/A')} |
| Corroboration Rate | {trust_metrics.get('corroboration_rate', 'N/A')} |
| Verification Rate | {trust_metrics.get('verification_rate', 'N/A')} |
| Authority Score | {trust_metrics.get('authority_score', 'N/A')} |
| Excerpt Verified | {trust_metrics.get('excerpt_verification_rate', 'N/A')} |

"""
        if trust_metrics.get('confidence_rationale'):
            trust_section += f"**Rationale:** {trust_metrics['confidence_rationale']}\n\n"

    # 6. Add footer
    md += f"""
---

{trust_section}## 5. Methodology Notes

- **Confidence Score**: Calculated per methodology/confidence-calibration.md with adjustments for corroboration, verification, freshness, and authority.
- **Maturity Classification**: Based on highest claim type found in verified evidence.
- **Verification**: Live URLs checked first, then Wayback Machine fallback for dead links.
- **Excerpt Verification**: Checks if claimed excerpts actually appear in source content.

---

_Report generated by CDM Forensic Research Engine v2.3_
_Run timestamp: {run_timestamp}_
"""

    # 6. Write output
    out_path = json_path.parent / "Final_Report.md"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(md)

    logger.info(f"Report rendered: {out_path}")
    return True


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python render_report.py <path/to/evidence.json>")
        sys.exit(1)

    json_path = sys.argv[1]
    success = render_report(json_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
