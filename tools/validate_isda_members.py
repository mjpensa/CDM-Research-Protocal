#!/usr/bin/env python3
"""
ISDA Members Validation and Management Tool

Validates, normalizes, and manages ISDA CDM/DRR member registry.
Designed for population via Claude Code WebFetch during research sessions.

Usage:
    python validate_isda_members.py --validate
    python validate_isda_members.py --add-member "Deutsche Bank" --type cdm_working_group --source "https://..."
    python validate_isda_members.py --map-banks
    python validate_isda_members.py --stats
    python validate_isda_members.py --list --type cdm_steering
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
from difflib import SequenceMatcher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
KB_DIR = PROJECT_ROOT / "knowledge_base"
CONFIG_DIR = PROJECT_ROOT / "config"

ISDA_MEMBERS_FILE = KB_DIR / "isda_members.json"
BANK_MANIFEST_FILE = CONFIG_DIR / "bank-manifest.json"

# Valid membership types
VALID_MEMBERSHIP_TYPES = [
    "cdm_steering",
    "cdm_working_group",
    "drr_working_group",
    "drr_pilot",
    "isda_member_general"
]

# Valid organization types
VALID_ORG_TYPES = [
    "bank",
    "vendor",
    "ccp",
    "exchange",
    "regulator",
    "trade_repository",
    "consulting",
    "law_firm",
    "other"
]


@dataclass
class IsdaMember:
    """Represents an ISDA CDM/DRR member organization."""
    organization_name: str
    organization_type: str
    membership_type: str
    bank_id: Optional[str] = None
    source_url: Optional[str] = None
    source_date: Optional[str] = None
    added_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    confidence: str = "confirmed"
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict) -> 'IsdaMember':
        return cls(
            organization_name=data.get('organization_name', ''),
            organization_type=data.get('organization_type', 'other'),
            membership_type=data.get('membership_type', 'isda_member_general'),
            bank_id=data.get('bank_id'),
            source_url=data.get('source_url'),
            source_date=data.get('source_date'),
            added_at=data.get('added_at', datetime.now(timezone.utc).isoformat()),
            confidence=data.get('confidence', 'confirmed'),
            notes=data.get('notes')
        )


class IsdaMemberValidator:
    """Validates and manages ISDA member registry."""

    def __init__(self):
        self.data = self._load_registry()
        self.bank_manifest = self._load_bank_manifest()
        self.name_to_bank_id = self._build_name_mapping()

    def _load_registry(self) -> dict:
        """Load the ISDA members registry."""
        if not ISDA_MEMBERS_FILE.exists():
            logger.warning(f"Registry not found: {ISDA_MEMBERS_FILE}")
            return {"members": [], "source_urls": [], "statistics": {}}

        with open(ISDA_MEMBERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_bank_manifest(self) -> dict:
        """Load bank manifest for ID mapping."""
        if not BANK_MANIFEST_FILE.exists():
            logger.warning(f"Bank manifest not found: {BANK_MANIFEST_FILE}")
            return {"banks": {}}

        with open(BANK_MANIFEST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _build_name_mapping(self) -> Dict[str, str]:
        """Build a mapping from organization names to bank IDs."""
        mapping = {}

        banks = self.bank_manifest.get('banks', [])
        # Handle both list and dict formats
        if isinstance(banks, list):
            for bank_data in banks:
                bank_id = bank_data.get('bank_id', '')
                if not bank_id:
                    continue

                # Add primary name
                primary_name = bank_data.get('bank_name', '').lower()
                if primary_name:
                    mapping[primary_name] = bank_id

                # Add aliases if present
                for alias in bank_data.get('aliases', []):
                    mapping[alias.lower()] = bank_id

                # Add the bank_id itself
                mapping[bank_id.lower()] = bank_id
        else:
            # Dictionary format
            for bank_id, bank_data in banks.items():
                primary_name = bank_data.get('name', '').lower()
                if primary_name:
                    mapping[primary_name] = bank_id

                for alias in bank_data.get('aliases', []):
                    mapping[alias.lower()] = bank_id

                mapping[bank_id.lower()] = bank_id

        return mapping

    def _fuzzy_match_bank(self, org_name: str, threshold: float = 0.8) -> Optional[str]:
        """Fuzzy match organization name to bank ID."""
        org_lower = org_name.lower()

        # Exact match first
        if org_lower in self.name_to_bank_id:
            return self.name_to_bank_id[org_lower]

        # Fuzzy matching
        best_match = None
        best_score = 0

        for name, bank_id in self.name_to_bank_id.items():
            score = SequenceMatcher(None, org_lower, name).ratio()
            if score > best_score and score >= threshold:
                best_score = score
                best_match = bank_id

        return best_match

    def validate_schema(self) -> List[str]:
        """Validate the registry schema. Returns list of issues."""
        issues = []

        # Check required top-level keys
        required_keys = ['members', 'source_urls', 'statistics']
        for key in required_keys:
            if key not in self.data:
                issues.append(f"Missing required key: {key}")

        # Validate each member
        for i, member in enumerate(self.data.get('members', [])):
            # Check required fields
            if not member.get('organization_name'):
                issues.append(f"Member {i}: missing organization_name")

            if not member.get('membership_type'):
                issues.append(f"Member {i}: missing membership_type")
            elif member['membership_type'] not in VALID_MEMBERSHIP_TYPES:
                issues.append(f"Member {i}: invalid membership_type '{member['membership_type']}'")

            if not member.get('organization_type'):
                issues.append(f"Member {i}: missing organization_type")
            elif member['organization_type'] not in VALID_ORG_TYPES:
                issues.append(f"Member {i}: invalid organization_type '{member['organization_type']}'")

        return issues

    def add_member(
        self,
        org_name: str,
        membership_type: str,
        org_type: str = "bank",
        source_url: Optional[str] = None,
        source_date: Optional[str] = None,
        notes: Optional[str] = None,
        dry_run: bool = False
    ) -> tuple[bool, str]:
        """Add a new member to the registry."""

        # Validate membership type
        if membership_type not in VALID_MEMBERSHIP_TYPES:
            return False, f"Invalid membership type: {membership_type}. Valid: {VALID_MEMBERSHIP_TYPES}"

        # Validate org type
        if org_type not in VALID_ORG_TYPES:
            return False, f"Invalid organization type: {org_type}. Valid: {VALID_ORG_TYPES}"

        # Check for duplicates
        existing = [m for m in self.data.get('members', [])
                   if m.get('organization_name', '').lower() == org_name.lower()
                   and m.get('membership_type') == membership_type]
        if existing:
            return False, f"Duplicate: {org_name} already has {membership_type} membership"

        # Try to map to bank ID
        bank_id = self._fuzzy_match_bank(org_name) if org_type == "bank" else None

        # Create member
        member = IsdaMember(
            organization_name=org_name,
            organization_type=org_type,
            membership_type=membership_type,
            bank_id=bank_id,
            source_url=source_url,
            source_date=source_date,
            notes=notes
        )

        if dry_run:
            return True, f"[DRY RUN] Would add: {member.to_dict()}"

        # Add to registry
        self.data['members'].append(member.to_dict())

        # Add source URL if new
        if source_url and source_url not in self.data.get('source_urls', []):
            self.data['source_urls'].append(source_url)

        # Update statistics
        self._update_statistics()

        # Save
        self._save_registry()

        bank_info = f" (mapped to: {bank_id})" if bank_id else " (no bank ID mapping)"
        return True, f"Added: {org_name} as {membership_type}{bank_info}"

    def map_banks(self, dry_run: bool = False) -> List[str]:
        """Map all unmapped bank organizations to bank IDs."""
        updates = []

        for member in self.data.get('members', []):
            if member.get('organization_type') == 'bank' and not member.get('bank_id'):
                org_name = member.get('organization_name', '')
                bank_id = self._fuzzy_match_bank(org_name)

                if bank_id:
                    if not dry_run:
                        member['bank_id'] = bank_id
                    updates.append(f"Mapped '{org_name}' -> {bank_id}")
                else:
                    updates.append(f"No match for '{org_name}'")

        if not dry_run and updates:
            self._save_registry()

        return updates

    def remove_member(
        self,
        org_name: str,
        membership_type: Optional[str] = None,
        dry_run: bool = False
    ) -> tuple[bool, str]:
        """Remove a member from the registry."""
        members = self.data.get('members', [])
        original_count = len(members)

        if membership_type:
            # Remove specific membership
            self.data['members'] = [
                m for m in members
                if not (m.get('organization_name', '').lower() == org_name.lower()
                       and m.get('membership_type') == membership_type)
            ]
        else:
            # Remove all memberships for this org
            self.data['members'] = [
                m for m in members
                if m.get('organization_name', '').lower() != org_name.lower()
            ]

        removed_count = original_count - len(self.data['members'])

        if removed_count == 0:
            return False, f"No matching member found: {org_name}"

        if dry_run:
            # Restore
            self.data['members'] = members
            return True, f"[DRY RUN] Would remove {removed_count} membership(s) for {org_name}"

        self._update_statistics()
        self._save_registry()

        return True, f"Removed {removed_count} membership(s) for {org_name}"

    def _update_statistics(self):
        """Update statistics based on current members."""
        members = self.data.get('members', [])

        self.data['statistics'] = {
            "total_members": len(members),
            "banks_with_cdm_membership": len(set(
                m.get('bank_id') for m in members
                if m.get('bank_id') and m.get('membership_type') in ['cdm_steering', 'cdm_working_group']
            )),
            "cdm_steering_count": sum(1 for m in members if m.get('membership_type') == 'cdm_steering'),
            "cdm_working_group_count": sum(1 for m in members if m.get('membership_type') == 'cdm_working_group'),
            "drr_working_group_count": sum(1 for m in members if m.get('membership_type') == 'drr_working_group'),
            "drr_pilot_count": sum(1 for m in members if m.get('membership_type') == 'drr_pilot')
        }

    def _save_registry(self):
        """Save the registry to file."""
        self.data['last_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')

        with open(ISDA_MEMBERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        logger.info(f"Registry saved to {ISDA_MEMBERS_FILE}")

    def get_statistics(self) -> dict:
        """Get current statistics."""
        self._update_statistics()
        return self.data.get('statistics', {})

    def list_members(
        self,
        membership_type: Optional[str] = None,
        org_type: Optional[str] = None,
        bank_only: bool = False
    ) -> List[dict]:
        """List members with optional filters."""
        members = self.data.get('members', [])

        if membership_type:
            members = [m for m in members if m.get('membership_type') == membership_type]

        if org_type:
            members = [m for m in members if m.get('organization_type') == org_type]

        if bank_only:
            members = [m for m in members if m.get('bank_id')]

        return members

    def get_bank_memberships(self, bank_id: str) -> List[dict]:
        """Get all memberships for a specific bank."""
        return [
            m for m in self.data.get('members', [])
            if m.get('bank_id') == bank_id
        ]


def main():
    parser = argparse.ArgumentParser(
        description='ISDA Members Validation and Management Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --validate
  %(prog)s --add-member "Deutsche Bank" --type cdm_working_group --source "https://isda.org/..."
  %(prog)s --add-member "Murex" --type cdm_working_group --org-type vendor
  %(prog)s --map-banks --dry-run
  %(prog)s --list --type cdm_steering
  %(prog)s --stats
        """
    )

    # Actions
    parser.add_argument('--validate', action='store_true',
                       help='Validate registry schema')
    parser.add_argument('--add-member', metavar='NAME',
                       help='Add a new member organization')
    parser.add_argument('--remove-member', metavar='NAME',
                       help='Remove a member organization')
    parser.add_argument('--map-banks', action='store_true',
                       help='Map unmapped bank organizations to bank IDs')
    parser.add_argument('--list', action='store_true',
                       help='List members')
    parser.add_argument('--stats', action='store_true',
                       help='Show statistics')
    parser.add_argument('--bank-memberships', metavar='BANK_ID',
                       help='Show memberships for a specific bank')

    # Options for add-member
    parser.add_argument('--type', dest='membership_type',
                       choices=VALID_MEMBERSHIP_TYPES,
                       help='Membership type')
    parser.add_argument('--org-type', default='bank',
                       choices=VALID_ORG_TYPES,
                       help='Organization type (default: bank)')
    parser.add_argument('--source', metavar='URL',
                       help='Source URL for the membership claim')
    parser.add_argument('--source-date', metavar='DATE',
                       help='Date of source (YYYY-MM-DD)')
    parser.add_argument('--notes', metavar='TEXT',
                       help='Additional notes')

    # Filters for list
    parser.add_argument('--bank-only', action='store_true',
                       help='Only show members with bank IDs')

    # General options
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')

    args = parser.parse_args()

    # Need at least one action
    if not any([args.validate, args.add_member, args.remove_member,
                args.map_banks, args.list, args.stats, args.bank_memberships]):
        parser.print_help()
        sys.exit(1)

    validator = IsdaMemberValidator()

    # Validate
    if args.validate:
        issues = validator.validate_schema()
        if issues:
            print("Validation issues found:")
            for issue in issues:
                print(f"  - {issue}")
            sys.exit(1)
        else:
            print("Registry schema is valid")

    # Add member
    if args.add_member:
        if not args.membership_type:
            print("Error: --type is required when adding a member")
            sys.exit(1)

        success, message = validator.add_member(
            org_name=args.add_member,
            membership_type=args.membership_type,
            org_type=args.org_type,
            source_url=args.source,
            source_date=args.source_date,
            notes=args.notes,
            dry_run=args.dry_run
        )

        print(message)
        if not success:
            sys.exit(1)

    # Remove member
    if args.remove_member:
        success, message = validator.remove_member(
            org_name=args.remove_member,
            membership_type=args.membership_type,
            dry_run=args.dry_run
        )

        print(message)
        if not success:
            sys.exit(1)

    # Map banks
    if args.map_banks:
        updates = validator.map_banks(dry_run=args.dry_run)
        if updates:
            print("Bank ID mappings:")
            for update in updates:
                print(f"  {update}")
        else:
            print("No unmapped banks to process")

    # List members
    if args.list:
        members = validator.list_members(
            membership_type=args.membership_type,
            org_type=args.org_type,
            bank_only=args.bank_only
        )

        if args.json:
            print(json.dumps(members, indent=2))
        else:
            if not members:
                print("No members found matching criteria")
            else:
                print(f"Found {len(members)} member(s):")
                for m in members:
                    bank_info = f" [{m['bank_id']}]" if m.get('bank_id') else ""
                    print(f"  - {m['organization_name']} ({m['membership_type']}){bank_info}")

    # Statistics
    if args.stats:
        stats = validator.get_statistics()

        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print("ISDA Members Statistics:")
            print(f"  Total members: {stats.get('total_members', 0)}")
            print(f"  Banks with CDM membership: {stats.get('banks_with_cdm_membership', 0)}")
            print(f"  CDM Steering Committee: {stats.get('cdm_steering_count', 0)}")
            print(f"  CDM Working Group: {stats.get('cdm_working_group_count', 0)}")
            print(f"  DRR Working Group: {stats.get('drr_working_group_count', 0)}")
            print(f"  DRR Pilot: {stats.get('drr_pilot_count', 0)}")

    # Bank memberships
    if args.bank_memberships:
        memberships = validator.get_bank_memberships(args.bank_memberships)

        if args.json:
            print(json.dumps(memberships, indent=2))
        else:
            if not memberships:
                print(f"No memberships found for bank: {args.bank_memberships}")
            else:
                print(f"Memberships for {args.bank_memberships}:")
                for m in memberships:
                    print(f"  - {m['membership_type']} ({m['organization_name']})")


if __name__ == '__main__':
    main()
