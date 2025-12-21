"""
Unit tests for suggest_negative_facts.py

Tests the negative facts suggestion system that captures institutional
knowledge from completed bank research sessions.
"""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from suggest_negative_facts import (
    NegativeFactsSuggester,
    NullSearchPattern,
    FalseLead,
    VendorCaution,
    JurisdictionPattern,
    Suggestion
)


# --- FIXTURES ---

@pytest.fixture
def sample_evidence():
    """Sample evidence.json structure for testing."""
    return {
        "bank_id": "test-bank",
        "bank_name": "Test Bank AG",
        "evidence_items": [
            {
                "id": "TEST-001",
                "claim": "Test Bank uses vendor CDM solution",
                "source_url": "https://vendor.com/press-release",
                "tier": 2,
                "claim_type": "vendor_proxy_signal",
                "product_scope": ["IRS", "CDS"],
                "jurisdiction_scope": ["EU"],
                "quality_assessment": {"recency": "current"}
            },
            {
                "id": "TEST-002",
                "claim": "Test Bank participated in 2018 DRR pilot",
                "source_url": "https://regulator.gov/pilot",
                "tier": 1,
                "claim_type": "pilot_or_poc",
                "product_scope": ["IRS"],
                "jurisdiction_scope": ["UK"],
                "quality_assessment": {"recency": "historical"},
                "temporal_weight": 0.3
            }
        ],
        "null_results": [
            {
                "category": "CDM Production Deployment",
                "queries": [
                    "Test Bank CDM production",
                    "Test Bank CDM live deployment",
                    "Test Bank CDM implementation 2024"
                ],
                "results_reviewed": 30,
                "null_type": "NO_RESULTS",
                "informative_absence": False,
                "implication": "No evidence of production CDM"
            },
            {
                "category": "FINOS CDM Contributions",
                "queries": ["Test Bank FINOS CDM contributor"],
                "results_reviewed": 10,
                "null_type": "NO_RESULTS",
                "informative_absence": True,
                "implication": "Not a CDM contributor"
            }
        ],
        "search_tracking": {
            "tier1_searches": {"queries": ["Test Bank ISDA CDM", "Test Bank DRR"]},
            "tier2_searches": {"queries": ["Test Bank Risk.net CDM"]},
            "tier3_searches": {"queries": ["Test Bank CDM LinkedIn"]}
        }
    }


@pytest.fixture
def sample_negative_facts_md():
    """Sample negative_facts.md content."""
    return """# Negative Facts Knowledge Base

**Last Updated**: 2025-12-20

---

## A. Dead End Search Patterns

| Query Pattern | Why It Fails | Better Alternative |
|--------------|--------------|-------------------|
| `"[Bank] derivatives reporting"` | Too vague | `"[Bank] ISDA CDM"` |

---

## B. False Leads Registry

### Fluxnova != CDM

- **Misleading Signal**: FINOS Fluxnova participation
- **Reality**: Not CDM related

---

## C. Debunked Claims

---

## D. Informative Absences

---

## E. Vendor Domain Cautions

| vendor.com | Vendor marketing | Bank confirmation required |

---

## F. Time Savings Estimates

| Pattern Avoided | Hours Saved per Bank |
|----------------|---------------------|
| Swiss site-restricted searches | 2-3 hours |

---

## G. Pattern Recognition by Phase

### Phase 1: European Tier 1 (Completed)
- _Add learnings after Phase 1 completion_

---

## H. How to Update This File

1. Document null searches
"""


@pytest.fixture
def temp_knowledge_base(sample_negative_facts_md):
    """Create a temporary negative_facts.md file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(sample_negative_facts_md)
        return Path(f.name)


@pytest.fixture
def temp_bank_dir(sample_evidence):
    """Create a temporary bank directory with evidence.json."""
    with tempfile.TemporaryDirectory() as tmpdir:
        bank_dir = Path(tmpdir)
        evidence_path = bank_dir / "evidence.json"
        evidence_path.write_text(json.dumps(sample_evidence, indent=2))
        yield bank_dir


# --- DEAD-END DETECTION TESTS ---

class TestDeadEndDetection:
    """Tests for dead-end search pattern detection."""

    def test_detects_repeated_null_queries(self, temp_bank_dir, temp_knowledge_base):
        """Queries appearing 3+ times with NO_RESULTS should be flagged."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        with open(temp_bank_dir / "evidence.json") as f:
            evidence = json.load(f)

        patterns = suggester._detect_dead_end_searches(evidence)

        # Should detect the CDM Production Deployment pattern (3 queries)
        assert len(patterns) >= 1
        prod_pattern = next((p for p in patterns if "Production" in p.category), None)
        assert prod_pattern is not None
        assert prod_pattern.times_tried == 3

    def test_ignores_informative_absences(self, temp_bank_dir, temp_knowledge_base):
        """Informative absences should NOT be flagged as dead ends."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        with open(temp_bank_dir / "evidence.json") as f:
            evidence = json.load(f)

        patterns = suggester._detect_dead_end_searches(evidence)

        # Should NOT detect FINOS pattern (informative_absence=True)
        finos_pattern = next((p for p in patterns if "FINOS" in p.category), None)
        assert finos_pattern is None

    def test_respects_time_threshold(self, temp_knowledge_base):
        """Only flag patterns exceeding minimum time wasted."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        evidence = {
            "bank_id": "test",
            "null_results": [
                {
                    "category": "Quick Search",
                    "queries": ["quick test"],
                    "results_reviewed": 5,  # 10 minutes < 30 min threshold
                    "null_type": "NO_RESULTS",
                    "informative_absence": False
                }
            ]
        }

        patterns = suggester._detect_dead_end_searches(evidence)
        assert len(patterns) == 0  # Should not detect (below threshold)


# --- FALSE LEAD DETECTION TESTS ---

class TestFalseLeadDetection:
    """Tests for false lead detection."""

    def test_detects_vendor_without_confirmation(self, temp_bank_dir, temp_knowledge_base):
        """Vendor claims without bank confirmation should be flagged."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        with open(temp_bank_dir / "evidence.json") as f:
            evidence = json.load(f)

        false_leads = suggester._detect_false_leads(evidence, {})

        # Should detect vendor claim without production_usage confirmation
        vendor_lead = next((fl for fl in false_leads if "vendor" in fl.misleading_signal.lower()), None)
        assert vendor_lead is not None
        assert "confirmation" in vendor_lead.lesson.lower()

    def test_detects_historical_pilot_without_followthrough(self, temp_bank_dir, temp_knowledge_base):
        """Historical pilots without current evidence should be flagged."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        with open(temp_bank_dir / "evidence.json") as f:
            evidence = json.load(f)

        false_leads = suggester._detect_false_leads(evidence, {})

        # Should detect historical pilot (temporal_weight=0.3)
        pilot_lead = next((fl for fl in false_leads if "pilot" in fl.misleading_signal.lower()), None)
        assert pilot_lead is not None
        assert "follow-through" in pilot_lead.lesson.lower()

    def test_ignores_confirmed_vendor_claims(self, temp_knowledge_base):
        """Vendor claims WITH bank confirmation should not be flagged."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        evidence = {
            "bank_id": "test",
            "evidence_items": [
                {
                    "id": "V1",
                    "claim": "Vendor says bank uses CDM",
                    "claim_type": "vendor_proxy_signal",
                    "product_scope": ["IRS"],
                    "source_url": "https://vendor.com/pr"
                },
                {
                    "id": "B1",
                    "claim": "Bank confirms production CDM usage",
                    "claim_type": "production_usage",
                    "product_scope": ["IRS"],
                    "source_url": "https://bank.com/announcement"
                }
            ],
            "null_results": []
        }

        false_leads = suggester._detect_false_leads(evidence, {})

        # Should NOT flag vendor claim (production_usage confirms it)
        vendor_leads = [fl for fl in false_leads if "vendor" in fl.misleading_signal.lower()]
        assert len(vendor_leads) == 0


# --- JURISDICTION PATTERN TESTS ---

class TestJurisdictionPatterns:
    """Tests for jurisdiction-specific pattern detection."""

    def test_detects_swiss_discretion_pattern(self, temp_knowledge_base):
        """Swiss bank site-restricted searches should be flagged."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        evidence = {
            "bank_id": "ubs",
            "bank_name": "UBS AG",
            "evidence_items": [],
            "null_results": [
                {
                    "category": "Site Search 1",
                    "queries": ["site:ubs.com CDM"],
                    "null_type": "NO_RESULTS",
                    "informative_absence": False
                },
                {
                    "category": "Site Search 2",
                    "queries": ["site:ubs.com ISDA"],
                    "null_type": "NO_RESULTS",
                    "informative_absence": False
                }
            ]
        }

        patterns = suggester._detect_jurisdiction_patterns(evidence)

        # Should detect Swiss jurisdiction pattern
        swiss_pattern = next((p for p in patterns if "Swiss" in p.jurisdiction), None)
        assert swiss_pattern is not None

    def test_suggests_appropriate_alternatives(self, temp_knowledge_base):
        """Jurisdiction patterns should suggest better alternatives."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        alt = suggester._suggest_jurisdiction_alternative("Swiss")
        assert "ISDA" in alt or "trade press" in alt or "discretion" in alt

        alt = suggester._suggest_jurisdiction_alternative("German")
        assert "German" in alt


# --- FORMATTING TESTS ---

class TestFormatting:
    """Tests for suggestion formatting."""

    def test_dead_end_table_format(self, temp_knowledge_base):
        """Dead ends should format as markdown tables."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        pattern = NullSearchPattern(
            queries=["test query CDM"],
            category="Test Category",
            bank_id="test-bank",
            null_type="NO_RESULTS",
            times_tried=3,
            informative_absence=False,
            implication="No results",
            time_wasted_minutes=60
        )

        suggestion = suggester._format_dead_end_suggestion(pattern)

        assert suggestion is not None
        assert suggestion.section == 'A'
        assert '|' in suggestion.content  # Table format
        assert 'test query' in suggestion.content.lower()

    def test_false_lead_bullet_format(self, temp_knowledge_base):
        """False leads should format with bullet points."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        lead = FalseLead(
            misleading_signal="Test signal",
            reality="Test reality",
            why_confuses="Test confusion reason",
            lesson="Test lesson",
            banks_affected=["bank1", "bank2"],
            time_wasted_minutes=30,
            pattern_name="Test Pattern"
        )

        suggestion = suggester._format_false_lead_suggestion(lead)

        assert suggestion is not None
        assert suggestion.section == 'B'
        assert "**Misleading Signal**" in suggestion.content
        assert "**Reality**" in suggestion.content
        assert "**Lesson**" in suggestion.content
        assert "bank1" in suggestion.content


# --- DUPLICATE AVOIDANCE TESTS ---

class TestDuplicateAvoidance:
    """Tests for duplicate detection."""

    def test_detects_exact_duplicate(self, temp_knowledge_base):
        """Exact matches to existing patterns should be flagged."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        # This pattern exists in the sample negative_facts.md
        suggestion = Suggestion(
            section='A',
            content='| `"[Bank] derivatives reporting"` | Too vague | Better |',
            confidence=0.8,
            source_bank="test",
            pattern_key="derivatives_reporting"
        )

        assert suggester._is_duplicate(suggestion) is True

    def test_detects_fuzzy_duplicate(self, temp_knowledge_base):
        """Similar patterns (50%+ word overlap) should be flagged."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        # Similar to "Fluxnova != CDM" in sample
        suggestion = Suggestion(
            section='B',
            content='FINOS Fluxnova project participation misleading',
            confidence=0.7,
            source_bank="test",
            pattern_key="fluxnova"
        )

        assert suggester._is_duplicate(suggestion) is True

    def test_allows_novel_patterns(self, temp_knowledge_base):
        """Genuinely new patterns should not be flagged."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)

        suggestion = Suggestion(
            section='A',
            content='| `"completely novel search pattern xyz"` | New reason | Alternative |',
            confidence=0.8,
            source_bank="test",
            pattern_key="novel_pattern"
        )

        assert suggester._is_duplicate(suggestion) is False


# --- CROSS-BANK CORRELATION TESTS ---

class TestCrossBankCorrelation:
    """Tests for phase-level cross-bank analysis."""

    def test_correlates_across_multiple_banks(self):
        """Patterns in 2+ banks should have higher confidence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            phase_dir = Path(tmpdir)

            # Create two bank directories with similar null results
            for bank_id in ["bank1", "bank2"]:
                bank_dir = phase_dir / bank_id
                bank_dir.mkdir()

                evidence = {
                    "bank_id": bank_id,
                    "evidence_items": [],
                    "null_results": [
                        {
                            "category": "Common Dead End",
                            "queries": ["common search query"],
                            "results_reviewed": 30,
                            "null_type": "NO_RESULTS",
                            "informative_absence": False
                        }
                    ]
                }

                (bank_dir / "evidence.json").write_text(json.dumps(evidence))

            # Create temporary knowledge base
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write("# Negative Facts\n\n## A. Dead Ends\n\n---\n\n## G. Phase Patterns\n\n---\n")
                kb_path = Path(f.name)

            suggester = NegativeFactsSuggester(knowledge_base_path=kb_path)
            suggestions = suggester.analyze_phase(phase_dir)

            # Should find cross-bank pattern
            cross_bank = [s for s in suggestions if s.section == 'G']
            assert len(cross_bank) >= 1

            # Cross-bank suggestions should mention both banks
            for s in cross_bank:
                assert "bank1" in s.source_bank or "bank2" in s.source_bank


# --- INTEGRATION TESTS ---

class TestBankAnalysis:
    """Integration tests for full bank analysis."""

    def test_analyze_bank_returns_suggestions(self, temp_bank_dir, temp_knowledge_base):
        """analyze_bank should return a list of suggestions."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)
        suggestions = suggester.analyze_bank(temp_bank_dir)

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

        # Each suggestion should have required fields
        for s in suggestions:
            assert hasattr(s, 'section')
            assert hasattr(s, 'content')
            assert hasattr(s, 'confidence')
            assert 0 <= s.confidence <= 1

    def test_handles_missing_evidence_json(self, temp_knowledge_base):
        """Should gracefully handle missing evidence.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)
            suggestions = suggester.analyze_bank(Path(tmpdir))

            assert suggestions == []

    def test_saves_suggestions_to_file(self, temp_bank_dir, temp_knowledge_base):
        """Suggestions should be saveable to JSON."""
        suggester = NegativeFactsSuggester(knowledge_base_path=temp_knowledge_base)
        suggestions = suggester.analyze_bank(temp_bank_dir)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_path = Path(f.name)

        suggester.save_suggestions_to_file(suggestions, output_path)

        # Verify file was created and is valid JSON
        assert output_path.exists()
        with open(output_path) as f:
            data = json.load(f)

        assert 'suggestions' in data
        assert 'generated_at' in data
        assert len(data['suggestions']) == len(suggestions)


# --- CLI TESTS ---

class TestCLI:
    """Tests for CLI functionality."""

    def test_print_suggestions_handles_empty(self, capsys):
        """print_suggestions should handle empty list."""
        from suggest_negative_facts import print_suggestions
        print_suggestions([])
        captured = capsys.readouterr()
        assert "No suggestions found" in captured.out

    def test_print_suggestions_groups_by_section(self, capsys):
        """print_suggestions should group by section."""
        from suggest_negative_facts import print_suggestions

        suggestions = [
            Suggestion(section='A', content='Dead end 1', confidence=0.8, source_bank='bank1'),
            Suggestion(section='A', content='Dead end 2', confidence=0.7, source_bank='bank2'),
            Suggestion(section='B', content='False lead 1', confidence=0.6, source_bank='bank1'),
        ]

        print_suggestions(suggestions)
        captured = capsys.readouterr()

        assert "[Section A:" in captured.out
        assert "[Section B:" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
