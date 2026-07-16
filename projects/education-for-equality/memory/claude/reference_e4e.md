---
name: e4e-reference-ips-urls-contacts-grants
description: "Quick-reference for server IPs, grant links, contact names, key URLs, and file paths"
metadata:
  node_type: memory
  type: reference
  sessions:
    - ff1faa52
    - f19ca767
    - efd7d7d2
    - 7464be26
    - 296c88b8
    - d72670bf
    - 1f61b0ac
    - 089265f6
    - 1b27663d
    - 262aa5fe
  originSessionId: c46a7821-57d5-46ff-9dac-304ed0ef2cbc
---

# E4E Quick Reference

## URLs
- **Curriculum App**: https://curriculum-app-eta.vercel.app (also https://eduforequality.org)
- **Sabi Frontend**: https://sabi.eduforequality.org (Vercel, voice demo + landing page)
- **Sabi API Backend**: https://api.eduforequality.org (Hetzner GPU server, FastAPI + Chatterbox TTS)
- **Sabi Voice Demo**: https://sabi.eduforequality.org/sabi-voice (or via key-gated access)
- **Domain registrar**: Cloudflare DNS, $7.50/year

## ElevenLabs Conversational AI (phone / ConvAI dashboard)
- **Agent id**: `agent_5701kp7djbvreqk9cb3mf4g55n09` (dashboard name: Education for Equality) — 1b27663d
- **Twilio native integration — voice URL** (what Twilio “A call comes in” shows when routed through ElevenLabs US ingress): `https://api.us.elevenlabs.io/twilio/inbound_call` — 262aa5fe
- **Custom LLM** (when not using EL built-in model): `https://eduforequality.org/api/sabi/voice/llm` (OpenAI-compatible; see `curriculum-app/app/api/sabi/voice/llm/route.ts`)
- **Agent prompt + ops table**: `curriculum-app/docs/elevenlabs-agent-prompt.md`
- **Env for embed/widget**: `NEXT_PUBLIC_ELEVENLABS_CONVAI_AGENT_ID` in `curriculum-app/.env.local.example`

## Server
- **Hetzner GPU IP**: 136.243.8.51
- **SSH**: `ssh root@136.243.8.51` (key-only, no password from Naomi's Mac)
- **Code on server**: `/opt/sabi/sabi-server/`
- **Env file**: `/opt/sabi/sabi-server/.env`
- **Restart**: `ssh root@136.243.8.51 'cd /opt/sabi/sabi-server && docker compose restart'`
- **Logs**: `ssh root@136.243.8.51 'cd /opt/sabi/sabi-server && docker compose logs -f sabi'`
- **SSL expires**: June 8, 2026 (auto-renews via certbot)
- **Cost**: ~EUR 184/month + EUR 264 one-time

## GitHub Repos (Private)
- **Curriculum App**: `thegirwhocodes/curriculum-app` (deployed to Vercel)
- **Sabi Server**: `thegirwhocodes/sabi-server` (deployed to Hetzner)
- **UNICEF access**: @unicefinnovation added as read-only collaborator

## Team & Contacts
- **Naomi Ivie** — Founder & Product Lead (nivie@wesleyan.edu, Wesleyan University)
- **Dr. Sonia Ivie** — Education Advisor, mother. 20+ years experience, EKOEXCEL/NewGlobe, 1,016 schools, 500K pupils. Lagos special schools researcher.
- **Joshua Ivie** — Technical Advisor. Head of Innovation at Bluechip Technologies (400+ employees, 9 countries).
- **Richard Ivie** — Governance Advisor. Executive Director at Corruption Observatory, ISO governance expert.
- **MIT Hackathon Team**: Grace (7yr telecom), Nali (Textiles Advancing Impact)
- **Chris Folayan** — Luma Learn founder, advisor (Luma = 501(c)(3) nonprofit for mobile learning in Africa)
- **Nelly** — TAI for Education founder (10K+ students)
- **Hakeemah** — Branding, Neon Nexus founder
- **Happy Niyorurema** — Bakame AI co-founder, Rwanda (no longer partner)
- **Jaara/Diarra Niang** — Bakame AI co-founder, Senegal (no longer partner)

## Funding & Applications
| Application | Status | Amount | Date |
|---|---|---|---|
| MIT Africa Business Challenge | **WON 2nd place** | $3,000 | Feb 28, 2026 |
| Wesleyan University grant | **Received** | $1,200 | ~Feb 2026 |
| Technovation AI Ventures 2026 | Submitted | $10K equity-free | Mar 4, 2026 |
| Harvard Innovation Labs Leadership | Applied | (experience) | Feb 18, 2026 |
| UNICEF Venture Fund | Submitted | $100K equity-free crypto | Mar 10, 2026 |
| CcHub/Mastercard EdTech Fellowship | **Due Mar 30, 2026** | $100K equity-free | Pending |
| See `GRANT_FUNDING_RESEARCH.md` for comprehensive funding landscape | | | |

## Key Project Files
| File | Description |
|---|---|
| `FOUNDATIONAL_COURSES_PLAN.md` | Voice courses plan (67.5KB, comprehensive) |
| `SABI_VOICE_LESSON_DESIGN.md` | 4 worked lesson examples |
| `SABI_HARD_QUESTIONS.md` | 25 Q&A on feasibility/impact |
| `SABI_SLIDE_DECK.md` | MIT ABC pitch deck (14 slides) |
| `FEATURE_PHONE_AI_DELIVERY_RESEARCH.md` | Deep technical research (55KB) |
| `SABI_INFRASTRUCTURE_RESEARCH.md` | Comprehensive reference (TTS, STT, LLM, telephony, all sources) |
| `Cost Breakdown.md` | All cost calculations |
| `BAKAME_AI_DUE_DILIGENCE_MEMO.md` | Legal due diligence on Bakame + Statement of Originality |
| `AT Partnership Email.md` | Draft pitch to Africa's Talking |
| `LEGAL_ROADMAP.md` | US 501(c)(3) + Nigerian CAC plan |
| `Implementation Plan for Claude.md` | Sabi server deployment (Hetzner) |
| `SABI_COPYRIGHT_BRIEF.md` | For Nigerian Copyright Commission |
| `UNICEF_APPLICATION_ANSWERS.md` | UNICEF Venture Fund responses |
| `TECHNOVATION_APPLICATION.md` | Technovation AI Ventures application |
| `Research Brief.md` / `Lagos Feasibility Assessment.md` / `Market Analysis and Impact Case.md` | Research documents |
| `lesson-scripts/` | Voice lesson scripts (literacy + numeracy + diagnostics) |
| `sabi-server/` | FastAPI backend (main.py, llm.py, voice.py, memory.py, Docker) |
| `On the Ground Research/` | NALABE assessments, EKOEXCEL reports, Dr. Sonia Ivie's Lagos research |
| `GRANT_FUNDING_RESEARCH.md` | Comprehensive funding landscape |
| `AT_ALTERNATIVES_RESEARCH.md` | Africa's Talking alternatives analysis |

## Hiring Plans
- **Chief CMO (Wesleyan student)**: Instagram + YouTube content. Naomi to put up poster at Wesleyan to recruit.

## Legal Structure (Planned)
1. **Phase 1**: Connecticut 501(c)(3) nonprofit — ~$325-350 (EIN free + CT $50-75 + 501(c)(3) $275)
2. **Phase 2**: Nigerian Incorporated Trustee via CAC — ~$75-130
3. **Phase 3** (if monetizing): Nigerian Ltd for private school sales
4. **Phase 4** (if VC): Delaware C-Corp
5. **Trademark**: Nigeria first (~$30-65), US later ($250-350)