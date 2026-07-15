---
name: Must re-read session transcript after compaction
description: Critical failure case — Claude lost context after compaction and gave wrong answers, duplicated work
type: feedback
---

After compaction, ALWAYS re-read your full session transcript before responding. No exceptions.

**Why:** In session e59a15e2, Claude compacted mid-conversation and then:
- Told the user "nothing is automatic" when a hook-based auto-export system was already set up earlier in the same session
- Rewrote CLAUDE.md files that had already been carefully iterated through 10+ rounds of feedback
- Dropped the WebSearch/WebFetch distinction that was explicitly requested
- Duplicated work that was already done (chaining scripts to export_all_sessions.py when the hook already handled it)
This wasted significant time and eroded trust.

**How to apply:** The PostCompact hook now injects a mandatory reminder into context. But even without the hook — if you notice gaps in your memory, if the user says "didn't we already do this?", or if something feels unfamiliar — stop and read .claude-sessions/ before continuing. The transcript has everything. Your compacted memory does not.
