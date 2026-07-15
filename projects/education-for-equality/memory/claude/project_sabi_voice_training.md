---
name: project-sabi-voice-training
description: "Sabi voice training — full history (Bukola v1-v3, Chatterbox switch) and the completed Jul 2 2026 kit: tag cleanup done + regression, 43-session recording kit ready; Naomi's recordings are the only remaining human step"
metadata:
  node_type: memory
  type: project
  originSessionId: 939e4955-243e-4ea8-b457-17ad531acd52
---

# Sabi Voice Training (completed machine-side 2026-07-02, session 939e4955)

## History (do NOT re-run these)
- Bukola Afro-TTS/XTTS fine-tunes (session 296c88b8, Mar 11-13): v1 15-epoch (loss 3.17→2.63, "too similar"), v2 50-epoch (→2.49, "slightly better"), v3 50-epoch lr 2e-5 (train →1.59, "much much much better") — ceiling hit because training data was synthetic ElevenLabs audio ("clone of a clone"). Pipeline is PROVEN and kept: `sabi-server/afro-tts/finetune/{prepare_data.py,train.py,export_model.py}`; winning recipe = 50 epochs, lr 2e-5.
- Mar 13: switched to Chatterbox Turbo (MIT, ~4.5GB VRAM, beats ElevenLabs 63.75% in blind tests per Resemble); Naomi's voice zero-shot cloned from 29s; live default voice `naomi` (verified Jun 10). Caveat: Turbo logs say `exaggeration` is ignored.
- The unfinished half of that plan: recording REAL voice (5-10h → "ultra high quality, unmistakably you") — Claude offered to generate a recording script; `2. The Solution/SABI_VOICE_RECORDING_SCRIPT.md` (3,725 blocks, ~96k words) was created but never operationalized. Naomi now owns a Focusrite interface (session 49bdfa0d, Jun 29).

## Completed 2026-07-02 ("complete the voice training plans with excellence")
1. **Tag cleanup plan executed to done-criteria** (`2. The Solution/SABI_VOICE_PERFORMANCE_TAG_CLEANUP_PLAN.md` now marked COMPLETE): all 1,068 `[laugh]`(529)/`[chuckle]`(451)/`[sigh]`(88) tags stripped from the 9 lesson-script modules; delivery intent preserved as a "Voice Performance (Delivery Metadata)" section in each module (celebration / playful_warmth / gentle_reassurance — old [sigh] = gentle reset on corrections, never exasperation). Backups in session scratchpad.
2. **Regression**: `scripts/check_voice_affect_tags.py` — scans lesson-scripts, master recording script, curriculum-app ts/tsx, sabi-server py; whitelists prompt lines that forbid tags + the chatterbox-tts engine (which legitimately consumes tags); asserts `clean_text_for_tts` stripper intact. PASS; negative-tested.
3. **Recording session kit** (the missing half of the Mar 13 plan):
   - `2. The Solution/voice-training/RECORDING_SESSION_PLAN.md` — operator plan: Focusrite setup (48kHz/24-bit mono WAV, peak −12dB), session hygiene, quality ladder (session 00 = same-day Chatterbox reference upgrade; ~2h = XTTS fine-tune; 9.6h total = ultra tier), post-recording commands, promotion rule (A/B on isolated lane per QA playbook, never straight to prod phone route).
   - `scripts/split_recording_script.py` → generated `voice-training/recording-sessions/` (43 teleprompter sessions + session_00_reference_set + INDEX.md; 3,827 deduped blocks; branch markers stripped; per-session delivery cues; name-rotation instruction).
   - `scripts/prepare_voice_recordings.py` — validates WAVs (ffprobe, clipping via volumedetect), normalizes to 48kHz mono −19 LUFS masters, manifest.json + tier, prints exact Chatterbox-upgrade and Hetzner fine-tune commands. End-to-end tested with synthetic WAVs.

## ElevenLabs cost elimination (the actual goal — deployed 2026-07-02, session 939e4955)
- Docs mandate (pilot/budget/Sabi Costs.md:208): phone TTS = Chatterbox self-hosted $0; ElevenLabs Impact = web demo only. Live reality was inverted: `SABI_TTS_PRIMARY=elevenlabs` AND the sabi-chatterbox container had been REMOVED (~Jun 10, Qwen3 experiments left `qwen3-tts-finetuner` running instead) — web demo /afro-tts was dead 3 weeks, everything silently paying ElevenLabs.
- Fixed: container restored (`docker run` on sabi-server_default network, alias `chatterbox`, --restart unless-stopped, voices naomi/bukola/lagos295/wura, 4.4GB VRAM); `synthesize_chatterbox` added to phone chain; `SABI_TTS_PRIMARY=chatterbox` supported (chain chatterbox→elevenlabs→yarngpt); **test lane 9020 = Chatterbox-first via `SABI_TTS_TEST_PRIMARY=chatterbox`, prod 9019 untouched** (playbook Tier 3); per-turn `assistant.tts_provider` + `tts_providers_used` rollup in sidecars. Regression `tts_provider_config_regression.py` 13/13 in live container; full adjacent suite green; commits `2d1b9a0` + docs commit pushed.
- Latency: warm short-turn 1.24s (ElevenLabs flash ~0.4–0.9s) — canary judges. Sample: `voice-tests/chatterbox_phone_lane_sample.mp3`.
- Promote after 5 adult canary calls on `direct-call-intron` (which now tests Chatterbox TTS + Intron STT together): flip `SABI_TTS_PRIMARY=chatterbox`, rollback = flip back (one container cycle). Full ops doc: `sabi-server/docs/chatterbox-tts-lane.md`.

## Remaining (human, Naomi)
- Record session 00 (~10 min) → same-day live voice upgrade; then work down INDEX.md.
- Decide canonical voice: her own vs. Nigerian speaker (kit is speaker-agnostic) — and whether to test ElevenLabs Professional Clone (~30 min audio) against self-hosted.

Related: [[project_e4e_tech]] [[project_sabi_status_jul2026]]
