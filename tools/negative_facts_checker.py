"""
CDM Research Protocol - Negative Facts Checker v1.0

Pre-search validation against known dead ends.
Parses knowledge_base/negative_facts.md and warns if proposed searches
match patterns known to waste time.

This tool helps:
- Avoid repeating known dead-end searches
- Save research time (estimated 15-40 hours per phase)
- Document why certain searches were skipped
- Log when dead ends are successfully avoided

Usage:
    from negative_facts_checker import NegativeFactsChecker

    checker = NegativeFactsChecker()
    if checker.is_dead_end("CDM blockchain bank"):
        print("This query matches known dead ends!")

    # Or CLI:
    python negative_facts_checker.py check "CDM blockchain"
    python negative_facts_checker.py list
"""

import re
import sys
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- PATHS ---
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_NEGATIVE_FACTS_PATH = PROJECT_ROOT / "knowledge_base" / "negative_facts.md"


@dataclass
class DeadEnd:
    """A known dead-end search pattern."""
    pattern: str
    reason: str
    category: str = "general"
    source: str = ""
    estimated_time_saved: str = ""


class NegativeFactsChecker:
    """
    Pre-search validation against known dead ends.

    Parses negative_facts.md and checks proposed queries against
    known patterns that don't yield useful results.
    """

    def __init__(self, knowledge_base_path: Optional[Path] = None):
        """
        Initialize the checker.

        Args:
            knowledge_base_path: Path to negative_facts.md (optional)
        """
        if knowledge_base_path is None:
            knowledge_base_path = DEFAULT_NEGATIVE_FACTS_PATH
        self.knowledge_base_path = Path(knowledge_base_path)
        self.dead_ends: list[DeadEnd] = []
        self._parse_negative_facts()

    def _parse_negative_facts(self):
        """Parse negative_facts.md into structured dead ends."""
        if not self.knowledge_base_path.exists():
            logger.warning(f"Negative facts file not found: {self.knowledge_base_path}")
            # Add some default dead ends
            self._add_default_dead_ends()
            return

        content = self.knowledge_base_path.read_text(encoding='utf-8')
        self._parse_content(content)

    def _parse_content(self, content: str):
        """Parse markdown content for dead-end patterns."""
        # Try different pattern formats that might be in the markdown:

        # Format 1: **Pattern**: "query" -> reason
        pattern1 = r'\*\*Pattern\*\*:\s*["\']([^"\']+)["\'].*?(?:->|->)\s*(.+)'

        # Format 2: - "query" - reason
        pattern2 = r'-\s*["\']([^"\']+)["\']\s*[-:]\s*(.+)'

        # Format 3: | pattern | reason | (table format)
        pattern3 = r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|'

        # Format 4: Bullet with explanation on next line
        pattern4 = r'[-*]\s*["\']?([^"\':\n]+)["\']?\s*\n\s*[-*]?\s*(?:Reason|Why|Note)?:?\s*(.+)'

        patterns_found = 0

        # Try pattern 1
        for match in re.finditer(pattern1, content, re.IGNORECASE):
            self.dead_ends.append(DeadEnd(
                pattern=match.group(1).lower().strip(),
                reason=match.group(2).strip(),
                source=str(self.knowledge_base_path)
            ))
            patterns_found += 1

        # Try pattern 2
        for match in re.finditer(pattern2, content, re.MULTILINE):
            pattern_text = match.group(1).lower().strip()
            if len(pattern_text) > 3 and pattern_text not in [d.pattern for d in self.dead_ends]:
                self.dead_ends.append(DeadEnd(
                    pattern=pattern_text,
                    reason=match.group(2).strip(),
                    source=str(self.knowledge_base_path)
                ))
                patterns_found += 1

        if patterns_found == 0:
            logger.warning("No dead-end patterns found in negative_facts.md")
            self._add_default_dead_ends()

        logger.debug(f"Loaded {len(self.dead_ends)} dead-end patterns")

    def _add_default_dead_ends(self):
        """Add default dead-end patterns when file is missing or empty."""
        defaults = [
            DeadEnd(
                pattern="cdm blockchain",
                reason="CDM is not blockchain-related; conflates with cryptocurrency",
                category="false_association"
            ),
            DeadEnd(
                pattern="cdm crypto",
                reason="CDM is not cryptocurrency-related",
                category="false_association"
            ),
            DeadEnd(
                pattern="common domain model retail",
                reason="CDM focuses on derivatives, not retail banking",
                category="out_of_scope"
            ),
            DeadEnd(
                pattern="isda digital asset",
                reason="Digital asset taxonomy is separate from CDM",
                category="false_association"
            ),
            DeadEnd(
                pattern="drr trade finance",
                reason="DRR focuses on derivatives reporting, not trade finance",
                category="out_of_scope"
            ),
            DeadEnd(
                pattern="cdm implementation guide pdf",
                reason="Generic PDFs rarely contain bank-specific information",
                category="low_yield"
            ),
            DeadEnd(
                pattern="cdm tutorial",
                reason="Tutorials are educational, not evidence of bank adoption",
                category="low_yield"
            ),
        ]

        self.dead_ends.extend(defaults)
        logger.debug(f"Added {len(defaults)} default dead-end patterns")

    def check_query(self, query: str) -> list[DeadEnd]:
        """
        Check if a query matches any known dead ends.

        Args:
            query: The search query to check

        Returns:
            List of matching DeadEnd patterns
        """
        query_lower = query.lower()
        matches = []

        for dead_end in self.dead_ends:
            # Check if pattern appears in query
            if dead_end.pattern in query_lower:
                matches.append(dead_end)
            # Also check for word-by-word overlap
            elif self._has_significant_overlap(dead_end.pattern, query_lower):
                matches.append(dead_end)

        return matches

    def _has_significant_overlap(self, pattern: str, query: str) -> bool:
        """Check if pattern and query have significant word overlap."""
        pattern_words = set(pattern.split())
        query_words = set(query.split())

        if len(pattern_words) < 2:
            return False

        overlap = pattern_words & query_words
        # Require at least 2 words or 50% of pattern words to match
        return len(overlap) >= 2 or len(overlap) >= len(pattern_words) * 0.5

    def is_dead_end(self, query: str) -> bool:
        """
        Check if query is a known dead end.

        Args:
            query: The search query to check

        Returns:
            True if query matches known dead ends
        """
        return len(self.check_query(query)) > 0

    def warn_if_dead_end(self, query: str) -> bool:
        """
        Print warning if query matches dead end.

        Args:
            query: The search query to check

        Returns:
            True if matched (warning printed), False otherwise
        """
        matches = self.check_query(query)
        if matches:
            print(f"\n[WARNING] Query may match known dead ends:")
            print(f"  Query: {query}")
            for m in matches:
                print(f"\n  Dead End Pattern: {m.pattern}")
                print(f"  Reason: {m.reason}")
                if m.category:
                    print(f"  Category: {m.category}")
            print()
            return True
        return False

    def get_all_patterns(self) -> list[dict]:
        """Get all dead-end patterns as dicts."""
        return [asdict(d) for d in self.dead_ends]

    def add_pattern(self, pattern: str, reason: str, category: str = "custom"):
        """
        Add a new dead-end pattern at runtime.

        Args:
            pattern: The pattern to match
            reason: Why this is a dead end
            category: Category of dead end
        """
        self.dead_ends.append(DeadEnd(
            pattern=pattern.lower(),
            reason=reason,
            category=category,
            source="runtime"
        ))

    def suggest_alternatives(self, query: str) -> list[str]:
        """
        Suggest alternative queries when a dead end is detected.

        Args:
            query: The problematic query

        Returns:
            List of suggested alternative queries
        """
        alternatives = []

        # Remove known problematic terms
        problematic_terms = [
            "blockchain", "crypto", "retail", "tutorial",
            "pdf", "guide", "digital asset"
        ]

        cleaned_query = query.lower()
        for term in problematic_terms:
            cleaned_query = cleaned_query.replace(term, "").strip()

        if cleaned_query and cleaned_query != query.lower():
            alternatives.append(cleaned_query)

        # Suggest site-specific searches
        base_terms = [w for w in query.split() if w.lower() not in problematic_terms]
        if base_terms:
            base = " ".join(base_terms)
            alternatives.extend([
                f"site:isda.org {base}",
                f"site:finos.org {base}",
                f"site:risk.net {base}"
            ])

        return alternatives


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python negative_facts_checker.py <command> [args]")
        print("Commands:")
        print("  check <query>  - Check if query matches dead ends")
        print("  list           - List all known dead-end patterns")
        print("  suggest <query>- Suggest alternatives if query is dead end")
        sys.exit(1)

    command = sys.argv[1]
    checker = NegativeFactsChecker()

    if command == 'check':
        if len(sys.argv) < 3:
            print("Error: check requires a query")
            sys.exit(1)
        query = " ".join(sys.argv[2:])

        if checker.warn_if_dead_end(query):
            print("[RESULT] Query matches known dead ends. Consider alternatives.")
            sys.exit(1)
        else:
            print(f"[OK] Query does not match known dead ends: {query}")
            sys.exit(0)

    elif command == 'list':
        patterns = checker.get_all_patterns()
        print(f"\nKnown Dead-End Patterns ({len(patterns)}):")
        print("=" * 60)
        for p in patterns:
            print(f"\nPattern:  {p['pattern']}")
            print(f"Reason:   {p['reason']}")
            print(f"Category: {p['category']}")

    elif command == 'suggest':
        if len(sys.argv) < 3:
            print("Error: suggest requires a query")
            sys.exit(1)
        query = " ".join(sys.argv[2:])

        matches = checker.check_query(query)
        if not matches:
            print(f"[OK] Query is not a known dead end: {query}")
        else:
            print(f"[WARNING] Query matches dead ends.")
            alternatives = checker.suggest_alternatives(query)
            if alternatives:
                print(f"\nSuggested alternatives:")
                for alt in alternatives:
                    print(f"  - {alt}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
