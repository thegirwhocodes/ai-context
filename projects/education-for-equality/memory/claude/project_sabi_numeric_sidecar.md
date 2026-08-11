---
name: project-sabi-numeric-sidecar
description: "Aug 10 2026 — shadow Groq+Whisper numeric STT sidecar shipped on Sabi's Gemini Live lane; measurement only, grading on consensus stays closed until a bake-off precision gate passes."
metadata:
  node_type: memory
  type: project
  originSessionId: 1f5e4922-dac1-47db-927f-e6ffa3f36d07
  modified: 2026-08-11T01:22:13.951Z
---

# Numeric STT sidecar — Phase 1 live (10 Aug 2026)

On every finished **numeric** turn of a Gemini Live call, Groq `whisper-large-v3` and local faster-whisper re-transcribe the same canonical 16 kHz clip and their votes are recorded. **Shadow only** — it cannot change Sabi's reply, grade or timing. `SABI_NUMERIC_SIDECAR_MODE` accepts only `shadow`; any other value logs a warning and stays shadow.

**Rules it enforces:** votes never see the question, operands or expected answer (that bias is what the turn-based path did wrong); both engines get byte-identical audio (SHA-256 recorded); only agreement on a *single* numeric value counts; object nouns are ignored ("two mangoes" = "two fries" = 2); teen/tens conflicts (13/30), multi-value speech and silence abstain; one engine alone never decides; late/dropped/crashed votes are recorded but never applied.

**Files:** `sabi-server/numeric_sidecar.py`, vote engines + `_canonical_numeric_clip` in `stt.py`, attachment at `gemini_live.py: GeminiLiveCallRunner._submit_numeric_sidecar`, 39 offline checks in `numeric_sidecar_regression.py`, read-out `scripts/numeric_sidecar_report.py`. Commit `96710a6`.

**Reading results:** records land at `/shared/audio/numeric_sidecar/<call_uuid>.jsonl` on the Hetzner box (136.243.8.51). Run `docker exec sabi-server python scripts/numeric_sidecar_report.py` (add `--turns` for per-turn rows). It reports agreement rate, would-have-graded precision, "sidecar rescues" (Gemini's transcript missed the number, the two engines agreed on it), latency percentiles and any WRONG agreements.

**Measured blocker for Phase 3:** local Whisper runs on **CPU** in the current compose (Groq ≈0.31 s, local ≈11–14 s on real archived clips). Nothing can pass a 1.5 s live decision deadline until local STT gets GPU or a smaller/faster model, so live consensus grading is blocked on infrastructure as well as on the labelled Nigerian PSTN bake-off (≥98% precision on accepted values).

Design + status table: `sabi-server/docs/PARALLEL_STT_FOR_GEMINI_LIVE_RESEARCH_2026-08-07.md`. Related: [[project-sabi-gemini-live]], [[project-stt-noise-accent-research]]
