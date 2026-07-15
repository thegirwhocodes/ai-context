========================================================================
AGENT RESEARCH: Deep-read megasession 262aa5fe
Session: 3b8ddd08-9e23-4598-83dd-60902b9107f3
Time: 2026-06-18 17:55:05 UTC
========================================================================

Read the ENTIRE session transcript at this absolute path (it is ~1.9MB, larger than one read — read it in full using multiple Read calls with offset/limit until you reach END OF SESSION):

/Users/naomiivie/Education for Equality/.claude-sessions/262aa5fe-cda2-4ed7-a392-fae7f4a7f583.txt

This is the most recent large "Education for Equality / Sabi" build session. I need you to return AT LEAST 90% of the SUBSTANTIVE content — do NOT summarize, do NOT give "key takeaways." Report the actual content: every technical decision, every architecture choice, every bug found and fix applied, every config value (URLs, phone numbers, API keys/agent IDs, model names, env vars), every cost/price figure, every person/org/contact name, every date/deadline, every grant/funding status, every curriculum decision, every research finding, and every explicit instruction or preference Naomi (the user) stated.

Ignore pure tool-call noise (file listing chatter) but capture WHAT was found/changed and WHY. Organize your output under clear headings (e.g., Voice pipeline / Telephony / Supabase / TTS / Curriculum / Funding / Decisions / Naomi's instructions / Open issues). Preserve exact identifiers verbatim. Your response should be a dense, faithful extraction I can rely on as if I read the file myself. Length is not a concern — completeness is.

----------------------------------------

I've now read the entire session from start to END OF SESSION. I have complete coverage of all 36,257 lines. Let me compile the full extraction.

This was a sprawling session spanning 2026-03-19 to 2026-06-09. Here is the complete, faithful extraction.

---

# Full Extraction: Session 262aa5fe (Education for Equality / Sabi)

**Span:** 2026-03-19 19:46 → 2026-06-09 22:02 UTC. 2,824 messages, ~1.9MB. Work happened across many dates: Mar 19, 24, 25, 28, 30, 31; May 1; Jun 6, 9 (multiple context compactions throughout).

The session breaks into distinct phases: (1) exhaustive context recovery, (2) folder reorganization, (3) Twilio voice debugging, (4) the PCE NVA application + economic-data deep dive (the dominant thread), (5) server load testing & cost re-modeling, (6) website partner section + advisor agreements + brand strategy + PCE Capstone (May 1), (7) legal/grant funding strategy (Jun 6), (8) final Africa's Talking voice-call debugging that ended with a Twilio pivot (Jun 9).

## Identifiers / Config (verbatim)

- **Hetzner server:** GEX44, IP **136.243.8.51**, RTX 4000 SFF Ada (20GB VRAM), Intel i5-13500 (14 cores), 64GB DDR4, 2×1.92TB NVMe, Falkenstein Germany. **€184/mo (~$203)** + €79 (also cited €264/€312) setup. Price rose to €212.30 on April 1, 2026. Bigger option: **GEX131** — RTX PRO 6000 Blackwell, **96GB VRAM**, 256GB DDR5, Xeon Gold 5412U, **€838 (~$920)/mo**.
- **Domains:** `eduforequality.org` (Cloudflare, ~$7.50/yr, frontend on Vercel), `sabi.eduforequality.org` (Vercel frontend), `api.eduforequality.org` (Hetzner backend). Old: `curriculum-app-eta.vercel.app`. GoDaddy `educationforequality.org` expired Mar 22, 2026.
- **Twilio:** number **+17153122345**, Account SID **ACc273246e24dac4d9ddaad3b80617bbe4**, Auth Token **7e8b4aa898cb0a5e9302d8445269ac6a**. Trial account (the "you have a trial account" message was being mistaken for an "application error"). Balance ~$12.86.
- **Africa's Talking number:** **+2342017001459** (Nigerian voice number). Webhooks: `/api/sabi/at/incoming` and `/api/sabi/at/events`. AT wallet ~NGN 18,432 (~$11.50).
- **Supabase:** project ref `ffrezdtqagwdacvqcqgn`. service_role JWT given inline (line 3318): `eyJhbG...W48R1gojirBY-g8OvQtw06gwWns76ZpzC0EczIabmKw`. Tables: `sabi_students`, `sabi_sessions`, `sabi_active_calls`, `sabi_sms_log`. Audio bucket: `sabi-audio`.
- **Sentry:** org slug **sabi-43**, auth token `[REDACTED:sentry-user-token]` (Claude flagged it should be regenerated). Integrated by Jun 9 for call-trace debugging.
- **GitHub:** `github.com/thegirwhocodes/sabi-server` (Asterisk commit `3633db8`).
- **LLM model id:** `claude-haiku-4-5-20251001` (used in both `llm.py` and the ElevenLabs Custom LLM route, max_tokens 200 voice / 300 text).
- **ElevenLabs:** Olufunmilola voice ID `9Dbo4hEvXQ5l7MXGZFQA`; Bukola voice ID earlier. Impact Program coupon `IMPACTNONPROFITMARCH2026-E16CC9D7` (Creator plan, 100K credits/mo free for a year, **must activate by April 3, 2026**, from Richard Cave, Partnerships). Logo backlink required.
- **YarnGPT:** `https://yarngpt.ai/api/v1/tts`, Bearer auth. Default voice **Wura**; others Chinenye, Adaora, Idera.
- **Chatterbox Turbo:** self-hosted port 8001, MIT license, ~4.5GB VRAM, default speaker "wura", "Sabi"→"Sahbee" pronunciation fix, ₦→"naira". Naomi's voice clone from 29s recording. Reference voices on server: bukola, lagos295, naomi, wura.
- **Instagram:** @_educationforequality. Demo video: `https://youtu.be/KUGy9RsFXzA`. Demo URL with key: `https://eduforequality.org/sabi/demo?key=yarn2026` (also earlier `?key=SECRET`/`SABI_DEMO_KEY`).
- **Email:** info@eduforequality.org; nivie@wesleyan.edu; naomi.ivie04@gmail.com.

## Voice pipeline / architecture (current deployed state)

- **STT:** Whisper large-v3 self-hosted (faster-whisper), Nigerian English prompt bias (naira, garri, suya, okada, danfo, keke, oya, wahala, etc.) — "single biggest accuracy boost without fine-tuning." Web demo uses Groq Whisper.
- **LLM:** Claude Haiku primary, Ollama Llama 3.1 8B fallback (self-hosted). RAG via Supabase pgvector (916 embeddings, all-MiniLM-L6-v2, reduces tokens ~60-70%).
- **TTS (phone):** Chatterbox primary → YarnGPT fallback. **TTS (web):** ElevenLabs primary → Chatterbox → YarnGPT.
- **Telephony:** Africa's Talking (₦3/min inbound, ₦15/min regular outbound, ₦3/min SIP both ways, ₦5,375/mo number maintenance = AT's cut) + Twilio (US demo). Flash-callback model on AT SIP designed (child beeps free, server calls back at ₦3/min). Asterisk PBX deployed (8 config files, FastAGI port 4573, dialplan `[from-at]`/`[sabi-callback]`, PJSIP `[africastalking]` trunk via IP whitelist of 136.243.8.51).
- **Whisper AfriSpeech-200 fine-tuning:** still UNRESOLVED (OOM at 64GB RAM — HuggingFace Trainer CPU memory explosion when processing real audio).

## Key NEW work this session

**1. Folder reorganization (Mar 19):** Reorganized E4E root into a 1-10 numbered scheme by substance (Naomi dictated the exact names): 1.The Problem, 2.The Solution/Sabi, 3.The Evidence, 4.Telephony & Infrastructure, 5.Cost & Feasibility, 6.Pitch & Applications, 7.Legal & IP, 8.Partnerships & Outreach, 9.On the Ground, 10.Bakame, + archive/assets/coursework. Files duplicated where they straddle. The 625 agent-research files were classified into the same 1-10 scheme; a `research-agents/` symlink was created in project root. CLAUDE.md got the "Research-Before-Deciding" rule added (Naomi insisted her impassioned all-caps text be preserved, not replaced).

**2. Twilio voice debugging (Mar 19-24):** Built `sabi-server/voice_twilio.py`. Bug chain fixed: 404 (code baked into Docker image, needed rebuild) → 500 (missing Supabase service_role key) → 500 (`maybe_single()` returns None in supabase-py 2.x → switched to `.execute()`) → 500 (missing `current_module`/`skills` columns → used `current_level`, dropped `skills`) → Chatterbox couldn't reach `localhost:8001` from container (Docker networking) → latency timeout. Discovered Twilio is a **trial account** (the "application error" IS the trial message). Naomi rejected "one moment please" filler and the Polly/Hausa-sounding default voice. Eventually pointed Twilio back to the old working Vercel pipeline (`<Gather>`+`<Say>`+Claude, no audio files). **ElevenLabs math:** 100K credits = ~41 calls/month — not enough for pilot; decision: Chatterbox (free, unlimited) for phone, ElevenLabs for web demo.

**3. PCE New Venture Awards application (the dominant thread, Mar 25-31):** Created `6. Pitch & Applications/PCE_NVA_APPLICATION.md`. Wesleyan Patricelli Center NVA — for-profit & nonprofit tracks, **$8,000 to track winners, $5,000 to other finalists**, due April 1, 2026; public pitches April 17 Memorial Chapel. Applied as **Education for Equality** (nonprofit track), not Sabi. 5 questions, 350-word max each + 150-word AI-use statement. Incorporated extensive feedback from advisor **Ahmed Badr** (PCE Director; full transcript pasted): lead with the point not stats; explain audience choice; map 3 technical pieces to user-experience beginning/middle/end; mention course lifespan; surface government connections; be succinct; mention hybrid nonprofit/for-profit potential. Linked Map the System Google Drive research (3+ years). Claude self-graded it 86→92→ effectively higher after adding board.

**4. Economic-data deep dive ($40B figure — extensively re-verified):** Created `3. The Evidence/ECONOMIC_COST_OF_EDUCATION_CRISIS_IN_NIGERIA.md` and `THESIS_PROPOSAL_ECONOMIC_COST_OF_OOSC_NIGERIA.md`. Key findings, traced source-by-source (Naomi pushed hard against hallucination):
   - The **$40 billion/year** OOSC GDP loss was **wrongly attributed to "SBM Intelligence"** across all docs; the real source is **CSEA/IDRC** (Centre for the Study of the Economies of Africa + IDRC Canada), applying **Milan & Burnett (2014)** "Exclusion from Education" methodology (Results for Development / Educate A Child). All docs + website + applications were updated SBM→CSEA/IDRC.
   - Micro approach = **7.83% of GDP (~$40B at 2013 GDP of ~$510B)**; macro (Barro & Lee growth regression) = **13.03% (~$56B)**. From the actual Milan & Burnett tables: Nigeria % non-completing OOSC = **23.7%**, primary wage premium = **30.0%** (Psacharopoulos & Patrinos 2011 + Colclough 2009, NOT Aromolaran), secondary premium 14.0% × 43% transition × 50% completion = 0.71%. 23.7%×30%=7.12% + 0.71% = 7.83%.
   - The $40B counts **OOSC only** (never-completed-primary) — NOT the 23M enrolled-but-can't-read children. At current GDP ($285B) it's ~$22B, but OOSC rose 10.5M→18.3M (+74%), netting back to ~$39B.
   - **World Bank HCI+ 2026 (confirmed from screenshots Naomi added to 3. The Evidence/):** Nigeria pillar scores — Health **33**/50, Education **64**/188, Employment **34**/87, total **131**/325. Education sub-indicators: preschool 0.5, expected years schooling 8.7, school quality (HLO) 318/625, tertiary completion 11.3%. Nigeria = lower-middle income. Education gap to LMI top performer (109) = **45 points** = ~**64-65% of the total human-capital deficit**. 111% of future earnings lost (vs ~51% global avg). +20% labor earnings if 12 effective years. HOPE-EDU = **$500M** World Bank for Nigerian foundational learning (April 2025).
   - Nigeria-specific (Aromolaran 2004): primary return ~2.5%/yr, ~15% over 6 years. Literacy premium: child who can read earns **NGN 4.4M (~$2,760) more lifetime** (2%→8% return; NGN 22,500 vs 31,700/mo). This is the defensible per-child floor; CSEA's macro $40B can't be cleanly divided per-child. Impact framing settled on: 100,000 children = $276M lifetime / $6.9M annual; 1M = $2.76B; ceiling (full trajectory) $6,563/child.

**5. New cost/revenue docs + corrected scale modeling (Mar 28-31):**
   - `5. Cost & Feasibility/REVENUE_AND_PROFITABILITY.md` (TAM/SAM/SOM). Adult market: TAM ~73M (53M illiterate adults + ~20M innumerate), SAM ~45M, SOM 30K-100K (Lagos). Pricing tiers: children free; adult basic ₦500-1,000/course; adult professional (job interview prep, financial literacy, trade skills, English, exam prep, health) ₦2,000-5,000; private-school B2B ₦5,000-10,000/mo (vs human tutors at 10x). Sweet spot ₦2,500-3,000/course = 40-48% margin.
   - **Load test (`load_test.py`, Mar 30) corrected the optimistic numbers.** Solo turn 3.3s; at 5 concurrent calls STT 12.83s, TTS 14.23s, 13/15 turns FAILED. Real capacity: **~300-500 students per single GEX44 server**, NOT the 5,000-10,000 the Cost Breakdown claimed. Cause: Whisper (4GB) + Chatterbox (4.5GB) + Ollama (6GB) contend for 20GB VRAM. Fixes discussed: stop Ollama; Whisper medium; split architecture (dedicated voice + LLM servers); GEX131 96GB; Phi-3.5 Mini. 
   - **Cerebras discovery:** Llama 3.1 8B at **$0.10/M tokens** (~$0.0012/call, $2.38/student for 2,000 calls), <0.1s latency, frees 6GB VRAM. With Cerebras LLM, one GEX44 (Whisper+Chatterbox only) ≈ 5,700 students; cost ~$0.16-0.81/student. Self-hosted-at-scale split architecture + telco zero-rating = $0.67-4.87/student/year.
   - Per-student costs (realistic): 300 kids/10mo self-hosted = $5,448 ($18.16); 5,000 = $11.70; with telco zero-rating $0.41-2.03. Pilot (300 kids, 10 weeks, AT callback) = ~$713 ($2.38/student). Alpha Technologies toll-free is its own SIP provider (₦14/min + ₦688,538/yr + ₦200K deposit, 24hr activation) — 4.7x more than AT flash callback, rejected for pilot.

**6. Infrastructure-collapse research refresh (Mar 31):** Nigeria needs **1,107,854 classrooms** + **194,876 teachers** (UBEC, July 2024). 4,000+ schools have no classrooms; 62% lack potable water, 78% no functional toilets (NBS 2022, worse than the earlier UBEC 31%/39%); only 14% meet basic safety; 58:1 pupil-qualified-teacher ratio; ₦68B dormant UBEC funds. ~$11-22B just to build the classrooms.

**7. Website + advisor work (May 1):** Built a "Built with and backed by" partner-logo section in `curriculum-app/app/page.tsx` (ElevenLabs, Wesleyan PCE, UNICEF Generation Unlimited × Technovation, MIT Sloan Africa Business Club). Long legal discussion: don't put EKOEXCEL/LASUBEB *logos* (no relationship with the company) but DO name advisors by their verified CVs. Drafted 7 advisor agreements in `7. Legal & IP/advisor-agreements/` (00_TEMPLATE + Adefisayo, Sonia Ivie, Odigboh, Tanimola, Richard Ivie, Joshua Ivie, Ogunlewe). **Hon. Folasade Adefisayo** (former Lagos Commissioner of Education 2019-2023, launched EKOEXCEL) added as advisor. **Remi Tanimola** (20+ yrs public primary education) added.

**8. Brand strategy decision (May 1):** Deep research — **keep Education for Equality as the parent 501(c)(3) nonprofit; Sabi is the flagship product** (Mozilla/Firefox, Wikimedia/Wikipedia pattern, per the existing LEGAL_ROADMAP IP-licensing structure). Don't abandon E4E (would lose 501(c)(3) eligibility, HOPE-EDU access, ~$1M+ non-dilutive capital). Put curriculum app + research site in maintenance mode; all engineering into Sabi. One-line identity: "Education for Equality is a nonprofit teaching every African child to read. We deliver that mission through Sabi, an AI voice tutor that works on any phone."

**9. PCE Capstone (May 1):** Created `6. Pitch & Applications/PCE_CAPSTONE_2026.md` (strategy plan + prototype). Claude initially flagged the PCE Fellowship AI-use prohibition (Honor Code risk) and refused to write; Naomi said proceed; doc was aligned to the NVA claims, with the YouTube demo + sabi.eduforequality.org links and an honest note that the live demo was temporarily down due to mid-edit.

**10. Legal/grant funding strategy (Jun 6):** CT incorporation done; Nigerian incorporation delayed; Naomi asked what's next for corporate funding. Findings: **biggest blocker is the missing IRS 501(c)(3) determination letter** (file Form 1023-EZ $275 if <$50K projected, else Form 1023 $600 long-form — likely the latter given grant pipeline) + missing policy package (Child Safeguarding, COI, Whistleblower, Data Privacy/NDPA, Anti-Bribery, etc.). Bridge via fiscal sponsor (Players Philanthropy Fund, 6% fee). **CcHub × Mastercard EdTech Fellowship Cohort 4 CLOSED April 10, 2026** (Cohort 5 in 2027; requires Nigerian for-profit Ltd, majority Nigerian-owned). **UNICEF Venture Fund requires for-profit Ltd — NGOs ineligible** (the March 10 application is at risk). Mastercard Foundation direct = invitation-only + African-led requirement. **Gates EdTech & AI Fund ($40M w/ ADQ, RFP launching 2026) = single best fit — watch weekly.** Cold-applyable now: DRK Foundation ($300K/3yr + $500K in-kind, rolling — top priority), AU Innovating Education in Africa ($50K), Builders of Africa's Future, D-Prize, Tony Elumelu, Westly Prize ($100K), Cartier Women's Initiative, Echoing Green (opens Sept 2026), MIT Solve, Jack Ma ABH. AI-generated CcHub applications = auto-disqualification. USADF requires 100% African-owned (skip until Nigerian Ltd).

**11. Final AT voice debugging → Twilio pivot (Jun 9, the session's end):** Naomi made 13 real calls to +2342017001459; most aborted 0s. Claude initially (wrongly, with incomplete Sentry data) blamed cold-start/Supabase env. **Real root cause found via the AT dashboard call-hop log:** AT's saved routing was still pointed at a dead localtunnel URL `https://short-waves-rule.loca.lt/api/sabi/at/incoming` (a config ChatGPT-in-Antigravity had introduced), returning **503 Tunnel Unavailable** on every call. Production (`eduforequality.org`) was confirmed healthy (HTTP 200, valid greeting XML, Supabase working). Claude pushed back on ChatGPT's localtunnel advice (also noted AT sends `application/x-www-form-urlencoded`, not JSON). URL-flush attempts and tunnel-bridge workarounds failed; concluded AT support must clear the routing cache (drafted support email to voice@africastalking.com). Also fixed an STT confidence-gate bug that was rejecting valid Whisper transcripts (e.g. `"Naomi. Thank you. Let do 20 minutes Energy ten"` rejected at confidence<0.3). Set up Node/npm PATH for Antigravity via `~/.zshenv` (Homebrew + /usr/local/bin). Naomi, frustrated ("YOU HAVE 30 MINUTES... STOP BULLSHITTING ME"), prompted the final pivot: **repointed Twilio +17153122345 from an unconfigured ElevenLabs ConvAI agent to `/api/sabi/voice/incoming`** and verified a working 3-turn synthetic conversation (Polly.Amy/en-GB, en-GH speech detection). **Session ended with: "IT WORKS — dial +17153122345"** for interactive Sabi, while the AT Nigerian number remained blocked on AT support and the Bukola/Nigerian voice on Twilio remained outstanding (Polly.Amy default).

## People / orgs

- **Naomi Ivie** — founder, Wesleyan, sole technical builder.
- **Dr. Sonia Ivie** — Naomi's mother, Director of Schools EKOEXCEL/NewGlobe (1,016 schools, 500,000 pupils); access to LASUBEB data + Lagos State government contract negotiators.
- **Joshua Ivie** — Head of Innovation, Bluechip Technologies (400+ employees, 9 African countries).
- **Richard Ivie** — Naomi's father, Executive Director Corruption Observatory, ISO 37001 anti-bribery, trains government officials at all levels.
- **Rhoda Odigboh** — CEO Kizazi, ex-NewGlobe Regional Director (managed EKOEXCEL & EdoBEST, trained 14,000+ educators).
- **Barrister Adejoke Ogunlewe** — Koriat Law, NGO/children's-rights law.
- **Hon. Folasade Adefisayo** — former Lagos Commissioner of Education 2019-2023.
- **Remi Tanimola** — 20+ years public primary education.
- **Ahmed Badr** — PCE Director (advisor on NVA). **Shiv Soin** — PCE Entrepreneur-in-Residence (capstone instructor). **Marisa MacClary** — PCE EiR.
- **Chris Folayan** — Luma Learn (WhatsApp AI tutor, 110K+ learners).
- **Bakame AI** — Happy Niyorurema (Rwanda) + Mame Diarra Niang (Senegal), TCU students; Rasa-based (MBAZA-NLP), not formally incorporated, won $50K Global Best M-Gov Award. Decision: independent from Bakame; "two separate products, B2B vs B2C."
- Former Nigerian Minister of Education connected via Naomi's church.

## Funding status snapshot

MIT Africa Business Challenge: **WON 2nd place, $3,000**. Wesleyan grant: $1,200 received. Technovation/UNICEF GenU AI Ventures: accepted (cohort). UNICEF Venture Fund $100K: submitted Mar 10 (at risk — needs for-profit Ltd). CcHub/Mastercard $100K: missed (Cohort 4 closed Apr 10). PCE NVA $8K: drafted this session, due Apr 1. EIN obtained; CT 501(c)(3) incorporated; 1023 not yet filed; Nigerian CAC delayed.

## Naomi's stated instructions/preferences (this session)

- Read everything **herself** (Claude), not via agents — repeatedly insisted, caught Claude delegating to agents and returning summaries; demanded direct reads of session transcripts and all docs.
- Re-read full session `.txt` after each compaction (happened several times).
- Do NOT hallucinate or reverse-engineer calculations to hit an expected answer; trace every figure to its actual source paper.
- Keep $40B but with the correct CSEA/IDRC source; verify the 40%/70%/72.6% stats against the actual PDFs.
- Folders numbered 1-10 by substance, in gitignore, files duplicable across folders.
- Pilot uses AT ring-back model at ₦3/min + self-hosted stack (not toll-free).
- Apply as Education for Equality, keep E4E as parent + Sabi as product.
- Be concise (a system-reminder enforced "respond with just the action, no thinking block" for much of the May work).
- Final: make the phone call actually work end-to-end before coming back.

## Open issues at session end

- AT Nigerian number +2342017001459 blocked on AT support clearing the stale localtunnel routing cache.
- Twilio path works but uses Polly.Amy, not Bukola/Nigerian voice (ElevenLabs streaming needed, ~1hr work).
- Whisper AfriSpeech-200 fine-tuning OOM still unresolved.
- IRS Form 1023 not filed; policy package not written; Nigerian for-profit Ltd not registered (blocks UNICEF/CcHub).
- Pre-pilot with 10 Nigerian kids pending working telephony.
- Sentry auth token exposed in transcript (flagged for regeneration).
- Server real capacity (~300-500/server) contradicts older Cost Breakdown claims (~5,000-10,000) — docs may need reconciling; Cerebras + split architecture is the path.
agentId: a0630530afd043ac6 (use SendMessage with to: 'a0630530afd043ac6' to continue this agent)
<usage>subagent_tokens: 500837
tool_uses: 31
duration_ms: 363534</usage>

========================================================================
END OF AGENT RESEARCH
========================================================================