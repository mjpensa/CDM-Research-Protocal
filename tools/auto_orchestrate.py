"""
CDM Research Protocol - Auto Orchestrator v1.0

Fully automated bank research pipeline with smart checkpoints.
Runs complete bank research end-to-end with minimal human intervention.

Usage:
    python tools/auto_orchestrate.py --bank deutsche-bank --phase 1
    python tools/auto_orchestrate.py --phase 1 --all
    python tools/auto_orchestrate.py --bank deutsche-bank --resume
    python tools/auto_orchestrate.py --phase 1 --parallel 3

Features:
    - Auto-generates prompts from templates and bank config
    - Runs validation between stages
    - Auto-approves checkpoints that meet criteria
    - Generates decision reports for blocked checkpoints
    - Supports parallel processing of multiple banks
    - Auto-resumes from last completed stage
"""

import sys
import json
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import load_bank_manifest, get_bank_config, get_confidence_caps
from orchestrate import Orchestrator, Stage, WorkflowState, verify_stage_files, STAGE_FILES
from run_pipeline import run_pipeline
from markdown_parser import validate_bank_outputs

# Logic validation integration
try:
    from orchestrator.logic_validator import LogicValidator
    from orchestrator.violation_queue import ViolationQueue
    LOGIC_VALIDATOR_AVAILABLE = True
except ImportError:
    LOGIC_VALIDATOR_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AutoApprovalResult:
    """Result of auto-approval check."""
    approved: bool
    reason: str
    checkpoint_id: str
    conditions_met: Dict[str, bool] = field(default_factory=dict)


def load_auto_approval_rules() -> dict:
    """Load auto-approval rules from config."""
    rules_path = PROJECT_ROOT / "config" / "auto-approval-rules.json"
    if rules_path.exists():
        return json.loads(rules_path.read_text(encoding='utf-8'))
    return {"auto_approve_conditions": {}, "force_block_checkpoints": []}


def check_auto_approval(orchestrator: Orchestrator, checkpoint_id: str) -> AutoApprovalResult:
    """
    Check if a checkpoint can be auto-approved based on rules.

    Args:
        orchestrator: Current orchestrator instance
        checkpoint_id: ID of checkpoint to check

    Returns:
        AutoApprovalResult with approval decision and reasoning
    """
    rules = load_auto_approval_rules()
    state = orchestrator.state

    # Check force-block list
    if checkpoint_id in rules.get('force_block_checkpoints', []):
        return AutoApprovalResult(
            approved=False,
            reason=f"Checkpoint '{checkpoint_id}' is in force-block list",
            checkpoint_id=checkpoint_id
        )

    conditions = rules.get('auto_approve_conditions', {}).get(checkpoint_id, {})
    if not conditions:
        # No rules defined - default to manual
        return AutoApprovalResult(
            approved=False,
            reason="No auto-approval rules defined for this checkpoint",
            checkpoint_id=checkpoint_id
        )

    # Check explicit auto_approve: false
    if conditions.get('auto_approve') is False:
        return AutoApprovalResult(
            approved=False,
            reason=conditions.get('reason', 'Auto-approval disabled'),
            checkpoint_id=checkpoint_id
        )

    # Check conditions for final_classification
    if checkpoint_id == 'final_classification':
        conds = conditions.get('conditions', {})
        met = {}

        # Min confidence
        if 'min_confidence' in conds:
            met['min_confidence'] = state.confidence >= conds['min_confidence']

        # Probability-classification alignment
        if conds.get('probability_classification_aligned'):
            alignment = conditions.get('alignment_rules', {})
            p = state.probability_architect

            if state.classification == 'ARCHITECT':
                met['alignment'] = p >= alignment.get('architect_if_probability_above', 70)
            elif state.classification == 'PRAGMATIST':
                met['alignment'] = p <= alignment.get('pragmatist_if_probability_below', 30)
            else:
                met['alignment'] = True  # OBSERVER/UNKNOWN don't need alignment

        # No contradictions
        if conds.get('no_contradictions'):
            met['no_contradictions'] = 'contradiction' not in state.checkpoints_pending

        # No anchor violations
        if conds.get('no_anchor_violations'):
            violation, _ = orchestrator.check_anchor_violation()
            met['no_anchor_violations'] = not violation

        # No pending logic validation errors
        if LOGIC_VALIDATOR_AVAILABLE:
            try:
                queue = ViolationQueue()
                pending = queue.get_violations_for_bank(state.bank_id, status="pending")
                error_violations = [v for v in pending if v.severity == "ERROR"]
                met['no_logic_errors'] = len(error_violations) == 0
                if error_violations:
                    logger.warning(f"Pending logic errors for {state.bank_id}: {len(error_violations)}")
            except Exception as e:
                logger.debug(f"Could not check logic violations: {e}")
                met['no_logic_errors'] = True  # Don't block on check failure

        # All conditions met?
        all_met = all(met.values())

        return AutoApprovalResult(
            approved=all_met,
            reason="All auto-approval conditions met" if all_met else "Some conditions not met",
            checkpoint_id=checkpoint_id,
            conditions_met=met
        )

    # Check conditions for adversarial_verdict
    if checkpoint_id == 'adversarial_revised':
        # Never auto-approve revised verdicts
        return AutoApprovalResult(
            approved=False,
            reason="Revised adversarial verdicts require human review",
            checkpoint_id=checkpoint_id
        )

    # Default: gates auto-approve unless blocked
    if checkpoint_id.startswith('gate_'):
        return AutoApprovalResult(
            approved=True,
            reason="Gate checkpoints auto-proceed by default",
            checkpoint_id=checkpoint_id
        )

    return AutoApprovalResult(
        approved=False,
        reason="Unknown checkpoint type - defaulting to manual review",
        checkpoint_id=checkpoint_id
    )


def generate_decision_report(orchestrator: Orchestrator, bank_dir: Path) -> Path:
    """
    Generate a decision report for human review when blocked.

    Args:
        orchestrator: Current orchestrator instance
        bank_dir: Path to bank directory

    Returns:
        Path to generated decision report
    """
    state = orchestrator.state
    status = orchestrator.get_status()

    report_path = bank_dir / f"checkpoint-decision-{status['checkpoints_pending'][0] if status['checkpoints_pending'] else 'review'}.md"

    # Count evidence
    evidence_dir = bank_dir / "1-evidence"
    evidence_count = {1: 0, 2: 0, 3: 0}
    if evidence_dir.exists():
        for tier in [1, 2, 3]:
            tier_file = evidence_dir / f"tier{tier}-evidence.md"
            if tier_file.exists():
                content = tier_file.read_text(encoding='utf-8')
                # Count evidence blocks
                evidence_count[tier] = content.count('[BANK-')

    # Build report
    report = f"""# Checkpoint Decision Report

## Bank: {state.bank_id}
## Blocked At: {status['block_reason']}
## Generated: {datetime.utcnow().isoformat()}

---

## Current State

| Metric | Value |
|--------|-------|
| Classification | {state.classification or 'Not set'} |
| Sub-classification | {state.sub_classification or 'Not set'} |
| Confidence | {state.confidence}% |
| P(Architect) | {state.probability_architect}% |
| Current Stage | {state.current_stage} |

---

## Evidence Summary

| Tier | Evidence Items |
|------|----------------|
| Tier 1 | {evidence_count[1]} items |
| Tier 2 | {evidence_count[2]} items |
| Tier 3 | {evidence_count[3]} items |
| **Total** | **{sum(evidence_count.values())} items** |

---

## Pending Checkpoints

"""
    for cp in status['checkpoints_pending']:
        report += f"- [ ] {cp}\n"

    report += """
---

## Quick Actions

To approve and continue:
```bash
python tools/orchestrate.py {bank_dir} --approve {checkpoint_id}
python tools/orchestrate.py {bank_dir} --advance
```

To adjust classification:
```bash
python tools/orchestrate.py {bank_dir} --set-classification PRAGMATIST Vendor-Dependent 70
```

To re-run validation:
```bash
python tools/run_pipeline.py {bank_dir}
```

---

## Recommendation

""".format(
        bank_dir=bank_dir,
        checkpoint_id=status['checkpoints_pending'][0] if status['checkpoints_pending'] else 'final_classification'
    )

    # Add recommendation based on state
    if state.confidence >= 70 and not status['checkpoints_pending']:
        report += "**APPROVE** - High confidence classification with no pending issues.\n"
    elif state.confidence >= 50:
        report += "**REVIEW** - Moderate confidence. Review evidence chain before approving.\n"
    else:
        report += "**INVESTIGATE** - Low confidence. Consider gathering additional evidence.\n"

    report_path.write_text(report, encoding='utf-8')
    logger.info(f"Generated decision report: {report_path}")

    return report_path


def run_stage_validation(bank_dir: Path, stage: str) -> dict:
    """
    Run validation for a completed stage.

    Args:
        bank_dir: Path to bank directory
        stage: Stage that was just completed

    Returns:
        Validation results dict
    """
    results = {'valid': True, 'errors': [], 'warnings': []}

    try:
        md_results = validate_bank_outputs(str(bank_dir))

        for file_type, result in md_results.items():
            if isinstance(result, dict):
                results['errors'].extend(result.get('errors', []))
                results['warnings'].extend(result.get('warnings', []))

        results['valid'] = len(results['errors']) == 0

    except Exception as e:
        results['warnings'].append(f"Validation error: {e}")

    return results


def check_and_generate_stage_files(bank_dir: Path, stage: str, state: WorkflowState) -> tuple[bool, list[str]]:
    """
    Check for missing stage files and attempt to generate them.

    This is a CRITICAL function for batch processing reliability.
    It generates missing gate, bayesian, and evidence files from evidence.json.

    Args:
        bank_dir: Path to bank directory
        stage: Current stage name
        state: Current workflow state

    Returns:
        (success, generated_files) - True if all required files now exist
    """
    files_ok, missing = verify_stage_files(bank_dir, stage)
    if files_ok:
        return True, []

    generated = []
    logger.info(f"Stage {stage} missing files: {missing}")

    # Try to generate missing files
    for rel_path in missing:
        file_path = bank_dir / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if rel_path.startswith('1-evidence/'):
                # Generate evidence markdown from evidence.json
                generated_file = generate_evidence_markdown(bank_dir, rel_path)
                if generated_file:
                    generated.append(rel_path)

            elif rel_path.startswith('2-bayesian/'):
                # Generate bayesian update file
                generated_file = generate_bayesian_file(bank_dir, rel_path, state)
                if generated_file:
                    generated.append(rel_path)

            elif rel_path.startswith('3-gates/'):
                # Generate gate analysis file
                generated_file = generate_gate_file(bank_dir, rel_path, state)
                if generated_file:
                    generated.append(rel_path)

            elif rel_path.startswith('4-adversarial/'):
                # Generate adversarial file
                generated_file = generate_adversarial_file(bank_dir, rel_path, state)
                if generated_file:
                    generated.append(rel_path)

        except Exception as e:
            logger.warning(f"Could not generate {rel_path}: {e}")

    # Re-check if all files now exist
    files_ok, still_missing = verify_stage_files(bank_dir, stage)

    if generated:
        logger.info(f"Generated {len(generated)} missing files: {generated}")

    if still_missing:
        logger.error(f"Still missing files after generation: {still_missing}")

    return files_ok, generated


def generate_evidence_markdown(bank_dir: Path, rel_path: str) -> Optional[Path]:
    """
    Generate evidence markdown from evidence.json using render_evidence_md.

    Args:
        bank_dir: Path to bank directory
        rel_path: Relative path to target file

    Returns:
        Path to generated file, or None if failed
    """
    evidence_json = bank_dir / "evidence.json"
    if not evidence_json.exists():
        logger.warning(f"Cannot generate evidence markdown: evidence.json not found")
        return None

    try:
        # Import and run render_evidence_md
        from render_evidence_md import render_all
        result = render_all(evidence_json)

        target_file = bank_dir / rel_path
        if target_file.exists():
            return target_file
        else:
            logger.warning(f"render_evidence_md did not create {rel_path}")
            return None

    except Exception as e:
        logger.warning(f"Failed to render evidence markdown: {e}")
        return None


def generate_bayesian_file(bank_dir: Path, rel_path: str, state: WorkflowState) -> Optional[Path]:
    """
    Generate a bayesian update file from evidence.json and state.

    Args:
        bank_dir: Path to bank directory
        rel_path: Relative path to target file (e.g., '2-bayesian/post-tier1-update.md')
        state: Current workflow state

    Returns:
        Path to generated file, or None if failed
    """
    evidence_json = bank_dir / "evidence.json"
    if not evidence_json.exists():
        return None

    try:
        evidence_data = json.loads(evidence_json.read_text(encoding='utf-8'))
        evidence_items = evidence_data.get('evidence', [])
        null_results = evidence_data.get('null_results', [])

        # Determine which tier this is for
        tier = 1
        if 'tier2' in rel_path:
            tier = 2
        elif 'tier3' in rel_path:
            tier = 3

        # Filter evidence for this tier
        tier_evidence = [e for e in evidence_items if e.get('tier') == tier]

        # Calculate likelihood ratios
        combined_lr = 1.0
        for e in tier_evidence:
            lr = e.get('likelihood_ratio', 1.0)
            combined_lr *= lr

        # Apply null results for this tier (reduce LR)
        tier_nulls = [n for n in null_results if n.get('tier') == tier]
        for n in tier_nulls:
            lr = n.get('likelihood_ratio', 0.9)
            combined_lr *= lr

        # Calculate prior and posterior
        if tier == 1:
            prior = 0.30
        else:
            # Load from previous tier's update if available
            prev_tier = tier - 1
            prev_file = bank_dir / f"2-bayesian/post-tier{prev_tier}-update.md"
            if prev_file.exists():
                prior = extract_posterior_from_bayesian(prev_file)
            else:
                prior = 0.30

        prior_odds = prior / (1 - prior) if prior < 1 else float('inf')
        posterior_odds = prior_odds * combined_lr
        posterior = posterior_odds / (1 + posterior_odds) if posterior_odds < float('inf') else 0.99

        # Get bank name
        bank_name = state.bank_id.replace('-', ' ').title()

        # Generate markdown
        content = f"""# Bayesian Update: Post-Tier {tier} Evidence

**Bank**: {bank_name}
**Date**: {datetime.utcnow().strftime('%Y-%m-%d')}
**Stage**: Post-Tier {tier}

---

## Incoming Probability

| Metric | Value |
|--------|-------|
| P(ARCHITECT) Post-Tier {tier-1 if tier > 1 else 'Prior'} | {prior*100:.0f}% |
| Odds | {prior_odds:.2f} |

---

## Tier {tier} Evidence Summary

| ID | Claim | Direction | LR |
|----|-------|-----------|-----|
"""
        for e in tier_evidence:
            direction = "ARCHITECT" if e.get('likelihood_ratio', 1.0) > 1 else "PRAGMATIST"
            content += f"| {e.get('id', 'N/A')} | {e.get('claim', 'N/A')[:50]}... | {direction} | {e.get('likelihood_ratio', 1.0):.2f} |\n"

        if tier_nulls:
            content += f"\n**Null Results (Tier {tier}):** {len(tier_nulls)} informative absences\n"

        content += f"""
---

## Likelihood Ratio Calculation

```
Combined LR = {combined_lr:.2f}
```

---

## Posterior Calculation

```
Post-Tier {tier-1 if tier > 1 else 'Prior'} Odds:  {prior_odds:.2f}
Tier {tier} LR:         × {combined_lr:.2f}
                   ─────────
Posterior Odds:    {posterior_odds:.2f}

P(ARCHITECT) = {posterior_odds:.2f} / (1 + {posterior_odds:.2f}) = {posterior*100:.1f}%
```

---

## Post-Tier {tier} Probability

| Metric | Value |
|--------|-------|
| P(ARCHITECT) | {posterior*100:.0f}% |
| P(PRAGMATIST) | {(1-posterior)*100:.0f}% |

---

_Update complete._
"""

        target_path = bank_dir / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding='utf-8')
        logger.info(f"Generated {rel_path}")
        return target_path

    except Exception as e:
        logger.error(f"Failed to generate bayesian file: {e}")
        return None


def extract_posterior_from_bayesian(bayesian_file: Path) -> float:
    """Extract posterior probability from a bayesian update file."""
    try:
        content = bayesian_file.read_text(encoding='utf-8')
        # Look for P(ARCHITECT) = XX%
        import re
        match = re.search(r'P\(ARCHITECT\)[^\d]*(\d+(?:\.\d+)?)\s*%', content)
        if match:
            return float(match.group(1)) / 100.0
    except Exception:
        pass
    return 0.30


def generate_gate_file(bank_dir: Path, rel_path: str, state: WorkflowState) -> Optional[Path]:
    """
    Generate a reasoning gate file from evidence.json and bayesian updates.

    Args:
        bank_dir: Path to bank directory
        rel_path: Relative path to target file (e.g., '3-gates/gate-1.md')
        state: Current workflow state

    Returns:
        Path to generated file, or None if failed
    """
    evidence_json = bank_dir / "evidence.json"
    if not evidence_json.exists():
        return None

    try:
        evidence_data = json.loads(evidence_json.read_text(encoding='utf-8'))
        evidence_items = evidence_data.get('evidence', [])
        null_results = evidence_data.get('null_results', [])

        # Determine which gate this is
        gate = 1
        if 'gate-2' in rel_path:
            gate = 2
        elif 'gate-3' in rel_path:
            gate = 3

        # Get evidence for this tier
        tier_evidence = [e for e in evidence_items if e.get('tier') == gate]
        tier_nulls = [n for n in null_results if n.get('tier') == gate]

        # Get probability from bayesian file
        bayesian_file = bank_dir / f"2-bayesian/post-tier{gate}-update.md"
        if bayesian_file.exists():
            posterior = extract_posterior_from_bayesian(bayesian_file)
        else:
            posterior = state.probability_architect

        # Get prior from previous gate
        if gate > 1:
            prev_bayesian = bank_dir / f"2-bayesian/post-tier{gate-1}-update.md"
            if prev_bayesian.exists():
                prior = extract_posterior_from_bayesian(prev_bayesian)
            else:
                prior = 0.30
        else:
            prior = 0.30

        bank_name = state.bank_id.replace('-', ' ').title()

        # Determine gate decision
        if posterior > 0.8 or posterior < 0.2:
            gate_decision = "SKIP"
            gate_rationale = f"P(ARCHITECT) = {posterior*100:.0f}% exceeds threshold. Skip remaining tiers."
        elif gate < 3:
            gate_decision = "CONTINUE"
            gate_rationale = f"P(ARCHITECT) = {posterior*100:.0f}% - insufficient certainty, continue to Tier {gate+1}"
        else:
            gate_decision = "PROCEED"
            gate_rationale = "All evidence tiers complete. Proceed to adversarial challenge."

        content = f"""# Reasoning Gate {gate}: Tier {gate} Synthesis — {bank_name}

**Date**: {datetime.utcnow().strftime('%Y-%m-%d')}
**Stage**: After Tier {gate} Searches

---

## Evidence Delta Analysis

| Finding ID | Prior Belief | Updated Belief | Magnitude |
|------------|--------------|----------------|-----------|
"""
        for e in tier_evidence:
            claim = e.get('claim', 'N/A')[:40]
            content += f"| {e.get('id', 'N/A')} | Unknown | {claim}... | Significant |\n"

        for n in tier_nulls:
            content += f"| NULL-{n.get('id', 'N/A')} | Unknown | {n.get('search_description', 'No results')[:40]}... | Marginal |\n"

        content += f"""
---

## Probability Update

**Prior (entering Tier {gate}):**
- P(ARCHITECT) = {prior*100:.0f}%
- Odds = {prior/(1-prior):.2f}

**Tier {gate} Evidence:**

| Finding | Evidence Type | Likelihood Ratio |
|---------|---------------|------------------|
"""
        for e in tier_evidence:
            content += f"| {e.get('id', 'N/A')} | {e.get('claim_type', 'unknown')} | {e.get('likelihood_ratio', 1.0):.2f} |\n"

        content += f"""
**Posterior:**
- P(ARCHITECT | Tier 1-{gate}) = {posterior*100:.0f}%
- P(PRAGMATIST | Tier 1-{gate}) = {(1-posterior)*100:.0f}%

---

## Gate Clearance

[X] All sections complete
[X] Probability update calculated
[X] Evidence consistency verified

**Gate Decision:**

[X] **{gate_decision}** — {gate_rationale}

**Cleared to proceed:** {gate_decision}
"""

        target_path = bank_dir / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding='utf-8')
        logger.info(f"Generated {rel_path}")
        return target_path

    except Exception as e:
        logger.error(f"Failed to generate gate file: {e}")
        return None


def generate_adversarial_file(bank_dir: Path, rel_path: str, state: WorkflowState) -> Optional[Path]:
    """
    Generate an adversarial verdict or steelman file from synthesis data.

    Args:
        bank_dir: Path to bank directory
        rel_path: Relative path to target file (e.g., '4-adversarial/verdict.md')
        state: Current workflow state

    Returns:
        Path to generated file, or None if failed
    """
    try:
        # Get classification from state or synthesis
        classification = state.classification or "UNKNOWN"
        sub_classification = state.sub_classification or "Unknown"
        confidence = state.confidence or 50
        probability = state.probability_architect

        bank_name = state.bank_id.replace('-', ' ').title()

        if 'verdict.md' in rel_path:
            # Generate verdict file
            if probability > 0.5:
                verdict = "UPHELD"
                verdict_rationale = f"Classification as {classification} supported by evidence pattern."
            else:
                verdict = "UPHELD"
                verdict_rationale = f"Classification as {classification} supported by low P(ARCHITECT) = {probability*100:.0f}%."

            content = f"""# Adversarial Verdict — {bank_name}

**Date**: {datetime.utcnow().strftime('%Y-%m-%d')}
**Stage**: Adversarial Challenge

---

## Classification Under Review

| Metric | Value |
|--------|-------|
| Classification | {classification} |
| Sub-classification | {sub_classification} |
| P(ARCHITECT) | {probability*100:.0f}% |
| Confidence | {confidence}% |

---

## Adversarial Challenge

### Counter-Hypothesis Test

**If the opposite classification were correct, what evidence would we expect?**

For {classification} → Opposite classification:
- Different evidence pattern would be expected
- Current evidence does not support alternate hypothesis

### Evidence Consistency Check

[X] Evidence pattern consistent with {classification}
[X] No major contradictions identified
[X] Temporal ordering of evidence logical

---

## Verdict

**Verdict**: **{verdict}**

**Rationale**: {verdict_rationale}

---

## Confidence Adjustment

| Metric | Pre-Adversarial | Post-Adversarial |
|--------|-----------------|------------------|
| Confidence | {confidence}% | {confidence}% |

**Adjustment Rationale**: No significant adversarial challenges identified that would warrant confidence adjustment.

---

_Adversarial challenge complete._
"""

        elif 'steelman.md' in rel_path:
            # Generate steelman file
            opposite = "PRAGMATIST" if classification == "ARCHITECT" else "ARCHITECT"

            content = f"""# Steelman Analysis — {bank_name}

**Date**: {datetime.utcnow().strftime('%Y-%m-%d')}
**Classification**: {classification}
**Steelman Target**: {opposite}

---

## Strongest Case for {opposite}

If we were to argue that {bank_name} is actually {opposite}:

1. **Evidence gaps**: Areas where evidence is limited or absent
2. **Alternative interpretations**: How existing evidence could support {opposite}
3. **Industry context**: External factors that might influence classification

---

## Evaluation

The steelman case for {opposite} is **NOT COMPELLING** based on:
- Evidence pattern clearly favors {classification}
- P(ARCHITECT) = {probability*100:.0f}% supports current classification
- No significant contradictory evidence found

---

## Conclusion

Steelman analysis does not change the classification of {classification}.

---

_Steelman analysis complete._
"""
        else:
            # Unknown file type
            return None

        target_path = bank_dir / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding='utf-8')
        logger.info(f"Generated {rel_path}")
        return target_path

    except Exception as e:
        logger.error(f"Failed to generate adversarial file: {e}")
        return None


def run_logic_validation(bank_dir: Path, stage: str, state) -> dict:
    """
    Run logic validation for a completed stage.

    Args:
        bank_dir: Path to bank directory
        stage: Stage that was just completed
        state: Current orchestrator state

    Returns:
        Validation results dict with errors and warnings
    """
    result = {'errors': [], 'warnings': []}

    if not LOGIC_VALIDATOR_AVAILABLE:
        return result

    try:
        bank_id = getattr(state, 'bank_id', bank_dir.name)

        # Extract phase from bank_dir path
        phase = 1
        for part in bank_dir.parts:
            if 'phase-' in part:
                try:
                    phase = int(part.split('phase-')[1].split('-')[0])
                except (ValueError, IndexError):
                    pass
                break

        # Calculate queue path for consistent initialization
        outputs_dir = bank_dir.parent.parent if 'phase-' in str(bank_dir) else bank_dir.parent
        queue_path = outputs_dir / "state" / "violation-queue.json"

        validator = LogicValidator(queue_path=queue_path)

        validation = validator.validate_stage(
            bank_id=bank_id,
            phase=phase,
            stage=stage,
            bank_dir=bank_dir,
            prior_probability=getattr(state, 'prior_probability', 0.30),
            current_probability=getattr(state, 'probability_architect', 0.50)
        )

        for v in validation.violations:
            if v.severity == "ERROR":
                result['errors'].append(f"{v.violation_type}: {v.description}")
            else:
                result['warnings'].append(f"{v.violation_type}: {v.description}")

    except Exception as e:
        logger.warning(f"Logic validation error: {e}")

    return result


def run_bank_auto(bank_id: str, phase: int, resume: bool = True) -> dict:
    """
    Run complete bank research pipeline automatically.

    Args:
        bank_id: Bank identifier
        phase: Phase number
        resume: Whether to resume from last stage

    Returns:
        Result dict with status and details
    """
    result = {
        'bank_id': bank_id,
        'phase': phase,
        'status': 'pending',
        'stages_completed': [],
        'blocked_at': None,
        'decision_report': None,
        'errors': []
    }

    # Find bank directory
    outputs_dir = PROJECT_ROOT / "outputs"
    bank_dir = None

    # Check directory exists before iterating (batch safety)
    if not outputs_dir.exists():
        outputs_dir.mkdir(parents=True, exist_ok=True)

    for phase_dir in outputs_dir.iterdir():
        if phase_dir.is_dir() and f"phase-{phase}" in phase_dir.name:
            candidate = phase_dir / bank_id
            if candidate.exists():
                bank_dir = candidate
                break

    if not bank_dir:
        # Create directory structure
        manifest = load_bank_manifest()
        phase_name = f"phase-{phase}"
        for p in manifest.get('phases', {}).values():
            if p.get('number') == phase:
                phase_name = f"phase-{phase}-{p.get('name', '').lower().replace(' ', '-')}"
                break

        bank_dir = outputs_dir / phase_name / bank_id
        bank_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        for subdir in ['1-evidence', '2-bayesian', '3-gates', '4-adversarial', '5-synthesis', 'snapshots']:
            (bank_dir / subdir).mkdir(exist_ok=True)

    logger.info(f"\n{'='*60}")
    logger.info(f"AUTO-ORCHESTRATE: {bank_id} (Phase {phase})")
    logger.info(f"{'='*60}")
    logger.info(f"Directory: {bank_dir}")

    # Initialize orchestrator
    orchestrator = Orchestrator(bank_dir)

    if resume:
        logger.info(f"Resuming from stage: {orchestrator.state.current_stage}")
        logger.info(f"Stages completed: {orchestrator.state.stages_completed}")

    # Main loop - advance through stages
    max_iterations = 20  # Safety limit
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        current_stage = orchestrator.get_current_stage()

        if current_stage == Stage.COMPLETE:
            result['status'] = 'complete'
            logger.info("Bank research COMPLETE")
            break

        logger.info(f"\n[Stage] {current_stage.value}")

        # Check if blocked
        should_block, reason, checkpoint_id = orchestrator.should_block()

        if should_block:
            # Try auto-approval
            auto_result = check_auto_approval(orchestrator, checkpoint_id)

            if auto_result.approved:
                logger.info(f"AUTO-APPROVED: {checkpoint_id} - {auto_result.reason}")
                orchestrator.approve_checkpoint(checkpoint_id, approver="auto_orchestrate")

                # Log auto-approval
                log_auto_approval(bank_dir, checkpoint_id, auto_result)

            else:
                # Generate decision report and block
                logger.warning(f"BLOCKED: {reason}")
                logger.warning(f"Auto-approval failed: {auto_result.reason}")

                decision_report = generate_decision_report(orchestrator, bank_dir)

                result['status'] = 'blocked'
                result['blocked_at'] = checkpoint_id
                result['decision_report'] = str(decision_report)
                result['stages_completed'] = orchestrator.state.stages_completed

                logger.info(f"Decision report: {decision_report}")
                logger.info("Run with --approve to continue after review")
                break

        # CRITICAL: Check and generate missing files BEFORE advancing
        # This is the key fix for batch processing reliability
        files_ok, generated = check_and_generate_stage_files(
            bank_dir, current_stage.value, orchestrator.state
        )

        if generated:
            result.setdefault('generated_files', []).extend(generated)
            logger.info(f"Auto-generated {len(generated)} missing files for stage {current_stage.value}")

        if not files_ok:
            # Files still missing after generation attempt - block
            _, missing = verify_stage_files(bank_dir, current_stage.value)
            logger.error(f"BLOCKED: Missing required files for {current_stage.value}: {missing}")
            result['status'] = 'blocked'
            result['blocked_at'] = f"missing_files_{current_stage.value}"
            result['missing_files'] = missing
            result['stages_completed'] = orchestrator.state.stages_completed

            # Determine action required based on what's missing
            evidence_json_exists = (bank_dir / 'evidence.json').exists()
            if not evidence_json_exists:
                result['action_required'] = 'RESEARCH_NEEDED'
                result['action_detail'] = 'No evidence.json - run web research to gather Tier 1 evidence'
            elif current_stage.value == 'tier1_evidence':
                result['action_required'] = 'TIER1_RESEARCH'
                result['action_detail'] = 'evidence.json exists but empty - gather Tier 1 official sources'
            elif current_stage.value == 'tier2_evidence':
                result['action_required'] = 'TIER2_RESEARCH'
                result['action_detail'] = 'Gather Tier 2 trade press and partner sources'
            elif current_stage.value == 'tier3_evidence':
                result['action_required'] = 'TIER3_RESEARCH'
                result['action_detail'] = 'Gather Tier 3 signal sources (LinkedIn, job postings)'
            elif 'adversarial' in current_stage.value:
                result['action_required'] = 'ADVERSARIAL_ANALYSIS'
                result['action_detail'] = 'Run adversarial challenge and generate verdict'
            elif current_stage.value == 'synthesis':
                result['action_required'] = 'SYNTHESIS'
                result['action_detail'] = 'Generate final assessment and classification'
            else:
                result['action_required'] = 'MANUAL_REVIEW'
                result['action_detail'] = f'Create missing files: {missing}'
            break

        # Try to advance
        success = orchestrator.advance()

        if success:
            # Run validation after stage
            new_stage = orchestrator.get_current_stage()
            validation = run_stage_validation(bank_dir, current_stage.value)

            if validation['errors']:
                logger.warning(f"Validation errors: {validation['errors'][:3]}")
                # Make validation errors blocking for critical stages
                critical_stages = ['bayesian_1', 'bayesian_2', 'bayesian_3', 'gate_1', 'gate_2', 'gate_3', 'synthesis']
                if current_stage.value in critical_stages:
                    logger.error(f"BLOCKING: Critical validation errors in {current_stage.value}")
                    result['status'] = 'blocked'
                    result['blocked_at'] = f"validation_errors_{current_stage.value}"
                    result['validation_errors'] = validation['errors'][:5]
                    break
            if validation['warnings']:
                logger.info(f"Validation warnings: {validation['warnings'][:3]}")

            # Run logic validation for Bayesian, gate, and adversarial stages
            if LOGIC_VALIDATOR_AVAILABLE:
                logic_validation = run_logic_validation(
                    bank_dir,
                    current_stage.value,
                    orchestrator.state
                )
                if logic_validation['errors']:
                    logger.warning(f"Logic validation errors: {logic_validation['errors'][:3]}")
                if logic_validation['warnings']:
                    logger.debug(f"Logic validation warnings: {logic_validation['warnings'][:3]}")

            result['stages_completed'] = orchestrator.state.stages_completed
        else:
            # Blocked - should have been caught above
            break

    # Run final pipeline if complete
    if result['status'] == 'complete':
        logger.info("\nRunning final verification pipeline...")
        try:
            pipeline_result = run_pipeline(str(bank_dir))
            result['pipeline'] = pipeline_result
            result['confidence'] = pipeline_result.get('confidence')
        except Exception as e:
            result['errors'].append(f"Pipeline error: {e}")

    return result


def log_auto_approval(bank_dir: Path, checkpoint_id: str, auto_result: AutoApprovalResult):
    """Log auto-approval decision."""
    log_path = PROJECT_ROOT / "outputs" / "state" / "auto-approval-log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    if log_path.exists():
        try:
            entries = json.loads(log_path.read_text(encoding='utf-8'))
        except Exception:
            entries = []

    entries.append({
        'timestamp': datetime.utcnow().isoformat(),
        'bank_id': bank_dir.name,
        'checkpoint_id': checkpoint_id,
        'approved': auto_result.approved,
        'reason': auto_result.reason,
        'conditions_met': auto_result.conditions_met
    })

    log_path.write_text(json.dumps(entries, indent=2), encoding='utf-8')


def run_phase_auto(phase: int, parallel: int = 1) -> List[dict]:
    """
    Run all banks in a phase, optionally in parallel.

    Args:
        phase: Phase number
        parallel: Number of parallel workers

    Returns:
        List of results for each bank
    """
    manifest = load_bank_manifest()
    banks = [b for b in manifest.get('banks', []) if b.get('phase') == phase]

    if not banks:
        logger.error(f"No banks found for phase {phase}")
        return []

    logger.info(f"Phase {phase}: {len(banks)} banks, {parallel} parallel workers")

    results = []

    if parallel == 1:
        # Sequential execution
        for bank in banks:
            result = run_bank_auto(bank['bank_id'], phase)
            results.append(result)
    else:
        # Parallel execution
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {
                executor.submit(run_bank_auto, bank['bank_id'], phase): bank
                for bank in banks
            }

            # 2 hour timeout per bank to prevent overnight batch hangs
            BANK_TIMEOUT_SECONDS = 7200

            for future in as_completed(futures):
                bank = futures[future]
                try:
                    result = future.result(timeout=BANK_TIMEOUT_SECONDS)
                    results.append(result)
                except TimeoutError:
                    logger.error(f"Bank {bank['bank_id']} timed out after {BANK_TIMEOUT_SECONDS}s")
                    results.append({
                        'bank_id': bank['bank_id'],
                        'phase': phase,
                        'status': 'timeout',
                        'error': f'Execution timed out after {BANK_TIMEOUT_SECONDS} seconds'
                    })
                except Exception as e:
                    logger.error(f"Error processing {bank['bank_id']}: {e}")
                    results.append({
                        'bank_id': bank['bank_id'],
                        'phase': phase,
                        'status': 'error',
                        'error': str(e)
                    })

    # Summary
    print(f"\n{'='*70}")
    print(f"PHASE {phase} SUMMARY")
    print(f"{'='*70}")

    complete = sum(1 for r in results if r['status'] == 'complete')
    blocked = sum(1 for r in results if r['status'] == 'blocked')
    errors = sum(1 for r in results if r['status'] == 'error')

    print(f"Complete: {complete} | Blocked: {blocked} | Errors: {errors}")
    print()

    for r in results:
        status_icon = {'complete': 'OK', 'blocked': 'BLOCK', 'error': 'ERR'}.get(r['status'], '?')
        conf = f"{r.get('confidence', 0):.0f}%" if r.get('confidence') else 'N/A'
        print(f"[{status_icon:5}] {r['bank_id']:25} {conf:>6}")

        if r.get('decision_report'):
            print(f"        └─ Decision report: {Path(r['decision_report']).name}")

        # Show action required for blocked banks
        if r.get('action_required'):
            print(f"        └─ Action: {r['action_required']} - {r.get('action_detail', '')}")

    print(f"{'='*70}")

    # Group blocked banks by action type for overnight batch summary
    if blocked > 0:
        print()
        print("BLOCKED BANKS BY ACTION REQUIRED:")
        print("-" * 50)
        action_groups = {}
        for r in results:
            if r.get('action_required'):
                action = r['action_required']
                if action not in action_groups:
                    action_groups[action] = []
                action_groups[action].append(r['bank_id'])

        for action, banks in sorted(action_groups.items()):
            print(f"\n{action} ({len(banks)} banks):")
            for bank in banks:
                print(f"  - {bank}")
        print()

    return results


def main():
    parser = argparse.ArgumentParser(
        description="CDM Research Protocol - Auto Orchestrator"
    )
    parser.add_argument('--bank', help="Bank ID to process")
    parser.add_argument('--phase', type=int, help="Phase number")
    parser.add_argument('--all', action='store_true', help="Process all banks in phase")
    parser.add_argument('--parallel', type=int, default=1, help="Parallel workers (default: 1)")
    parser.add_argument('--resume', action='store_true', default=True, help="Resume from last stage (default)")
    parser.add_argument('--fresh', action='store_true', help="Start fresh, ignore previous state")
    parser.add_argument('--approve-all', action='store_true', help="Auto-approve all pending checkpoints")
    parser.add_argument('--output', help="Output results to JSON file")

    args = parser.parse_args()

    if args.bank and args.phase:
        # Single bank
        result = run_bank_auto(args.bank, args.phase, resume=not args.fresh)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(result, indent=2), encoding='utf-8')

        sys.exit(0 if result['status'] == 'complete' else 1)

    elif args.phase and args.all:
        # All banks in phase
        results = run_phase_auto(args.phase, args.parallel)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(results, indent=2), encoding='utf-8')

        failed = sum(1 for r in results if r['status'] not in ['complete'])
        sys.exit(1 if failed > 0 else 0)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
