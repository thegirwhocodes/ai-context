#!/usr/bin/env python3
"""Rebuild compact, sidebar-compatible Codex JSONL from redacted archives.

The generated files contain only the durable user/assistant text already stored
in this private repository. They intentionally omit tool output, reasoning,
attachments, credentials, and injected runtime instructions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


HOME = Path.home()
REPO = Path(__file__).resolve().parents[1]
DEFAULT_CODEX_HOME = HOME / ".codex"
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
SECTION_RE = re.compile(
    r"^## (Naomi|Codex) · ([^\n·]+?)(?: · ([^\n]+))?\n\n",
    re.M,
)
SESSION_ID_RE = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.I,
)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        try:
            value = json.loads(raw.strip())
        except json.JSONDecodeError:
            value = raw.strip()
        result[key.strip()] = str(value)
    return result


def parse_messages(text: str) -> list[dict[str, str]]:
    matches = list(SECTION_RE.finditer(text))
    messages: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end].rstrip()
        if not body:
            continue
        messages.append(
            {
                "role": "user" if match.group(1) == "Naomi" else "assistant",
                "timestamp": match.group(2).strip(),
                "phase": (match.group(3) or "").strip(),
                "text": body,
            }
        )
    return messages


def parse_user_worker_messages(
    text: str,
    meta: dict[str, str],
    title: str,
) -> list[dict[str, str]]:
    """Turn a user-owned worker's saved report into a transparent compact task."""
    match = FRONTMATTER_RE.match(text)
    body = text[match.end():] if match else text
    report = body.strip()
    if not report:
        return []
    session_id = meta["session_id"]
    started = parse_timestamp("", session_id)
    started_iso = started.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return [
        {
            "role": "user",
            "timestamp": started_iso,
            "phase": "",
            "text": (
                f"[Recovered worker task] {title}\n\n"
                "This compact task was rebuilt from the redacted GitHub recovery archive. "
                "Its original delegation prompt remains summarized in the parent lead task."
            ),
        },
        {
            "role": "assistant",
            "timestamp": meta.get("ended", "") or started_iso,
            "phase": "final_answer",
            "text": report,
        },
    ]


def parse_timestamp(value: str, session_id: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        # Codex session IDs are UUIDv7; their first 48 bits are Unix milliseconds.
        millis = int(session_id.replace("-", "")[:12], 16)
        return datetime.fromtimestamp(millis / 1000, timezone.utc)


def load_rollout_paths(state_db: Path) -> dict[str, str]:
    if not state_db.is_file():
        return {}
    try:
        with sqlite3.connect(f"file:{state_db}?mode=ro", uri=True) as connection:
            return dict(connection.execute("SELECT id, rollout_path FROM threads"))
    except (sqlite3.Error, OSError):
        return {}


def existing_session_ids(codex_home: Path) -> set[str]:
    found: set[str] = set()
    for directory in (codex_home / "sessions", codex_home / "archived_sessions"):
        if not directory.is_dir():
            continue
        for path in directory.rglob("*.jsonl"):
            match = SESSION_ID_RE.search(path.name)
            if match:
                found.add(match.group(0).lower())
    return found


def existing_session_paths(codex_home: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for directory in (codex_home / "sessions", codex_home / "archived_sessions"):
        if not directory.is_dir():
            continue
        for path in directory.rglob("*.jsonl"):
            match = SESSION_ID_RE.search(path.name)
            if match:
                found[match.group(0).lower()] = path
    return found


def destination_path(
    session_id: str,
    started: datetime,
    codex_home: Path,
    rollout_paths: dict[str, str],
) -> Path:
    known = rollout_paths.get(session_id)
    if known:
        known_path = Path(known).expanduser()
        try:
            relative = known_path.relative_to(DEFAULT_CODEX_HOME)
            return codex_home / relative
        except ValueError:
            pass
    local = started.astimezone(ZoneInfo("America/New_York"))
    filename = f"rollout-{local:%Y-%m-%dT%H-%M-%S}-{session_id}.jsonl"
    return codex_home / "sessions" / f"{local:%Y}" / f"{local:%m}" / f"{local:%d}" / filename


def stable_message_id(session_id: str, index: int) -> str:
    digest = hashlib.sha256(f"{session_id}:{index}".encode()).hexdigest()[:48]
    return f"msg_{digest}"


def render_jsonl(meta: dict[str, str], messages: list[dict[str, str]]) -> str:
    session_id = meta["session_id"]
    started = parse_timestamp(meta.get("started", ""), session_id)
    started_iso = started.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    records: list[dict[str, Any]] = [
        {
            "timestamp": started_iso,
            "type": "session_meta",
            "payload": {
                "id": session_id,
                "session_id": session_id,
                "timestamp": started_iso,
                "cwd": meta.get("cwd") or str(HOME),
                "originator": "Codex Desktop",
                "cli_version": "0.144.5",
                "source": "vscode",
                "thread_source": meta.get("thread_source") or "user",
                "model_provider": "openai",
            },
        }
    ]
    for index, message in enumerate(messages):
        timestamp = message["timestamp"] or started_iso
        if message["role"] == "user":
            records.append(
                {
                    "timestamp": timestamp,
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "client_id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"{session_id}:{index}")),
                        "message": message["text"],
                        "images": [],
                        "local_images": [],
                        "text_elements": [],
                    },
                }
            )
        else:
            phase = message["phase"] or "final_answer"
            records.append(
                {
                    "timestamp": timestamp,
                    "type": "event_msg",
                    "payload": {
                        "type": "agent_message",
                        "message": message["text"],
                        "phase": phase,
                        "memory_citation": None,
                    },
                }
            )
            records.append(
                {
                    "timestamp": timestamp,
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "id": stable_message_id(session_id, index),
                        "role": "assistant",
                        "content": [{"type": "output_text", "text": message["text"]}],
                        "phase": phase,
                    },
                }
            )
    return "".join(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n" for record in records)


def load_archive(
    archive: Path,
    titles: dict[str, str],
) -> tuple[dict[str, str], list[dict[str, str]]] | None:
    text = archive.read_text(encoding="utf-8", errors="replace")
    meta = parse_frontmatter(text)
    session_id = meta.get("session_id", "").lower()
    if not SESSION_ID_RE.fullmatch(session_id):
        return None
    meta["session_id"] = session_id

    if meta.get("source") != "codex-subagent":
        return meta, parse_messages(text)

    # Internal collaboration subagents were never standalone sidebar tasks.
    # A blank parent_session_id plus a session-index title identifies the
    # user-owned worker tasks created through the Codex app.
    title = titles.get(session_id)
    if meta.get("parent_session_id") or not title:
        return None
    project = meta.get("project", "")
    project_dir = HOME / project if project else HOME
    meta["cwd"] = str(project_dir if project_dir.is_dir() else HOME)
    meta["thread_source"] = "user"
    return meta, parse_user_worker_messages(text, meta, title)


def restorable_archives(archive_root: Path) -> list[Path]:
    return sorted(
        list(archive_root.glob("*/sessions/codex/*.md"))
        + list(archive_root.glob("*/research/codex-subagents/*.md"))
    )


def restore(args: argparse.Namespace) -> dict[str, int]:
    codex_home = args.codex_home.expanduser().resolve()
    archive_root = args.archive_root.expanduser().resolve()
    state_db = args.state_db.expanduser().resolve()
    rollout_paths = load_rollout_paths(state_db)
    existing = existing_session_ids(codex_home)
    titles = latest_session_titles(codex_home / "session_index.jsonl")
    selected = {value.lower() for value in args.session_id}
    counts = {"archives": 0, "created": 0, "existing": 0, "invalid": 0, "skipped": 0}

    paths = restorable_archives(archive_root)
    if args.limit:
        paths = paths[: args.limit]
    for archive in paths:
        loaded = load_archive(archive, titles)
        if loaded is None:
            counts["skipped"] += 1
            continue
        meta, messages = loaded
        session_id = meta["session_id"]
        if selected and session_id not in selected:
            counts["skipped"] += 1
            continue
        counts["archives"] += 1
        if not messages:
            counts["invalid"] += 1
            continue
        if session_id in existing:
            counts["existing"] += 1
            continue
        started = parse_timestamp(meta.get("started", ""), session_id)
        output = destination_path(session_id, started, codex_home, rollout_paths)
        if args.apply:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(render_jsonl(meta, messages), encoding="utf-8")
            output.chmod(0o600)
            ended_value = meta.get("ended") or messages[-1]["timestamp"] or meta.get("started", "")
            ended_epoch = parse_timestamp(ended_value, session_id).timestamp()
            os.utime(output, (ended_epoch, ended_epoch))
        counts["created"] += 1
    return counts


def latest_session_titles(path: Path) -> dict[str, str]:
    titles: dict[str, tuple[str, str]] = {}
    if not path.is_file():
        return {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        session_id = str(item.get("id") or "").lower()
        title = str(item.get("thread_name") or "").strip()
        updated = str(item.get("updated_at") or "")
        if SESSION_ID_RE.fullmatch(session_id) and title and updated >= titles.get(session_id, ("", ""))[0]:
            titles[session_id] = (updated, title)
    return {session_id: value[1] for session_id, value in titles.items()}


def repair_restored_state(args: argparse.Namespace) -> int:
    """Restore dates/titles only for files byte-identical to this generator."""
    codex_home = args.codex_home.expanduser().resolve()
    state_db = args.state_db.expanduser().resolve()
    existing = existing_session_paths(codex_home)
    titles = latest_session_titles(codex_home / "session_index.jsonl")
    selected = {value.lower() for value in args.session_id}
    repairs: list[tuple[str, int, str | None]] = []

    for archive in restorable_archives(args.archive_root.expanduser().resolve()):
        loaded = load_archive(archive, titles)
        if loaded is None:
            continue
        meta, messages = loaded
        session_id = meta["session_id"]
        if selected and session_id not in selected:
            continue
        path = existing.get(session_id)
        if not path or not messages or path.read_text(encoding="utf-8", errors="replace") != render_jsonl(meta, messages):
            continue
        ended_value = meta.get("ended") or messages[-1]["timestamp"] or meta.get("started", "")
        ended_epoch = int(parse_timestamp(ended_value, session_id).timestamp())
        os.utime(path, (ended_epoch, ended_epoch))
        repairs.append((session_id, ended_epoch, titles.get(session_id)))

    if not repairs or not state_db.is_file():
        return len(repairs)

    backup_dir = HOME / ".secrets" / "ai-context-config-backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"state_5-before-sidebar-repair-{datetime.now():%Y%m%d-%H%M%S}.sqlite"
    with sqlite3.connect(state_db) as source, sqlite3.connect(backup_path) as backup:
        source.backup(backup)
        for session_id, ended_epoch, title in repairs:
            if title:
                source.execute(
                    "UPDATE threads SET updated_at=?, updated_at_ms=?, recency_at=?, recency_at_ms=?, title=? WHERE id=?",
                    (ended_epoch, ended_epoch * 1000, ended_epoch, ended_epoch * 1000, title, session_id),
                )
            else:
                source.execute(
                    "UPDATE threads SET updated_at=?, updated_at_ms=?, recency_at=?, recency_at_ms=? WHERE id=?",
                    (ended_epoch, ended_epoch * 1000, ended_epoch, ended_epoch * 1000, session_id),
                )
        source.commit()
    return len(repairs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write reconstructed JSONL; default is a dry run")
    parser.add_argument("--codex-home", type=Path, default=DEFAULT_CODEX_HOME)
    parser.add_argument("--archive-root", type=Path, default=REPO / "projects")
    parser.add_argument("--state-db", type=Path, default=DEFAULT_CODEX_HOME / "state_5.sqlite")
    parser.add_argument("--limit", type=int, default=0, help="limit archives for isolated testing")
    parser.add_argument(
        "--session-id",
        action="append",
        default=[],
        help="restore only this session ID; may be supplied more than once",
    )
    parser.add_argument("--repair-state", action="store_true", help="repair dates/titles for reconstructed sessions")
    args = parser.parse_args()
    counts = restore(args)
    counts["state_repaired"] = repair_restored_state(args) if args.repair_state else 0
    counts["dry_run"] = int(not args.apply)
    print(json.dumps(counts, sort_keys=True))
    return 1 if counts["invalid"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
