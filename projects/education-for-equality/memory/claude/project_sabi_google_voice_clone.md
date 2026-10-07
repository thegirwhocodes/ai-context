---
name: project-sabi-google-voice-clone
description: "Parked 20 Aug 2026 — the only way to give Sabi a real Nigerian voice on Google's stack is Chirp 3 Instant Custom Voice (allow-list only), and taking it means leaving Gemini Live for a split pipeline."
metadata:
  node_type: memory
  type: project
  originSessionId: 2f1d5115-e07a-4c23-a102-15cd8cec38ad
  modified: 2026-08-20T21:24:22.252Z
---

# Sabi's voice on Google's stack — researched, then parked

Naomi's call, 20 Aug 2026: *"this sounds like a lot - please roll back to the kore from earlier today
- and we can pick this up another time."* Nothing was built. The findings below are verified and
keep.

**Google has NO Nigerian English voice, anywhere, at any tier.** Verified against Google's own
published voice list: 489 voices, and the only English locales in the entire Cloud TTS catalogue are
`en-AU`, `en-GB`, `en-IN`, `en-US`. No `en-NG`. No `en-ZA`. The only African locale of any kind is
`af-ZA` (Afrikaans). Chirp 3: HD covers 52 locales, none Nigerian. **Cloud Speech-to-Text has no
`en-NG` either** — v1 and v2 both list `yo-NG`, `ig-NG` and `ha-NG` (the Nigerian *languages*) but not
Nigerian English, so recognition has to run under `en-US`/`en-GB`/`en-IN` with the `telephony_short`
model, which does support the phrase-set biasing.

**The one real path is Chirp 3: Instant Custom Voice** — voice cloning. Allow-list only; you request
it through Google Cloud sales at `cloud.google.com/contact`. Check
`console.cloud.google.com/vertex-ai/studio/media/generate;tab=audio` first in case the project is
already allow-listed. Creation needs a verbatim consent recording ("I am the owner of this voice, and
I consent to Google using this voice to create a synthetic voice model.") plus **up to 10 seconds** of
clean reference audio, single channel, no background noise, **same room and same session**, in Cloud
Storage; you get back a `voiceCloningKey`. It supports **streaming synthesis with MULAW/ALAW output**
(telephony-native), pace control 0.25x–2x, pause tags, and IPA/X-SAMPA pronunciation control — which
is the real fix for "she talks too fast", not another prompt edit.

⚠️ **The consent statement means the old Sabi voice can never be cloned** — it has to be a person who
owns the voice and consents. So this is a casting decision: Naomi, Sonia, or a paid Nigerian voice
actor. Undecided.

**The cost of that path is Gemini Live.** A cloned voice needs text to speak, and a Live session
refuses to emit text — re-verified today, both `gemini-3.1-flash-live-preview` and
`gemini-2.5-flash-native-audio` close the socket with 1007 "response modalities (TEXT) is not
supported", and AUDIO+TEXT together is refused too. So taking the voice means going back to a split
pipeline (recognise → text model → cloned voice), which is the shape [[project-sabi-gemini-live]]
replaced — and which also restores deterministic grading and a real output safety filter.

**Gemini cannot be trusted on its own API.** Asked cold with the audio and full context, it invented
a Cloud TTS voice — `en-NG-Neural2-A` — called it "an excellent Nigerian voice", and built its whole
recommendation on it. Asked again with the real voice list, it also claimed Cloud STT supports
`en-NG` (it does not) and told us to use `gemini-1.5-flash-002` (retired, unreachable on our key). It
never mentioned Instant Custom Voice until it was handed to it. A separate grounded-with-search run
earlier the same day insisted a Live session *can* emit TEXT. **Verify every claim against the live
API before acting on it** — see [[feedback-dont-assert-inferences]].

Full write-ups, both in git: `sabi-server/docs/SABI_ON_GOOGLE_STACK_BLUEPRINT.html` (the blueprint
with a verification ledger, artifact `307681e0`), `SABI_GOOGLE_STACK_BRIEF_SENT_TO_GEMINI.txt` (what
it was sent), and `SABI_VOICE_CLONE_ACCESS_AND_RECORDING.md` (the access request and the
ten-second recording sheet, ready to act on).

Related: [[project-sabi-gemini-live]], [[project-sabi-brand]], [[project-stt-noise-accent-research]]
