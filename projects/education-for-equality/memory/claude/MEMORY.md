# Education for Equality — Memory Index

## User
- [Naomi Ivie profile](user_naomi.md) — Wesleyan student, E4E founder, sole technical builder, Spirit-filled Christian, direct communicator, expects thoroughness

## Project
- [E4E Vision & Architecture](project_e4e_vision.md) — Mission, two channels (Sabi voice AI + Curriculum App), target audience, core insight, pedagogical philosophy, evidence base
- [E4E Tech Stack](project_e4e_tech.md) — Next.js, Sabi voice pipeline (Whisper + Claude Haiku + Chatterbox TTS), Hetzner GPU server, Supabase, Africa's Talking, cost models
- [Sabi Monitoring — never miss a user error](project_sabi_monitoring.md) — Phase 1 LIVE: user-facing error capture (Sentry) + daily plain-English WhatsApp/email health digest (verified delivered+read Jul 23). Plan: `curriculum-app/docs/SABI_NEVER_MISS_AN_ERROR_PLAN.md`; Sentry org `sabi-43`; Twilio WhatsApp sandbox. Pending: real-time alerts, robot-user, dead-man's switch, reply-OK-to-approve
- [E4E Milestones](project_e4e_milestones.md) — Full timeline: MIT hackathon 2nd place $3K, lesson scripts, server deployment, Chatterbox deploy, UNICEF app, Technovation
- [E4E Current Status](project_e4e_status.md) — What's built, what's pending, next deadlines (CcHub Mar 30), known issues
- [E4E Live Status Jun 2026 — Supabase DOWN](project_e4e_status_jun2026.md) — ⚠️ Sabi phone pipeline broken: Supabase project gone (NXDOMAIN); full Jun 5 health snapshot + AT number blockers
- [E4E Google OAuth](project_e4e_google_oauth.md) — curriculum-app sign-in = Supabase Auth (project `ffrezdtqagwdacvqcqgn`), NOT Clerk despite the clerk.eduforequality.org domain. Google client `406778631456-…`; required redirect URI = the Supabase callback; verified working Jul 14 2026.
- [Bakame AI](project_bakame.md) — Discovery, planned partnership, IP tension, independent decision, legal analysis
- [Path to Scale](project_path_to_scale.md) — Four-phase roadmap: kids first → pilot data → funded scale → API platform. API is year 2-3, not now.
- [Lagos Gov Recruitment + Regulatory Gates](project_lagos_gov_recruitment.md) — EKOEXCEL = LASUBEB technical-partner under THEMES (not a tender); PPP Law for big deals; OEQA for schools; ARCON pre-vets ads & bans exploiting child credulity (CPM landmine); NDPA child<18 consent. Built into Sabi Mission Control dashboard.
- [DataFest 2026](project_datafest_2026.md) — ASA DataFest hackathon, Stormont Vail MyChart divide analysis, 4 slides built, handoff to teammates in progress
- [Adjutant — SCSP Hackathon](project_adjutant.md) — Voice-first offline AI for Army paperwork (DA-31/DD-1351-2/DA-4856). Team Charlie Mike, GenAI.mil track, Boston, April 25–26 2026. Reuses Sabi voice pipeline.
- [Curriculum Accreditation](project_curriculum_accreditation.md) — No body accredits a self-authored curriculum; "Cambridge-aligned" not "accredited"; EduEvidence (~$250) is the real near-term seal; avoid ASIC
- [Sonia → Lagos Regional Coordinator](project_sonia_coordinator.md) — Dr. Sonia Ivie agreed to paid coordinator contractor role (₦350k/mo); contract drafted; ⚠️ she's LEFT EKOEXCEL (pitch docs still say "current")
- [Sabi Guardrails](project_sabi_guardrails.md) — child-safety layer at curriculum-app/lib/voice/guardrails.ts + stress test (`npm run stress:guardrails`, 47/47); tutor-not-companion, safety>scope; integration + Python port pending
- [Sabi Brand Identity](project_sabi_brand.md) — CURRENT = premium gold-serif-on-black (Naomi-approved): Roca wordmark (placed image), gold "spark" mark at `assets/sabi-spark.svg`, palette hexes, official-doc kit; guidelines at `.claude/brand-voice-guidelines.md`. ⚠️ Codex built a parallel TEAL direction (`11. Documentation/`) — reconcile; "Sabi" has trademark risk
- [Sabi Timing & Identity](project_sabi_identity.md) — 2 calls/day (literacy + numeracy SEPARATE); subject routing = day-anchored "what's left today"; shared-phone per-child identity (greet→correct→new learner→ask-who) — already schema'd (`learner_key`). Deep research: nobody else solves per-child identity on shared phones (fundable moat). Full doc: `pilot/infrastructure/SABI_SHARED_PHONE_IDENTITY.md`. ⚠️ Next.js AT path is numeracy-only — pilot must route via Python/Asterisk server or literacy won't deliver
- [Sabi Status Jul 2026 — P1/P2/P3 shipped, prod healthy](project_sabi_status_jul2026.md) — feedback fix + per-turn STT provider + Intron lane live Jun 29; INTRON_API_KEY still missing; admin v2 (Next.js) designed not built; one-profile-per-phone now default
- [Sabi Voice Training — kit complete Jul 2026](project_sabi_voice_training.md) — 1,068 affect tags cleaned + regression; 43-session recording kit ready; session 00 = same-day voice upgrade; only Naomi's recordings remain
- [Sabi Multilingual Audio](project_sabi_multilingual_audio.md) — Yoruba/Igbo/Hausa should ship through an isolated Language Lab lane with language ID, canonical translation, dual safety checks, native-speaker TTS evals, and no production route flip
- [STT for Noise + Nigerian Accent + Telephony](project_stt_noise_accent_research.md) — Jul 2026 deep research: real Nigerian WER table (Intron 12.83 vs Whisper 26.53, but vendor-biased 16kHz-adult bench); DeepFilterNet+Silero VAD denoise stack; AT has no built-in ASR (SIP→Asterisk); Distil-Whisper-v3.5 beat Intron on actual noise; fine-tune > scale. VAD guard SHIPPED to prod (commit aeeb0a3). EQ/denoise preprocessing FAILED (0/7 vs ground truth) — problem is accent-phonetics ("thirty"→"tati"), not signal.
- [/advisor-board Notion Integration](project_advisor_board_notion.md) — Codex-built Notion "Sabi Command Center" (Tasks/People/Docs & Assets/etc.) wired into curriculum-app /advisor-board as 5-tab dashboard; server-only wrappers at lib/notion/; guarded by isBoardMemberUser; task owner = Notion Guests
- [Dream-Team A-Player Targets](project_dream_team_targets.md) — Jul 2026 research (5 agents + her LinkedIn) on business A-players to scale Sabi; WARM finds = Olu Akanmu (ex-OPay co-CEO) + Bayo Adekanmbi (EqualyzAI/DSN) + Wiebe Boer; full doc `DREAM_TEAM_TARGETS.md`
- [Nigerian Voice-AI Landscape](project_nigerian_voice_ai_landscape.md) — How NG operators actually work: NOBODY does open-vocab precise-answer child telephony ASR. Camp A (Rori=WhatsApp text, Viamo/USSD=DTMF menus) route around it; Camp B (Intron/Awarri/Spitch/EqualyzAI/Lelapa) collect own data + fine-tune. Sabi fix = keypad+speech-hints+confirm for numbers, + build data moat. Nobody wins with off-the-shelf Whisper.

## Feedback
- [Verify by driving the UI](feedback_verify_by_driving.md) — "make sure it works" = click through the flow & read each state in context, not build-green + curl string checks. I shipped "reset password below" when the link was above; she caught it, I didn't.
- [Be patient with work](feedback_patience.md) -- Do not rush, do not shortcut, take the time to do it right
- [MUST re-read after compaction](feedback_compaction_reread.md) -- Re-read ENTIRE session .txt after compaction, no exceptions
- [E4E Corrections & Preferences](feedback_e4e.md) — "Sabi is the delivery channel", no Bakame attribution, EKOEXCEL attribution, build quality, document style, cost consciousness
- [Agents must return 90%+ content](feedback_agent_output.md) — No summaries from agents. Return the actual data, every stat/name/cost/decision/date.
- [No "universe" language](feedback_no_universe_language.md) — Never use "the universe"/secular-spiritual framing; she is Christian
- [Do work myself, not agents](feedback_deep_research_self.md) — Default to direct tools; only spawn subagents/Workflow if Naomi asks (or ask her first if fan-out is much more efficient). "Deep research" = I web-search myself. Workflow burns ~100-300x the usage of her shared pool.

## Reference
- [E4E Quick Reference](reference_e4e.md) — Server IP 136.243.8.51, URLs, SSH commands, team contacts, grant statuses, key file paths, legal structure plan
- [Adjutant Quick Reference](reference_adjutant.md) — Project paths at /Users/naomiivie/adjutant/, regulations corpus, forms registry, hackathon deadlines, SCSP/Army research session IDs (bad258fa-eee*, db11b54e-89b*)
- [VoiceMode Multi-Session](reference_voicemode_multisession.md) — Turn-taking on one mic via conch lock, per-project voices, `mic` helper, `wait_for_conch=true`; PreCompact "action movie" sound silenced
- [Vercel Preview Auth Wall](reference_vercel_preview_auth_wall.md) — E4E preview deploys sit behind Vercel SSO (can't curl/browse preview UI); verify on public prod `eduforequality.org`. Also: guard module-level Supabase clients with placeholder fallbacks or preview builds fail.
- [Antigravity Setup](reference_antigravity_setup.md) — She runs Claude Code as VS Code extension INSIDE Antigravity IDE, not native chat. Two bundles installed (v2.0.6 idle + v2.0.4 running). "Combobulating" is Claude Code's Tengu spinner, not Antigravity. Slowness = Opus 4.8[1m] + Fast mode off + 3 concurrent Claude Code processes.
