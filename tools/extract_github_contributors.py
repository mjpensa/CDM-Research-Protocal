"""
CDM Research Protocol - GitHub Contributor Extraction v1.0

Extracts contributor list from FINOS CDM repository and maps
email domains to bank IDs for evidence pre-population.

Usage:
    python tools/extract_github_contributors.py --update
    python tools/extract_github_contributors.py --repo https://github.com/finos/common-domain-model
    python tools/extract_github_contributors.py --dry-run
    python tools/extract_github_contributors.py --use-api  # Fallback if git CLI unavailable
"""

import argparse
import json
import subprocess
import re
import sys
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List, Dict, Optional, Set
from collections import defaultdict
from urllib.parse import urlparse

# --- PROJECT PATHS ---
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"
CACHE_DIR = PROJECT_ROOT / ".cache" / "repos"

sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import load_bank_manifest, get_bank_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# --- DATACLASSES ---

@dataclass
class Contributor:
    """Individual contributor record."""
    name: str
    email: str
    domain: str
    commit_count: int
    first_commit: Optional[str] = None
    last_commit: Optional[str] = None
    bank_id: Optional[str] = None
    bank_name: Optional[str] = None
    confidence: str = "inferred"  # "confirmed" or "inferred"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Contributor':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class ContributorRegistry:
    """Complete contributor registry from a repository."""
    repo_url: str
    repo_name: str
    extracted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    extraction_method: str = "git_log"  # "git_log" or "github_api"
    total_contributors: int = 0
    mapped_contributors: int = 0
    unmapped_contributors: int = 0
    contributors: List[Contributor] = field(default_factory=list)
    banks_found: Dict[str, int] = field(default_factory=dict)
    domain_mapping: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        data = asdict(self)
        data['contributors'] = [c.to_dict() if isinstance(c, Contributor) else c for c in self.contributors]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'ContributorRegistry':
        contributors = [Contributor.from_dict(c) for c in data.get('contributors', [])]
        data_copy = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        data_copy['contributors'] = contributors
        return cls(**data_copy)


# --- DOMAIN MAPPING ---

# Known email domain patterns for major banks
KNOWN_DOMAIN_PATTERNS = {
    # US Banks
    'jpmorgan.com': 'jpmorgan',
    'jpmchase.com': 'jpmorgan',
    'gs.com': 'goldman-sachs',
    'goldmansachs.com': 'goldman-sachs',
    'morganstanley.com': 'morgan-stanley',
    'citi.com': 'citigroup',
    'citigroup.com': 'citigroup',
    'bofa.com': 'bank-of-america',
    'bankofamerica.com': 'bank-of-america',

    # UK Banks
    'barclays.com': 'barclays',
    'barcap.com': 'barclays',
    'hsbc.com': 'hsbc',
    'sc.com': 'standard-chartered',
    'standardchartered.com': 'standard-chartered',
    'lloydsbanking.com': 'lloyds',
    'natwest.com': 'natwest',
    'rbs.com': 'natwest',

    # European Banks
    'db.com': 'deutsche-bank',
    'deutsche-bank.com': 'deutsche-bank',
    'bnpparibas.com': 'bnp-paribas',
    'sgcib.com': 'societe-generale',
    'socgen.com': 'societe-generale',
    'ubs.com': 'ubs',
    'credit-suisse.com': 'credit-suisse',
    'cs.com': 'credit-suisse',
    'unicredit.eu': 'unicredit',
    'ing.com': 'ing',

    # Japanese Banks
    'nomura.com': 'nomura',
    'mufg.jp': 'mufg',
    'mizuho-sc.com': 'mizuho',
    'smbc.co.jp': 'smbc',
    'daiwa.co.jp': 'daiwa',

    # Swiss Private Banks
    'pictet.com': 'pictet',
    'juliusbaer.com': 'julius-baer',

    # Vendors (for filtering)
    'regnosys.com': '_vendor_regnosys',
    'isda.org': '_vendor_isda',
    'finos.org': '_vendor_finos',
}


def build_domain_to_bank_mapping() -> Dict[str, str]:
    """
    Build mapping from email domains to bank IDs.
    Combines known patterns with bank-manifest.json data.
    """
    domain_map = dict(KNOWN_DOMAIN_PATTERNS)

    try:
        manifest = load_bank_manifest()
        for bank in manifest.get('banks', []):
            bank_id = bank.get('bank_id')
            bank_name = bank.get('bank_name', '')

            # Generate additional domain patterns from bank name
            patterns = generate_domain_patterns(bank_name, bank_id)
            for pattern in patterns:
                if pattern not in domain_map:
                    domain_map[pattern] = bank_id
    except Exception as e:
        logger.warning(f"Could not load bank manifest: {e}")

    return domain_map


def generate_domain_patterns(bank_name: str, bank_id: str) -> List[str]:
    """Generate possible email domain patterns for a bank."""
    patterns = []

    # Clean bank name
    clean_name = re.sub(r'[^a-z0-9\s]', '', bank_name.lower())
    words = clean_name.split()

    if not words:
        return patterns

    # Full hyphenated name: deutsche-bank.com
    if len(words) > 1:
        patterns.append(f"{'-'.join(words)}.com")

    # First word only: deutsche.com
    patterns.append(f"{words[0]}.com")

    # First two words concatenated: deutschebank.com
    if len(words) >= 2:
        patterns.append(f"{''.join(words[:2])}.com")

    # Abbreviations: db.com for Deutsche Bank
    if len(words) >= 2:
        abbrev = ''.join(w[0] for w in words if w)
        if len(abbrev) >= 2:
            patterns.append(f"{abbrev}.com")

    return patterns


# --- GIT EXTRACTION ---

def check_git_available() -> bool:
    """Check if git CLI is available."""
    try:
        result = subprocess.run(
            ['git', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def clone_or_update_repo(repo_url: str, cache_dir: Path = CACHE_DIR) -> Path:
    """
    Clone repository or update existing clone.

    Args:
        repo_url: GitHub repository URL
        cache_dir: Directory for cached repository clones

    Returns:
        Path to cloned repository
    """
    # Extract repo name from URL
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) >= 2:
        repo_name = path_parts[-1].replace('.git', '')
    else:
        repo_name = 'repo'

    repo_path = cache_dir / repo_name

    if repo_path.exists():
        logger.info(f"Updating existing clone at {repo_path}")
        try:
            subprocess.run(
                ['git', 'fetch', '--all'],
                cwd=repo_path,
                check=True,
                capture_output=True
            )
            subprocess.run(
                ['git', 'pull', '--ff-only'],
                cwd=repo_path,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git fetch/pull failed: {e}")
    else:
        logger.info(f"Cloning {repo_url} to {repo_path}")
        cache_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ['git', 'clone', '--depth=1000', repo_url, str(repo_path)],
            check=True
        )
        # Unshallow to get full history
        subprocess.run(
            ['git', 'fetch', '--unshallow'],
            cwd=repo_path,
            capture_output=True
        )

    return repo_path


def extract_git_contributors(repo_path: Path) -> List[Dict]:
    """
    Extract contributor info from git log.

    Args:
        repo_path: Path to cloned repository

    Returns:
        List of contributor dicts with name, email, commit info
    """
    cmd = [
        'git', 'log',
        '--format=%aN|%aE|%aI',  # Author name, email, ISO date
        '--all'
    ]

    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    if result.returncode != 0:
        raise RuntimeError(f"git log failed: {result.stderr}")

    # Parse commits and aggregate by author
    author_data = defaultdict(lambda: {'commits': [], 'count': 0})

    for line in result.stdout.strip().split('\n'):
        if '|' not in line:
            continue
        parts = line.split('|')
        if len(parts) >= 3:
            name, email, date = parts[0], parts[1], parts[2]
            key = (name, email)
            author_data[key]['commits'].append(date)
            author_data[key]['count'] += 1

    # Convert to list with first/last commit
    contributors = []
    for (name, email), data in author_data.items():
        dates = sorted(data['commits'])
        domain = email.split('@')[-1].lower() if '@' in email else 'unknown'

        contributors.append({
            'name': name,
            'email': email,
            'domain': domain,
            'commit_count': data['count'],
            'first_commit': dates[0] if dates else None,
            'last_commit': dates[-1] if dates else None
        })

    return contributors


# --- GITHUB API FALLBACK ---

def fetch_contributors_via_api(repo_url: str) -> List[Dict]:
    """
    Fetch contributors via GitHub API (fallback when git CLI unavailable).

    Note: This provides less detail than git log (no email domains for privacy).
    """
    try:
        import urllib.request
        import urllib.error
    except ImportError:
        raise RuntimeError("urllib not available for API fallback")

    # Parse repo URL to get owner/repo
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) < 2:
        raise ValueError(f"Invalid GitHub URL: {repo_url}")

    owner, repo = path_parts[0], path_parts[1].replace('.git', '')

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100"

    logger.info(f"Fetching contributors from GitHub API: {api_url}")

    request = urllib.request.Request(
        api_url,
        headers={'User-Agent': 'CDM-Research-Protocol/1.0'}
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"GitHub API error: {e.code} {e.reason}")

    contributors = []
    for c in data:
        contributors.append({
            'name': c.get('login', 'unknown'),
            'email': f"{c.get('login', 'unknown')}@users.noreply.github.com",
            'domain': 'users.noreply.github.com',
            'commit_count': c.get('contributions', 0),
            'first_commit': None,
            'last_commit': None
        })

    return contributors


# --- MAPPING ---

def map_contributors_to_banks(
    contributors: List[Dict],
    domain_mapping: Dict[str, str]
) -> List[Contributor]:
    """
    Map contributor email domains to bank IDs.

    Args:
        contributors: Raw contributor data
        domain_mapping: Domain to bank_id mapping

    Returns:
        List of Contributor objects with bank mapping
    """
    result = []

    for c in contributors:
        domain = c.get('domain', '').lower()
        bank_id = None
        bank_name = None
        confidence = "inferred"

        # Direct domain match
        if domain in domain_mapping:
            bank_id = domain_mapping[domain]
            # Skip vendors
            if bank_id and bank_id.startswith('_vendor'):
                bank_id = None
            else:
                confidence = "confirmed"
        else:
            # Fuzzy matching for subdomains
            for pattern, bid in domain_mapping.items():
                if bid.startswith('_vendor'):
                    continue
                if domain.endswith(f".{pattern}") or pattern in domain:
                    bank_id = bid
                    confidence = "inferred"
                    break

        # Get bank name if we have a bank_id
        if bank_id:
            bank_config = get_bank_config(bank_id)
            bank_name = bank_config.get('bank_name') if bank_config else None

        result.append(Contributor(
            name=c['name'],
            email=c['email'],
            domain=domain,
            commit_count=c['commit_count'],
            first_commit=c.get('first_commit'),
            last_commit=c.get('last_commit'),
            bank_id=bank_id,
            bank_name=bank_name,
            confidence=confidence
        ))

    return result


# --- MAIN ---

def extract_contributors(
    repo_url: str,
    use_api: bool = False,
    dry_run: bool = False
) -> ContributorRegistry:
    """
    Main extraction function.

    Args:
        repo_url: Repository URL to analyze
        use_api: Force use of GitHub API instead of git CLI
        dry_run: If True, don't write output file

    Returns:
        ContributorRegistry with all contributor data
    """
    # Determine extraction method
    if use_api or not check_git_available():
        method = "github_api"
        logger.info("Using GitHub API for extraction")
        raw_contributors = fetch_contributors_via_api(repo_url)
    else:
        method = "git_log"
        logger.info("Using git CLI for extraction")
        repo_path = clone_or_update_repo(repo_url)
        raw_contributors = extract_git_contributors(repo_path)

    logger.info(f"Found {len(raw_contributors)} raw contributors")

    # Build domain mapping
    domain_mapping = build_domain_to_bank_mapping()

    # Map to banks
    contributors = map_contributors_to_banks(raw_contributors, domain_mapping)

    # Calculate statistics
    banks_found = defaultdict(int)
    mapped_count = 0
    for c in contributors:
        if c.bank_id:
            banks_found[c.bank_id] += 1
            mapped_count += 1

    # Parse repo name
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip('/').split('/')
    repo_name = path_parts[-1].replace('.git', '') if path_parts else 'unknown'

    registry = ContributorRegistry(
        repo_url=repo_url,
        repo_name=repo_name,
        extraction_method=method,
        total_contributors=len(contributors),
        mapped_contributors=mapped_count,
        unmapped_contributors=len(contributors) - mapped_count,
        contributors=contributors,
        banks_found=dict(banks_found),
        domain_mapping={k: v for k, v in domain_mapping.items() if not v.startswith('_vendor')}
    )

    return registry


def main():
    parser = argparse.ArgumentParser(
        description="Extract GitHub contributors and map to bank IDs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--repo',
        default='https://github.com/finos/common-domain-model',
        help='Repository URL to analyze'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help='Update existing clone before extraction'
    )
    parser.add_argument(
        '--use-api',
        action='store_true',
        help='Use GitHub API instead of git CLI (less detailed)'
    )
    parser.add_argument(
        '--output',
        default=str(KNOWLEDGE_BASE_DIR / 'github_contributors.json'),
        help='Output file path'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without writing'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON to stdout'
    )

    args = parser.parse_args()

    try:
        registry = extract_contributors(
            repo_url=args.repo,
            use_api=args.use_api,
            dry_run=args.dry_run
        )

        # Print summary
        print(f"\n{'='*60}")
        print(f"GitHub Contributor Extraction Results")
        print(f"{'='*60}")
        print(f"Repository: {registry.repo_url}")
        print(f"Method: {registry.extraction_method}")
        print(f"Total Contributors: {registry.total_contributors}")
        print(f"Mapped to Banks: {registry.mapped_contributors}")
        print(f"Unmapped: {registry.unmapped_contributors}")
        print(f"\nBanks Found:")
        for bank_id, count in sorted(registry.banks_found.items(), key=lambda x: -x[1]):
            print(f"  {bank_id}: {count} contributor(s)")

        if args.json:
            print(f"\n{'='*60}")
            print(json.dumps(registry.to_dict(), indent=2))

        if not args.dry_run:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                json.dumps(registry.to_dict(), indent=2),
                encoding='utf-8'
            )
            print(f"\nOutput written to: {output_path}")
        else:
            print(f"\n[DRY RUN] Would write to: {args.output}")

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
