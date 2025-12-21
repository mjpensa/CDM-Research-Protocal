#!/usr/bin/env python3
"""
Relationship Analyzer Tool

Analyzes entity relationship graph to infer adoption pressure and network effects.
Calculates pressure vectors based on bank relationships with vendors, CCPs, and peers.

Usage:
    python relationship_analyzer.py --bank deutsche-bank
    python relationship_analyzer.py --phase 1 --flag-exposure 0.5
    python relationship_analyzer.py --export-graph --output relationship_graph.json
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field, asdict
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

# Import config loader
sys.path.insert(0, str(SCRIPT_DIR))
from config_loader import (
    load_relationships,
    load_bank_manifest,
    get_bank_relationships,
    get_entity_info,
    load_regulatory_calendar,
    get_bank_vendor_depth,
    get_depth_classification_impact,
    get_bank_mandate_exposure
)


@dataclass
class PressureVector:
    """Represents net adoption pressure on a bank."""
    bank_id: str
    architect_pressure: float
    pragmatist_pressure: float
    net_direction: str  # ARCHITECT, PRAGMATIST, NEUTRAL
    net_strength: float
    confidence: float
    contributing_relationships: List[str]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'PressureVector':
        return cls(**data)


@dataclass
class NetworkMetrics:
    """Network analysis metrics for a bank."""
    bank_id: str
    degree_centrality: int
    architect_exposure: float
    pragmatist_exposure: float
    ccp_connectivity: int
    vendor_dependency: float
    mandatory_cdm_pressure: bool
    pressure_vector: PressureVector

    def to_dict(self) -> dict:
        result = asdict(self)
        result['pressure_vector'] = self.pressure_vector.to_dict()
        return result


class RelationshipAnalyzer:
    """Analyzes entity relationships for adoption pressure inference."""

    def __init__(self):
        self.relationships_data = load_relationships()
        self.bank_manifest = load_bank_manifest()
        self.regulatory_calendar = load_regulatory_calendar()
        self.relationship_types = self.relationships_data.get('relationship_types', {})

    def get_bank_relationships(self, bank_id: str) -> List[dict]:
        """Get all relationships for a bank."""
        return get_bank_relationships(bank_id)

    def calculate_pressure_from_relationship(self, relationship: dict) -> tuple[float, float]:
        """
        Calculate ARCHITECT and PRAGMATIST pressure from a single relationship.

        Returns:
            (architect_pressure, pragmatist_pressure) as floats 0-1
        """
        rel_type = relationship.get('relationship_type', '')
        rel_config = self.relationship_types.get(rel_type, {})

        inferred = relationship.get('inferred_pressure', {})
        direction = inferred.get('direction', rel_config.get('default_pressure', 'neutral'))
        strength = inferred.get('strength', rel_config.get('pressure_strength', 0.5))
        confidence = relationship.get('confidence', 0.5)

        # Adjust strength by confidence
        adjusted_strength = strength * confidence

        if direction == 'architect':
            return (adjusted_strength, 0.0)
        elif direction == 'pragmatist':
            return (0.0, adjusted_strength)
        elif direction == 'depends_on_ccp':
            # Check if CCP mandates CDM
            target = relationship.get('target_entity', '')
            ccp_info = get_entity_info(target, 'ccps')
            if ccp_info and ccp_info.get('cdm_mandate'):
                return (adjusted_strength, 0.0)
            return (0.0, 0.0)
        elif direction == 'depends_on_mandate':
            # Check regulatory calendar
            return (adjusted_strength * 0.5, 0.0)  # Assume moderate pressure
        else:
            return (0.0, 0.0)

    def calculate_pressure_vector(self, bank_id: str) -> PressureVector:
        """Calculate net pressure vector for a bank.

        Incorporates:
        - Relationship-based pressure (CCPs, vendors, peers)
        - Vendor CDM depth taxonomy (L0-L4) pressure adjustments
        """
        relationships = self.get_bank_relationships(bank_id)

        architect_total = 0.0
        pragmatist_total = 0.0
        contributing = []

        for rel in relationships:
            arch, prag = self.calculate_pressure_from_relationship(rel)
            if arch > 0 or prag > 0:
                architect_total += arch
                pragmatist_total += prag
                contributing.append(rel.get('id', 'unknown'))

        # Add vendor CDM depth pressure (Enhancement 2)
        vendor_depth_info = get_bank_vendor_depth(bank_id)
        if vendor_depth_info:
            depth_level = vendor_depth_info.get('depth_level', 'L0_none')
            depth_impact = get_depth_classification_impact(depth_level)

            if depth_impact:
                pressure_direction = depth_impact.get('pressure_direction', 'neutral')
                pressure_strength = depth_impact.get('pressure_strength', 0.0)

                # Apply vendor depth pressure (weighted by 0.5 to balance with relationship pressure)
                vendor_pressure_weight = 0.5
                adjusted_pressure = pressure_strength * vendor_pressure_weight

                if pressure_direction == 'architect':
                    architect_total += adjusted_pressure
                    contributing.append(f"vendor_depth_{depth_level}")
                elif pressure_direction == 'pragmatist':
                    pragmatist_total += adjusted_pressure
                    contributing.append(f"vendor_depth_{depth_level}")

        # Add regulatory mandate pressure (Enhancement 3)
        mandate_exposure = get_bank_mandate_exposure(bank_id)
        if mandate_exposure.get('mandate_count', 0) > 0:
            # Mandatory CDM = strong ARCHITECT pressure
            if mandate_exposure.get('has_mandatory_cdm'):
                architect_total += 0.8  # Strong mandatory pressure
                contributing.append("mandatory_cdm_mandate")
            else:
                # Non-mandatory mandates still create moderate pressure toward CDM
                total_mandate_pressure = mandate_exposure.get('total_pressure', 0.0)
                # Apply at 0.4 weight relative to other factors
                regulatory_pressure = total_mandate_pressure * 0.4
                if regulatory_pressure > 0:
                    architect_total += regulatory_pressure
                    strongest = mandate_exposure.get('strongest_mandate')
                    if strongest:
                        contributing.append(f"regulatory_{strongest.get('mandate_id', 'unknown')}")

        # Normalize
        total = architect_total + pragmatist_total
        if total > 0:
            architect_norm = architect_total / (total + 1)  # +1 to prevent extreme values
            pragmatist_norm = pragmatist_total / (total + 1)
        else:
            architect_norm = 0.0
            pragmatist_norm = 0.0

        # Determine direction
        net_strength = abs(architect_total - pragmatist_total)
        if architect_total > pragmatist_total * 1.2:
            net_direction = "ARCHITECT"
        elif pragmatist_total > architect_total * 1.2:
            net_direction = "PRAGMATIST"
        else:
            net_direction = "NEUTRAL"

        # Confidence based on number of relationships
        rel_count = len(relationships)
        if rel_count >= 5:
            confidence = 0.8
        elif rel_count >= 3:
            confidence = 0.6
        elif rel_count >= 1:
            confidence = 0.4
        else:
            confidence = 0.2

        return PressureVector(
            bank_id=bank_id,
            architect_pressure=architect_norm,
            pragmatist_pressure=pragmatist_norm,
            net_direction=net_direction,
            net_strength=net_strength,
            confidence=confidence,
            contributing_relationships=contributing
        )

    def calculate_network_metrics(self, bank_id: str) -> NetworkMetrics:
        """Calculate comprehensive network metrics for a bank."""
        relationships = self.get_bank_relationships(bank_id)
        pressure_vector = self.calculate_pressure_vector(bank_id)

        # Count relationship types
        ccp_count = 0
        vendor_strength = 0.0
        architect_exposure = 0.0
        pragmatist_exposure = 0.0
        mandatory_cdm = False

        for rel in relationships:
            rel_type = rel.get('relationship_type', '')
            target_type = rel.get('target_type', '')

            if rel_type == 'ccp_connectivity' or target_type == 'ccp':
                ccp_count += 1
                # Check if CCP mandates CDM
                target = rel.get('target_entity', '')
                ccp_info = get_entity_info(target, 'ccps')
                if ccp_info and ccp_info.get('cdm_mandate'):
                    mandatory_cdm = True
                    architect_exposure += rel.get('confidence', 0.5)

            if rel_type == 'vendor_partnership' or target_type == 'vendor':
                vendor_strength += rel.get('confidence', 0.5)
                pragmatist_exposure += rel.get('confidence', 0.5) * 0.5

            if rel_type == 'finos_contributor':
                architect_exposure += rel.get('confidence', 0.5)

            if rel_type == 'peer_adoption':
                architect_exposure += rel.get('confidence', 0.5) * 0.3

        return NetworkMetrics(
            bank_id=bank_id,
            degree_centrality=len(relationships),
            architect_exposure=min(architect_exposure, 1.0),
            pragmatist_exposure=min(pragmatist_exposure, 1.0),
            ccp_connectivity=ccp_count,
            vendor_dependency=min(vendor_strength, 1.0),
            mandatory_cdm_pressure=mandatory_cdm,
            pressure_vector=pressure_vector
        )

    def flag_high_architect_exposure(
        self,
        phase: Optional[int] = None,
        threshold: float = 0.5
    ) -> List[dict]:
        """Flag banks with high ARCHITECT exposure."""
        flagged = []

        # Get banks to analyze
        banks = self.bank_manifest.get('banks', [])
        if phase:
            banks = [b for b in banks if b.get('phase') == phase]

        for bank_data in banks:
            bank_id = bank_data.get('bank_id', '')
            if not bank_id:
                continue

            metrics = self.calculate_network_metrics(bank_id)

            if metrics.architect_exposure >= threshold:
                flagged.append({
                    'bank_id': bank_id,
                    'bank_name': bank_data.get('bank_name', bank_id),
                    'architect_exposure': metrics.architect_exposure,
                    'mandatory_cdm': metrics.mandatory_cdm_pressure,
                    'pressure_direction': metrics.pressure_vector.net_direction,
                    'contributing_relationships': metrics.pressure_vector.contributing_relationships
                })

        return sorted(flagged, key=lambda x: x['architect_exposure'], reverse=True)

    def export_graph(self, output_path: Path) -> dict:
        """Export relationship graph in JSON format suitable for visualization."""
        nodes = []
        edges = []
        node_ids = set()

        relationships = self.relationships_data.get('relationships', [])
        entities = self.relationships_data.get('entities', {})

        # Add bank nodes
        for bank_data in self.bank_manifest.get('banks', []):
            bank_id = bank_data.get('bank_id', '')
            nodes.append({
                'id': bank_id,
                'label': bank_data.get('bank_name', bank_id),
                'type': 'bank',
                'phase': bank_data.get('phase')
            })
            node_ids.add(bank_id)

        # Add entity nodes from relationships
        for rel in relationships:
            source = rel.get('source_entity', '')
            target = rel.get('target_entity', '')
            source_type = rel.get('source_type', 'unknown')
            target_type = rel.get('target_type', 'unknown')

            if source not in node_ids:
                nodes.append({
                    'id': source,
                    'label': source,
                    'type': source_type
                })
                node_ids.add(source)

            if target not in node_ids:
                # Try to get entity info
                entity_info = get_entity_info(target, target_type + 's')
                label = entity_info.get('name', target) if entity_info else target
                nodes.append({
                    'id': target,
                    'label': label,
                    'type': target_type
                })
                node_ids.add(target)

            # Add edge
            edges.append({
                'id': rel.get('id', f"{source}-{target}"),
                'source': source,
                'target': target,
                'relationship_type': rel.get('relationship_type', 'unknown'),
                'confidence': rel.get('confidence', 0.5),
                'pressure_direction': rel.get('inferred_pressure', {}).get('direction', 'neutral'),
                'pressure_strength': rel.get('inferred_pressure', {}).get('strength', 0.5)
            })

        graph = {
            'nodes': nodes,
            'edges': edges,
            'exported_at': datetime.now(timezone.utc).isoformat(),
            'node_count': len(nodes),
            'edge_count': len(edges)
        }

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(graph, f, indent=2)
            logger.info(f"Graph exported to {output_path}")

        return graph

    def generate_report(self, bank_id: str) -> str:
        """Generate markdown analysis report for a bank."""
        metrics = self.calculate_network_metrics(bank_id)
        relationships = self.get_bank_relationships(bank_id)

        lines = []
        lines.append(f"# Relationship Analysis: {bank_id}")
        lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")

        lines.append("## Network Metrics")
        lines.append(f"- **Degree Centrality**: {metrics.degree_centrality} relationships")
        lines.append(f"- **ARCHITECT Exposure**: {metrics.architect_exposure:.2f}")
        lines.append(f"- **PRAGMATIST Exposure**: {metrics.pragmatist_exposure:.2f}")
        lines.append(f"- **CCP Connectivity**: {metrics.ccp_connectivity}")
        lines.append(f"- **Vendor Dependency**: {metrics.vendor_dependency:.2f}")
        lines.append(f"- **Mandatory CDM Pressure**: {'Yes' if metrics.mandatory_cdm_pressure else 'No'}")
        lines.append("")

        lines.append("## Pressure Vector")
        pv = metrics.pressure_vector
        lines.append(f"- **Net Direction**: {pv.net_direction}")
        lines.append(f"- **Net Strength**: {pv.net_strength:.2f}")
        lines.append(f"- **Confidence**: {pv.confidence:.2f}")
        lines.append(f"- **ARCHITECT Pressure**: {pv.architect_pressure:.2f}")
        lines.append(f"- **PRAGMATIST Pressure**: {pv.pragmatist_pressure:.2f}")
        lines.append("")

        if pv.contributing_relationships:
            lines.append("## Contributing Relationships")
            for rel_id in pv.contributing_relationships:
                rel = next((r for r in relationships if r.get('id') == rel_id), None)
                if rel:
                    lines.append(f"- **{rel_id}**: {rel.get('relationship_type')} -> {rel.get('target_entity')}")
                    lines.append(f"  - Confidence: {rel.get('confidence', 0):.2f}")
                    lines.append(f"  - Pressure: {rel.get('inferred_pressure', {}).get('direction', 'unknown')}")
            lines.append("")

        if relationships:
            lines.append("## All Relationships")
            for rel in relationships:
                lines.append(f"\n### {rel.get('id', 'Unknown')}")
                lines.append(f"- Type: {rel.get('relationship_type')}")
                lines.append(f"- Target: {rel.get('target_entity')} ({rel.get('target_type')})")
                lines.append(f"- Confidence: {rel.get('confidence', 0):.2f}")
                if rel.get('notes'):
                    lines.append(f"- Notes: {rel.get('notes')}")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Relationship Analyzer for CDM adoption pressure inference',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --bank deutsche-bank
  %(prog)s --bank hsbc --report
  %(prog)s --phase 1 --flag-exposure 0.5
  %(prog)s --export-graph --output relationship_graph.json
        """
    )

    # Scope options
    parser.add_argument('--bank', metavar='BANK_ID',
                       help='Analyze specific bank')
    parser.add_argument('--phase', type=int, metavar='N',
                       help='Analyze banks in specific phase')
    parser.add_argument('--all', action='store_true',
                       help='Analyze all banks')

    # Analysis options
    parser.add_argument('--flag-exposure', type=float, metavar='THRESHOLD',
                       help='Flag banks with ARCHITECT exposure above threshold')
    parser.add_argument('--report', action='store_true',
                       help='Generate detailed markdown report')
    parser.add_argument('--export-graph', action='store_true',
                       help='Export relationship graph for visualization')

    # Output options
    parser.add_argument('--output', metavar='FILE',
                       help='Output file path')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')

    args = parser.parse_args()

    # Need at least one action
    if not any([args.bank, args.phase, args.all, args.flag_exposure, args.export_graph]):
        parser.print_help()
        sys.exit(1)

    analyzer = RelationshipAnalyzer()

    # Export graph
    if args.export_graph:
        output_path = Path(args.output) if args.output else PROJECT_ROOT / "outputs" / "state" / "relationship_graph.json"
        graph = analyzer.export_graph(output_path)
        print(f"Graph exported: {graph['node_count']} nodes, {graph['edge_count']} edges")
        return

    # Flag high exposure
    if args.flag_exposure is not None:
        flagged = analyzer.flag_high_architect_exposure(
            phase=args.phase,
            threshold=args.flag_exposure
        )

        if args.json:
            print(json.dumps(flagged, indent=2))
        else:
            print(f"\nBanks with ARCHITECT exposure >= {args.flag_exposure}:")
            if not flagged:
                print("  None found")
            for bank in flagged:
                mandatory = " [MANDATORY CDM]" if bank['mandatory_cdm'] else ""
                print(f"  {bank['bank_name']}: {bank['architect_exposure']:.2f}{mandatory}")
        return

    # Analyze specific bank
    if args.bank:
        if args.report:
            report = analyzer.generate_report(args.bank)
            if args.output:
                Path(args.output).write_text(report, encoding='utf-8')
                print(f"Report saved to {args.output}")
            else:
                print(report)
        else:
            metrics = analyzer.calculate_network_metrics(args.bank)

            if args.json:
                print(json.dumps(metrics.to_dict(), indent=2))
            else:
                print(f"\nNetwork Metrics for {args.bank}:")
                print(f"  Degree Centrality: {metrics.degree_centrality}")
                print(f"  ARCHITECT Exposure: {metrics.architect_exposure:.2f}")
                print(f"  PRAGMATIST Exposure: {metrics.pragmatist_exposure:.2f}")
                print(f"  CCP Connectivity: {metrics.ccp_connectivity}")
                print(f"  Vendor Dependency: {metrics.vendor_dependency:.2f}")
                print(f"  Mandatory CDM: {metrics.mandatory_cdm_pressure}")
                print(f"\nPressure Vector:")
                print(f"  Direction: {metrics.pressure_vector.net_direction}")
                print(f"  Confidence: {metrics.pressure_vector.confidence:.2f}")
        return

    # Analyze phase or all
    banks = analyzer.bank_manifest.get('banks', [])
    if args.phase:
        banks = [b for b in banks if b.get('phase') == args.phase]

    results = []
    for bank_data in banks:
        bank_id = bank_data.get('bank_id', '')
        if not bank_id:
            continue

        metrics = analyzer.calculate_network_metrics(bank_id)
        results.append(metrics.to_dict())

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\nAnalyzed {len(results)} banks:")
        for r in results:
            pv = r['pressure_vector']
            print(f"  {r['bank_id']}: {pv['net_direction']} (strength: {pv['net_strength']:.2f})")


if __name__ == '__main__':
    main()
