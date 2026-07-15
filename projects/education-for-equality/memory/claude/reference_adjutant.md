---
name: Adjutant Quick Reference
description: Adjutant project paths, regulations corpus, demo deadlines, key files, SCSP/Army research session IDs, judge backgrounds, voice pipeline + bulk crawler endpoints.
type: reference
originSessionId: 3f0fd587-a8ad-4ce6-86a4-cb6c031d7c7e
---
# Adjutant Quick Reference

## Paths

- **Project root:** [/Users/naomiivie/adjutant/](/Users/naomiivie/adjutant/) (separate from E4E)
- **Python package:** [/Users/naomiivie/adjutant/adjutant/](/Users/naomiivie/adjutant/adjutant/)
  - server.py, llm.py, rag.py, stt.py, tts.py, pdf_fill.py, per_diem.py, prompts.py, forms.py, **voice_loop.py** (untracked, NEW)
- **Founder-facing build plan:** [foundry/BUILD_PLAN.md](/Users/naomiivie/adjutant/foundry/BUILD_PLAN.md) — phase-by-phase 30-hour schedule with cut-list
- **Engineering plan:** [foundry/CODE_PLAN.md](/Users/naomiivie/adjutant/foundry/CODE_PLAN.md) — 17 build steps with acceptance gates, file-by-file
- **Voice pipeline upgrade plan:** [foundry/VOICE_PIPELINE_PLAN.md](/Users/naomiivie/adjutant/foundry/VOICE_PIPELINE_PLAN.md) — NEW. ChatGPT-AVM-feel voice loop, 7 phases V0–V6, ~7.5 h, 1.0–1.4s ESV→FAO target on M2. Architecture A (recommended) is what was built. Cut-list to Architecture C for fallback.
- **Saturating corpus plan:** [foundry/SCRAPING.md](/Users/naomiivie/adjutant/foundry/SCRAPING.md) — NEW. APD + DTIC + eCFR ingestion → ~500 docs / ~500K chunks / ~1.5GB; cross-encoder reranker mandatory past ~200K chunks. ~30 LOC patch shown.
- **Demo script:** [docs/DEMO_SCRIPT.md](/Users/naomiivie/adjutant/docs/DEMO_SCRIPT.md) — 5-min judge walkthrough with 5 beats and Q&A bank
- **Persona:** [docs/PERSONA.md](/Users/naomiivie/adjutant/docs/PERSONA.md) — SGT Maya Chen
- **Registration email template:** [docs/SCSP_REGISTRATION_EMAIL.md](/Users/naomiivie/adjutant/docs/SCSP_REGISTRATION_EMAIL.md) (sent Sat 2 PM)
- **30-hour table:** [docs/30_HOUR_PLAN.md](/Users/naomiivie/adjutant/docs/30_HOUR_PLAN.md) — block-by-block ownership grid
- **Corpus PDFs:** [corpus/](/Users/naomiivie/adjutant/corpus/) (76 MB / 15 files + per_diem.json)
- **Blank form PDFs:** [forms/](/Users/naomiivie/adjutant/forms/) (3 forms)
- **FAISS index:** `.faiss_index/faiss.bin` (25 MB) + `chunks.pkl` (12 MB) — 16,301 chunks indexed (12 of 15 docs; 3 un-ingested)
- **Filled form output:** [filled_forms/](/Users/naomiivie/adjutant/filled_forms/) — 8 generated PDFs from prior runs
- **TTS audio output:** [audio_cache/](/Users/naomiivie/adjutant/audio_cache/) — 10 reply WAVs + cues/ subdir
- **TTS cue cache:** [audio_cache/cues/](/Users/naomiivie/adjutant/audio_cache/cues/) — NEW. 9 pre-generated WAVs loaded into RAM at startup: thinking_0..thinking_4, retry_low_conf, ack_da31, ack_dd13512, ack_da4856
- **Kokoro TTS model:** [models/kokoro/](/Users/naomiivie/adjutant/models/kokoro/) — kokoro-v1.0.onnx (325 MB) + voices-v1.0.bin (28 MB)
- **Web frontend:** [web/](/Users/naomiivie/adjutant/web/) — vanilla HTML/JS. NOW: continuous-listen mode primary (AudioWorklet → WS), push-to-talk fallback hidden under `<details>`. audio_worklet.js does 48k→16k downsample + 32ms Int16 PCM frames.
- **Bulk crawler:** [scripts/bulk_crawl_apd.py](/Users/naomiivie/adjutant/scripts/bulk_crawl_apd.py) — NEW. ~450 LOC. HTTP-first, Playwright fallback for APD. TIER_1 hardcoded ~25 docs ready to download. `python scripts/bulk_crawl_apd.py --tier 1` runs.

## Adjacent project research files (in E4E project root)

- [SCSP_ARMY_PAPERWORK_PAIN_RESEARCH.md](/Users/naomiivie/Education for Equality/SCSP_ARMY_PAPERWORK_PAIN_RESEARCH.md) — 320 lines, RAND/MWI stats, IPPS-A/DTS pain points, GenAI.mil critique, persona ranking, judge backgrounds, pitch script. Persona A (junior NCO TDY) recommended.
- [SCSP_DA_FORM_CONCIERGE_PRIOR_ART_SCAN.md](/Users/naomiivie/Education for Equality/SCSP_DA_FORM_CONCIERGE_PRIOR_ART_SCAN.md) — 205 lines, 7-column gap matrix, Tier 1-5 competitive landscape, judge Q&A bank
- [SABI_DEEP_RESEARCH_DOSSIER.md](/Users/naomiivie/Education for Equality/SABI_DEEP_RESEARCH_DOSSIER.md) — Sabi research dossier (parallel project, voice-pipeline-shared)

## Regulations corpus (15 PDFs in folder, 12 indexed in FAISS)

| File | Authority | Indexed |
|---|---|---|
| AR 27-10 | Military Justice | ✅ (1,519 chunks) |
| AR 600-8-101 | Personnel Processing (in/out) | ✅ (210 chunks) |
| AR 600-8-10 | Leaves and Passes — DA-31 governing reg, ¶ 4-3 cited in demo | ✅ (420 chunks) |
| AR 600-8-22 | Military Awards | ✅ (1,349 chunks) |
| AR 600-85 | Army Substance Abuse Program | ✅ (975 chunks) |
| AR 600-9 | Body Composition | ✅ (164 chunks) |
| AR 623-3 | Evaluation Reporting (NCOERs/OERs) — DA-4856 governing | ✅ (1,440 chunks) |
| AR 670-1 | Wear and Appearance | ✅ (395 chunks) |
| AR 735-5 | Property Accountability | ✅ (1,088 chunks) |
| DA Pam 600-25 | NCO Guide | ✅ (4,637 chunks) |
| FM 6-22 | Leader Development | ✅ (1,152 chunks) |
| JTR 2025-06 | Joint Travel Regulations — DD-1351-2 governing | ✅ (2,952 chunks) |
| **FM 3-0** | **Operations** | ❌ pending re-ingest (31 MB) |
| **DA Pam 600-25 (CMF)** | **Career Management Field** | ❌ pending re-ingest |
| **DA Pam 623-3** | **Evaluation Reporting (eval doctrine)** | ❌ pending re-ingest |

**Run to update:** `python scripts/ingest_corpus.py` (re-builds FAISS over all 15 PDFs).

## Tier 1 expansion targets (in bulk_crawl_apd.py TIER_1, ready to download)

Personnel & admin: AR 350-1 (Training/Leader Development), AR 614-100 (Officer Assignments), AR 165-1 (Chaplain Corps), AR 690-700 (Personnel Relations Civilian)
Investigations / discipline / legal: AR 15-6 (Procedures Investigations), Manual for Courts-Martial 2024, DA Pam 27-9 (Military Judges' Benchbook)
Health / readiness: AR 40-501 (Standards of Medical Fitness)
Safety / security / records: AR 380-5 (Information Security), AR 385-10 (Safety Program)
Joint Publications: JP 1-0 (Personnel), JP 3-0 (Operations), JP 5-0 (Planning)
Doctrine: ADP 6-22 (Leadership), FM 7-22 (Holistic Health/Fitness), FM 7-0 (Training), ADP 1 (The Army)
DA Pamphlets: DA Pam 600-3 (Officer Pro Dev), DA Pam 600-8-22 (Awards Procedures)
Reserves / civilian / safety / recreation: AR 135-178 (Enlisted Admin Separations), AR 600-43 (Conscientious Objection), AR 215-1 (MWR Programs), AR 615-1 (Officer Assignment Defaults)

## Tier 1.5 targets (listed in foundry/SCRAPING.md but not in bulk_crawl_apd.py yet)

Personnel: AR 614-200, AR 600-8-105, AR 600-20, AR 600-100, AR 600-8-2 (Flag), AR 600-8-19 (Promotions), AR 600-8-24 (Officer Discharges), AR 690-950, AR 690-12, AR 135-91
Legal: AR 27-3, AR 27-26, AR 638-2 (Mortuary)
Health: AR 40-66
Records: AR 25-1 (IT), AR 25-22 (Privacy), AR 25-50 (Correspondence), AR 25-400-2 (ARIMS)
Family/MWR: AR 608-99
Pamphlets: DA Pam 600-67, DA Pam 638-2, DA Pam 25-50
Forms: DA-2823, DA-3349, DA-705, DA-5500, DA-2062, DA-1059, DA-67-9

## Forms registered

| Form | Title | Reg | PDF type | Engine |
|---|---|---|---|---|
| DA-31 | Request and Authority for Leave | AR 600-8-10 | XFA-only ("Please wait" page) | reportlab text-on-coordinates overlay |
| DD-1351-2 | Travel Voucher | JTR | Hybrid XFA + AcroForm | pikepdf field-fill (strip /XFA so non-Adobe viewers render) |
| DA-4856 | Developmental Counseling | AR 623-3 | AcroForm-mostly | pikepdf primary, overlay fallback |

## Hackathon timing (today is Sat 2026-04-25)

| Anchor | Time |
|---|---|
| Registration email to hack@scsp.ai | **Sat 2:00 PM** (sent) |
| GitHub link + README submission | **Sun 5:00 PM** |
| Demo to judges | **Sun 5:00–7:00 PM** |
| Phase 2 (AI+ Expo) | **Sat 9 May 2026** at Walter E. Washington Convention Center DC |

## Prizes

| Place | Per track |
|---|---|
| 1st | $10,000 |
| 2nd | $5,000 |
| 3rd | $2,500 |

4 tracks (Autonomous Labs / Electric Grid / Wargaming / GenAI.mil) × 3 places = $70K total Phase 1 pool.

## Judges (Boston)

- **Dr. Sanjeev Mohindra** — MIT Lincoln Lab AI Tech Group lead, ISR & Tactical Systems Division. PhD Cornell, BTech IIT Delhi. CDAO-funded AI test & evaluation researcher. Bio: ll.mit.edu/biographies/sanjeev-mohindra. Will probe for hallucination + sycophancy. Wins on: rigor, retrieval-grounded constraints, side-by-side eval.
- **Dr. Ho-Chit Liu** — Boston co-judge, likely also Lincoln Lab.

## Judges (DC, name carries weight)

- **Stuart Wagner** — Air Force/Space Force CDTO. Built NIPRGPT at AFRL (phased out / Army-blocked Apr 17 2025). Founded BRAVO Hackathon. CS Master's UPenn + LSE public policy. Believes in operational prototypes "10x-100x lower cost than DoD's normal pathway." Bio: safcn.af.mil/About-Us/Biographies/Display/Article/2593412/stuart-wagner.

## Key endpoints (when server runs)

- `http://localhost:8000/` — server health
- `http://localhost:8000/web/` — frontend
- `/health`, `/forms`, `/transcribe`, `/query`, `/voice` — REST routes (legacy push-to-talk + JSON)
- **`/ws/voice`** — NEW WebSocket route for continuous voice loop (binary PCM in, JSON events + WAV chunks out)
- `/filled/<pdf>` — generated form PDFs
- `/audio/<wav>` — TTS replies
- Ollama on `http://localhost:11434`

## Tech stack (pinned by 8GB M1 hardware constraint)

- Python 3.13 (3.14 too new for ML wheels)
- FastAPI / Uvicorn (now also serves WebSocket)
- faster-whisper `small.en` int8 CPU (NOT large-v3 — too heavy for 8GB)
- Ollama + `llama3.2:3b` (NOT llama3.1:8b — swap-thrashed). Streaming via ollama-python `stream=True`.
- sentence-transformers/all-MiniLM-L6-v2 (FAISS embedder)
- faiss-cpu
- pikepdf (AcroForm fill, libqpdf-backed for encryption) + reportlab (XFA overlay fallback)
- **Kokoro-82M ONNX (kokoro-onnx package, Apache 2.0)** — primary TTS, `af_heart` voice, 24kHz
- **Silero VAD ONNX (silero-vad package, MIT)** — server-side VAD, 32ms hop, 0.5 activation threshold
- **soundfile** — WAV bytes encoding for streaming WS path
- pyttsx3 + macOS `say -v Samantha` — TTS fallbacks if Kokoro fails
- ffmpeg (transcodes browser WebM/MP4 → WAV; replaces unreliable PyAV)
- python-multipart (for FastAPI UploadFile)
- python-dotenv
- **playwright (commented out in requirements.txt; install separately for bulk_crawl_apd.py)** — `pip install playwright && playwright install chromium`

**NOT yet pinned in requirements.txt** (installed manually in .venv): kokoro-onnx, silero-vad, onnxruntime, soundfile. Per VOICE_PIPELINE_PLAN.md V0 — pin before final push.

## Competitive landscape (the gap matrix)

| Capability | GenAI.mil | CamoGPT | Ask Sage | Milnerva | SergeantAI | EdgeRunner | **Adjutant** |
|---|---|---|---|---|---|---|---|
| Voice I/O | ❌ | ❌ | ❌ | ❌ | ❌ | listens 1-way | **✅ conversational** |
| Offline | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ tactical | **✅ admin** |
| Cites Reg by section | generic | generic | generic | partial | ✅ (one AR only) | generic | **✅ multi-AR + FM** |
| Auto-fills DA-form PDF | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅** |
| End-to-end persona flow | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅** |
| Hands-free | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅** |

Closest competitors:
- **Milnerva** — $10/mo, 20K users, ex-Army-built. Text-only NCOER/OER writing copilot. iOS shipped. milnerva.com.
- **EdgeRunner AI** — $12M Series A May 2025 (Madrona-led). Apr 2026: EdgeRunner 20B GPT-5-class on-device, deployed with US SOF overseas. Tactical doctrine focus, NOT admin/forms. edgerunnerai.com. Recent press: "Digital Adjutant" tagline (DefensePost Apr 6 2026) — name overlap risk.
- **Ask Sage** — $49M IDIQ, CUI-accredited SaaS, 300K personnel descriptions in a week. Text. asksage.ai.
- **SergeantAI (WWT)** — RAG over AR 670-1 only. Demo project. wwt.com/blog.
- **CamoGPT** — 75K users, transitioning to program of record + Army-specific LLM.

## Headline stats (memorize for pitch)

- **RAND (2019):** Army company leaders work 12.5-hour days — longer than 96% of US workers. <1/3 on readiness.
- **Modern War Institute (West Point):** Companies submit 3–4 dozen monthly reports → 1 week/month for company command teams.
- **Pentagon framing on GenAI.mil:** automating *"thousands of man-hours"* of routine staff processes.
- **Ask Sage proof:** 300K personnel descriptions in a week vs. ~50K hours manual.
- **TAM:** 3M service members × 6 hrs/wk × $25/hr = **$23.4B/yr** in recoverable labor.
- **DefenseScoop quote:** *"Not everyone is sitting in a nice, cushy, air-conditioned office typing away at a computer all day."*

## Acronym primer (the 10 that matter most)

1. **TDY** — Temporary Duty (military "business travel")
2. **DTS** — Defense Travel System (the website soldiers hate; Col. Strong's "Don't Travel Service")
3. **JTR** — Joint Travel Regulations (the 1,000+ page travel rulebook)
4. **DA-31** — Request for leave (most-touched form)
5. **DD-1351-2** — Travel voucher
6. **NCO** — Noncommissioned Officer (sergeants)
7. **S1** — Unit personnel/admin officer (the "HR person")
8. **AR 600-8-10** — The leave regulation (demo cites ¶ 4-3)
9. **GenAI.mil** — The Pentagon AI platform Adjutant runs alongside
10. **EdgeRunner** — The offline-military-AI peer (tactical, not admin)

## Voice pipeline latency budget (M2 target ≤1.4s ESV→FAO)

| Stage | Time | Note |
|---|---|---|
| Audio capture + WS to server | 30–60 ms | localhost loopback |
| Silero VAD silence detection | 600 ms | tune-down to 400 ms post-demo |
| faster-whisper `small.en` int8 (3 s utterance) | 200–400 ms | RTF ~0.1 on M2 |
| Ollama TTFT for llama3.2:3b (cached system prompt) | 150–300 ms | KV cache stays warm between turns |
| First sentence assembly (5–10 tokens) | overlaps with TTFT | sentence buffer flushes on `[.!?]` |
| Kokoro first chunk (warm, resident in RAM) | 200–400 ms | model loaded at startup, not first request |
| WS transport + decode + schedule | 30 ms | |
| **Total ESV→FAO** | **~1.0–1.4 s** | |

**Sabi trick masking the budget:** thinking-cue WAV (`thinking_0..thinking_4`, ~1s pre-rendered "Checking the regs...") queues IMMEDIATELY at end-of-speech, plays in client within ~50ms. User never hears dead air; the actual first sentence audio queues behind the cue.

## SCSP / Army research files (already gathered)

In `~/.claude/projects/-Users-naomiivie-Education-for-Equality/agent-research/` — read these BEFORE doing new web research on SCSP/Army topics:

- **`bad258fa-eee*`** — SCSP hackathon research session: prior winners (Spectre Nov 2024 grand prize $25K, Project Perception June 2025), AGI House, AI Expo Crystal City, Port Sentinel, Sentinel Pilot. ~30 files including WebFetches of expo.scsp.ai, scsp222.substack.com, github.com/scspai.
- **`db11b54e-89b*`** — Army paperwork pain research session: AR/DA Form auto-fill state of art, CamoGPT/Ask Sage/NIPRGPT comparison, EdgeRunner offline LLM, Army S1 paperwork bottleneck, IPPS-A complaints, NCOER/OER time burden, MWI company command stats, AR 27-10/670-1/735-5/600-8-22/600-9/600-85 PDF locations. Project Perception deep-dive. ~50+ files.

Session transcripts:
- [.claude-sessions/db11b54e-89b2-473e-b485-24b7a9698b7e.txt](/Users/naomiivie/Education for Equality/.claude-sessions/db11b54e-89b2-473e-b485-24b7a9698b7e.txt) — 8,228 lines, the main Adjutant build session (Apr 25 18:19 → Apr 26 00:36 UTC at compaction; continued past compaction with Kokoro/Silero/voice_loop/bulk_crawl/SCRAPING.md/VOICE_PIPELINE_PLAN.md work)
- [.claude-sessions/bad258fa-eee1-445d-8edd-6cc575bc8e30.txt](/Users/naomiivie/Education for Equality/.claude-sessions/bad258fa-eee1-445d-8edd-6cc575bc8e30.txt) — 1,783 lines, prior SCSP research session
- [.claude-sessions/b997d564-ec8f-4c14-b674-542be74b8003.txt](/Users/naomiivie/Education for Equality/.claude-sessions/b997d564-ec8f-4c14-b674-542be74b8003.txt) — 123KB, additional Adjutant context

## Key external URLs (for re-download / verification)

**Primary corpus sources:**
- `https://armypubs.army.mil` — AR PDFs and blank DA forms (BLOCKED for non-browser clients — needs Playwright; bulk_crawl_apd.py has the playwright_fetch fallback wired)
- `https://armypubs.army.mil/ProductMaps/PubForm/Active.aspx` — current-revision-only index (target for bulk crawler `--apd-only` mode)
- `https://api.army.mil/e2/c/downloads/2025/06/10/0da05172/jtr-june-2025.pdf` — JTR June 2025
- `https://www.esd.whs.mil/Portals/54/Documents/DD/forms/dd/dd1351-2.pdf` — DD-1351-2
- `https://home.army.mil/<base>/...` — base-mirror pattern that works (worked for 11 of 12 corpus docs)
- `https://irp.fas.org/doddir/army/` — FAS DoD mirror (~300 docs, smaller but reliable; got FM 6-22 here)
- `https://discover.dtic.mil` — DTIC public archive, ~1.5M docs, REST/JSON public API
- `https://apps.dtic.mil/sti/citations/AD<ACCESSION>` — DTIC citation page (HTML metadata)
- `https://apps.dtic.mil/sti/pdfs/AD<ACCESSION>.pdf` — DTIC full-text PDF (only Distribution A available without CAC)
- `https://apps.dtic.mil/sitemap.xml` — DTIC bulk-discovery sitemap-of-sitemaps for unclassified/unlimited reports
- `https://api.ecfr.gov` — eCFR REST API; CFR Title 32 (National Defense), Title 48 (FAR)
- `https://www.ecfr.gov/api/versioner/v1/full/<YYYY-MM-DD>/title-<N>.xml` — full title XML
- `https://www.ecfr.gov/api/versioner/v1/structure/<YYYY-MM-DD>/title-<N>.json` — title TOC structure
- `https://www.ecfr.gov/api/search/v1/results?query=<text>&title=<N>` — search across titles

**Per-diem & travel:**
- `https://open.gsa.gov/api/perdiem-api/` — GSA per-diem rates (live API, replaces 6-city stub)
- `https://www.travel.dod.mil/Travel-Transportation-Rates/Per-Diem/` — DTMO

**Demo competitor URL (Beat 4 kill-shot):**
- `https://gemini.genai.mil` — GenAI.mil's hosted Gemini

## TIER_1 bulk-crawler URLs (already wired in scripts/bulk_crawl_apd.py)

- AR 600-8-10: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN30018-AR_600-8-10-000-WEB-1.pdf`
- JTR 2025-06: `https://api.army.mil/e2/c/downloads/2025/06/10/0da05172/jtr-june-2025.pdf`
- AR 350-1: `https://media.defense.gov/2025/Jul/23/2003759901/-1/-1/0/AR_350-1-001-WEB-2.PDF`
- AR 15-6: `https://www.ucmjlaw.com/wp-content/uploads/2023/02/ar15_6.pdf`
- AR 380-5: `https://irp.fas.org/doddir/army/ar380-5.pdf`
- AR 40-501: `https://dmna.ny.gov/hro/agr/army/files/1557332720--AR%2040-501%20Standard%20of%20Medical%20Fitness.pdf`
- AR 614-100: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN30989-AR_614-100-000-WEB-1.pdf` (may need Playwright)
- AR 165-1: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/r165_1.pdf`
- AR 690-700: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/r690_700.pdf`
- JP 1-0: `https://www.jcs.mil/Portals/36/Documents/Doctrine/pubs/jp1_0.pdf?ver=wzWGXaj9anm9XlmWKqKq8Q%3D%3D` (`?ver` query param required)
- JP 3-0: `https://www.jcs.mil/Portals/36/Documents/Doctrine/pubs/jp3_0ch1.pdf`
- JP 5-0: `https://www.jcs.mil/Portals/36/Documents/Doctrine/pubs/jp5_0.pdf`
- MCM 2024: `https://jsc.defense.gov/Portals/99/2024%20MCM%20files/MCM%20(2024%20ed)%20(2024_01_02)%20(adjusted%20bookmarks).pdf`
- DA Pam 27-9: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/p27_9.pdf`
- ADP 6-22: `https://www.usarcent.army.mil/Portals/1/Documents/regs/ADP_6-22_Army%20Leadership%20And%20The%20Profession%20July2019.pdf`
- FM 7-22: `https://arotc.charlotte.edu/wp-content/uploads/sites/149/2023/04/FM-7-22-Holistic-Health-and-Fitness.pdf`
- FM 7-0: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/ARN20801_FM%207-0%20FINAL%20WEB%20v2.pdf`
- ADP 1: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/ARN18138_ADP%201%20FINAL%20WEB%202.pdf`
- DA Pam 600-3: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/p600_3.pdf`
- DA Pam 600-8-22: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/p600_8_22.pdf`
- AR 135-178: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/r135_178.pdf`
- AR 600-43: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/r600_43.pdf`
- AR 215-1: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/r215_1.pdf`
- AR 385-10: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/r385_10.pdf`
- AR 615-1: `https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/r615_1.pdf`

## APD anti-bot insight (baked into bulk_crawl_apd.py)

armypubs.army.mil checks: User-Agent + Sec-Fetch-Dest + Sec-Fetch-Mode + Sec-Fetch-Site + session cookie set on parent page visit. Bare `requests.get()` returns a 1,226-byte HTML error page. HEADERS dict in bulk_crawl_apd.py satisfies the headers-only checks; Playwright covers the cookie-required pages. >50KB threshold filters error pages.

## Pitch opener (memorize)

> *"Army company leaders work 12.5-hour days — longer than 96% of all American workers — and less than a third of that time is on readiness. Why? Companies submit three to four dozen reports a month. GenAI.mil rolled out to 1.2 million users in December, but the people who need it most — the mechanics, the platoon sergeants, the soldiers in motor pools where the wifi cuts out — don't have desks. So we built Adjutant: voice-first, fully offline, cites the regulation by section, fills the actual DA-31 PDF. Watch this..."* **[pull wifi cable]**

## Saturating-corpus pitch (post-bulk-crawler-run)

> *"Adjutant retrieves over 500 current-revision Army regulations, joint publications, DoD technical reports, and Title 32 of the Code of Federal Regulations — every authoritative source the rank-and-file would ever cite. Half a million chunks, two-stage retrieval with a cross-encoder reranker, all running locally on this laptop. When you ask about leave, we cite AR 600-8-10 paragraph 4-3 *and* the underlying 10 U.S.C. § 701 statute, *and* the RAND analysis explaining why the regulation is worded that way. No internet. No cloud. No leakage."*

## Known link to E4E (Sabi)

The DSN voice surface in Adjutant's business model is an explicit port of E4E's **Sabi voice pipeline** (Whisper → Claude/Llama → Chatterbox TTS over Africa's Talking telephony) onto FedRAMP-compliant gov telephony. Same backend, different telco. Naomi's voice clone runs on Hetzner at 136.243.8.51 for E4E (server was suspended Apr 25 2026 for non-payment — does NOT affect Adjutant which runs 100% locally on M1 Air).

The Sabi → Adjutant code reuse is now even tighter: voice_loop.py explicitly cites "Sabi-pattern" cue queueing (audible "Checking the regs..." within ~50ms of end-of-speech, bridging LLM-prefill gap), and the streaming Ollama → sentence-buffer → async TTS architecture mirrors Sabi's tutoring loop.
