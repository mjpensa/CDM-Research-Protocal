"""
CDM Research Protocol - Markdown Parser v1.0

Parses structured markdown outputs from agents into Python dictionaries.
Validates that required sections and fields are present.

Supported formats:
- Evidence blocks (tier1-evidence.md, tier2-evidence.md, tier3-evidence.md)
- Bayesian updates (post-tier1-update.md, etc.)
- Gate outputs (gate-1.md, gate-2.md, gate-3.md, pre-mortem.md)
- Adversarial outputs (counter-case.md, verdict.md, etc.)

Usage:
    from markdown_parser import parse_evidence_file, parse_bayesian_file

    evidence = parse_evidence_file("outputs/phase-1/barclays/1-evidence/tier1-evidence.md")
    bayesian = parse_bayesian_file("outputs/phase-1/barclays/2-bayesian/post-tier1-update.md")
"""

import re
import json
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of validating a parsed markdown file."""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, msg: str):
        self.errors.append(msg)
        self.valid = False

    def add_warning(self, msg: str):
        self.warnings.append(msg)


@dataclass
class EvidenceBlock:
    """Parsed evidence block."""
    id: str
    tier: int
    direction: str  # SUPPORTS ARCHITECT, SUPPORTS PRAGMATIST, NEUTRAL
    source: str
    source_url: Optional[str]
    date: Optional[str]
    finding: str
    authority: str  # High, Medium, Low
    recency: str  # Current, Dated, Historical
    specificity: str  # Specific, Moderate, Vague
    confidence: str  # HIGH, MEDIUM, LOW
    reasoning: str
    caveats: str
    raw_text: str


@dataclass
class BayesianUpdate:
    """
    Parsed Bayesian update.

    Note: evidence_items and absence_items are currently NOT PARSED from markdown.
    They return empty lists. Use parse_evidence_file() for evidence block parsing.
    The combined_lr, posteriors, and other calculated values ARE parsed correctly.
    """
    bank_name: str
    tier: int
    prior_architect: float
    prior_pragmatist: float
    prior_odds: float
    evidence_items: List[Dict]  # NOT PARSED - returns empty list
    absence_items: List[Dict]   # NOT PARSED - returns empty list
    combined_lr: float
    posterior_odds: float
    posterior_architect: float
    posterior_pragmatist: float
    interpretation: str
    recommendation: str
    confidence_cap_applied: bool
    capped_confidence: Optional[float]
    raw_text: str


@dataclass
class GateOutput:
    """Parsed gate output."""
    gate_name: str  # pre-mortem, gate-1, gate-2, gate-3
    bank_name: str
    sections: Dict[str, str]  # Section name -> content
    decision: str  # PROCEED, SKIP, BLOCK
    raw_text: str


# --- EVIDENCE PARSING ---

EVIDENCE_BLOCK_PATTERN = re.compile(
    r'\[([A-Z]+-\d+)\]\s+TIER\s+(\d+)\s+[—-]+\s+(SUPPORTS\s+ARCHITECT|SUPPORTS\s+PRAGMATIST|NEUTRAL)',
    re.IGNORECASE
)

EVIDENCE_FIELD_PATTERNS = {
    'source': re.compile(r'^Source:\s*(.+)$', re.MULTILINE),
    'date': re.compile(r'^Date:\s*(.+)$', re.MULTILINE),
    'url': re.compile(r'^URL:\s*(.+)$', re.MULTILINE),
    'finding': re.compile(r'^Finding:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE | re.DOTALL),
    'authority': re.compile(r'Authority:\s*(High|Medium|Low)', re.IGNORECASE),
    'recency': re.compile(r'Recency:\s*(Current|Dated|Historical)', re.IGNORECASE),
    'specificity': re.compile(r'Specificity:\s*(Specific|Moderate|Vague)', re.IGNORECASE),
    'confidence': re.compile(r'^Confidence:\s*(HIGH|MEDIUM|LOW)', re.MULTILINE | re.IGNORECASE),
    'reasoning': re.compile(r'^Reasoning:\s*(.+)$', re.MULTILINE),
    'caveats': re.compile(r'^Caveats:\s*(.+)$', re.MULTILINE),
}


def parse_evidence_block(text: str) -> Optional[EvidenceBlock]:
    """Parse a single evidence block from text."""
    header_match = EVIDENCE_BLOCK_PATTERN.search(text)
    if not header_match:
        return None

    evidence_id = header_match.group(1)
    tier = int(header_match.group(2))
    direction = header_match.group(3).upper()

    # Extract fields
    fields = {}
    for field_name, pattern in EVIDENCE_FIELD_PATTERNS.items():
        match = pattern.search(text)
        fields[field_name] = match.group(1).strip() if match else ""

    return EvidenceBlock(
        id=evidence_id,
        tier=tier,
        direction=direction,
        source=fields.get('source', ''),
        source_url=fields.get('url') or None,
        date=fields.get('date') or None,
        finding=fields.get('finding', ''),
        authority=fields.get('authority', 'Unknown'),
        recency=fields.get('recency', 'Unknown'),
        specificity=fields.get('specificity', 'Unknown'),
        confidence=fields.get('confidence', 'Unknown'),
        reasoning=fields.get('reasoning', ''),
        caveats=fields.get('caveats', ''),
        raw_text=text
    )


def parse_evidence_file(file_path: str) -> Tuple[List[EvidenceBlock], ValidationResult]:
    """
    Parse an evidence markdown file into structured blocks.

    Args:
        file_path: Path to tier{N}-evidence.md file

    Returns:
        Tuple of (list of EvidenceBlock, ValidationResult)
    """
    path = Path(file_path)
    result = ValidationResult(valid=True)

    if not path.exists():
        result.add_error(f"File not found: {file_path}")
        return [], result

    content = path.read_text(encoding='utf-8')

    # Split on evidence block boundaries (--- or horizontal rule)
    blocks_text = re.split(r'\n-{3,}\n', content)

    evidence_blocks = []
    for block_text in blocks_text:
        if EVIDENCE_BLOCK_PATTERN.search(block_text):
            block = parse_evidence_block(block_text)
            if block:
                evidence_blocks.append(block)

    # Validation
    if len(evidence_blocks) == 0:
        result.add_warning("No evidence blocks found in file")

    for block in evidence_blocks:
        if not block.source:
            result.add_error(f"{block.id}: Missing source")
        if not block.finding:
            result.add_error(f"{block.id}: Missing finding")
        if block.authority == 'Unknown':
            result.add_warning(f"{block.id}: Missing authority assessment")
        if block.recency == 'Unknown':
            result.add_warning(f"{block.id}: Missing recency assessment")

    return evidence_blocks, result


# --- BAYESIAN PARSING ---

def parse_bayesian_file(file_path: str) -> Tuple[Optional[BayesianUpdate], ValidationResult]:
    """
    Parse a Bayesian update markdown file.

    Args:
        file_path: Path to post-tier{N}-update.md file

    Returns:
        Tuple of (BayesianUpdate or None, ValidationResult)
    """
    path = Path(file_path)
    result = ValidationResult(valid=True)

    if not path.exists():
        result.add_error(f"File not found: {file_path}")
        return None, result

    content = path.read_text(encoding='utf-8')

    # Extract tier from filename
    tier_match = re.search(r'tier(\d+)', path.name)
    tier = int(tier_match.group(1)) if tier_match else 0

    # Extract bank name - look for "Bank:" field or header
    bank_match = re.search(r'##\s*Bank:\s*(.+?)(?:\n|$)', content)
    if not bank_match:
        bank_match = re.search(r'#.*?:\s*(.+?)\s*[—-]', content)
    bank_name = bank_match.group(1).strip() if bank_match else "Unknown"

    # Extract prior - handle multiple formats:
    # Format 1: **P(Architect)** = X%
    # Format 2: **P(Architect) = X%**
    # Format 3: **P(ARCHITECT) Prior = X%**
    # Format 4: P(Architect) = X% (no bold)
    prior_patterns = [
        r'\*\*P\(Architect\)\*\*\s*=\s*([\d.]+)%',
        r'\*\*P\(ARCHITECT\)\s*(?:Prior\s*)?=\s*([\d.]+)%\*\*',
        r'\*\*P\(ARCHITECT\)\s*(?:Prior\s*)?=\s*([\d.]+)%',
        r'P\(Architect\)\s*=\s*([\d.]+)%',
        r'Prior\s+(?:P\()?(?:Architect|ARCHITECT)\)?\s*=\s*([\d.]+)%',
    ]

    prior_architect = 0
    for pattern in prior_patterns:
        prior_section = re.search(pattern, content, re.IGNORECASE)
        if prior_section:
            prior_architect = float(prior_section.group(1)) / 100
            break

    # Extract pragmatist prior
    pragmatist_patterns = [
        r'\*\*P\((?:Pragmatist|Not-Architect)\)\*\*\s*=\s*([\d.]+)%',
        r'\*\*P\(PRAGMATIST\)\s*(?:Prior\s*)?=\s*([\d.]+)%\*\*',
        r'\*\*P\(PRAGMATIST\)\s*(?:Prior\s*)?=\s*([\d.]+)%',
        r'P\((?:Pragmatist|Not-Architect)\)\s*=\s*([\d.]+)%',
    ]

    prior_pragmatist = 0
    for pattern in pragmatist_patterns:
        prior_section2 = re.search(pattern, content, re.IGNORECASE)
        if prior_section2:
            prior_pragmatist = float(prior_section2.group(1)) / 100
            break

    if prior_architect > 0:
        if prior_pragmatist == 0:
            prior_pragmatist = 1 - prior_architect
        prior_odds = prior_architect / prior_pragmatist if prior_pragmatist > 0 else 0
    else:
        result.add_error("Could not parse prior probability section")
        prior_architect = prior_pragmatist = prior_odds = 0

    # Extract combined LR - handle various formats
    lr_patterns = [
        r'Combined\s+(?:LR|Likelihood\s+Ratio)[:\s]*=?\s*([\d.]+)',
        r'Sum\s+of\s+positive[:\s]*[\d.]+\s*\+\s*[\d.]+.*?=\s*\*\*([\d.]+)\*\*',
        r'(?:Total|Net|Overall)\s+LR[:\s]*=?\s*([\d.]+)',
    ]

    combined_lr = 0
    for pattern in lr_patterns:
        lr_match = re.search(pattern, content, re.IGNORECASE)
        if lr_match:
            combined_lr = float(lr_match.group(1))
            break

    # If no explicit combined LR, try to infer from calculation methodology
    if combined_lr == 0:
        # Check for individual LRs - multiple formats
        # Format 1: **Likelihood Ratio**: P(E1|A) / P(E1|B) = 0.90 / 0.15 = **6.0**
        individual_lrs = re.findall(r'\*\*Likelihood\s+Ratio\*\*[^=]*=\s*[\d.]+\s*/\s*[\d.]+\s*=\s*\*\*([\d.]+)\*\*', content)
        if not individual_lrs:
            # Format 2: Likelihood Ratio (LR): X.X
            individual_lrs = re.findall(r'Likelihood\s+Ratio\s*\([^)]*\)[:\s]*([\d.]+)', content)
        if not individual_lrs:
            # Format 3: LR = X.X
            individual_lrs = re.findall(r'\bLR\s*[=:]\s*([\d.]+)', content)
        if individual_lrs:
            # Multiple LRs found - implies step-by-step calculation
            combined_lr = 1.0  # Mark as present but calculated step-by-step
            result.add_warning(f"Combined LR inferred from {len(individual_lrs)} individual LRs")
        else:
            result.add_error("Could not parse combined likelihood ratio")

    # Extract posterior - handle various formats
    posterior_patterns = [
        r'P\(Architect\s*\|\s*[^)]+\)\s*=\s*\*?\*?([\d.]+)%',
        r'P\(ARCHITECT\s*\|\s*[^)]+\)\s*=\s*\*?\*?([\d.]+)%',
        r'(?:Updated|Posterior|Final)\s+P\((?:Architect|ARCHITECT)\)[:\s]*[~≈]?\s*([\d.]+)%',
        r'Posterior\s+P\((?:Architect|ARCHITECT)\)\s*=\s*([\d.]+)%',
        r'Architect\s*\([^)]*\)\s*\|\s*[\d.]+%\s*\|\s*([\d.]+)%',
        r'(?:Post|Posterior|Final).*?probability[:\s]*\*?\*?([\d.]+)%',
        r'Updated\s+P\(ARCHITECT\)[^:]*:\s*[~≈]?\*?\*?([\d.]+)%',
    ]

    posterior_architect = 0
    for pattern in posterior_patterns:
        posterior_section = re.search(pattern, content, re.IGNORECASE)
        if posterior_section:
            posterior_architect = float(posterior_section.group(1)) / 100
            break

    if posterior_architect > 0:
        posterior_pragmatist = 1 - posterior_architect
    else:
        result.add_error("Could not parse posterior probability")
        posterior_architect = posterior_pragmatist = 0

    # Calculate posterior odds
    posterior_odds = posterior_architect / posterior_pragmatist if posterior_pragmatist > 0 else 0

    # Extract interpretation
    interp_match = re.search(r'##\s*Interpretation\s*\n+(.+?)(?=\n##|\Z)', content, re.DOTALL)
    interpretation = interp_match.group(1).strip() if interp_match else ""

    # Extract recommendation
    rec_match = re.search(r'Recommendation:\s*(.+?)(?=\n|$)', content)
    recommendation = rec_match.group(1).strip() if rec_match else ""

    # Check for confidence cap
    cap_match = re.search(r'Cap\s+applied:\s*(YES|NO)', content, re.IGNORECASE)
    confidence_cap_applied = cap_match and cap_match.group(1).upper() == 'YES'

    capped_match = re.search(r'Capped.*?:\s*([\d.]+)%', content)
    capped_confidence = float(capped_match.group(1)) / 100 if capped_match else None

    # Validation
    if abs(prior_architect + prior_pragmatist - 1.0) > 0.05:
        result.add_error(f"Prior probabilities don't sum to 1: {prior_architect} + {prior_pragmatist}")

    if abs(posterior_architect + posterior_pragmatist - 1.0) > 0.05:
        result.add_error(f"Posterior probabilities don't sum to 1: {posterior_architect} + {posterior_pragmatist}")

    if combined_lr > 100 or combined_lr < 0.01:
        result.add_warning(f"Extreme combined LR: {combined_lr}")

    return BayesianUpdate(
        bank_name=bank_name,
        tier=tier,
        prior_architect=prior_architect,
        prior_pragmatist=prior_pragmatist,
        prior_odds=prior_odds,
        evidence_items=[],  # NOT IMPLEMENTED: Use parse_evidence_file() instead
        absence_items=[],   # NOT IMPLEMENTED: Absence parsing not yet supported
        combined_lr=combined_lr,
        posterior_odds=posterior_odds,
        posterior_architect=posterior_architect,
        posterior_pragmatist=posterior_pragmatist,
        interpretation=interpretation,
        recommendation=recommendation,
        confidence_cap_applied=confidence_cap_applied,
        capped_confidence=capped_confidence,
        raw_text=content
    ), result


# --- GATE PARSING ---

REQUIRED_GATE_SECTIONS = {
    'pre-mortem': ['failure modes', 'success criteria'],
    'gate-1': ['evidence delta', 'probability update', 'sufficiency'],
    'gate-2': ['evidence delta', 'probability update', 'observable implications'],
    'gate-3': ['evidence delta', 'final probability', 'trajectory'],
}


def parse_gate_file(file_path: str) -> Tuple[Optional[GateOutput], ValidationResult]:
    """
    Parse a gate output markdown file.

    Args:
        file_path: Path to gate-{N}.md or pre-mortem.md file

    Returns:
        Tuple of (GateOutput or None, ValidationResult)
    """
    path = Path(file_path)
    result = ValidationResult(valid=True)

    if not path.exists():
        result.add_error(f"File not found: {file_path}")
        return None, result

    content = path.read_text(encoding='utf-8')

    # Determine gate name
    gate_name = path.stem  # e.g., "gate-1", "pre-mortem"

    # Extract bank name
    bank_match = re.search(r'#.*?:\s*(.+?)(?:\s*[—-]|\n)', content)
    bank_name = bank_match.group(1).strip() if bank_match else "Unknown"

    # Extract sections (## headers)
    sections = {}
    section_pattern = re.compile(r'^##\s+(.+?)$', re.MULTILINE)
    section_matches = list(section_pattern.finditer(content))

    for i, match in enumerate(section_matches):
        section_name = match.group(1).strip().lower()
        start = match.end()
        end = section_matches[i + 1].start() if i + 1 < len(section_matches) else len(content)
        section_content = content[start:end].strip()
        sections[section_name] = section_content

    # Extract decision
    decision_match = re.search(r'\b(PROCEED|SKIP|BLOCK|CONTINUE)\b', content, re.IGNORECASE)
    decision = decision_match.group(1).upper() if decision_match else "UNKNOWN"

    # Validate required sections
    required = REQUIRED_GATE_SECTIONS.get(gate_name, [])
    for req_section in required:
        found = any(req_section in s for s in sections.keys())
        if not found:
            result.add_warning(f"Missing section: {req_section}")

    return GateOutput(
        gate_name=gate_name,
        bank_name=bank_name,
        sections=sections,
        decision=decision,
        raw_text=content
    ), result


# --- ADVERSARIAL PARSING ---

@dataclass
class AdversarialOutput:
    """Parsed adversarial output."""
    output_type: str  # counter-case, disconfirming-searches, steelman, verdict
    bank_name: str
    sections: Dict[str, str]
    verdict: Optional[str]  # STRENGTHENED, UNCHANGED, WEAKENED, REVISED
    confidence_adjustment: Optional[str]
    raw_text: str


def parse_adversarial_file(file_path: str) -> Tuple[Optional[AdversarialOutput], ValidationResult]:
    """
    Parse an adversarial output markdown file.

    Args:
        file_path: Path to counter-case.md, verdict.md, etc.

    Returns:
        Tuple of (AdversarialOutput or None, ValidationResult)
    """
    path = Path(file_path)
    result = ValidationResult(valid=True)

    if not path.exists():
        result.add_error(f"File not found: {file_path}")
        return None, result

    content = path.read_text(encoding='utf-8')

    # Determine output type
    output_type = path.stem  # e.g., "counter-case", "verdict"

    # Extract bank name
    bank_match = re.search(r'#.*?:\s*(.+?)(?:\s*[—-]|\n)', content)
    bank_name = bank_match.group(1).strip() if bank_match else "Unknown"

    # Extract sections
    sections = {}
    section_pattern = re.compile(r'^##\s+(.+?)$', re.MULTILINE)
    section_matches = list(section_pattern.finditer(content))

    for i, match in enumerate(section_matches):
        section_name = match.group(1).strip().lower()
        start = match.end()
        end = section_matches[i + 1].start() if i + 1 < len(section_matches) else len(content)
        section_content = content[start:end].strip()
        sections[section_name] = section_content

    # Extract verdict - handle various terminology
    # Standard: STRENGTHENED, UNCHANGED, WEAKENED, REVISED
    # Also accept: CONFIRMED, REJECTED, PASSED (map to standard)
    verdict_match = re.search(r'\b(STRENGTHENED|UNCHANGED|WEAKENED|REVISED|CONFIRMED|REJECTED|PASSED)\b', content, re.IGNORECASE)
    verdict = verdict_match.group(1).upper() if verdict_match else None

    # Normalize non-standard verdicts
    if verdict == 'CONFIRMED':
        verdict = 'UNCHANGED'  # Classification was confirmed/upheld
    elif verdict == 'PASSED':
        verdict = 'STRENGTHENED'  # Passed adversarial challenge
    elif verdict == 'REJECTED':
        # Check context - REJECTED hypothesis means classification unchanged
        if re.search(r'hypothesis.*REJECTED|REJECTED.*hypothesis', content, re.IGNORECASE):
            verdict = 'UNCHANGED'
        # Otherwise leave as REJECTED (needs manual review)

    # Extract confidence adjustment
    adj_match = re.search(r'Confidence\s+(?:Adjustment|Impact|Level)[:\s]*(.+?)(?:\n|$)', content, re.IGNORECASE)
    confidence_adjustment = adj_match.group(1).strip() if adj_match else None

    # Validation based on output type
    if output_type == 'verdict' and not verdict:
        result.add_error("Verdict file missing verdict (STRENGTHENED/UNCHANGED/WEAKENED/REVISED)")
    elif output_type == 'verdict' and verdict not in ['STRENGTHENED', 'UNCHANGED', 'WEAKENED', 'REVISED']:
        result.add_warning(f"Non-standard verdict term: {verdict}")

    return AdversarialOutput(
        output_type=output_type,
        bank_name=bank_name,
        sections=sections,
        verdict=verdict,
        confidence_adjustment=confidence_adjustment,
        raw_text=content
    ), result


# --- BATCH VALIDATION ---

def validate_bank_outputs(bank_dir: str) -> Dict:
    """
    Validate all markdown outputs for a bank.

    Args:
        bank_dir: Path to bank output directory

    Returns:
        Dict with validation results for each file type
    """
    bank_path = Path(bank_dir)
    results = {}

    # Validate evidence files
    evidence_dir = bank_path / "1-evidence"
    if evidence_dir.exists():
        for tier in [1, 2, 3]:
            file_path = evidence_dir / f"tier{tier}-evidence.md"
            if file_path.exists():
                blocks, validation = parse_evidence_file(str(file_path))
                results[f"tier{tier}_evidence"] = {
                    "blocks_found": len(blocks),
                    "valid": validation.valid,
                    "errors": validation.errors,
                    "warnings": validation.warnings
                }

    # Validate Bayesian files
    bayesian_dir = bank_path / "2-bayesian"
    if bayesian_dir.exists():
        for tier in [1, 2, 3]:
            file_path = bayesian_dir / f"post-tier{tier}-update.md"
            if file_path.exists():
                update, validation = parse_bayesian_file(str(file_path))
                results[f"bayesian_tier{tier}"] = {
                    "posterior_architect": update.posterior_architect if update else None,
                    "combined_lr": update.combined_lr if update else None,
                    "valid": validation.valid,
                    "errors": validation.errors,
                    "warnings": validation.warnings
                }

    # Validate gate files
    gates_dir = bank_path / "3-gates"
    if gates_dir.exists():
        for gate_file in gates_dir.glob("*.md"):
            gate, validation = parse_gate_file(str(gate_file))
            results[f"gate_{gate_file.stem}"] = {
                "decision": gate.decision if gate else None,
                "sections_found": len(gate.sections) if gate else 0,
                "valid": validation.valid,
                "errors": validation.errors,
                "warnings": validation.warnings
            }

    # Validate adversarial files
    adversarial_dir = bank_path / "4-adversarial"
    if adversarial_dir.exists():
        for adv_file in adversarial_dir.glob("*.md"):
            adv, validation = parse_adversarial_file(str(adv_file))
            results[f"adversarial_{adv_file.stem}"] = {
                "verdict": adv.verdict if adv else None,
                "sections_found": len(adv.sections) if adv else 0,
                "valid": validation.valid,
                "errors": validation.errors,
                "warnings": validation.warnings
            }

    return results


# --- CLI ---

def main():
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    if len(sys.argv) < 2:
        print("Usage: python markdown_parser.py <file_or_directory>")
        print("       python markdown_parser.py outputs/phase-1/barclays/")
        print("       python markdown_parser.py outputs/phase-1/barclays/1-evidence/tier1-evidence.md")
        sys.exit(1)

    path = Path(sys.argv[1])

    if path.is_dir():
        # Validate entire bank directory
        print(f"Validating bank outputs: {path.name}\n")
        results = validate_bank_outputs(str(path))

        all_valid = True
        for file_type, result in results.items():
            status = "[OK]" if result['valid'] else "[FAIL]"
            print(f"{status} {file_type}")

            if result.get('errors'):
                all_valid = False
                for err in result['errors']:
                    print(f"      ERROR: {err}")

            if result.get('warnings'):
                for warn in result['warnings']:
                    print(f"      WARN: {warn}")

        print(f"\n{'='*50}")
        print(f"Overall: {'VALID' if all_valid else 'INVALID'}")

    elif path.suffix == '.md':
        # Parse single file
        if 'evidence' in path.name:
            blocks, result = parse_evidence_file(str(path))
            print(f"Parsed {len(blocks)} evidence blocks")
            print(f"Valid: {result.valid}")
            for block in blocks:
                print(f"  {block.id}: {block.direction} (Tier {block.tier})")
            if result.errors:
                print("\nErrors:")
                for err in result.errors:
                    print(f"  - {err}")
            if result.warnings:
                print("\nWarnings:")
                for warn in result.warnings:
                    print(f"  - {warn}")
        elif 'bayesian' in str(path) or 'tier' in path.name:
            update, result = parse_bayesian_file(str(path))
            if update:
                print(f"Bank: {update.bank_name}")
                print(f"Prior: {update.prior_architect:.1%}")
                print(f"Posterior: {update.posterior_architect:.1%}")
                print(f"Combined LR: {update.combined_lr}")
            print(f"Valid: {result.valid}")
            if result.errors:
                print("\nErrors:")
                for err in result.errors:
                    print(f"  - {err}")
        elif 'gate' in path.name or 'pre-mortem' in path.name:
            gate, result = parse_gate_file(str(path))
            if gate:
                print(f"Gate: {gate.gate_name}")
                print(f"Bank: {gate.bank_name}")
                print(f"Decision: {gate.decision}")
                print(f"Sections: {list(gate.sections.keys())}")
            print(f"Valid: {result.valid}")
            if result.errors:
                print("\nErrors:")
                for err in result.errors:
                    print(f"  - {err}")
        elif any(x in path.name for x in ['counter-case', 'verdict', 'steelman', 'disconfirming']):
            adv, result = parse_adversarial_file(str(path))
            if adv:
                print(f"Type: {adv.output_type}")
                print(f"Bank: {adv.bank_name}")
                print(f"Verdict: {adv.verdict}")
                print(f"Sections: {list(adv.sections.keys())}")
            print(f"Valid: {result.valid}")
        else:
            print(f"Unknown markdown file type: {path.name}")
            print("Trying gate parser as default...")
            gate, result = parse_gate_file(str(path))
            if gate:
                print(f"Sections: {list(gate.sections.keys())}")
            print(f"Valid: {result.valid}")
    else:
        print(f"Unknown file type: {path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
