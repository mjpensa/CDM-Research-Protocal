# CDM Research Protocol - Remediation Plan v2

## Overview

This plan addresses **16 issues** across 4 layers of the CDM Research Protocol codebase. Issues range from documentation cleanup to critical workflow enforcement gaps.

**Estimated Total Effort**: 10-12 hours
**Execution Strategy**: Layer-by-layer with verification gates

---

## Issue Summary

| ID | Issue | Layer | Complexity | Status |
|----|-------|-------|------------|--------|
| 1 | REDUNDANT-DOCS-1 | 0 | N/A | ✓ No action needed |
| 2 | REDUNDANT-DOCS-2 | 0 | M | Pending |
| 3 | MISSING-FILE | 0 | S | Pending |
| 4 | CONFIG-DRIFT | 0 | S | Pending |
| 5 | SCHEMA-VARIANTS | 1 | S | Pending |
| 6 | TIER4-GAP | 1 | S | Pending |
| 7 | OBSERVABLE-IMPL | 1 | N/A | ✓ Already complete |
| 8 | CLAIM-VALIDATION | 1 | S | Pending |
| 9 | ANCHOR-VALIDATION | 2 | M | Pending |
| 10 | CONTRADICTION-DETECTION | 2 | M | Pending |
| 11 | CROSS-BANK-WIRE | 2 | S | Pending |
| 12 | CHECKPOINT-PERSIST | 2 | S | Pending |
| 13 | BLOCK-ENFORCEMENT | 3 | S | Pending |
| 14 | PROVENANCE-VERIFY | 3 | M | Pending |
| 15 | TRIANGULATION-ENFORCE | 3 | M | Pending |
| 16 | CONFIG-INJECTION | 3 | M | Pending |

---

## Layer 0: Foundation (No Dependencies)

These can be done in parallel. Must complete before Layer 1.

### Issue 2: REDUNDANT-DOCS-2 - Consolidate Workflow Docs [M]

**Problem**: Three overlapping workflow documents create maintenance burden and confusion.

**Files to consolidate**:
| Current File | Lines | Action |
|--------------|-------|--------|
| `orchestrate-research.md` | 615 | Primary content → `docs/workflow.md` |
| `HYBRID-WORKFLOW-GUIDE.md` | 311 | Move → `docs/hybrid-workflow.md` |
| `EXECUTION-CHECKLIST.md` | 222 | Move → `docs/execution-checklist.md` |

**Implementation**:
1. Create `docs/` directory
2. Create `docs/workflow.md` with content from `orchestrate-research.md`
3. Move other files to `docs/` with cleaner names
4. Update all internal references
5. Delete original files

**Verification**: All links work, no broken references

---

### Issue 3: MISSING-FILE - Fix master_orchestrator.md Reference [S]

**Problem**: `CLAUDE.md` line 4 references non-existent file.

**File**: `CLAUDE.md`

**Current** (line 4):
```markdown
**Read During**: Pre-Flight (Step 1) of master_orchestrator.md
```

**Fix**:
```markdown
**Read During**: Pre-Flight (Step 1) of docs/workflow.md
```

---

### Issue 4: CONFIG-DRIFT - Consolidate Thresholds [S]

**Problem**: Threshold values duplicated in 3 places, risk of drift.

**File**: `CLAUDE.md` Section 7

**Current**: Hardcodes values (95%, 75%, 50%, 35%)

**Fix**: Replace with reference:
```markdown
## 7. Confidence Maxima by Evidence Tier

**Authoritative source**: `config/decision-thresholds.json` → `confidence_caps`

| Highest Tier Present | Maximum Confidence |
|---------------------|-------------------|
| Tier 1 evidence | `confidence_caps.tier1_only` |
| Tier 2 evidence only | `confidence_caps.tier2_only` |
| Tier 3 evidence only | `confidence_caps.tier3_only` |
| Inference only | `confidence_caps.tier4_inference_only` |
```

---

## Layer 1: Schema Alignment (Depends on Layer 0)

### Issue 5: SCHEMA-VARIANTS - Add Missing Classification Variants [S]

**Problem**: `evidence-schema.json` missing OBSERVER variants that appear in actual outputs.

**File**: `templates/evidence-schema.json`

**Current** (lines 82-93):
```json
"valid_sub_classifications": {
  "ARCHITECT": ["Native", "Leader", "Follower"],
  "PRAGMATIST": ["Vendor-Dependent", "Integration-Constrained", "Regulatory-Driven", "Network-Accelerant"],
  "UNKNOWN": ["Insufficient-Evidence", "Conflicting-Evidence"]
}
```

**Fix**:
```json
"valid_sub_classifications": {
  "ARCHITECT": ["Native", "Leader", "Follower"],
  "PRAGMATIST": ["Vendor-Dependent", "Integration-Constrained", "Regulatory-Driven", "Network-Accelerant"],
  "OBSERVER": ["Active-Watcher", "Passive"],
  "UNKNOWN": ["Insufficient-Evidence", "Conflicting-Evidence"]
}
```

---

### Issue 6: TIER4-GAP - Clarify Tier 4 Documentation [S]

**Problem**: Tier 4 documented but no workflow stage exists (by design, but unclear).

**File**: `CLAUDE.md` Section 2

**Add clarification**:
```markdown
### Tier 4: Contextual Inference (Lowest Authority)
- Business model analysis without direct CDM evidence
- Regulatory pressure inference ("EMIR Refit deadline approaching...")
- Peer behavior extrapolation ("Other European banks are adopting...")
- Informative absence (exhaustive search yielded no evidence)
- No direct source URL required (inference-based)
- **Note**: Tier 4 is applied during synthesis stage, not as a separate evidence-gathering stage
- **Maximum Confidence**: 35%
```

---

### Issue 8: CLAIM-VALIDATION - Add Enum Validation [S]

**Problem**: `process_evidence.py` doesn't validate claim_type values against schema.

**File**: `tools/process_evidence.py`

**Add** (after imports):
```python
from config_loader import get_valid_claim_types

def validate_claim_types(items: list) -> list:
    """Validate claim_type enum values against schema."""
    valid_types = get_valid_claim_types()
    warnings = []
    for item in items:
        claim_type = item.get('claim_type')
        if claim_type and claim_type not in valid_types:
            warnings.append(
                f"Invalid claim_type '{claim_type}' for {item.get('id')}. "
                f"Valid: {', '.join(valid_types)}"
            )
    return warnings
```

**Integrate** into `process_bank_evidence()`:
```python
# After loading data:
claim_warnings = validate_claim_types(data.get('evidence_items', []))
for warning in claim_warnings:
    logger.warning(warning)
```

---

## Layer 2: Tool Implementation (Depends on Layer 1)

### Issue 9: ANCHOR-VALIDATION - Implement Anchor Point Checks [M]

**Problem**: Anchor points defined but never enforced - can classify BNP Paribas as PRAGMATIST.

**File**: `tools/orchestrate.py`

**Add methods to Orchestrator class**:

```python
def _load_anchor_points(self) -> dict:
    """Load anchor points from config."""
    anchor_path = Path(__file__).parent.parent / "config" / "anchor-points.json"
    if anchor_path.exists():
        try:
            return json.loads(anchor_path.read_text(encoding='utf-8'))
        except Exception:
            return {}
    return {}

def check_anchor_violation(self) -> tuple[bool, str]:
    """Check if current classification violates anchor points."""
    anchors = self._load_anchor_points()
    bank_id = self.state.bank_id.lower().replace('-', '_')
    classification = self.state.classification
    sub_class = self.state.sub_classification

    # Check production banks (must be ARCHITECT-Native)
    for prod_bank in anchors.get('production_banks', {}).get('banks', []):
        if prod_bank.get('id', '').lower().replace('-', '_') == bank_id:
            if classification != 'ARCHITECT' or sub_class != 'Native':
                return True, (
                    f"ANCHOR VIOLATION: {self.state.bank_id} is confirmed in production "
                    f"but classified as {classification}/{sub_class}. "
                    f"Must be ARCHITECT/Native."
                )

    # Check confirmed contributors (must be ARCHITECT)
    for contrib in anchors.get('confirmed_contributors', {}).get('banks', []):
        if contrib.get('id', '').lower().replace('-', '_') == bank_id:
            if classification != 'ARCHITECT':
                return True, (
                    f"ANCHOR WARNING: {self.state.bank_id} is confirmed contributor "
                    f"but classified as {classification}. Should be ARCHITECT."
                )

    return False, ""
```

**Integrate into `should_block()`** (around line 295):
```python
# Check anchor point violations
if self.state.classification:
    violation, msg = self.check_anchor_violation()
    if violation:
        return True, msg, "anchor_point_violation"
```

**Test case**: Set BNP Paribas classification to PRAGMATIST → should BLOCK

---

### Issue 10: CONTRADICTION-DETECTION - Enhance Trust Audit [M]

**Problem**: Basic contradiction detection exists but doesn't catch tier conflicts.

**File**: `tools/trust_audit.py`

**Enhance `detect_contradictions()`** (around line 279):

```python
def detect_contradictions(items: list[dict]) -> list[dict]:
    """Detect contradictions in evidence items."""
    contradictions = []

    # Existing: Timeline contradictions, duplicate URLs...

    # NEW: Tier conflict detection
    tier1_items = [i for i in items if i.get('tier') == 1]
    tier2_items = [i for i in items if i.get('tier') == 2]

    # Check if Tier 1 and Tier 2 support opposite hypotheses
    tier1_supports = set()
    tier2_supports = set()

    for item in tier1_items:
        if 'production' in item.get('claim', '').lower():
            tier1_supports.add('ARCHITECT')
        if 'no evidence' in item.get('claim', '').lower():
            tier1_supports.add('PRAGMATIST')

    for item in tier2_items:
        if 'production' in item.get('claim', '').lower():
            tier2_supports.add('ARCHITECT')
        if 'no evidence' in item.get('claim', '').lower():
            tier2_supports.add('PRAGMATIST')

    if 'ARCHITECT' in tier1_supports and 'PRAGMATIST' in tier2_supports:
        contradictions.append({
            "type": "tier_conflict",
            "description": "Tier 1 evidence supports ARCHITECT but Tier 2 supports PRAGMATIST",
            "resolution": "unresolved",
            "severity": "high"
        })

    return contradictions
```

---

### Issue 11: CROSS-BANK-WIRE - Auto-trigger Validator [S]

**Problem**: Cross-bank validator exists but never called automatically.

**File**: `tools/run_pipeline.py`

**Add to `run_batch()`** (after line 440, after summary table):

```python
# Cross-bank validation
logger.info("\n" + "=" * 70)
logger.info("CROSS-BANK VALIDATION")
logger.info("=" * 70)

try:
    from cross_bank_validator import run_checks
    xbank_results = run_checks(str(directory))

    if xbank_results.get('passed', True):
        logger.info("Cross-bank validation: PASSED")
    else:
        logger.warning("Cross-bank validation: ISSUES DETECTED")
        for issue in xbank_results.get('critical', [])[:5]:
            logger.error(f"  CRITICAL: {issue.get('issue', 'Unknown')}")
        for issue in xbank_results.get('warnings', [])[:5]:
            logger.warning(f"  WARNING: {issue.get('issue', 'Unknown')}")

except ImportError:
    logger.warning("Cross-bank validator not available")
except Exception as e:
    logger.error(f"Cross-bank validation failed: {e}")
```

---

### Issue 12: CHECKPOINT-PERSIST - Central Checkpoint Log [S]

**Problem**: Checkpoint decisions not logged centrally for audit.

**File**: `tools/orchestrate.py`

**Add method to Orchestrator class**:

```python
def log_checkpoint(self, checkpoint_id: str, action: str, reason: str = None):
    """Log checkpoint decision to central log file."""
    log_path = self.bank_dir.parent.parent / "state" / "checkpoint-log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    existing = []
    if log_path.exists():
        try:
            existing = json.loads(log_path.read_text(encoding='utf-8'))
        except Exception:
            existing = []

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "bank_id": self.state.bank_id,
        "checkpoint_id": checkpoint_id,
        "action": action,  # "BLOCK", "AUTO_PROCEED", "APPROVED"
        "reason": reason,
        "stage": self.state.current_stage,
        "probability": self.state.probability_architect
    }
    existing.append(entry)

    log_path.write_text(json.dumps(existing, indent=2), encoding='utf-8')
    logger.debug(f"Logged checkpoint: {checkpoint_id} -> {action}")
```

**Call from**:
- `advance()` when blocking: `self.log_checkpoint(checkpoint_id, "BLOCK", reason)`
- `approve_checkpoint()`: `self.log_checkpoint(checkpoint_id, "APPROVED")`

---

## Layer 3: Workflow Enforcement (Depends on Layer 2)

### Issue 13: BLOCK-ENFORCEMENT - Strengthen Block Logic [S]

**Problem**: `should_block()` returns decision but callers may not respect it.

**File**: `tools/orchestrate.py`

**Enhance `should_block()`** to save state immediately:

```python
def should_block(self) -> tuple[bool, str, str]:
    """Check if current checkpoint requires human approval."""
    current = self.get_current_stage()

    # ... existing checks ...

    # If blocking, persist state immediately
    if should_block:
        if checkpoint_id not in self.state.checkpoints_pending:
            self.state.checkpoints_pending.append(checkpoint_id)
        self.log_checkpoint(checkpoint_id, "BLOCK", reason)
        self.state.save(self.state_path)

    return should_block, reason, checkpoint_id
```

**Add convenience method**:
```python
def is_blocked(self) -> bool:
    """Check if workflow is currently blocked awaiting approval."""
    blocked, _, _ = self.should_block()
    return blocked
```

---

### Issue 14: PROVENANCE-VERIFY - Detect File Tampering [M]

**Problem**: Stage hashes computed but never verified - can't detect if output files were modified.

**File**: `tools/orchestrate.py`

**Add to WorkflowState class**:

```python
def verify_provenance(self, bank_dir: Path) -> list[str]:
    """
    Verify all recorded stage hashes match current files.
    Returns list of stages with drift detected.
    """
    drift = []
    for stage, record in self.provenance.items():
        expected_hash = record.get('hash')
        if not expected_hash:
            continue

        current_hash = compute_stage_hash(bank_dir, stage)
        if current_hash != expected_hash:
            drift.append(
                f"{stage}: expected {expected_hash[:8]}..., "
                f"got {current_hash[:8]}... (file modified)"
            )

    return drift
```

**Call from `_load_or_init_state()`**:
```python
def _load_or_init_state(self) -> WorkflowState:
    if self.state_path.exists():
        try:
            state = WorkflowState.load(self.state_path)

            # Verify provenance integrity
            drift = state.verify_provenance(self.bank_dir)
            if drift:
                logger.warning("PROVENANCE DRIFT DETECTED:")
                for d in drift:
                    logger.warning(f"  {d}")
                # Optionally add to checkpoints_pending

            return state
        except Exception as e:
            logger.warning(f"Failed to load state: {e}")

    # ... rest of method
```

---

### Issue 15: TRIANGULATION-ENFORCE - Block Single-Source Claims [M]

**Problem**: Single-source claims flagged but don't block progression.

**Files**:
- `tools/orchestrate.py`
- `tools/trust_audit.py`
- `config/checkpoint-rules.json`

**In `trust_audit.py`**, after detecting single-source (around line 699):
```python
if source_diversity < 0.3:
    flags.append("SINGLE_SOURCE_CLAIM")
    # Signal to orchestrator
    if 'checkpoints_pending' not in data:
        data['checkpoints_pending'] = []
    if 'single_source' not in data['checkpoints_pending']:
        data['checkpoints_pending'].append('single_source')
```

**In `orchestrate.py` `should_block()`**:
```python
# Check for single-source triangulation requirement
if "single_source" in self.state.checkpoints_pending:
    return True, "Single-source claim requires corroboration (triangulation)", "triangulation"
```

**In `checkpoint-rules.json`**, add:
```json
{
  "checkpoint_id": "single_source_triangulation",
  "checkpoint_name": "Single Source - Triangulation Required",
  "action": "BLOCK",
  "condition": "source_diversity < 0.3",
  "rationale": "High-confidence claims require corroboration from multiple independent sources"
}
```

---

### Issue 16: CONFIG-INJECTION - Template System for Prompts [M]

**Problem**: Agent prompts hardcode threshold values instead of reading from config.

**Create new file**: `tools/prompt_renderer.py`

```python
"""
CDM Research Protocol - Prompt Template Renderer

Injects configuration values into agent prompts using {{config.X}} placeholders.
"""

from pathlib import Path
from config_loader import (
    get_skip_threshold,
    get_low_confidence_block_threshold,
    get_confidence_caps,
    get_extreme_lr_bounds
)


def get_replacements() -> dict:
    """Build replacement dictionary from config."""
    caps = get_confidence_caps()
    lr_bounds = get_extreme_lr_bounds()

    return {
        '{{config.skip_threshold}}': str(get_skip_threshold()),
        '{{config.low_confidence_block}}': str(get_low_confidence_block_threshold()),
        '{{config.tier1_cap}}': str(caps.get(1, 95)),
        '{{config.tier2_cap}}': str(caps.get(2, 75)),
        '{{config.tier3_cap}}': str(caps.get(3, 50)),
        '{{config.tier4_cap}}': str(caps.get(4, 35)),
        '{{config.extreme_lr_lower}}': str(lr_bounds[0]),
        '{{config.extreme_lr_upper}}': str(lr_bounds[1]),
    }


def render_prompt(template_path: Path) -> str:
    """
    Render a prompt template with injected config values.

    Args:
        template_path: Path to .md template file

    Returns:
        Rendered content with placeholders replaced
    """
    template = template_path.read_text(encoding='utf-8')

    for placeholder, value in get_replacements().items():
        template = template.replace(placeholder, value)

    # Warn about unreplaced placeholders
    import re
    remaining = re.findall(r'\{\{config\.[^}]+\}\}', template)
    if remaining:
        import logging
        logging.warning(f"Unreplaced placeholders: {remaining}")

    return template


def render_all_prompts(output_dir: Path = None):
    """Render all agent prompts to output directory."""
    prompts_dir = Path(__file__).parent.parent / "config" / "agent-prompts"
    output_dir = output_dir or prompts_dir.parent / "rendered-prompts"
    output_dir.mkdir(exist_ok=True)

    for prompt_file in prompts_dir.glob("*.md"):
        rendered = render_prompt(prompt_file)
        (output_dir / prompt_file.name).write_text(rendered, encoding='utf-8')
        print(f"Rendered: {prompt_file.name}")


if __name__ == "__main__":
    render_all_prompts()
```

**Update agent prompts** to use placeholders, e.g. in `reasoning-gate.md`:
```markdown
# Before
If P(Architect) > 80% OR P(Architect) < 20%, skip to adversarial

# After
If P(Architect) > {{config.skip_threshold}}% OR P(Architect) < {{config.skip_threshold}}%, skip to adversarial
```

---

## Execution Order

```
PHASE 1: Foundation (Layer 0) ─────────────────────────────────
│
├─► Issue 2: Consolidate workflow docs [M]
├─► Issue 3: Fix CLAUDE.md reference [S]
└─► Issue 4: Consolidate thresholds [S]
    │
    ▼
PHASE 2: Schema (Layer 1) ─────────────────────────────────────
│
├─► Issue 5: Add schema variants [S]
├─► Issue 6: Clarify Tier 4 docs [S]
└─► Issue 8: Add claim validation [S]
    │
    ▼
PHASE 3: Tools (Layer 2) ──────────────────────────────────────
│
├─► Issue 12: Checkpoint persist [S] ← Do first (used by others)
├─► Issue 9: Anchor validation [M]
├─► Issue 10: Contradiction detection [M]
└─► Issue 11: Cross-bank wiring [S]
    │
    ▼
PHASE 4: Enforcement (Layer 3) ────────────────────────────────
│
├─► Issue 13: Block enforcement [S]
├─► Issue 14: Provenance verify [M]
├─► Issue 15: Triangulation enforce [M]
└─► Issue 16: Config injection [M]
    │
    ▼
PHASE 5: Validation ───────────────────────────────────────────
│
├─► Run `python -m py_compile tools/*.py`
├─► Run pipeline on test bank
├─► Verify BLOCK conditions trigger
├─► Run cross-bank validation
└─► Check no regressions
```

---

## Critical Files Summary

| File | Changes | Issues |
|------|---------|--------|
| `tools/orchestrate.py` | Add anchor validation, provenance verify, checkpoint logging, block enforcement | 9, 12, 13, 14, 15 |
| `tools/trust_audit.py` | Enhance contradiction detection, add triangulation signaling | 10, 15 |
| `tools/run_pipeline.py` | Wire cross-bank validator | 11 |
| `tools/process_evidence.py` | Add claim_type validation | 8 |
| `tools/prompt_renderer.py` | **NEW** - Config injection system | 16 |
| `CLAUDE.md` | Fix reference, consolidate thresholds, clarify Tier 4 | 3, 4, 6 |
| `templates/evidence-schema.json` | Add OBSERVER variants | 5 |
| `config/checkpoint-rules.json` | Add triangulation rule | 15 |

---

## Verification Checklist

After all fixes complete:

- [ ] All Python files compile: `python -m py_compile tools/*.py`
- [ ] Orchestrate status works: `python tools/orchestrate.py outputs/phase-1-european-tier1/barclays --status`
- [ ] Anchor violation blocks: Classify BNP as PRAGMATIST → BLOCKS
- [ ] Single-source blocks: Evidence from one URL → BLOCKS
- [ ] Provenance drift warns: Modify output file → warns on status
- [ ] Cross-bank auto-runs: `--batch` triggers validation
- [ ] Config injection works: No `{{config.X}}` in rendered prompts
- [ ] No regressions: Existing outputs still validate

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking existing outputs | Backup outputs/ before starting |
| Circular imports in tools | Keep config_loader pure (no tool imports) |
| Over-strict blocking | Add `--force` flag for edge case override |
| Agent prompt changes break workflow | Test prompts in isolation first |
| Missing config files | All loaders have try/except with sensible defaults |

---

*Plan Version: 2.0*
*Created: 2024-12-19*
*Issues: 16 total, 14 requiring implementation*
*Estimated Effort: 10-12 hours*
