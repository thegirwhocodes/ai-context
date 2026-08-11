---
name: project-sabi-numeric-sidecar
description: "Aug 10 2026 — shadow Groq+Whisper numeric STT sidecar shipped on Sabi's Gemini Live lane; measurement only, grading on consensus stays closed until a bake-off precision gate passes."
metadata:
  node_type: memory
  type: project
  originSessionId: 1f5e4922-dac1-47db-927f-e6ffa3f36d07
  modified: 2026-08-11T21:14:32.698Z
---

# Numeric STT sidecar — Phase 1 live (10 Aug 2026)

On every finished **numeric** turn of a Gemini Live call, Groq `whisper-large-v3` and local faster-whisper re-transcribe the same canonical 16 kHz clip and their votes are recorded. **Shadow only** — it cannot change Sabi's reply, grade or timing. `SABI_NUMERIC_SIDECAR_MODE` accepts only `shadow`; any other value logs a warning and stays shadow.

**Rules it enforces:** votes never see the question, operands or expected answer (that bias is what the turn-based path did wrong); both engines get byte-identical audio (SHA-256 recorded); only agreement on a *single* numeric value counts; object nouns are ignored ("two mangoes" = "two fries" = 2); teen/tens conflicts (13/30), multi-value speech and silence abstain; one engine alone never decides; late/dropped/crashed votes are recorded but never applied.

**Files:** `sabi-server/numeric_sidecar.py`, vote engines + `_canonical_numeric_clip` in `stt.py`, attachment at `gemini_live.py: GeminiLiveCallRunner._submit_numeric_sidecar`, 39 offline checks in `numeric_sidecar_regression.py`, read-out `scripts/numeric_sidecar_report.py`. Commit `96710a6`.

**Reading results:** records land at `/shared/audio/numeric_sidecar/<call_uuid>.jsonl` on the Hetzner box (136.243.8.51). Run `docker exec sabi-server python scripts/numeric_sidecar_report.py` (add `--turns` for per-turn rows). It reports agreement rate, would-have-graded precision, "sidecar rescues" (Gemini's transcript missed the number, the two engines agreed on it), latency percentiles and any WRONG agreements.

**Second vote is Azure Speech as of 11 Aug 2026** (commit `d26a60f`). Gold-clip bake-off on the 7 labelled Nigerian phone clips in `output/sabi-unheard-clips-july-2026/`:

| engine | hits | median latency |
|---|---|---|
| Groq `whisper-large-v3` | 0/7 | 0.25 s |
| local faster-whisper + number hotwords | 2/7 | 11 s |
| Gemini Live (raw + contextual) | 2/7 | — |
| **Azure Speech** | **4/7** | **0.71 s** |

Azure cracked `thirty-turn-05` — the clip every Whisper renders "Tati" — and is the only engine ever to recover a child's name ("Her name is Gideon"). Two honest caveats worth repeating in any pitch: **`en-NG` and `en-US` returned byte-identical output on all 7 clips**, so the win is Azure's model, NOT the Nigerian locale; and Azure's confidence is useless as a gate (correct "30" scored 0.07, wrong "Woodward" 0.048) — it's recorded but never used to accept an answer. Azure resource: `sabi-speech-test`, RG `sabi-stt`, **East US**, Free F0, on her **Azure for Students** subscription (⚠️ Wesleyan tenant — same migration trap as the Google billing account; move to a company subscription before production). Key/region live at `secrets/AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION`; `SABI_NUMERIC_SIDECAR_SECOND_ENGINE=auto|azure|local_whisper`.

**Latency is no longer the Phase 3 blocker** (Groq 0.31 s + Azure 0.71 s both clear 1.5 s). Local Whisper stays available as the offline fallback but is CPU-bound at 11–14 s. What remains before consensus can grade: the labelled Nigerian PSTN bake-off and its ≥98% accepted-value precision gate — which real calls now build automatically, since each record pairs the engines' transcripts with the item's known expected answer.

Design + status table: `sabi-server/docs/PARALLEL_STT_FOR_GEMINI_LIVE_RESEARCH_2026-08-07.md`. Related: [[project-sabi-gemini-live]], [[project-stt-noise-accent-research]]
