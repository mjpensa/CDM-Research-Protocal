# Implementation Plan: CDM Research Protocol Enhancements

**Created**: 2025-12-19
**Based On**: [strategy.md](strategy.md)
**Total Estimated Effort**: 28-41 hours
**Phases**: 7 (Phase 0-6)

---

## Table of Contents

1. [Phase 0: Quick Wins](#phase-0-quick-wins)
2. [Phase 1: Centralize Configuration](#phase-1-centralize-configuration)
3. [Phase 2: Markdown Schema Validation](#phase-2-markdown-schema-validation)
4. [Phase 3: Bayesian Validation Engine](#phase-3-bayesian-validation-engine)
5. [Phase 4: Real-Time URL Validation](#phase-4-real-time-url-validation)
6. [Phase 5: Enhanced QA Validator](#phase-5-enhanced-qa-validator)
7. [Phase 6: Full Integration Layer](#phase-6-full-integration-layer)

---

## Pre-Implementation Checklist

Before starting, verify:

- [ ] Python 3.10+ installed
- [ ] All dependencies available (`pip install -r requirements.txt`)
- [ ] Git repository clean (`git status` shows no uncommitted critical changes)
- [ ] Backup created (`git stash` or copy outputs/ folder)

```bash
# Verify environment
python --version
pip list | grep -E "requests|jsonschema"
git status
```

---

# Phase 0: Quick Wins

**Effort**: 1-2 hours
**Dependencies**: None
**Fixes Addressed**: #8 (Deprecated Terminology)

## Step 0.1: Run Terminology Migration (Dry Run)

First, preview what will change without modifying files.

```bash
cd c:\cdm-research-protocol
python tools/migrate_terminology.py outputs/
```

**Expected Output**:
```
DRY RUN - Found X files with deprecated terms

  outputs/state/workflow-state.json:
    - "NOT ENGAGED" -> "PRAGMATIST" (2 occurrences)
    - "NON-ARCHITECT" -> "PRAGMATIST" (1 occurrences)

  outputs/phase-2-uk-regional/lloyds/status.json:
    - ...

Run with --apply to make changes (backups will be created)
```

**Checkpoint**: Review the list. Ensure no false positives.

---

## Step 0.2: Apply Terminology Migration

```bash
python tools/migrate_terminology.py outputs/ --apply
```

**Expected Output**:
```
Applied changes to X files (backups created with .bak extension)
```

**Verification**:
```bash
# Check that deprecated terms are gone
grep -r "NOT ENGAGED" outputs/ --include="*.json" --include="*.md"
grep -r "NON-ARCHITECT" outputs/ --include="*.json" --include="*.md"
# Should return no results
```

---

## Step 0.3: Run Cross-Bank Validation (Baseline)

```bash
python tools/cross_bank_validator.py outputs/
```

**Expected Output**:
```
============================================================
CROSS-BANK VALIDATION: PASSED/FAILED
============================================================

Summary:
  Banks analyzed: 31
  Classifications: {'ARCHITECT': 5, 'PRAGMATIST': 20, 'OBSERVER': 4, 'UNKNOWN': 2}
  Confidence range: 35% - 96%
  Average confidence: 68.5%

Issues (X):
  bank-name:
    [check_type] Issue description
```

**Action**: Save this output as baseline.
```bash
python tools/cross_bank_validator.py outputs/ > outputs/qa/baseline-validation.txt
```

---

## Step 0.4: Test Config Loader

```bash
python tools/config_loader.py
```

**Expected Output**:
```
CDM Research Protocol - Configuration Loader Test
==================================================

1. Decision Thresholds:
   Skip threshold: 80%
   Low confidence block: 50%
   Uncertainty range: (40, 60)
   Early termination: 95%
   Extreme LR bounds: (0.01, 100)

2. Confidence Caps:
   Tier 1: 95%
   Tier 2: 75%
   Tier 3: 50%
   Tier 4: 35%

[OK] All configuration loaded successfully!
```

**Checkpoint**: If errors occur, fix config files before proceeding.

---

## Phase 0 Completion Checklist

- [ ] Terminology migration applied (no deprecated terms in outputs)
- [ ] Backup files created (*.bak)
- [ ] Baseline validation report saved
- [ ] Config loader working correctly
- [ ] Git commit made

```bash
git add outputs/qa/baseline-validation.txt
git commit -m "Phase 0: Apply terminology migration, create baseline validation

- Migrated deprecated terms (NOT ENGAGED -> PRAGMATIST)
- Generated baseline cross-bank validation report
- Verified config_loader.py working"
```

---

# Phase 1: Centralize Configuration

**Effort**: 2-3 hours
**Dependencies**: Phase 0
**Fixes Addressed**: #4 (Centralize Thresholds)

## Step 1.1: Create Agent Config Reference File

Create a human-readable reference that agents can consult.

**File**: `config/agent-config-reference.md`

```bash
# Create the file
```

**Content**:
```markdown
# Agent Configuration Reference

> **IMPORTANT**: This file is auto-generated from `config/decision-thresholds.json`.
> Do NOT hardcode these values in agent prompts. Reference this file instead.

Generated: [TIMESTAMP]

---

## Workflow Decision Thresholds

| Threshold | Value | Description |
|-----------|-------|-------------|
| Skip to Adversarial | 80% | If P(Architect) > 80% OR P(Architect) < 20%, skip remaining evidence tiers |
| Low Confidence Block | 50% | BLOCK checkpoint if final confidence below this value |
| Uncertainty Range | 40-60% | Flag as high uncertainty if probability in this range |
| Early Termination | 95% | May terminate early if confidence exceeds this after Tier 1 |
| Extreme LR Upper | 100 | Flag if combined LR exceeds this |
| Extreme LR Lower | 0.01 | Flag if combined LR below this |

---

## Confidence Caps by Evidence Tier

| Highest Evidence Tier | Maximum Confidence | Rationale |
|----------------------|-------------------|-----------|
| Tier 1 (Official) | 95% | Even official sources can be outdated |
| Tier 2 (Industry) | 75% | Industry sources require triangulation |
| Tier 3 (Signals) | 50% | Indirect signals are inherently uncertain |
| Tier 4 (Inference) | 35% | Pure inference has high uncertainty |

---

## Classification Thresholds

| Classification | Minimum P(Architect) | Required Evidence |
|---------------|---------------------|-------------------|
| ARCHITECT-Native | 90% | production_usage confirmed |
| ARCHITECT-Leader | 75% | pilot_or_poc with significant contribution |
| ARCHITECT-Follower | 60% | open_source_contribution or membership |
| PRAGMATIST | < 50% | Any variant |

---

## Gate Decision Points

### Gate 1 (After Tier 1)
- **Proceed to Tier 2**: P(Architect) between 20% and 80%
- **Skip to Adversarial**: P(Architect) > 80% OR P(Architect) < 20%

### Gate 2 (After Tier 2)
- **Proceed to Tier 3**: P(Architect) between 20% and 80%
- **Skip to Adversarial**: P(Architect) > 80% OR P(Architect) < 20%

### Gate 3 (After Tier 3)
- **Always proceed to Adversarial**

---

## How to Use This File

In agent prompts, instead of writing:
```
If P(Architect) > 80%, skip to adversarial
```

Write:
```
If P(Architect) > skip_threshold (see config/agent-config-reference.md), skip to adversarial
```

This ensures all agents use consistent, centrally-managed thresholds.
```

---

## Step 1.2: Create Config Injector Tool

**File**: `tools/inject_agent_config.py`

```python
"""
CDM Research Protocol - Agent Config Injector v1.0

Generates agent-config-reference.md from decision-thresholds.json.
Optionally injects values into agent prompt templates.

Usage:
    python inject_agent_config.py                    # Generate reference file
    python inject_agent_config.py --check-prompts    # Check for hardcoded values
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_ROOT / "config"
AGENT_PROMPTS_DIR = CONFIG_DIR / "agent-prompts"

# Patterns that suggest hardcoded thresholds
HARDCODED_PATTERNS = [
    (r'\b80\s*%', 'skip_threshold (80%)'),
    (r'\b50\s*%', 'low_confidence_block (50%)'),
    (r'\b95\s*%', 'tier1_confidence_cap (95%)'),
    (r'\b75\s*%', 'tier2_confidence_cap (75%)'),
    (r'>\s*80', 'skip_threshold'),
    (r'<\s*20', 'inverse skip_threshold'),
    (r'<\s*50', 'low_confidence_block'),
]


def load_thresholds() -> dict:
    """Load decision thresholds from JSON."""
    path = CONFIG_DIR / "decision-thresholds.json"
    return json.loads(path.read_text(encoding='utf-8'))


def generate_reference_file() -> str:
    """Generate the agent-config-reference.md content."""
    thresholds = load_thresholds()
    wd = thresholds['workflow_decisions']
    caps = thresholds['confidence_caps']
    ct = thresholds['classification_thresholds']

    content = f"""# Agent Configuration Reference

> **IMPORTANT**: This file is auto-generated from `config/decision-thresholds.json`.
> Do NOT hardcode these values in agent prompts. Reference this file instead.

Generated: {datetime.utcnow().isoformat()}Z

---

## Workflow Decision Thresholds

| Threshold | Value | Description |
|-----------|-------|-------------|
| Skip to Adversarial | {wd['skip_to_adversarial']['threshold']}% | {wd['skip_to_adversarial']['description']} |
| Low Confidence Block | {wd['low_confidence_block']['threshold']}% | {wd['low_confidence_block']['description']} |
| Uncertainty Range | {wd['uncertainty_range']['lower']}-{wd['uncertainty_range']['upper']}% | {wd['uncertainty_range']['description']} |
| Early Termination | {wd['early_termination']['threshold']}% | {wd['early_termination']['description']} |
| Extreme LR Upper | {wd['extreme_lr_flag']['upper']} | Flag if combined LR exceeds this |
| Extreme LR Lower | {wd['extreme_lr_flag']['lower']} | Flag if combined LR below this |

---

## Confidence Caps by Evidence Tier

| Highest Evidence Tier | Maximum Confidence | Rationale |
|----------------------|-------------------|-----------|
| Tier 1 (Official) | {caps['tier1_only']}% | {caps['rationale']['tier1']} |
| Tier 2 (Industry) | {caps['tier2_only']}% | {caps['rationale']['tier2']} |
| Tier 3 (Signals) | {caps['tier3_only']}% | {caps['rationale']['tier3']} |
| Tier 4 (Inference) | {caps['tier4_inference_only']}% | {caps['rationale']['tier4']} |

---

## Classification Thresholds

| Classification | Minimum P(Architect) | Required Evidence |
|---------------|---------------------|-------------------|
| ARCHITECT-Native | {ct['architect_native']['minimum_probability']}% | {ct['architect_native']['required_evidence']} |
| ARCHITECT-Leader | {ct['architect_leader']['minimum_probability']}% | {ct['architect_leader']['required_evidence']} |
| ARCHITECT-Follower | {ct['architect_follower']['minimum_probability']}% | {ct['architect_follower']['required_evidence']} |
| PRAGMATIST | {ct['pragmatist']['probability_range']} | Any variant |

---

## Gate Decision Points

### Gate 1 (After Tier 1)
- **Proceed to Tier 2**: P(Architect) between {100 - wd['skip_to_adversarial']['threshold']}% and {wd['skip_to_adversarial']['threshold']}%
- **Skip to Adversarial**: P(Architect) > {wd['skip_to_adversarial']['threshold']}% OR P(Architect) < {100 - wd['skip_to_adversarial']['threshold']}%

### Gate 2 (After Tier 2)
- **Proceed to Tier 3**: P(Architect) between {100 - wd['skip_to_adversarial']['threshold']}% and {wd['skip_to_adversarial']['threshold']}%
- **Skip to Adversarial**: P(Architect) > {wd['skip_to_adversarial']['threshold']}% OR P(Architect) < {100 - wd['skip_to_adversarial']['threshold']}%

### Gate 3 (After Tier 3)
- **Always proceed to Adversarial**

---

## How to Use This File

In agent prompts, instead of writing:
```
If P(Architect) > 80%, skip to adversarial
```

Write:
```
If P(Architect) > skip_threshold (see config/agent-config-reference.md), skip to adversarial
```

This ensures all agents use consistent, centrally-managed thresholds.

---

## Source Files

- Thresholds: `config/decision-thresholds.json`
- LR Tables: `config/bayesian-lr-tables.json`
- Taxonomy: `config/classification-taxonomy.json`
"""
    return content


def check_prompts_for_hardcoded() -> list:
    """Check agent prompts for potentially hardcoded threshold values."""
    issues = []

    for prompt_file in AGENT_PROMPTS_DIR.glob("*.md"):
        content = prompt_file.read_text(encoding='utf-8')
        file_issues = []

        for pattern, description in HARDCODED_PATTERNS:
            matches = list(re.finditer(pattern, content))
            for match in matches:
                # Get line number
                line_num = content[:match.start()].count('\n') + 1
                # Get context
                line_start = content.rfind('\n', 0, match.start()) + 1
                line_end = content.find('\n', match.end())
                line_text = content[line_start:line_end].strip()

                file_issues.append({
                    'line': line_num,
                    'pattern': description,
                    'context': line_text[:80]
                })

        if file_issues:
            issues.append({
                'file': prompt_file.name,
                'issues': file_issues
            })

    return issues


def main():
    if '--check-prompts' in sys.argv:
        print("Checking agent prompts for hardcoded thresholds...\n")
        issues = check_prompts_for_hardcoded()

        if not issues:
            print("[OK] No hardcoded thresholds found!")
        else:
            print(f"Found potential hardcoded values in {len(issues)} files:\n")
            for file_info in issues:
                print(f"  {file_info['file']}:")
                for issue in file_info['issues']:
                    print(f"    Line {issue['line']}: {issue['pattern']}")
                    print(f"      Context: {issue['context']}")
                print()

            print("Consider replacing these with references to config/agent-config-reference.md")

        return

    # Generate reference file
    print("Generating agent-config-reference.md...")
    content = generate_reference_file()

    output_path = CONFIG_DIR / "agent-config-reference.md"
    output_path.write_text(content, encoding='utf-8')

    print(f"[OK] Generated: {output_path}")
    print("\nNext steps:")
    print("1. Run: python inject_agent_config.py --check-prompts")
    print("2. Update agent prompts to reference this file")


if __name__ == "__main__":
    main()
```

---

## Step 1.3: Generate Reference File

```bash
python tools/inject_agent_config.py
```

**Expected Output**:
```
Generating agent-config-reference.md...
[OK] Generated: c:\cdm-research-protocol\config\agent-config-reference.md

Next steps:
1. Run: python inject_agent_config.py --check-prompts
2. Update agent prompts to reference this file
```

---

## Step 1.4: Check Agent Prompts for Hardcoded Values

```bash
python tools/inject_agent_config.py --check-prompts
```

**Expected Output**:
```
Checking agent prompts for hardcoded thresholds...

Found potential hardcoded values in 4 files:

  orchestrator.md:
    Line 132: skip_threshold (80%)
      Context: If P(Architect) > 80%: SKIP to Adversarial
    Line 139: skip_threshold (80%)
      Context: IF P > 80%: SKIP to Adversarial
    ...

  bayesian-analyst.md:
    Line 250: skip_threshold (80%)
      Context: P > 80%: Evidence sufficient for classification
    ...

Consider replacing these with references to config/agent-config-reference.md
```

---

## Step 1.5: Update Agent Prompts

For each file identified, update the hardcoded values.

**Example update for `orchestrator.md`**:

Find:
```markdown
5. REASONING GATE 1 (auto-proceed)
   ↓ [Check: P(Architect) > 80% OR P(Pragmatist) > 80%? → Skip to Adversarial]
```

Replace with:
```markdown
5. REASONING GATE 1 (auto-proceed)
   ↓ [Check: P(Architect) > skip_threshold OR P(Pragmatist) > skip_threshold? → Skip to Adversarial]
   ↓ [Reference: config/decision-thresholds.json → workflow_decisions.skip_to_adversarial.threshold]
```

**Files to update**:
- [ ] `config/agent-prompts/orchestrator.md`
- [ ] `config/agent-prompts/bayesian-analyst.md`
- [ ] `config/agent-prompts/reasoning-gate.md`
- [ ] `config/agent-prompts/qa-validator.md`

---

## Step 1.6: Add Configuration Section to Each Agent Prompt

Add this section at the top of each agent prompt:

```markdown
## Configuration Reference

All threshold values are defined in `config/decision-thresholds.json`.
Do NOT use hardcoded values. Reference the config file for:

- `skip_to_adversarial.threshold`: When to skip remaining evidence tiers
- `low_confidence_block.threshold`: When to BLOCK for human review
- `confidence_caps`: Maximum confidence by evidence tier
- `uncertainty_range`: Range flagged as high uncertainty

See `config/agent-config-reference.md` for current values.
```

---

## Phase 1 Completion Checklist

- [ ] `config/agent-config-reference.md` generated
- [ ] `tools/inject_agent_config.py` created and tested
- [ ] Agent prompts checked for hardcoded values
- [ ] Hardcoded values replaced with config references
- [ ] Configuration section added to each agent prompt
- [ ] Git commit made

```bash
git add config/agent-config-reference.md tools/inject_agent_config.py
git add config/agent-prompts/*.md
git commit -m "Phase 1: Centralize configuration

- Created agent-config-reference.md (auto-generated from thresholds)
- Created inject_agent_config.py tool
- Updated agent prompts to reference config files
- Removed hardcoded threshold values"
```

---

# Phase 2: Markdown Schema Validation

**Effort**: 4-6 hours
**Dependencies**: Phase 1
**Fixes Addressed**: #3 (Schema Validation for Markdown)

## Step 2.1: Create Markdown Parser Module

**File**: `tools/markdown_parser.py`

```python
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
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of validating a parsed markdown file."""
    valid: bool
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

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
    """Parsed Bayesian update."""
    bank_name: str
    tier: int
    prior_architect: float
    prior_pragmatist: float
    prior_odds: float
    evidence_items: list  # List of {id, type, lr, direction, rationale}
    absence_items: list  # List of {category, informative, lr, rationale}
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
    sections: dict  # Section name -> content
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


def parse_evidence_file(file_path: str) -> tuple[list[EvidenceBlock], ValidationResult]:
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

def parse_bayesian_file(file_path: str) -> tuple[Optional[BayesianUpdate], ValidationResult]:
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

    # Extract bank name from header
    bank_match = re.search(r'#.*?:\s*(.+?)\s*[—-]', content)
    bank_name = bank_match.group(1).strip() if bank_match else "Unknown"

    # Extract prior
    prior_section = re.search(
        r'##\s*Prior.*?P\(Architect\)\s*=\s*([\d.]+)%.*?P\(Pragmatist\)\s*=\s*([\d.]+)%.*?Prior\s+Odds\s*=.*?([\d.]+)',
        content, re.DOTALL | re.IGNORECASE
    )

    if prior_section:
        prior_architect = float(prior_section.group(1)) / 100
        prior_pragmatist = float(prior_section.group(2)) / 100
        prior_odds = float(prior_section.group(3))
    else:
        result.add_error("Could not parse prior probability section")
        prior_architect = prior_pragmatist = prior_odds = 0

    # Extract combined LR
    lr_match = re.search(r'Combined\s+LR\s*=\s*([\d.]+)', content)
    combined_lr = float(lr_match.group(1)) if lr_match else 0

    if combined_lr == 0:
        result.add_error("Could not parse combined likelihood ratio")

    # Extract posterior
    posterior_section = re.search(
        r'P\(Architect\s*\|\s*Evidence\)\s*=.*?([\d.]+)%',
        content, re.DOTALL | re.IGNORECASE
    )

    if posterior_section:
        posterior_architect = float(posterior_section.group(1)) / 100
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
        evidence_items=[],  # TODO: Parse evidence table
        absence_items=[],  # TODO: Parse absence table
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


def parse_gate_file(file_path: str) -> tuple[Optional[GateOutput], ValidationResult]:
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


# --- BATCH VALIDATION ---

def validate_bank_outputs(bank_dir: str) -> dict:
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

    return results


# --- CLI ---

def main():
    import sys

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
        elif 'bayesian' in str(path) or 'tier' in path.name:
            update, result = parse_bayesian_file(str(path))
            if update:
                print(f"Bank: {update.bank_name}")
                print(f"Prior: {update.prior_architect:.1%}")
                print(f"Posterior: {update.posterior_architect:.1%}")
                print(f"Combined LR: {update.combined_lr}")
            print(f"Valid: {result.valid}")
        elif 'gate' in path.name or 'pre-mortem' in path.name:
            gate, result = parse_gate_file(str(path))
            if gate:
                print(f"Gate: {gate.gate_name}")
                print(f"Bank: {gate.bank_name}")
                print(f"Decision: {gate.decision}")
                print(f"Sections: {list(gate.sections.keys())}")
            print(f"Valid: {result.valid}")
    else:
        print(f"Unknown file type: {path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## Step 2.2: Create Markdown Schema Definitions

**File**: `templates/markdown-schemas.json`

```json
{
  "$schema": "CDM/DRR Markdown Schema Definitions v1.0",
  "description": "Validation schemas for agent markdown outputs",

  "evidence_block": {
    "required_fields": [
      "id",
      "tier",
      "direction",
      "source",
      "finding"
    ],
    "optional_fields": [
      "source_url",
      "date",
      "authority",
      "recency",
      "specificity",
      "confidence",
      "reasoning",
      "caveats",
      "corroborated"
    ],
    "id_pattern": "^[A-Z]+-\\d{3}$",
    "tier_values": [1, 2, 3],
    "direction_values": ["SUPPORTS ARCHITECT", "SUPPORTS PRAGMATIST", "NEUTRAL"],
    "authority_values": ["High", "Medium", "Low"],
    "recency_values": ["Current", "Dated", "Historical"],
    "specificity_values": ["Specific", "Moderate", "Vague"],
    "confidence_values": ["HIGH", "MEDIUM", "LOW"]
  },

  "bayesian_update": {
    "required_sections": [
      "Prior",
      "Evidence This Tier",
      "Combined Likelihood Ratio",
      "Posterior Calculation",
      "Interpretation"
    ],
    "optional_sections": [
      "Absence Evidence",
      "Proceeding Decision",
      "Calibration Checks",
      "Confidence Cap Assessment",
      "Thinking Trace"
    ],
    "required_values": [
      "prior_architect",
      "prior_pragmatist",
      "prior_odds",
      "combined_lr",
      "posterior_architect",
      "posterior_pragmatist"
    ],
    "validation_rules": {
      "probability_sum": "prior_architect + prior_pragmatist ≈ 1.0 (±0.02)",
      "posterior_sum": "posterior_architect + posterior_pragmatist ≈ 1.0 (±0.02)",
      "extreme_lr": "combined_lr should be between 0.01 and 100"
    }
  },

  "gate_output": {
    "pre-mortem": {
      "required_sections": ["Failure Modes", "Success Criteria"],
      "min_failure_modes": 4
    },
    "gate-1": {
      "required_sections": ["Evidence Delta", "Probability Update", "Sufficiency Assessment"],
      "decision_values": ["PROCEED", "SKIP TO ADVERSARIAL"]
    },
    "gate-2": {
      "required_sections": ["Evidence Delta", "Probability Update", "Observable Implications"],
      "min_implications_tested": 3,
      "decision_values": ["PROCEED", "SKIP TO ADVERSARIAL"]
    },
    "gate-3": {
      "required_sections": ["Evidence Delta", "Final Probability", "Trajectory Assessment"],
      "decision_values": ["PROCEED TO ADVERSARIAL"]
    }
  },

  "adversarial_output": {
    "counter-case": {
      "required_sections": ["Counter-Argument"]
    },
    "disconfirming-searches": {
      "required_sections": ["Search Query", "Results", "Conclusion"]
    },
    "verdict": {
      "required_sections": ["Original Classification", "Adversarial Verdict", "Confidence Adjustment"],
      "verdict_values": ["STRENGTHENED", "UNCHANGED", "WEAKENED", "REVISED"]
    }
  },

  "null_results": {
    "required_fields": [
      "search_category",
      "queries_executed",
      "results_reviewed",
      "null_classification",
      "informative_absence_assessment"
    ],
    "null_classification_values": [
      "NO RESULTS",
      "IRRELEVANT RESULTS",
      "PAYWALLED",
      "OUTDATED ONLY"
    ]
  }
}
```

---

## Step 2.3: Integrate Validation into Pipeline

**Modify**: `tools/run_pipeline.py`

Add after line 100 (after `ensure_evidence_json`):

```python
from markdown_parser import validate_bank_outputs

def validate_markdown_outputs(bank_dir: Path) -> dict:
    """
    Validate markdown outputs before processing.

    Args:
        bank_dir: Path to bank directory

    Returns:
        Validation results
    """
    logger.info("Validating markdown outputs...")
    results = validate_bank_outputs(str(bank_dir))

    errors = []
    warnings = []

    for file_type, result in results.items():
        errors.extend([f"{file_type}: {e}" for e in result.get('errors', [])])
        warnings.extend([f"{file_type}: {w}" for w in result.get('warnings', [])])

    if errors:
        logger.error(f"Markdown validation failed with {len(errors)} errors")
        for err in errors:
            logger.error(f"  {err}")

    if warnings:
        logger.warning(f"Markdown validation has {len(warnings)} warnings")
        for warn in warnings[:5]:  # Limit to first 5
            logger.warning(f"  {warn}")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }
```

Update `run_pipeline()` function to call validation:

```python
def run_pipeline(path_input: str, skip_verification: bool = False) -> dict:
    # ... existing code ...

    # NEW: Step 0.5 - Validate markdown outputs
    logger.info("\n[0.5/3] Validating markdown structure...")
    md_validation = validate_markdown_outputs(bank_dir)
    result["steps"]["markdown_validation"] = "success" if md_validation['valid'] else "warnings"
    result["markdown_errors"] = md_validation.get('errors', [])

    # Continue with existing steps...
```

---

## Step 2.4: Test Markdown Parser

```bash
# Test on a single file
python tools/markdown_parser.py outputs/phase-1-european-tier1/barclays/1-evidence/tier1-evidence.md

# Test on entire bank
python tools/markdown_parser.py outputs/phase-1-european-tier1/barclays/
```

**Expected Output**:
```
Validating bank outputs: barclays

[OK] tier1_evidence
[OK] tier2_evidence
[FAIL] bayesian_tier1
      ERROR: Could not parse combined likelihood ratio
[OK] gate_pre-mortem
[OK] gate_gate-1
      WARN: Missing section: observable implications

==================================================
Overall: INVALID
```

---

## Phase 2 Completion Checklist

- [ ] `tools/markdown_parser.py` created with all parsers
- [ ] `templates/markdown-schemas.json` created
- [ ] `run_pipeline.py` updated to call validation
- [ ] Parser tested on existing outputs
- [ ] All critical errors fixed in existing outputs
- [ ] Git commit made

```bash
git add tools/markdown_parser.py templates/markdown-schemas.json
git add tools/run_pipeline.py
git commit -m "Phase 2: Add markdown schema validation

- Created markdown_parser.py with evidence, Bayesian, gate parsers
- Created markdown-schemas.json with validation rules
- Integrated validation into run_pipeline.py
- Validates structure before processing"
```

---

# Phase 3: Bayesian Validation Engine

**Effort**: 6-8 hours
**Dependencies**: Phase 2
**Fixes Addressed**: #2 (Bayesian Validation), #5 (LR Independence)

## Step 3.1: Create Bayesian Calculator

**File**: `tools/bayesian_calculator.py`

```python
"""
CDM Research Protocol - Bayesian Calculator v1.0

Python implementation of Bayesian probability updates.
Used to validate agent calculations and detect errors.

Features:
- Prior to posterior calculation
- LR table lookups
- Independence checking
- Extreme LR detection
- Agent calculation validation

Usage:
    from bayesian_calculator import BayesianCalculator

    calc = BayesianCalculator()
    result = calc.calculate_posterior(
        prior=0.30,
        evidence_items=[
            {"type": "official_pilot_announcement_with_timeline", "tier": 1},
            {"type": "named_working_group_membership", "tier": 2}
        ]
    )
    print(f"Posterior: {result.posterior:.1%}")
"""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from collections import Counter
from urllib.parse import urlparse

# Import config loader
import sys
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import (
    load_bayesian_tables,
    get_confidence_caps,
    get_extreme_lr_bounds
)


@dataclass
class LRResult:
    """Result of looking up a likelihood ratio."""
    evidence_type: str
    tier: int
    lr: float
    interpretation: str
    found_in_table: bool
    notes: str = ""


@dataclass
class IndependenceCheck:
    """Result of checking evidence independence."""
    independent: bool
    warnings: list = field(default_factory=list)
    adjustments: dict = field(default_factory=dict)


@dataclass
class BayesianResult:
    """Result of a Bayesian calculation."""
    prior: float
    posterior: float
    prior_odds: float
    posterior_odds: float
    combined_lr: float
    individual_lrs: list  # List of LRResult
    independence_check: IndependenceCheck
    confidence_cap: Optional[float]
    capped_posterior: Optional[float]
    warnings: list = field(default_factory=list)
    calculation_trace: str = ""


@dataclass
class ValidationResult:
    """Result of validating agent calculation."""
    valid: bool
    agent_posterior: float
    calculated_posterior: float
    discrepancy: float
    agent_lr: float
    calculated_lr: float
    lr_discrepancy: float
    issues: list = field(default_factory=list)


class BayesianCalculator:
    """
    Performs Bayesian probability calculations for CDM research.
    """

    def __init__(self):
        """Initialize with LR tables from config."""
        self.lr_tables = load_bayesian_tables()
        self.confidence_caps = get_confidence_caps()
        self.extreme_lr_bounds = get_extreme_lr_bounds()

        # Build flat lookup of all evidence types
        self._build_lr_lookup()

    def _build_lr_lookup(self):
        """Build a flat dictionary of evidence_type -> LR info."""
        self.lr_lookup = {}

        for tier_key in ['tier1_evidence', 'tier2_evidence', 'tier3_evidence', 'tier4_evidence']:
            tier_data = self.lr_tables.get(tier_key, {})
            tier_num = int(tier_key[4])  # Extract number from 'tierN_evidence'

            evidence_types = tier_data.get('evidence_types', {})
            for ev_type, ev_info in evidence_types.items():
                self.lr_lookup[ev_type] = {
                    'tier': tier_num,
                    'lr': ev_info.get('lr', 1.0),
                    'interpretation': ev_info.get('interpretation', ''),
                    'p_e_given_architect': ev_info.get('p_e_given_architect', 0.5),
                    'p_e_given_pragmatist': ev_info.get('p_e_given_pragmatist', 0.5)
                }

    def lookup_lr(self, evidence_type: str, tier: int = None) -> LRResult:
        """
        Look up likelihood ratio for an evidence type.

        Args:
            evidence_type: Type of evidence (e.g., 'official_pilot_announcement_with_timeline')
            tier: Optional tier hint

        Returns:
            LRResult with LR value and metadata
        """
        if evidence_type in self.lr_lookup:
            info = self.lr_lookup[evidence_type]
            return LRResult(
                evidence_type=evidence_type,
                tier=info['tier'],
                lr=info['lr'],
                interpretation=info['interpretation'],
                found_in_table=True
            )

        # Not found - return neutral LR with warning
        return LRResult(
            evidence_type=evidence_type,
            tier=tier or 3,
            lr=1.0,
            interpretation="Unknown - using neutral LR",
            found_in_table=False,
            notes=f"Evidence type '{evidence_type}' not found in LR tables"
        )

    def check_independence(self, evidence_items: list) -> IndependenceCheck:
        """
        Check if evidence items are independent.

        Flags:
        - Same URL appearing multiple times
        - Multiple items from same domain
        - Causally linked evidence (e.g., vendor + vendor confirmation)

        Args:
            evidence_items: List of dicts with 'source_url' field

        Returns:
            IndependenceCheck with warnings and suggested adjustments
        """
        result = IndependenceCheck(independent=True)

        if not evidence_items:
            return result

        # Check 1: Duplicate URLs
        urls = [item.get('source_url', '') for item in evidence_items if item.get('source_url')]
        url_counts = Counter(urls)

        for url, count in url_counts.items():
            if count > 1:
                result.independent = False
                result.warnings.append(f"DUPLICATE_URL: '{url[:50]}...' appears {count} times")
                result.adjustments[url] = f"Count only once (not {count}x)"

        # Check 2: Domain concentration
        def extract_domain(url):
            try:
                parsed = urlparse(url)
                domain = parsed.netloc.lower()
                if domain.startswith('www.'):
                    domain = domain[4:]
                return domain
            except:
                return 'unknown'

        domains = [extract_domain(item.get('source_url', '')) for item in evidence_items]
        domain_counts = Counter(d for d in domains if d and d != 'unknown')

        for domain, count in domain_counts.items():
            if count > 2:
                result.warnings.append(
                    f"DOMAIN_CONCENTRATION: {count} items from {domain} - consider if independent"
                )

        # Check 3: Vendor + vendor confirmation pattern
        evidence_types = [item.get('type', '') for item in evidence_items]
        has_vendor_claim = any('vendor' in t.lower() for t in evidence_types)
        has_vendor_confirmation = any('confirm' in t.lower() for t in evidence_types)

        if has_vendor_claim and has_vendor_confirmation:
            result.warnings.append(
                "CAUSAL_LINK: Vendor claim and confirmation may not be independent"
            )

        return result

    def calculate_posterior(
        self,
        prior: float,
        evidence_items: list,
        apply_cap: bool = True
    ) -> BayesianResult:
        """
        Calculate posterior probability from prior and evidence.

        Args:
            prior: Prior probability of Architect (0.0 to 1.0)
            evidence_items: List of dicts with 'type' and optionally 'tier', 'source_url'
            apply_cap: Whether to apply confidence caps

        Returns:
            BayesianResult with full calculation details
        """
        warnings = []
        calculation_lines = []

        # Step 1: Calculate prior odds
        prior_odds = prior / (1 - prior) if prior < 1 else float('inf')
        calculation_lines.append(f"Prior: P(Architect) = {prior:.2%}")
        calculation_lines.append(f"Prior Odds = {prior:.2f} / {1-prior:.2f} = {prior_odds:.3f}")

        # Step 2: Look up LRs for each evidence item
        individual_lrs = []
        for item in evidence_items:
            ev_type = item.get('type', item.get('evidence_type', 'unknown'))
            tier = item.get('tier')

            lr_result = self.lookup_lr(ev_type, tier)
            individual_lrs.append(lr_result)

            if not lr_result.found_in_table:
                warnings.append(lr_result.notes)

            calculation_lines.append(
                f"  {ev_type}: LR = {lr_result.lr} ({lr_result.interpretation})"
            )

        # Step 3: Check independence
        independence = self.check_independence(evidence_items)
        if not independence.independent:
            warnings.extend(independence.warnings)

        # Step 4: Calculate combined LR
        combined_lr = 1.0
        for lr_result in individual_lrs:
            combined_lr *= lr_result.lr

        calculation_lines.append(f"\nCombined LR = {' × '.join(str(lr.lr) for lr in individual_lrs)}")
        calculation_lines.append(f"           = {combined_lr:.4f}")

        # Check for extreme LR
        lower_bound, upper_bound = self.extreme_lr_bounds
        if combined_lr > upper_bound:
            warnings.append(f"EXTREME_LR: Combined LR ({combined_lr:.2f}) exceeds {upper_bound}")
        elif combined_lr < lower_bound:
            warnings.append(f"EXTREME_LR: Combined LR ({combined_lr:.4f}) below {lower_bound}")

        # Step 5: Calculate posterior odds
        posterior_odds = prior_odds * combined_lr
        calculation_lines.append(f"\nPosterior Odds = {prior_odds:.3f} × {combined_lr:.4f} = {posterior_odds:.4f}")

        # Step 6: Convert to probability
        posterior = posterior_odds / (1 + posterior_odds) if posterior_odds < float('inf') else 1.0
        calculation_lines.append(f"\nP(Architect | Evidence) = {posterior_odds:.4f} / (1 + {posterior_odds:.4f})")
        calculation_lines.append(f"                        = {posterior:.2%}")

        # Step 7: Apply confidence cap if needed
        confidence_cap = None
        capped_posterior = None

        if apply_cap and individual_lrs:
            highest_tier = min(lr.tier for lr in individual_lrs)
            cap = self.confidence_caps.get(highest_tier, 0.35)
            confidence_cap = cap

            if posterior > cap:
                capped_posterior = cap
                calculation_lines.append(f"\nConfidence cap (Tier {highest_tier}): {cap:.0%}")
                calculation_lines.append(f"Capped posterior: {capped_posterior:.2%}")
                warnings.append(f"Posterior capped from {posterior:.1%} to {cap:.0%} (Tier {highest_tier} evidence)")

        return BayesianResult(
            prior=prior,
            posterior=posterior,
            prior_odds=prior_odds,
            posterior_odds=posterior_odds,
            combined_lr=combined_lr,
            individual_lrs=individual_lrs,
            independence_check=independence,
            confidence_cap=confidence_cap,
            capped_posterior=capped_posterior,
            warnings=warnings,
            calculation_trace='\n'.join(calculation_lines)
        )

    def validate_agent_calculation(
        self,
        agent_posterior: float,
        agent_combined_lr: float,
        prior: float,
        evidence_items: list,
        tolerance: float = 0.05
    ) -> ValidationResult:
        """
        Validate an agent's Bayesian calculation against Python calculation.

        Args:
            agent_posterior: Agent's reported posterior probability
            agent_combined_lr: Agent's reported combined LR
            prior: Prior probability used
            evidence_items: Evidence items used
            tolerance: Acceptable discrepancy (default 5%)

        Returns:
            ValidationResult with comparison details
        """
        # Calculate using Python
        result = self.calculate_posterior(prior, evidence_items, apply_cap=False)

        # Compare
        posterior_discrepancy = abs(agent_posterior - result.posterior)
        lr_discrepancy = abs(agent_combined_lr - result.combined_lr) / max(agent_combined_lr, result.combined_lr, 0.001)

        issues = []

        if posterior_discrepancy > tolerance:
            issues.append(
                f"Posterior discrepancy: agent={agent_posterior:.1%}, calculated={result.posterior:.1%}, diff={posterior_discrepancy:.1%}"
            )

        if lr_discrepancy > tolerance:
            issues.append(
                f"LR discrepancy: agent={agent_combined_lr:.2f}, calculated={result.combined_lr:.2f}, diff={lr_discrepancy:.1%}"
            )

        # Check for independence issues
        if result.independence_check.warnings:
            issues.extend([f"Independence: {w}" for w in result.independence_check.warnings])

        return ValidationResult(
            valid=len(issues) == 0,
            agent_posterior=agent_posterior,
            calculated_posterior=result.posterior,
            discrepancy=posterior_discrepancy,
            agent_lr=agent_combined_lr,
            calculated_lr=result.combined_lr,
            lr_discrepancy=lr_discrepancy,
            issues=issues
        )


# --- CLI ---

def main():
    import sys

    print("CDM Research Protocol - Bayesian Calculator Test\n")

    calc = BayesianCalculator()

    # Example calculation
    evidence = [
        {"type": "official_pilot_announcement_with_timeline", "tier": 1, "source_url": "https://example.com/pilot"},
        {"type": "named_working_group_membership", "tier": 2, "source_url": "https://isda.org/members"},
        {"type": "no_evidence_after_exhaustive_tier1_search", "tier": 4}
    ]

    result = calc.calculate_posterior(prior=0.30, evidence_items=evidence)

    print("=== Calculation Trace ===")
    print(result.calculation_trace)

    print("\n=== Summary ===")
    print(f"Prior: {result.prior:.1%}")
    print(f"Posterior: {result.posterior:.1%}")
    print(f"Combined LR: {result.combined_lr:.2f}")

    if result.capped_posterior:
        print(f"Capped Posterior: {result.capped_posterior:.1%}")

    if result.warnings:
        print(f"\nWarnings:")
        for w in result.warnings:
            print(f"  - {w}")

    # Test validation
    print("\n=== Validation Test ===")
    validation = calc.validate_agent_calculation(
        agent_posterior=0.75,
        agent_combined_lr=20.0,
        prior=0.30,
        evidence_items=evidence
    )

    print(f"Agent posterior: {validation.agent_posterior:.1%}")
    print(f"Calculated posterior: {validation.calculated_posterior:.1%}")
    print(f"Discrepancy: {validation.discrepancy:.1%}")
    print(f"Valid: {validation.valid}")

    if validation.issues:
        print("Issues:")
        for issue in validation.issues:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()
```

---

## Step 3.2: Integrate Into Pipeline

**Modify**: `tools/run_pipeline.py`

Add after markdown validation:

```python
from bayesian_calculator import BayesianCalculator
from markdown_parser import parse_bayesian_file, parse_evidence_file

def validate_bayesian_calculations(bank_dir: Path) -> dict:
    """
    Validate Bayesian calculations against Python implementation.
    """
    logger.info("Validating Bayesian calculations...")

    calc = BayesianCalculator()
    results = {'valid': True, 'issues': [], 'warnings': []}

    evidence_dir = bank_dir / "1-evidence"
    bayesian_dir = bank_dir / "2-bayesian"

    if not bayesian_dir.exists():
        return results

    # For each tier, validate the calculation
    prior = 0.30  # Default prior

    for tier in [1, 2, 3]:
        bayesian_file = bayesian_dir / f"post-tier{tier}-update.md"
        evidence_file = evidence_dir / f"tier{tier}-evidence.md"

        if not bayesian_file.exists():
            continue

        # Parse agent's output
        agent_update, parse_result = parse_bayesian_file(str(bayesian_file))
        if not agent_update:
            results['issues'].append(f"Tier {tier}: Could not parse Bayesian file")
            continue

        # Parse evidence
        evidence_blocks, _ = parse_evidence_file(str(evidence_file)) if evidence_file.exists() else ([], None)

        # Convert evidence blocks to calculator format
        evidence_items = []
        for block in evidence_blocks:
            # Map block to evidence type (simplified - you'd need more sophisticated mapping)
            evidence_items.append({
                'type': 'unknown',  # Would need to infer from block content
                'tier': block.tier,
                'source_url': block.source_url
            })

        # Validate calculation
        validation = calc.validate_agent_calculation(
            agent_posterior=agent_update.posterior_architect,
            agent_combined_lr=agent_update.combined_lr,
            prior=prior,
            evidence_items=evidence_items
        )

        if not validation.valid:
            results['valid'] = False
            results['issues'].extend([f"Tier {tier}: {i}" for i in validation.issues])

        # Use this posterior as prior for next tier
        prior = agent_update.posterior_architect

    return results
```

---

## Step 3.3: Test Bayesian Calculator

```bash
python tools/bayesian_calculator.py
```

**Expected Output**:
```
CDM Research Protocol - Bayesian Calculator Test

=== Calculation Trace ===
Prior: P(Architect) = 30.00%
Prior Odds = 0.30 / 0.70 = 0.429
  official_pilot_announcement_with_timeline: LR = 27.0 (Very strong Architect)
  named_working_group_membership: LR = 3.7 (Moderate Architect)
  no_evidence_after_exhaustive_tier1_search: LR = 0.21 (Moderate Pragmatist)

Combined LR = 27.0 × 3.7 × 0.21
           = 20.9790

Posterior Odds = 0.429 × 20.9790 = 8.9971

P(Architect | Evidence) = 8.9971 / (1 + 8.9971)
                        = 90.00%

Confidence cap (Tier 1): 95%

=== Summary ===
Prior: 30.0%
Posterior: 90.0%
Combined LR: 20.98
```

---

## Phase 3 Completion Checklist

- [ ] `tools/bayesian_calculator.py` created
- [ ] Calculator tested standalone
- [ ] Pipeline integration added
- [ ] Independence checking working
- [ ] Extreme LR detection working
- [ ] Git commit made

```bash
git add tools/bayesian_calculator.py
git add tools/run_pipeline.py
git commit -m "Phase 3: Add Bayesian validation engine

- Created bayesian_calculator.py with full Bayesian math
- Added LR independence checking (duplicate URL, domain concentration)
- Added extreme LR detection
- Integrated validation into pipeline"
```

---

# Phase 4: Real-Time URL Validation

**Effort**: 3-4 hours
**Dependencies**: Phase 1
**Fixes Addressed**: #6 (Real-Time URL Validation)

## Step 4.1: Create URL Validator

**File**: `tools/url_validator.py`

```python
"""
CDM Research Protocol - URL Validator v1.0

Lightweight URL validation for evidence sources.
Supports quick HEAD checks and full content verification.

Features:
- Quick HEAD request validation
- Full GET with content hashing
- Batch validation with rate limiting
- Wayback Machine fallback suggestions
- Session caching

Usage:
    from url_validator import URLValidator

    validator = URLValidator()
    status = validator.check_url("https://example.com/article")
    print(status.alive, status.status_code)
"""

import time
import hashlib
import requests
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# Rate limiting
REQUEST_DELAY = 0.5  # seconds between requests to same domain
MAX_CONCURRENT = 5


@dataclass
class URLStatus:
    """Status of a URL check."""
    url: str
    alive: bool
    status_code: int
    content_type: Optional[str] = None
    content_hash: Optional[str] = None
    final_url: Optional[str] = None
    error: Optional[str] = None
    wayback_url: Optional[str] = None
    check_time: float = 0.0


class URLValidator:
    """
    Validates URLs for evidence sources.
    """

    def __init__(self, cache_path: Optional[str] = None, timeout: int = 10):
        """
        Initialize validator.

        Args:
            cache_path: Optional path to cache file
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (ResearchBot/2.3; CDMValidator)'
        })

        # Domain rate limiting
        self.last_request_time: Dict[str, float] = {}

        # Cache
        self.cache: Dict[str, URLStatus] = {}
        self.cache_path = Path(cache_path) if cache_path else None

        if self.cache_path and self.cache_path.exists():
            self._load_cache()

    def _load_cache(self):
        """Load cache from file."""
        try:
            data = json.loads(self.cache_path.read_text())
            for url, status_dict in data.items():
                self.cache[url] = URLStatus(**status_dict)
        except Exception:
            pass

    def _save_cache(self):
        """Save cache to file."""
        if not self.cache_path:
            return

        data = {
            url: {
                'url': s.url,
                'alive': s.alive,
                'status_code': s.status_code,
                'content_type': s.content_type,
                'content_hash': s.content_hash,
                'final_url': s.final_url,
                'error': s.error,
                'wayback_url': s.wayback_url,
                'check_time': s.check_time
            }
            for url, s in self.cache.items()
        }
        self.cache_path.write_text(json.dumps(data, indent=2))

    def _rate_limit(self, domain: str):
        """Apply rate limiting for domain."""
        last_time = self.last_request_time.get(domain, 0)
        elapsed = time.time() - last_time

        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)

        self.last_request_time[domain] = time.time()

    def _get_wayback_url(self, url: str) -> Optional[str]:
        """Get Wayback Machine URL for a dead link."""
        try:
            api_url = f"http://archive.org/wayback/available?url={url}"
            response = self.session.get(api_url, timeout=5)
            data = response.json()

            snapshot = data.get('archived_snapshots', {}).get('closest', {})
            if snapshot.get('available'):
                return snapshot.get('url')
        except Exception:
            pass

        return None

    def check_url(self, url: str, quick: bool = True, use_cache: bool = True) -> URLStatus:
        """
        Check if a URL is alive.

        Args:
            url: URL to check
            quick: If True, use HEAD request only. If False, GET full content.
            use_cache: Whether to use/update cache

        Returns:
            URLStatus with check results
        """
        # Check cache
        if use_cache and url in self.cache:
            cached = self.cache[url]
            # Cache valid for 1 hour
            if time.time() - cached.check_time < 3600:
                return cached

        start_time = time.time()

        try:
            parsed = urlparse(url)
            domain = parsed.netloc

            # Rate limit
            self._rate_limit(domain)

            if quick:
                response = self.session.head(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True
                )
            else:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True
                )

            status = URLStatus(
                url=url,
                alive=200 <= response.status_code < 400,
                status_code=response.status_code,
                content_type=response.headers.get('Content-Type'),
                final_url=response.url if response.url != url else None,
                check_time=time.time()
            )

            # Calculate content hash for full GET
            if not quick and response.status_code == 200:
                status.content_hash = hashlib.sha256(response.content).hexdigest()[:16]

            # Get Wayback URL for dead links
            if not status.alive:
                status.wayback_url = self._get_wayback_url(url)

        except requests.Timeout:
            status = URLStatus(
                url=url,
                alive=False,
                status_code=0,
                error="Timeout",
                check_time=time.time()
            )
        except requests.RequestException as e:
            status = URLStatus(
                url=url,
                alive=False,
                status_code=0,
                error=str(e)[:100],
                check_time=time.time()
            )

        # Update cache
        if use_cache:
            self.cache[url] = status
            self._save_cache()

        return status

    def check_batch(
        self,
        urls: list,
        quick: bool = True,
        progress_callback=None
    ) -> Dict[str, URLStatus]:
        """
        Check multiple URLs with parallel execution.

        Args:
            urls: List of URLs to check
            quick: Use HEAD requests
            progress_callback: Optional callback(completed, total)

        Returns:
            Dict mapping URL to status
        """
        results = {}
        completed = 0

        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
            future_to_url = {
                executor.submit(self.check_url, url, quick): url
                for url in urls
            }

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    results[url] = future.result()
                except Exception as e:
                    results[url] = URLStatus(
                        url=url,
                        alive=False,
                        status_code=0,
                        error=str(e)[:100],
                        check_time=time.time()
                    )

                completed += 1
                if progress_callback:
                    progress_callback(completed, len(urls))

        return results


def validate_evidence_urls(evidence_file: str) -> dict:
    """
    Validate all URLs in an evidence file.

    Args:
        evidence_file: Path to evidence markdown or JSON file

    Returns:
        Validation results
    """
    from markdown_parser import parse_evidence_file

    path = Path(evidence_file)
    validator = URLValidator()

    if path.suffix == '.md':
        blocks, _ = parse_evidence_file(str(path))
        urls = [b.source_url for b in blocks if b.source_url]
    elif path.suffix == '.json':
        data = json.loads(path.read_text())
        urls = [item.get('source_url') for item in data.get('evidence_items', []) if item.get('source_url')]
    else:
        return {'error': f'Unsupported file type: {path.suffix}'}

    print(f"Checking {len(urls)} URLs...")

    def progress(completed, total):
        print(f"  Progress: {completed}/{total}", end='\r')

    results = validator.check_batch(urls, quick=True, progress_callback=progress)
    print()  # New line after progress

    alive = sum(1 for s in results.values() if s.alive)
    dead = len(results) - alive

    summary = {
        'total': len(urls),
        'alive': alive,
        'dead': dead,
        'alive_rate': alive / len(urls) if urls else 0,
        'dead_urls': [
            {
                'url': s.url,
                'status_code': s.status_code,
                'error': s.error,
                'wayback': s.wayback_url
            }
            for s in results.values() if not s.alive
        ]
    }

    return summary


# --- CLI ---

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python url_validator.py <url_or_file>")
        print("       python url_validator.py https://example.com")
        print("       python url_validator.py outputs/phase-1/barclays/1-evidence/tier1-evidence.md")
        sys.exit(1)

    target = sys.argv[1]

    if target.startswith('http'):
        # Single URL check
        validator = URLValidator()
        status = validator.check_url(target, quick=False)

        print(f"URL: {status.url}")
        print(f"Alive: {status.alive}")
        print(f"Status Code: {status.status_code}")
        print(f"Content Type: {status.content_type}")
        print(f"Final URL: {status.final_url}")

        if status.error:
            print(f"Error: {status.error}")

        if status.wayback_url:
            print(f"Wayback URL: {status.wayback_url}")

        if status.content_hash:
            print(f"Content Hash: {status.content_hash}")

    else:
        # File validation
        results = validate_evidence_urls(target)

        print(f"\n=== URL Validation Results ===")
        print(f"Total URLs: {results['total']}")
        print(f"Alive: {results['alive']} ({results['alive_rate']:.0%})")
        print(f"Dead: {results['dead']}")

        if results.get('dead_urls'):
            print(f"\nDead URLs:")
            for dead in results['dead_urls']:
                print(f"  {dead['url'][:60]}...")
                if dead.get('wayback'):
                    print(f"    Wayback: {dead['wayback']}")
                elif dead.get('error'):
                    print(f"    Error: {dead['error']}")


if __name__ == "__main__":
    main()
```

---

## Step 4.2: Add to Pipeline

**Modify**: `tools/run_pipeline.py`

Add option for pre-validation:

```python
parser.add_argument(
    '--validate-urls-first',
    action='store_true',
    help="Validate URLs before processing (catches dead links early)"
)

# In run_pipeline():
if args.validate_urls_first:
    from url_validator import validate_evidence_urls

    evidence_dir = bank_dir / "1-evidence"
    for tier_file in evidence_dir.glob("tier*-evidence.md"):
        url_results = validate_evidence_urls(str(tier_file))
        if url_results.get('dead', 0) > 0:
            logger.warning(f"Found {url_results['dead']} dead URLs in {tier_file.name}")
            result["flags"].append("DEAD_URLS_DETECTED")
```

---

## Phase 4 Completion Checklist

- [ ] `tools/url_validator.py` created
- [ ] Batch validation with rate limiting working
- [ ] Wayback fallback suggestions implemented
- [ ] Pipeline integration added
- [ ] Git commit made

```bash
git add tools/url_validator.py
git add tools/run_pipeline.py
git commit -m "Phase 4: Add real-time URL validation

- Created url_validator.py with HEAD/GET checking
- Added batch validation with rate limiting
- Added Wayback Machine fallback suggestions
- Added --validate-urls-first option to pipeline"
```

---

# Phase 5: Enhanced QA Validator

**Effort**: 4-6 hours
**Dependencies**: Phase 3
**Fixes Addressed**: #7 (QA Validator)

## Step 5.1: Create Anchor Points Configuration

**File**: `config/anchor-points.json`

```json
{
  "$schema": "CDM/DRR Anchor Points v1.0",
  "description": "Immutable facts that no classification can violate",

  "production_banks": {
    "description": "Banks confirmed in CDM production as of knowledge cutoff",
    "banks": [
      {"id": "bnp-paribas", "date": "2022-Q3", "source": "ISDA official announcement"},
      {"id": "jpmorgan", "date": "2024-10", "source": "ISDA official announcement"},
      {"id": "jscc", "date": "2023", "source": "ISDA official announcement"},
      {"id": "pictet", "date": "2024", "source": "FINOS announcement"}
    ],
    "constraint": "These banks MUST be classified as ARCHITECT-Native"
  },

  "confirmed_contributors": {
    "description": "Banks confirmed as CDM contributors",
    "banks": [
      {"id": "barclays", "evidence": "Lee Braine public advocacy, ISDA working groups"},
      {"id": "standard-chartered", "evidence": "FINOS contributor lists"}
    ],
    "constraint": "These banks MUST be classified as ARCHITECT (any variant) or have explicit contrary evidence"
  },

  "regulatory_deadlines": {
    "emir_refit_eu": "2024-04-29",
    "emir_refit_uk": "2024-09-30",
    "cftc_rewrite": "2025-01-01",
    "constraint": "Post-deadline evidence for EU/UK banks carries higher weight"
  },

  "first_major_bank": {
    "bank": "bnp-paribas",
    "date": "2022-Q3",
    "constraint": "No other bank can claim production before this date without exceptional evidence"
  }
}
```

---

## Step 5.2: Extend Cross-Bank Validator

**Modify**: `tools/cross_bank_validator.py`

Add the 5 consistency tests from qa-validator.md:

```python
# Add these imports at top
from config_loader import load_bank_manifest, get_default_priors

# Add after existing check functions:

def load_anchor_points() -> dict:
    """Load anchor points configuration."""
    path = Path(__file__).parent.parent / "config" / "anchor-points.json"
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {}


def check_ordinal_ranking(statuses: dict) -> list:
    """
    Test 1: Ordinal Ranking Consistency

    If Bank A has stronger evidence than Bank B on every dimension,
    then A must rank >= B in classification hierarchy.

    Hierarchy: ARCHITECT-Native > Leader > Follower > PRAGMATIST
    """
    issues = []

    HIERARCHY = {
        'ARCHITECT': {'Native': 4, 'Leader': 3, 'Follower': 2},
        'PRAGMATIST': {'*': 1},
        'OBSERVER': {'*': 0},
        'UNKNOWN': {'*': -1}
    }

    def get_rank(status: dict) -> int:
        classification = status.get('classification', 'UNKNOWN').upper()
        sub = status.get('sub_classification', '*')

        if classification in HIERARCHY:
            variants = HIERARCHY[classification]
            return variants.get(sub, variants.get('*', 0))
        return -1

    # Compare banks with confidence data
    banks_with_data = [
        (bank, s) for bank, s in statuses.items()
        if not s.get('_error') and s.get('confidence', 0) > 0
    ]

    for i, (bank_a, status_a) in enumerate(banks_with_data):
        for bank_b, status_b in banks_with_data[i+1:]:
            rank_a = get_rank(status_a)
            rank_b = get_rank(status_b)
            conf_a = status_a.get('confidence', 0)
            conf_b = status_b.get('confidence', 0)

            # If A has higher confidence but lower rank, flag it
            if conf_a > conf_b + 10 and rank_a < rank_b:
                issues.append({
                    'bank': f"{bank_a} vs {bank_b}",
                    'check': 'ordinal_ranking',
                    'issue': f"{bank_a} has higher confidence ({conf_a}%) but lower rank than {bank_b} ({conf_b}%)"
                })

    return issues


def check_similar_profiles(statuses: dict) -> list:
    """
    Test 2: Similar Profile Cohorts

    Banks with similar business models, regions, and derivatives exposure
    should have similar classifications unless exceptional circumstances.
    """
    issues = []

    try:
        manifest = load_bank_manifest()
        banks_config = {b['id']: b for b in manifest.get('banks', [])}
    except:
        return issues  # Can't run without manifest

    # Group by region
    by_region = {}
    for bank, status in statuses.items():
        if bank in banks_config:
            region = banks_config[bank].get('region', 'Unknown')
            if region not in by_region:
                by_region[region] = []
            by_region[region].append((bank, status))

    # Check for outliers within regions
    for region, banks in by_region.items():
        if len(banks) < 2:
            continue

        classifications = [s.get('classification', 'UNKNOWN') for _, s in banks]
        class_counts = Counter(classifications)

        # If one bank is very different from peers
        majority_class = class_counts.most_common(1)[0][0]
        majority_count = class_counts.most_common(1)[0][1]

        if majority_count >= len(banks) - 1 and len(banks) >= 3:
            # One outlier
            for bank, status in banks:
                if status.get('classification') != majority_class:
                    issues.append({
                        'bank': bank,
                        'check': 'similar_profiles',
                        'issue': f"Outlier in {region}: {bank} is {status.get('classification')} while {majority_count} peers are {majority_class}"
                    })

    return issues


def check_evidence_confidence_correlation(statuses: dict) -> list:
    """
    Test 3: Evidence-Confidence Correlation

    More/higher-tier evidence should correlate with higher confidence.
    Banks with only Tier 3 evidence shouldn't have >50% confidence.
    """
    issues = []

    # This would need evidence data - simplified check based on classification
    for bank, status in statuses.items():
        if status.get('_error'):
            continue

        confidence = status.get('confidence', 0)
        classification = status.get('classification', '').upper()

        # ARCHITECT classifications should have higher confidence
        if classification == 'ARCHITECT' and confidence < 60:
            issues.append({
                'bank': bank,
                'check': 'evidence_confidence',
                'issue': f"ARCHITECT classification with only {confidence}% confidence - needs stronger evidence"
            })

        # UNKNOWN shouldn't have high confidence
        if classification == 'UNKNOWN' and confidence > 50:
            issues.append({
                'bank': bank,
                'check': 'evidence_confidence',
                'issue': f"UNKNOWN classification with {confidence}% confidence - contradictory"
            })

    return issues


def check_classification_distribution(statuses: dict) -> list:
    """
    Test 4: Classification Distribution Sanity

    Global distribution should roughly match priors (~30% Architect, ~70% Pragmatist).
    Flag if Architects > 40% or if all banks have same classification.
    """
    issues = []

    valid_statuses = [s for s in statuses.values() if not s.get('_error')]
    if not valid_statuses:
        return issues

    classifications = [s.get('classification', 'UNKNOWN').upper() for s in valid_statuses]
    counts = Counter(classifications)
    total = len(classifications)

    architect_count = counts.get('ARCHITECT', 0)
    architect_pct = architect_count / total

    # Expected: ~30% Architects based on default priors
    if architect_pct > 0.45:
        issues.append({
            'bank': 'GLOBAL',
            'check': 'distribution',
            'issue': f"High ARCHITECT rate: {architect_pct:.0%} ({architect_count}/{total}) - expected ~30%"
        })
    elif architect_pct < 0.10 and total >= 10:
        issues.append({
            'bank': 'GLOBAL',
            'check': 'distribution',
            'issue': f"Low ARCHITECT rate: {architect_pct:.0%} ({architect_count}/{total}) - verify not under-classifying"
        })

    # All same classification is suspicious
    if len(counts) == 1 and total >= 5:
        issues.append({
            'bank': 'GLOBAL',
            'check': 'distribution',
            'issue': f"All {total} banks have same classification: {list(counts.keys())[0]}"
        })

    return issues


def check_anchor_points(statuses: dict) -> list:
    """
    Test 5: Anchor Point Coherence

    No classification can violate immutable facts (e.g., known production banks).
    """
    issues = []

    anchors = load_anchor_points()
    if not anchors:
        return issues

    # Check production banks
    for prod_bank in anchors.get('production_banks', {}).get('banks', []):
        bank_id = prod_bank['id']

        if bank_id in statuses:
            status = statuses[bank_id]
            classification = status.get('classification', '').upper()
            sub = status.get('sub_classification', '')

            if classification != 'ARCHITECT' or sub != 'Native':
                issues.append({
                    'bank': bank_id,
                    'check': 'anchor_point',
                    'issue': f"ANCHOR VIOLATION: {bank_id} is in production (since {prod_bank['date']}) but classified as {classification} {sub}"
                })

    # Check confirmed contributors
    for contrib_bank in anchors.get('confirmed_contributors', {}).get('banks', []):
        bank_id = contrib_bank['id']

        if bank_id in statuses:
            status = statuses[bank_id]
            classification = status.get('classification', '').upper()

            if classification not in ['ARCHITECT']:
                issues.append({
                    'bank': bank_id,
                    'check': 'anchor_point',
                    'issue': f"ANCHOR WARNING: {bank_id} is confirmed contributor but classified as {classification}"
                })

    return issues


# Update run_checks to include new tests:

def run_checks(outputs_dir: Path) -> dict:
    """Run all cross-bank validation checks."""
    statuses = load_all_statuses(outputs_dir)

    if not statuses:
        return {
            'banks': 0,
            'issues': [{'bank': 'N/A', 'check': 'load', 'issue': 'No bank status files found'}],
            'passed': False
        }

    all_issues = []

    # Original checks
    all_issues.extend(check_probability_sanity(statuses))
    all_issues.extend(check_taxonomy(statuses))
    all_issues.extend(check_alignment(statuses))
    all_issues.extend(check_confidence_bounds(statuses))

    # NEW: QA validator checks
    all_issues.extend(check_ordinal_ranking(statuses))
    all_issues.extend(check_similar_profiles(statuses))
    all_issues.extend(check_evidence_confidence_correlation(statuses))
    all_issues.extend(check_classification_distribution(statuses))
    all_issues.extend(check_anchor_points(statuses))

    summary = generate_summary(statuses)

    # Separate critical (anchor violations) from warnings
    critical_issues = [i for i in all_issues if 'ANCHOR VIOLATION' in i.get('issue', '')]

    return {
        'banks': len(statuses),
        'issues': all_issues,
        'critical': critical_issues,
        'passed': len(critical_issues) == 0,  # Fail only on critical issues
        'summary': summary
    }
```

---

## Step 5.3: Test Enhanced Validator

```bash
python tools/cross_bank_validator.py outputs/
```

**Expected Output** (with new checks):
```
============================================================
CROSS-BANK VALIDATION: PASSED
============================================================

Summary:
  Banks analyzed: 31
  Classifications: {'ARCHITECT': 5, 'PRAGMATIST': 20, ...}

Issues (3):

  barclays:
    [anchor_point] ANCHOR WARNING: barclays is confirmed contributor but classified as ARCHITECT Follower

  GLOBAL:
    [distribution] Classification distribution looks reasonable

  deutsche-bank vs ubs:
    [ordinal_ranking] Check peer ranking consistency

Critical Issues: 0

============================================================
```

---

## Phase 5 Completion Checklist

- [ ] `config/anchor-points.json` created
- [ ] 5 new consistency tests added to `cross_bank_validator.py`
- [ ] Anchor point violations treated as critical
- [ ] All tests working
- [ ] Git commit made

```bash
git add config/anchor-points.json
git add tools/cross_bank_validator.py
git commit -m "Phase 5: Enhanced QA validator

- Created anchor-points.json with immutable facts
- Added 5 consistency tests from qa-validator.md:
  - Ordinal ranking
  - Similar profile cohorts
  - Evidence-confidence correlation
  - Classification distribution
  - Anchor point coherence
- Anchor violations treated as critical failures"
```

---

# Phase 6: Full Integration Layer

**Effort**: 8-12 hours
**Dependencies**: All previous phases
**Fixes Addressed**: #1 (Integration Layer)

## Step 6.1: Create Research Runner

**File**: `tools/research_runner.py`

```python
"""
CDM Research Protocol - Research Runner v1.0

End-to-end research execution for banks.
Orchestrates all tools and validates at each stage.

Usage:
    python research_runner.py --bank barclays --phase 1
    python research_runner.py --phase 1 --all
    python research_runner.py --validate-only outputs/phase-1/barclays/
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import load_bank_manifest, get_bank_config
from markdown_parser import validate_bank_outputs
from bayesian_calculator import BayesianCalculator
from url_validator import URLValidator
from trust_audit import run_trust_audit
from cross_bank_validator import run_checks
from render_report import render_report
from orchestrate import Orchestrator, Stage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class StageResult:
    """Result of executing a stage."""
    stage: str
    success: bool
    duration_seconds: float
    outputs: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class BankResult:
    """Result of researching a bank."""
    bank_id: str
    phase: int
    success: bool
    classification: Optional[str] = None
    confidence: Optional[float] = None
    stages: List[StageResult] = field(default_factory=list)
    total_duration: float = 0.0


class ResearchRunner:
    """
    Orchestrates end-to-end research for banks.
    """

    def __init__(self, outputs_dir: Path = None):
        self.outputs_dir = outputs_dir or PROJECT_ROOT / "outputs"
        self.bayesian_calc = BayesianCalculator()
        self.url_validator = URLValidator()

    def get_bank_dir(self, bank_id: str, phase: int) -> Path:
        """Get output directory for a bank."""
        # Find the phase directory
        for phase_dir in self.outputs_dir.iterdir():
            if phase_dir.is_dir() and f"phase-{phase}" in phase_dir.name:
                bank_dir = phase_dir / bank_id
                return bank_dir

        # Create if doesn't exist
        phase_name = f"phase-{phase}"
        manifest = load_bank_manifest()
        for phase_info in manifest.get('phases', []):
            if phase_info.get('number') == phase:
                phase_name = f"phase-{phase}-{phase_info.get('name', '')}"
                break

        bank_dir = self.outputs_dir / phase_name / bank_id
        bank_dir.mkdir(parents=True, exist_ok=True)
        return bank_dir

    def validate_stage(self, bank_dir: Path, stage: str) -> StageResult:
        """Validate outputs for a completed stage."""
        start_time = datetime.now()
        result = StageResult(stage=stage, success=True, duration_seconds=0)

        if stage.startswith('tier') and stage.endswith('_evidence'):
            # Validate evidence file
            tier = stage.replace('tier', '').replace('_evidence', '')
            evidence_file = bank_dir / "1-evidence" / f"tier{tier}-evidence.md"

            if not evidence_file.exists():
                result.errors.append(f"Missing: {evidence_file.name}")
                result.success = False
            else:
                from markdown_parser import parse_evidence_file
                blocks, validation = parse_evidence_file(str(evidence_file))

                if not validation.valid:
                    result.errors.extend(validation.errors)
                    result.success = False
                result.warnings.extend(validation.warnings)
                result.outputs.append(str(evidence_file))

        elif stage.startswith('bayesian_'):
            # Validate Bayesian file
            tier = stage.replace('bayesian_', '')
            bayesian_file = bank_dir / "2-bayesian" / f"post-tier{tier}-update.md"

            if not bayesian_file.exists():
                result.errors.append(f"Missing: {bayesian_file.name}")
                result.success = False
            else:
                from markdown_parser import parse_bayesian_file
                update, validation = parse_bayesian_file(str(bayesian_file))

                if not validation.valid:
                    result.errors.extend(validation.errors)
                    result.success = False
                result.warnings.extend(validation.warnings)
                result.outputs.append(str(bayesian_file))

        elif stage.startswith('gate_'):
            # Validate gate file
            gate_name = stage.replace('gate_', '')
            gate_file = bank_dir / "3-gates" / f"{gate_name}.md"

            if not gate_file.exists():
                result.errors.append(f"Missing: {gate_file.name}")
                result.success = False
            else:
                result.outputs.append(str(gate_file))

        result.duration_seconds = (datetime.now() - start_time).total_seconds()
        return result

    def run_validation_pipeline(self, bank_dir: Path) -> dict:
        """
        Run full validation pipeline on existing bank outputs.

        Returns:
            Dict with validation results
        """
        logger.info(f"Running validation pipeline for {bank_dir.name}")

        results = {
            'bank': bank_dir.name,
            'valid': True,
            'stages': {}
        }

        # 1. Validate markdown structure
        logger.info("  [1/4] Validating markdown structure...")
        md_results = validate_bank_outputs(str(bank_dir))
        results['stages']['markdown'] = md_results

        md_errors = sum(len(r.get('errors', [])) for r in md_results.values())
        if md_errors > 0:
            results['valid'] = False

        # 2. Validate URLs
        logger.info("  [2/4] Validating URLs...")
        evidence_dir = bank_dir / "1-evidence"
        url_results = {'alive': 0, 'dead': 0}

        if evidence_dir.exists():
            for tier_file in evidence_dir.glob("tier*-evidence.md"):
                from url_validator import validate_evidence_urls
                tier_urls = validate_evidence_urls(str(tier_file))
                url_results['alive'] += tier_urls.get('alive', 0)
                url_results['dead'] += tier_urls.get('dead', 0)

        results['stages']['urls'] = url_results

        # 3. Run trust audit
        logger.info("  [3/4] Running trust audit...")
        evidence_json = bank_dir / "evidence.json"

        if evidence_json.exists():
            trust_results = run_trust_audit(str(evidence_json))
            results['stages']['trust'] = trust_results.get('trust_metrics', {})
            results['confidence'] = trust_results.get('trust_metrics', {}).get('overall_confidence')

        # 4. Validate status.json
        logger.info("  [4/4] Validating status...")
        status_file = bank_dir / "status.json"

        if status_file.exists():
            status = json.loads(status_file.read_text())
            results['classification'] = status.get('classification')
            results['stages']['status'] = {
                'classification': status.get('classification'),
                'sub_classification': status.get('sub_classification'),
                'confidence': status.get('confidence'),
                'stages_completed': status.get('stages_completed', [])
            }

        return results

    def run_bank(self, bank_id: str, phase: int) -> BankResult:
        """
        Execute full research pipeline for a bank.

        NOTE: This requires human/agent execution of each stage.
        This method orchestrates and validates, but doesn't generate content.

        Args:
            bank_id: Bank identifier
            phase: Phase number

        Returns:
            BankResult with execution details
        """
        start_time = datetime.now()
        bank_dir = self.get_bank_dir(bank_id, phase)

        result = BankResult(
            bank_id=bank_id,
            phase=phase,
            success=True
        )

        logger.info(f"Starting research for {bank_id} (Phase {phase})")
        logger.info(f"Output directory: {bank_dir}")

        # Initialize orchestrator
        orchestrator = Orchestrator(bank_dir)
        status = orchestrator.get_status()

        logger.info(f"Current stage: {status['current_stage']}")
        logger.info(f"Stages completed: {status['stages_completed']}")

        # Validate completed stages
        for stage in status['stages_completed']:
            stage_result = self.validate_stage(bank_dir, stage)
            result.stages.append(stage_result)

            if not stage_result.success:
                result.success = False
                logger.error(f"Stage {stage} validation failed")
                for err in stage_result.errors:
                    logger.error(f"  - {err}")

        # Run full validation pipeline
        validation = self.run_validation_pipeline(bank_dir)
        result.classification = validation.get('classification')
        result.confidence = validation.get('confidence')

        result.total_duration = (datetime.now() - start_time).total_seconds()

        logger.info(f"Research validation complete for {bank_id}")
        logger.info(f"  Classification: {result.classification}")
        logger.info(f"  Confidence: {result.confidence}%")
        logger.info(f"  Duration: {result.total_duration:.1f}s")

        return result

    def run_phase(self, phase: int) -> List[BankResult]:
        """
        Run validation for all banks in a phase.

        Args:
            phase: Phase number

        Returns:
            List of BankResult for each bank
        """
        results = []

        # Find phase directory
        phase_dir = None
        for d in self.outputs_dir.iterdir():
            if d.is_dir() and f"phase-{phase}" in d.name:
                phase_dir = d
                break

        if not phase_dir:
            logger.error(f"Phase {phase} directory not found")
            return results

        # Process each bank
        for bank_dir in sorted(phase_dir.iterdir()):
            if bank_dir.is_dir() and not bank_dir.name.startswith('.'):
                result = self.run_bank(bank_dir.name, phase)
                results.append(result)

        # Run cross-bank validation
        logger.info(f"\nRunning cross-bank validation for Phase {phase}...")
        cross_results = run_checks(phase_dir)

        if not cross_results['passed']:
            logger.warning("Cross-bank validation found issues:")
            for issue in cross_results.get('critical', []):
                logger.error(f"  CRITICAL: {issue['issue']}")

        return results


def main():
    parser = argparse.ArgumentParser(
        description="CDM Research Protocol - Research Runner"
    )
    parser.add_argument('--bank', help="Bank ID to process")
    parser.add_argument('--phase', type=int, help="Phase number")
    parser.add_argument('--all', action='store_true', help="Process all banks in phase")
    parser.add_argument('--validate-only', help="Validate existing outputs (path to bank dir)")
    parser.add_argument('--output', help="Output results to JSON file")

    args = parser.parse_args()
    runner = ResearchRunner()

    if args.validate_only:
        # Validate existing outputs
        bank_dir = Path(args.validate_only)
        results = runner.run_validation_pipeline(bank_dir)

        print(f"\n{'='*60}")
        print(f"VALIDATION RESULTS: {bank_dir.name}")
        print(f"{'='*60}")
        print(f"Valid: {results['valid']}")
        print(f"Classification: {results.get('classification')}")
        print(f"Confidence: {results.get('confidence')}%")

        if args.output:
            Path(args.output).write_text(json.dumps(results, indent=2))

    elif args.bank and args.phase:
        # Single bank
        result = runner.run_bank(args.bank, args.phase)

        if args.output:
            Path(args.output).write_text(json.dumps(asdict(result), indent=2))

    elif args.phase and args.all:
        # All banks in phase
        results = runner.run_phase(args.phase)

        print(f"\n{'='*60}")
        print(f"PHASE {args.phase} RESULTS")
        print(f"{'='*60}")

        for r in results:
            status = "OK" if r.success else "FAIL"
            print(f"[{status}] {r.bank_id}: {r.classification} ({r.confidence}%)")

        if args.output:
            Path(args.output).write_text(json.dumps([asdict(r) for r in results], indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

---

## Step 6.2: Update run_pipeline.py to Use Research Runner

**Modify**: `tools/run_pipeline.py`

Add integration option:

```python
parser.add_argument(
    '--full-validation',
    action='store_true',
    help="Run full validation pipeline including all Phase 1-5 checks"
)

# In run_pipeline():
if args.full_validation:
    from research_runner import ResearchRunner
    runner = ResearchRunner()
    validation = runner.run_validation_pipeline(bank_dir)

    result["full_validation"] = validation
    if not validation['valid']:
        result["status"] = "validation_failed"
```

---

## Step 6.3: Create Quick Reference Card

**File**: `QUICKSTART.md`

```markdown
# CDM Research Protocol - Quick Reference

## Run Full Pipeline on a Bank

```bash
# Validate and process existing outputs
python tools/run_pipeline.py outputs/phase-1-european-tier1/barclays/

# Full validation with all checks
python tools/run_pipeline.py outputs/phase-1-european-tier1/barclays/ --full-validation

# Validate URLs before processing
python tools/run_pipeline.py outputs/phase-1-european-tier1/barclays/ --validate-urls-first
```

## Validate Research Outputs

```bash
# Validate single bank
python tools/research_runner.py --validate-only outputs/phase-1-european-tier1/barclays/

# Validate entire phase
python tools/research_runner.py --phase 1 --all

# Run cross-bank validation
python tools/cross_bank_validator.py outputs/
```

## Individual Tools

```bash
# Check for deprecated terminology
python tools/migrate_terminology.py outputs/

# Test config loader
python tools/config_loader.py

# Parse markdown outputs
python tools/markdown_parser.py outputs/phase-1-european-tier1/barclays/

# Test Bayesian calculations
python tools/bayesian_calculator.py

# Validate URLs
python tools/url_validator.py outputs/phase-1-european-tier1/barclays/1-evidence/tier1-evidence.md

# Run trust audit
python tools/trust_audit.py outputs/phase-1-european-tier1/barclays/evidence.json

# Render final report
python tools/render_report.py outputs/phase-1-european-tier1/barclays/evidence.json
```

## Configuration

All thresholds are in `config/decision-thresholds.json`.
Agent reference: `config/agent-config-reference.md`.
Anchor points: `config/anchor-points.json`.
```

---

## Phase 6 Completion Checklist

- [ ] `tools/research_runner.py` created
- [ ] `run_pipeline.py` updated with `--full-validation`
- [ ] `QUICKSTART.md` created
- [ ] End-to-end validation working
- [ ] Git commit made

```bash
git add tools/research_runner.py QUICKSTART.md
git add tools/run_pipeline.py
git commit -m "Phase 6: Full integration layer

- Created research_runner.py for end-to-end orchestration
- Added --full-validation option to run_pipeline.py
- Created QUICKSTART.md with command reference
- All validation stages connected and working"
```

---

# Final Checklist

After completing all phases:

- [ ] **Phase 0**: Terminology migrated, baseline created
- [ ] **Phase 1**: Config centralized, agent prompts updated
- [ ] **Phase 2**: Markdown validation working
- [ ] **Phase 3**: Bayesian validation engine working
- [ ] **Phase 4**: URL validation working
- [ ] **Phase 5**: QA validator enhanced with 5 tests
- [ ] **Phase 6**: Full integration complete

## Final Validation

```bash
# Run complete validation on all banks
python tools/research_runner.py --phase 1 --all --output phase1-validation.json

# Check cross-bank consistency
python tools/cross_bank_validator.py outputs/

# Verify no deprecated terms
python tools/migrate_terminology.py outputs/

# Generate config reference
python tools/inject_agent_config.py
```

## Final Commit

```bash
git add .
git commit -m "Complete implementation of fixes 1-8

Phases completed:
- Phase 0: Quick wins (terminology, baseline)
- Phase 1: Centralized configuration
- Phase 2: Markdown schema validation
- Phase 3: Bayesian validation engine
- Phase 4: Real-time URL validation
- Phase 5: Enhanced QA validator
- Phase 6: Full integration layer

New tools:
- inject_agent_config.py
- markdown_parser.py
- bayesian_calculator.py
- url_validator.py
- research_runner.py

New config:
- agent-config-reference.md
- anchor-points.json
- markdown-schemas.json

All validation checks passing."
```

---

*Implementation Plan v1.0 - Created 2025-12-19*
