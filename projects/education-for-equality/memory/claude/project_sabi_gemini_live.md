---
name: project-sabi-gemini-live
description: "Aug 2026 — Sabi's phone tutor was rebuilt onto a continuous Gemini Live audio session (Naomi's caller ID only), replacing the Claude Haiku + separate-STT turn loop on that lane."
metadata:
  node_type: memory
  type: project
  originSessionId: 1f5e4922-dac1-47db-927f-e6ffa3f36d07
  modified: 2026-08-11T01:10:41.214Z
---

# Sabi on Gemini Live (Aug 7–8 2026, codex session `019fdd47`)

**Routing.** Twilio **+1 (715) 312-2345** → SIP trunk → Asterisk `from-twilio` → `sabi-inbound` → AudioSocket **9020**. The old ElevenLabs managed-agent URL still shows in Twilio but is bypassed because the number is bound to the Elastic SIP trunk. Ports 9019/9021 are the older lanes (barge-in off).

**Gemini Live canary.** Naomi's number `+1 860-436-7048` alone runs one persistent `gemini-3.1-flash-live-preview` session (voice `Kore`) that owns listening, reasoning, speech, VAD and native barge-in — no separate STT step, no Claude Haiku, no ElevenLabs TTS on that lane. Everyone else stays on the established pipeline. Scoped via `SABI_GEMINI_LIVE_PHONES` / `phone_uses_gemini_live()`. Her number is also forced numeracy-only. Code: `sabi-server/gemini_live.py`, doc `sabi-server/docs/GEMINI_LIVE_PHONE_CANARY.md`.

**Self-hosted turn-taking** (built before the Live switch, still used on the non-Live lanes): Silero speech gate + echo comparator vs Sabi's outgoing audio + Pipecat Smart Turn v3 endpointing in `sabi-server/turn_taking.py`. It replaced a 2-frame/RMS-420 energy trigger that turned coughs and echo into turns. Docs: `SELF_HOSTED_TURN_TAKING.md`, `ELEVENLABS_CLEANROOM_PARITY.md`, `OPENAI_REALTIME_BARGE_IN_BLUEPRINT.md`.

**Grading is deterministic, not Gemini's opinion:** numeric-first (“thirty fries” = 30), a registered-question tool so Gemini cannot ask a problem the backend isn't grading, an enforced 5–7 minute lesson clock, an “I don't know → teach one step” gate, and a beginner deck that starts 2×2 → 2×3 with larger facts locked. Tutor prompt shrank 32,555 → ~3.7k chars. Mastery rule from the research doc: 4 of the last 5 **independent** probes across ≥2 calls; unclear audio is “not scorable”, never wrong. See `docs/FLN_GRADING_RESEARCH_AND_SABI_STANDARD_2026-08-07.md`.

**Known limitation that drives [[project-sabi-numeric-sidecar]]:** Gemini Live's visible `inputAudioTranscription` (enabled with no prompt at all) often mis-renders Nigerian 8 kHz phone speech — “thirty” → “Tati”, foreign-language text — while the model's *semantic* hearing is frequently still right. On the archived Oluremi/Gideon clips: 3/5 of Oluremi's verified turns recovered, 0/2 of Gideon's name turns. Isolated clip probe: 2/7 correct, 4/7 wrong, 1/7 no turn detected. Replay tooling: `scripts/replay_gemini_live_hearing.py`, `scripts/probe_gemini_live_clips.py`, `scripts/replay_gemini_live_archive.py`.

**Operational rule learned the hard way:** recreating the `sabi-server` container kills any live AudioSocket call (it cut a 371 s call on Aug 7). Always check `docker exec sabi-asterisk asterisk -rx "core show channels concise"` before `docker compose up -d sabi`.

Related: [[project-e4e-tech]], [[project-stt-noise-accent-research]]
