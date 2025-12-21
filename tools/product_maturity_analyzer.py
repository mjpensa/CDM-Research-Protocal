#!/usr/bin/env python3
"""
Product Maturity Analyzer

Analyzes evidence to determine per-product-line CDM maturity.
Domain experts know banks may be ARCHITECT for IRS but PRAGMATIST for CDS.
This tool enables granular product-level classification.

Usage:
    python tools/product_maturity_analyzer.py --bank deutsche-bank --phase 1
    python tools/product_maturity_analyzer.py --phase 1 --batch --output product-maturity-report.json
    python tools/product_maturity_analyzer.py --bank hsbc --product IRS
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CONFIG_DIR = PROJECT_ROOT / "config"

# Product weights by regulatory importance
PRODUCT_WEIGHTS = {
    "IRS": 0.35,           # Core EMIR/CFTC scope
    "CDS": 0.25,           # EMIR/CFTC, high complexity
    "FX_Forwards": 0.15,   # EMIR Phase 5
    "FX_Options": 0.05,    # Less common
    "Equity_Swaps": 0.05,  # Part of equity derivatives
    "Equity_Options": 0.05,# Part of equity derivatives
    "Commodities": 0.05,   # Commodity derivatives
    "Structured_Products": 0.02,
    "Repo": 0.02,
    "ETD": 0.01            # Exchange-traded, less CDM focus
}

# Claim type to maturity score mapping
CLAIM_TYPE_SCORES = {
    "production_usage": 5,
    "pilot_or_poc": 3,
    "open_source_contribution": 2,
    "vendor_proxy_signal": 2,
    "membership_or_participation": 1,
    "hiring_signal": 1
}

# Maturity score to classification mapping
MATURITY_THRESHOLDS = {
    5: "ARCHITECT",
    3: "ARCHITECT",  # Pilot indicates active pursuit
    2: "PRAGMATIST",
    1: "OBSERVER",
    0: "UNKNOWN"
}


@dataclass
class ProductMaturity:
    """Per-product CDM maturity assessment."""
    product: str
    classification: str  # ARCHITECT, PRAGMATIST, OBSERVER, UNKNOWN
    confidence: float
    evidence_count: int
    highest_claim_type: Optional[str]
    maturity_score: int
    regulatory_driver: Optional[str]
    evidence_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CompositeClassification:
    """Bank-level composite classification from product breakdown."""
    bank_id: str
    bank_name: str
    overall_classification: str
    overall_confidence: float
    weighted_maturity_score: float
    product_breakdown: Dict[str, ProductMaturity]
    primary_product: str  # Highest maturity product
    regulatory_alignment: float  # How well product focus matches mandate scope
    products_with_evidence: int
    products_without_evidence: int
    analysis_date: str

    def to_dict(self) -> dict:
        result = {
            "bank_id": self.bank_id,
            "bank_name": self.bank_name,
            "overall_classification": self.overall_classification,
            "overall_confidence": self.overall_confidence,
            "weighted_maturity_score": self.weighted_maturity_score,
            "primary_product": self.primary_product,
            "regulatory_alignment": self.regulatory_alignment,
            "products_with_evidence": self.products_with_evidence,
            "products_without_evidence": self.products_without_evidence,
            "analysis_date": self.analysis_date,
            "product_breakdown": {
                k: v.to_dict() for k, v in self.product_breakdown.items()
            }
        }
        return result


class ProductMaturityAnalyzer:
    """Analyzes per-product CDM maturity from evidence."""

    def __init__(self):
        self.regulatory_calendar = self._load_regulatory_calendar()

    def _load_regulatory_calendar(self) -> dict:
        """Load regulatory calendar for driver mapping."""
        path = CONFIG_DIR / "regulatory-calendar.json"
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"active_mandates": []}

    def load_evidence(self, bank_id: str, phase: int) -> Optional[dict]:
        """Load evidence.json for a bank."""
        # Try to find the bank in phase directories
        phase_dirs = list(OUTPUTS_DIR.glob(f"phase-{phase}-*"))

        for phase_dir in phase_dirs:
            evidence_path = phase_dir / bank_id / "evidence.json"
            if evidence_path.exists():
                with open(evidence_path, 'r', encoding='utf-8') as f:
                    return json.load(f)

        # Try direct path
        evidence_path = OUTPUTS_DIR / f"phase-{phase}" / bank_id / "evidence.json"
        if evidence_path.exists():
            with open(evidence_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        return None

    def extract_product_mentions(self, evidence_item: dict) -> List[str]:
        """Extract products mentioned in an evidence item."""
        # First check explicit product_scope
        products = evidence_item.get('product_scope', [])
        if products:
            return products

        # Infer from claim text if not explicit
        claim = evidence_item.get('claim', '').lower()
        inferred = []

        product_keywords = {
            'IRS': ['interest rate swap', 'irs', 'interest rate derivative', 'rates'],
            'CDS': ['credit default swap', 'cds', 'credit derivative'],
            'FX_Forwards': ['fx forward', 'foreign exchange', 'fx derivative', 'currency'],
            'FX_Options': ['fx option', 'currency option'],
            'Equity_Swaps': ['equity swap', 'equity derivative', 'stock swap'],
            'Equity_Options': ['equity option', 'stock option'],
            'Commodities': ['commodity', 'commodities derivative'],
            'Repo': ['repo', 'repurchase agreement'],
            'ETD': ['exchange traded', 'etd', 'listed derivative']
        }

        for product, keywords in product_keywords.items():
            if any(kw in claim for kw in keywords):
                inferred.append(product)

        return inferred

    def get_regulatory_driver(self, product: str, jurisdictions: List[str] = None) -> Optional[str]:
        """Determine primary regulatory driver for a product."""
        # Map products to common regulatory drivers
        product_drivers = {
            'IRS': 'EMIR_Refit',
            'CDS': 'EMIR_Refit',
            'FX_Forwards': 'EMIR_Refit',
            'FX_Options': 'EMIR_Refit',
            'Equity_Swaps': 'EMIR_Refit',
            'Equity_Options': 'EMIR_Refit',
            'Commodities': 'EMIR_Refit',
            'Repo': 'SFTR',
            'ETD': 'MiFID'
        }

        # Check for jurisdiction-specific overrides
        if jurisdictions:
            if 'Japan' in jurisdictions and product == 'IRS':
                return 'JSCC'
            if 'US' in jurisdictions and product in ['IRS', 'CDS']:
                return 'CFTC_Rewrite'

        return product_drivers.get(product)

    def calculate_product_maturity(
        self,
        product: str,
        evidence_items: List[dict]
    ) -> ProductMaturity:
        """Calculate maturity for a specific product."""
        # Filter evidence for this product
        product_evidence = []
        for item in evidence_items:
            products = self.extract_product_mentions(item)
            if product in products or not products:  # Include general CDM evidence
                product_evidence.append(item)

        if not product_evidence:
            return ProductMaturity(
                product=product,
                classification="UNKNOWN",
                confidence=0.0,
                evidence_count=0,
                highest_claim_type=None,
                maturity_score=0,
                regulatory_driver=self.get_regulatory_driver(product),
                evidence_ids=[]
            )

        # Find highest claim type
        highest_score = 0
        highest_claim = None
        evidence_ids = []
        jurisdictions = []

        for item in product_evidence:
            claim_type = item.get('claim_type', '')
            score = CLAIM_TYPE_SCORES.get(claim_type, 0)
            if score > highest_score:
                highest_score = score
                highest_claim = claim_type
            evidence_ids.append(item.get('id', 'unknown'))
            jurisdictions.extend(item.get('jurisdiction_scope', []))

        # Determine classification
        classification = MATURITY_THRESHOLDS.get(highest_score, "UNKNOWN")

        # Calculate confidence based on evidence count and tier mix
        tier_weights = {1: 1.0, 2: 0.75, 3: 0.5}
        weighted_count = sum(
            tier_weights.get(item.get('tier', 3), 0.5)
            for item in product_evidence
        )
        confidence = min(95, 30 + (weighted_count * 10))  # Cap at 95%

        return ProductMaturity(
            product=product,
            classification=classification,
            confidence=confidence,
            evidence_count=len(product_evidence),
            highest_claim_type=highest_claim,
            maturity_score=highest_score,
            regulatory_driver=self.get_regulatory_driver(product, list(set(jurisdictions))),
            evidence_ids=evidence_ids
        )

    def generate_product_matrix(self, evidence_data: dict) -> Dict[str, ProductMaturity]:
        """Generate maturity matrix for all products."""
        evidence_items = evidence_data.get('evidence_items', [])
        matrix = {}

        for product in PRODUCT_WEIGHTS.keys():
            matrix[product] = self.calculate_product_maturity(product, evidence_items)

        return matrix

    def calculate_composite_classification(
        self,
        bank_id: str,
        bank_name: str,
        product_matrix: Dict[str, ProductMaturity]
    ) -> CompositeClassification:
        """Calculate composite bank classification from product matrix."""
        # Calculate weighted maturity score
        weighted_score = 0.0
        total_weight = 0.0

        for product, maturity in product_matrix.items():
            weight = PRODUCT_WEIGHTS.get(product, 0.05)
            weighted_score += maturity.maturity_score * weight
            total_weight += weight

        if total_weight > 0:
            weighted_score = weighted_score / total_weight

        # Determine overall classification
        if weighted_score >= 4.0:
            overall_class = "ARCHITECT"
        elif weighted_score >= 2.5:
            overall_class = "ARCHITECT"  # Active adoption
        elif weighted_score >= 1.5:
            overall_class = "PRAGMATIST"
        elif weighted_score >= 0.5:
            overall_class = "OBSERVER"
        else:
            overall_class = "UNKNOWN"

        # Find primary product (highest maturity)
        primary_product = max(
            product_matrix.items(),
            key=lambda x: (x[1].maturity_score, x[1].confidence)
        )[0]

        # Calculate regulatory alignment
        # (how well evidence aligns with regulatory-important products)
        products_with_evidence = sum(
            1 for m in product_matrix.values() if m.evidence_count > 0
        )
        products_without = len(product_matrix) - products_with_evidence

        # Regulatory alignment: evidence in high-weight products
        aligned_weight = sum(
            PRODUCT_WEIGHTS.get(p, 0) for p, m in product_matrix.items()
            if m.evidence_count > 0
        )
        regulatory_alignment = aligned_weight / sum(PRODUCT_WEIGHTS.values())

        # Overall confidence
        confidences = [m.confidence for m in product_matrix.values() if m.evidence_count > 0]
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return CompositeClassification(
            bank_id=bank_id,
            bank_name=bank_name,
            overall_classification=overall_class,
            overall_confidence=overall_confidence,
            weighted_maturity_score=weighted_score,
            product_breakdown=product_matrix,
            primary_product=primary_product,
            regulatory_alignment=regulatory_alignment,
            products_with_evidence=products_with_evidence,
            products_without_evidence=products_without,
            analysis_date=datetime.now(timezone.utc).isoformat()
        )

    def analyze_bank(self, bank_id: str, phase: int) -> Optional[CompositeClassification]:
        """Full analysis for a single bank."""
        evidence_data = self.load_evidence(bank_id, phase)
        if not evidence_data:
            logger.warning(f"No evidence found for {bank_id} in phase {phase}")
            return None

        bank_name = evidence_data.get('bank_name', bank_id)
        product_matrix = self.generate_product_matrix(evidence_data)
        return self.calculate_composite_classification(bank_id, bank_name, product_matrix)

    def analyze_phase_batch(self, phase: int) -> List[CompositeClassification]:
        """Analyze all banks in a phase."""
        results = []
        phase_dirs = list(OUTPUTS_DIR.glob(f"phase-{phase}-*"))

        for phase_dir in phase_dirs:
            for bank_dir in phase_dir.iterdir():
                if bank_dir.is_dir() and (bank_dir / "evidence.json").exists():
                    bank_id = bank_dir.name
                    result = self.analyze_bank(bank_id, phase)
                    if result:
                        results.append(result)

        return results

    def generate_report(
        self,
        results: List[CompositeClassification],
        output_path: Optional[Path] = None
    ) -> dict:
        """Generate analysis report."""
        report = {
            "report_type": "product_maturity_analysis",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_banks_analyzed": len(results),
            "summary": {
                "architect_count": sum(1 for r in results if r.overall_classification == "ARCHITECT"),
                "pragmatist_count": sum(1 for r in results if r.overall_classification == "PRAGMATIST"),
                "observer_count": sum(1 for r in results if r.overall_classification == "OBSERVER"),
                "unknown_count": sum(1 for r in results if r.overall_classification == "UNKNOWN")
            },
            "product_coverage": {},
            "banks": [r.to_dict() for r in results]
        }

        # Calculate product coverage across all banks
        for product in PRODUCT_WEIGHTS.keys():
            banks_with_evidence = sum(
                1 for r in results
                if r.product_breakdown.get(product) and r.product_breakdown[product].evidence_count > 0
            )
            report["product_coverage"][product] = {
                "banks_with_evidence": banks_with_evidence,
                "coverage_rate": banks_with_evidence / len(results) if results else 0
            }

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Report saved to {output_path}")

        return report


def format_product_matrix(result: CompositeClassification) -> str:
    """Format product matrix for display."""
    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"PRODUCT MATURITY ANALYSIS: {result.bank_name}")
    lines.append(f"{'='*70}")
    lines.append(f"\nOverall Classification: {result.overall_classification}")
    lines.append(f"Overall Confidence: {result.overall_confidence:.1f}%")
    lines.append(f"Weighted Maturity Score: {result.weighted_maturity_score:.2f}")
    lines.append(f"Primary Product: {result.primary_product}")
    lines.append(f"Regulatory Alignment: {result.regulatory_alignment:.1%}")

    lines.append(f"\n{'Product':<20} {'Classification':<15} {'Score':<6} {'Evidence':<10} {'Driver':<15}")
    lines.append("-" * 70)

    for product, maturity in sorted(
        result.product_breakdown.items(),
        key=lambda x: PRODUCT_WEIGHTS.get(x[0], 0),
        reverse=True
    ):
        lines.append(
            f"{product:<20} {maturity.classification:<15} {maturity.maturity_score:<6} "
            f"{maturity.evidence_count:<10} {maturity.regulatory_driver or 'N/A':<15}"
        )

    lines.append(f"\nProducts with evidence: {result.products_with_evidence}")
    lines.append(f"Products without evidence: {result.products_without_evidence}")
    lines.append(f"Analysis date: {result.analysis_date}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze per-product CDM maturity',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --bank deutsche-bank --phase 1
  %(prog)s --phase 1 --batch --output product-maturity-report.json
  %(prog)s --bank hsbc --product IRS
        """
    )

    parser.add_argument('--bank', metavar='BANK_ID',
                       help='Bank ID to analyze')
    parser.add_argument('--phase', type=int, default=1,
                       help='Phase number (default: 1)')
    parser.add_argument('--product', metavar='PRODUCT',
                       help='Analyze specific product only')
    parser.add_argument('--batch', action='store_true',
                       help='Analyze all banks in phase')
    parser.add_argument('--output', metavar='FILE',
                       help='Output report to JSON file')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')

    args = parser.parse_args()

    analyzer = ProductMaturityAnalyzer()

    if args.batch:
        # Batch analysis
        results = analyzer.analyze_phase_batch(args.phase)

        if not results:
            print(f"No banks found in phase {args.phase}")
            sys.exit(1)

        if args.output:
            report = analyzer.generate_report(results, Path(args.output))
        else:
            report = analyzer.generate_report(results)

        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"\nAnalyzed {len(results)} banks in phase {args.phase}")
            print(f"ARCHITECT: {report['summary']['architect_count']}")
            print(f"PRAGMATIST: {report['summary']['pragmatist_count']}")
            print(f"OBSERVER: {report['summary']['observer_count']}")
            print(f"UNKNOWN: {report['summary']['unknown_count']}")

            if args.output:
                print(f"\nFull report saved to: {args.output}")

    elif args.bank:
        # Single bank analysis
        result = analyzer.analyze_bank(args.bank, args.phase)

        if not result:
            print(f"Could not analyze {args.bank} in phase {args.phase}")
            sys.exit(1)

        if args.product:
            # Single product focus
            if args.product in result.product_breakdown:
                maturity = result.product_breakdown[args.product]
                if args.json:
                    print(json.dumps(maturity.to_dict(), indent=2))
                else:
                    print(f"\n{args.product} Maturity for {result.bank_name}:")
                    print(f"  Classification: {maturity.classification}")
                    print(f"  Confidence: {maturity.confidence:.1f}%")
                    print(f"  Evidence Count: {maturity.evidence_count}")
                    print(f"  Highest Claim: {maturity.highest_claim_type}")
                    print(f"  Regulatory Driver: {maturity.regulatory_driver}")
            else:
                print(f"Product {args.product} not found")
                sys.exit(1)
        else:
            # Full product matrix
            if args.json:
                print(json.dumps(result.to_dict(), indent=2))
            else:
                print(format_product_matrix(result))

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, indent=2)
            print(f"\nSaved to: {args.output}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
