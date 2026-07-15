#!/usr/bin/env python3
"""Install global Claude/Codex hooks and a periodic launchd sync safely."""

from __future__ import annotations

import json
import plistlib
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


HOME = Path.home()
REPO = Path(__file__).resolve().parents[1]
BACKUPS = HOME / ".secrets" / "ai-context-config-backups"
HOOK_COMMAND = f"python3 {REPO / 'scripts' / 'hook_context.py'}"


def backup(path: Path) -> None:
    if not path.exists():
        return
    BACKUPS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(path, BACKUPS / f"{path.name}.{stamp}.bak")


def install_codex() -> None:
    target = HOME / ".codex" / "hooks.json"
    backup(target)
    source = REPO / "hooks" / "codex-hooks.json"
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def remove_old_context_hooks(groups: list[dict]) -> list[dict]:
    cleaned = []
    for group in groups:
        hooks = [h for h in group.get("hooks", []) if "hook_export_session.sh" not in h.get("command", "") and "ai-context/scripts/hook_context.py" not in h.get("command", "")]
        if hooks:
            copy = dict(group)
            copy["hooks"] = hooks
            cleaned.append(copy)
    return cleaned


def install_claude() -> None:
    target = HOME / ".claude" / "settings.json"
    backup(target)
    data = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    hooks = data.setdefault("hooks", {})
    for event in ("UserPromptSubmit", "Stop"):
        groups = remove_old_context_hooks(hooks.get(event, []))
        groups.append({"matcher": "", "hooks": [{"type": "command", "command": HOOK_COMMAND, "timeout": 120}]})
        hooks[event] = groups
    groups = remove_old_context_hooks(hooks.get("SessionStart", []))
    groups.append({"matcher": "startup|resume|clear|compact", "hooks": [{"type": "command", "command": HOOK_COMMAND, "timeout": 45}]})
    hooks["SessionStart"] = groups
    target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def install_launchd() -> None:
    target = HOME / "Library" / "LaunchAgents" / "com.thegirwhocodes.ai-context-sync.plist"
    backup(target)
    payload = {
        "Label": "com.thegirwhocodes.ai-context-sync",
        "ProgramArguments": ["/usr/bin/python3", str(REPO / "scripts" / "sync_context.py")],
        "RunAtLoad": True,
        "StartInterval": 1800,
        "EnvironmentVariables": {"HOME": str(HOME), "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"},
        "StandardOutPath": str(HOME / ".secrets" / "ai-context-sync.log"),
        "StandardErrorPath": str(HOME / ".secrets" / "ai-context-sync.log"),
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("wb") as handle:
        plistlib.dump(payload, handle)
    domain = f"gui/{subprocess.check_output(['id', '-u'], text=True).strip()}"
    subprocess.run(["launchctl", "bootout", domain, str(target)], check=False, capture_output=True)
    subprocess.run(["launchctl", "bootstrap", domain, str(target)], check=True)


def main() -> int:
    install_codex()
    install_claude()
    install_launchd()
    print("Installed Claude/Codex recovery hooks and 30-minute GitHub sync.")
    print("Codex will ask you to review/trust the new hook definition in /hooks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
