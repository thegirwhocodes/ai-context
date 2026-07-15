---
name: Education for Equality — Milestones & Timeline
description: Chronological project history from inception through current state
type: project
sessions: [ff1faa52, f19ca767, efd7d7d2, 7464be26, 296c88b8, d72670bf, 1f61b0ac, 089265f6]
---

# Education for Equality — Milestones & Timeline

## Phase 1: Foundation (Jan-Feb 2026)
- **Jan 25-Feb 5, 2026**: Project initiated. Curriculum app built (Next.js 16, Supabase, Clerk). Hardcoded Grade 4 content. Created HISTORY.md.
- **Feb 18**: Applied to Harvard Venturing x CUSI Innovation Labs Leadership Experience
- **Feb 19**: Discovered MIT Africa Business Challenge hackathon — Feb 27-28 at MIT, $5K/$3K/$1K prizes, Education track

## Phase 2: Deep Research (Feb 25-26, 2026)
- Finalized Lagos Data Report — mobile penetration, feature phone stats, affordability gaps
- Discovered Bakame AI (Happy Niyorurema + Diarra Niang, TCU students, Rwanda voice AI tutoring)
- Created TIER2_PROBLEM_ANALYSIS.md, PROBLEM_CLASSIFICATION.md, RESEARCH_BRIEF_SENDABLE.md
- Created BAKAME_EFE_LESSON_DESIGN.md — mapping app lessons to voice calls
- Key insight: Nigeria's crisis is a learning problem, not an access problem

## Phase 3: MIT Hackathon Build Marathon (Feb 27-28, 2026)
- **Named the product "Sabi"** (Nigerian Pidgin for "to know")
- Built Sabi from scratch in one night: web chat, Twilio voice calls, ElevenLabs TTS (**Bukola** custom Nigerian voice — team had already moved off stock Olufunmilola before the pitch), Supabase persistence, adaptive learning
- Created Y-Combinator style pitch (3 speakers: Naomi, Grace, Nali)
- Created 14-slide deck, 25 anticipated Q&As (SABI_HARD_QUESTIONS.md)
- Created Cambridge Grade 4 curriculum plan (286+ lessons)
- **WON 2ND PLACE — $3,000 PRIZE**

## Phase 4: Post-Hackathon (Mar 3-5, 2026)
- Website redesigned for literacy/numeracy focus
- Bakame IP tension arose — Bakame said Sabi "sounds like their idea"
- Naomi decided to move forward independently (no NDA signed, different markets, ideas not copyrightable)
- Legal roadmap created: 501(c)(3) + Nigerian CAC registration
- **Technovation AI Ventures 2026 application submitted** (deadline Mar 4)
- GitHub repos made private for IP protection
- LinkedIn hackathon win post drafted (held pending Bakame clarity)
- Foundational Courses Plan created (67.5KB, comprehensive)

## Phase 5: Lesson Script Marathon (Feb 27-Mar 5, 2026)
- Wrote 240+ voice lesson scripts across 9 modules:
  - Literacy Phase 1: 5 modules (Phonemic Awareness, Vocabulary, Listening Comprehension, Oral English, Advanced Sound Manipulation)
  - Numeracy: 4 modules (Number Sense/Counting, Addition, Subtraction, Multiplication)
  - 2 diagnostic assessments (literacy + numeracy)
- Reformulated documents to remove Cambridge/Bakame references, replace with Sabi branding

## Phase 6: Self-Hosted Infrastructure (Mar 7-13, 2026)
- **Mar 7-9**: Designed self-hosted architecture — no Rasa (too expensive), use lightweight script engine + Ollama
- Ordered Hetzner GEX44 GPU server (RTX 4000 Ada, 20GB VRAM)
- **Mar 10**: Sabi GPU server deployed — https://sabi.eduforequality.org live with Whisper + Claude Haiku + YarnGPT + Ollama
- **Mar 10**: UNICEF Venture Fund application submitted ($100K equity-free crypto)
- **Mar 13**: Chatterbox Turbo deployed — emotion-aware TTS with Naomi's own voice (zero-shot cloned from 29s recording), replaced Afro-TTS
- Nigerian English prompt bias added to Whisper STT
- Bukola voice from ElevenLabs also deployed, then replaced by Chatterbox

## Phase 7: Copyright & Legal (Mar 11, 2026)
- Created SABI_COPYRIGHT_BRIEF.md for Nigerian Copyright Commission
- Trimmed to protect IP (removed tech stack details, adaptive logic specifics)
- Explored trademark options: Nigeria (NGN 50K-100K / ~$30-65) vs USPTO ($250-350)
- Recommended path: EIN (free) + CT incorporation ($50-75) + 501(c)(3) ($275) + Nigeria trademark ($30-65) = ~$355-415

## Phase 8: Ongoing (Mar 2026)
- CcHub/Mastercard EdTech Fellowship application due March 30, 2026 ($100K equity-free)
- Voice panel on web demo upgraded to Groq Whisper (server-side)
- Navbar Sabi link updated to point to /sabi-voice
- Recruiting CMO at Wesleyan (poster to be put up)

## Future Planned
- **Q2-Q3 2026**: Grades 5-9 curriculum expansion, remaining lesson scripts (Literacy Phase 2, Numeracy Modules 5-6)
- **Q4 2026**: Lagos pilot — 100-500 students, pre/post assessments
- **2027+**: Government partnership (Lagos State, UNICEF), national scale to 100K+ learners