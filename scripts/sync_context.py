#!/usr/bin/env python3
"""Serialize export, verification, commit, pull/rebase, and push."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
LOCK = Path.home() / ".ai-context-sync.lock"


def run(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=REPO, capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or " ".join(args))
    return result


def acquire_lock() -> None:
    try:
        LOCK.mkdir()
    except FileExistsError:
        # A crashed hook must not block recovery forever.
        if LOCK.stat().st_mtime < datetime.now().timestamp() - 1800:
            shutil.rmtree(LOCK)
            LOCK.mkdir()
        else:
            raise RuntimeError("another ai-context sync is already running")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-export", action="store_true")
    parser.add_argument("--pull-only", action="store_true")
    args = parser.parse_args()
    acquire_lock()
    try:
        if args.pull_only:
            run(["git", "pull", "--ff-only"])
            return 0
        # Reconcile remote changes before generating deterministic local files.
        if not run(["git", "status", "--porcelain"], check=True).stdout.strip():
            run(["git", "pull", "--ff-only"])
        if not args.no_export:
            run([sys.executable, str(REPO / "scripts" / "export_context.py"), "--all"])
        run([sys.executable, str(REPO / "scripts" / "verify_archive.py")])
        scanner = shutil.which("gitleaks")
        if scanner:
            run([scanner, "dir", ".", "--no-banner", "--redact"])
        run(["git", "add", "-A"])
        staged = run(["git", "diff", "--cached", "--quiet"], check=False)
        if staged.returncode:
            message = f"Sync context {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            run(["git", "commit", "-m", message])
        run(["git", "pull", "--rebase"])
        run(["git", "push", "origin", "main"])
        print("ai-context synchronized")
        return 0
    finally:
        shutil.rmtree(LOCK, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
