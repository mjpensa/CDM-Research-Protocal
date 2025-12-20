"""
CDM Research Protocol - Agent Config Injector v1.0

Generates agent-config-reference.md from decision-thresholds.json.
Optionally checks agent prompts for hardcoded threshold values.

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
    (r'>\s*80\s*%', 'skip_threshold (80%)'),
    (r'<\s*20\s*%', 'inverse skip_threshold (20%)'),
    (r'<\s*50\s*%', 'low_confidence_block (50%)'),
    (r'>\s*95\s*%', 'tier1_confidence_cap (95%)'),
    (r'>\s*75\s*%', 'tier2_confidence_cap (75%)'),
    (r'P\(Architect\)\s*>\s*80', 'skip_threshold reference'),
    (r'P\(Pragmatist\)\s*>\s*80', 'skip_threshold reference'),
    (r'confidence\s*[<>]\s*50', 'low_confidence_block reference'),
    (r'\b40-60\b', 'uncertainty_range'),
    (r'\b40%?\s*-\s*60%?\b', 'uncertainty_range'),
]

# Patterns to IGNORE (these are OK in context)
IGNORE_PATTERNS = [
    r'config.*threshold',  # References to config files
    r'decision-thresholds',  # References to the threshold file
    r'see\s+config',  # Explicit config references
    r'from\s+config',  # Loading from config
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

**Generated**: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}

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
If P(Architect) exceeds skip_threshold (see config/decision-thresholds.json), skip to adversarial
```

This ensures all agents use consistent, centrally-managed thresholds.

---

## Quick Reference Values

For copy-paste into agent prompts:

```
skip_to_adversarial.threshold = {wd['skip_to_adversarial']['threshold']}%
low_confidence_block.threshold = {wd['low_confidence_block']['threshold']}%
uncertainty_range = {wd['uncertainty_range']['lower']}-{wd['uncertainty_range']['upper']}%
confidence_caps.tier1 = {caps['tier1_only']}%
confidence_caps.tier2 = {caps['tier2_only']}%
confidence_caps.tier3 = {caps['tier3_only']}%
confidence_caps.tier4 = {caps['tier4_inference_only']}%
extreme_lr_bounds = ({wd['extreme_lr_flag']['lower']}, {wd['extreme_lr_flag']['upper']})
```

---

## Source Files

- **Thresholds**: `config/decision-thresholds.json`
- **LR Tables**: `config/bayesian-lr-tables.json`
- **Taxonomy**: `config/classification-taxonomy.json`
- **Bank Manifest**: `config/bank-manifest.json`

---

*Auto-generated by `tools/inject_agent_config.py`*
"""
    return content


def should_ignore_match(line: str) -> bool:
    """Check if a line should be ignored (contains config reference)."""
    for pattern in IGNORE_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False


def check_prompts_for_hardcoded() -> list:
    """Check agent prompts for potentially hardcoded threshold values."""
    issues = []

    if not AGENT_PROMPTS_DIR.exists():
        print(f"Warning: Agent prompts directory not found: {AGENT_PROMPTS_DIR}")
        return issues

    for prompt_file in AGENT_PROMPTS_DIR.glob("*.md"):
        content = prompt_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        file_issues = []

        for line_num, line in enumerate(lines, 1):
            # Skip lines that reference config
            if should_ignore_match(line):
                continue

            for pattern, description in HARDCODED_PATTERNS:
                matches = list(re.finditer(pattern, line, re.IGNORECASE))
                for match in matches:
                    # Double-check it's not in a config reference context
                    context_start = max(0, match.start() - 50)
                    context = line[context_start:match.end() + 50]

                    if not should_ignore_match(context):
                        file_issues.append({
                            'line': line_num,
                            'pattern': description,
                            'match': match.group(),
                            'context': line.strip()[:100]
                        })

        if file_issues:
            issues.append({
                'file': prompt_file.name,
                'path': str(prompt_file),
                'issues': file_issues
            })

    return issues


def main():
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    if '--check-prompts' in sys.argv:
        print("Checking agent prompts for hardcoded thresholds...\n")
        issues = check_prompts_for_hardcoded()

        if not issues:
            print("[OK] No hardcoded thresholds found!")
            return 0
        else:
            total_issues = sum(len(f['issues']) for f in issues)
            print(f"Found {total_issues} potential hardcoded values in {len(issues)} files:\n")

            for file_info in issues:
                print(f"  {file_info['file']}:")
                for issue in file_info['issues']:
                    print(f"    Line {issue['line']}: {issue['pattern']}")
                    print(f"      Match: '{issue['match']}'")
                    print(f"      Context: {issue['context'][:80]}...")
                print()

            print("=" * 60)
            print("Consider replacing these with references to:")
            print("  config/agent-config-reference.md")
            print("  config/decision-thresholds.json")
            print("=" * 60)
            return 1

    # Generate reference file
    print("Generating agent-config-reference.md...")
    content = generate_reference_file()

    output_path = CONFIG_DIR / "agent-config-reference.md"
    output_path.write_text(content, encoding='utf-8')

    print(f"[OK] Generated: {output_path}")
    print(f"\nFile contains current threshold values from decision-thresholds.json")
    print("\nNext steps:")
    print("1. Run: python tools/inject_agent_config.py --check-prompts")
    print("2. Update agent prompts to reference config files instead of hardcoding")
    return 0


if __name__ == "__main__":
    sys.exit(main())
