#!/usr/bin/env python3
"""
Technical Debt Proxy Analyzer

Banks with heavy technical debt are more likely PRAGMATIST.
Proxies include: legacy system job postings, M&A activity, cost-cutting announcements.

Usage:
    python debt_proxy_analyzer.py --bank deutsche-bank --analyze
    python debt_proxy_analyzer.py --bank hsbc --scan-job-postings
    python debt_proxy_analyzer.py --phase 1 --batch-analyze
"""

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Import config loader
sys.path.insert(0, str(SCRIPT_DIR))
from config_loader import load_bank_manifest, get_bank_config


def load_debt_proxies() -> dict:
    """Load technical debt proxy configuration."""
    path = CONFIG_DIR / "technical-debt-proxies.json"
    if not path.exists():
        return {"job_posting_proxies": {}, "organizational_proxies": {}}
    return json.loads(path.read_text(encoding='utf-8'))


@dataclass
class ProxySignal:
    """Represents a detected proxy signal."""
    signal_type: str
    category: str
    description: str
    weight: float
    direction: str  # 'pragmatist' or 'architect'
    source: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DebtProxyAnalysis:
    """Complete debt proxy analysis for a bank."""
    bank_id: str
    bank_name: str
    signals: List[ProxySignal]
    pragmatist_score: float
    architect_score: float
    net_direction: str
    net_strength: float
    recommended_prior_adjustment: float
    contributing_signals: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = asdict(self)
        result['signals'] = [s.to_dict() for s in self.signals]
        return result


class DebtProxyAnalyzer:
    """Analyzes technical debt proxies to inform classification."""

    def __init__(self):
        self.config = load_debt_proxies()
        self.bank_manifest = load_bank_manifest()
        self.job_proxies = self.config.get('job_posting_proxies', {})
        self.org_proxies = self.config.get('organizational_proxies', {})
        self.aggregation = self.config.get('signal_aggregation', {})

    def load_bank_evidence(
        self,
        bank_id: str,
        phase: Optional[int] = None
    ) -> List[dict]:
        """Load evidence items for a bank."""
        if phase:
            phase_patterns = [f"phase-{phase}-*"]
        else:
            phase_patterns = ["phase-*"]

        for pattern in phase_patterns:
            for phase_dir in OUTPUTS_DIR.glob(pattern):
                bank_dir = phase_dir / bank_id
                evidence_file = bank_dir / "evidence.json"
                if evidence_file.exists():
                    try:
                        data = json.loads(evidence_file.read_text(encoding='utf-8'))
                        return data.get('evidence', data.get('evidence_items', []))
                    except (json.JSONDecodeError, KeyError):
                        pass
        return []

    def scan_text_for_keywords(
        self,
        text: str,
        keyword_config: dict
    ) -> List[tuple]:
        """Scan text for keyword matches."""
        matches = []
        text_lower = text.lower()
        keywords = keyword_config.get('keywords', [])

        for keyword in keywords:
            if keyword.lower() in text_lower:
                matches.append((
                    keyword,
                    keyword_config.get('weight', 0.5),
                    keyword_config.get('direction', 'neutral')
                ))

        return matches

    def analyze_evidence_for_proxies(
        self,
        evidence: List[dict]
    ) -> List[ProxySignal]:
        """Analyze evidence items for debt proxy signals."""
        signals = []

        # Check hiring signals for debt proxies
        hiring_items = [
            e for e in evidence
            if e.get('claim_type') == 'hiring_signal'
        ]

        for item in hiring_items:
            claim_text = item.get('claim', '') + ' ' + item.get('notes', '')

            # Check legacy keywords
            legacy_config = self.job_proxies.get('legacy_system_keywords', {})
            legacy_matches = self.scan_text_for_keywords(claim_text, legacy_config)
            for keyword, weight, direction in legacy_matches:
                signals.append(ProxySignal(
                    signal_type='legacy_keyword',
                    category='job_posting',
                    description=f"Legacy keyword detected: {keyword}",
                    weight=weight,
                    direction=direction,
                    source=item.get('source_url')
                ))

            # Check cost pressure keywords
            cost_config = self.job_proxies.get('cost_pressure_keywords', {})
            cost_matches = self.scan_text_for_keywords(claim_text, cost_config)
            for keyword, weight, direction in cost_matches:
                signals.append(ProxySignal(
                    signal_type='cost_pressure_keyword',
                    category='job_posting',
                    description=f"Cost pressure keyword: {keyword}",
                    weight=weight,
                    direction=direction,
                    source=item.get('source_url')
                ))

            # Check modernization keywords
            modern_config = self.job_proxies.get('modernization_keywords', {})
            modern_matches = self.scan_text_for_keywords(claim_text, modern_config)
            for keyword, weight, direction in modern_matches:
                signals.append(ProxySignal(
                    signal_type='modernization_keyword',
                    category='job_posting',
                    description=f"Modernization keyword: {keyword}",
                    weight=weight,
                    direction=direction,
                    source=item.get('source_url')
                ))

            # Check CDM direct keywords
            cdm_config = self.job_proxies.get('cdm_direct_keywords', {})
            cdm_matches = self.scan_text_for_keywords(claim_text, cdm_config)
            for keyword, weight, direction in cdm_matches:
                signals.append(ProxySignal(
                    signal_type='cdm_direct_keyword',
                    category='job_posting',
                    description=f"CDM hiring: {keyword}",
                    weight=weight,
                    direction=direction,
                    source=item.get('source_url')
                ))

        # Check all evidence for organizational proxy keywords
        restructuring_config = self.org_proxies.get('restructuring_announcements', {})
        for item in evidence:
            claim_text = item.get('claim', '') + ' ' + item.get('notes', '')
            restructuring_matches = self.scan_text_for_keywords(
                claim_text, restructuring_config
            )
            for keyword, weight, direction in restructuring_matches:
                signals.append(ProxySignal(
                    signal_type='restructuring_keyword',
                    category='organizational',
                    description=f"Restructuring signal: {keyword}",
                    weight=weight,
                    direction=direction,
                    source=item.get('source_url')
                ))

        return signals

    def analyze_bank(
        self,
        bank_id: str,
        phase: Optional[int] = None
    ) -> DebtProxyAnalysis:
        """Analyze technical debt proxies for a bank."""
        bank_config = get_bank_config(bank_id)
        bank_name = bank_config.get('bank_name', bank_id) if bank_config else bank_id

        # Load evidence and analyze
        evidence = self.load_bank_evidence(bank_id, phase)
        signals = self.analyze_evidence_for_proxies(evidence)

        # Calculate scores
        pragmatist_score = 0.0
        architect_score = 0.0
        contributing = []

        for signal in signals:
            if signal.direction == 'pragmatist':
                pragmatist_score += signal.weight
                contributing.append(f"[-] {signal.description}")
            elif signal.direction == 'architect':
                architect_score += signal.weight
                contributing.append(f"[+] {signal.description}")

        # Normalize scores
        total = pragmatist_score + architect_score
        if total > 0:
            pragmatist_norm = pragmatist_score / total
            architect_norm = architect_score / total
        else:
            pragmatist_norm = 0.5
            architect_norm = 0.5

        # Determine direction
        threshold_pragmatist = self.aggregation.get('pragmatist_threshold', 0.55)
        threshold_architect = self.aggregation.get('architect_threshold', 0.45)

        if pragmatist_norm >= threshold_pragmatist:
            net_direction = 'pragmatist'
        elif architect_norm >= (1 - threshold_architect):
            net_direction = 'architect'
        else:
            net_direction = 'neutral'

        net_strength = abs(pragmatist_norm - architect_norm)

        # Calculate prior adjustment
        max_adjustment = self.aggregation.get('max_adjustment', 0.25)
        if net_direction == 'pragmatist':
            recommended_adjustment = -min(net_strength * 0.5, max_adjustment)
        elif net_direction == 'architect':
            recommended_adjustment = min(net_strength * 0.5, max_adjustment)
        else:
            recommended_adjustment = 0.0

        return DebtProxyAnalysis(
            bank_id=bank_id,
            bank_name=bank_name,
            signals=signals,
            pragmatist_score=round(pragmatist_score, 2),
            architect_score=round(architect_score, 2),
            net_direction=net_direction,
            net_strength=round(net_strength, 2),
            recommended_prior_adjustment=round(recommended_adjustment, 3),
            contributing_signals=contributing
        )

    def batch_analyze(
        self,
        phase: Optional[int] = None
    ) -> List[DebtProxyAnalysis]:
        """Analyze all banks in a phase."""
        results = []
        banks = self.bank_manifest.get('banks', [])

        if phase:
            banks = [b for b in banks if b.get('phase') == phase]

        for bank_data in banks:
            bank_id = bank_data.get('bank_id', bank_data.get('id'))
            if not bank_id:
                continue

            analysis = self.analyze_bank(bank_id, phase)
            if analysis.signals:  # Only include banks with detected signals
                results.append(analysis)

        return results


def format_debt_analysis(analysis: DebtProxyAnalysis) -> str:
    """Format debt analysis as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"Technical Debt Proxy Analysis: {analysis.bank_name}")
    lines.append(f"{'='*60}")
    lines.append(f"Signals Detected: {len(analysis.signals)}")
    lines.append(f"PRAGMATIST Score: {analysis.pragmatist_score:.2f}")
    lines.append(f"ARCHITECT Score: {analysis.architect_score:.2f}")
    lines.append(f"Net Direction: {analysis.net_direction.upper()}")
    lines.append(f"Net Strength: {analysis.net_strength:.2f}")
    lines.append(f"Recommended Prior Adjustment: {analysis.recommended_prior_adjustment:+.3f}")

    if analysis.signals:
        lines.append("\nDetected Signals:")
        for signal in analysis.signals:
            direction_icon = "[-]" if signal.direction == 'pragmatist' else "[+]"
            lines.append(f"  {direction_icon} {signal.description}")
            lines.append(f"      Weight: {signal.weight:.2f}, Category: {signal.category}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze technical debt proxies for PRAGMATIST likelihood',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --bank deutsche-bank --analyze
  %(prog)s --bank hsbc --scan-job-postings
  %(prog)s --phase 1 --batch-analyze
        """
    )

    # Scope options
    parser.add_argument('--bank', metavar='BANK_ID',
                       help='Analyze specific bank')
    parser.add_argument('--phase', type=int, metavar='N',
                       help='Phase number for batch analysis')

    # Analysis options
    parser.add_argument('--analyze', action='store_true',
                       help='Full proxy analysis')
    parser.add_argument('--scan-job-postings', action='store_true',
                       help='Focus on job posting proxies')
    parser.add_argument('--batch-analyze', action='store_true',
                       help='Analyze all banks in phase')

    # Output options
    parser.add_argument('--output', metavar='FILE',
                       help='Output file path')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')

    args = parser.parse_args()

    # Validate arguments
    if not any([args.bank, args.batch_analyze]):
        parser.print_help()
        sys.exit(1)

    analyzer = DebtProxyAnalyzer()

    # Analyze specific bank
    if args.bank:
        analysis = analyzer.analyze_bank(args.bank, args.phase)

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(
                json.dumps(analysis.to_dict(), indent=2),
                encoding='utf-8'
            )
            print(f"Report saved to: {args.output}")
        elif args.json:
            print(json.dumps(analysis.to_dict(), indent=2))
        else:
            print(format_debt_analysis(analysis))
        return

    # Batch analyze
    if args.batch_analyze:
        results = analyzer.batch_analyze(args.phase)

        if args.json:
            print(json.dumps([a.to_dict() for a in results], indent=2))
        else:
            print(f"\nTechnical Debt Proxy Analysis")
            print(f"Phase: {args.phase or 'All'}")
            print(f"Banks with Signals: {len(results)}")
            print("=" * 60)

            if not results:
                print("No technical debt signals detected.")
            for analysis in results:
                print(format_debt_analysis(analysis))


if __name__ == '__main__':
    main()
