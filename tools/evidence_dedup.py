"""
CDM Research Protocol - Evidence Deduplication

Category 6 fix: Duplicate Evidence IDs on Re-run
Prevents duplicate evidence items using content-based hashing.

Uses GLOBAL registry (user preference) - prevents same evidence appearing
across ALL banks, not just within one bank.

Registry stored at: outputs/state/evidence-registry.json

Usage:
    from evidence_dedup import EvidenceRegistry, generate_evidence_hash

    # Initialize registry
    registry = EvidenceRegistry(Path("outputs/state/evidence-registry.json"))

    # Check if duplicate
    if registry.is_duplicate(evidence_item):
        print("Already seen this evidence")

    # Register new item
    registry.register(evidence_item, bank_id="deutsche-bank")

    # Deduplicate a list
    unique_items = registry.dedup_list(items, bank_id="deutsche-bank")
"""

import hashlib
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


def normalize_url(url: str) -> str:
    """
    Normalize URL for consistent hashing.

    - Converts to lowercase
    - Removes trailing slashes
    - Strips common tracking parameters
    - Removes fragments

    Args:
        url: Source URL to normalize

    Returns:
        Normalized URL string
    """
    if not url:
        return ""

    normalized = url.lower().rstrip('/')

    # Remove tracking parameters
    tracking_params = ['?utm_', '&utm_', '?ref=', '&ref=', '?source=', '&source=']
    for param in tracking_params:
        if param in normalized:
            normalized = normalized.split(param)[0]

    # Remove fragment identifiers
    if '#' in normalized:
        normalized = normalized.split('#')[0]

    return normalized


def generate_evidence_hash(item: Dict[str, Any]) -> str:
    """
    Generate deterministic hash from content-significant fields.

    Ignores metadata like timestamps, IDs, and verification status.
    Uses fields that represent the actual evidence content.

    Hash components:
    - source_url (normalized)
    - tier
    - claim_type
    - claim text (first 200 chars, normalized)

    Args:
        item: Evidence item dictionary

    Returns:
        16-character hex hash string
    """
    # Normalize URL
    url = normalize_url(item.get('source_url', ''))

    # Get core content fields
    tier = str(item.get('tier', 0))
    claim_type = item.get('claim_type', '').lower().strip()
    claim = item.get('claim', '')[:200].lower().strip()

    # Build hash input with delimiters
    hash_input = '|'.join([url, tier, claim_type, claim])

    # Generate SHA-256 and truncate to 16 chars for readability
    full_hash = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
    return full_hash[:16]


class EvidenceRegistry:
    """
    Global registry to track evidence and prevent duplicates.

    Thread-safe with atomic file writes.
    Registry persists across runs at: outputs/state/evidence-registry.json

    Attributes:
        registry_path: Path to the registry JSON file
        registry: Dict mapping content_hash -> metadata
    """

    def __init__(self, registry_path: Path):
        """
        Initialize or load existing registry.

        Args:
            registry_path: Path to store the registry JSON file
        """
        self.registry_path = registry_path
        self.registry: Dict[str, Dict[str, Any]] = {}

        # Ensure parent directory exists
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        self._load()

    def _load(self) -> None:
        """Load registry from disk if it exists."""
        if self.registry_path.exists():
            try:
                data = json.loads(self.registry_path.read_text(encoding='utf-8'))
                self.registry = data.get('items', {})
                logger.debug(f"Loaded evidence registry with {len(self.registry)} items")
            except Exception as e:
                logger.warning(f"Could not load evidence registry: {e}")
                self.registry = {}

    def _save(self) -> None:
        """Atomically save registry to disk."""
        data = {
            "version": "1.0",
            "description": "Global evidence deduplication registry",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "item_count": len(self.registry),
            "items": self.registry
        }

        # Atomic write: write to temp, then rename
        temp_path = self.registry_path.with_suffix('.tmp')
        try:
            temp_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
            temp_path.replace(self.registry_path)
        except Exception as e:
            logger.error(f"Failed to save evidence registry: {e}")
            raise

    def is_duplicate(self, item: Dict[str, Any]) -> bool:
        """
        Check if evidence item is already registered.

        Args:
            item: Evidence item dictionary

        Returns:
            True if item (by content hash) already exists in registry
        """
        content_hash = generate_evidence_hash(item)
        return content_hash in self.registry

    def get_existing(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get existing registry entry for an item if it exists.

        Args:
            item: Evidence item dictionary

        Returns:
            Registry entry dict if exists, None otherwise
        """
        content_hash = generate_evidence_hash(item)
        return self.registry.get(content_hash)

    def register(self, item: Dict[str, Any], bank_id: str) -> str:
        """
        Register a new evidence item.

        Does nothing if item already exists (idempotent).

        Args:
            item: Evidence item dictionary
            bank_id: Bank this evidence was found for

        Returns:
            Content hash of the item
        """
        content_hash = generate_evidence_hash(item)

        if content_hash not in self.registry:
            self.registry[content_hash] = {
                "id": item.get('id'),
                "bank_id": bank_id,
                "tier": item.get('tier'),
                "claim_type": item.get('claim_type'),
                "source_url": item.get('source_url', '')[:100],  # Truncate for readability
                "added_at": datetime.now(timezone.utc).isoformat()
            }
            self._save()
            logger.debug(f"Registered new evidence: {content_hash}")

        return content_hash

    def dedup_list(
        self,
        items: List[Dict[str, Any]],
        bank_id: str,
        log_duplicates: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicates from a list of evidence items.

        Registers unique items and returns only non-duplicate items.

        Args:
            items: List of evidence item dictionaries
            bank_id: Bank this evidence was found for
            log_duplicates: Whether to log duplicate detection

        Returns:
            List containing only unique (non-duplicate) items
        """
        unique = []
        duplicate_count = 0

        for item in items:
            if self.is_duplicate(item):
                duplicate_count += 1
                if log_duplicates:
                    existing = self.get_existing(item)
                    original_bank = existing.get('bank_id', 'unknown') if existing else 'unknown'
                    logger.debug(
                        f"Skipping duplicate evidence (first seen in {original_bank}): "
                        f"{item.get('source_url', '')[:50]}"
                    )
            else:
                self.register(item, bank_id)
                unique.append(item)

        if duplicate_count > 0:
            logger.info(f"Deduplicated {duplicate_count} items, {len(unique)} unique remaining")

        return unique

    def get_stats(self) -> Dict[str, Any]:
        """
        Get registry statistics.

        Returns:
            Dict with counts and breakdown by bank/tier
        """
        by_bank: Dict[str, int] = {}
        by_tier: Dict[int, int] = {}

        for entry in self.registry.values():
            bank = entry.get('bank_id', 'unknown')
            tier = entry.get('tier', 0)

            by_bank[bank] = by_bank.get(bank, 0) + 1
            by_tier[tier] = by_tier.get(tier, 0) + 1

        return {
            "total_items": len(self.registry),
            "by_bank": by_bank,
            "by_tier": by_tier,
            "registry_path": str(self.registry_path)
        }

    def clear(self) -> None:
        """
        Clear all entries from the registry.

        Use with caution - typically only for testing or fresh starts.
        """
        self.registry = {}
        self._save()
        logger.info("Evidence registry cleared")

    def remove_bank(self, bank_id: str) -> int:
        """
        Remove all entries for a specific bank.

        Useful when re-running research for a single bank.

        Args:
            bank_id: Bank identifier to remove

        Returns:
            Number of entries removed
        """
        to_remove = [
            hash_key for hash_key, entry in self.registry.items()
            if entry.get('bank_id') == bank_id
        ]

        for hash_key in to_remove:
            del self.registry[hash_key]

        if to_remove:
            self._save()
            logger.info(f"Removed {len(to_remove)} entries for bank: {bank_id}")

        return len(to_remove)


def get_default_registry() -> EvidenceRegistry:
    """
    Get the default global evidence registry.

    Convenience function that uses the standard registry path.

    Returns:
        EvidenceRegistry instance at outputs/state/evidence-registry.json
    """
    default_path = Path(__file__).parent.parent / "outputs" / "state" / "evidence-registry.json"
    return EvidenceRegistry(default_path)


if __name__ == "__main__":
    # Simple CLI for registry management
    import argparse

    parser = argparse.ArgumentParser(description="Evidence Registry Management")
    parser.add_argument('--stats', action='store_true', help="Show registry statistics")
    parser.add_argument('--clear', action='store_true', help="Clear all entries")
    parser.add_argument('--remove-bank', type=str, help="Remove entries for specific bank")

    args = parser.parse_args()

    registry = get_default_registry()

    if args.stats:
        stats = registry.get_stats()
        print(f"\nEvidence Registry Statistics")
        print(f"{'='*40}")
        print(f"Total items: {stats['total_items']}")
        print(f"\nBy Bank:")
        for bank, count in sorted(stats['by_bank'].items()):
            print(f"  {bank}: {count}")
        print(f"\nBy Tier:")
        for tier, count in sorted(stats['by_tier'].items()):
            print(f"  Tier {tier}: {count}")

    elif args.clear:
        confirm = input("Are you sure you want to clear the registry? (yes/no): ")
        if confirm.lower() == 'yes':
            registry.clear()
            print("Registry cleared.")
        else:
            print("Cancelled.")

    elif args.remove_bank:
        removed = registry.remove_bank(args.remove_bank)
        print(f"Removed {removed} entries for bank: {args.remove_bank}")

    else:
        parser.print_help()
