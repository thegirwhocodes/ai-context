---
name: claude-artifact-links-dont-work
description: "claude.ai/code/artifact/... links never work for this user — always also save a local file copy and open it"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1fa96259-56b5-4578-bed1-0d0d13e43f83
  modified: 2026-08-25T19:29:51.723Z
---

Claude.ai artifact page links (https://claude.ai/code/artifact/...) do not work for this user — she cannot open them. Never rely on the artifact link alone as the way to deliver a built page/tool.

**Why:** She said outright "claude page links never work." Earlier in the same session she also said "I can see - I can't see t[he artifact]" when only a link was given.

**How to apply:** Whenever publishing an HTML artifact for her (Artifact tool), ALWAYS also copy the file to a real local path (e.g. `~/Desktop/<name>.html`) and `open` it so it launches in her actual browser. Treat the local-file-plus-open step as mandatory, not optional, every single time — including on every redeploy/update of that artifact, not just the first publish. Do this before or alongside mentioning the claude.ai link, not as an afterthought only when she complains.
