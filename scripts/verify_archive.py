#!/usr/bin/env python3
"""Fail closed when the recovery repository is unsafe or incomplete."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {".jsonl", ".sqlite", ".db", ".pem", ".key", ".p12", ".pfx"}
MAX_FILE = 10 * 1024 * 1024
SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "anthropic-key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{16,}"),
    "openai-key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    "github-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "stripe-secret": re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}"),
    "runpod-key": re.compile(r"\brpa_[A-Za-z0-9_-]{16,}"),
    "slack-token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    "notion-token": re.compile(r"\b(?:secret|ntn)_[A-Za-z0-9]{20,}"),
    "sentry-user-token": re.compile(r"\bsntryu_[A-Za-z0-9_-]{20,}"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
}


def main() -> int:
    errors: list[str] = []
    manifest_path = REPO / "MANIFEST.json"
    if not manifest_path.exists():
        errors.append("MANIFEST.json is missing")
        manifest = {}
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    archive_files = list((REPO / "projects").rglob("*")) if (REPO / "projects").exists() else []
    session_files = [p for p in archive_files if p.is_file() and p.name != "INDEX.md" and ("sessions" in p.parts or "codex-subagents" in p.parts)]
    if manifest and manifest.get("record_count") != len(session_files):
        errors.append(f"manifest record_count={manifest.get('record_count')} but found {len(session_files)} archive records")
    for path in [p for p in REPO.rglob("*") if p.is_file() and ".git" not in p.parts]:
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden file type: {path.relative_to(REPO)}")
            continue
        if path.stat().st_size > MAX_FILE:
            errors.append(f"oversized file: {path.relative_to(REPO)}")
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"secret candidate ({name}): {path.relative_to(REPO)}")
    diff = subprocess.run(["git", "diff", "--check"], cwd=REPO, capture_output=True, text=True)
    if diff.returncode:
        errors.append(diff.stdout.strip() or diff.stderr.strip())
    if errors:
        print("Archive verification failed:", file=sys.stderr)
        for error in errors[:100]:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Archive verified: {len(session_files)} recovery records; no forbidden files or secret candidates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
