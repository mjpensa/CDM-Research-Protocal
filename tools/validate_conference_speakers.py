#!/usr/bin/env python3
"""
Conference Speakers Validation and Management Tool

Validates, normalizes, and manages conference speaker registry.
Designed for population via Claude Code WebFetch during research sessions.

Usage:
    python validate_conference_speakers.py --validate
    python validate_conference_speakers.py --add-event "ISDA AGM 2024" --date 2024-04-10 --type isda_agm
    python validate_conference_speakers.py --add-speaker "John Smith" --org "Barclays" --event "ISDA AGM 2024"
    python validate_conference_speakers.py --map-banks
    python validate_conference_speakers.py --stats
"""

import argparse
import json
import logging
import re
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

SPEAKERS_FILE = KB_DIR / "conference_speakers.json"
BANK_MANIFEST_FILE = CONFIG_DIR / "bank-manifest.json"

# Valid event types
VALID_EVENT_TYPES = [
    "isda_agm",
    "finos_osff",
    "risk_live",
    "derivhack",
    "isda_regional",
    "sibos",
    "cftc_roundtable",
    "webinar",
    "other"
]

# CDM relevance keywords for session matching
CDM_KEYWORDS = [
    "cdm", "common domain model", "digital regulatory reporting", "drr",
    "isda", "finos", "derivatives reporting", "emir refit", "cftc rewrite",
    "trade reporting", "regulatory reporting", "standardization", "interoperability",
    "rosetta", "regnosys", "digital asset"
]


@dataclass
class Speaker:
    """Represents a conference speaker."""
    name: str
    organization: str
    bank_id: Optional[str] = None
    title: Optional[str] = None
    session_title: Optional[str] = None
    cdm_relevant: bool = False

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict) -> 'Speaker':
        return cls(
            name=data.get('name', ''),
            organization=data.get('organization', ''),
            bank_id=data.get('bank_id'),
            title=data.get('title'),
            session_title=data.get('session_title'),
            cdm_relevant=data.get('cdm_relevant', False)
        )


@dataclass
class Event:
    """Represents a conference event."""
    event_name: str
    event_date: str
    event_type: str
    event_url: Optional[str] = None
    speakers: List[dict] = field(default_factory=list)
    added_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        result = {
            'event_name': self.event_name,
            'event_date': self.event_date,
            'event_type': self.event_type,
            'speakers': self.speakers,
            'added_at': self.added_at
        }
        if self.event_url:
            result['event_url'] = self.event_url
        if self.notes:
            result['notes'] = self.notes
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        return cls(
            event_name=data.get('event_name', ''),
            event_date=data.get('event_date', ''),
            event_type=data.get('event_type', 'other'),
            event_url=data.get('event_url'),
            speakers=data.get('speakers', []),
            added_at=data.get('added_at', datetime.now(timezone.utc).isoformat()),
            notes=data.get('notes')
        )


class ConferenceSpeakersValidator:
    """Validates and manages conference speakers registry."""

    def __init__(self):
        self.data = self._load_registry()
        self.bank_manifest = self._load_bank_manifest()
        self.name_to_bank_id = self._build_name_mapping()

    def _load_registry(self) -> dict:
        """Load the conference speakers registry."""
        if not SPEAKERS_FILE.exists():
            logger.warning(f"Registry not found: {SPEAKERS_FILE}")
            return {"events": [], "speakers_by_bank": {}, "statistics": {}}

        with open(SPEAKERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_bank_manifest(self) -> dict:
        """Load bank manifest for ID mapping."""
        if not BANK_MANIFEST_FILE.exists():
            logger.warning(f"Bank manifest not found: {BANK_MANIFEST_FILE}")
            return {"banks": []}

        with open(BANK_MANIFEST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _build_name_mapping(self) -> Dict[str, str]:
        """Build a mapping from organization names to bank IDs."""
        mapping = {}

        banks = self.bank_manifest.get('banks', [])
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

        return mapping

    def _fuzzy_match_bank(self, org_name: str, threshold: float = 0.7) -> Optional[str]:
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

    def _is_cdm_relevant(self, session_title: str) -> bool:
        """Check if session title indicates CDM relevance."""
        if not session_title:
            return False

        title_lower = session_title.lower()
        return any(keyword in title_lower for keyword in CDM_KEYWORDS)

    def validate_schema(self) -> List[str]:
        """Validate the registry schema. Returns list of issues."""
        issues = []

        # Check required top-level keys
        required_keys = ['events', 'speakers_by_bank', 'statistics']
        for key in required_keys:
            if key not in self.data:
                issues.append(f"Missing required key: {key}")

        # Validate each event
        for i, event in enumerate(self.data.get('events', [])):
            if not event.get('event_name'):
                issues.append(f"Event {i}: missing event_name")

            if not event.get('event_date'):
                issues.append(f"Event {i}: missing event_date")
            else:
                # Validate date format
                try:
                    datetime.strptime(event['event_date'], '%Y-%m-%d')
                except ValueError:
                    issues.append(f"Event {i}: invalid date format '{event['event_date']}' (expected YYYY-MM-DD)")

            if not event.get('event_type'):
                issues.append(f"Event {i}: missing event_type")
            elif event['event_type'] not in VALID_EVENT_TYPES:
                issues.append(f"Event {i}: invalid event_type '{event['event_type']}'")

            # Validate speakers
            for j, speaker in enumerate(event.get('speakers', [])):
                if not speaker.get('name'):
                    issues.append(f"Event {i}, Speaker {j}: missing name")
                if not speaker.get('organization'):
                    issues.append(f"Event {i}, Speaker {j}: missing organization")

        return issues

    def add_event(
        self,
        event_name: str,
        event_date: str,
        event_type: str = "other",
        event_url: Optional[str] = None,
        notes: Optional[str] = None,
        dry_run: bool = False
    ) -> tuple[bool, str]:
        """Add a new event to the registry."""

        # Validate event type
        if event_type not in VALID_EVENT_TYPES:
            return False, f"Invalid event type: {event_type}. Valid: {VALID_EVENT_TYPES}"

        # Validate date format
        try:
            datetime.strptime(event_date, '%Y-%m-%d')
        except ValueError:
            return False, f"Invalid date format: {event_date}. Expected YYYY-MM-DD"

        # Check for duplicates
        existing = [e for e in self.data.get('events', [])
                   if e.get('event_name', '').lower() == event_name.lower()
                   and e.get('event_date') == event_date]
        if existing:
            return False, f"Duplicate: {event_name} on {event_date} already exists"

        # Create event
        event = Event(
            event_name=event_name,
            event_date=event_date,
            event_type=event_type,
            event_url=event_url,
            notes=notes
        )

        if dry_run:
            return True, f"[DRY RUN] Would add event: {event.to_dict()}"

        # Add to registry
        self.data['events'].append(event.to_dict())

        # Update statistics
        self._update_statistics()

        # Save
        self._save_registry()

        return True, f"Added event: {event_name} on {event_date} ({event_type})"

    def add_speaker(
        self,
        name: str,
        organization: str,
        event_name: str,
        session_title: Optional[str] = None,
        title: Optional[str] = None,
        dry_run: bool = False
    ) -> tuple[bool, str]:
        """Add a speaker to an event."""

        # Find the event
        event_idx = None
        for i, event in enumerate(self.data.get('events', [])):
            if event.get('event_name', '').lower() == event_name.lower():
                event_idx = i
                break

        if event_idx is None:
            return False, f"Event not found: {event_name}. Add the event first with --add-event"

        # Check for duplicate speaker
        existing_speakers = self.data['events'][event_idx].get('speakers', [])
        if any(s.get('name', '').lower() == name.lower() for s in existing_speakers):
            return False, f"Speaker {name} already added to {event_name}"

        # Try to map to bank ID
        bank_id = self._fuzzy_match_bank(organization)

        # Check CDM relevance
        cdm_relevant = self._is_cdm_relevant(session_title) if session_title else False

        # Create speaker
        speaker = Speaker(
            name=name,
            organization=organization,
            bank_id=bank_id,
            title=title,
            session_title=session_title,
            cdm_relevant=cdm_relevant
        )

        if dry_run:
            return True, f"[DRY RUN] Would add speaker: {speaker.to_dict()}"

        # Add to event
        self.data['events'][event_idx]['speakers'].append(speaker.to_dict())

        # Update speakers_by_bank
        if bank_id:
            if bank_id not in self.data['speakers_by_bank']:
                self.data['speakers_by_bank'][bank_id] = []
            self.data['speakers_by_bank'][bank_id].append({
                'name': name,
                'event': event_name,
                'event_date': self.data['events'][event_idx].get('event_date'),
                'session_title': session_title,
                'cdm_relevant': cdm_relevant
            })

        # Update statistics
        self._update_statistics()

        # Save
        self._save_registry()

        bank_info = f" (mapped to: {bank_id})" if bank_id else " (no bank ID mapping)"
        cdm_info = " [CDM-relevant]" if cdm_relevant else ""
        return True, f"Added speaker: {name} from {organization}{bank_info}{cdm_info}"

    def map_banks(self, dry_run: bool = False) -> List[str]:
        """Map all unmapped speaker organizations to bank IDs."""
        updates = []

        for event in self.data.get('events', []):
            for speaker in event.get('speakers', []):
                if not speaker.get('bank_id'):
                    org_name = speaker.get('organization', '')
                    bank_id = self._fuzzy_match_bank(org_name)

                    if bank_id:
                        if not dry_run:
                            speaker['bank_id'] = bank_id
                        updates.append(f"Mapped '{org_name}' -> {bank_id}")
                    else:
                        updates.append(f"No match for '{org_name}'")

        if not dry_run and updates:
            self._rebuild_speakers_by_bank()
            self._save_registry()

        return updates

    def _rebuild_speakers_by_bank(self):
        """Rebuild the speakers_by_bank index."""
        self.data['speakers_by_bank'] = {}

        for event in self.data.get('events', []):
            for speaker in event.get('speakers', []):
                bank_id = speaker.get('bank_id')
                if bank_id:
                    if bank_id not in self.data['speakers_by_bank']:
                        self.data['speakers_by_bank'][bank_id] = []
                    self.data['speakers_by_bank'][bank_id].append({
                        'name': speaker.get('name'),
                        'event': event.get('event_name'),
                        'event_date': event.get('event_date'),
                        'session_title': speaker.get('session_title'),
                        'cdm_relevant': speaker.get('cdm_relevant', False)
                    })

    def _update_statistics(self):
        """Update statistics based on current data."""
        events = self.data.get('events', [])

        total_speakers = sum(len(e.get('speakers', [])) for e in events)
        cdm_relevant = sum(
            1 for e in events
            for s in e.get('speakers', [])
            if s.get('cdm_relevant')
        )

        self.data['statistics'] = {
            "total_events": len(events),
            "total_speakers": total_speakers,
            "banks_represented": len(self.data.get('speakers_by_bank', {})),
            "cdm_relevant_sessions": cdm_relevant
        }

    def _save_registry(self):
        """Save the registry to file."""
        self.data['last_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')

        with open(SPEAKERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        logger.info(f"Registry saved to {SPEAKERS_FILE}")

    def get_statistics(self) -> dict:
        """Get current statistics."""
        self._update_statistics()
        return self.data.get('statistics', {})

    def list_events(self, event_type: Optional[str] = None) -> List[dict]:
        """List events with optional type filter."""
        events = self.data.get('events', [])

        if event_type:
            events = [e for e in events if e.get('event_type') == event_type]

        return events

    def get_bank_speakers(self, bank_id: str) -> List[dict]:
        """Get all speakers from a specific bank."""
        return self.data.get('speakers_by_bank', {}).get(bank_id, [])

    def get_cdm_relevant_speakers(self) -> List[dict]:
        """Get all speakers with CDM-relevant sessions."""
        result = []
        for event in self.data.get('events', []):
            for speaker in event.get('speakers', []):
                if speaker.get('cdm_relevant'):
                    result.append({
                        'name': speaker.get('name'),
                        'organization': speaker.get('organization'),
                        'bank_id': speaker.get('bank_id'),
                        'event': event.get('event_name'),
                        'event_date': event.get('event_date'),
                        'session_title': speaker.get('session_title')
                    })
        return result


def main():
    parser = argparse.ArgumentParser(
        description='Conference Speakers Validation and Management Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --validate
  %(prog)s --add-event "ISDA AGM 2024" --date 2024-04-10 --type isda_agm
  %(prog)s --add-speaker "John Smith" --org "Barclays" --event "ISDA AGM 2024" --session "CDM Implementation"
  %(prog)s --map-banks --dry-run
  %(prog)s --list-events --type isda_agm
  %(prog)s --bank-speakers barclays
  %(prog)s --cdm-relevant
  %(prog)s --stats
        """
    )

    # Actions
    parser.add_argument('--validate', action='store_true',
                       help='Validate registry schema')
    parser.add_argument('--add-event', metavar='NAME',
                       help='Add a new event')
    parser.add_argument('--add-speaker', metavar='NAME',
                       help='Add a speaker to an event')
    parser.add_argument('--map-banks', action='store_true',
                       help='Map unmapped speaker organizations to bank IDs')
    parser.add_argument('--list-events', action='store_true',
                       help='List events')
    parser.add_argument('--bank-speakers', metavar='BANK_ID',
                       help='List speakers from a specific bank')
    parser.add_argument('--cdm-relevant', action='store_true',
                       help='List speakers with CDM-relevant sessions')
    parser.add_argument('--stats', action='store_true',
                       help='Show statistics')

    # Options for add-event
    parser.add_argument('--date', metavar='YYYY-MM-DD',
                       help='Event date')
    parser.add_argument('--type', dest='event_type',
                       choices=VALID_EVENT_TYPES,
                       default='other',
                       help='Event type')
    parser.add_argument('--url', metavar='URL',
                       help='Event URL')

    # Options for add-speaker
    parser.add_argument('--org', metavar='ORG',
                       help='Speaker organization')
    parser.add_argument('--event', metavar='EVENT',
                       help='Event name (for adding speaker)')
    parser.add_argument('--session', metavar='TITLE',
                       help='Session title')
    parser.add_argument('--title', metavar='TITLE',
                       help='Speaker job title')

    # General options
    parser.add_argument('--notes', metavar='TEXT',
                       help='Additional notes')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')

    args = parser.parse_args()

    # Need at least one action
    if not any([args.validate, args.add_event, args.add_speaker,
                args.map_banks, args.list_events, args.bank_speakers,
                args.cdm_relevant, args.stats]):
        parser.print_help()
        sys.exit(1)

    validator = ConferenceSpeakersValidator()

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

    # Add event
    if args.add_event:
        if not args.date:
            print("Error: --date is required when adding an event")
            sys.exit(1)

        success, message = validator.add_event(
            event_name=args.add_event,
            event_date=args.date,
            event_type=args.event_type,
            event_url=args.url,
            notes=args.notes,
            dry_run=args.dry_run
        )

        print(message)
        if not success:
            sys.exit(1)

    # Add speaker
    if args.add_speaker:
        if not args.org:
            print("Error: --org is required when adding a speaker")
            sys.exit(1)
        if not args.event:
            print("Error: --event is required when adding a speaker")
            sys.exit(1)

        success, message = validator.add_speaker(
            name=args.add_speaker,
            organization=args.org,
            event_name=args.event,
            session_title=args.session,
            title=args.title,
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
            print("No unmapped speakers to process")

    # List events
    if args.list_events:
        events = validator.list_events(event_type=args.event_type if args.event_type != 'other' else None)

        if args.json:
            print(json.dumps(events, indent=2))
        else:
            if not events:
                print("No events found")
            else:
                print(f"Found {len(events)} event(s):")
                for e in events:
                    speaker_count = len(e.get('speakers', []))
                    print(f"  - {e['event_name']} ({e['event_date']}) - {speaker_count} speaker(s)")

    # Bank speakers
    if args.bank_speakers:
        speakers = validator.get_bank_speakers(args.bank_speakers)

        if args.json:
            print(json.dumps(speakers, indent=2))
        else:
            if not speakers:
                print(f"No speakers found for bank: {args.bank_speakers}")
            else:
                print(f"Speakers from {args.bank_speakers}:")
                for s in speakers:
                    cdm = " [CDM]" if s.get('cdm_relevant') else ""
                    print(f"  - {s['name']} at {s['event']} ({s['event_date']}){cdm}")

    # CDM relevant speakers
    if args.cdm_relevant:
        speakers = validator.get_cdm_relevant_speakers()

        if args.json:
            print(json.dumps(speakers, indent=2))
        else:
            if not speakers:
                print("No CDM-relevant speakers found")
            else:
                print(f"CDM-relevant speakers ({len(speakers)}):")
                for s in speakers:
                    bank = f" [{s['bank_id']}]" if s.get('bank_id') else ""
                    print(f"  - {s['name']} ({s['organization']}){bank}")
                    print(f"      Event: {s['event']} ({s['event_date']})")
                    print(f"      Session: {s['session_title']}")

    # Statistics
    if args.stats:
        stats = validator.get_statistics()

        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print("Conference Speakers Statistics:")
            print(f"  Total events: {stats.get('total_events', 0)}")
            print(f"  Total speakers: {stats.get('total_speakers', 0)}")
            print(f"  Banks represented: {stats.get('banks_represented', 0)}")
            print(f"  CDM-relevant sessions: {stats.get('cdm_relevant_sessions', 0)}")


if __name__ == '__main__':
    main()
