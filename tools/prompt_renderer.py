"""
CDM Research Protocol - Prompt Template Renderer v1.0

Injects configuration values into agent prompts using {{config.X}} placeholders.
This ensures agent prompts always use current threshold values from config.

Usage:
    from prompt_renderer import render_prompt
    content = render_prompt(Path('config/agent-prompts/orchestrator.md'))

    # Or render all prompts to a directory:
    python tools/prompt_renderer.py
"""

import re
import logging
from pathlib import Path

# Import config loader
try:
    from config_loader import (
        get_skip_threshold,
        get_low_confidence_block_threshold,
        get_confidence_caps,
        get_extreme_lr_bounds
    )
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    # Fallback defaults
    def get_skip_threshold(): return 80
    def get_low_confidence_block_threshold(): return 50
    def get_confidence_caps(): return {1: 95, 2: 75, 3: 50, 4: 35}
    def get_extreme_lr_bounds(): return (0.01, 100)

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_replacements() -> dict:
    """
    Build replacement dictionary from config.

    Returns:
        Dict mapping placeholder strings to their values
    """
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

    Replaces {{config.X}} placeholders with actual values from config.

    Args:
        template_path: Path to .md template file

    Returns:
        Rendered content with placeholders replaced
    """
    template_path = Path(template_path)

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    template = template_path.read_text(encoding='utf-8')

    # Replace all known placeholders
    for placeholder, value in get_replacements().items():
        template = template.replace(placeholder, value)

    # Warn about unreplaced placeholders
    remaining = re.findall(r'\{\{config\.[^}]+\}\}', template)
    if remaining:
        logger.warning(f"Unreplaced placeholders in {template_path.name}: {remaining}")

    return template


def render_all_prompts(output_dir: Path = None):
    """
    Render all agent prompts to output directory.

    Args:
        output_dir: Directory to write rendered prompts (default: config/rendered-prompts/)
    """
    prompts_dir = Path(__file__).parent.parent / "config" / "agent-prompts"
    output_dir = output_dir or prompts_dir.parent / "rendered-prompts"
    output_dir.mkdir(exist_ok=True)

    if not prompts_dir.exists():
        logger.error(f"Prompts directory not found: {prompts_dir}")
        return

    rendered_count = 0
    for prompt_file in prompts_dir.glob("*.md"):
        try:
            rendered = render_prompt(prompt_file)
            output_path = output_dir / prompt_file.name
            output_path.write_text(rendered, encoding='utf-8')
            logger.info(f"Rendered: {prompt_file.name} -> {output_path}")
            rendered_count += 1
        except Exception as e:
            logger.error(f"Failed to render {prompt_file.name}: {e}")

    logger.info(f"Rendered {rendered_count} prompt files to {output_dir}")


def validate_prompts() -> dict:
    """
    Validate all prompts for unreplaced placeholders.

    Returns:
        Dict with 'valid' bool and 'issues' list
    """
    prompts_dir = Path(__file__).parent.parent / "config" / "agent-prompts"
    results = {'valid': True, 'issues': []}

    if not prompts_dir.exists():
        results['valid'] = False
        results['issues'].append(f"Prompts directory not found: {prompts_dir}")
        return results

    for prompt_file in prompts_dir.glob("*.md"):
        content = prompt_file.read_text(encoding='utf-8')
        remaining = re.findall(r'\{\{config\.[^}]+\}\}', content)
        if remaining:
            results['issues'].append({
                'file': prompt_file.name,
                'placeholders': remaining
            })

    if results['issues']:
        results['valid'] = False

    return results


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--validate':
        # Validate mode
        results = validate_prompts()
        if results['valid']:
            print("All prompts valid - no unreplaced placeholders")
        else:
            print("Validation issues found:")
            for issue in results['issues']:
                if isinstance(issue, dict):
                    print(f"  {issue['file']}: {issue['placeholders']}")
                else:
                    print(f"  {issue}")
            sys.exit(1)
    else:
        # Render mode
        if not CONFIG_AVAILABLE:
            logger.warning("Config loader not available - using defaults")
        render_all_prompts()


if __name__ == "__main__":
    main()
