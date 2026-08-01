---
name: terminal-open-auto-trust-folder
description: "When opening claude terminals for Naomi, auto-answer the \"trust this folder\" prompt so windows are usable"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9af50e67-d4e1-4ae4-8f53-bd53883325fd
  modified: 2026-08-01T22:53:01.895Z
---

When Naomi asks to open a `claude` CLI terminal, always take it through the initial "Do you trust the files in this folder?" prompt so the window arrives fully usable — she should not have to click into each window and answer yes.

**Why:** On 2026-08-01, after opening 6 Terminal windows with `cd /path && claude`, every window was stuck at the trust prompt. She said: "from now on when I tell you to open, take them through the 'yes I trust this folder'". Unanswered prompts make a batch of terminals useless.

**How to apply:**
- After launching the shell command in a new Terminal window, send the "yes" + Return keystrokes via `osascript`/System Events to the newly-created window before moving on.
- Verify (`ps` on the tty, or brief pause + screenshot) that the prompt actually cleared.
- If macOS accessibility/automation permission blocks the keystroke path, stop and tell Naomi — do not silently leave prompts unanswered.
- Related: [[feedback_ask_first]].
