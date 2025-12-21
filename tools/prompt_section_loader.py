"""
Prompt Section Loader - Extracts tagged sections from static prompts.

Ensures prompt_assembler.py uses static prompts as the single source of truth.
Sections are tagged with HTML comments: <!-- @section:name --> ... <!-- @endsection -->

Usage:
    loader = PromptSectionLoader(Path("config/agent-prompts"))
    role_section = loader.get_section("evidence-gatherer", "role")
    multiple = loader.get_sections("evidence-gatherer", ["role", "output_format"])
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, Optional, List, Any
from functools import lru_cache
from dataclasses import dataclass

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class PromptMetadata:
    """Metadata extracted from prompt frontmatter."""
    prompt_id: str
    version: str
    last_updated: str
    dependencies: List[str]
    compatible_with: Dict[str, str]
    deprecated_sections: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'PromptMetadata':
        return cls(
            prompt_id=data.get('prompt_id', 'unknown'),
            version=data.get('version', '0.0-00000000'),
            last_updated=data.get('last_updated', ''),
            dependencies=data.get('dependencies', []),
            compatible_with=data.get('compatible_with', {}),
            deprecated_sections=data.get('deprecated_sections', [])
        )


class PromptSectionLoader:
    """
    Loads and caches prompt sections from static markdown files.

    Supports:
    - Section extraction via <!-- @section:name --> tags
    - YAML frontmatter parsing for metadata
    - LRU caching for performance
    - Validation of required sections
    """

    SECTION_PATTERN = re.compile(
        r'<!-- @section:(\w+) -->\s*\n(.*?)<!-- @endsection -->',
        re.DOTALL
    )

    FRONTMATTER_PATTERN = re.compile(
        r'^---\s*\n(.*?)\n---\s*\n',
        re.DOTALL
    )

    def __init__(self, prompts_dir: Path, config_dir: Path = None):
        """
        Initialize the section loader.

        Args:
            prompts_dir: Path to config/agent-prompts/
            config_dir: Path to config/ (for loading search-templates.json, etc.)
        """
        self.prompts_dir = Path(prompts_dir)
        self.config_dir = config_dir or self.prompts_dir.parent
        self._section_cache: Dict[str, Dict[str, str]] = {}
        self._metadata_cache: Dict[str, PromptMetadata] = {}
        self._search_templates: Optional[Dict] = None

    @lru_cache(maxsize=20)
    def load_prompt(self, agent_name: str) -> str:
        """
        Load full prompt file content.

        Args:
            agent_name: Name of the agent (e.g., 'evidence-gatherer')

        Returns:
            Full file content as string

        Raises:
            FileNotFoundError: If prompt file doesn't exist
        """
        path = self.prompts_dir / f"{agent_name}.md"
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")
        return path.read_text(encoding='utf-8')

    def get_metadata(self, agent_name: str) -> Optional[PromptMetadata]:
        """
        Extract YAML frontmatter metadata from a prompt.

        Args:
            agent_name: Name of the agent

        Returns:
            PromptMetadata object or None if no frontmatter
        """
        if agent_name in self._metadata_cache:
            return self._metadata_cache[agent_name]

        content = self.load_prompt(agent_name)
        match = self.FRONTMATTER_PATTERN.match(content)

        if not match:
            return None

        if not YAML_AVAILABLE:
            logger.warning("PyYAML not available, cannot parse frontmatter")
            return None

        try:
            data = yaml.safe_load(match.group(1))
            metadata = PromptMetadata.from_dict(data)
            self._metadata_cache[agent_name] = metadata
            return metadata
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse frontmatter for {agent_name}: {e}")
            return None

    def get_section(self, agent_name: str, section_name: str) -> Optional[str]:
        """
        Extract a specific section from a prompt.

        Args:
            agent_name: Name of the agent (e.g., 'evidence-gatherer')
            section_name: Name of the section (e.g., 'role', 'tier1_searches')

        Returns:
            Section content or None if not found
        """
        if agent_name not in self._section_cache:
            content = self.load_prompt(agent_name)
            self._section_cache[agent_name] = self._parse_sections(content)

        section = self._section_cache[agent_name].get(section_name)

        if section is None:
            logger.warning(f"Section '{section_name}' not found in {agent_name}")

        return section

    def get_sections(self, agent_name: str, section_names: List[str],
                     separator: str = "\n\n---\n\n") -> str:
        """
        Combine multiple sections from a prompt.

        Args:
            agent_name: Name of the agent
            section_names: List of section names to extract
            separator: String to join sections with

        Returns:
            Combined sections as single string
        """
        sections = []
        for name in section_names:
            section = self.get_section(agent_name, name)
            if section:
                sections.append(section.strip())
        return separator.join(sections)

    def get_all_sections(self, agent_name: str) -> Dict[str, str]:
        """
        Get all sections from a prompt.

        Args:
            agent_name: Name of the agent

        Returns:
            Dictionary of section_name -> content
        """
        if agent_name not in self._section_cache:
            content = self.load_prompt(agent_name)
            self._section_cache[agent_name] = self._parse_sections(content)
        return self._section_cache[agent_name].copy()

    def list_sections(self, agent_name: str) -> List[str]:
        """
        List all available sections in a prompt.

        Args:
            agent_name: Name of the agent

        Returns:
            List of section names
        """
        sections = self.get_all_sections(agent_name)
        return list(sections.keys())

    def _parse_sections(self, content: str) -> Dict[str, str]:
        """
        Parse all section tags from content.

        Args:
            content: Full prompt content

        Returns:
            Dictionary of section_name -> content
        """
        sections = {}
        for match in self.SECTION_PATTERN.finditer(content):
            section_name = match.group(1)
            section_content = match.group(2).strip()
            sections[section_name] = section_content
        return sections

    def validate_sections(self, agent_name: str, required: List[str]) -> List[str]:
        """
        Check if all required sections exist.

        Args:
            agent_name: Name of the agent
            required: List of required section names

        Returns:
            List of missing section names
        """
        available = set(self.list_sections(agent_name))
        return [s for s in required if s not in available]

    def get_prompt_without_frontmatter(self, agent_name: str) -> str:
        """
        Get prompt content with frontmatter stripped.

        Args:
            agent_name: Name of the agent

        Returns:
            Prompt content without YAML frontmatter
        """
        content = self.load_prompt(agent_name)
        return self.FRONTMATTER_PATTERN.sub('', content)

    # External reference loading methods

    def load_search_templates(self) -> Dict[str, Any]:
        """
        Load search templates from external JSON file.

        Returns:
            Search templates dictionary
        """
        if self._search_templates is not None:
            return self._search_templates

        templates_path = self.config_dir / "search-templates.json"
        if not templates_path.exists():
            logger.warning(f"Search templates not found: {templates_path}")
            return {}

        with open(templates_path, 'r', encoding='utf-8') as f:
            self._search_templates = json.load(f)

        return self._search_templates

    def get_tier_searches(self, tier: int, bank_name: str,
                          bank_domain: str = "", regulator: str = "",
                          year: int = 2024) -> str:
        """
        Generate tier-specific search queries with bank context.

        Args:
            tier: Evidence tier (1, 2, or 3)
            bank_name: Name of the bank
            bank_domain: Bank's primary domain
            regulator: Primary regulator domain
            year: Current/target year

        Returns:
            Formatted search queries as markdown string
        """
        templates = self.load_search_templates()
        tier_key = f"tier{tier}"

        if tier_key not in templates:
            return f"[No templates found for tier {tier}]"

        tier_templates = templates[tier_key]
        searches = []

        for category, config in tier_templates.items():
            if category == "description":
                continue

            queries = config.get("queries", config) if isinstance(config, dict) else config
            if not isinstance(queries, list):
                continue

            category_title = category.replace("_", " ").title()
            searches.append(f"### {category_title}")
            searches.append("```")

            for query in queries:
                formatted = query.replace("[BANK]", bank_name)
                formatted = formatted.replace("[DOMAIN]", bank_domain)
                formatted = formatted.replace("[REGULATOR]", regulator)
                formatted = formatted.replace("[YEAR]", str(year))
                formatted = formatted.replace("[YEAR-1]", str(year - 1))
                searches.append(formatted)

            searches.append("```")
            searches.append("")

        return "\n".join(searches)

    def load_reference(self, reference_name: str) -> str:
        """
        Load an external reference file.

        Args:
            reference_name: Name of reference file (without path)

        Returns:
            Reference file content
        """
        ref_path = self.prompts_dir / "references" / reference_name
        if not ref_path.exists():
            # Try with .md extension
            ref_path = self.prompts_dir / "references" / f"{reference_name}.md"

        if not ref_path.exists():
            logger.warning(f"Reference file not found: {reference_name}")
            return f"[Reference {reference_name} not found]"

        return ref_path.read_text(encoding='utf-8')

    def clear_cache(self):
        """Clear all cached data."""
        self.load_prompt.cache_clear()
        self._section_cache.clear()
        self._metadata_cache.clear()
        self._search_templates = None


def main():
    """CLI interface for testing section loading."""
    import argparse

    parser = argparse.ArgumentParser(description="Prompt Section Loader")
    parser.add_argument("--agent", required=True, help="Agent name")
    parser.add_argument("--section", help="Section to extract")
    parser.add_argument("--list", action="store_true", help="List all sections")
    parser.add_argument("--metadata", action="store_true", help="Show metadata")
    parser.add_argument("--prompts-dir", default="config/agent-prompts",
                        help="Path to prompts directory")

    args = parser.parse_args()

    loader = PromptSectionLoader(Path(args.prompts_dir))

    try:
        if args.list:
            sections = loader.list_sections(args.agent)
            print(f"Sections in {args.agent}:")
            for s in sections:
                print(f"  - {s}")
        elif args.metadata:
            meta = loader.get_metadata(args.agent)
            if meta:
                print(f"Metadata for {args.agent}:")
                print(f"  Version: {meta.version}")
                print(f"  Last Updated: {meta.last_updated}")
                print(f"  Dependencies: {meta.dependencies}")
            else:
                print(f"No metadata found for {args.agent}")
        elif args.section:
            content = loader.get_section(args.agent, args.section)
            if content:
                print(content)
            else:
                print(f"Section '{args.section}' not found")
        else:
            print("Specify --section, --list, or --metadata")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
