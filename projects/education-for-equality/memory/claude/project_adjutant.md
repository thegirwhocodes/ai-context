---
name: Adjutant — SCSP Hackathon Project
description: Voice-first offline AI for Army paperwork. SCSP Boston GenAI.mil track, team Charlie Mike, due Sun Apr 26 2026 5 PM. Naomi solo (8GB M1 Air). Pipeline executes end-to-end; ChatGPT-AVM-feel WebSocket voice loop + Kokoro TTS + bulk APD crawler all built but uncommitted.
type: project
originSessionId: 3f0fd587-a8ad-4ce6-86a4-cb6c031d7c7e
buildSessionId: db11b54e-89b2-473e-b485-24b7a9698b7e
---
# Adjutant

**Tagline:** *"Speak it. Sign it. Move out."*

A voice-first, fully offline AI assistant for the Army's "bureaucratic tail." Junior NCO talks to it the way they'd talk to their S1 — *"I need to file leave for ten days starting June 3"* — and gets back a regulation-cited answer plus a populated DA-31 PDF. Same flow for TDY (DD-1351-2 with JTR per-diem math) and counseling (DA-4856).

Located at [/Users/naomiivie/adjutant/](/Users/naomiivie/adjutant/) (separate repo from E4E, `git init`'d, planned public GitHub at `https://github.com/<user>/adjutant`).

## Submission

- **Team Name:** Charlie Mike
- **Product Name:** Adjutant
- **Track:** GenAI.mil
- **Location:** Boston (Phase 1)
- **Hackathon dates:** April 25–26, 2026
- **Deadlines:** Sat 2:00 PM team-registration email (sent), Sun 5:00 PM submission, Sun 5–7 PM judging
- **Members:** Naomi Ivie solo as of compaction time

## Strategic frame — "win like Spectre"

SCSP prior winners researched ([SCSP_DA_FORM_CONCIERGE_PRIOR_ART_SCAN.md](/Users/naomiivie/Education for Equality/SCSP_DA_FORM_CONCIERGE_PRIOR_ART_SCAN.md)) — session bad258fa-eee*. Spectre Red Teaming won $25K Nov 2024 grand prize by *provably breaking* an existing Pentagon system on stage with measurable evidence. Adjutant's analogue: side-by-side eval vs GenAI.mil's hosted Gemini, showing measurable hallucination on out-of-corpus regulation queries while Adjutant correctly refuses. Project Perception (June 2025 SCSP winner) also referenced.

## Boston judging panel

- **Dr. Sanjeev Mohindra** (MIT Lincoln Lab AI Tech Group lead, CDAO-funded test & evaluation researcher) — will probe for hallucination + sycophancy
- **Dr. Ho-Chit Liu** — Mohindra's co-judge, likely also Lincoln Lab
- **Stuart Wagner** (DC judge but his name carries weight) — Air Force/Space Force CDTO, built NIPRGPT, BRAVO Hackathon founder, believes in cheap operational prototypes

Mohindra-targeting moves: 25-question eval harness, side-by-side hallucination demo, deliberate out-of-corpus refusal.

## The pipeline (5 stages, all local, all offline)

1. **STT** — browser mic → faster-whisper `small.en` int8 on CPU. ffmpeg transcodes Chrome WebM/Safari MP4 → 16kHz mono WAV (PyAV choked 1-in-3 on Chrome's Opus). Replaced original large-v3 plan after 8GB swap-thrash.
2. **RAG** — FAISS over curated corpus, sentence-transformers/all-MiniLM-L6-v2, `RAG_SCORE_THRESHOLD=0.35`. Threshold makes out-of-corpus refusal architecturally reliable. Saturating-corpus plan ([foundry/SCRAPING.md](/Users/naomiivie/adjutant/foundry/SCRAPING.md)) adds two-stage retrieval w/ cross-encoder reranker once corpus exceeds ~200K chunks.
3. **LLM** — `llama3.2:3b` via Ollama (replaced llama3.1:8b — 8GB Air swap-thrashed). Constrained-context prompts, `_clean_nulls` post-process strips "null"/"N/A"/"TBD" strings. Now exposes both blocking `answer_query()` AND streaming `answer_query_stream()` (sentence-buffered, ollama-python sync iterator wrapped via thread).
4. **Post-processors** — `_correct_leave_type` (overrides RAG-anchored "emergency" hallucination from "emergency contact"), `_wire_per_diem` (deterministic GSA math beats LLM math).
5. **PDF fill + TTS** — pikepdf AcroForm primary (libqpdf handles encrypted DD-1351-2), reportlab overlay fallback (DA-31 ships as XFA-only — needs reportlab text-on-coordinates engine). **Kokoro-82M ONNX is now primary TTS** (`af_heart` voice, 24kHz, ~300ms warm on M2, fully offline). pyttsx3 + macOS `say` are fallbacks. Chatterbox/CHATTERBOX_URL no longer the path.

## Persona — SGT Maya Chen

E-5, 82nd Airborne, Fort Bragg, 6 yrs in service, infantry squad leader. Documented in [docs/PERSONA.md](/Users/naomiivie/adjutant/docs/PERSONA.md).

**Demo voice query:** *"I'm Sergeant Chen at Fort Bragg. I need to file ten days of ordinary leave starting June 3, going to my sister's wedding in Atlanta. Emergency contact is Maria Chen at 919-555-0144."* → DA-31 cited at AR 600-8-10 ¶ 4-3, signed-ready PDF.

Same flow for JRTC TDY (DD-1351-2, Leesville LA per-diem $110/$68 with 75% travel-day math ≈ $746 for 5 days) and counseling (DA-4856, AR 623-3 reference).

## The wow move — multi-form from one prompt

`_infer_forms` in [server.py](/Users/naomiivie/adjutant/adjutant/server.py) returns a LIST of form IDs. Single voice request like *"I'm going to JRTC at Fort Polk July 14 for 5 days, need to counsel SPC Garcia tomorrow, and want 2 days of leave when I get back"* → DD-1351-2 + DA-4856 + DA-31 all in one shot. Has hard-exclude for pure Q&A ("how does leave accrue?"); requires action verbs (need/want/file/submit/draft/N days of). None of GenAI.mil/CamoGPT/Ask Sage/Milnerva/EdgeRunner do this.

## Demo kill-shot beats

[docs/DEMO_SCRIPT.md](/Users/naomiivie/adjutant/docs/DEMO_SCRIPT.md) — 5-min walkthrough.

- **Beat 1 — Cold open offline.** Pull wifi cable visibly before any code runs. Browser badge flips to OFFLINE.
- **Beat 2 — Voice → DA-31.** SGT Chen's leave query → grounded answer + filled PDF.
- **Beat 3 — Multi-form.** One JRTC sentence → 3 PDFs.
- **Beat 4 — Side-by-side hallucination kill shot.** Same query to GenAI.mil's hosted Gemini live. Gemini reads confident hallucinated paragraph numbers; Adjutant refuses out-of-corpus regs. *"I don't have AR 27-10 in my regulation corpus. Check with your S1 or pull it directly from armypubs.army.mil. I won't guess on regulation language."*
- **Beat 5 — Compliance refusal.** *"35 days of leave"* → cites AR 600-8-10 ¶ 4-3 30-day rule, drafts 30-day form, flags extension for battalion commander. (Not yet wired — Phase 4 polish add.)

## Comparator matrix (judge slide)

| Capability | GenAI.mil | CamoGPT | Ask Sage | Milnerva | SergeantAI | EdgeRunner | **Adjutant** |
|---|---|---|---|---|---|---|---|
| Voice I/O | ❌ | ❌ | ❌ | ❌ | ❌ | listens 1-way | **✅ conversational** |
| Offline | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ tactical | **✅ admin** |
| Cites Reg by section | generic | generic | generic | partial | ✅ (one AR only) | generic | **✅ multi-AR + FM** |
| Auto-fills DA-form PDF | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅** |
| End-to-end persona flow | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅** |
| Hands-free | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅** |

EdgeRunner serves tactical/SOF doctrine. GenAI.mil serves desk-bound officers. Adjutant serves the rank-and-file with paperwork problems — Pentagon's own framing on GenAI.mil (DefenseScoop Dec 2025): *"Not everyone is sitting in a nice, cushy, air-conditioned office."*

## National impact pillar

- **RAND:** Army company leaders work 12.5-hour days — longer than 96% of all American workers. Less than one-third on actual unit readiness.
- **Modern War Institute (West Point):** Companies submit *"three to four dozen monthly reports"* — *"one week every month for company command teams."*
- **Pentagon framing on GenAI.mil:** automating *"thousands of man-hours"* of routine staff processes.
- **TAM:** 3M service members × 6 hrs/wk on paperwork × $25/hr loaded = **$23.4B/yr**.
- GenAI.mil rolled out to 1.2M users in December 2025 (cloud platform). Adjutant is the offline standalone for motor-pool / FOB / barracks where wifi cuts out.

## Build status as of 2026-04-25 21:13 UTC (post-compaction work)

Current commits on `main` (newest first) — same as compaction snapshot:
- `d75060d` — multi-form-from-one-prompt — single voice request → N filled PDFs
- `d2f438d` — form-fill engine + DD-1351-2 AcroForm + per-diem math + STT robustness
- `ef47caf` — switch to llama3.2:3b + whisper small.en; fix env loading + PDF decrypt
- `35a3468` — deps: add python-multipart for FastAPI UploadFile
- `9ea3cb6` — docs(demo): cold-open offline + GenAI.mil side-by-side hallucination kill shot
- `0f5f41a` — fix(download): replace dead DA-4856 URL with api.army.mil mirror
- `9bc9a7e` — Initial scaffolding

**Significant uncommitted work since compaction (post-session continuation):**

Modified:
- [adjutant/llm.py](/Users/naomiivie/adjutant/adjutant/llm.py) — added `answer_query_stream()` async-friendly streaming generator with sentence-buffer regex (negative lookbehinds for decimals/acronyms/e.g./i.e.)
- [adjutant/rag.py](/Users/naomiivie/adjutant/adjutant/rag.py) — RAG_SCORE_THRESHOLD=0.35 baked in
- [adjutant/server.py](/Users/naomiivie/adjutant/adjutant/server.py) — added `@app.on_event("startup")` warmup (TTS+STT+VAD+Ollama+RAG cold-load tax paid once); added `/ws/voice` WebSocket route delegating to VoiceLoop
- [adjutant/tts.py](/Users/naomiivie/adjutant/adjutant/tts.py) — **REWRITTEN.** Kokoro-82M ONNX is primary. `synthesize_wav_bytes_async()` for streaming WS path; cue cache loaded into RAM at startup; pyttsx3 + macOS `say` fallbacks preserved.
- [scripts/ingest_corpus.py](/Users/naomiivie/adjutant/scripts/ingest_corpus.py) — improved section detection (Paragraph/Para/Section + ASCII hyphen + Unicode en-dash; Chapter; Appendix; § CFR style)
- [requirements.txt](/Users/naomiivie/adjutant/requirements.txt) — playwright still commented out; kokoro-onnx + silero-vad + soundfile NOT yet listed (installed manually in .venv per VOICE_PIPELINE_PLAN V0 instructions)
- [web/app.js](/Users/naomiivie/adjutant/web/app.js) — full rewrite (339 lines): AudioWorklet → WS pipeline, gapless `AudioBufferSourceNode.start(when)` chain via `nextStartTime` scheduling, online/offline badge, state machine (idle/listening/speaking_user/thinking/speaking/error), push-to-talk fallback kept under `<details>` for venue safety
- [web/index.html](/Users/naomiivie/adjutant/web/index.html) — Start/Mute buttons, state indicator dot, transcript area, fallback push-to-talk hidden under `<details>`
- [web/styles.css](/Users/naomiivie/adjutant/web/styles.css) — state-color CSS vars, indicator animations

New (untracked):
- [adjutant/voice_loop.py](/Users/naomiivie/adjutant/adjutant/voice_loop.py) — **VoiceLoop class** (~350 LOC). Per-WebSocket state machine. Silero VAD (ONNX, 32ms hops, threshold 0.5), 240ms pre-buffer to catch word-onset, MIN_SPEECH_FRAMES=5 (ignores <160ms blips), SILENCE_FRAMES_TO_END=18 (~600ms), STT_CONFIDENCE_FLOOR=0.5. **Sabi pattern: thinking_0..thinking_4 cues queue IMMEDIATELY at end-of-speech, bridging the LLM-prefill gap with audible "Checking the regs..." instead of dead silence.** Streaming Ollama → sentence-buffer → async Kokoro → asyncio.Queue TTS sender. Barge-in: user speaks while bot speaking → cancel in-flight task, drain TTS queue, send INTERRUPT event. Form-fill side-channel runs AFTER audio reply finishes.
- [foundry/VOICE_PIPELINE_PLAN.md](/Users/naomiivie/adjutant/foundry/VOICE_PIPELINE_PLAN.md) — 7-phase plan (V0–V6, ~7.5h) for ChatGPT-AVM-feel voice. Latency budget targets 1.0–1.4s ESV→FAO on M2. Cut-list: drop AudioWorklet → drop server VAD → keep streaming-only V1+V2 (Architecture C: 60% of perceived improvement for 30% of the work). Architecture A diagram, latency table per-stage, file-by-file change list.
- [foundry/SCRAPING.md](/Users/naomiivie/adjutant/foundry/SCRAPING.md) — saturating-corpus plan. Three sources: APD (~4,000 docs via Playwright Active.aspx index), DTIC (~1.5M unclassified, sitemap-driven crawl), eCFR Title 32 / 5 / 10 / 48 (REST API). Target ~500 docs / ~500K chunks / ~1.5GB. Cross-encoder reranker (`cross-encoder/ms-marco-MiniLM-L-6-v2`, ~300ms latency on 50 candidates) becomes mandatory past ~200K chunks. ~30 LOC two-stage `retrieve()` patch shown inline.
- [scripts/bulk_crawl_apd.py](/Users/naomiivie/adjutant/scripts/bulk_crawl_apd.py) — **BUILT** (~450 LOC). HTTP-first, Playwright fallback for APD anti-bot. TIER_1 hardcoded ~25 docs (AR 350-1, AR 15-6, AR 380-5, AR 40-501, AR 614-100, AR 165-1, AR 690-700, JP 1-0/3-0/5-0, MCM 2024, DA Pam 27-9, ADP 6-22, FM 7-22, FM 7-0, ADP 1, DA Pam 600-3, DA Pam 600-8-22, AR 135-178, AR 600-43, AR 215-1, AR 385-10, AR 615-1) + Active.aspx Playwright sweep. MAX_CORPUS_BYTES=1.5GB cap. TIER_2 (eCFR + DTIC) is a stub. Anti-bot insight baked in: APD checks User-Agent + Sec-Fetch-Dest/Mode/Site + session cookie; >1226-byte threshold filters error pages.
- [web/audio_worklet.js](/Users/naomiivie/adjutant/web/audio_worklet.js) — 53 LOC capture processor. Downsamples 48k→16k by every-3rd-sample, packs 512-sample (32ms) Int16 frames, posts ArrayBuffer to main thread.

New on disk (not in git):
- [models/kokoro/kokoro-v1.0.onnx](/Users/naomiivie/adjutant/models/kokoro/) (325 MB)
- models/kokoro/voices-v1.0.bin (28 MB)
- [audio_cache/cues/](/Users/naomiivie/adjutant/audio_cache/cues/) — 9 pre-generated WAVs: thinking_0..thinking_4, retry_low_conf, ack_da31, ack_dd13512, ack_da4856

**Pipeline has actually executed end-to-end** — [filled_forms/](/Users/naomiivie/adjutant/filled_forms/) has 8 PDFs (5 DA-31 + 3 DD-1351-2), [audio_cache/](/Users/naomiivie/adjutant/audio_cache/) has 10 reply WAVs from prior runs.

**Corpus state:** still 15 PDFs at [corpus/](/Users/naomiivie/adjutant/corpus/) (76 MB) but FAISS index only contains 12. **Same 3 docs need re-ingest:** FM 3-0 (Operations, 31 MB), DA Pam 600-25 (CMF), DA Pam 623-3. FAISS currently: 16,301 chunks, 25 MB faiss.bin, 12 MB chunks.pkl. Ingest improvements not yet re-run over the 3 missing docs.

## Issues fixed in this session (chronological)

- **Python 3.14 too new for ML wheels** → Created venv on python3.13, loosened pins
- **`python-multipart` missing** → Added to requirements.txt (commit 35a3468)
- **8GB RAM swap-thrashing on llama3.1:8b + whisper large-v3** → Switched to llama3.2:3b + whisper small.en (commit ef47caf). Hardware-forced.
- **Env vars read at module-import before load_dotenv()** → Added `load_dotenv()` to top of llm.py, stt.py, rag.py
- **PyAV decode failures on Chrome WebM (1 in 3)** → ffmpeg transcode in stt.py. Compared to Dactyl's native PyAudio approach.
- **DA-31 PDF is XFA-only ("Please wait" page renders)** → Built reportlab overlay engine with hand-tuned coordinate maps in PDF points
- **DD-1351-2 hybrid XFA+AcroForm** → Stripped /XFA so non-Adobe viewers (Preview, Chrome pdf.js) render the AcroForm fill
- **LLM emitting literal "null" strings** → `_clean_nulls()` normalizes
- **LLM dating to 2023 not 2026** → Inject today's date into FORM_EXTRACTION_PROMPT
- **leave_type RAG anchoring on "emergency" from "emergency contact"** → Strip "emergency contact ..." phrase before keyword scan in `_correct_leave_type`
- **Form-fill triggered on Q&A queries** → `_infer_forms` requires action verbs (need/want/file/submit/draft/N days of)
- **PDF encryption block-length error in pypdf** → Switched to pikepdf (libqpdf-backed)
- **Multi-form date conflation** → Known issue, mitigated with scripted demo prompts
- **Hetzner server 136.243.8.51 suspended (non-payment) at session start** → Not a blocker for Adjutant (runs 100% local). Sabi affected.
- **armypubs.army.mil URL pattern returns 1226-byte HTML error for non-browser clients** → Built Playwright fallback in bulk_crawl_apd.py; identified anti-bot triggers (User-Agent + Sec-Fetch headers + session cookie)
- **Sequential STT→LLM→TTS feels like ~6s of dead air** → Sabi-pattern thinking cues queued at end-of-speech bridge the LLM-prefill gap; streaming Ollama → sentence-buffer → async Kokoro lets first audio leave server while LLM still generating sentence #2

## What's NOT yet built (Phase 4 polish + open work)

- **Re-ingest FAISS over the full 15-doc corpus** (3 docs un-indexed)
- **Tier 1 corpus expansion** — bulk_crawl_apd.py exists, hasn't been run yet. ~25 docs hardcoded in TIER_1 list ready to download.
- **TIER_2 eCFR + DTIC fetch implementations** — currently stubs. ~150 LOC each. eCFR endpoint: `https://www.ecfr.gov/api/versioner/v1/full/2026-04-01/title-32.xml`. DTIC sitemap: `https://apps.dtic.mil/sitemap.xml` (sitemap-of-sitemaps, walk + filter by Distribution Statement A + admin/personnel regex).
- **Cross-encoder reranker** (~30 LOC patch to rag.py per SCRAPING.md §5) — not needed for current 16K-chunk demo, becomes mandatory if corpus grows past ~200K chunks.
- **ingest_corpus.py XML/TXT support** — currently only handles `.pdf`; needs `.xml` (eCFR walk `<DIV*>`/`<P>`/`<HD>`) and `.txt` (DTIC plain text) handlers.
- **Pipeline trace UI** — visible 5-stage trace panel showing each AI stage with timing
- **Compliance refusal wiring** — 35-day leave → cite + draft 30 + flag battalion commander
- **GSA per-diem live API** — replace 6-city stub with `open.gsa.gov/api/perdiem-api/`
- **Multi-form single-LLM-call** — fix date conflation
- **SSN/PII redactor** in prompts
- **Eval harness** — 25 questions × Adjutant + 25 × Gemini side-by-side hallucination evidence (the Mohindra-winning move)
- **Test suite expansion** — test_rag.py, test_pdf_fill.py, multi-form integration
- **Browser-iframe verification** (Chrome pdf.js)
- **Wifi-disconnect rehearsal** ×5 — Phase V6 acceptance test in VOICE_PIPELINE_PLAN
- **README rewrite + demo GIF**
- **GitHub repo creation** (currently `<your-username>` placeholder in README)
- **Final commit + tag v0.1-scsp + push** — significant work uncommitted: voice_loop.py, bulk_crawl_apd.py, foundry/SCRAPING.md, foundry/VOICE_PIPELINE_PLAN.md, audio_worklet.js, plus all the modified pipeline files
- **kokoro-onnx + silero-vad + soundfile not in requirements.txt** — installed in .venv but should be pinned for reproducibility before push

## Voice pipeline architecture (now built — Architecture A from VOICE_PIPELINE_PLAN.md)

```
Browser (web/app.js + audio_worklet.js)              Server (FastAPI)
  getUserMedia w/ AEC+NS+AGC                          /ws/voice WebSocket
  → AudioWorklet 48k→16k downsample                   → VoiceLoop instance
  → 32ms PCM16 Int16 frames                           → Silero VAD ONNX (0.5 thr, 32ms hop)
  → ws.send(arrayBuffer)                                ├─ pre-buffer 240ms (catch word-onset)
                                                        ├─ on speech_start, if bot_speaking → INTERRUPT
                                                        └─ on 600ms silence → flush utterance
                                                      → STT cue queued IMMEDIATELY
                                                      → faster-whisper small.en (asyncio.to_thread)
                                                      → retrieve() FAISS top-5 over threshold
                                                      → BOT_SPEAKING_START + citations event
                                                      → answer_query_stream() yield sentences
                                                        ↓ each sentence → asyncio.to_thread Kokoro
                                                      → asyncio.Queue → tts_sender_loop → ws.send_bytes(WAV)
                                                      → after audio done: _maybe_form_fill() → PDF_READY events
  → ws.onmessage:
      binary → audioCtx.decodeAudioData → AudioBufferSourceNode.start(nextStartTime) → gapless playback
      text → JSON event handler → state machine + UI
```

WebSocket events server→client: USER_SPEAKING_START, USER_DONE, USER_SILENT, TRANSCRIPT, BOT_SPEAKING_START (+ citations), BOT_SPEAKING_END (+ spoken_summary), PDF_READY (+ form_id, pdf_url, missing_fields), INTERRUPT, ERROR, PONG.
Client→server: binary PCM16 frames; JSON {type:"MUTE"} or {type:"PING"}.

## Comprehensive corpus question (open strategic decision)

User asked about getting "all the army stuff" — comprehensive APD = ~4,000+ docs / 15-25 GB. SCRAPING.md is the answer: target ~500 current-revision docs (Tier 1.5 list of ~50 ARs/Pams/FMs + JP/MCM + eCFR Title 32 + DTIC filtered). Pitch line: *"Adjutant retrieves over 500 current-revision Army regulations, joint publications, DoD technical reports, and Title 32 of the Code of Federal Regulations — every authoritative source the rank-and-file would ever cite. Half a million chunks, two-stage retrieval with a cross-encoder reranker, all running locally on this laptop. When you ask about leave, we cite AR 600-8-10 paragraph 4-3 *and* the underlying 10 U.S.C. § 701 statute, *and* the RAND analysis explaining why the regulation is worded that way."*

DTIC API = `[REDACTED:sensitive-label]`, REST/JSON, public, internet only at ingest time. Demo runs offline because corpus is pre-indexed locally. Same for eCFR (`api.ecfr.gov`). Internet is a build-time requirement, not runtime.

## Hardware constraint

8GB MacBook Air M1. Model choices forced:
- llama3.2:3b not 8b (~2GB resident)
- whisper small.en not large-v3 (~250MB)
- sentence-transformers MiniLM-L6 (~80MB)
- Kokoro-82M ONNX (~325MB on disk; <300MB resident warm)
- Total resident ~3GB leaves headroom for browser + FastAPI + ffmpeg subprocess + Silero VAD ONNX (<10MB)

Renting a server was rejected — would compromise the offline pitch (*"works on a laptop, no cloud"*).

## Business model post-hackathon

Three paths:
1. **GovCon** — license to SI primary (Booz, Leidos, Accenture Federal) as vertical AI app for IL5 deployments
2. **Direct** — SBIR Phase I → II → III with Army CDAO as customer
3. **Open-source** — sell hosted/managed on top

The DSN voice surface (Sabi pipeline ported onto FedRAMP gov telephony — soldier dials a landline, talks to Adjutant, form lands in their .mil inbox) is the moat for path 2. Reaches every soldier regardless of OPSEC posture. Explicit Sabi → Adjutant pipeline reuse — same voice stack already deployed at E4E scale teaching Nigerian children to read.

## Why: Naomi's strategic frame

- Wesleyan student, E4E founder, parallel hackathon project leveraging shared voice infra
- "Charlie Mike" = "Continue the Mission" — military slang signals fluency without LARPing
- Targeting Mohindra-style judging (eval harness, side-by-side, architectural reliability) over flashier demos
- Persona (SGT Chen) is universal, specific, unclassified, 30-hour buildable, scales horizontally to other personas (UPL urinalysis, XO property, 1LT OERs)
- User explicit guidance during build: *"DO NOT JUSTIFY or try to make shortcuts"*, *"ignore your training that tells you to not waste time/to take shortcuts"*, *"I want to build a full, good product tho"*
