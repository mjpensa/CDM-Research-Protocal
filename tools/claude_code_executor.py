"""
CDM Research Protocol - Claude Code Executor v1.0

Executes research using Claude Code's built-in WebSearch capabilities.
No API key required - uses Claude Code Max subscription.

Usage:
    # Generate prompt queue for Claude Code to process
    python tools/claude_code_executor.py --bank deutsche-bank --phase 1 --generate

    # Process next prompt in queue (run from Claude Code)
    python tools/claude_code_executor.py --process-next

    # Check queue status
    python tools/claude_code_executor.py --status
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import (
    load_bank_manifest, get_bank_config, load_decision_thresholds
)

# Import prompt generators from research_executor
from research_executor import (
    generate_evidence_prompt,
    generate_bayesian_prompt,
    generate_adversarial_prompt,
    ResearchState,
    create_output_structure
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class PromptTask:
    """A single prompt task for Claude Code to execute."""
    task_id: str
    bank_id: str
    bank_name: str
    phase: int
    stage: str  # tier1_evidence, tier2_evidence, tier3_evidence, bayesian_t1, etc.
    prompt: str
    requires_web_search: bool
    output_file: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "pending"  # pending, processing, complete, error
    completed_at: Optional[str] = None


class ClaudeCodeQueue:
    """Manages the prompt queue for Claude Code execution."""

    def __init__(self, queue_path: Optional[Path] = None):
        self.queue_path = queue_path or PROJECT_ROOT / "outputs" / "state" / "claude-code-queue.json"
        self.queue_path.parent.mkdir(parents=True, exist_ok=True)
        self.tasks: List[PromptTask] = []
        self.load()

    def load(self):
        """Load existing queue from disk."""
        if self.queue_path.exists():
            try:
                data = json.loads(self.queue_path.read_text(encoding='utf-8'))
                self.tasks = [PromptTask(**task) for task in data.get('tasks', [])]
            except Exception as e:
                logger.warning(f"Could not load queue: {e}")
                self.tasks = []

    def save(self):
        """Save queue to disk."""
        data = {
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'tasks': [asdict(task) for task in self.tasks],
            'summary': self.get_summary()
        }
        self.queue_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def add_task(self, task: PromptTask):
        """Add a task to the queue."""
        self.tasks.append(task)
        self.save()

    def get_next_pending(self) -> Optional[PromptTask]:
        """Get the next pending task."""
        for task in self.tasks:
            if task.status == "pending":
                return task
        return None

    def mark_complete(self, task_id: str):
        """Mark a task as complete."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.status = "complete"
                task.completed_at = datetime.now(timezone.utc).isoformat()
        self.save()

    def mark_error(self, task_id: str, error: str):
        """Mark a task as errored."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.status = "error"
        self.save()

    def get_summary(self) -> Dict[str, Any]:
        """Get queue summary."""
        return {
            'total': len(self.tasks),
            'pending': sum(1 for t in self.tasks if t.status == 'pending'),
            'processing': sum(1 for t in self.tasks if t.status == 'processing'),
            'complete': sum(1 for t in self.tasks if t.status == 'complete'),
            'error': sum(1 for t in self.tasks if t.status == 'error'),
            'banks': list(set(t.bank_id for t in self.tasks))
        }

    def clear(self):
        """Clear the queue."""
        self.tasks = []
        self.save()

    def get_bank_tasks(self, bank_id: str) -> List[PromptTask]:
        """Get all tasks for a specific bank."""
        return [t for t in self.tasks if t.bank_id == bank_id]


def generate_bank_tasks(bank_id: str, phase: int) -> List[PromptTask]:
    """
    Generate all prompt tasks for a bank's research pipeline.

    Returns list of PromptTask objects ready for Claude Code execution.
    """
    bank_config = get_bank_config(bank_id)
    if not bank_config:
        raise ValueError(f"Bank config not found: {bank_id}")

    bank_name = bank_config.get('bank_name', bank_id)

    # Determine output directory
    manifest = load_bank_manifest()
    phase_info = manifest.get('phase_summary', {}).get(f'phase_{phase}', {})
    phase_name = phase_info.get('name', f'phase-{phase}').lower().replace(' ', '-')
    bank_dir = PROJECT_ROOT / "outputs" / f"phase-{phase}-{phase_name}" / bank_id

    create_output_structure(bank_dir)

    tasks = []

    # Calculate initial prior for state
    prior_adj = bank_config.get('prior_adjustments', {})
    base_prior = 30
    if prior_adj.get('derivatives_dominant'):
        base_prior += prior_adj.get('adjustment_pct', 10)
    if prior_adj.get('confirmed_contributor'):
        base_prior += prior_adj.get('contributor_adjustment_pct', 20)
    if prior_adj.get('confirmed_production'):
        base_prior += prior_adj.get('production_adjustment_pct', 30)
    base_prior = min(base_prior, 90)

    # Create initial state for prompt generation
    state = ResearchState(
        bank_id=bank_id,
        bank_name=bank_name,
        phase=phase,
        probability_architect=base_prior,
        probability_pragmatist=100 - base_prior
    )

    # Generate evidence gathering tasks for each tier
    for tier in [1, 2, 3]:
        evidence_prompt = generate_evidence_prompt(bank_config, tier)

        task = PromptTask(
            task_id=f"{bank_id}_tier{tier}_evidence",
            bank_id=bank_id,
            bank_name=bank_name,
            phase=phase,
            stage=f"tier{tier}_evidence",
            prompt=evidence_prompt,
            requires_web_search=True,
            output_file=str(bank_dir / "1-evidence" / f"tier{tier}-evidence.md")
        )
        tasks.append(task)

        # Bayesian update task (placeholder - actual prompt needs evidence)
        bayesian_task = PromptTask(
            task_id=f"{bank_id}_bayesian_t{tier}",
            bank_id=bank_id,
            bank_name=bank_name,
            phase=phase,
            stage=f"bayesian_t{tier}",
            prompt=f"[DEPENDS ON: {bank_id}_tier{tier}_evidence] Run Bayesian update after reading the evidence.",
            requires_web_search=False,
            output_file=str(bank_dir / "2-bayesian" / f"post-tier{tier}-update.md")
        )
        tasks.append(bayesian_task)

    # Adversarial task
    adversarial_task = PromptTask(
        task_id=f"{bank_id}_adversarial",
        bank_id=bank_id,
        bank_name=bank_name,
        phase=phase,
        stage="adversarial",
        prompt=f"[DEPENDS ON: all evidence] Run adversarial challenge.",
        requires_web_search=True,
        output_file=str(bank_dir / "4-adversarial" / "verdict.md")
    )
    tasks.append(adversarial_task)

    # Synthesis task
    synthesis_task = PromptTask(
        task_id=f"{bank_id}_synthesis",
        bank_id=bank_id,
        bank_name=bank_name,
        phase=phase,
        stage="synthesis",
        prompt=f"[DEPENDS ON: adversarial] Generate final synthesis report.",
        requires_web_search=False,
        output_file=str(bank_dir / "5-synthesis" / "assessment.md")
    )
    tasks.append(synthesis_task)

    return tasks


def generate_claude_code_instructions(bank_id: str, phase: int) -> str:
    """
    Generate instructions for Claude Code to execute the research.

    This creates a single comprehensive prompt that Claude Code can follow.
    """
    bank_config = get_bank_config(bank_id)
    if not bank_config:
        raise ValueError(f"Bank config not found: {bank_id}")

    bank_name = bank_config.get('bank_name', bank_id)

    # Get output path
    manifest = load_bank_manifest()
    phase_info = manifest.get('phase_summary', {}).get(f'phase_{phase}', {})
    phase_name = phase_info.get('name', f'phase-{phase}').lower().replace(' ', '-')
    bank_dir = f"outputs/phase-{phase}-{phase_name}/{bank_id}"

    instructions = f"""# Research Task: {bank_name}

## Overview
Execute CDM/DRR research for {bank_name} following the protocol in docs/workflow.md.

## Output Directory
{bank_dir}/

## Steps to Execute

### 1. Pre-Flight
- Read CLAUDE.md for rules
- Check knowledge_base/negative_facts.md for known dead ends
- Create output directory structure

### 2. Tier 1 Evidence (Official Sources)
Use WebSearch to find evidence from:
- {bank_name}'s official website (investor relations, press, technology)
- ISDA.org mentions of this bank
- FINOS.org / github.com/finos contribution history
- Regulatory filings (SEC, FCA, BaFin, ESMA)
- Annual reports mentioning CDM/DRR

Search queries to try:
- "{bank_name}" "Common Domain Model" OR CDM
- "{bank_name}" ISDA contribution OR member
- "{bank_name}" FINOS CDM
- site:isda.org "{bank_name}"
- site:finos.org "{bank_name}"

Save findings to: {bank_dir}/1-evidence/tier1-evidence.md

### 3. Bayesian Update T1
Calculate P(ARCHITECT) update based on Tier 1 evidence.
Save to: {bank_dir}/2-bayesian/post-tier1-update.md

### 4. Gate 1 Decision
If P(ARCHITECT) > 80% or P(PRAGMATIST) > 80%, skip to adversarial.
Otherwise continue to Tier 2.

### 5. Tier 2 Evidence (Industry Sources)
Search Risk.net, Waters Technology, Bloomberg, FT for:
- "{bank_name}" derivatives reporting modernization
- "{bank_name}" CDM pilot OR implementation
- Conference presentations by {bank_name} on CDM

Save to: {bank_dir}/1-evidence/tier2-evidence.md

### 6. Bayesian Update T2
Update probabilities.
Save to: {bank_dir}/2-bayesian/post-tier2-update.md

### 7. Gate 2 Decision
Check skip conditions again.

### 8. Tier 3 Evidence (Signals)
Search for:
- Job postings: site:{bank_name.lower().replace(' ', '')}.com CDM OR "ISDA" jobs
- LinkedIn: {bank_name} CDM team
- Patent filings

Save to: {bank_dir}/1-evidence/tier3-evidence.md

### 9. Bayesian Update T3
Final probability update.
Save to: {bank_dir}/2-bayesian/post-tier3-update.md

### 10. Adversarial Challenge
Try to DISPROVE the current classification:
- Search for counter-evidence
- Build strongest case for opposite classification
- Issue verdict: SUSTAINED, WEAKENED, or REVISED

Save to: {bank_dir}/4-adversarial/verdict.md

### 11. Synthesis
Generate final assessment following templates/per-bank-output.md.
Save to: {bank_dir}/5-synthesis/assessment.md

### 12. Status Update
Create/update {bank_dir}/status.json with:
- classification
- sub_classification
- confidence
- probability_architect
- stages_completed

## Key Research Questions
"""

    research_obj = bank_config.get('research_objective', {})
    for q in research_obj.get('key_questions', ['What is this bank doing with CDM/DRR?']):
        instructions += f"- {q}\n"

    instructions += f"""
## Known Starting Evidence
"""
    for ev in bank_config.get('known_evidence', []):
        instructions += f"- {ev.get('evidence')}: {ev.get('implication', '')}\n"

    if not bank_config.get('known_evidence'):
        instructions += "- No prior evidence. Start from scratch.\n"

    instructions += """
## Evidence Output Format
For each piece of evidence found:

### Evidence [ID]
- **Source URL**: [exact URL]
- **Source Date**: [YYYY-MM-DD]
- **Claim Type**: [production_usage/pilot_or_poc/membership_or_participation/open_source_contribution/vendor_proxy_signal/hiring_signal]
- **Finding**: [what you found]
- **Excerpt**: "[relevant quote]"
- **Supports**: [ARCHITECT/PRAGMATIST/NEUTRAL]
- **Confidence**: [1-10]

---

Ready to begin? Start with Step 1 (Pre-Flight) and proceed through all steps.
"""

    return instructions


def print_status(queue: ClaudeCodeQueue):
    """Print queue status."""
    summary = queue.get_summary()

    print(f"\n{'='*60}")
    print("CLAUDE CODE QUEUE STATUS")
    print(f"{'='*60}")
    print(f"Total tasks:    {summary['total']}")
    print(f"Pending:        {summary['pending']}")
    print(f"Processing:     {summary['processing']}")
    print(f"Complete:       {summary['complete']}")
    print(f"Errors:         {summary['error']}")
    print(f"Banks:          {', '.join(summary['banks']) if summary['banks'] else 'None'}")
    print(f"{'='*60}\n")

    # Show next pending task
    next_task = queue.get_next_pending()
    if next_task:
        print(f"Next task: {next_task.task_id}")
        print(f"  Bank: {next_task.bank_name}")
        print(f"  Stage: {next_task.stage}")
        print(f"  Web search: {'Yes' if next_task.requires_web_search else 'No'}")
        print(f"  Output: {next_task.output_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Claude Code Research Executor")
    parser.add_argument('--bank', help="Bank ID to research")
    parser.add_argument('--phase', type=int, help="Phase number")
    parser.add_argument('--generate', action='store_true', help="Generate task queue")
    parser.add_argument('--generate-instructions', action='store_true',
                        help="Generate Claude Code instructions file")
    parser.add_argument('--status', action='store_true', help="Show queue status")
    parser.add_argument('--clear', action='store_true', help="Clear the queue")
    parser.add_argument('--all-phase', type=int, help="Generate for all banks in phase")

    args = parser.parse_args()

    queue = ClaudeCodeQueue()

    if args.status:
        print_status(queue)
        return

    if args.clear:
        queue.clear()
        print("Queue cleared.")
        return

    if args.generate_instructions and args.bank and args.phase:
        instructions = generate_claude_code_instructions(args.bank, args.phase)

        # Save to file
        output_file = PROJECT_ROOT / "outputs" / "state" / f"research-instructions-{args.bank}.md"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(instructions, encoding='utf-8')

        print(f"Instructions saved to: {output_file}")
        print(f"\nTo execute, tell Claude Code:")
        print(f"  'Execute the research instructions in {output_file}'")
        return

    if args.generate and args.bank and args.phase:
        tasks = generate_bank_tasks(args.bank, args.phase)
        for task in tasks:
            queue.add_task(task)
        print(f"Generated {len(tasks)} tasks for {args.bank}")
        print_status(queue)
        return

    if args.all_phase:
        manifest = load_bank_manifest()
        banks = [b for b in manifest.get('banks', []) if b.get('phase') == args.all_phase]

        total = 0
        for bank in banks:
            tasks = generate_bank_tasks(bank['bank_id'], args.all_phase)
            for task in tasks:
                queue.add_task(task)
            total += len(tasks)

        print(f"Generated {total} tasks for {len(banks)} banks in phase {args.all_phase}")
        print_status(queue)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
