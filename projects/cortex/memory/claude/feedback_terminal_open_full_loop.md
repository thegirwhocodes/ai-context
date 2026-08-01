---
name: terminal-open-full-loop-to-ready
description: "When opening claude terminals, always take them through the full setup loop until they are ready for the first user message"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9af50e67-d4e1-4ae4-8f53-bd53883325fd
  modified: 2026-08-01T23:03:02.770Z
---

When Naomi asks to open a `claude` CLI terminal, the terminal must arrive fully ready for her first typed message — not stuck at a trust prompt, not in the wrong directory, not requiring permission-mode toggling. Take it all the way through the setup loop before considering the task done.

**Why:** On 2026-08-01 after multiple terminal-open attempts left windows unusable (wrong dir, trust prompt open, permission mode not bypass), she said "always take them through the whole loop until they're ready for the first message". Half-open terminals waste her time and require her to fix them one by one.

**How to apply:**
- Launch each terminal with the full command: `cd <target-dir> && claude --dangerously-skip-permissions`.
- `--dangerously-skip-permissions` skips both the trust dialog and permission prompts — the session lands directly at the input prompt.
- Verify (list ttys, brief pause, or screenshot) that each window is actually at the ready state before reporting complete.
- If any window still has a prompt sitting open, address it before finishing.
- Related: [[feedback_ask_first]], [[feedback_terminal_open_trust]], [[feedback_terminal_open_bypass]].
