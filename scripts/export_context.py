#!/usr/bin/env python3
"""Export redacted, recovery-ready Claude and Codex context.

Raw provider transcripts are treated as an unstable local source format. Only
visible user/assistant messages, final subagent reports, and curated text
memory/research are written to this repository.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


HOME = Path.home()
REPO = Path(__file__).resolve().parents[1]
PROJECTS = REPO / "projects"
CLAUDE_PROJECTS = HOME / ".claude" / "projects"
CODEX_STORES = (HOME / ".codex" / "sessions", HOME / ".codex" / "archived_sessions")
MAX_CURATED_FILE = 10 * 1024 * 1024
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".toml"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "unknown-project"


def project_slug_from_cwd(cwd: str | None) -> str:
    if not cwd:
        return "unknown-project"
    path = Path(cwd)
    try:
        rel = path.relative_to(HOME)
        first = rel.parts[0] if rel.parts else path.name
    except ValueError:
        first = path.name
    # Treat the Cortex umbrella folder and its worktrees/apps as one project.
    if first.lower() == "cortex":
        return "cortex"
    return slugify(first)


def project_slug_from_claude_dir(name: str) -> str:
    prefix = f"-{slugify(HOME.as_posix()).replace('-', '-')}"
    known_prefix = f"-Users-{HOME.name}-"
    if name.startswith(known_prefix):
        return slugify(name[len(known_prefix):])
    if name == f"-Users-{HOME.name}":
        return "home"
    # Claude's encoding is lossy; this still gives a stable private-repo slug.
    return slugify(name.lstrip("-"))


class Redactor:
    """Conservative, auditable secret redaction with counts but no values."""

    def __init__(self) -> None:
        self.counts: Counter[str] = Counter()
        self.patterns: list[tuple[str, re.Pattern[str]]] = [
            ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)),
            ("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{16,}")),
            ("openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
            ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
            ("stripe-secret", re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}")),
            ("runpod-key", re.compile(r"\brpa_[A-Za-z0-9_-]{16,}")),
            ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
            ("huggingface-token", re.compile(r"\bhf_[A-Za-z0-9]{20,}")),
            ("groq-key", re.compile(r"\bgsk_[A-Za-z0-9]{20,}")),
            ("google-api-key", re.compile(r"\bAIza[A-Za-z0-9_-]{30,}")),
            ("notion-token", re.compile(r"\b(?:secret|ntn)_[A-Za-z0-9]{20,}")),
            ("sentry-user-token", re.compile(r"\bsntryu_[A-Za-z0-9_-]{20,}")),
            ("clerk-key", re.compile(r"\bpk_(?:live|test)_[A-Za-z0-9_-]{20,}")),
            ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
            ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
            ("bearer-token", re.compile(r"(?i)(Authorization\s*:\s*Bearer\s+)[A-Za-z0-9._~+/-]{12,}")),
            ("header-credential", re.compile(r"(?i)((?:X-API-Key|apiKey|X-Auth-Token)\s*:\s*)[A-Za-z0-9._~+/-]{8,}")),
            ("sensitive-label", re.compile(r"(?i)(\b(?:API|API[ _-]?Key|Auth(?:entication)?[ _-]?Token|Access[ _-]?Token|Secret|Password)\b\s*[:=,]\s*(?:`{1,3}\s*)?)[A-Za-z0-9._~+/-]{12,}")),
            ("meta-token", re.compile(r"\bEA[A-Za-z0-9]{40,}")),
        ]
        self.assignment = re.compile(
            r"(?i)\b([A-Z][A-Z0-9_]*(?:API_KEY|ACCESS_KEY|ACCESS_TOKEN|REFRESH_TOKEN|TOKEN|SECRET|PASSWORD|PRIVATE_KEY))"
            r"(\s*[\"']?\s*[:=]\s*[\"']?)([^\s\"'`,;]{8,})"
        )

    def redact(self, text: str) -> str:
        if not text:
            return text
        for name, pattern in self.patterns:
            def replace(match: re.Match[str], label: str = name) -> str:
                self.counts[label] += 1
                if label in {"bearer-token", "header-credential", "sensitive-label"}:
                    return f"{match.group(1)}[REDACTED:{label}]"
                return f"[REDACTED:{label}]"
            text = pattern.sub(replace, text)

        def replace_assignment(match: re.Match[str]) -> str:
            label = slugify(match.group(1))
            self.counts[f"assignment:{label}"] += 1
            return f"{match.group(1)}{match.group(2)}[REDACTED:{label}]"

        text = self.assignment.sub(replace_assignment, text)
        # Generated Markdown must remain verifier-clean even when a transcript
        # contains spaces or tabs at the ends of user-authored lines.
        return re.sub(r"[ \t]+$", "", text, flags=re.M)


REDACTOR = Redactor()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def fmt_ts(value: str | None) -> str:
    return value or ""


def first_line(text: str, limit: int = 120) -> str:
    line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    line = line.replace("|", "\\|")
    return line[:limit] + ("…" if len(line) > limit else "")


def read_json_lines(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                value = json.loads(line)
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
            if isinstance(value, dict):
                yield value


def claude_visible_text(content: Any) -> str:
    if isinstance(content, str):
        return REDACTOR.redact(content.strip())
    parts: list[str] = []
    if not isinstance(content, list):
        return ""
    for block in content:
        if isinstance(block, str):
            parts.append(block)
        elif isinstance(block, dict):
            kind = block.get("type")
            if kind == "text":
                parts.append(str(block.get("text", "")))
            elif kind == "tool_use":
                parts.append(f"[Tool: {block.get('name', 'unknown')}]")
    return REDACTOR.redact("\n".join(part for part in parts if part).strip())


def parse_claude(path: Path) -> tuple[list[dict[str, str]], dict[str, Any]]:
    messages: list[dict[str, str]] = []
    for entry in read_json_lines(path):
        kind = entry.get("type")
        if kind not in ("user", "assistant"):
            continue
        message = entry.get("message") or {}
        if not isinstance(message, dict):
            continue
        text = claude_visible_text(message.get("content", ""))
        if not text:
            continue
        role = str(message.get("role") or kind)
        item = {"role": role, "text": text, "timestamp": str(entry.get("timestamp") or "")}
        if messages and item == messages[-1]:
            continue
        messages.append(item)
    meta = {
        "session_id": path.stem,
        "source": "claude",
        "started": messages[0]["timestamp"] if messages else "",
        "ended": messages[-1]["timestamp"] if messages else "",
        "thread_source": "user",
    }
    return messages, meta


def parse_codex(path: Path) -> tuple[list[dict[str, str]], dict[str, Any]]:
    messages: list[dict[str, str]] = []
    meta: dict[str, Any] = {"session_id": path.stem, "source": "codex"}
    for entry in read_json_lines(path):
        kind = entry.get("type")
        payload = entry.get("payload")
        if not isinstance(payload, dict):
            continue
        if kind == "session_meta" and not meta.get("cwd"):
            meta.update({
                "session_id": payload.get("id") or payload.get("session_id") or path.stem,
                "cwd": payload.get("cwd") or "",
                "started": payload.get("timestamp") or entry.get("timestamp") or "",
                "thread_source": payload.get("thread_source"),
                "originator": payload.get("originator") or "",
                "spawn_source": payload.get("source"),
            })
            continue
        if kind != "event_msg":
            continue
        event_type = payload.get("type")
        role = ""
        text = ""
        phase = ""
        if event_type == "user_message":
            role = "user"
            text = str(payload.get("message") or "")
            image_count = len(payload.get("images") or []) + len(payload.get("local_images") or [])
            if image_count:
                text += f"\n\n[Attached images omitted from Git archive: {image_count}]"
        elif event_type == "agent_message":
            role = "assistant"
            text = str(payload.get("message") or "")
            phase = str(payload.get("phase") or "")
        if not role or not text.strip():
            continue
        item = {
            "role": role,
            "text": REDACTOR.redact(text.strip()),
            "timestamp": str(entry.get("timestamp") or ""),
            "phase": phase,
        }
        if messages and item == messages[-1]:
            continue
        messages.append(item)
    if messages:
        meta.setdefault("started", messages[0]["timestamp"])
        meta["ended"] = messages[-1]["timestamp"]
    if not meta.get("thread_source"):
        source = meta.get("spawn_source")
        meta["thread_source"] = "subagent" if isinstance(source, dict) and "subagent" in source else "user"
    return messages, meta


def yaml_value(value: Any) -> str:
    return json.dumps(value if value is not None else "", ensure_ascii=False)


def render_session(messages: list[dict[str, str]], meta: dict[str, Any], project: str) -> str:
    lines = [
        "---",
        f"session_id: {yaml_value(meta.get('session_id'))}",
        f"source: {yaml_value(meta.get('source'))}",
        f"project: {yaml_value(project)}",
        f"started: {yaml_value(meta.get('started'))}",
        f"ended: {yaml_value(meta.get('ended'))}",
        f"cwd: {yaml_value(meta.get('cwd', ''))}",
        f"thread_source: {yaml_value(meta.get('thread_source', 'user'))}",
        "---",
        "",
        f"# Session {meta.get('session_id')}",
        "",
    ]
    for message in messages:
        label = "Naomi" if message["role"] == "user" else str(meta.get("source", "agent")).title()
        phase = f" · {message.get('phase')}" if message.get("phase") else ""
        lines.extend([
            f"## {label} · {fmt_ts(message.get('timestamp'))}{phase}",
            "",
            message["text"],
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def codex_agent_details(meta: dict[str, Any]) -> tuple[str, str, str]:
    source = meta.get("spawn_source")
    if not isinstance(source, dict):
        return "", "", ""
    subagent = source.get("subagent")
    if not isinstance(subagent, dict):
        return "", "", ""
    spawn = subagent.get("thread_spawn")
    if not isinstance(spawn, dict):
        return "", "", ""
    return (
        str(spawn.get("parent_thread_id") or ""),
        str(spawn.get("agent_path") or ""),
        str(spawn.get("agent_nickname") or ""),
    )


def render_subagent(messages: list[dict[str, str]], meta: dict[str, Any], project: str) -> str:
    finals = [m for m in messages if m["role"] == "assistant" and m.get("phase") == "final"]
    assistant = finals[-1] if finals else next((m for m in reversed(messages) if m["role"] == "assistant"), None)
    if not assistant:
        return ""
    parent, agent_path, nickname = codex_agent_details(meta)
    return "\n".join([
        "---",
        f"session_id: {yaml_value(meta.get('session_id'))}",
        "source: \"codex-subagent\"",
        f"project: {yaml_value(project)}",
        f"parent_session_id: {yaml_value(parent)}",
        f"agent_path: {yaml_value(agent_path)}",
        f"nickname: {yaml_value(nickname)}",
        f"ended: {yaml_value(meta.get('ended'))}",
        "---",
        "",
        f"# Codex subagent report: {agent_path or nickname or meta.get('session_id')}",
        "",
        assistant["text"],
        "",
    ])


def export_claude_file(path: Path) -> dict[str, Any] | None:
    messages, meta = parse_claude(path)
    if not messages:
        return None
    project_dir = path.parent.name
    slug = project_slug_from_claude_dir(project_dir)
    meta["cwd"] = project_dir
    out = PROJECTS / slug / "sessions" / "claude" / f"{path.stem}.md"
    atomic_write(out, render_session(messages, meta, slug))
    return {**meta, "project": slug, "path": str(out.relative_to(REPO)), "title": first_line(next((m["text"] for m in messages if m["role"] == "user"), "")), "message_count": len(messages)}


def export_codex_file(path: Path) -> dict[str, Any] | None:
    messages, meta = parse_codex(path)
    if not messages:
        return None
    slug = project_slug_from_cwd(str(meta.get("cwd") or ""))
    session_id = str(meta.get("session_id") or path.stem)
    if meta.get("thread_source") == "subagent":
        rendered = render_subagent(messages, meta, slug)
        if not rendered:
            return None
        out = PROJECTS / slug / "research" / "codex-subagents" / f"{session_id}.md"
        atomic_write(out, rendered)
        kind = "codex-subagent"
        title = first_line(rendered.split("---", 2)[-1])
    else:
        out = PROJECTS / slug / "sessions" / "codex" / f"{session_id}.md"
        atomic_write(out, render_session(messages, meta, slug))
        kind = "codex"
        title = first_line(next((m["text"] for m in messages if m["role"] == "user"), ""))
    return {**meta, "source": kind, "project": slug, "path": str(out.relative_to(REPO)), "title": title, "message_count": len(messages)}


def copy_curated_tree(source: Path, destination: Path) -> int:
    if not source.is_dir():
        return 0
    copied = 0
    for path in source.rglob("*"):
        if not path.is_file() or path.name.startswith(".") or path.name == "memory_build_context.txt":
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > MAX_CURATED_FILE:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        relative = path.relative_to(source)
        atomic_write(destination / relative, REDACTOR.redact(content))
        copied += 1
    return copied


def export_curated() -> int:
    copied = 0
    if CLAUDE_PROJECTS.is_dir():
        for project in CLAUDE_PROJECTS.iterdir():
            if not project.is_dir():
                continue
            slug = project_slug_from_claude_dir(project.name)
            copied += copy_curated_tree(project / "memory", PROJECTS / slug / "memory" / "claude")
            copied += copy_curated_tree(project / "agent-research", PROJECTS / slug / "research" / "claude")
    codex_projects = HOME / ".codex" / "projects"
    if codex_projects.is_dir():
        for project in codex_projects.iterdir():
            if not project.is_dir():
                continue
            slug = project_slug_from_claude_dir(project.name)
            copied += copy_curated_tree(project / "memory", PROJECTS / slug / "memory" / "codex")
    return copied


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
REDACTION_MARKER_RE = re.compile(r"\[REDACTED:([^\]]+)\]")


def read_archive_meta(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        try:
            value = json.loads(raw.strip())
        except json.JSONDecodeError:
            value = raw.strip()
        data[key] = str(value)
    return data


def archive_redaction_counts() -> Counter[str]:
    """Count markers in the durable archive, independent of deleted raw sources."""
    counts: Counter[str] = Counter()
    if not PROJECTS.is_dir():
        return counts
    for path in PROJECTS.rglob("*"):
        if not path.is_file() or path.name == "INDEX.md":
            continue
        try:
            counts.update(REDACTION_MARKER_RE.findall(path.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            continue
    return counts


def archive_curated_count() -> int:
    """Count durable memory/research files rather than files copied in this run."""
    count = 0
    if not PROJECTS.is_dir():
        return count
    for path in PROJECTS.rglob("*"):
        if not path.is_file():
            continue
        parts = path.relative_to(PROJECTS).parts
        if len(parts) >= 3 and parts[1] == "memory":
            count += 1
        elif len(parts) >= 3 and parts[1] == "research" and parts[2] != "codex-subagents":
            count += 1
    return count


def generate_indexes(records: list[dict[str, Any]], curated_count: int) -> dict[str, Any]:
    all_records: list[dict[str, Any]] = []
    for path in PROJECTS.glob("*/sessions/*/*.md"):
        meta = read_archive_meta(path)
        if meta:
            all_records.append({**meta, "path": str(path.relative_to(REPO))})
    for path in PROJECTS.glob("*/research/codex-subagents/*.md"):
        meta = read_archive_meta(path)
        if meta:
            all_records.append({**meta, "path": str(path.relative_to(REPO))})

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in all_records:
        grouped[record.get("project", "unknown-project")].append(record)

    recovery = [
        "# Recovery index",
        "",
        f"Generated: {now_iso()}",
        "",
        "GitHub is the source of truth. Pull this repository before recovery.",
        "Read the relevant project index and curated memory first; open full session files only when needed.",
        "",
        "## Projects",
        "",
    ]
    project_summaries: dict[str, Any] = {}
    for project, items in sorted(grouped.items()):
        items.sort(key=lambda item: item.get("started") or item.get("ended") or "", reverse=True)
        source_counts = Counter(item.get("source", "unknown") for item in items)
        project_summaries[project] = {"records": len(items), "sources": dict(source_counts)}
        recovery.append(f"- [{project}](projects/{project}/INDEX.md) — {len(items)} records")
        index = [f"# {project} context", "", "| Date | Source | Session |", "|---|---|---|"]
        for item in items:
            date = (item.get("started") or item.get("ended") or "")[:19]
            source = item.get("source", "")
            relative = Path(item["path"]).relative_to(Path("projects") / project)
            session = item.get("session_id", relative.stem)
            index.append(f"| {date} | {source} | [{session}]({relative.as_posix()}) |")
        atomic_write(PROJECTS / project / "INDEX.md", "\n".join(index) + "\n")
    atomic_write(REPO / "RECOVERY.md", "\n".join(recovery) + "\n")

    durable_redactions = archive_redaction_counts()
    durable_curated_count = archive_curated_count()
    manifest = {
        "generated_at": now_iso(),
        "project_count": len(grouped),
        "record_count": len(all_records),
        "projects": project_summaries,
        "curated_files_copied": durable_curated_count,
        "redactions": dict(sorted(durable_redactions.items())),
    }
    atomic_write(REPO / "MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    atomic_write(REPO / "REDACTION_REPORT.json", json.dumps({"generated_at": now_iso(), "counts": dict(sorted(durable_redactions.items()))}, indent=2, sort_keys=True) + "\n")
    return manifest


def newest_by_session(paths: Iterable[Path]) -> list[Path]:
    selected: dict[str, Path] = {}
    for path in paths:
        current = selected.get(path.stem)
        if current is None or path.stat().st_mtime > current.stat().st_mtime:
            selected[path.stem] = path
    return list(selected.values())


def export_all() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    if CLAUDE_PROJECTS.is_dir():
        for path in sorted(CLAUDE_PROJECTS.glob("*/*.jsonl")):
            record = export_claude_file(path)
            if record:
                records.append(record)
    codex_paths: list[Path] = []
    for store in CODEX_STORES:
        if store.is_dir():
            codex_paths.extend(store.rglob("*.jsonl"))
    for path in sorted(newest_by_session(codex_paths)):
        record = export_codex_file(path)
        if record:
            records.append(record)
    curated = export_curated()
    return generate_indexes(records, curated)


def export_one(path: Path) -> dict[str, Any]:
    if ".codex" in path.parts:
        record = export_codex_file(path)
    else:
        record = export_claude_file(path)
    if not record:
        raise RuntimeError(f"No visible recovery messages in {path}")
    return generate_indexes([record], 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="export every local project")
    parser.add_argument("--transcript", type=Path, help="export one exact hook transcript")
    args = parser.parse_args()
    if args.transcript:
        manifest = export_one(args.transcript.expanduser())
    elif args.all:
        manifest = export_all()
    else:
        parser.error("choose --all or --transcript")
    print(json.dumps({"projects": manifest["project_count"], "records": manifest["record_count"], "redactions": sum(manifest["redactions"].values())}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
