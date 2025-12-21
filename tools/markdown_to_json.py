"""
CDM Research Protocol - Markdown to JSON Converter v2.0

Parses evidence blocks from agent Markdown output and generates evidence.json.
This bridges the gap between agent-produced Markdown files and the Python
verification pipeline that expects JSON input.

Supports two evidence formats:

1. Fenced code blocks (legacy):
```evidence
id: E001
claim: Bank X announced CDM pilot
source_url: https://example.com/announcement
tier: 1
claim_type: pilot_or_poc
```

2. Markdown headers (current agent output):
### Evidence Block 1
**Source**: FINOS Press Release
**URL**: https://finos.org/press/...
**Date**: 2024-06-15
**Tier**: 1
**Finding**: Deutsche Bank participated in...
**Direction**: ARCHITECT

Usage:
    python markdown_to_json.py <tier1-evidence.md> [tier2-evidence.md ...] <output/evidence.json>
    python markdown_to_json.py <bank_directory>  # Auto-discovers tier*-evidence.md files
    python markdown_to_json.py --dry-run <input> <output>
"""

import re
import json
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, TYPE_CHECKING

# Type hint for optional EvidenceRegistry import
if TYPE_CHECKING:
    from evidence_dedup import EvidenceRegistry

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- PATTERNS ---
# Match evidence blocks: ```evidence ... ``` (case insensitive) - Legacy format
EVIDENCE_BLOCK_PATTERN = re.compile(
    r'```evidence\s*\n(.*?)```',
    re.DOTALL | re.IGNORECASE
)

# Match key: value lines (handles multi-line excerpts) - Legacy format
KEY_VALUE_PATTERN = re.compile(r'^([a-z_]+):\s*(.+)$', re.MULTILINE | re.IGNORECASE)

# NEW: Match markdown header evidence blocks: ### Evidence Block N
MD_EVIDENCE_HEADER = re.compile(
    r'^###\s+Evidence\s+Block\s+(\d+)',
    re.MULTILINE | re.IGNORECASE
)

# NEW: Match **Field**: Value patterns in markdown
MD_FIELD_PATTERNS = {
    'source': re.compile(r'\*\*Source\*\*:\s*(.+?)(?=\n\*\*|\n---|\n###|\Z)', re.DOTALL),
    'url': re.compile(r'\*\*URL\*\*:\s*(https?://[^\s\)]+)'),
    'date': re.compile(r'\*\*Date\*\*:\s*([^\n]+)'),
    'source_type': re.compile(r'\*\*Source\s*Type\*\*:\s*([^\n]+)'),
    'tier': re.compile(r'\*\*Tier\*\*:\s*(\d+)'),
    'finding': re.compile(r'\*\*Finding\*\*:\s*(.+?)(?=\n\*\*Interpretation|\n\*\*Strength|\n---|\n###|\Z)', re.DOTALL),
    'interpretation': re.compile(r'\*\*Interpretation\*\*:\s*(.+?)(?=\n\*\*Strength|\n\*\*Direction|\n---|\n###|\Z)', re.DOTALL),
    'strength': re.compile(r'\*\*Strength\*\*:\s*(Strong|Moderate|Weak)', re.IGNORECASE),
    'direction': re.compile(r'\*\*Direction\*\*:\s*(ARCHITECT|PRAGMATIST|NEUTRAL|OBSERVER)', re.IGNORECASE),
}

# Keywords for inferring claim_type from findings
CLAIM_TYPE_KEYWORDS = {
    'production_usage': ['production', 'live', 'deployed', 'in production', 'running'],
    'pilot_or_poc': ['pilot', 'poc', 'proof of concept', 'prototype', 'trial', 'testing'],
    'open_source_contribution': ['commit', 'contributor', 'github', 'finos', 'contributed', 'open source'],
    'membership_or_participation': ['member', 'working group', 'participant', 'board', 'joined', 'governance'],
    'vendor_proxy_signal': ['vendor', 'partner', 'client', 'supplier', 'platform'],
    'hiring_signal': ['job', 'hiring', 'career', 'position', 'recruiting'],
}

# Valid tiers
VALID_TIERS = {1, 2, 3, 4}

# Valid claim types
VALID_CLAIM_TYPES = {
    'production_usage',
    'pilot_or_poc',
    'membership_or_participation',
    'open_source_contribution',
    'vendor_proxy_signal',
    'hiring_signal'
}

# Required fields
REQUIRED_FIELDS = {'id', 'claim', 'source_url', 'tier', 'claim_type'}


def parse_evidence_block(block_text: str) -> dict:
    """
    Parse a single evidence block into a dict.

    Handles:
    - Key: value pairs
    - Multi-line excerpts (quoted strings)
    - Type conversion for tier (int)
    - Stripping of quotes from values
    """
    item = {}
    lines = block_text.strip().split('\n')

    current_key = None
    current_value = []

    for line in lines:
        line = line.rstrip()

        # Check if this line starts a new key
        if ':' in line and not line.startswith(' ') and not line.startswith('\t'):
            # Save previous key if exists
            if current_key:
                item[current_key] = '\n'.join(current_value).strip()

            # Parse new key-value
            key, value = line.split(':', 1)
            current_key = key.strip().lower()
            current_value = [value.strip()]
        elif current_key:
            # Continuation of previous value (multi-line)
            current_value.append(line)

    # Save last key
    if current_key:
        item[current_key] = '\n'.join(current_value).strip()

    # Post-processing
    for key, value in item.items():
        # Strip surrounding quotes
        if value.startswith('"') and value.endswith('"'):
            item[key] = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            item[key] = value[1:-1]

    # Type conversion
    if 'tier' in item:
        try:
            item['tier'] = int(item['tier'])
        except ValueError:
            logger.warning(f"Invalid tier value: {item['tier']}, defaulting to 3")
            item['tier'] = 3

    return item


def infer_claim_type(finding: str, direction: str) -> str:
    """
    Infer claim_type from finding text and direction.
    Uses keyword matching with priority ordering.
    """
    if not finding:
        return 'membership_or_participation'

    finding_lower = finding.lower()

    # Priority order: production > pilot > open_source > membership > vendor > hiring
    for claim_type, keywords in CLAIM_TYPE_KEYWORDS.items():
        if any(kw in finding_lower for kw in keywords):
            return claim_type

    # Default based on direction
    if direction and direction.upper() == 'ARCHITECT':
        return 'membership_or_participation'
    elif direction and direction.upper() == 'PRAGMATIST':
        return 'vendor_proxy_signal'

    return 'membership_or_participation'


def parse_md_evidence_block(block_text: str, block_num: int, bank_id: str = '') -> dict:
    """
    Parse a markdown-format evidence block (### Evidence Block N).

    Args:
        block_text: The text content of the block
        block_num: The block number from the header
        bank_id: Bank identifier for generating evidence IDs

    Returns:
        Parsed evidence item dict
    """
    item = {}

    # Extract fields using patterns
    for field, pattern in MD_FIELD_PATTERNS.items():
        match = pattern.search(block_text)
        if match:
            value = match.group(1).strip()
            # Clean up multi-line values
            value = re.sub(r'\n+', ' ', value).strip()
            item[field] = value

    # Generate ID from bank_id and block number
    prefix = bank_id.upper().replace('-', '')[:3] if bank_id else 'E'
    item['id'] = f"{prefix}-{block_num:03d}"

    # Map 'url' to 'source_url'
    if 'url' in item:
        item['source_url'] = item.pop('url')

    # Map 'finding' to 'claim'
    if 'finding' in item:
        item['claim'] = item['finding']

    # Parse tier as int
    if 'tier' in item:
        try:
            item['tier'] = int(item['tier'])
        except ValueError:
            item['tier'] = 2  # Default to Tier 2
    else:
        item['tier'] = 2  # Default

    # Infer claim_type if not present
    if 'claim_type' not in item:
        direction = item.get('direction', '')
        finding = item.get('finding', item.get('claim', ''))
        item['claim_type'] = infer_claim_type(finding, direction)

    # Parse date - try to normalize
    if 'date' in item:
        date_str = item['date']
        # Handle year-only dates
        if re.match(r'^\d{4}$', date_str):
            item['date'] = f"{date_str}-06-15"  # Mid-year estimate
        # Handle month-year dates
        elif re.match(r'^[A-Za-z]+\s+\d{4}$', date_str):
            try:
                from datetime import datetime as dt
                parsed = dt.strptime(date_str, "%B %Y")
                item['date'] = parsed.strftime("%Y-%m-15")
            except ValueError:
                pass  # Leave date unparsed if format doesn't match

    return item


def parse_markdown_header_format(content: str, bank_id: str = '') -> list[dict]:
    """
    Parse evidence from markdown header format (### Evidence Block N).

    Args:
        content: Full markdown file content
        bank_id: Bank identifier for generating evidence IDs

    Returns:
        List of parsed evidence items
    """
    items = []

    # Find all evidence block headers
    headers = list(MD_EVIDENCE_HEADER.finditer(content))

    if not headers:
        return []

    for i, match in enumerate(headers):
        block_num = int(match.group(1))
        start = match.end()

        # Find end of this block (next header or end of file)
        if i + 1 < len(headers):
            end = headers[i + 1].start()
        else:
            # Look for end markers
            end_match = re.search(r'\n##\s+Summary|\n---\s*\n##|\Z', content[start:])
            end = start + (end_match.start() if end_match else len(content) - start)

        block_text = content[start:end]

        try:
            item = parse_md_evidence_block(block_text, block_num, bank_id)
            items.append(item)
        except Exception as e:
            logger.warning(f"Failed to parse Evidence Block {block_num}: {e}")

    return items


def validate_evidence_item(item: dict) -> tuple[bool, list[str]]:
    """
    Validate an evidence item has all required fields and valid values.

    Returns:
        (is_valid, list_of_errors)
    """
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in item or not item[field]:
            errors.append(f"Missing required field: {field}")

    # Validate tier
    if 'tier' in item and item['tier'] not in VALID_TIERS:
        errors.append(f"Invalid tier: {item['tier']} (must be 1-4)")

    # Validate claim_type
    if 'claim_type' in item and item['claim_type'] not in VALID_CLAIM_TYPES:
        errors.append(f"Invalid claim_type: {item['claim_type']}")

    # Validate source_url format
    if 'source_url' in item:
        url = item['source_url']
        if not url.startswith(('http://', 'https://')):
            errors.append(f"Invalid source_url (must be http/https): {url[:50]}...")

    # Validate ID format (alphanumeric, underscore, hyphen)
    if 'id' in item:
        if not re.match(r'^[a-zA-Z0-9_-]+$', item['id']):
            errors.append(f"Invalid ID format: {item['id']} (only alphanumeric, underscore, hyphen)")

    return (len(errors) == 0, errors)


def parse_markdown_file(md_path: Path, bank_id: str = '') -> list[dict]:
    """
    Extract all evidence blocks from a Markdown file.
    Tries both legacy fenced format and markdown header format.

    Args:
        md_path: Path to the Markdown file
        bank_id: Bank identifier for generating evidence IDs

    Returns:
        List of parsed evidence items
    """
    if not md_path.exists():
        logger.error(f"File not found: {md_path}")
        return []

    content = md_path.read_text(encoding='utf-8')

    # Try markdown header format first (current agent output)
    items = parse_markdown_header_format(content, bank_id)

    if items:
        logger.info(f"  Parsed {len(items)} items using markdown header format")
    else:
        # Fall back to legacy fenced code block format
        blocks = EVIDENCE_BLOCK_PATTERN.findall(content)
        for i, block in enumerate(blocks):
            try:
                item = parse_evidence_block(block)
                items.append(item)
            except Exception as e:
                logger.error(f"Failed to parse block {i+1} in {md_path.name}: {e}")

        if items:
            logger.info(f"  Parsed {len(items)} items using legacy fenced format")

    # Validate all items
    for item in items:
        is_valid, errors = validate_evidence_item(item)
        if not is_valid:
            logger.warning(f"Item {item.get('id')} has validation errors:")
            for error in errors:
                logger.warning(f"  - {error}")
            item['_validation_errors'] = errors

    return items


def merge_into_evidence_json(
    evidence_items: list,
    json_path: Path,
    registry: 'EvidenceRegistry' = None
) -> dict:
    """
    Merge new items into existing evidence.json or create new.

    Merging strategy:
    - If registry provided, filter duplicates first (Category 6 fix)
    - If item ID exists, update the existing item
    - If item ID is new, append to the list
    - Preserves verification/content data from existing items

    Args:
        evidence_items: List of new evidence items
        json_path: Path to evidence.json
        registry: Optional EvidenceRegistry for deduplication

    Returns:
        Updated evidence data dict
    """
    # Apply deduplication if registry provided (Category 6 fix)
    if registry is not None:
        bank_id = json_path.parent.name
        original_count = len(evidence_items)
        evidence_items = registry.dedup_list(evidence_items, bank_id)
        if len(evidence_items) < original_count:
            logger.info(
                f"Deduplication removed {original_count - len(evidence_items)} items, "
                f"{len(evidence_items)} remaining"
            )
    if json_path.exists():
        try:
            data = json.loads(json_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {json_path}: {e}")
            logger.info("Creating new evidence.json")
            data = None
    else:
        data = None

    if data is None:
        data = {
            "bank_id": json_path.parent.name,
            "created_at": datetime.utcnow().isoformat(),
            "evidence_items": []
        }

    # Build index of existing items by ID
    existing_ids = {}
    for i, item in enumerate(data.get('evidence_items', [])):
        item_id = item.get('id')
        if item_id:
            existing_ids[item_id] = i

    # Merge new items
    for new_item in evidence_items:
        new_id = new_item.get('id')
        if not new_id:
            logger.warning("Skipping item without ID")
            continue

        if new_id in existing_ids:
            # Update existing item, preserving verification data
            idx = existing_ids[new_id]
            existing = data['evidence_items'][idx]

            # Preserve these fields from existing
            preserved_fields = ['verification', 'content', 'freshness']
            for field in preserved_fields:
                if field in existing and field not in new_item:
                    new_item[field] = existing[field]

            data['evidence_items'][idx] = new_item
            logger.info(f"Updated existing item: {new_id}")
        else:
            data['evidence_items'].append(new_item)
            logger.info(f"Added new item: {new_id}")

    data['updated_at'] = datetime.utcnow().isoformat()
    data['item_count'] = len(data['evidence_items'])

    return data


def convert_bank_directory(bank_dir: Path) -> dict:
    """
    Convert all evidence Markdown files in a bank directory to JSON.

    Args:
        bank_dir: Path to bank directory (e.g., outputs/phase-1/deutsche-bank)

    Returns:
        Evidence data dict ready for JSON serialization
    """
    evidence_dir = bank_dir / '1-evidence'
    if not evidence_dir.exists():
        raise FileNotFoundError(f"Evidence directory not found: {evidence_dir}")

    # Get bank metadata from status.json if available
    status_path = bank_dir / 'status.json'
    if status_path.exists():
        try:
            status = json.loads(status_path.read_text(encoding='utf-8'))
            bank_name = status.get('bank_name', bank_dir.name.replace('-', ' ').title())
            bank_id = status.get('bank_id', bank_dir.name)
        except json.JSONDecodeError:
            bank_name = bank_dir.name.replace('-', ' ').title()
            bank_id = bank_dir.name
    else:
        bank_name = bank_dir.name.replace('-', ' ').title()
        bank_id = bank_dir.name

    # Parse all tier evidence files
    all_evidence = []
    source_files = []

    for tier in [1, 2, 3]:
        tier_file = evidence_dir / f'tier{tier}-evidence.md'
        if tier_file.exists():
            items = parse_markdown_file(tier_file, bank_id)
            # Ensure tier is set correctly
            for item in items:
                if 'tier' not in item or item['tier'] != tier:
                    item['tier'] = tier
            all_evidence.extend(items)
            source_files.append(tier_file.name)
            logger.info(f"Parsed {len(items)} items from {tier_file.name}")

    return {
        'bank_id': bank_id,
        'bank_name': bank_name,
        'schema_version': '3.0',
        'generated_from': 'markdown',
        'generated_at': datetime.utcnow().isoformat(),
        'evidence_items': all_evidence,
        'item_count': len(all_evidence),
        'meta': {
            'source_files': source_files,
            'converter_version': '2.0'
        }
    }


def convert_with_dedup(
    bank_dir: Path,
    registry: 'EvidenceRegistry' = None
) -> dict:
    """
    Convert bank directory with optional deduplication.

    Convenience function that combines convert_bank_directory with dedup.

    Args:
        bank_dir: Path to bank directory
        registry: Optional EvidenceRegistry for deduplication

    Returns:
        Evidence data dict (deduplicated if registry provided)
    """
    data = convert_bank_directory(bank_dir)

    if registry is not None:
        bank_id = data.get('bank_id', bank_dir.name)
        original_count = len(data['evidence_items'])
        data['evidence_items'] = registry.dedup_list(
            data['evidence_items'],
            bank_id
        )
        dedup_count = original_count - len(data['evidence_items'])
        if dedup_count > 0:
            logger.info(f"Deduplication removed {dedup_count} items")
        data['item_count'] = len(data['evidence_items'])

    return data


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_json.py <bank_directory>")
        print("       python markdown_to_json.py <tier1-evidence.md> [tier2.md ...] <output/evidence.json>")
        print("       python markdown_to_json.py --dry-run <bank_directory>")
        print("       python markdown_to_json.py --dedup <bank_directory>")
        print("\nOptions:")
        print("  --dry-run    Preview output without writing files")
        print("  --dedup      Enable global deduplication registry")
        print("\nExamples:")
        print("  python markdown_to_json.py outputs/phase-1-european-tier1/deutsche-bank/")
        print("  python markdown_to_json.py --dedup outputs/phase-1-european-tier1/deutsche-bank/")
        print("  python markdown_to_json.py outputs/bank/1-evidence/*.md outputs/bank/evidence.json")
        sys.exit(1)

    # Handle flags
    dry_run = False
    use_dedup = False
    args = sys.argv[1:]

    while args and args[0].startswith('--'):
        if args[0] == '--dry-run':
            dry_run = True
            args = args[1:]
            logger.info("DRY RUN MODE - no files will be modified")
        elif args[0] == '--dedup':
            use_dedup = True
            args = args[1:]
            logger.info("DEDUP MODE - using global evidence registry")
        else:
            print(f"Unknown flag: {args[0]}")
            sys.exit(1)

    # Initialize dedup registry if enabled
    registry = None
    if use_dedup:
        try:
            from evidence_dedup import get_default_registry
            registry = get_default_registry()
            logger.info(f"Loaded evidence registry with {len(registry.registry)} existing items")
        except ImportError as e:
            logger.error(f"Could not import evidence_dedup: {e}")
            logger.error("Continuing without deduplication")
            registry = None

    if len(args) < 1:
        print("Error: Need at least one argument (bank directory or markdown files)")
        sys.exit(1)

    # Check if first argument is a directory (bank directory mode)
    first_path = Path(args[0])
    if first_path.is_dir() and (first_path / '1-evidence').exists():
        # Directory mode: convert entire bank directory
        bank_dir = first_path
        json_path = bank_dir / 'evidence.json'

        logger.info(f"Converting bank directory: {bank_dir}")

        try:
            # Use dedup-enabled conversion if registry available
            if registry is not None:
                data = convert_with_dedup(bank_dir, registry)
            else:
                data = convert_bank_directory(bank_dir)
        except FileNotFoundError as e:
            logger.error(str(e))
            sys.exit(1)

        if not data['evidence_items']:
            logger.warning("No evidence items found in any source files")

        # Summary
        logger.info(f"\nSummary:")
        logger.info(f"  Bank: {data['bank_name']}")
        logger.info(f"  Total items: {len(data['evidence_items'])}")

        # Count by tier
        tier_counts = {}
        for item in data['evidence_items']:
            tier = item.get('tier', 'unknown')
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        for tier, count in sorted(tier_counts.items()):
            logger.info(f"  Tier {tier}: {count} items")

        if dry_run:
            logger.info("\nDRY RUN - would write to: " + str(json_path))
            print("\n--- Preview of output ---")
            print(json.dumps(data, indent=2)[:2000])
            if len(json.dumps(data)) > 2000:
                print("... (truncated)")
        else:
            json_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
            logger.info(f"\nWrote {len(data['evidence_items'])} items to {json_path}")

    else:
        # Legacy mode: explicit markdown files and output path
        if len(args) < 2:
            print("Error: Need at least one markdown file and one output path")
            sys.exit(1)

        # Last argument is output path, rest are input markdown files
        json_path = Path(args[-1])
        md_paths = [Path(p) for p in args[:-1]]

        # Ensure output directory exists
        json_path.parent.mkdir(parents=True, exist_ok=True)

        # Parse all markdown files
        all_items = []
        for md_path in md_paths:
            logger.info(f"Parsing {md_path}...")
            items = parse_markdown_file(md_path)
            logger.info(f"  Found {len(items)} evidence items")
            all_items.extend(items)

        if not all_items:
            logger.warning("No evidence items found in any input files")
            if not dry_run:
                # Still create empty evidence.json
                data = {
                    "bank_id": json_path.parent.name,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "evidence_items": [],
                    "item_count": 0
                }
                json_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
                logger.info(f"Created empty evidence.json at {json_path}")
            sys.exit(0)

        # Merge into evidence.json
        data = merge_into_evidence_json(all_items, json_path)

        # Summary
        logger.info(f"\nSummary:")
        logger.info(f"  Total items: {len(data['evidence_items'])}")

        # Count by tier
        tier_counts = {}
        for item in data['evidence_items']:
            tier = item.get('tier', 'unknown')
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        for tier, count in sorted(tier_counts.items()):
            logger.info(f"  Tier {tier}: {count} items")

        # Count validation errors
        error_count = sum(1 for item in data['evidence_items'] if '_validation_errors' in item)
        if error_count > 0:
            logger.warning(f"  Items with validation errors: {error_count}")

        if dry_run:
            logger.info("\nDRY RUN - would write to: " + str(json_path))
            print("\n--- Preview of output ---")
            print(json.dumps(data, indent=2)[:2000])
            if len(json.dumps(data)) > 2000:
                print("... (truncated)")
        else:
            json_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
            logger.info(f"\nWrote {len(data['evidence_items'])} items to {json_path}")


if __name__ == "__main__":
    main()
