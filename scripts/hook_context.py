#!/usr/bin/env python3
"""Shared lightweight lifecycle hook for Claude Code and Codex."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def detached_sync() -> None:
    log_dir = REPO / "local-logs"
    log_dir.mkdir(exist_ok=True)
    log = (log_dir / "hook-sync.log").open("ab")
    subprocess.Popen(
        [sys.executable, str(REPO / "scripts" / "sync_context.py"), "--no-export"],
        cwd=REPO,
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=log,
        start_new_session=True,
    )


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        payload = {}
    event = str(payload.get("hook_event_name") or "")
    transcript = payload.get("transcript_path")
    if transcript and Path(transcript).is_file():
        subprocess.run(
            [sys.executable, str(REPO / "scripts" / "export_context.py"), "--transcript", str(transcript)],
            cwd=REPO,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=120,
            check=False,
        )
        detached_sync()
    if event == "SessionStart":
        subprocess.run(
            [sys.executable, str(REPO / "scripts" / "sync_context.py"), "--pull-only"],
            cwd=REPO,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30,
            check=False,
        )
        print(
            "GitHub-backed recovery is at ~/ai-context/RECOVERY.md. "
            "Read the relevant project index and memory when prior context is needed. "
            "After compaction, use the exact session_id supplied by the hook rather than the newest file."
        )
    elif event in ("PostCompact", "PreCompact"):
        session_id = payload.get("session_id", "current")
        print(f"Context was exported before/after compaction. Recover exact session {session_id} through ~/ai-context/RECOVERY.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
