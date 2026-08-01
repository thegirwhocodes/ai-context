---
name: terminal-open-bypass-permissions-default
description: "When opening claude CLI terminals for Naomi, always launch with --dangerously-skip-permissions by default"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9af50e67-d4e1-4ae4-8f53-bd53883325fd
  modified: 2026-08-01T22:56:38.865Z
---

When opening a `claude` CLI terminal for Naomi, always launch with `--dangerously-skip-permissions` so she does not have to enable bypass mode manually inside each session.

**Why:** On 2026-08-01 she said "from now on when I tell you to open them, set them to bypass permissions don't make me tell you". She already runs bypass-permissions mode globally (per her CLAUDE.md) and does not want per-terminal friction.

**How to apply:**
- Default the launch command to `cd <target-dir> && claude --dangerously-skip-permissions`.
- Combines with [[feedback_terminal_open_trust]] — the flag also skips the workspace trust dialog, so no keystroke follow-up is needed.
- Related: [[feedback_ask_first]], [[feedback_terminal_open_trust]].
