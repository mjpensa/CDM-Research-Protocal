#!/usr/bin/env python3
"""
Document Standardization Tool for CDM/DRR Research Protocol

Standardizes all 434 markdown files across 31 banks to consistent hybrid templates.
Eliminates structural variations while preserving all content.

Usage:
    python tools/standardize_documents.py --bank deutsche-bank --dry-run
    python tools/standardize_documents.py --bank deutsche-bank
    python tools/standardize_documents.py --phase 1
    python tools/standardize_documents.py --all
    python tools/standardize_documents.py --bank deutsche-bank --rollback
"""

import argparse
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Bank ID to prefix mapping for evidence ID standardization
BANK_PREFIX_MAP = {
    "deutsche-bank": "DB",
    "societe-generale": "SG",
    "ubs": "UBS",
    "barclays": "BARC",
    "hsbc": "HSBC",
    "natwest": "NW",
    "lloyds": "LBG",
    "nomura": "NOM",
    "mufg": "MUFG",
    "mizuho": "MIZ",
    "smbc": "SMBC",
    "ing": "ING",
    "credit-agricole": "CA",
    "unicredit": "UC",
    "commerzbank": "CBK",
    "santander": "SAN",
    "bbva": "BBVA",
    "standard-chartered": "SC",
    "pictet": "PIC",
    "dbs": "DBS",
    "icbc": "ICBC",
    "bank-of-china": "BOC",
    "ccb": "CCB",
    "abc": "ABC",
    "jpmorgan": "JPM",
    "goldman-sachs": "GS",
    "morgan-stanley": "MS",
    "citigroup": "CITI",
    "bank-of-america": "BAC",
    "state-street": "STT",
    "bny-mellon": "BNY",
}

# File types to process
FILE_TYPES = {
    "1-evidence": ["tier1-evidence.md", "tier2-evidence.md", "tier3-evidence.md", "null-results.md"],
    "2-bayesian": ["post-tier1-update.md", "post-tier2-update.md", "post-tier3-update.md"],
    "3-gates": ["pre-mortem.md", "gate-1.md", "gate-2.md", "gate-3.md"],
    "4-adversarial": ["counter-case.md", "steelman.md", "verdict.md"],
    "5-synthesis": ["assessment.md"],
}

# Phase directories (must match actual filesystem structure in outputs/)
PHASE_DIRS = {
    1: "phase-1-european-tier1",
    2: "phase-2-uk-regional",
    3: "phase-3-japanese",
    4: "phase-4-other-european",
    5: "phase-5-spanish",
    6: "phase-6-deep-dives",
    7: "phase-7-emerging-markets",
    8: "phase-8-us-investment-banks",
    9: "phase-9-us-custody-banks",
}


# ==============================================================================
# DATA CLASSES
# ==============================================================================

@dataclass
class BankInfo:
    """Bank metadata from manifest"""
    bank_id: str
    bank_name: str
    phase: int
    phase_name: str
    headquarters: str = ""
    region: str = ""


@dataclass
class ProbabilityState:
    """Probability state extracted from documents"""
    p_architect: float = 0.0
    p_pragmatist: float = 0.0
    confidence: float = 0.0


@dataclass
class EvidenceBlock:
    """Single evidence item"""
    id: str
    tier: int
    title: str = ""
    source_url: str = ""
    date: str = ""
    claim_type: str = ""
    direction: str = ""
    lr_value: float = 1.0
    excerpt: str = ""
    analysis: str = ""
    authority: str = ""
    recency: str = ""
    specificity: str = ""
    caveats: str = ""


@dataclass
class ExtractedData:
    """All data extracted from a document"""
    bank_info: BankInfo
    probability_state: Optional[ProbabilityState] = None
    evidence_blocks: List[EvidenceBlock] = field(default_factory=list)
    null_results: List[Dict] = field(default_factory=list)
    trajectory: List[Dict] = field(default_factory=list)
    classification: str = ""
    sub_classification: str = ""
    sections: Dict[str, str] = field(default_factory=dict)
    raw_content: str = ""


# ==============================================================================
# EXTRACTION CLASSES
# ==============================================================================

class ContentExtractor:
    """Extracts structured data from markdown documents"""

    @staticmethod
    def extract_probability_state(content: str) -> Optional[ProbabilityState]:
        """Extract probability values from tables or inline text"""
        state = ProbabilityState()

        # Pattern 1: Table format
        table_patterns = [
            r'\|\s*P\(ARCHITECT\)\s*\|\s*(\d+(?:\.\d+)?)\s*%?\s*\|',
            r'\|\s*P\(PRAGMATIST\)\s*\|\s*(\d+(?:\.\d+)?)\s*%?\s*\|',
            r'\|\s*Confidence\s*\|\s*(\d+(?:\.\d+)?)\s*%?\s*\|',
        ]

        for i, pattern in enumerate(table_patterns):
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                if i == 0:
                    state.p_architect = value
                elif i == 1:
                    state.p_pragmatist = value
                else:
                    state.confidence = value

        # Pattern 2: Inline format "P(ARCHITECT) = 25%"
        inline_patterns = [
            (r'P\(ARCHITECT\)\s*[=:]\s*(\d+(?:\.\d+)?)\s*%?', 'p_architect'),
            (r'P\(PRAGMATIST\)\s*[=:]\s*(\d+(?:\.\d+)?)\s*%?', 'p_pragmatist'),
            (r'[Cc]onfidence\s*[=:]\s*(\d+(?:\.\d+)?)\s*%?', 'confidence'),
        ]

        for pattern, attr in inline_patterns:
            match = re.search(pattern, content)
            if match and getattr(state, attr) == 0.0:
                setattr(state, attr, float(match.group(1)))

        # Pattern 3: Phase 8 format - "ARCHITECT (Native) at 90% confidence"
        phase8_match = re.search(
            r'(ARCHITECT|PRAGMATIST)\s*\([^)]+\)\s*at\s*(\d+)%\s*confidence',
            content, re.IGNORECASE
        )
        if phase8_match:
            if phase8_match.group(1).upper() == 'ARCHITECT':
                state.p_architect = 90
                state.p_pragmatist = 10
            else:
                state.p_architect = 10
                state.p_pragmatist = 90
            state.confidence = float(phase8_match.group(2))

        # Pattern 4: Phase 8 format - "Final Confidence: [X]%" with placeholder
        final_conf_match = re.search(r'\*\*Final Confidence\*\*:\s*\[?X?\]?%?', content)
        if final_conf_match and state.confidence == 0.0:
            # Placeholder means no confidence yet - use default
            state.confidence = 50

        return state if state.p_architect > 0 or state.p_pragmatist > 0 or state.confidence > 0 else None

    @staticmethod
    def extract_evidence_blocks(content: str, bank_id: str) -> List[EvidenceBlock]:
        """Extract evidence blocks from various formats"""
        blocks = []
        prefix = BANK_PREFIX_MAP.get(bank_id, bank_id.upper()[:3])

        # Pattern 1: [DB-001] TIER 1 — DIRECTION
        pattern1 = r'\[([A-Z]+-\d+)\]\s*TIER\s*(\d)\s*[—-]\s*(\w+(?:\s+\w+)?)'
        for match in re.finditer(pattern1, content):
            blocks.append(EvidenceBlock(
                id=match.group(1),
                tier=int(match.group(2)),
                direction=match.group(3).strip()
            ))

        # Pattern 2: ### ID: Title
        pattern2 = r'###\s*([A-Z]+-\d+|E\d+|[A-Z]+\d+):\s*(.+?)(?:\n|$)'
        for match in re.finditer(pattern2, content):
            raw_id = match.group(1)
            # Standardize ID format
            if not '-' in raw_id:
                # E001 -> DB-001 style
                num_match = re.search(r'(\d+)', raw_id)
                if num_match:
                    std_id = f"{prefix}-{num_match.group(1).zfill(3)}"
                else:
                    std_id = raw_id
            else:
                std_id = raw_id
            blocks.append(EvidenceBlock(
                id=std_id,
                tier=1,  # Will be updated from context
                title=match.group(2).strip()
            ))

        return blocks

    @staticmethod
    def extract_classification(content: str) -> Tuple[str, str]:
        """Extract classification and sub-classification"""
        classification = ""
        sub_classification = ""

        # Pattern 1: Table format | Classification | PRAGMATIST |
        table_match = re.search(
            r'\|\s*Classification\s*\|\s*\*?\*?(ARCHITECT|PRAGMATIST|OBSERVER|UNKNOWN)\*?\*?\s*\|',
            content, re.IGNORECASE
        )
        if table_match:
            classification = table_match.group(1).upper()

        # Pattern 2: Inline format - **Classification**: PRAGMATIST or Classification: ARCHITECT
        if not classification:
            inline_match = re.search(
                r'\*?\*?[Cc]lassification\*?\*?[:\s]+\*?\*?(ARCHITECT|PRAGMATIST|OBSERVER|UNKNOWN)\*?\*?',
                content
            )
            if inline_match:
                classification = inline_match.group(1).upper()

        # Pattern 3: "classified as PRAGMATIST" or "classified as **PRAGMATIST**"
        if not classification:
            prose_match = re.search(
                r'classified as\s+\*?\*?(ARCHITECT|PRAGMATIST|OBSERVER|UNKNOWN)\*?\*?',
                content, re.IGNORECASE
            )
            if prose_match:
                classification = prose_match.group(1).upper()

        # Pattern 4: Phase 8 format - "**Preliminary Classification**: ARCHITECT (Native)"
        if not classification:
            prelim_match = re.search(
                r'\*\*Preliminary Classification\*\*:\s*(ARCHITECT|PRAGMATIST|OBSERVER|UNKNOWN)',
                content, re.IGNORECASE
            )
            if prelim_match:
                classification = prelim_match.group(1).upper()

        # Sub-Classification patterns
        # Pattern 1: Table format | Sub-Classification | Regulatory-Driven |
        sub_table_match = re.search(
            r'\|\s*Sub-?[Cc]lassification\s*\|\s*\*?\*?([A-Za-z-]+)\*?\*?\s*\|',
            content
        )
        if sub_table_match:
            sub_classification = sub_table_match.group(1)

        # Pattern 2: Inline or parenthetical (Regulatory-Driven)
        if not sub_classification:
            paren_match = re.search(
                r'(PRAGMATIST|ARCHITECT)\s*\(([A-Za-z-]+)\)',
                content, re.IGNORECASE
            )
            if paren_match:
                sub_classification = paren_match.group(2)

        return classification, sub_classification

    @staticmethod
    def extract_sections(content: str) -> Dict[str, str]:
        """Extract all sections by header, handling numbered sections like '## 1. Bank Profile'"""
        sections = {}
        current_section = None
        current_raw_section = None
        current_content = []

        for line in content.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = ContentExtractor._clean_section_content(
                        '\n'.join(current_content)
                    )
                    # Also store with raw name for fallback
                    if current_raw_section and current_raw_section != current_section:
                        sections[current_raw_section] = sections[current_section]
                # Extract section name, removing leading numbers like "1. " or "14. "
                raw_section = line[3:].strip()
                current_raw_section = raw_section
                # Remove leading number and period/colon if present
                section_match = re.match(r'^(\d+\.?\s*)?(.+)$', raw_section)
                if section_match:
                    current_section = section_match.group(2).strip()
                else:
                    current_section = raw_section
                current_content = []
            elif line.startswith('# '):
                if current_section:
                    sections[current_section] = ContentExtractor._clean_section_content(
                        '\n'.join(current_content)
                    )
                    if current_raw_section and current_raw_section != current_section:
                        sections[current_raw_section] = sections[current_section]
                current_section = None
                current_raw_section = None
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = ContentExtractor._clean_section_content(
                '\n'.join(current_content)
            )
            if current_raw_section and current_raw_section != current_section:
                sections[current_raw_section] = sections[current_section]

        return sections

    @staticmethod
    def _clean_section_content(content: str) -> str:
        """Clean trailing footers and separators from section content"""
        # Strip trailing whitespace
        content = content.rstrip()

        # Remove trailing footer patterns like:
        # ---
        # *Gate X passed...*
        # or
        # ---
        # *Assessment complete...*
        footer_pattern = r'\n*---\s*\n+\*[^*]+\*\s*$'
        content = re.sub(footer_pattern, '', content)

        # Also remove standalone --- at the end
        if content.rstrip().endswith('---'):
            content = content.rstrip()[:-3].rstrip()

        return content.strip()

    @staticmethod
    def extract_trajectory(content: str) -> List[Dict]:
        """Extract probability trajectory from tables"""
        trajectory = []

        # Pattern: | Stage | P(ARCHITECT) | Change |
        pattern = r'\|\s*(Prior|Post-Tier\s*\d)\s*\|\s*(\d+(?:\.\d+)?)\s*%?\s*\|\s*([+-]?\d+(?:\.\d+)?%?|[-–—])\s*\|'
        for match in re.finditer(pattern, content, re.IGNORECASE):
            stage = match.group(1).strip()
            p_arch = float(match.group(2))
            change = match.group(3).strip()
            if change in ['-', '–', '—']:
                change = '-'
            trajectory.append({
                'stage': stage,
                'p_architect': p_arch,
                'change': change
            })

        return trajectory


# ==============================================================================
# TEMPLATE CLASSES
# ==============================================================================

class DocumentTemplate:
    """Base class for document templates"""

    def __init__(self, bank_info: BankInfo):
        self.bank_info = bank_info
        self.date = datetime.now().strftime("%Y-%m-%d")

    def render_header(self, title: str) -> str:
        """Render standard header"""
        return f"""# {title}: {self.bank_info.bank_name}

**Bank:** {self.bank_info.bank_name}
**Phase:** {self.bank_info.phase} - {self.bank_info.phase_name}
**Date:** {self.date}

---
"""

    def render_probability_table(self, state: ProbabilityState) -> str:
        """Render probability state table"""
        return f"""
| Metric | Value |
|--------|-------|
| P(ARCHITECT) | {state.p_architect:.0f}% |
| P(PRAGMATIST) | {state.p_pragmatist:.0f}% |
| Confidence | {state.confidence:.0f}% |
"""

    def render_na_section(self, section_name: str) -> str:
        """Render N/A section when content is missing"""
        return f"""
## {section_name}

N/A
"""

    def extract(self, content: str) -> ExtractedData:
        """Extract data from content - override in subclasses"""
        raise NotImplementedError

    def render(self, data: ExtractedData) -> str:
        """Render standardized content - override in subclasses"""
        raise NotImplementedError


class GateTemplate(DocumentTemplate):
    """Template for gate files (gate-1, gate-2, gate-3)"""

    def __init__(self, bank_info: BankInfo, gate_num: int):
        super().__init__(bank_info)
        self.gate_num = gate_num

    def extract(self, content: str) -> ExtractedData:
        data = ExtractedData(bank_info=self.bank_info, raw_content=content)
        data.probability_state = ContentExtractor.extract_probability_state(content)
        data.sections = ContentExtractor.extract_sections(content)
        data.trajectory = ContentExtractor.extract_trajectory(content)

        # Handle Phase 8 alternate format: extract phase from "Research Phase" header
        phase_match = re.search(r'\*\*Research Phase\*\*:\s*(\d+)', content)
        if phase_match and self.bank_info.phase == 0:
            self.bank_info.phase = int(phase_match.group(1))

        return data

    def render(self, data: ExtractedData) -> str:
        gate_titles = {
            1: "Reasoning Gate 1: Post-Tier 1 Assessment",
            2: "Reasoning Gate 2: Post-Tier 2 Assessment",
            3: "Reasoning Gate 3: Pre-Adversarial Assessment"
        }

        output = self.render_header(gate_titles.get(self.gate_num, f"Gate {self.gate_num}"))

        # Current Probability State
        output += "\n## Current Probability State\n"
        if data.probability_state:
            output += self.render_probability_table(data.probability_state)
        else:
            output += "\nN/A\n"

        # Gate Decision Criteria
        output += "\n## Gate Decision Criteria\n\n"
        if "Gate Decision Criteria" in data.sections:
            output += data.sections["Gate Decision Criteria"] + "\n"
        else:
            output += "Per `config/decision-thresholds.json`:\n"
            output += "- Skip to adversarial if P(ARCHITECT) > 80% OR P(ARCHITECT) < 20%\n"
            if data.probability_state:
                p = data.probability_state.p_architect
                if p > 80:
                    output += f"- Current P(ARCHITECT) = {p:.0f}% → **Above 80% threshold**\n"
                elif p < 20:
                    output += f"- Current P(ARCHITECT) = {p:.0f}% → **Below 20% threshold**\n"
                else:
                    output += f"- Current P(ARCHITECT) = {p:.0f}% → **Within 20-80% range**\n"

        # Decision
        output += "\n## Decision: "
        if "Decision" in data.sections:
            # Extract just the decision line
            decision_content = data.sections["Decision"]
            output += decision_content.split('\n')[0] if decision_content else "PROCEED"
            output += "\n\n"
            if '\n' in decision_content:
                output += '\n'.join(decision_content.split('\n')[1:]) + "\n"
        else:
            tier_next = self.gate_num + 1 if self.gate_num < 3 else "ADVERSARIAL"
            output += f"PROCEED TO TIER {tier_next}\n\n"
            output += "**Rationale**: Per protocol to process all tiers.\n"

        # Evidence Trajectory (for gate 2 and 3)
        if self.gate_num >= 2:
            output += "\n## Evidence Trajectory Analysis\n"
            if data.trajectory:
                output += "\n| Stage | P(ARCHITECT) | Change |\n"
                output += "|-------|--------------|--------|\n"
                for t in data.trajectory:
                    output += f"| {t['stage']} | {t['p_architect']:.0f}% | {t['change']} |\n"
            elif "Evidence Trajectory" in data.sections:
                output += "\n" + data.sections["Evidence Trajectory"] + "\n"
            else:
                output += "\nN/A\n"

        # Evidence Quality Assessment
        output += "\n## Evidence Quality Assessment\n"
        if "Evidence Quality Assessment" in data.sections:
            output += "\n" + data.sections["Evidence Quality Assessment"] + "\n"
        elif "Strengths" in data.sections or "Weaknesses" in data.sections:
            if "Strengths" in data.sections:
                output += "\n### Strengths\n" + data.sections["Strengths"] + "\n"
            if "Weaknesses" in data.sections:
                output += "\n### Weaknesses\n" + data.sections["Weaknesses"] + "\n"
        else:
            output += "\nN/A\n"

        # Key Questions
        tier_label = "Tier 2" if self.gate_num == 1 else ("Tier 3" if self.gate_num == 2 else "Adversarial")
        output += f"\n## Key Questions for {tier_label}\n"

        for section_name in data.sections:
            if "Questions" in section_name or "Key Questions" in section_name:
                output += "\n" + data.sections[section_name] + "\n"
                break
        else:
            output += "\nN/A\n"

        # Framework Claim Assessment (if present)
        if "Framework Claim" in str(data.sections):
            for section_name in data.sections:
                if "Framework" in section_name:
                    output += f"\n## {section_name}\n"
                    output += "\n" + data.sections[section_name] + "\n"
                    break

        # Footer
        output += "\n---\n\n"
        output += f"*Gate {self.gate_num} passed. Proceeding to {tier_label.lower()} evidence gathering.*\n"

        return output


class PreMortemTemplate(DocumentTemplate):
    """Template for pre-mortem files"""

    def extract(self, content: str) -> ExtractedData:
        data = ExtractedData(bank_info=self.bank_info, raw_content=content)
        data.sections = ContentExtractor.extract_sections(content)

        # Handle Phase 8 alternate format: extract phase from "Research Phase" header
        phase_match = re.search(r'\*\*Research Phase\*\*:\s*(\d+)', content)
        if phase_match and self.bank_info.phase == 0:
            self.bank_info.phase = int(phase_match.group(1))

        return data

    def render(self, data: ExtractedData) -> str:
        output = self.render_header("Pre-Mortem Analysis")

        # Research Objective
        output += "\n## Research Objective\n"
        if "Research Objective" in data.sections:
            output += "\n" + data.sections["Research Objective"] + "\n"
        else:
            output += f"\nAssess {self.bank_info.bank_name}'s CDM/DRR adoption maturity.\n"

        # Potential Failure Modes
        output += "\n## Potential Failure Modes\n"
        if "Potential Failure Modes" in data.sections:
            output += "\n" + data.sections["Potential Failure Modes"] + "\n"
        elif "Failure Modes" in data.sections:
            output += "\n" + data.sections["Failure Modes"] + "\n"
        else:
            output += """
| Risk | Description | Mitigation |
|------|-------------|------------|
| False Positive | Overstating CDM engagement | Require Tier 1 corroboration |
| False Negative | Missing silent implementation | Check job postings, LinkedIn |
| Stale Evidence | Outdated information | Apply temporal weighting |
"""

        # Search Strategy
        output += "\n## Search Strategy\n"
        if "Search Strategy" in data.sections:
            output += "\n" + data.sections["Search Strategy"] + "\n"
        else:
            output += """
### Tier 1 (Official Sources)
- Bank official website, annual reports
- ISDA.org, FINOS.org
- Regulatory filings

### Tier 2 (Industry Sources)
- Risk.net, Waters Technology
- Trade press coverage
- Vendor announcements

### Tier 3 (Signal Sources)
- Job postings
- LinkedIn profiles
- Conference presentations
"""

        # Key Hypotheses
        output += "\n## Key Hypotheses to Test\n"
        if "Key Hypotheses" in data.sections:
            output += "\n" + data.sections["Key Hypotheses"] + "\n"
        elif "Hypotheses" in data.sections:
            output += "\n" + data.sections["Hypotheses"] + "\n"
        else:
            output += "\nN/A\n"

        # Decision Points
        output += "\n## Decision Points\n"
        if "Decision Points" in data.sections:
            output += "\n" + data.sections["Decision Points"] + "\n"
        else:
            output += """
1. After Tier 1: If P(ARCHITECT) < 20% or > 80%, consider early classification
2. After Tier 2: Assess if Tier 3 signals will add value
3. After Tier 3: Proceed to adversarial challenge
"""

        # Null Hypothesis
        output += "\n## Null Hypothesis Reminder\n"
        if "Null Hypothesis" in data.sections:
            output += "\n" + data.sections["Null Hypothesis"] + "\n"
        else:
            output += f"\nAssume {self.bank_info.bank_name} is PRAGMATIST until evidence proves otherwise.\n"

        output += "\n---\n"
        return output


class BayesianTemplate(DocumentTemplate):
    """Template for Bayesian update files"""

    def __init__(self, bank_info: BankInfo, tier_num: int):
        super().__init__(bank_info)
        self.tier_num = tier_num

    def extract(self, content: str) -> ExtractedData:
        data = ExtractedData(bank_info=self.bank_info, raw_content=content)
        data.probability_state = ContentExtractor.extract_probability_state(content)
        data.sections = ContentExtractor.extract_sections(content)
        data.evidence_blocks = ContentExtractor.extract_evidence_blocks(content, self.bank_info.bank_id)

        # Handle Phase 8 alternate format: extract phase from "Research Phase" header
        phase_match = re.search(r'\*\*Research Phase\*\*:\s*(\d+)', content)
        if phase_match and self.bank_info.phase == 0:
            self.bank_info.phase = int(phase_match.group(1))

        # Handle Phase 8 "Null Hypothesis: PRAGMATIST" format
        null_match = re.search(r'\*\*Null Hypothesis\*\*:\s*(PRAGMATIST|ARCHITECT)', content, re.IGNORECASE)
        if null_match and not data.probability_state:
            data.probability_state = ProbabilityState()
            if null_match.group(1).upper() == 'PRAGMATIST':
                data.probability_state.p_architect = 25
                data.probability_state.p_pragmatist = 75
            else:
                data.probability_state.p_architect = 75
                data.probability_state.p_pragmatist = 25

        return data

    def render(self, data: ExtractedData) -> str:
        output = self.render_header(f"Bayesian Update: Post-Tier {self.tier_num} Evidence")

        # Prior Probability
        output += "\n## Prior Probability\n"
        if "Prior Probability" in data.sections:
            output += "\n" + data.sections["Prior Probability"] + "\n"
        elif "Prior" in data.sections:
            output += "\n" + data.sections["Prior"] + "\n"
        else:
            prior = 25 if self.tier_num == 1 else (data.probability_state.p_architect if data.probability_state else 20)
            output += f"\nP(ARCHITECT) prior: {prior:.0f}%\n"

        # Evidence Summary
        output += f"\n## Tier {self.tier_num} Evidence Summary\n"
        if f"Tier {self.tier_num} Evidence" in data.sections:
            output += "\n" + data.sections[f"Tier {self.tier_num} Evidence"] + "\n"
        elif "Evidence Summary" in data.sections:
            output += "\n" + data.sections["Evidence Summary"] + "\n"
        elif data.evidence_blocks:
            output += "\n| ID | Description | Direction | LR |\n"
            output += "|----|----|-------|----|\n"
            for e in data.evidence_blocks:
                output += f"| {e.id} | {e.title or 'Evidence'} | {e.direction or 'NEUTRAL'} | {e.lr_value} |\n"
        else:
            output += "\nNo Tier " + str(self.tier_num) + " evidence found.\n"

        # Likelihood Ratio Calculation
        output += "\n## Likelihood Ratio Calculation\n"
        if "Likelihood Ratio" in data.sections:
            output += "\n" + data.sections["Likelihood Ratio"] + "\n"
        elif "LR Calculation" in data.sections:
            output += "\n" + data.sections["LR Calculation"] + "\n"
        else:
            output += "\n```\nCombined LR = 1.0 (no evidence)\n```\n"

        # Posterior Calculation
        output += "\n## Posterior Calculation\n"
        if "Posterior Calculation" in data.sections:
            output += "\n" + data.sections["Posterior Calculation"] + "\n"
        elif "Posterior" in data.sections:
            output += "\n" + data.sections["Posterior"] + "\n"
        else:
            output += "\n```\nPosterior = Prior (no update)\n```\n"

        # Updated Probabilities
        output += "\n## Updated Probabilities\n"
        if data.probability_state:
            output += self.render_probability_table(data.probability_state)
        else:
            output += "\nN/A\n"

        # Key Insights
        output += "\n## Key Insights\n"
        if "Key Insights" in data.sections:
            output += "\n" + data.sections["Key Insights"] + "\n"
        elif "Insights" in data.sections:
            output += "\n" + data.sections["Insights"] + "\n"
        elif "Interpretation" in data.sections:
            output += "\n" + data.sections["Interpretation"] + "\n"
        else:
            output += "\nN/A\n"

        # Cumulative Evidence (for tier 2 and 3)
        if self.tier_num >= 2:
            output += "\n## Cumulative Evidence Summary\n"
            if "Cumulative" in str(data.sections):
                for section_name in data.sections:
                    if "Cumulative" in section_name:
                        output += "\n" + data.sections[section_name] + "\n"
                        break
            else:
                output += "\n| Tier | Combined LR | Cumulative LR |\n"
                output += "|------|-------------|---------------|\n"
                for t in range(1, self.tier_num + 1):
                    output += f"| Tier {t} | 1.0 | 1.0 |\n"

        # Final Confidence (for tier 3)
        if self.tier_num == 3:
            output += "\n## Final Confidence Assessment\n"
            if "Final Confidence" in data.sections:
                output += "\n" + data.sections["Final Confidence"] + "\n"
            elif "Confidence Assessment" in data.sections:
                output += "\n" + data.sections["Confidence Assessment"] + "\n"
            else:
                conf = data.probability_state.confidence if data.probability_state else 50
                output += f"\nFinal confidence: {conf:.0f}%\n"

        output += "\n---\n\n"
        output += f"*Proceeding to {'Tier ' + str(self.tier_num + 1) if self.tier_num < 3 else 'adversarial review'}.*\n"

        return output


class AdversarialTemplate(DocumentTemplate):
    """Template for adversarial files (counter-case, steelman, verdict)"""

    def __init__(self, bank_info: BankInfo, file_type: str):
        super().__init__(bank_info)
        self.file_type = file_type  # 'counter-case', 'steelman', 'verdict'

    def extract(self, content: str) -> ExtractedData:
        data = ExtractedData(bank_info=self.bank_info, raw_content=content)
        data.probability_state = ContentExtractor.extract_probability_state(content)
        data.sections = ContentExtractor.extract_sections(content)
        data.classification, data.sub_classification = ContentExtractor.extract_classification(content)

        # Handle Phase 8 alternate format: extract phase from "Research Phase" header
        phase_match = re.search(r'\*\*Research Phase\*\*:\s*(\d+)', content)
        if phase_match and self.bank_info.phase == 0:
            self.bank_info.phase = int(phase_match.group(1))

        return data

    def render(self, data: ExtractedData) -> str:
        titles = {
            "counter-case": "Counter-Case: Devil's Advocate Analysis",
            "steelman": "Steelman: Strongest Counter-Argument",
            "verdict": "Adversarial Verdict"
        }

        output = self.render_header(titles.get(self.file_type, self.file_type.title()))

        if self.file_type == "counter-case":
            output += self._render_counter_case(data)
        elif self.file_type == "steelman":
            output += self._render_steelman(data)
        elif self.file_type == "verdict":
            output += self._render_verdict(data)

        return output

    def _render_counter_case(self, data: ExtractedData) -> str:
        output = ""

        # Thesis
        output += "\n## Thesis Under Challenge\n"
        if "Thesis" in data.sections:
            output += "\n" + data.sections["Thesis"] + "\n"
        else:
            output += f"\nPreliminary classification: {data.classification or 'PRAGMATIST'}\n"

        # Counter-Arguments
        output += "\n## Counter-Arguments\n"

        # Look for numbered arguments
        arg_found = False
        for i in range(1, 6):
            for section_name in data.sections:
                if f"Argument {i}" in section_name or f"Counter-Argument {i}" in section_name:
                    output += f"\n### {section_name}\n"
                    output += data.sections[section_name] + "\n"
                    arg_found = True

        if not arg_found:
            if "Counter-Arguments" in data.sections:
                output += "\n" + data.sections["Counter-Arguments"] + "\n"
            elif "Arguments" in data.sections:
                output += "\n" + data.sections["Arguments"] + "\n"
            else:
                output += "\n1. N/A\n"

        # Strength Assessment
        output += "\n## Counter-Case Strength Assessment\n"
        if "Strength" in data.sections:
            output += "\n" + data.sections["Strength"] + "\n"
        elif "Assessment" in data.sections:
            output += "\n" + data.sections["Assessment"] + "\n"
        else:
            output += "\n**Strength**: WEAK\n"
            output += "\nCounter-arguments do not warrant reclassification.\n"

        output += "\n---\n"
        return output

    def _render_steelman(self, data: ExtractedData) -> str:
        output = ""

        # Hypothesis Name
        output += "\n## Strongest Counter-Hypothesis\n"
        for section_name in data.sections:
            if "Hypothesis" in section_name or "Strongest" in section_name:
                output += "\n" + data.sections[section_name] + "\n"
                break
        else:
            output += "\nN/A\n"

        # Supporting Logic
        output += "\n## Supporting Logic\n"
        if "Supporting Logic" in data.sections:
            output += "\n" + data.sections["Supporting Logic"] + "\n"
        elif "Supporting" in data.sections:
            output += "\n" + data.sections["Supporting"] + "\n"
        else:
            output += "\nN/A\n"

        # Why It Fails
        output += "\n## Why This Argument Fails\n"
        if "Why" in str(data.sections) and "Fail" in str(data.sections):
            for section_name in data.sections:
                if "Fail" in section_name:
                    output += "\n" + data.sections[section_name] + "\n"
                    break
        else:
            output += "\nN/A\n"

        # Grade
        output += "\n## Steelman Assessment\n"
        if "Steelman Assessment" in data.sections:
            output += "\n" + data.sections["Steelman Assessment"] + "\n"
        elif "Grade" in data.sections:
            output += "\n" + data.sections["Grade"] + "\n"
        else:
            output += "\n**Grade**: 2/5 (Weak)\n"

        output += "\n---\n"
        return output

    def _render_verdict(self, data: ExtractedData) -> str:
        output = ""

        # Final Classification Table
        output += "\n## Final Classification\n"
        output += f"""
| Element | Value |
|---------|-------|
| Classification | {data.classification or 'PRAGMATIST'} |
| Sub-Classification | {data.sub_classification or 'N/A'} |
| Confidence | {data.probability_state.confidence if data.probability_state else 50:.0f}% |
| P(ARCHITECT) | {data.probability_state.p_architect if data.probability_state else 20:.0f}% |
| P(PRAGMATIST) | {data.probability_state.p_pragmatist if data.probability_state else 80:.0f}% |
"""

        # Verdict Rationale
        output += "\n## Verdict Rationale\n"
        if "Verdict Rationale" in data.sections:
            output += "\n" + data.sections["Verdict Rationale"] + "\n"
        elif "Rationale" in data.sections:
            output += "\n" + data.sections["Rationale"] + "\n"
        else:
            output += "\nN/A\n"

        # Sub-Classification Justification
        output += "\n## Sub-Classification Justification\n"
        if "Sub-Classification" in data.sections:
            output += "\n" + data.sections["Sub-Classification"] + "\n"
        else:
            output += "\nN/A\n"

        # Why Not Other Classifications
        output += "\n## Why Not Other Classifications\n"
        if "Why Not" in str(data.sections):
            for section_name in data.sections:
                if "Why Not" in section_name:
                    output += "\n" + data.sections[section_name] + "\n"
                    break
        else:
            output += """
| Alternative | Reason Rejected |
|-------------|-----------------|
| N/A | N/A |
"""

        # Confidence Assessment
        output += "\n## Confidence Assessment\n"
        if "Confidence" in data.sections:
            output += "\n" + data.sections["Confidence"] + "\n"
        else:
            output += "\nN/A\n"

        # Challenge Status
        output += "\n## Adversarial Challenge Status\n"
        output += "\n**Status**: UPHELD\n"
        output += "\nClassification confirmed after adversarial review.\n"

        output += "\n---\n"
        return output


class EvidenceTemplate(DocumentTemplate):
    """Template for evidence files (tier1, tier2, tier3)"""

    def __init__(self, bank_info: BankInfo, tier_num: int):
        super().__init__(bank_info)
        self.tier_num = tier_num

    def extract(self, content: str) -> ExtractedData:
        data = ExtractedData(bank_info=self.bank_info, raw_content=content)
        data.evidence_blocks = ContentExtractor.extract_evidence_blocks(content, self.bank_info.bank_id)
        data.sections = ContentExtractor.extract_sections(content)

        # Handle Phase 8 alternate format: extract phase from "Research Phase" header
        phase_match = re.search(r'\*\*Research Phase\*\*:\s*(\d+)', content)
        if phase_match and self.bank_info.phase == 0:
            self.bank_info.phase = int(phase_match.group(1))

        return data

    def render(self, data: ExtractedData) -> str:
        output = self.render_header(f"Tier {self.tier_num} Evidence")

        # Search Execution Summary
        output += "\n## Search Execution Summary\n"
        output += f"""
| Metric | Value |
|--------|-------|
| Date | {self.date} |
| Evidence Items Found | {len(data.evidence_blocks)} |
| Schema Version | 4.3 |
"""

        # Evidence Inventory
        output += "\n## Evidence Inventory\n"
        if data.evidence_blocks:
            for block in data.evidence_blocks:
                output += self._render_evidence_block(block)
        elif "Evidence Inventory" in data.sections:
            output += "\n" + data.sections["Evidence Inventory"] + "\n"
        else:
            output += "\nNo Tier " + str(self.tier_num) + " evidence found.\n"

        # Informative Absences
        output += "\n## Informative Absences\n"
        if "Informative Absences" in data.sections:
            output += "\n" + data.sections["Informative Absences"] + "\n"
        elif "Absences" in data.sections:
            output += "\n" + data.sections["Absences"] + "\n"
        else:
            output += "\nN/A\n"

        output += "\n---\n"
        return output

    def _render_evidence_block(self, block: EvidenceBlock) -> str:
        return f"""
### {block.id}: {block.title or 'Evidence Item'}

| Field | Value |
|-------|-------|
| Source | {block.source_url or 'N/A'} |
| Date | {block.date or 'N/A'} |
| Tier | {block.tier} |
| Claim Type | {block.claim_type or 'N/A'} |
| Direction | {block.direction or 'NEUTRAL'} |
| LR | {block.lr_value} |

**Excerpt:** {block.excerpt or 'N/A'}

**Analysis:** {block.analysis or 'N/A'}

**Quality Assessment:**
- Authority: {block.authority or 'N/A'}
- Recency: {block.recency or 'N/A'}
- Specificity: {block.specificity or 'N/A'}

**Caveats:** {block.caveats or 'N/A'}
"""


class NullResultsTemplate(DocumentTemplate):
    """Template for null-results files"""

    def extract(self, content: str) -> ExtractedData:
        data = ExtractedData(bank_info=self.bank_info, raw_content=content)
        data.sections = ContentExtractor.extract_sections(content)

        # Handle Phase 8 alternate format: extract phase from "Research Phase" header
        phase_match = re.search(r'\*\*Research Phase\*\*:\s*(\d+)', content)
        if phase_match and self.bank_info.phase == 0:
            self.bank_info.phase = int(phase_match.group(1))

        return data

    def render(self, data: ExtractedData) -> str:
        output = self.render_header("Null Results Registry")

        # Summary
        output += "\n## Summary\n"
        if "Summary" in data.sections:
            output += "\n" + data.sections["Summary"] + "\n"
        else:
            output += "\nNull results documented from exhaustive search.\n"

        # Null Results by Tier
        for tier in [1, 2, 3]:
            output += f"\n## Tier {tier} Null Results\n"
            section_found = False
            for section_name in data.sections:
                if f"Tier {tier}" in section_name:
                    output += "\n" + data.sections[section_name] + "\n"
                    section_found = True
                    break
            if not section_found:
                output += "\nN/A\n"

        # Implications
        output += "\n## Implications for Classification\n"
        if "Implications" in data.sections:
            output += "\n" + data.sections["Implications"] + "\n"
        elif "Classification" in data.sections:
            output += "\n" + data.sections["Classification"] + "\n"
        else:
            output += "\nInformative absence supports PRAGMATIST classification.\n"

        output += "\n---\n"
        return output


class AssessmentTemplate(DocumentTemplate):
    """Template for assessment files - preserves all original sections"""

    # Core sections that must appear in order
    CORE_SECTIONS = [
        "Executive Summary",
        "Bank Profile",
        "Classification Summary",
        "Evidence Inventory",
        "Probability Trajectory",
    ]

    # Additional sections to look for (will be included if present)
    OPTIONAL_SECTIONS = [
        "Null Results",
        "Bayesian Analysis Summary",
        "FINOS Paradox Analysis",
        "Regulatory Compliance Assessment",
        "Vendor Relationship Analysis",
        "Counterparty Network Analysis",
        "Product Coverage Assessment",
        "Knowledge Gaps",
        "Framework Claim Validation",
        "Competitive Positioning",
        "Adoption Drivers Analysis",
        "Risk Factors",
        "Forward-Looking Assessment",
        "Recommendations",
        "Confidence Calibration",
        "Appendix: Source URLs",
    ]

    def extract(self, content: str) -> ExtractedData:
        data = ExtractedData(bank_info=self.bank_info, raw_content=content)
        data.probability_state = ContentExtractor.extract_probability_state(content)
        data.sections = ContentExtractor.extract_sections(content)
        data.classification, data.sub_classification = ContentExtractor.extract_classification(content)
        data.trajectory = ContentExtractor.extract_trajectory(content)

        # Handle Phase 8 alternate format: extract phase from "Research Phase" header
        phase_match = re.search(r'\*\*Research Phase\*\*:\s*(\d+)', content)
        if phase_match and self.bank_info.phase == 0:
            self.bank_info.phase = int(phase_match.group(1))

        return data

    def render(self, data: ExtractedData) -> str:
        output = self.render_header("CDM/DRR Assessment")
        rendered_sections = set()

        # Executive Summary
        output += "\n## Executive Summary\n"
        if "Executive Summary" in data.sections:
            output += "\n" + data.sections["Executive Summary"] + "\n"
            rendered_sections.add("Executive Summary")
        else:
            output += f"""
{self.bank_info.bank_name} is classified as **{data.classification or 'PRAGMATIST'}** ({data.sub_classification or 'N/A'}) with **{data.probability_state.confidence if data.probability_state else 50:.0f}%** confidence.
"""

        # Bank Profile
        output += "\n## Bank Profile\n"
        if "Bank Profile" in data.sections:
            output += "\n" + data.sections["Bank Profile"] + "\n"
            rendered_sections.add("Bank Profile")
        else:
            output += f"""
| Attribute | Value |
|-----------|-------|
| Legal Name | {self.bank_info.bank_name} |
| Headquarters | {self.bank_info.headquarters or 'N/A'} |
| Region | {self.bank_info.region or 'N/A'} |
| Phase | {self.bank_info.phase} - {self.bank_info.phase_name} |
"""

        # Classification Summary - always render with standardized format
        output += "\n## Classification Summary\n"
        output += f"""
| Metric | Value |
|--------|-------|
| Classification | {data.classification or 'PRAGMATIST'} |
| Sub-Classification | {data.sub_classification or 'N/A'} |
| P(ARCHITECT) | {data.probability_state.p_architect if data.probability_state else 20:.0f}% |
| P(PRAGMATIST) | {data.probability_state.p_pragmatist if data.probability_state else 80:.0f}% |
| Confidence | {data.probability_state.confidence if data.probability_state else 50:.0f}% |
"""
        rendered_sections.add("Classification Summary")

        # Evidence Inventory
        output += "\n## Evidence Inventory\n"
        if "Evidence Inventory" in data.sections:
            output += "\n" + data.sections["Evidence Inventory"] + "\n"
            rendered_sections.add("Evidence Inventory")
        else:
            output += "\nN/A\n"

        # Probability Trajectory
        output += "\n## Probability Trajectory\n"
        if "Probability Trajectory" in data.sections:
            output += "\n" + data.sections["Probability Trajectory"] + "\n"
            rendered_sections.add("Probability Trajectory")
        elif data.trajectory:
            output += "\n| Stage | P(ARCHITECT) | Change |\n"
            output += "|-------|--------------|--------|\n"
            for t in data.trajectory:
                output += f"| {t['stage']} | {t['p_architect']:.0f}% | {t['change']} |\n"
        else:
            output += "\nN/A\n"

        # Render all optional sections that exist in the original
        for section_name in self.OPTIONAL_SECTIONS:
            if section_name in data.sections and section_name not in rendered_sections:
                output += f"\n## {section_name}\n"
                output += "\n" + data.sections[section_name] + "\n"
                rendered_sections.add(section_name)

        # Render any remaining sections not in our predefined lists
        for section_name, content in data.sections.items():
            # Skip already rendered or numbered duplicates
            if section_name in rendered_sections:
                continue
            # Skip if it's a numbered version we already handled
            clean_name = re.sub(r'^\d+\.?\s*', '', section_name)
            if clean_name in rendered_sections:
                continue
            # Skip empty sections
            if not content.strip() or content.strip() == 'N/A':
                continue

            output += f"\n## {section_name}\n"
            output += "\n" + content + "\n"
            rendered_sections.add(section_name)

        output += "\n---\n\n"
        output += f"*Assessment complete. Classification: {data.classification or 'PRAGMATIST'} ({data.sub_classification or 'N/A'}) with {data.probability_state.confidence if data.probability_state else 50:.0f}% confidence.*\n"

        return output


# ==============================================================================
# BACKUP MANAGER
# ==============================================================================

class BackupManager:
    """Manages file backups and rollback"""

    def __init__(self, outputs_dir: Path):
        self.outputs_dir = outputs_dir
        self.manifest_path = outputs_dir / "standardization_backups.json"
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> Dict:
        if self.manifest_path.exists():
            with open(self.manifest_path) as f:
                return json.load(f)
        return {"created": datetime.now().isoformat(), "backups": []}

    def _save_manifest(self):
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def backup_file(self, file_path: Path) -> Path:
        """Create backup of file"""
        backup_path = file_path.with_suffix(file_path.suffix + ".backup")
        shutil.copy2(file_path, backup_path)

        self.manifest["backups"].append({
            "original": str(file_path),
            "backup": str(backup_path),
            "timestamp": datetime.now().isoformat()
        })
        self._save_manifest()

        return backup_path

    def rollback(self, bank_id: Optional[str] = None):
        """Rollback files from backups"""
        count = 0
        for backup_info in self.manifest["backups"]:
            if bank_id and bank_id not in backup_info["original"]:
                continue

            backup_path = Path(backup_info["backup"])
            original_path = Path(backup_info["original"])

            if backup_path.exists():
                shutil.copy2(backup_path, original_path)
                backup_path.unlink()
                count += 1

        print(f"Rolled back {count} files")

        # Update manifest
        if bank_id:
            self.manifest["backups"] = [
                b for b in self.manifest["backups"]
                if bank_id not in b["original"]
            ]
        else:
            self.manifest["backups"] = []
        self._save_manifest()


# ==============================================================================
# MAIN STANDARDIZER
# ==============================================================================

class DocumentStandardizer:
    """Main standardization orchestrator"""

    def __init__(self, outputs_dir: Path, dry_run: bool = False):
        self.outputs_dir = outputs_dir
        self.dry_run = dry_run
        self.backup_manager = BackupManager(outputs_dir)
        self.bank_manifest = self._load_bank_manifest()
        self.stats = {
            "processed": 0,
            "backed_up": 0,
            "failed": 0,
            "skipped": 0
        }

    def _load_bank_manifest(self) -> Dict:
        """Load bank manifest"""
        manifest_path = self.outputs_dir.parent / "config" / "bank-manifest.json"
        if manifest_path.exists():
            with open(manifest_path) as f:
                return json.load(f)
        return {"banks": []}

    def _get_bank_info(self, bank_id: str) -> BankInfo:
        """Get bank info from manifest"""
        for bank in self.bank_manifest.get("banks", []):
            if bank["bank_id"] == bank_id:
                return BankInfo(
                    bank_id=bank["bank_id"],
                    bank_name=bank["bank_name"],
                    phase=bank["phase"],
                    phase_name=bank["phase_name"],
                    headquarters=bank.get("headquarters", ""),
                    region=bank.get("region", "")
                )
        # Fallback
        return BankInfo(
            bank_id=bank_id,
            bank_name=bank_id.replace("-", " ").title(),
            phase=0,
            phase_name="Unknown"
        )

    def _get_template(self, bank_info: BankInfo, folder: str, filename: str) -> DocumentTemplate:
        """Get appropriate template for file type"""
        if folder == "3-gates":
            if filename == "pre-mortem.md":
                return PreMortemTemplate(bank_info)
            elif filename.startswith("gate-"):
                gate_num = int(filename.replace("gate-", "").replace(".md", ""))
                return GateTemplate(bank_info, gate_num)
        elif folder == "2-bayesian":
            tier_num = int(filename.replace("post-tier", "").replace("-update.md", ""))
            return BayesianTemplate(bank_info, tier_num)
        elif folder == "4-adversarial":
            file_type = filename.replace(".md", "")
            return AdversarialTemplate(bank_info, file_type)
        elif folder == "1-evidence":
            if filename == "null-results.md":
                return NullResultsTemplate(bank_info)
            else:
                tier_num = int(filename.replace("tier", "").replace("-evidence.md", ""))
                return EvidenceTemplate(bank_info, tier_num)
        elif folder == "5-synthesis":
            return AssessmentTemplate(bank_info)

        raise ValueError(f"Unknown file type: {folder}/{filename}")

    def process_file(self, file_path: Path, bank_info: BankInfo) -> bool:
        """Process single file"""
        try:
            folder = file_path.parent.name
            filename = file_path.name

            # Read current content
            with open(file_path, encoding='utf-8') as f:
                content = f.read()

            # Get template
            template = self._get_template(bank_info, folder, filename)

            # Extract and render
            data = template.extract(content)
            new_content = template.render(data)

            if self.dry_run:
                print(f"  [DRY RUN] Would process: {file_path}")
                return True

            # Backup
            self.backup_manager.backup_file(file_path)
            self.stats["backed_up"] += 1

            # Write standardized content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            self.stats["processed"] += 1
            return True

        except Exception as e:
            print(f"  [ERROR] {file_path}: {e}")
            self.stats["failed"] += 1
            return False

    def process_bank(self, bank_id: str):
        """Process all files for a bank"""
        bank_info = self._get_bank_info(bank_id)
        print(f"\nProcessing: {bank_info.bank_name} ({bank_id})")

        # Find bank directory
        bank_dir = None
        for phase_dir in self.outputs_dir.iterdir():
            if phase_dir.is_dir() and phase_dir.name.startswith("phase-"):
                potential_bank_dir = phase_dir / bank_id
                if potential_bank_dir.exists():
                    bank_dir = potential_bank_dir
                    break

        if not bank_dir:
            print(f"  [SKIP] Bank directory not found: {bank_id}")
            self.stats["skipped"] += 1
            return

        # Process each file type
        for folder, files in FILE_TYPES.items():
            folder_path = bank_dir / folder
            if not folder_path.exists():
                continue

            for filename in files:
                file_path = folder_path / filename
                if file_path.exists():
                    self.process_file(file_path, bank_info)

    def process_phase(self, phase_num: int):
        """Process all banks in a phase"""
        phase_dir_name = PHASE_DIRS.get(phase_num)
        if not phase_dir_name:
            print(f"Unknown phase: {phase_num}")
            return

        phase_dir = self.outputs_dir / phase_dir_name
        if not phase_dir.exists():
            print(f"Phase directory not found: {phase_dir}")
            return

        print(f"\n=== Processing Phase {phase_num}: {phase_dir_name} ===")

        for bank_dir in sorted(phase_dir.iterdir()):
            if bank_dir.is_dir() and not bank_dir.name.startswith("."):
                self.process_bank(bank_dir.name)

    def process_all(self):
        """Process all banks"""
        print("\n=== Processing All Banks ===")

        for phase_num in sorted(PHASE_DIRS.keys()):
            self.process_phase(phase_num)

    def print_summary(self):
        """Print processing summary"""
        print("\n" + "=" * 50)
        print("STANDARDIZATION SUMMARY")
        print("=" * 50)
        print(f"Files processed: {self.stats['processed']}")
        print(f"Files backed up: {self.stats['backed_up']}")
        print(f"Files failed: {self.stats['failed']}")
        print(f"Banks skipped: {self.stats['skipped']}")
        if self.dry_run:
            print("\n[DRY RUN - No files were modified]")


# ==============================================================================
# CLI
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Standardize CDM/DRR research documents"
    )

    parser.add_argument(
        "--bank",
        help="Process single bank by ID"
    )
    parser.add_argument(
        "--phase",
        type=int,
        help="Process all banks in phase (1-9)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all banks"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback to backup files"
    )
    parser.add_argument(
        "--outputs-dir",
        default="outputs",
        help="Path to outputs directory"
    )

    args = parser.parse_args()

    # Determine outputs directory
    script_dir = Path(__file__).parent
    outputs_dir = script_dir.parent / args.outputs_dir

    if not outputs_dir.exists():
        print(f"Outputs directory not found: {outputs_dir}")
        return

    standardizer = DocumentStandardizer(outputs_dir, dry_run=args.dry_run)

    if args.rollback:
        standardizer.backup_manager.rollback(args.bank)
        return

    if args.bank:
        standardizer.process_bank(args.bank)
    elif args.phase:
        standardizer.process_phase(args.phase)
    elif args.all:
        standardizer.process_all()
    else:
        parser.print_help()
        return

    standardizer.print_summary()


if __name__ == "__main__":
    main()
