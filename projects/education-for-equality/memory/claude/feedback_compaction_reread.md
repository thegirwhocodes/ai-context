---
name: Must re-read FULL session transcript after compaction
description: Critical failure case — Claudes have repeatedly skipped or shortcut the post-compaction re-read and given wrong answers. Read the ENTIRE file, every line, no rationalizing.
type: feedback
originSessionId: 32030cb5-c0ef-4006-a1f9-d25bc9ad27b0
---
After compaction, STOP and read your ENTIRE session transcript from `.claude-sessions/` before responding to anything — even "hello." No exceptions.

**Why (incidents, oldest first):**
- **Session e59a15e2** — Claude compacted mid-conversation, told user "nothing is automatic" when an auto-export hook was already set up earlier in that same session, rewrote CLAUDE.md files that had been iterated through 10+ rounds, dropped the WebSearch/WebFetch distinction the user explicitly requested, duplicated work.
- **Subsequent session** — a Claude read only the last 300 lines of the transcript and missed critical context from the early/middle of the session. Gave confident but wrong answers.
- **Pattern:** Claudes rationalize "the user's message is short so I don't need the full context" or "this file is really big, the tail is probably enough." Both are wrong. Naomi notices every time and it erodes trust.

**How to apply:**
1. Find your session ID in `.claude-sessions/INDEX.txt` (most recent entry).
2. Read that ENTIRE `.txt` file, start to finish, in chunks if needed. Do NOT stop at 2000 lines. Do NOT skip the middle. Do NOT read just the tail.
3. The SessionStart / PostCompact hook injects a reminder, but follow this rule even if the hook misfires.
4. Be patient. If recovery takes 5 minutes, take 5 minutes — Naomi would rather wait than get a fast wrong answer. She has said this verbatim multiple times and written it in all-caps in CLAUDE.md.
5. If you notice gaps in your memory, if Naomi says "didn't we already do this?", or if something feels unfamiliar — treat that as a compaction signal and re-read before continuing.
6. Your compacted summary is not a substitute for the transcript. The transcript has the exact decisions, the exact file paths, the exact phrasing of feedback. The summary loses all of that.

**What NOT to do:**
- Do not say "let me skim the recent part and catch up" — read the whole thing.
- Do not try to reconstruct context from memory files alone — memory is a curated subset, the transcript has the raw detail.
- Do not ask Naomi to summarize what happened — she has already written it in the transcript and does not want to re-explain.
