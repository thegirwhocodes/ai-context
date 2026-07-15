---
name: feedback-deep-research-self
description: Do work yourself with direct tools; only spawn agents / Workflow if Naomi explicitly asks (or ask her first if fan-out would be materially more efficient)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 400bc972-a5a2-4e9d-a2f5-f3697bf0e69e
---

**Default to doing the work myself** with direct tools (WebSearch, Read, Bash, Edit, etc.). Do NOT spawn subagents or the multi-agent `Workflow` (incl. the `deep-research` harness) unless Naomi explicitly asks for it. If a fan-out would genuinely be much more efficient, I may ASK her first — but the default is solo. - 400bc972

**Specifically:** "do deep research" / "deep research into X" means *I* run a series of web searches myself, inline — NOT the `deep-research` Workflow. - 400bc972

**Why:** The Workflow fans out dozens of subagents and burns huge usage. Measured on one *partial* run (stopped early): 52 sub-agents, ~18.5M input tokens, ~122k output — roughly a full day of heavy coding in 7 minutes, ~100-300x more than me just searching myself. Naomi shares a usage pool with her brother and does not want to exhaust it. - 400bc972

**How to apply:** For research/multi-file tasks, do it inline (parallelize my own tool calls in one message). Reserve agents/Workflow for when she explicitly requests them. If a running workflow exists and she says "don't kill it," let it finish but salvage its `journal.jsonl` rather than re-running. Related: [[feedback_patience]], [[feedback_agent_output]].
