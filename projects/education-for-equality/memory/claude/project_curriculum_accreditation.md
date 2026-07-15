---
name: project-curriculum-accreditation
description: "What international seal/accreditation E4E can legitimately put on its curriculum (and why \"Cambridge-accredited\" is impossible)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5335de07-9464-40e1-812e-565cd4926043
---

E4E wants an internationally recognized "stamp" for its curriculum (Naomi's framing: something like "Cambridge accredited curriculum"). Deep research (session 5335de07, 2026-06-05; full report in agent-research/5335de07-946_01_Research_international_curriculum_accreditation_bodies.txt) confirmed the prior May 2026 finding:

**No international body will accredit a SELF-AUTHORED curriculum.** Cambridge International, Cognia, CIS, ASIC, IB etc. accredit WHOLE SCHOOLS/INSTITUTIONS, not standalone third-party curricula. Cambridge's only third-party route ("Endorsed resources") is for recognised publishers teaching Cambridge's OWN syllabus.

- The ONLY honest Cambridge claim for our self-authored Grade 4 curriculum = **"aligned to Cambridge standards"**, NEVER "accredited". - 5335de07
- Best attainable real seal NOW: **EduEvidence / ICEIE** (eduevidence.org) — certifies evidence-of-impact of the tech PRODUCT (Sabi or web app), ~$250 + free registration, 5-7 business days. Claim: "EduEvidence-certified EdTech." Awardees incl. Kahoot!, Age of Learning. - 5335de07
- **NCFE** (UK Ofqual awarding body) can give awarding-body recognition to self-authored content (Customised Qualifications / Endorsed Programmes) — real but more effort. - 5335de07
- **Assured by Pearson** (ex-Pearson Assured) — org QA seal, but requires 18 MONTHS prior delivery (blocked until after the pilot) and contractually BANS the word "accredited". Post-2027 option. - 5335de07
- AVOID **ASIC** — issues a badge but has diploma-mill criticism, not CHEA/US-DoE recognised; could hurt credibility with funders. - 5335de07
- Real credibility lever is pilot data (0.30 SD TaRL) + named expert/UBEC sign-off, not a purchasable badge — ties to the [[project_e4e_status]] external-validator step in the 6-month plan.

Open gaps still unverified: IB, WASC, COBIS, Oxford AQA, ISO 21001, EdReports, UNESCO/UNICEF, AU/ADEA.

## Curriculum Validation / Standards Registry — 2026-06-15

- Restored `curriculum-app` from `~/.Trash/curriculum-app` to `/Users/naomiivie/Education for Equality/curriculum-app`; repo is on `main` with remote `https://github.com/thegirwhocodes/Education-for-Equality.git`. - 510de61
- Created Week 1 external validation packet at `/Users/naomiivie/Education for Equality/2. The Solution/SABI_VALIDATION_WEEK1_PACKET.md`, covering all 64 existing numeracy voice lessons, planned Division and Word Problems modules, Phase 1 literacy registry, lesson quality rubric, 10 review samples, and reviewer feedback form. - 510de61
- Added machine-readable standards registry files in `curriculum-app/lib/standards/`: complete existing numeracy lesson crosswalk in `foundational-numeracy-crosswalk.ts`, new literacy references in `literacy-frameworks.ts`, new Phase 1 literacy crosswalk in `foundational-literacy-crosswalk.ts`, and exports via `index.ts`; current claim boundary remains `working_crosswalk`, not official NERDC/Cambridge approval. - 510de61
- Tightened the standards registry after review: added optional `code`, `sourceUrl`, and `reviewNotes` to standard refs; added exact verified Cambridge Primary Mathematics 0096 and English 0058 Stage 4 objective refs where source text was checked; expanded literacy from review samples to all 80 Phase 1 lesson entries; added restored app Module 5/6 numeracy lessons to the crosswalk; fixed diagnostic routing so multiplication mastery routes to Division before Word Problems; removed bracketed performance tags from diagnostic scripts. - codex-20260615
- Finished cleanup artifacts after handoff: exported structured diagnostic blueprints, added `review-queue.ts` with exact NERDC row verification, Grade 4 Cambridge audit, GPF descriptor selection, Module 5/6 source-of-truth, Phase 2 print bridge, and performance-tag migration items; created `SABI_VOICE_PERFORMANCE_TAG_CLEANUP_PLAN.md`; updated validation docs and standards README; `npx tsc --noEmit` and targeted ESLint passed; remaining bracketed affect tag inventory is 1068 outside diagnostics. - 019eadb0/codex-20260615
