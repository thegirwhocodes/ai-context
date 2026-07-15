---
name: reference-voicemode-multisession
description: How multiple concurrent VoiceMode voice sessions are set up to share one mic via turn-taking
metadata: 
  node_type: memory
  type: reference
  originSessionId: 31093a5b-56b7-45cc-8b84-61853918b374
---

VoiceMode multi-session setup (local turn-taking — chosen over VoiceMode Connect). Local VoiceMode always records from the system **default mic** (`sd.default.device[0]`, no per-session device override exists), so concurrent voice sessions must **take turns**, coordinated by the "conch" lock at `~/.voicemode/conch` (flock-based; `voice_mode/conch.py`).

Key behavior: `converse(wait_for_conch=...)` defaults to **false** = decline immediately if another session holds the mic. Set **`wait_for_conch=true`** to queue politely — this instruction was added to `~/.claude/CLAUDE.md` so all sessions do it.

What was configured:
- Global `~/.voicemode/voicemode.env`: `VOICEMODE_CONCH_ENABLED=true`, `VOICEMODE_CONCH_TIMEOUT=45`, `VOICEMODE_CONCH_LOCK_EXPIRY=180`.
- Per-project `.voicemode.env` (voice picked up by walking up from cwd, `config.py:find_voicemode_env_files`), distinct voice each: E4E=af_sky, portfolio=af_bella, devsync=af_nova, adjutant=am_adam, cortex-web=af_sarah, cortex/cortex-web=am_michael. `.voicemode.env` gitignored in the git repos.
- Helper `~/.voicemode/bin/mic` (`mic` = who holds the mic, `mic free` = clear stuck lock).
- Doc: `~/.voicemode/MULTI-SESSION.md`. Crashed session frees mic instantly (PID check); alive-but-stuck cleared after 180s.

Upgrade path for TRUE parallel (separate audio channels, e.g. phone + browser): VoiceMode Connect (voicemode.dev) — needs her OAuth login + internet, higher latency, multi-agent routing still maturing. LiveKit room-based = "coming soon" in v8.6.1, not usable.

Separately, the mystery "action-movie / something bad is happening" sound she heard was VoiceMode's 14-second `PreCompact/default.mp3` soundfont (plays when Claude Code compacts context). All soundfonts except "Permission needed" were silenced by overwriting them with 0.1s silence; originals backed up at `~/.voicemode/soundfonts/voicemode.bak`.
