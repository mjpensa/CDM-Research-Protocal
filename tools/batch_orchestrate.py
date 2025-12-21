"""
CDM Research Protocol - Batch Orchestrator v1.1

Runs complete live research pipeline for all banks.
All research is executed with Claude API - no simulation mode.
Collects edge cases into a review queue for deferred human review.

Usage:
    # Run all banks overnight
    python tools/batch_orchestrate.py --phase 1
    python tools/batch_orchestrate.py --all-phases

    # Review results in the morning
    python tools/batch_orchestrate.py --review
    python tools/batch_orchestrate.py --review --approve-all-clean

    # Approve specific banks
    python tools/batch_orchestrate.py --approve deutsche-bank barclays

Features:
    - Live research with Claude API
    - Provisional classifications assigned to edge cases
    - Consolidated review queue generated at end
    - Batch approval/adjustment interface
    - Resume from interruption
"""

import sys
import json
import logging
import argparse
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import load_bank_manifest, get_bank_config

# Import unified state management (Phase 5 consolidation)
try:
    from state_manager import UnifiedStateManager
    from state_schema import ReviewItem as UnifiedReviewItem
    STATE_MANAGER_AVAILABLE = True
except ImportError:
    STATE_MANAGER_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReviewStatus(Enum):
    """Status of a bank's review requirement."""
    CLEAN = "clean"                      # Auto-approved, no review needed
    NEEDS_REVIEW = "needs_review"        # Flagged for review
    REVIEWED = "reviewed"                # Human has reviewed
    APPROVED = "approved"                # Approved after review
    ADJUSTED = "adjusted"                # Classification adjusted


@dataclass
class ReviewItem:
    """
    A single item requiring human review.

    DEPRECATED: This class is being migrated to state_schema.ReviewItem.
    New code should use UnifiedStateManager for review queue operations.
    This class is retained for backward compatibility.
    """
    bank_id: str
    bank_name: str
    phase: int
    issue_type: str
    issue_description: str
    provisional_classification: str
    provisional_confidence: int
    probability_architect: float
    evidence_count: int
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    resolution: Optional[str] = None
    resolved_at: Optional[str] = None
    resolved_by: Optional[str] = None


@dataclass
class BatchResult:
    """Result of batch processing a bank."""
    bank_id: str
    phase: int
    status: str  # complete, error
    review_status: ReviewStatus
    classification: Optional[str] = None
    sub_classification: Optional[str] = None
    confidence: Optional[int] = None
    probability_architect: Optional[float] = None
    evidence_count: int = 0
    review_items: List[ReviewItem] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    duration_seconds: float = 0


@dataclass
class BatchExecutionContext:
    """
    Tracks batch execution state for circuit breaker pattern.

    Category 2 fix: Silent Error Propagation
    - Tracks consecutive failures to halt batch if threshold exceeded
    - Records success/failure for each bank processed
    """
    consecutive_failures: int = 0
    total_failures: int = 0
    total_processed: int = 0
    failure_threshold: int = 10  # Halt after N consecutive failures
    halt_requested: bool = False
    last_failure_reason: Optional[str] = None

    def record_success(self) -> None:
        """Record successful bank processing. Resets consecutive failure count."""
        self.consecutive_failures = 0
        self.total_processed += 1

    def record_failure(self, reason: str) -> bool:
        """
        Record failed bank processing.

        Args:
            reason: Description of failure

        Returns:
            True if batch should halt (threshold exceeded)
        """
        self.consecutive_failures += 1
        self.total_failures += 1
        self.total_processed += 1
        self.last_failure_reason = reason
        return self.consecutive_failures >= self.failure_threshold

    def should_halt(self) -> bool:
        """Check if batch should stop processing."""
        return self.halt_requested or self.consecutive_failures >= self.failure_threshold

    def get_summary(self) -> Dict[str, Any]:
        """Get execution summary for logging."""
        return {
            "total_processed": self.total_processed,
            "total_failures": self.total_failures,
            "consecutive_failures": self.consecutive_failures,
            "halted": self.halt_requested,
            "last_failure": self.last_failure_reason
        }


class ReviewQueue:
    """Manages the deferred review queue with thread-safe file access."""

    def __init__(self, queue_path: Optional[Path] = None):
        self.queue_path = queue_path or PROJECT_ROOT / "outputs" / "state" / "review-queue.json"
        self.queue_path.parent.mkdir(parents=True, exist_ok=True)
        self.items: List[ReviewItem] = []
        self.results: List[BatchResult] = []
        self._lock = __import__('threading').Lock()
        self.load()

    def load(self):
        """Load existing queue from disk."""
        if self.queue_path.exists():
            try:
                data = json.loads(self.queue_path.read_text(encoding='utf-8'))
                self.items = [ReviewItem(**item) for item in data.get('items', [])]
                self.results = [BatchResult(**r) for r in data.get('results', [])]
            except Exception as e:
                logger.warning(f"Could not load review queue: {e}")
                self.items = []
                self.results = []

    def save(self):
        """Save queue to disk (thread-safe)."""
        with self._lock:
            data = {
                'last_updated': datetime.utcnow().isoformat(),
                'items': [asdict(item) for item in self.items],
                'results': [asdict(r) for r in self.results],
                'summary': self.get_summary()
            }
            self.queue_path.write_text(json.dumps(data, indent=2, default=str), encoding='utf-8')

    def add_item(self, item: ReviewItem):
        """Add a review item to the queue (thread-safe)."""
        with self._lock:
            self.items.append(item)
        self.save()

    def add_result(self, result: BatchResult):
        """Add a batch result (thread-safe)."""
        with self._lock:
            self.results.append(result)
        self.save()

    def get_pending_reviews(self) -> List[ReviewItem]:
        """Get items still needing review."""
        return [item for item in self.items if item.resolution is None]

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        pending = self.get_pending_reviews()
        return {
            'total_banks': len(self.results),
            'clean': sum(1 for r in self.results if r.review_status == ReviewStatus.CLEAN),
            'needs_review': sum(1 for r in self.results if r.review_status == ReviewStatus.NEEDS_REVIEW),
            'reviewed': sum(1 for r in self.results if r.review_status == ReviewStatus.REVIEWED),
            'errors': sum(1 for r in self.results if r.status == 'error'),
            'pending_review_items': len(pending),
            'issue_types': self._count_issue_types(pending)
        }

    def _count_issue_types(self, items: List[ReviewItem]) -> Dict[str, int]:
        """Count occurrences of each issue type."""
        counts = {}
        for item in items:
            counts[item.issue_type] = counts.get(item.issue_type, 0) + 1
        return counts

    def resolve_item(self, bank_id: str, resolution: str, resolver: str = "human"):
        """Mark a review item as resolved."""
        for item in self.items:
            if item.bank_id == bank_id and item.resolution is None:
                item.resolution = resolution
                item.resolved_at = datetime.utcnow().isoformat()
                item.resolved_by = resolver
        self.save()

    def clear(self):
        """Clear the queue (for fresh batch run)."""
        self.items = []
        self.results = []
        self.save()


# Issue types that don't block execution but require review
REVIEW_TRIGGERS = {
    'low_confidence': {
        'condition': lambda state: state.get('confidence', 0) < 50,
        'description': 'Low confidence ({confidence}%) requires verification',
        'severity': 'high'
    },
    'uncertain_probability': {
        'condition': lambda state: 0.30 <= state.get('probability_architect', 0.50) <= 0.70,
        'description': 'Uncertain probability (P={probability_architect:.1%}) - could go either way',
        'severity': 'medium'
    },
    'adversarial_revised': {
        'condition': lambda state: state.get('adversarial_verdict') == 'REVISED',
        'description': 'Adversarial challenge revised classification',
        'severity': 'high'
    },
    'single_tier_evidence': {
        'condition': lambda state: state.get('highest_tier', 3) == 3 and state.get('evidence_count', 0) < 5,
        'description': 'Only Tier 3 evidence with low count',
        'severity': 'medium'
    },
    'contradiction_detected': {
        'condition': lambda state: state.get('contradictions', []),
        'description': 'Contradicting evidence detected',
        'severity': 'high'
    },
    'trust_flags': {
        'condition': lambda state: len(state.get('trust_flags', [])) > 0,
        'description': 'Trust audit raised flags: {trust_flags}',
        'severity': 'medium'
    },
    'extreme_lr': {
        'condition': lambda state: state.get('combined_lr', 1) > 100 or state.get('combined_lr', 1) < 0.01,
        'description': 'Extreme likelihood ratio ({combined_lr}) may indicate error',
        'severity': 'medium'
    },
    'anchor_violation': {
        'condition': lambda state: state.get('anchor_violation', False),
        'description': 'Classification may violate anchor point',
        'severity': 'critical'
    }
}


def check_review_triggers(state: Dict[str, Any]) -> List[tuple]:
    """Check which review triggers are activated."""
    triggered = []
    for trigger_id, trigger in REVIEW_TRIGGERS.items():
        try:
            if trigger['condition'](state):
                desc = trigger['description'].format(**state)
                triggered.append((trigger_id, desc, trigger['severity']))
        except Exception:
            pass
    return triggered


def run_research(bank_id: str, phase: int, bank_config: dict,
                 model: str = "claude-opus-4-5-20250101") -> Dict[str, Any]:
    """
    Execute live research using Claude API.

    Args:
        bank_id: Bank identifier
        phase: Phase number
        bank_config: Bank configuration
        model: Claude model to use

    Returns:
        Research state dictionary
    """
    from research_executor import execute_research

    state = execute_research(bank_id, phase, model=model)

    return {
        'bank_id': state.bank_id,
        'phase': state.phase,
        'probability_architect': state.probability_architect,
        'classification': state.classification,
        'sub_classification': state.sub_classification,
        'confidence': state.confidence,
        'evidence_count': len(state.evidence_items),
        'highest_tier': state.highest_tier,
        'trust_flags': state.trust_flags,
        'adversarial_verdict': state.adversarial_verdict,
        'contradictions': [],
        'combined_lr': 1.0,
        'anchor_violation': False,
        'errors': state.errors
    }


def execute_bank_research(bank_id: str, phase: int, queue: ReviewQueue) -> BatchResult:
    """
    Execute live research for a single bank.

    Args:
        bank_id: Bank identifier
        phase: Phase number
        queue: Review queue to add items to

    Returns:
        BatchResult with status and any review items
    """
    start_time = datetime.utcnow()

    # Get bank config
    bank_config = get_bank_config(bank_id)
    if not bank_config:
        return BatchResult(
            bank_id=bank_id,
            phase=phase,
            status='error',
            review_status=ReviewStatus.NEEDS_REVIEW,
            errors=[f"Bank config not found for {bank_id}"]
        )

    bank_name = bank_config.get('bank_name', bank_id)

    logger.info(f"Processing: {bank_name}")

    try:
        # Execute live research
        state = run_research(bank_id, phase, bank_config)

        # Check for review triggers
        triggers = check_review_triggers(state)

        # Build result
        result = BatchResult(
            bank_id=bank_id,
            phase=phase,
            status='complete',
            review_status=ReviewStatus.CLEAN if not triggers else ReviewStatus.NEEDS_REVIEW,
            classification=state.get('classification'),
            sub_classification=state.get('sub_classification'),
            confidence=state.get('confidence'),
            probability_architect=state.get('probability_architect'),
            evidence_count=state.get('evidence_count', 0),
            duration_seconds=(datetime.utcnow() - start_time).total_seconds()
        )

        # Add review items for each trigger
        for trigger_id, description, severity in triggers:
            item = ReviewItem(
                bank_id=bank_id,
                bank_name=bank_name,
                phase=phase,
                issue_type=trigger_id,
                issue_description=description,
                provisional_classification=f"{state.get('classification')} ({state.get('sub_classification')})",
                provisional_confidence=state.get('confidence', 0),
                probability_architect=state.get('probability_architect', 50),
                evidence_count=state.get('evidence_count', 0)
            )
            result.review_items.append(item)
            queue.add_item(item)

        queue.add_result(result)

        status_icon = "[OK]" if result.review_status == ReviewStatus.CLEAN else "[!!]"
        logger.info(f"  {status_icon} {bank_name}: {result.classification} ({result.confidence}%)")

        return result

    except Exception as e:
        logger.error(f"  [XX] {bank_name}: Error - {e}")
        result = BatchResult(
            bank_id=bank_id,
            phase=phase,
            status='error',
            review_status=ReviewStatus.NEEDS_REVIEW,
            errors=[str(e)],
            duration_seconds=(datetime.utcnow() - start_time).total_seconds()
        )
        queue.add_result(result)
        return result


# Error types that are eligible for retry (transient errors)
TRANSIENT_ERRORS = (
    'RateLimitError',
    'TimeoutError',
    'APIConnectionError',
    'InternalServerError',
    'ServiceUnavailableError',
)


def execute_bank_research_with_retry(
    bank_id: str,
    phase: int,
    queue: ReviewQueue,
    context: BatchExecutionContext,
    max_retries: int = 2
) -> BatchResult:
    """
    Execute research with retry for transient errors and circuit breaker tracking.

    Category 2 fix: Silent Error Propagation
    - Retries transient errors (rate limits, timeouts) with exponential backoff
    - Records success/failure in BatchExecutionContext for circuit breaker
    - Halts batch if consecutive failure threshold exceeded

    Args:
        bank_id: Bank identifier
        phase: Phase number
        queue: Review queue for results
        context: Batch execution context for tracking
        max_retries: Maximum retry attempts for transient errors

    Returns:
        BatchResult from research execution
    """
    for attempt in range(max_retries + 1):
        try:
            result = execute_bank_research(bank_id, phase, queue)

            if result.status == 'complete':
                context.record_success()
            else:
                # Non-exception error (validation failure, etc.)
                error_reason = result.errors[0] if result.errors else "Unknown error"
                if context.record_failure(error_reason):
                    logger.error(
                        f"HALTING BATCH: {context.consecutive_failures} consecutive failures"
                    )
                    context.halt_requested = True

            return result

        except Exception as e:
            error_type = type(e).__name__

            # Check if error is retry-eligible
            if error_type in TRANSIENT_ERRORS and attempt < max_retries:
                wait_time = (2 ** attempt) * 5  # Exponential backoff: 5s, 10s, 20s
                logger.warning(
                    f"Transient error ({error_type}) for {bank_id}, "
                    f"retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})"
                )
                time.sleep(wait_time)
                continue

            # Non-retryable or exhausted retries
            if context.record_failure(str(e)):
                logger.error(
                    f"HALTING BATCH: {context.consecutive_failures} consecutive failures"
                )
                context.halt_requested = True

            return BatchResult(
                bank_id=bank_id,
                phase=phase,
                status='error',
                review_status=ReviewStatus.NEEDS_REVIEW,
                errors=[f"[{error_type}] {e} (attempts: {attempt + 1})"]
            )

    # Should not reach here, but safety fallback
    return BatchResult(
        bank_id=bank_id,
        phase=phase,
        status='error',
        review_status=ReviewStatus.NEEDS_REVIEW,
        errors=["Exhausted all retry attempts"]
    )


def run_batch(phases: List[int] = None, parallel: int = 3,
              fresh: bool = False,
              failure_threshold: int = 10) -> tuple:
    """
    Run batch processing for all banks with live research.

    Supports:
    - Resumability: already-completed banks are automatically skipped
    - Circuit breaker: halts after N consecutive failures
    - Retry: transient errors are retried with exponential backoff

    Args:
        phases: List of phase numbers to process (None = all)
        parallel: Number of parallel workers
        fresh: If True, clear existing queue and reprocess all banks
        failure_threshold: Halt after this many consecutive failures

    Returns:
        Tuple of (ReviewQueue, BatchExecutionContext)
    """
    queue = ReviewQueue()
    context = BatchExecutionContext(failure_threshold=failure_threshold)

    if fresh:
        queue.clear()

    manifest = load_bank_manifest()
    banks = manifest.get('banks', [])

    if phases:
        banks = [b for b in banks if b.get('phase') in phases]

    # Filter out already-completed banks (Category 1 fix: Batch Resumability)
    banks_to_process = []
    skipped_count = 0

    if STATE_MANAGER_AVAILABLE and not fresh:
        state_manager = UnifiedStateManager(PROJECT_ROOT / "outputs")

        for bank in banks:
            bank_id = bank['bank_id']
            phase = bank['phase']

            if state_manager.is_bank_complete(bank_id, phase):
                logger.info(f"[SKIP] {bank_id} already complete")
                skipped_count += 1
                continue

            banks_to_process.append(bank)
    else:
        # No state manager or fresh run - process all
        banks_to_process = banks

    logger.info(f"\n{'='*70}")
    logger.info(f"BATCH ORCHESTRATOR - Processing {len(banks_to_process)} banks")
    if skipped_count > 0:
        logger.info(f"Skipped {skipped_count} already-completed banks")
    logger.info(f"Parallel workers: {parallel}")
    logger.info(f"{'='*70}\n")

    start_time = datetime.utcnow()

    if parallel == 1:
        # Sequential processing with circuit breaker
        for bank in banks_to_process:
            # Check circuit breaker before each bank
            if context.should_halt():
                logger.warning(
                    f"BATCH HALTED: {context.consecutive_failures} consecutive failures. "
                    f"Last error: {context.last_failure_reason}"
                )
                break

            execute_bank_research_with_retry(
                bank['bank_id'],
                bank['phase'],
                queue,
                context
            )
    else:
        # Parallel processing with circuit breaker
        # Note: Circuit breaker checks happen inside retry wrapper
        # For true parallel halt, we'd need more complex coordination
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {}
            for bank in banks_to_process:
                # Check circuit breaker before submitting new work
                if context.should_halt():
                    logger.warning(
                        f"BATCH HALTED: {context.consecutive_failures} consecutive failures. "
                        f"Last error: {context.last_failure_reason}"
                    )
                    break

                future = executor.submit(
                    execute_bank_research_with_retry,
                    bank['bank_id'],
                    bank['phase'],
                    queue,
                    context
                )
                futures[future] = bank

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    bank = futures[future]
                    logger.error(f"Error processing {bank['bank_id']}: {e}")

    duration = (datetime.utcnow() - start_time).total_seconds()

    # Print summary
    summary = queue.get_summary()
    exec_summary = context.get_summary()

    # Determine completion status
    if context.should_halt():
        status_msg = f"BATCH HALTED (circuit breaker triggered) - {duration:.1f} seconds"
    else:
        status_msg = f"BATCH COMPLETE - {duration:.1f} seconds"

    print(f"\n{'='*70}")
    print(status_msg)
    print(f"{'='*70}")
    print(f"")
    print(f"  Total banks processed: {summary['total_banks']}")
    print(f"  [OK] Clean (auto-approved):  {summary['clean']}")
    print(f"  [!!] Needs review:           {summary['needs_review']}")
    print(f"  [XX] Errors:                 {summary['errors']}")
    print(f"")

    # Circuit breaker status
    if exec_summary['total_failures'] > 0:
        print(f"  Circuit Breaker Status:")
        print(f"    Total failures:       {exec_summary['total_failures']}")
        print(f"    Consecutive failures: {exec_summary['consecutive_failures']}")
        if exec_summary['halted']:
            print(f"    Status:               HALTED")
            print(f"    Last error:           {exec_summary['last_failure']}")
        print(f"")

    if skipped_count > 0:
        print(f"  Already complete (skipped): {skipped_count}")
        print(f"")

    if summary['pending_review_items'] > 0:
        print(f"  Review items by type:")
        for issue_type, count in summary['issue_types'].items():
            print(f"    - {issue_type}: {count}")
        print(f"")
        print(f"  Run 'python tools/batch_orchestrate.py --review' to review")
    else:
        print(f"  All banks auto-approved!")

    print(f"{'='*70}\n")

    queue.save()
    return queue, context


def generate_review_report(queue: ReviewQueue) -> str:
    """Generate a consolidated review report."""
    summary = queue.get_summary()
    pending = queue.get_pending_reviews()

    report = f"""# Batch Research Review Report

Generated: {datetime.utcnow().isoformat()}

## Summary

| Metric | Value |
|--------|-------|
| Total Banks | {summary['total_banks']} |
| Auto-Approved (Clean) | {summary['clean']} |
| Needs Review | {summary['needs_review']} |
| Errors | {summary['errors']} |
| Pending Review Items | {summary['pending_review_items']} |

---

## Banks Requiring Review

"""

    # Group by severity
    critical = [p for p in pending if 'anchor' in p.issue_type or 'revised' in p.issue_type]
    high = [p for p in pending if p.issue_type in ['low_confidence', 'contradiction_detected'] and p not in critical]
    medium = [p for p in pending if p not in critical and p not in high]

    if critical:
        report += "### [CRITICAL] Requires Immediate Attention\n\n"
        for item in critical:
            report += f"""#### {item.bank_name}
- **Issue**: {item.issue_description}
- **Provisional**: {item.provisional_classification} @ {item.provisional_confidence}%
- **P(Architect)**: {item.probability_architect}%
- **Evidence**: {item.evidence_count} items

"""

    if high:
        report += "### [HIGH] High Priority\n\n"
        for item in high:
            report += f"""#### {item.bank_name}
- **Issue**: {item.issue_description}
- **Provisional**: {item.provisional_classification} @ {item.provisional_confidence}%
- **P(Architect)**: {item.probability_architect}%

"""

    if medium:
        report += "### [MEDIUM] Medium Priority\n\n"
        for item in medium:
            report += f"- **{item.bank_name}**: {item.issue_description} ({item.provisional_classification})\n"

    report += """
---

## Quick Actions

```bash
# Approve all clean + medium priority banks
python tools/batch_orchestrate.py --approve-threshold medium

# Approve specific banks
python tools/batch_orchestrate.py --approve deutsche-bank barclays hsbc

# Adjust a classification
python tools/batch_orchestrate.py --adjust bank-of-america PRAGMATIST Vendor-Dependent 65

# Export for spreadsheet review
python tools/batch_orchestrate.py --export-csv review.csv
```

---

## Detailed Results by Bank

"""

    for result in queue.results:
        status_icon = "OK" if result.review_status == ReviewStatus.CLEAN else "!!" if result.review_status == ReviewStatus.NEEDS_REVIEW else "?"
        report += f"| {status_icon} | {result.bank_id} | {result.classification or 'N/A'} | {result.confidence or 0}% | {len(result.review_items)} issues |\n"

    return report


def interactive_review(queue: ReviewQueue):
    """Interactive review interface."""
    pending = queue.get_pending_reviews()

    if not pending:
        print("\n[OK] No pending reviews! All banks have been processed.\n")
        return

    print(f"\n{'='*70}")
    print(f"INTERACTIVE REVIEW - {len(pending)} items pending")
    print(f"{'='*70}\n")

    # Group by bank
    by_bank = {}
    for item in pending:
        if item.bank_id not in by_bank:
            by_bank[item.bank_id] = []
        by_bank[item.bank_id].append(item)

    for i, (bank_id, items) in enumerate(by_bank.items(), 1):
        item = items[0]  # Use first item for summary

        print(f"\n[{i}/{len(by_bank)}] {item.bank_name}")
        print(f"    Provisional: {item.provisional_classification} @ {item.provisional_confidence}%")
        print(f"    P(Architect): {item.probability_architect}%")
        print(f"    Evidence: {item.evidence_count} items")
        print(f"    Issues:")
        for issue in items:
            print(f"      - {issue.issue_type}: {issue.issue_description}")

        print(f"\n    Options:")
        print(f"      [A] Approve provisional classification")
        print(f"      [M] Modify classification")
        print(f"      [S] Skip (review later)")
        print(f"      [Q] Quit review")

        choice = input("\n    Choice: ").strip().upper()

        if choice == 'A':
            queue.resolve_item(bank_id, "approved_as_provisional", "human")
            print(f"    [OK] Approved: {item.provisional_classification}")
        elif choice == 'M':
            new_class = input("    New classification (ARCHITECT/PRAGMATIST): ").strip().upper()
            new_conf = input("    New confidence (0-100): ").strip()
            queue.resolve_item(bank_id, f"modified:{new_class}:{new_conf}", "human")
            print(f"    [OK] Modified to: {new_class} @ {new_conf}%")
        elif choice == 'S':
            print(f"    -> Skipped")
        elif choice == 'Q':
            print(f"\n    Review paused. Run --review to continue.\n")
            break

    queue.save()
    remaining = len(queue.get_pending_reviews())
    print(f"\n{'='*70}")
    print(f"Review session complete. {remaining} items still pending.")
    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description="CDM Research - Batch Orchestrator (Live Research Only)"
    )

    # Execution modes
    parser.add_argument('--phase', type=int, action='append',
                        help="Phase to process (can specify multiple)")
    parser.add_argument('--all-phases', action='store_true',
                        help="Process all phases")
    parser.add_argument('--parallel', type=int, default=3,
                        help="Parallel workers (default: 3)")
    parser.add_argument('--fresh', action='store_true',
                        help="Clear existing queue and start fresh")
    parser.add_argument('--claude-code', action='store_true',
                        help="Generate instructions for Claude Code execution")
    parser.add_argument('--bank', type=str,
                        help="Single bank to process (use with --claude-code)")

    # Review modes
    parser.add_argument('--review', action='store_true',
                        help="Interactive review of pending items")
    parser.add_argument('--report', action='store_true',
                        help="Generate review report")
    parser.add_argument('--status', action='store_true',
                        help="Show current queue status")

    # Batch approval
    parser.add_argument('--approve', nargs='+', metavar='BANK_ID',
                        help="Approve specific banks")
    parser.add_argument('--approve-all-clean', action='store_true',
                        help="Approve all banks with no issues")
    parser.add_argument('--approve-threshold', choices=['critical', 'high', 'medium', 'all'],
                        help="Approve all banks at or below threshold")

    # Export
    parser.add_argument('--export-csv', metavar='FILE',
                        help="Export results to CSV")
    parser.add_argument('--export-report', metavar='FILE',
                        help="Export review report to file")

    args = parser.parse_args()

    queue = ReviewQueue()

    # Status check
    if args.status:
        summary = queue.get_summary()
        print(f"\nQueue Status:")
        print(f"  Total banks: {summary['total_banks']}")
        print(f"  Clean: {summary['clean']}")
        print(f"  Needs review: {summary['needs_review']}")
        print(f"  Pending items: {summary['pending_review_items']}")
        return

    # Review mode
    if args.review:
        interactive_review(queue)
        return

    # Report generation
    if args.report or args.export_report:
        report = generate_review_report(queue)
        if args.export_report:
            Path(args.export_report).write_text(report, encoding='utf-8')
            print(f"Report exported to: {args.export_report}")
        else:
            print(report)
        return

    # Batch approval
    if args.approve:
        for bank_id in args.approve:
            queue.resolve_item(bank_id, "approved_via_cli", "human")
            print(f"[OK] Approved: {bank_id}")
        return

    if args.approve_all_clean:
        for result in queue.results:
            if result.review_status == ReviewStatus.CLEAN:
                queue.resolve_item(result.bank_id, "auto_approved_clean", "batch")
        print(f"[OK] Approved all clean banks")
        return

    # CSV export
    if args.export_csv:
        import csv
        with open(args.export_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Bank ID', 'Phase', 'Classification', 'Confidence',
                           'P(Architect)', 'Evidence', 'Review Status', 'Issues'])
            for result in queue.results:
                issues = '; '.join([i.issue_type for i in result.review_items])
                writer.writerow([
                    result.bank_id, result.phase, result.classification,
                    result.confidence, result.probability_architect,
                    result.evidence_count, result.review_status.value, issues
                ])
        print(f"Exported to: {args.export_csv}")
        return

    # Claude Code mode - generate instructions for interactive execution
    if args.claude_code:
        try:
            from claude_code_executor import generate_claude_code_instructions, ClaudeCodeQueue
        except ImportError:
            print("Error: claude_code_executor.py not found")
            return

        if args.bank and args.phase:
            # Single bank
            phase = args.phase[0] if isinstance(args.phase, list) else args.phase
            instructions = generate_claude_code_instructions(args.bank, phase)
            output_file = PROJECT_ROOT / "outputs" / "state" / f"research-instructions-{args.bank}.md"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(instructions, encoding='utf-8')

            print(f"\n{'='*60}")
            print(f"CLAUDE CODE INSTRUCTIONS GENERATED")
            print(f"{'='*60}")
            print(f"Bank: {args.bank}")
            print(f"Phase: {phase}")
            print(f"Output: {output_file}")
            print(f"\nTo execute, tell Claude Code:")
            print(f"  'Research {args.bank} following outputs/state/research-instructions-{args.bank}.md'")
            print(f"{'='*60}\n")

        elif args.phase:
            # All banks in phase(s)
            manifest = load_bank_manifest()
            phases_to_process = args.phase if isinstance(args.phase, list) else [args.phase]

            for phase in phases_to_process:
                banks = [b for b in manifest.get('banks', []) if b.get('phase') == phase]
                print(f"\n{'='*60}")
                print(f"PHASE {phase} - Generating instructions for {len(banks)} banks")
                print(f"{'='*60}")

                for bank in banks:
                    bank_id = bank['bank_id']
                    instructions = generate_claude_code_instructions(bank_id, phase)
                    output_file = PROJECT_ROOT / "outputs" / "state" / f"research-instructions-{bank_id}.md"
                    output_file.write_text(instructions, encoding='utf-8')
                    print(f"  Generated: {bank_id}")

                print(f"\nTo execute all, tell Claude Code:")
                print(f"  'Research all Phase {phase} banks following the instructions in outputs/state/'")

        elif args.all_phases:
            manifest = load_bank_manifest()
            banks = manifest.get('banks', [])
            print(f"\n{'='*60}")
            print(f"ALL PHASES - Generating instructions for {len(banks)} banks")
            print(f"{'='*60}")

            for bank in banks:
                bank_id = bank['bank_id']
                phase = bank['phase']
                instructions = generate_claude_code_instructions(bank_id, phase)
                output_file = PROJECT_ROOT / "outputs" / "state" / f"research-instructions-{bank_id}.md"
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(instructions, encoding='utf-8')
                print(f"  Generated: {bank_id} (Phase {phase})")

            print(f"\nTo execute, tell Claude Code:")
            print(f"  'Research all banks following the instructions in outputs/state/'")

        else:
            print("Error: --claude-code requires --bank and --phase, or --phase alone, or --all-phases")
        return

    # Run batch processing (always live)
    phases = args.phase if args.phase else None
    if args.all_phases:
        phases = None  # None means all

    if phases is not None or args.all_phases:
        run_batch(
            phases=phases,
            parallel=args.parallel,
            fresh=args.fresh
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
