---
name: reference-antigravity-setup
description: "Naomi's actual Antigravity setup — she runs Claude Code as a VS Code extension INSIDE Antigravity IDE, not Antigravity's native chat. Key paths, version state, and known performance traps."
metadata: 
  node_type: memory
  type: reference
  originSessionId: a4ea39cd-2bd1-4931-94a8-310dccbcb03d
---

Naomi uses Antigravity IDE primarily as a host for the **Claude Code VS Code extension** (`anthropic.claude-code` at `~/.antigravity-ide/extensions/anthropic.claude-code-<version>-darwin-arm64/`). She's NOT using Antigravity's native Gemini chat — her MCP config at `~/.gemini/antigravity/mcp_config.json` is a 0-byte empty file.

So when she asks "why is Claude slow in Antigravity," the slowness is **Claude Code's**, not Antigravity's relay (the popular `cloudcode-pa.googleapis.com` theory only applies to people using Antigravity's native chat with Claude as the picked model).

**Bundle state (the v2.0 self-hijack):**
- `/Applications/Antigravity.app` → `com.google.antigravity` v2.0.6 — idle, not running
- `/Applications/Antigravity IDE.app` → `com.google.antigravity-ide` v2.0.4 — the one actually running
- Both have TCC mic grants in `~/Library/Application Support/com.apple.TCC/TCC.db` (auth_value=2)
- Documented self-hijack thread: https://discuss.ai.google.dev/t/.../146158

**Where Claude Code's logs live inside Antigravity:**
`~/Library/Application Support/Antigravity IDE/logs/<timestamp>/window<N>/exthost/Anthropic.claude-code/Claude VSCode.log`

**Where the slowness comes from (per live log inspection 2026-06-27, session 8269da7e + this one):**
1. Opus 4.8 `[1m]` 1M-context calls — 2.2-10.7s TTFT on her actual logs
2. Fast mode disabled (logged 106× in one day: "Fast mode requires usage credits")
3. Three concurrent Claude Code processes sharing OAuth quota — Antigravity extension + 2 in standalone Claude.app
4. Explore sub-agent runs of 79+ seconds freeze parent chat
5. Vercel plugin SessionStart hook prepends ~4.5KB to every conversation start

**"Combobulating" is a Claude Code spinner verb** (Tengu codename, `tengu_spinner_words` Statsig key) — seeing it confirms Claude Code (not Antigravity's UI) is what's spinning. Reference: https://github.com/levindixon/tengu_spinner_words

Related: [[reference-voicemode-multisession]], [[project-e4e-status]]
