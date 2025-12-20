"""
CDM Forensic Research Engine v2.3 - Evidence Processor
Security-hardened implementation with:
- Path traversal prevention
- SSRF protection
- Download size limits
- Proper error handling
- Content drift detection
- Hash history tracking
- Verification counting
"""

import json
import os
import hashlib
import requests
import sys
import platform
import uuid
import re
import logging
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from jsonschema import validate, ValidationError

# --- CONFIG ---
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
SCHEMA_PATH = PROJECT_ROOT / "templates" / "evidence-schema.json"
USER_AGENT = "Mozilla/5.0 (ResearchBot/2.3; ForensicEngine)"
TIMEOUT = 10
MAX_DOWNLOAD_SIZE = 10 * 1024 * 1024  # 10 MB limit

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_meta():
    """Generate metadata for the processing run."""
    return {
        "run_id": str(uuid.uuid4())[:8],
        "timestamp": datetime.utcnow().isoformat(),
        "tool_versions": {
            "python": platform.python_version(),
            "requests": requests.__version__
        }
    }


def sanitize_id(item_id: str) -> str:
    """
    SECURITY FIX: Sanitize item ID to prevent path traversal attacks.
    Only allows alphanumeric characters, underscores, and hyphens.
    """
    if not item_id:
        return "unknown"
    # Remove any path separators and keep only safe characters
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', str(item_id))
    # Prevent empty result
    return sanitized if sanitized else "unknown"


def is_safe_url(url: str) -> tuple[bool, str]:
    """
    SECURITY FIX: Validate URL to prevent SSRF attacks.
    Returns (is_safe, error_message).
    """
    try:
        parsed = urlparse(url)

        # Only allow HTTP(S) schemes
        if parsed.scheme not in ('http', 'https'):
            return False, f"Blocked scheme: {parsed.scheme}"

        hostname = parsed.hostname or ''
        hostname_lower = hostname.lower()

        # Block localhost and loopback
        blocked_hosts = [
            'localhost', '127.0.0.1', '::1', '0.0.0.0',
            '169.254.169.254',  # AWS metadata
            'metadata.google.internal',  # GCP metadata
        ]
        if hostname_lower in blocked_hosts:
            return False, f"Blocked host: {hostname}"

        # Block private IP ranges
        if hostname_lower.startswith(('10.', '192.168.', '172.16.', '172.17.',
                                       '172.18.', '172.19.', '172.20.', '172.21.',
                                       '172.22.', '172.23.', '172.24.', '172.25.',
                                       '172.26.', '172.27.', '172.28.', '172.29.',
                                       '172.30.', '172.31.')):
            return False, f"Blocked private IP: {hostname}"

        return True, ""

    except Exception as e:
        return False, f"URL parse error: {e}"


def check_wayback(url: str) -> str | None:
    """Fallback to Internet Archive Wayback Machine."""
    try:
        api = f"http://archive.org/wayback/available?url={url}"
        r = requests.get(api, timeout=5)
        r.raise_for_status()
        data = r.json()
        snap = data.get('archived_snapshots', {}).get('closest', {})
        if snap.get('available'):
            return snap.get('url')
    except requests.RequestException as e:
        logger.warning(f"Wayback API error: {e}")
    except (KeyError, ValueError) as e:
        logger.warning(f"Wayback response parse error: {e}")
    return None


def download_with_limit(url: str, headers: dict, timeout: int) -> requests.Response:
    """
    SECURITY FIX: Download content with size limit to prevent DoS.
    Streams the response and checks Content-Length header.
    """
    r = requests.get(url, headers=headers, timeout=timeout,
                     allow_redirects=True, stream=True)

    # Check Content-Length header first
    content_length = r.headers.get('Content-Length')
    if content_length and int(content_length) > MAX_DOWNLOAD_SIZE:
        r.close()
        raise ValueError(f"Content too large: {content_length} bytes (max: {MAX_DOWNLOAD_SIZE})")

    # Read content with chunked limit
    content = b''
    for chunk in r.iter_content(chunk_size=8192):
        content += chunk
        if len(content) > MAX_DOWNLOAD_SIZE:
            r.close()
            raise ValueError(f"Download exceeded size limit of {MAX_DOWNLOAD_SIZE} bytes")

    # Attach content to response object for compatibility
    r._content = content
    return r


def process_bank_evidence(json_path: str) -> bool:
    """
    Process and verify evidence for a bank.
    Returns True on success, False on failure.
    """
    json_path = Path(json_path).resolve()
    logger.info(f"Processing {json_path}...")

    # 1. Load & Schema Validate
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not SCHEMA_PATH.exists():
            logger.error(f"Schema file not found: {SCHEMA_PATH}")
            return False

        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        validate(instance=data, schema=schema)
        logger.info("Schema validation passed")

    except json.JSONDecodeError as e:
        logger.error(f"FATAL: Invalid JSON: {e}")
        return False
    except ValidationError as e:
        logger.error(f"FATAL: Schema Validation Failed: {e.message}")
        return False
    except FileNotFoundError as e:
        logger.error(f"FATAL: File not found: {e}")
        return False

    # 2. Inject Metadata
    if 'meta' not in data:
        data['meta'] = get_meta()

    # 3. Setup snapshot directory
    snapshot_dir = json_path.parent / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # 4. Process each evidence item
    for item in data.get('evidence_items', []):
        url = item.get('source_url')
        if not url:
            continue

        # SECURITY: Sanitize ID for file path
        safe_id = sanitize_id(item.get('id', 'unknown'))

        # Init verification block if missing
        if 'verification' not in item:
            item['verification'] = {"live_ok": False, "archive_ok": False, "status": "pending"}
        if 'content' not in item:
            item['content'] = {}

        logger.info(f"Checking {safe_id}: {url[:60]}...")

        # SECURITY: Validate URL before making request
        is_safe, error_msg = is_safe_url(url)
        if not is_safe:
            logger.warning(f"Blocked unsafe URL: {error_msg}")
            item['verification']['status'] = "error"
            item['verification']['error_msg'] = f"Security: {error_msg}"
            continue

        try:
            # A. Live Check
            try:
                r = download_with_limit(
                    url,
                    headers={'User-Agent': USER_AGENT},
                    timeout=TIMEOUT
                )
                final_url = r.url
                status_code = r.status_code
            except ValueError as e:
                # Size limit exceeded
                status_code = 0
                item['verification']['error_msg'] = str(e)
                item['verification']['status'] = "error"
                logger.warning(f"Download error: {e}")
                continue
            except requests.RequestException as e:
                status_code = 0
                item['verification']['error_msg'] = str(e)

            if 200 <= status_code < 300:
                # Live Success
                item['verification']['live_ok'] = True
                item['verification']['status'] = "verified"
                content_bytes = r.content

                # Calculate new hash
                new_hash = hashlib.sha256(content_bytes).hexdigest()
                now = datetime.utcnow().isoformat()

                # Content drift detection
                previous_hash = item['content'].get('hash_sha256')
                content_changed = False

                if previous_hash and previous_hash != new_hash:
                    content_changed = True
                    logger.warning(f"  CONTENT DRIFT DETECTED for {safe_id}")

                    # Add to hash history
                    if 'hash_history' not in item['content']:
                        item['content']['hash_history'] = []

                    # Store previous hash in history
                    item['content']['hash_history'].append({
                        "hash": previous_hash,
                        "retrieved_at": item['content'].get('retrieved_at', 'unknown'),
                        "byte_length": item['content'].get('byte_length', 0)
                    })

                # Update verification count
                verification_count = item['verification'].get('verification_count', 0) + 1

                # Excerpt verification - check if claimed excerpt appears in content
                excerpt = item.get('excerpt', '')
                excerpt_verified = False
                if excerpt and len(excerpt) > 10:
                    try:
                        # Try to decode content as text
                        content_text = content_bytes.decode('utf-8', errors='ignore').lower()
                        # Normalize whitespace for comparison
                        excerpt_normalized = ' '.join(excerpt.lower().split())
                        content_normalized = ' '.join(content_text.split())
                        excerpt_verified = excerpt_normalized in content_normalized
                        if not excerpt_verified:
                            logger.warning(f"  EXCERPT NOT FOUND in content for {safe_id}")
                    except Exception:
                        pass  # Binary content, skip excerpt check

                # Content Identity
                item['content'].update({
                    "hash_sha256": new_hash,
                    "byte_length": len(content_bytes),
                    "retrieved_at": now,
                    "content_type": r.headers.get('Content-Type', 'unknown'),
                    "final_url": final_url,
                    "content_changed": content_changed,
                    "excerpt_verified": excerpt_verified if excerpt else None
                })

                # Update verification metadata
                item['verification']['last_verified'] = now
                item['verification']['verification_count'] = verification_count

                # SECURITY: Use sanitized ID for snapshot filename
                snap_path = snapshot_dir / f"{safe_id}_raw.bin"
                with open(snap_path, 'wb') as f:
                    f.write(content_bytes)
                logger.info(f"  Verified and cached: {snap_path.name} (check #{verification_count})")

            else:
                # Live Fail -> Wayback Fallback
                logger.warning(f"Live check failed ({status_code}). Checking Archive...")
                if status_code in [403, 401]:
                    item['verification']['status'] = "paywalled"
                else:
                    item['verification']['status'] = "dead"

                archive_url = check_wayback(url)
                if archive_url:
                    item['verification']['archive_ok'] = True
                    item['verification']['status'] = "archived"
                    item['content']['archive_url'] = archive_url
                    logger.info("  Found in Wayback Machine")
                else:
                    logger.warning("  Dead link - not archived")

        except Exception as e:
            item['verification']['status'] = "error"
            item['verification']['error_msg'] = str(e)
            logger.error(f"Unexpected error: {e}")

    # 5. Write updated data back
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info("Processing complete.")
    return True


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python process_evidence.py <path/to/evidence.json>")
        print("       python process_evidence.py --dry-run <path/to/evidence.json>")
        sys.exit(1)

    # Handle --dry-run flag
    dry_run = False
    json_path = sys.argv[1]

    if sys.argv[1] == '--dry-run':
        if len(sys.argv) < 3:
            print("Error: --dry-run requires a file path")
            sys.exit(1)
        dry_run = True
        json_path = sys.argv[2]
        logger.info("DRY RUN MODE - no files will be modified")

    if dry_run:
        # In dry-run mode, just validate the file
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            validate(instance=data, schema=schema)
            logger.info("Validation passed (dry run)")

            # Show what would be processed
            for item in data.get('evidence_items', []):
                url = item.get('source_url', 'N/A')
                is_safe, msg = is_safe_url(url) if url != 'N/A' else (True, '')
                status = "OK" if is_safe else f"BLOCKED: {msg}"
                logger.info(f"  {item.get('id')}: {status}")

        except Exception as e:
            logger.error(f"Dry run failed: {e}")
            sys.exit(1)
    else:
        success = process_bank_evidence(json_path)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
