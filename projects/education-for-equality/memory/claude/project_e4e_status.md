---
name: Education for Equality — Current Status
description: What's built, what's pending, next deadlines as of March 2026
type: project
sessions: [ff1faa52, f19ca767, efd7d7d2, 296c88b8]
---

# Education for Equality — Current Status (as of March 18, 2026)

## What's Built & Live
- **Curriculum App**: Grade 4 complete (286+ lessons), deployed at https://curriculum-app-eta.vercel.app and https://eduforequality.org
- **Sabi GPU Server**: Live at https://sabi.eduforequality.org with landing page + API
  - Whisper large-v3 (STT, Nigerian English bias)
  - Claude Haiku API (primary LLM)
  - Ollama Llama 3.1 8B (fallback LLM)
  - Chatterbox Turbo TTS (Naomi's voice, emotion-aware)
  - Africa's Talking telephony integration
- **Sabi Web Demo**: /sabi-voice page on curriculum app (Groq Whisper server-side STT, Claude Haiku, Chatterbox TTS)
- **Lesson Scripts**: 9 modules written (5 literacy phase 1, 4 numeracy, 2 diagnostics) — ~240 lessons total
- **SABI_COPYRIGHT_BRIEF.md**: Ready for Nigerian Copyright Commission submission
- **All research documents**: Research Brief, Lagos Feasibility, Market Analysis, SABI Infrastructure Research, Cost Breakdown, Hard Questions Q&A

## What's Pending / Not Yet Built
- **Lesson scripts remaining**: Literacy Phase 2 (Modules 6-8: Phonics, Blending/Decoding, Reading Comprehension), Numeracy Modules 5-6 (Division, Word Problems)
- **Script engine**: Lightweight Python parser to run lesson scripts deterministically (designed but not finished)
- **Answer matcher**: Started in sabi-server/answer_matcher.py (not completed)
- **Toll-free calling solution**: Africa's Talking doesn't offer toll-free in Nigeria; flash callback or MNO partnership needed
- **AfriSpeech-200 fine-tuning**: Whisper fine-tune on Nigerian English dataset (planned, not started)
- **Grades 5-9 curriculum**: Planned for Q2-Q3 2026
- **Lagos pilot**: Planned for Q4 2026 — needs school partnerships, pre/post assessment design
- **501(c)(3) registration**: Not filed yet (~$325-350 without trademark)
- **Nigerian CAC registration**: Not filed yet (~$75-130)
- **Nigeria trademark for "Sabi"**: Not filed (~$30-65)
- **CMO hire at Wesleyan**: Poster not yet put up

## Upcoming Deadlines
- **April 10, 2026**: CcHub/Mastercard EdTech Fellowship application ($100K equity-free) — STILL OPEN, deadline extended
- **June 8, 2026**: SSL certificate auto-renewal (Let's Encrypt)
- **Q2-Q3 2026**: Grades 5-9 expansion
- **Q4 2026**: Lagos pilot launch

## Awaiting Decisions/Results
- **UNICEF Venture Fund**: Application submitted March 10, 2026 ($100K equity-free crypto)
- **Technovation AI Ventures 2026**: Application submitted March 4, 2026 ($10K equity-free)
- **Harvard Innovation Labs Leadership Experience**: Applied February 2026

## Known Issues
- Sabi voice page (/sabi-voice) is open — no API key gate to protect costs
- Bukola voice sounded Hausa/Fulani — replaced by Chatterbox with Naomi's voice
- Telephony cost to child (NGN 3/min) is a barrier — need callback or toll-free solution