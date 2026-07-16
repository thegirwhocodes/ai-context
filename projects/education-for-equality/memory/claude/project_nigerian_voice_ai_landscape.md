---
name: project-nigerian-voice-ai-landscape
description: How Nigerian/African voice-AI operators actually make in-the-wild Nigerian voice machine-readable — and the strategic implication for Sabi (route around the hardest case)
metadata:
  node_type: memory
  type: project
  originSessionId: 400bc972-a5a2-4e9d-a2f5-f3697bf0e69e
---

Deep research (Jul 7 2026, session 400bc972) on how companies on the ground in Nigeria/Africa capture & interpret Nigerian voice. **Nobody solves Sabi's hardest case head-on** (open-vocab + precise-answer-checking + children + noisy 8kHz telephony + Nigerian accent). They all route around it in one of two ways. - 400bc972

**CAMP A — avoid open ASR for the precise bits; use TEXT or KEYPAD (proven, at-scale):**
- **Rori** (Rising Academies) — the closest analog: AI *math* tutor, 100k+ African kids, +11pp RCT in Ghana. Uses **WhatsApp TEXT**, NOT voice. Sidesteps STT entirely.
- **Viamo 3-2-1** (40M+ users, 6 langs) — **DTMF keypad menus** ("listen-and-choose"). Their voice-first GenAI "Ask Viamo Anything" (Zambia, 40k callers/1M questions) is a newer frontier pilot for open Q&A (semantic gist, not exact-answer checking).
- **USSD banking** — 515M txns/yr (2022); 20M+ Nigerians have no smartphone. Menu/text, any phone.
- **uLesson** (biggest NG edtech) — app + video + touch quizzes, no voice input, needs smartphone.
- **Academic consensus**: telephone services rely on push-button DTMF *because* high-accuracy ASR isn't available for developing-region languages — and even high-accuracy ASR shows low task-success on its own.

**CAMP B — do voice, but COLLECT YOUR OWN Nigerian data + fine-tune (moat-building). Nobody wins with off-the-shelf Whisper:**
- **Intron Sahara v2** — 50,000 hrs / 14M clips / 40k speakers / 500 accents, recorded in REAL noisy places (clinics, courts, **busy streets**), patented "AccentMix". Built native.
- **Awarri / N-ATLaS** — **LangEasy** crowdsourcing app (read English→NG langs; 24k→500k hr target), gov-mobilized via 3MTT fellows (NCAIR/NITDA).
- **Spitch** — sells API/SDK (`pip install spitch`), internal data-collection+labelling pipeline + partner corpora.
- **EqualyzAI** — ground-up *code-switched* data via VoiceBridge feature-phone IVR.
- **Lelapa AI (Vulavula)** — pan-African API, expert human linguists label accents/local-names/code-switch; on-prem deployable.
- **NaijaVoices** — 1,800 hrs; expert-generated culturally-rich sentences (144 experts, 100 themes) → 5,220 donors × 240 sentences; deliberately included children + traditional counting systems.
- **Airtel** — runs ASR on 84% of contact-center calls via NVIDIA **NeMo Conformer** + Triton (post-hoc analytics, adult).
- **Google Gboard/Chirp** — added Yoruba/Hausa/Igbo/Pidgin voice typing (cooperative adult, smartphone mic — not noisy telephony kids).

**ENGINEERING PATTERN for "expect a number" (Twilio-standard, directly usable):** `<Gather input="dtmf speech" hints="one,two,...,thirty,...fifty" numDigits=N speechTimeout=auto>` + Confidence score + **DTMF fallback** + confirm on low confidence. Hints (≤500 words) sharply boost accuracy when the expected vocab is known. Purpose-built connected-digit models hit 95-99% clean / ~69% noisy — still >> general ASR for the number sub-task.

**IMPLICATION FOR SABI:** the "thirty→tati" failure (see [[project_stt_noise_accent_research]]) is because we're attempting open-vocab precise-answer ASR — the one thing everyone avoids. Fix = **hybrid input**: for numbers/answers use **keypad (DTMF) + speech-with-hints + confirmation** (product change, not ML); keep Whisper+VAD for names/free talk with confirmation loops (3-attempts rule); and **build the data moat** by labeling real Sabi call audio (Naomi's ground-truth labels are the seed) to fine-tune on later — NaijaVoices/Intron playbook, on real noisy child telephony, not WAXAL/adult data. Voice stays Sabi's differentiator (reaches non-smartphone/low-literacy kids), but the *precise* bits shouldn't ride on open ASR. Possible partners/APIs: Spitch, Lelapa Vulavula, Intron (Intron was worse on noise in our bake-off — verify in-domain before depending). - 400bc972
