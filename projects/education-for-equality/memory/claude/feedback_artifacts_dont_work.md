---
name: feedback-artifacts-dont-work
description: "Claude Artifacts (published via the Artifact tool) don't work for Naomi in her actual setup — don't rely on them to deliver documents"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8db06326-4b4d-4049-9b7a-48ebcf0eced6
  modified: 2026-08-27T21:59:01.977Z
---

Naomi said directly: "claude artifacts dont work." She said this right after I published a government pilot proposal as an Artifact and handed her the link.

**Why:** Not fully diagnosed, but consistent with [[reference-antigravity-setup]] — she runs Claude Code as a VS Code extension *inside* Antigravity IDE, not Claude Code's native desktop/web/mobile clients. Artifact rendering (the `claude.ai/code/artifact/...` viewer) may not resolve or open correctly from that host environment.

**How to apply:** Don't default to `Artifact` for deliverables in her sessions. When a task calls for a polished document (proposals, reports, decks) that would normally become an Artifact, prefer writing it as a local file — `.html`/`.pdf`/`.md` in the project directory — and consider `SendUserFile` to hand it over directly, or ask her which format actually opens for her, before publishing another Artifact link that may not load. If she asks for an Artifact specifically or one already worked for her, follow her lead — this is about not defaulting to it, not never using it.
