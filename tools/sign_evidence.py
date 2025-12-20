"""
CDM Research Protocol - Evidence Signing Tool v1.0

Cryptographic signing for evidence integrity using SHA256 hash chains.
Creates tamper-evident audit trail where each block references the previous.

This tool:
- Creates hash chain blocks for evidence files
- Verifies chain integrity (detects tampering)
- Verifies individual file integrity
- Stores chain in evidence-chain.json

Usage:
    python sign_evidence.py <bank_dir> sign <file> <stage>
    python sign_evidence.py <bank_dir> verify
    python sign_evidence.py <bank_dir> verify-file <file>
    python sign_evidence.py <bank_dir> status
"""

import json
import sys
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EvidenceChain:
    """
    Hash chain for tamper-evident evidence tracking.

    Each block contains:
    - index: Block number in chain
    - timestamp: When block was created
    - file: Relative path to signed file
    - stage: Workflow stage when signed
    - content_hash: SHA256 of file content
    - prev_hash: Hash of previous block (or "GENESIS")
    - block_hash: SHA256(prev_hash + content_hash + stage)

    Chain integrity check:
    - Each block's prev_hash must match previous block's block_hash
    - Each block's block_hash must match recalculated value
    """

    def __init__(self, bank_dir: Path):
        """
        Initialize evidence chain for a bank.

        Args:
            bank_dir: Path to bank output directory
        """
        self.bank_dir = Path(bank_dir)
        self.chain_path = self.bank_dir / "evidence-chain.json"
        self.chain: list[dict] = []
        self._load_chain()

    def _load_chain(self):
        """Load existing chain from file."""
        if self.chain_path.exists():
            try:
                data = json.loads(self.chain_path.read_text(encoding='utf-8'))
                self.chain = data.get('chain', [])
                logger.debug(f"Loaded chain with {len(self.chain)} blocks")
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Failed to load chain: {e}")
                self.chain = []

    def _save(self):
        """Save chain to file."""
        # Ensure directory exists
        self.bank_dir.mkdir(parents=True, exist_ok=True)

        data = {
            "bank_id": self.bank_dir.name,
            "chain_length": len(self.chain),
            "created_at": self.chain[0]['timestamp'] if self.chain else None,
            "last_updated": datetime.utcnow().isoformat(),
            "last_block": self.chain[-1] if self.chain else None,
            "chain": self.chain
        }
        self.chain_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def _hash_content(self, content: str) -> str:
        """Calculate SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _hash_bytes(self, data: bytes) -> str:
        """Calculate SHA256 hash of bytes."""
        return hashlib.sha256(data).hexdigest()

    def add_block(self, file_path: Path, stage: str) -> dict:
        """
        Add new block to chain for a file.

        Args:
            file_path: Path to file to sign
            stage: Current workflow stage

        Returns:
            The created block dict
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read file content
        try:
            content = file_path.read_text(encoding='utf-8')
            content_hash = self._hash_content(content)
        except UnicodeDecodeError:
            # Binary file - hash bytes directly
            content_bytes = file_path.read_bytes()
            content_hash = self._hash_bytes(content_bytes)

        # Get previous block hash
        prev_hash = self.chain[-1]['block_hash'] if self.chain else "GENESIS"

        # Calculate relative path
        try:
            rel_path = str(file_path.relative_to(self.bank_dir))
        except ValueError:
            rel_path = str(file_path)

        # Create block
        block = {
            'index': len(self.chain),
            'timestamp': datetime.utcnow().isoformat(),
            'file': rel_path,
            'stage': stage,
            'content_hash': content_hash,
            'prev_hash': prev_hash,
            'block_hash': self._hash_content(f"{prev_hash}{content_hash}{stage}")
        }

        self.chain.append(block)
        self._save()

        logger.info(f"Added block {block['index']}: {rel_path} at {stage}")
        return block

    def verify_chain(self) -> tuple[bool, Optional[str]]:
        """
        Verify entire chain integrity.

        Returns:
            (is_valid, error_message or None)
        """
        if not self.chain:
            return True, None

        for i, block in enumerate(self.chain):
            # Check previous hash link
            if i == 0:
                expected_prev = "GENESIS"
            else:
                expected_prev = self.chain[i - 1]['block_hash']

            if block['prev_hash'] != expected_prev:
                return False, f"Chain broken at block {i}: prev_hash mismatch (expected {expected_prev[:16]}..., got {block['prev_hash'][:16]}...)"

            # Recalculate block hash
            expected_hash = self._hash_content(
                f"{block['prev_hash']}{block['content_hash']}{block['stage']}"
            )
            if block['block_hash'] != expected_hash:
                return False, f"Chain broken at block {i}: block_hash mismatch (expected {expected_hash[:16]}..., got {block['block_hash'][:16]}...)"

        return True, None

    def verify_file(self, file_path: Path) -> tuple[bool, Optional[str]]:
        """
        Verify a file matches its latest chain entry.

        Args:
            file_path: Path to file to verify

        Returns:
            (is_valid, error_message or None)
        """
        file_path = Path(file_path)

        if not file_path.exists():
            return False, f"File not found: {file_path}"

        # Get relative path
        try:
            rel_path = str(file_path.relative_to(self.bank_dir))
        except ValueError:
            rel_path = str(file_path)

        # Find latest block for this file
        file_blocks = [b for b in self.chain if b['file'] == rel_path]
        if not file_blocks:
            return False, f"No chain entry for {rel_path}"

        latest = file_blocks[-1]

        # Calculate current hash
        try:
            content = file_path.read_text(encoding='utf-8')
            current_hash = self._hash_content(content)
        except UnicodeDecodeError:
            content_bytes = file_path.read_bytes()
            current_hash = self._hash_bytes(content_bytes)

        if current_hash != latest['content_hash']:
            return False, f"Content modified since {latest['timestamp']} (block {latest['index']})"

        return True, None

    def get_file_history(self, file_path: Path) -> list[dict]:
        """
        Get all chain entries for a specific file.

        Args:
            file_path: Path to file

        Returns:
            List of block dicts for this file, chronologically ordered
        """
        try:
            rel_path = str(file_path.relative_to(self.bank_dir))
        except ValueError:
            rel_path = str(file_path)

        return [b for b in self.chain if b['file'] == rel_path]

    def get_status(self) -> dict:
        """Get chain status summary."""
        is_valid, error = self.verify_chain()

        # Count files
        files = set(b['file'] for b in self.chain)

        # Count by stage
        stages = {}
        for b in self.chain:
            stages[b['stage']] = stages.get(b['stage'], 0) + 1

        return {
            "bank_id": self.bank_dir.name,
            "chain_length": len(self.chain),
            "unique_files": len(files),
            "blocks_by_stage": stages,
            "is_valid": is_valid,
            "validation_error": error,
            "first_block": self.chain[0]['timestamp'] if self.chain else None,
            "last_block": self.chain[-1]['timestamp'] if self.chain else None
        }


def print_status(status: dict):
    """Print chain status in human-readable format."""
    print(f"\n{'='*60}")
    print(f"Evidence Chain: {status['bank_id']}")
    print(f"{'='*60}")
    print(f"Chain length:    {status['chain_length']} blocks")
    print(f"Unique files:    {status['unique_files']}")

    if status['blocks_by_stage']:
        print(f"\nBlocks by stage:")
        for stage, count in sorted(status['blocks_by_stage'].items()):
            print(f"  {stage}: {count}")

    if status['first_block']:
        print(f"\nFirst block:     {status['first_block']}")
        print(f"Last block:      {status['last_block']}")

    if status['is_valid']:
        print(f"\n[OK] Chain integrity verified")
    else:
        print(f"\n[INVALID] {status['validation_error']}")

    print(f"{'='*60}\n")


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: python sign_evidence.py <bank_dir> <command> [args]")
        print("Commands:")
        print("  sign <file> <stage>  - Add file to chain")
        print("  verify               - Verify entire chain")
        print("  verify-file <file>   - Verify specific file")
        print("  status               - Show chain status")
        print("  history <file>       - Show file history")
        print("\nExamples:")
        print("  python sign_evidence.py outputs/phase-1/barclays sign evidence.json tier1_evidence")
        print("  python sign_evidence.py outputs/phase-1/barclays verify")
        sys.exit(1)

    bank_dir = Path(sys.argv[1])
    command = sys.argv[2]
    chain = EvidenceChain(bank_dir)

    if command == 'sign':
        if len(sys.argv) < 5:
            print("Error: sign requires <file> and <stage>")
            sys.exit(1)
        file_path = Path(sys.argv[3])
        stage = sys.argv[4]

        # Handle relative paths
        if not file_path.is_absolute():
            file_path = bank_dir / file_path

        try:
            block = chain.add_block(file_path, stage)
            print(f"[OK] Added block {block['index']}: {block['block_hash'][:16]}...")
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)

    elif command == 'verify':
        valid, error = chain.verify_chain()
        if valid:
            print(f"[OK] Chain valid ({len(chain.chain)} blocks)")
            sys.exit(0)
        else:
            print(f"[INVALID] {error}")
            sys.exit(1)

    elif command == 'verify-file':
        if len(sys.argv) < 4:
            print("Error: verify-file requires <file>")
            sys.exit(1)
        file_path = Path(sys.argv[3])
        if not file_path.is_absolute():
            file_path = bank_dir / file_path

        valid, error = chain.verify_file(file_path)
        if valid:
            print(f"[OK] File verified")
            sys.exit(0)
        else:
            print(f"[INVALID] {error}")
            sys.exit(1)

    elif command == 'status':
        status = chain.get_status()
        print_status(status)

    elif command == 'history':
        if len(sys.argv) < 4:
            print("Error: history requires <file>")
            sys.exit(1)
        file_path = Path(sys.argv[3])
        if not file_path.is_absolute():
            file_path = bank_dir / file_path

        history = chain.get_file_history(file_path)
        if not history:
            print(f"No history for {file_path}")
        else:
            print(f"\nHistory for {file_path} ({len(history)} entries):")
            for block in history:
                print(f"  [{block['index']}] {block['timestamp']} - {block['stage']}")
                print(f"      Hash: {block['content_hash'][:24]}...")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
