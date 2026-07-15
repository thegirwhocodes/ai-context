---
name: Education for Equality — Vision & Architecture
description: Mission, two-channel model, target audience, core insight, and pedagogical philosophy
type: project
sessions: [ff1faa52, f19ca767, efd7d7d2, 7464be26, 296c88b8, d72670bf, 089265f6]
---

# Education for Equality — Vision & Architecture

## Mission
Free, world-class education for every child in Nigeria/Africa via technology. Targeting 20M+ out-of-school children in Nigeria (highest globally). 70% of 10-year-olds cannot read a simple sentence.

## Core Insight
95% phone ownership + 99% 2G coverage in Nigeria = voice calls reach everyone. No smartphone, no internet, no reading ability required. At $0.50-5/student/year (vs $48 for World Bank AI tutoring), Sabi is the most cost-effective education intervention ever measured (benefit-cost ratio 161-260).

## The Organization
**Education for Equality** is the organization. It delivers learning through two channels:

### Channel 1: Sabi (Voice AI — feature phone users) — PRIMARY CHANNEL
- **Sabi IS the voice delivery channel** — AI tutor via phone calls, no internet needed
- "Sabi" = "to know" in Nigerian Pidgin
- Foundational Literacy (8 modules, ~140 calls) + Foundational Numeracy (6 modules, ~100 calls)
- Target: Ages 8-14, never-readers, TaRL Level 0 to Level 3-4
- 5-7 min calls, 3-5x/week, adaptive branching, student memory per phone number
- Warm Nigerian English, patient older sibling personality

### Channel 2: Curriculum App (Web — smartphone users)
- Khan Academy-style platform — live at https://curriculum-app-eta.vercel.app
- Grade 4 complete (286+ lessons, ~47 hours: Math/English/Science/Social Studies)
- Cambridge-aligned, OER content (CC-BY), mobile-first, PWA-ready
- Code: `curriculum-app/`

### Pipeline
Child masters foundational skills via Sabi -> transitions to Curriculum App for full grade-level curriculum.

## Pedagogical Philosophy
- **TaRL** (Teaching at the Right Level): 0.10-0.71 SD improvement, proven at scale
- **"Naira-first, abstract-second"**: real market scenarios before formal math. Correct 9x citation is Weber, Bogler & Vollmer 2024, *Economics of Education Review*, North-West Nigeria (n=5,997; 48.5% market framing vs 5.4% formal school format); do not cite the Nigeria 9x stat as Nature 2025. Nature 2025 is the separate India working-children transfer-gap paper. - 019ef0d9-20cb-7eb1-b87d-6bffea0a9275
- **Adaptive**: right -> harder; wrong -> scaffold (smaller numbers, rephrase); 3+ correct -> advance module
- **Spaced repetition**: returning students get recall question from last session
- **Never says "wrong"**: always scaffolds with encouragement
- **Literacy two-phase**: Phase 1 oral-only (3 months); Phase 2 oral + print flashcards ~NGN 200-500/child
- **Numeracy**: 100% voice-teachable, Modules 0-7 (diagnostic -> word problems -> Grade 4 ready)
- Built on 7 frameworks: TaRL, Jolly Phonics, Rising On Air, Rori AI, Cambridge Primary, Global Proficiency Framework, XPRIZE winners

## Evidence Base
- World Bank RCT: AI tutoring = 1.5-2 years learning in 6 weeks ($48/student)
- Rori AI: 0.37 SD gains, WhatsApp math, $5/student/year
- ConnectEd: Phone tutoring, 0.33 SD across 6 countries
- EKOEXCEL Lagos: Non-readers 38%->12%, comprehension 21%->60%
- Jolly Phonics: 60% increase word recognition (Nigeria, 72K pupils)

## Impact Case
- Learning worth 4x more than attendance: literate child earns NGN 4.4M more lifetime than illiterate peer with same years of school
- Girls' education returns up to 10%/year — highest-ROI development intervention globally
- Nigeria loses $40B/year (~8% GDP) to under-education
- 133M Nigerians in multidimensional poverty — education deprivation is primary driver
