---
name: Voice Email standalone app
description: The hands-free voice-driven email triage app — separate from cortex-web, lives at /Users/naomiivie/cortex/voice-email
type: project
sessions: [7e45b89a-bcd4-4187-bdc7-954593f71707]
originSessionId: 7e45b89a-bcd4-4187-bdc7-954593f71707
---
## Location & how to run

- **Path:** `/Users/naomiivie/cortex/voice-email/`
- **Dev:** `npm run dev` → http://localhost:3001 (cortex-web stays on 3000)
- **Stack:** Next.js 16 + React 19 + Tailwind v4. Same versions as cortex-web.

## Why it exists (Naomi's vision)

Built per Naomi's RAW_TRANSCRIPTION_NOTES.md: "small face / small hole / jet black / one email at a time / non-anxiety-inducing / app talks to me, I talk back." She explicitly asked for it as a **separate standalone app**, not a route inside cortex-web. The existing `/email` page in cortex-web stays as the text-mode fallback (her call: "keep that").

## Architecture decisions

- **STT/TTS:** Web Speech API. Zero new credentials. Naomi said "doesn't need more permissions for it to be working." Apple's on-device neural voices via Chrome on macOS sound natural — the research agent confirmed this is good enough for MVP. Upgrade path is OpenAI Realtime API if Naomi wants studio quality later.
- **LLM:** Claude Haiku for everything (summarize, intent classify, draft). Same `ANTHROPIC_API_KEY` as cortex-web.
- **Data:** Reads from cortex-web's `cortex_documents` table — no separate sync. Sending uses tokens in `cortex_integrations`.
- **No DB migrations** — strictly read/write existing cortex tables. Same Supabase project.
- **Auth:** Same Clerk dev instance. User signs in once per port (cookies are per-port for security).

## Voice loop (implemented)

1. `/api/queue` → filter promotions/social/forums/updates, drop replied threads
2. `/api/summarize` → Haiku one-sentence summary read by browser TTS
3. User push-to-talk → `/api/intent` (stage=after_summary) → reply | skip | archive | repeat | send
4. `/api/draft` → uses recipient-matched past sent emails + profile_text (no embeddings)
5. After draft: `/api/intent` (stage=after_draft) → send | redraft | skip | repeat
6. `/api/send` (Gmail API) or `/api/archive` (remove INBOX label)
7. Auto-advance to next email

## Deferred (Naomi's words: "see how the experience feels")

- Per-user LoRA in the drafting step — currently base Haiku + few-shot. Naomi said: "I might change some stuff at the end maybe see if we'll do a per-user LoRA based on how the experience feels but carry on."
- OpenAI Realtime API upgrade (would replace Web Speech for production polish)
- Multi-account selection on send (currently picks most-recent active Gmail integration)
- Mobile / native — currently desktop Chrome only
- Vercel deploy
- Wake-word ("hey cortex") — research said push-to-talk is the right MVP pattern

## Files worth knowing about

- `app/voice-email-client.tsx` — the whole voice loop state machine
- `components/use-voice.ts` — Web Speech API wrapper hook
- `components/orb.tsx` — the "small face" — pulses based on speaking/listening/thinking
- `lib/ai/summarize.ts` — Haiku prompt for the calm one-line read
- `lib/ai/intent.ts` — Haiku JSON intent classifier (reply/skip/archive/send/redraft/repeat/unclear)
- `lib/ai/email-drafter.ts` — recipient-matched past emails + profile, NO embeddings (faster than cortex-web's drafter)
- `lib/integrations/gmail-token.ts` — central "give me a fresh access token" helper that handles refresh

## 2026-07-01 Production Hardening

- Sage/voice-email production hardening shipped in commit `d789d10` (`Harden Sage Mail production readiness`): sends/archives/session actions now persist assistant memory and follow-up state, cron routes require shared cron auth for scheduled work, `/api/health/readiness` reports production env/token/Supabase/LoRA-serving health, and the personal draft model now tries LoRAX first then RunPod `RUNPOD_LORA_INFERENCE_ENDPOINT_ID` with the same deployed Cortex adapter path and sanitizer pattern. Vercel Production for `email-app` now has `RUNPOD_API_KEY` as sensitive plus `RUNPOD_LORA_INFERENCE_ENDPOINT_ID=hhsl3wgl1unt7d`; deployment `dpl_9Sk6v39zVSHzzVXbUP9zCiyZvZPV` / `https://email-n2okpbyhf-naomi-ivies-projects.vercel.app` is aliased to `https://voice-email-app.vercel.app`, and live `/api/health/readiness` returned `status:"ok"` with `lora-serving-backend` ok. Root `npm run check:production-smoke` returned ok for both `cortex-web` and `voice-email`; root `npm run audit:production` returned status ok with only non-blocking env-sensitivity/development-env warnings. - 019f1ed5-4699-7bb3-861a-5e9b19ddbd8d
- Sage guardrails were tightened in commit `a8778c1` (`Add Sage launch readiness guardrails`): the streaming assistant prompt and the Claude tool-agent prompt now require explicit user approval before `send` and explicit user request before `archive`; the archive tool no longer allows judgment-based archival for "clearly not worth keeping" messages. Added `npm run check:launch` in `voice-email`, which verifies 42 launch invariants covering review-first send, explicit-only archive, pending draft approval, untrusted tool outputs, cron auth, readiness, RunPod LoRA inference, and env docs. Verification passed: `npm run check:launch` (`42 ok / 0 fail`), `npx tsc --noEmit`, `git diff --check`, `npm run build`, live readiness `status:"ok"`, root `npm run check:production-smoke` ok for both apps, and root `npm run audit:production` ok with only pre-existing env hygiene warnings. Deployed as `dpl_6NQaSZ2bAxcPUkjyff9XkmXvyCTB` / `https://email-l75y8qbxr-naomi-ivies-projects.vercel.app`, aliased to `https://voice-email-app.vercel.app`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- Sage anonymous API gates were hardened in commit `a7bab68` (`Harden Sage Mail anonymous API gates`): `getUserId()` now throws a typed `UnauthorizedError`, all protected Sage API routes return explicit 401 when middleware does not privacy-shield them, and `npm run check:production-smoke` verifies the signed-out app shell, readiness, cron auth, and anonymous rejection for send/archive/draft/queue/assistant/digest routes. Verification passed: `npm run check:launch` (`62 ok / 0 fail`), `npx tsc --noEmit`, `git diff --check`, `npm run build`, Sage `npm run check:production-smoke` (`18 ok / 0 fail`), root `npm run check:production-smoke` ok for Cortex web and Sage Mail, and root `npm run audit:production` ok with no blockers. Deployed as `dpl_CqY9PYQhoFqCVt9PeGGve8CfSzRs` / `https://email-or6wet7me-naomi-ivies-projects.vercel.app`, aliased to `https://voice-email-app.vercel.app`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
