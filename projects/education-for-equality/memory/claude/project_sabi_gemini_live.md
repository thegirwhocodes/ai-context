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

**Gemini Live canary.** Naomi's number `+1 860-436-7048` alone runs one persistent `gemini-3.1-flash-live-preview` session (voice **`Kore`** — the Aug 13 switch to `Leda` (6dbfcf8) was REVERTED by `801991b`, confirmed in code + git log Aug 20 2026 - 7e3c69b7) that owns listening, reasoning, speech, VAD and native barge-in — no separate STT step, no Claude Haiku, no ElevenLabs TTS on that lane. Everyone else stays on the established pipeline. Scoped via `SABI_GEMINI_LIVE_PHONES` / `phone_uses_gemini_live()`. Her number is also forced numeracy-only. Code: `sabi-server/gemini_live.py`, doc `sabi-server/docs/GEMINI_LIVE_PHONE_CANARY.md`.

**Self-hosted turn-taking** (built before the Live switch, still used on the non-Live lanes): Silero speech gate + echo comparator vs Sabi's outgoing audio + Pipecat Smart Turn v3 endpointing in `sabi-server/turn_taking.py`. It replaced a 2-frame/RMS-420 energy trigger that turned coughs and echo into turns. Docs: `SELF_HOSTED_TURN_TAKING.md`, `ELEVENLABS_CLEANROOM_PARITY.md`, `OPENAI_REALTIME_BARGE_IN_BLUEPRINT.md`.

**Grading is deterministic, not Gemini's opinion:** numeric-first (“thirty fries” = 30), a registered-question tool so Gemini cannot ask a problem the backend isn't grading, an enforced 5–7 minute lesson clock, an “I don't know → teach one step” gate, and a beginner deck that starts 2×2 → 2×3 with larger facts locked. Tutor prompt shrank 32,555 → ~3.7k chars. Mastery rule from the research doc: 4 of the last 5 **independent** probes across ≥2 calls; unclear audio is “not scorable”, never wrong. See `docs/FLN_GRADING_RESEARCH_AND_SABI_STANDARD_2026-08-07.md`.

**Known limitation that drives [[project-sabi-numeric-sidecar]]:** Gemini Live's visible `inputAudioTranscription` (enabled with no prompt at all) often mis-renders Nigerian 8 kHz phone speech — “thirty” → “Tati”, foreign-language text — while the model's *semantic* hearing is frequently still right. On the archived Oluremi/Gideon clips: 3/5 of Oluremi's verified turns recovered, 0/2 of Gideon's name turns. Isolated clip probe: 2/7 correct, 4/7 wrong, 1/7 no turn detected. Replay tooling: `scripts/replay_gemini_live_hearing.py`, `scripts/probe_gemini_live_clips.py`, `scripts/replay_gemini_live_archive.py`.

**Operational rule learned the hard way:** recreating the `sabi-server` container kills any live AudioSocket call (it cut a 371 s call on Aug 7). Always check `docker exec sabi-asterisk asterisk -rx "core show channels concise"` before `docker compose up -d sabi`.

**Voice choice (Aug 13 2026):** the options on this lane are a **Gemini prebuilt voice** (one-line change, no latency or cost) or **ElevenLabs** (needs a text→TTS bridge: Live returns TEXT, +200–400ms streaming, plus a playback ledger so barge-in truncates history to what the child actually heard). ⚠️ **Do not propose Chatterbox for this** — Naomi said plainly she is not interested, twice. Voice auditions of all 30 Gemini voices (studio + 8 kHz phone band) live at `~/Desktop/sabi-voice-auditions/`; voice went `Kore` → `Leda` (6dbfcf8, Aug 13) → **reverted to `Kore`** (`801191b` "revert Sabi's Gemini Live voice to Kore"). ⚠️ **Current default is `Kore`**, matching `GEMINI_LIVE_VOICE` in `gemini_live.py`; `SABI_GEMINI_LIVE_VOICE=auto` sends no voice at all and lets the model pick - 7e3c69b7

**⚠️ Safety gap verified in code (Aug 20 2026) - 7e3c69b7.** `gemini_live.py` imports **only** `SABI_SAFETY_PREAMBLE` from `guardrails.py`. The deterministic pattern layer — `guard_input`, `guard_output`, `raise_safeguarding_incident` — is called **only from `llm.py`**, i.e. the turn-based lane. So on the Gemini Live lane a crisis disclosure is handled by prompt-following alone: **no regex crisis detection, no output filtering, no safeguarding incident is ever raised.** This matters before any child calls that lane.

**Prompt now lives in a file, and the inline fallback is stale - 7e3c69b7.** `prompts/sabi_tutor_prompt.md` (74 lines) is the live prompt, loaded by `_load_tutor_prompt()`; the `_FALLBACK_TUTOR_PROMPT` string inside `gemini_live.py` is only used if that file is missing — and it is now **out of date** (it still carries the scripted move list "Yeees!/Ehn ehn/Sharp sharp", which `ca6dedf` removed from the live file in favour of "Be warm and familiar."). Editing the Python fallback does nothing on a healthy box.

**Lesson clock + deck (verified in code) - 7e3c69b7.** `SABI_MAX_CALL_SECONDS=480` hard deadline; min lesson 300s; target wrap 420s. Deck = 19 `MULTIPLICATION_PROBLEMS` in 3 difficulty tiers, answers 3→48; tier is set by saved `multiplication_difficulty_tier`, never inferred from mastery. Audio in 8 kHz, Gemini out 24 kHz downsampled by `Pcm24kTo8k`. Three Gemini tools: `get_next_numeracy_problem`, `grade_numeric_answer`, `get_lesson_progress` (must be called before any wrap-up). Anti-drift guards: `is_early_wrap_text` (blocks goodbye <300s, max 3 repairs) and `registered_followup_enforcement` (re-asks the reserved question if Gemini invents its own).

**Live box state, verified over SSH Aug 20 2026 ~12:20 ET - e254ca93.** `SABI_GEMINI_LIVE_VOICE=auto` is what is actually set in the container env, so the deployed lane runs **no voice name at all** (model picks) — the `Kore` default in code is overridden. Model `gemini-3.1-flash-live-preview`, allowlist `+18604367048` only, `SABI_SIP_PROVIDER=twilio` / caller ID `+17153122345`. The container's `AT_USERNAME=sandbox` is NOT an account problem — see [[project-e4e-africas-talking]]. `prompts/sabi_tutor_prompt.md` was replaced by commit `c96b703` with the **original Claude-era hackathon prompt copied byte-for-byte from `original_sabi_prompt.py`** (7,873 chars live) — deliberately accepted regressions: the compactness guard fails (35/36 regressions pass), the ElevenLabs template `{{system__caller_id}}` reaches Gemini literally with nothing substituting it, and the prompt's own rules contradict the tool contract ("NEVER repeat the same question" vs scaffold-the-same-item; "after 8-10 exchanges start wrapping up" vs the 300s/420s/480s lesson clock).

**It sounds right on a real call.** Call `da1bfb97` (Naomi, live while I was reading): turn 0 — "Yeees! Nine groundnuts is correct! You're too sharp! Oya, try this next one..."; turn 1 (wrong answer) — "Ah ah, good try, Naomi! One hand has five. Let's count five more..." Deterministic grading fired correctly both turns.

**The server checkout is not the deployed source - e254ca93.** `/opt/sabi/sabi-server` HEAD is `3b51788` (March) with ~10 tracked files dirty; deploys happen by copying files in. `git log` on the box tells you nothing about what is running — read the container instead (`docker exec sabi-server python -c "import gemini_live ..."`).

**The deck is what made her sound scripted — tools are OFF on the live lane (Aug 20 2026) - 69b43c76.** Naomi's verdict once the tools were removed: *"sounds much closer to original Sabi."* `SABI_GEMINI_LIVE_TOOLS` is now three-way: `on` = deck-driven (old behaviour), `off` = **live setting**, no `functionDeclarations` sent at all, `ledger` = written but never deployed. In `off` mode Sabi invents her own naira questions and marks them herself, exactly like the Claude Haiku system; the injected constraints swap the tool contract for "make up your own questions as you go… no list to work through… mark the answer to the question you actually asked."

**Why the deck had to go — the 16:15 call `715af326` - 69b43c76.** The tool registered `eqg_a_2x2_eggs` ("Two plates have two eggs each", expected 4). Sabi ignored it and invented *"You buy groundnuts for 20 Naira, and you buy biscuits for 10 Naira. How much are you going to pay altogether?"* Naomi answered **30 — correct** — and `grade_numeric_answer` scored 30 against 4 and returned `incorrect`. Sabi then abandoned the naira question and started teaching the eggs. Root cause: `registered_followup_from_tool_events` only enforces a problem registered by a *correct grade*, so **the opening question of every call was never enforced at all**. The prompt's "ALWAYS use market and naira framing for every single maths question" guarantees she rewrites any non-money item.

**⚠️ Three separate brevity caps, not one - 69b43c76.** Removing "keep it short" from the prompt does not work, because it was written in three places: the prose block and the `IMPORTANT RULES` line (both in `prompts/sabi_tutor_prompt.md`), **and** "Speak warmly in one or two short sentences" inside `build_live_call_constraints` in `gemini_live.py` — injected per call, invisible from the markdown. All three are now removed. Naomi's standing preference: brevity is the wrong target, the longer register is what stops Sabi feeling transactional.

**The numeric sidecar has never once influenced a call - 69b43c76.** It is pure shadow by construction: `submit()` queues to a thread pool and returns a bool, nothing on the reply path awaits it, and `sidecar.drain` runs only *after* `memory.clear_call` at teardown — **so it can never cause mid-call silence.** Measured on `715af326`: deadline 1.5s vs actual 3.24/3.59/3.97s, `decision_eligible: 0`, every turn `stale=True`. It also gates on `expected_answer is None`, so with tools `off` it is **completely inert**. Naomi's idea worth building: use the two re-hearers as a *hearing consensus only* (no answer key needed) and let Sabi self-correct one turn later — 3.5s lands before the next turn even though it misses the same-turn deadline. ⚠️ The Groq key returned **403** on Aug 20, so that lane may be dead.

**⚠️ Restart trap, tripped Aug 20 2026 - e254ca93.** The running container had
`SABI_GEMINI_LIVE_VOICE=auto` as a *runtime override* while `/opt/sabi/sabi-server/.env` on disk
still said `Leda`. Recreating the container reverted the live voice to Leda. **Any** restart would
have done this, by anyone. Fixed by writing `auto` into `.env` so it is durable. Lesson: before
running `safe_deploy.sh`, diff what the container reports against what `.env` says — the running
process is not necessarily reproducible from disk.

**Carrier switched back to Africa's Talking Aug 20 2026 - e254ca93.** `SABI_SIP_PROVIDER=africastalking`,
`SABI_CALLER_ID=+2342017001459`. Driven by cost, not audio: Twilio Nigeria termination is $0.2263/min
and the account is a Trial that can only dial one verified number. `main.py` maps provider → PJSIP
endpoint automatically via `SIP_PROVIDER_ENDPOINTS`. Backup at `.env.bak-20260820-181248`.
Roll back = set provider `twilio` + caller ID `+17153122345`, then `./scripts/safe_deploy.sh`.
⚠️ **The reason she left AT — Sabi could not hear her — is unfixed.** Cost and audio are separate
problems; this switch only addressed cost. Switching back also re-enables the `from-at` inbound
context, which is the only one with flash-callback (₦0 for the caller).

Related: [[project-e4e-tech]], [[project-stt-noise-accent-research]], [[project-sabi-brand]], [[project-sabi-numeric-sidecar]]

**Live config verified over SSH Aug 20 2026 ~15:45 ET - 2f1d5115.** Container up 54 min (the 18:44 UTC
deploy), 0 active calls, `api.eduforequality.org/health` = ok. Env on the box now reads
`SABI_GEMINI_LIVE_VOICE=Leda` (**not** `auto` — it changed after the earlier note in this file),
`SABI_GEMINI_LIVE_TOOLS=off`, `SABI_SIP_PROVIDER=africastalking`, `SABI_CALLER_ID=+2342017001459`,
allowlist `+18604367048` only, `SABI_TTS_PRIMARY=elevenlabs` (that account lapsed to free/402, so the
non-Gemini lane silently falls through to YarnGPT). `.env` also carries a Gemini STT lane
(`SABI_GEMINI_STT_MODEL=gemini-3.5-flash-lite`, tagged prompt mode) and
`SABI_FLASH_CALLBACK_PHONE_ALIASES=+2347065177271=+18604367048`.

**The prompt that is live (8,425 chars, `prompts/sabi_tutor_prompt.md`)** = the original hackathon
prompt with Naomi's edits on top: "AI **teacher**" not tutor, the 1–3-sentence cap deleted in all
three places, "talk a bit slowly… let each sentence breathe", naira questions ask the **price** and
work in tens, and the accent line is **variant 1** — *"You speak Nigerian English — not Pidgin, but
warm, natural, Nigerian-accented standard English."* (the thick/street version was swapped out at
18:44 UTC and sits uncommitted in the working tree).

**Two days of voice hunting ended in one finding - 69b43c76:** Gemini has **no Nigerian voices** —
30 prebuilts, no accent or locale variants, no `en-NG` in Gemini TTS or Cloud TTS (only `en-ZA`), and
no API lists them (the names come from Google's speech-generation docs; **gender is published
nowhere**, which is how Achird — a man — got auditioned as Sabi). Native audio **adapts to the voice
it hears**: fed Naomi's real voice memo, both Kore and Leda answered in Pidgin ("How you dey",
"Ah, nne!") — text probes never did that. Leda returned **more** audio than Kore (415,682 vs 352,802
bytes) on the identical clip, so the "Leda is silent on my handset" fault is downstream of Gemini and
still unexplained. Sending **no voice at all** (`auto`) is the config Naomi called "so so much better",
and with no voice pinned Gemini need not pick the same one twice — the voice-lottery test (2–3 calls
on one config) was never run.

**And the channel is the real ceiling.** Comparing a studio clip against the phone leg: same accent —
the unaspirated `/t/` survives both — but 8 kHz strips F3–F5, fricative brightness and plosive bursts,
which is exactly what carries "Nigerian" to the ear. Naomi's verdict stands and is the one to work
from: *she sounds like a refined Nigerian lady, sometimes American.* Asking Gemini itself (with the
June 15 ElevenLabs call audio, the site copy, the original prompt and the architecture) it answered
**voice `Achernar`, no config changes, the original prompt verbatim** — that choice was never made;
the session ended waiting on "Achernar + verbatim (undoes your edits)" vs "Achernar + the prompt as
it stands".

**Rolled back to Kore, 20 Aug 2026 ~17:16 ET - 2f1d5115.** Naomi: *"this sounds like a lot - please
roll back to the kore from earlier today - and we can pick this up another time."* Changed
`SABI_GEMINI_LIVE_VOICE=Leda` → `Kore` in `/opt/sabi/sabi-server/.env` (durable, not a runtime
override), backup at `.env.bak-kore-rollback-20260820-211643`, deployed with
`./scripts/safe_deploy.sh --wait 180` — line was clear, no call cut. Verified after: voice `Kore`,
model `gemini-3.1-flash-live-preview`, all four listeners up (8000/9019/9020/9021 + FastAGI 4573),
health ok.

**Voice only — nothing else was reverted.** Still live: `SABI_GEMINI_LIVE_TOOLS=off`, carrier
`africastalking` / caller ID `+2342017001459`, allowlist her number only, and the prompt is still the
hackathon base with the **variant-1** accent line ("You speak Nigerian English — not Pidgin, but warm,
natural, Nigerian-accented standard English") plus her edits (AI *teacher*, no brevity cap, "take your
time", naira in tens).

⚠️ **`6cbe0ea "promote Gemini Live to the production lane"` is committed and pushed but NOT deployed.**
The running container and `/opt/sabi/sabi-server` both lack it (`grep -c SAFEGUARDING_CUE` = 0), and
`phone_uses_gemini_live` on the box is still the opt-IN allowlist version. `safe_deploy.sh` only runs
`docker compose up -d --no-deps sabi` against the existing image, so a plain redeploy will NOT ship it —
but **any `docker compose build` or file copy will**, and that flips Gemini Live on for every caller.
Know that before the next deploy.

**The Google-stack path is parked, not dead** — see [[project-sabi-google-voice-clone]].
