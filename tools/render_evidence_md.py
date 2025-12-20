"""
CDM Research Protocol - Evidence JSON to Markdown Renderer v1.0

Renders evidence.json to human-readable Markdown files.
This is the reverse of markdown_to_json.py.

Per CLAUDE.md Ledger-First mandate:
- evidence.json is the PRIMARY output (source of truth)
- Markdown files are SECONDARY (rendered views for human readability)

Outputs:
- tier1-evidence.md, tier2-evidence.md, tier3-evidence.md
- null-results.md

Usage:
    python render_evidence_md.py <evidence.json>
    python render_evidence_md.py <bank_directory>
    python render_evidence_md.py --batch <phase_directory>
"""

import json
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def render_evidence_block(item: dict) -> str:
    """Render a single evidence item to Markdown block format."""

    # Determine direction label
    direction = item.get('direction', 'NEUTRAL')
    if direction == 'SUPPORTS_ARCHITECT':
        direction_label = 'SUPPORTS ARCHITECT'
    elif direction == 'SUPPORTS_PRAGMATIST':
        direction_label = 'SUPPORTS PRAGMATIST'
    else:
        direction_label = 'NEUTRAL'

    # Get quality assessment
    qa = item.get('quality_assessment', {})
    authority = qa.get('authority', 'MEDIUM')
    recency = qa.get('recency', 'current').title()
    specificity = qa.get('specificity', 'moderate').title()

    # Get LR mapping
    lr_mapping = item.get('lr_mapping', {})
    lr_type = lr_mapping.get('evidence_type', 'unknown')
    lr_value = lr_mapping.get('likelihood_ratio', 1.0)

    # Build the block
    lines = [
        f"[{item.get('id', 'UNKNOWN')}] TIER {item.get('tier', '?')} — {direction_label}",
        "",
        f"**Source**: {item.get('source_url', 'No URL provided')}",
        f"**Date**: {item.get('date', 'Unknown')}",
        "",
        f"**Finding**: \"{item.get('excerpt', item.get('claim', 'No finding recorded'))}\"",
        "",
        "**Quality Assessment**:",
        f"- Authority: {authority}",
        f"- Recency: {recency}",
        f"- Specificity: {specificity}",
        "",
        f"**Claim Type**: `{item.get('claim_type', 'unknown')}`",
        f"**LR Mapping**: {lr_type} (LR = {lr_value})",
        "",
    ]

    if item.get('caveats'):
        lines.append(f"**Caveats**: {item['caveats']}")
        lines.append("")

    lines.append("---")

    return "\n".join(lines)


def render_null_result_block(null_item: dict) -> str:
    """Render a single null result to Markdown block format."""

    lines = [
        f"### {null_item.get('category', 'Unknown Category')}",
        "",
        "**Queries Executed**:",
    ]

    for query in null_item.get('queries', []):
        lines.append(f"- `{query}`")

    lines.extend([
        "",
        f"**Results Reviewed**: {null_item.get('results_reviewed', 0)}",
        f"**Null Classification**: {null_item.get('null_type', 'UNKNOWN')}",
        "",
        f"**Informative Absence**: {'YES' if null_item.get('informative_absence') else 'NO'}",
        "",
        f"**Implication**: {null_item.get('implication', 'No implication recorded')}",
        "",
        "---",
    ])

    return "\n".join(lines)


def render_tier_evidence(evidence_json: dict, tier: int) -> Optional[str]:
    """
    Render evidence items for a specific tier to Markdown format.
    Returns None if no evidence exists for this tier.
    """

    # Filter items for this tier
    tier_items = [
        item for item in evidence_json.get('evidence_items', [])
        if item.get('tier') == tier
    ]

    if not tier_items:
        return None

    bank_name = evidence_json.get('bank_name', 'Unknown Bank')
    meta = evidence_json.get('meta', {})

    # Build header
    lines = [
        f"# Tier {tier} Evidence: {bank_name}",
        "",
        "## Search Execution Summary",
        "",
        f"- **Date**: {meta.get('generated_at', datetime.now().isoformat())[:10]}",
        f"- **Evidence Blocks Found**: {len(tier_items)}",
        f"- **Schema Version**: {evidence_json.get('schema_version', '3.1')}",
        "",
        "---",
        "",
        "## Evidence Inventory",
        "",
    ]

    # Render each evidence block
    for item in tier_items:
        lines.append(render_evidence_block(item))
        lines.append("")

    return "\n".join(lines)


def render_null_results(evidence_json: dict) -> Optional[str]:
    """
    Render null results to Markdown format.
    Returns None if no null results exist.
    """

    null_results = evidence_json.get('null_results', [])

    if not null_results:
        return None

    bank_name = evidence_json.get('bank_name', 'Unknown Bank')

    # Count informative absences
    informative_count = sum(1 for n in null_results if n.get('informative_absence'))

    lines = [
        f"# Null Results: {bank_name}",
        "",
        "## Summary",
        "",
        f"- **Total Search Categories**: {len(null_results)}",
        f"- **Categories with Null Results**: {len(null_results)}",
        f"- **Informative Absences**: {informative_count}",
        "",
        "---",
        "",
        "## Null Result Blocks",
        "",
    ]

    for null_item in null_results:
        lines.append(render_null_result_block(null_item))
        lines.append("")

    # Summary section
    lines.extend([
        "## Null Results Summary",
        "",
        f"- Total null searches: {len(null_results)}",
        f"- Informative absences supporting Pragmatist: {informative_count}",
        f"- Search exhaustiveness: {'Exhaustive' if len(null_results) >= 10 else 'Thorough' if len(null_results) >= 5 else 'Basic'}",
    ])

    return "\n".join(lines)


def render_all(json_path: Path) -> dict:
    """
    Render all tiers and null results from evidence.json.
    Creates Markdown files in the appropriate locations.

    Returns dict with status of each file rendered.
    """

    json_path = Path(json_path)

    if not json_path.exists():
        logger.error(f"Evidence file not found: {json_path}")
        return {'error': f'File not found: {json_path}'}

    # Load evidence JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            evidence_json = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {json_path}: {e}")
        return {'error': f'Invalid JSON: {e}'}

    # Determine output directory
    bank_dir = json_path.parent
    evidence_dir = bank_dir / '1-evidence'
    evidence_dir.mkdir(parents=True, exist_ok=True)

    results = {
        'bank_id': evidence_json.get('bank_id', 'unknown'),
        'bank_name': evidence_json.get('bank_name', 'Unknown'),
        'files_rendered': [],
        'files_skipped': []
    }

    # Render each tier
    for tier in [1, 2, 3]:
        content = render_tier_evidence(evidence_json, tier)
        if content:
            output_path = evidence_dir / f'tier{tier}-evidence.md'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            results['files_rendered'].append(str(output_path))
            logger.info(f"Rendered: {output_path}")
        else:
            results['files_skipped'].append(f'tier{tier}-evidence.md (no tier {tier} evidence)')

    # Render null results
    null_content = render_null_results(evidence_json)
    if null_content:
        output_path = evidence_dir / 'null-results.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(null_content)
        results['files_rendered'].append(str(output_path))
        logger.info(f"Rendered: {output_path}")
    else:
        results['files_skipped'].append('null-results.md (no null results)')

    return results


def render_bank_directory(bank_dir: Path) -> dict:
    """
    Render evidence.json from a bank directory.
    """
    bank_dir = Path(bank_dir)
    json_path = bank_dir / 'evidence.json'

    if not json_path.exists():
        logger.warning(f"No evidence.json found in {bank_dir}")
        return {'error': f'No evidence.json in {bank_dir}'}

    return render_all(json_path)


def render_batch(phase_dir: Path) -> dict:
    """
    Render evidence.json for all banks in a phase directory.
    """
    phase_dir = Path(phase_dir)

    if not phase_dir.is_dir():
        logger.error(f"Not a directory: {phase_dir}")
        return {'error': f'Not a directory: {phase_dir}'}

    results = {
        'phase': phase_dir.name,
        'banks_processed': [],
        'banks_skipped': []
    }

    for bank_dir in sorted(phase_dir.iterdir()):
        if not bank_dir.is_dir():
            continue

        json_path = bank_dir / 'evidence.json'
        if json_path.exists():
            bank_result = render_all(json_path)
            results['banks_processed'].append({
                'bank_id': bank_dir.name,
                'result': bank_result
            })
        else:
            results['banks_skipped'].append(bank_dir.name)

    return results


def main():
    """Main entry point."""

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Check for batch mode
    if sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print("Usage: python render_evidence_md.py --batch <phase_directory>")
            sys.exit(1)

        phase_dir = Path(sys.argv[2])
        results = render_batch(phase_dir)
        print(json.dumps(results, indent=2))
        return

    input_path = Path(sys.argv[1])

    if input_path.is_file() and input_path.suffix == '.json':
        # Direct JSON file
        results = render_all(input_path)
    elif input_path.is_dir():
        # Bank directory
        results = render_bank_directory(input_path)
    else:
        logger.error(f"Invalid input: {input_path}")
        print(f"Error: {input_path} is not a valid JSON file or directory")
        sys.exit(1)

    # Print results
    print(json.dumps(results, indent=2))

    if 'error' in results:
        sys.exit(1)


if __name__ == '__main__':
    main()
