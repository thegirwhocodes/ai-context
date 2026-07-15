---
session_id: "019ecc6f-2cab-7810-bdb3-68bc5dab5d3e"
source: "codex-subagent"
project: "education-for-equality"
parent_session_id: ""
agent_path: ""
nickname: ""
ended: "2026-07-04T22:51:51.888Z"
---

# Codex subagent report: 019ecc6f-2cab-7810-bdb3-68bc5dab5d3e

I did the research and saved the durable note here: [SABI_STT_PROVIDER_RESEARCH_2026-07-04.md](/Users/naomiivie/Education%20for%20Equality/11.%20Documentation/SABI_STT_PROVIDER_RESEARCH_2026-07-04.md).

Bottom line: **Intron Sahara v2 still looks like the best Africa-specific provider to beat.** I did not find another provider with stronger public evidence on African names, African-accented English, numbers/currency, noisy calls, and silence robustness. Intron’s own benchmark shows Sahara v2 beating GPT-4o, Whisper, Deepgram, Azure, ElevenLabs, etc. on African datasets, and AfriSpeech-MultiBench also reports Sahara leading on finance/numerals, African names, call center, and noise robustness.

Best challengers to test:

1. **Soniox v5 Real-Time / Async**  
   Best non-Intron live-call challenger. Strong claims around telephony, accents, multilingual speech, names, numbers, endpointing, and very low pricing. Needs Sabi gold-clip testing.

2. **OpenAI `gpt-4o-transcribe`**  
   Best general high-accuracy offline comparator. Good for replay/evals, but not obviously best for realtime Nigerian child phone audio.

3. **ElevenLabs Scribe v2 / Realtime**  
   Very strong global STT, 90+ languages, keyterm prompting, cheap. But Intron’s African benchmark shows it weaker on African numbers and names.

4. **Deepgram Nova-3 / Flux**  
   Mature voice-agent infra, low latency, keyterm prompting. Good baseline, but African-specific numbers look weak in Intron’s table.

5. **Google Chirp 3 with phrase adaptation**  
   Serious enterprise baseline. Phrase sets/custom classes can help Sabi’s bounded vocabulary, but no Africa-specific edge.

6. **Microsoft MAI-Transcribe-1.5**  
   New high-ranking general model. Worth offline testing, but no Nigerian/African proof yet.

7. **Mistral Voxtral**  
   Best open-weight/self-host watchlist path. Interesting for privacy and cost, but not first for Nigerian child speech.

Recommendation: run Sabi’s bake-off in this order: **Groq baseline → Intron → Soniox → OpenAI → ElevenLabs → Deepgram → Google → Microsoft**. Promote nothing until it beats baseline on Sabi’s own clips: numbers, Naira, short literacy words, Nigerian names, silence/noise, and live call latency.

Key sources: [Intron](https://www.intron.io/), [AfriSpeech-MultiBench](https://arxiv.org/html/2511.14255v1), [AfriSpeech-200](https://aclanthology.org/2023.tacl-1.93/), [OpenAI STT docs](https://developers.openai.com/api/docs/guides/speech-to-text), [Soniox v5](https://soniox.com/blog/soniox-v5-real-time), [Deepgram keyterms](https://developers.deepgram.com/docs/keyterm), [Google Chirp 3](https://docs.cloud.google.com/speech-to-text/docs/models/chirp-3), [ElevenLabs Scribe](https://elevenlabs.io/docs/overview/capabilities/speech-to-text), [Artificial Analysis STT leaderboard](https://artificialanalysis.ai/speech-to-text/non-streaming).
