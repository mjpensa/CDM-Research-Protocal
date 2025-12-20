"""
CDM Research Protocol - URL Validator v1.0

Lightweight URL validation for evidence sources.
Supports quick HEAD checks and full content verification.

Features:
- Quick HEAD request validation
- Full GET with content hashing
- Batch validation with rate limiting
- Wayback Machine fallback suggestions
- Session caching

Usage:
    from url_validator import URLValidator

    validator = URLValidator()
    status = validator.check_url("https://example.com/article")
    print(status.alive, status.status_code)
"""

import time
import hashlib
import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, List, Callable
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    print("Warning: 'requests' module not installed. URL validation will be limited.")
    requests = None

# Rate limiting
REQUEST_DELAY = 0.5  # seconds between requests to same domain
MAX_CONCURRENT = 5


@dataclass
class URLStatus:
    """Status of a URL check."""
    url: str
    alive: bool
    status_code: int
    content_type: Optional[str] = None
    content_hash: Optional[str] = None
    final_url: Optional[str] = None
    error: Optional[str] = None
    wayback_url: Optional[str] = None
    check_time: float = 0.0


class URLValidator:
    """
    Validates URLs for evidence sources.
    """

    def __init__(self, cache_path: Optional[str] = None, timeout: int = 10):
        """
        Initialize validator.

        Args:
            cache_path: Optional path to cache file
            timeout: Request timeout in seconds
        """
        self.timeout = timeout

        if requests:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (ResearchBot/2.3; CDMValidator)'
            })
        else:
            self.session = None

        # Domain rate limiting
        self.last_request_time: Dict[str, float] = {}

        # Cache
        self.cache: Dict[str, URLStatus] = {}
        self.cache_path = Path(cache_path) if cache_path else None

        if self.cache_path and self.cache_path.exists():
            self._load_cache()

    def _load_cache(self):
        """Load cache from file."""
        try:
            data = json.loads(self.cache_path.read_text(encoding='utf-8'))
            for url, status_dict in data.items():
                self.cache[url] = URLStatus(**status_dict)
        except Exception:
            pass

    def _save_cache(self):
        """Save cache to file."""
        if not self.cache_path:
            return

        try:
            data = {
                url: {
                    'url': s.url,
                    'alive': s.alive,
                    'status_code': s.status_code,
                    'content_type': s.content_type,
                    'content_hash': s.content_hash,
                    'final_url': s.final_url,
                    'error': s.error,
                    'wayback_url': s.wayback_url,
                    'check_time': s.check_time
                }
                for url, s in self.cache.items()
            }
            self.cache_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        except Exception:
            pass

    def _rate_limit(self, domain: str):
        """Apply rate limiting for domain."""
        last_time = self.last_request_time.get(domain, 0)
        elapsed = time.time() - last_time

        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)

        self.last_request_time[domain] = time.time()

    def _get_wayback_url(self, url: str) -> Optional[str]:
        """Get Wayback Machine URL for a dead link."""
        if not self.session:
            return None

        try:
            api_url = f"http://archive.org/wayback/available?url={url}"
            response = self.session.get(api_url, timeout=5)
            data = response.json()

            snapshot = data.get('archived_snapshots', {}).get('closest', {})
            if snapshot.get('available'):
                return snapshot.get('url')
        except Exception:
            pass

        return None

    def check_url(self, url: str, quick: bool = True, use_cache: bool = True) -> URLStatus:
        """
        Check if a URL is alive.

        Args:
            url: URL to check
            quick: If True, use HEAD request only. If False, GET full content.
            use_cache: Whether to use/update cache

        Returns:
            URLStatus with check results
        """
        if not self.session:
            return URLStatus(
                url=url,
                alive=False,
                status_code=0,
                error="requests module not installed",
                check_time=time.time()
            )

        # Check cache
        if use_cache and url in self.cache:
            cached = self.cache[url]
            # Cache valid for 1 hour
            if time.time() - cached.check_time < 3600:
                return cached

        try:
            parsed = urlparse(url)
            domain = parsed.netloc

            # Rate limit
            self._rate_limit(domain)

            if quick:
                response = self.session.head(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True
                )
            else:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True
                )

            status = URLStatus(
                url=url,
                alive=200 <= response.status_code < 400,
                status_code=response.status_code,
                content_type=response.headers.get('Content-Type'),
                final_url=response.url if response.url != url else None,
                check_time=time.time()
            )

            # Calculate content hash for full GET
            if not quick and response.status_code == 200:
                status.content_hash = hashlib.sha256(response.content).hexdigest()[:16]

            # Get Wayback URL for dead links
            if not status.alive:
                status.wayback_url = self._get_wayback_url(url)

        except requests.Timeout:
            status = URLStatus(
                url=url,
                alive=False,
                status_code=0,
                error="Timeout",
                check_time=time.time()
            )
        except requests.RequestException as e:
            status = URLStatus(
                url=url,
                alive=False,
                status_code=0,
                error=str(e)[:100],
                check_time=time.time()
            )
        except Exception as e:
            status = URLStatus(
                url=url,
                alive=False,
                status_code=0,
                error=f"Unexpected error: {str(e)[:80]}",
                check_time=time.time()
            )

        # Update cache
        if use_cache:
            self.cache[url] = status
            self._save_cache()

        return status

    def check_batch(
        self,
        urls: List[str],
        quick: bool = True,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Dict[str, URLStatus]:
        """
        Check multiple URLs with parallel execution.

        Args:
            urls: List of URLs to check
            quick: Use HEAD requests
            progress_callback: Optional callback(completed, total)

        Returns:
            Dict mapping URL to status
        """
        results = {}
        completed = 0

        # Remove duplicates while preserving order
        unique_urls = list(dict.fromkeys(urls))

        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
            future_to_url = {
                executor.submit(self.check_url, url, quick): url
                for url in unique_urls
            }

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    results[url] = future.result()
                except Exception as e:
                    results[url] = URLStatus(
                        url=url,
                        alive=False,
                        status_code=0,
                        error=str(e)[:100],
                        check_time=time.time()
                    )

                completed += 1
                if progress_callback:
                    progress_callback(completed, len(unique_urls))

        return results


def validate_evidence_urls(evidence_file: str) -> dict:
    """
    Validate all URLs in an evidence file.

    Args:
        evidence_file: Path to evidence markdown or JSON file

    Returns:
        Validation results
    """
    # Import here to avoid circular imports
    from markdown_parser import parse_evidence_file

    path = Path(evidence_file)
    validator = URLValidator()

    if path.suffix == '.md':
        blocks, _ = parse_evidence_file(str(path))
        urls = [b.source_url for b in blocks if b.source_url]
    elif path.suffix == '.json':
        data = json.loads(path.read_text(encoding='utf-8'))
        urls = [item.get('source_url') for item in data.get('evidence_items', []) if item.get('source_url')]
    else:
        return {'error': f'Unsupported file type: {path.suffix}'}

    if not urls:
        return {
            'total': 0,
            'alive': 0,
            'dead': 0,
            'alive_rate': 1.0,
            'dead_urls': []
        }

    print(f"Checking {len(urls)} URLs...")

    def progress(completed, total):
        print(f"  Progress: {completed}/{total}", end='\r')

    results = validator.check_batch(urls, quick=True, progress_callback=progress)
    print()  # New line after progress

    alive = sum(1 for s in results.values() if s.alive)
    dead = len(results) - alive

    summary = {
        'total': len(urls),
        'alive': alive,
        'dead': dead,
        'alive_rate': alive / len(urls) if urls else 0,
        'dead_urls': [
            {
                'url': s.url,
                'status_code': s.status_code,
                'error': s.error,
                'wayback': s.wayback_url
            }
            for s in results.values() if not s.alive
        ]
    }

    return summary


def validate_bank_urls(bank_dir: str) -> dict:
    """
    Validate all URLs across a bank's evidence files.

    Args:
        bank_dir: Path to bank directory

    Returns:
        Validation results
    """
    bank_path = Path(bank_dir)
    evidence_dir = bank_path / "1-evidence"

    all_results = {
        'total': 0,
        'alive': 0,
        'dead': 0,
        'by_tier': {},
        'dead_urls': []
    }

    if not evidence_dir.exists():
        return all_results

    for tier in [1, 2, 3]:
        tier_file = evidence_dir / f"tier{tier}-evidence.md"
        if tier_file.exists():
            tier_results = validate_evidence_urls(str(tier_file))
            all_results['total'] += tier_results.get('total', 0)
            all_results['alive'] += tier_results.get('alive', 0)
            all_results['dead'] += tier_results.get('dead', 0)
            all_results['by_tier'][f'tier{tier}'] = tier_results
            all_results['dead_urls'].extend(tier_results.get('dead_urls', []))

    all_results['alive_rate'] = all_results['alive'] / all_results['total'] if all_results['total'] > 0 else 1.0

    return all_results


# --- CLI ---

def main():
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    if len(sys.argv) < 2:
        print("Usage: python url_validator.py <url_or_file>")
        print("       python url_validator.py https://example.com")
        print("       python url_validator.py outputs/phase-1/barclays/1-evidence/tier1-evidence.md")
        print("       python url_validator.py outputs/phase-1/barclays/  # Validate all bank URLs")
        sys.exit(1)

    target = sys.argv[1]

    if target.startswith('http'):
        # Single URL check
        validator = URLValidator()
        status = validator.check_url(target, quick=False)

        print(f"URL: {status.url}")
        print(f"Alive: {status.alive}")
        print(f"Status Code: {status.status_code}")
        print(f"Content Type: {status.content_type}")
        print(f"Final URL: {status.final_url}")

        if status.error:
            print(f"Error: {status.error}")

        if status.wayback_url:
            print(f"Wayback URL: {status.wayback_url}")

        if status.content_hash:
            print(f"Content Hash: {status.content_hash}")

    elif Path(target).is_dir():
        # Bank directory validation
        results = validate_bank_urls(target)

        print(f"\n=== URL Validation Results for {Path(target).name} ===")
        print(f"Total URLs: {results['total']}")
        print(f"Alive: {results['alive']} ({results['alive_rate']:.0%})")
        print(f"Dead: {results['dead']}")

        if results.get('dead_urls'):
            print(f"\nDead URLs:")
            for dead in results['dead_urls'][:10]:  # Limit to first 10
                print(f"  {dead['url'][:60]}...")
                if dead.get('wayback'):
                    print(f"    Wayback: {dead['wayback']}")
                elif dead.get('error'):
                    print(f"    Error: {dead['error']}")

    else:
        # File validation
        results = validate_evidence_urls(target)

        print(f"\n=== URL Validation Results ===")
        print(f"Total URLs: {results.get('total', 0)}")
        print(f"Alive: {results.get('alive', 0)} ({results.get('alive_rate', 0):.0%})")
        print(f"Dead: {results.get('dead', 0)}")

        if results.get('dead_urls'):
            print(f"\nDead URLs:")
            for dead in results['dead_urls']:
                print(f"  {dead['url'][:60]}...")
                if dead.get('wayback'):
                    print(f"    Wayback: {dead['wayback']}")
                elif dead.get('error'):
                    print(f"    Error: {dead['error']}")


if __name__ == "__main__":
    main()
