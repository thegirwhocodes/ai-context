---
name: Cortex tech stack and infrastructure
description: Next.js, Supabase, Clerk, Claude API, LoRA pipeline, Vercel — full technical details
type: project
sessions: [0d91dd3c-6d8d-4983-b72b-a1df57377021]
---

## Working Directories

- **Web app:** /Users/naomiivie/cortex-web/
- **Docs & plans:** /Users/naomiivie/cortex/ (CORTEX_FULL_PLAN.md, PERSONAL_LLM_RESEARCH.md, RAW_TRANSCRIPTION_NOTES.md, BUSINESS_PLANS.md)

## Core Stack

- **Framework:** Next.js 15 + TypeScript + Tailwind v4
- **Auth:** Clerk (keyless mode claimed, proxy.ts middleware, `<Show>` components — NOT `<SignedIn>`/`<SignedOut>`)
- **Database:** Supabase PostgreSQL + pgvector (384-dim vectors, IVFFlat index, 12 tables, RLS on all)
- **AI:** Claude API (Haiku for chat/queries, Sonnet for profile building/deep analysis)
- **Embeddings:** all-MiniLM-L6-v2 via @xenova/transformers (runs on CPU)
- **Deployment:** Vercel (free tier), vercel.json with 5 cron jobs
- **Encryption:** AES-256 for OAuth tokens

## Database Tables (12)

cortex_users, cortex_integrations, cortex_documents, cortex_profiles, cortex_memory, cortex_actions, cortex_spheres, cortex_open_loops, cortex_lora_adapters, cortex_training_data, cortex_conversations, cortex_messages

All have RLS enabled. GDPR deletion function wipes all user data. Service role key bypasses RLS.

## LoRA Pipeline

- **Base model:** Qwen3-4B (best quality per research)
- **Training infra:** RunPod cloud GPU initially ($0.22-$1.44/user), dedicated Hetzner server at 200+ users (~$180/mo flat)
- **Serving:** LoRAX — serves thousands of per-user LoRA adapters on a single GPU, sub-2-second latency
- **Adapter size:** ~16-20 MB per user (NOT a separate model per person)
- **Re-fine-tune cycle:** Monthly cron job, or threshold-based (500 new data points), or user-initiated
- **Data formatter:** Converts emails/messages into training examples (instruction/input/output format)
- **Router:** Routes queries to personal LoRA when available, falls back to Claude

## Integrations Built

- **Gmail:** OAuth connect, fetch (with 2-year default limit), send, body extraction, sync endpoint. Labels used for basic filtering (skip PROMOTIONS/FORUMS/SOCIAL).
- **Google Calendar:** Adapter built, connect/callback/sync routes built. Not yet connected in UI.

## Ingestion Pipeline

- Chunker: splits content into embeddable chunks
- Pipeline: 5x parallel processing, junk filtering (skip very short emails), dedup by content hash
- Embeddings generated via transformers.js on CPU (~100-200ms each)

## Cron Jobs (vercel.json)

1. sync-all — syncs all integrations every 15 min
2. daily-briefing — generates daily briefing
3. weekly-profile — rebuilds user profiles
4. memory-maintenance — cleans expired memories
5. monthly-retrain — triggers LoRA re-fine-tune

## Implementation Notes (2026-06-15)

- voice-email is currently the most developed day-to-day Cortex slice: it preloads a session bundle, streams low-latency voice turns, classifies Naomi's email tiers, uses follow-up loops, and now persists send/archive/skip/wrap outcomes back into memory/open loops - codex-2026-06-15
- cortex-web remains the broader Cortex shell with RAG, profile, spheres, integrations, actions, and LoRA infrastructure; LoRA export is now inspectable through `/api/lora/export` and downloadable with `?format=jsonl` - codex-2026-06-15
- Current local recovery reality: `.Codex-sessions/` was not present; historical context is in `/Users/naomiivie/cortex/.claude-sessions/`, `/Users/naomiivie/.claude-sessions/`, and `~/.claude/projects/-Users-naomiivie-cortex/` - codex-2026-06-15
- Plan My Day implementation lives in `cortex-web/lib/ai/day-planner.ts` with API route `/api/day-plan`; it combines profile, calendar events, open loops, recent email heads, and memory into structured JSON for UI/voice reuse - codex-2026-06-15
- GroupMe import is available at `cortex-web/app/api/integrations/groupme/import/route.ts`; it expects an authenticated request with a GroupMe access token, encrypts the token, fetches groups/messages, and ingests messages as `dm_sent`/`dm_received` - codex-2026-06-15
- iMessage is intentionally local-first: `cortex-web/scripts/export-imessage.mjs` copies `~/Library/Messages/chat.db` to `/tmp`, queries with `/usr/bin/sqlite3`, and writes JSONL RawItem-shaped records for later ingestion - codex-2026-06-15
- Local/exported data can now be imported through `cortex-web/app/api/integrations/local/import/route.ts`, which accepts authenticated JSON bodies with `source` (`imessage`, `apple_notes`, or `whatsapp`) and either `items` or `jsonl`, caps requests at 500 items, and calls `ingestItems` - codex-2026-06-15
- Cron authorization helper lives at `cortex-web/lib/auth/cron.ts` and `voice-email/lib/auth/cron.ts`; production deployments should set `CRON_SECRET` and Vercel cron should send `Authorization: Bearer <CRON_SECRET>` - codex-2026-06-15
- Readiness checks live in `cortex-web/lib/config/readiness.ts` and are exposed publicly at `/api/health/readiness`; `proxy.ts` explicitly allows `/api/health(.*)` so monitoring does not require Clerk auth - codex-2026-06-15
- voice-email now mirrors cortex-web readiness through `voice-email/lib/config/readiness.ts` and `/api/health/readiness`; `voice-email/proxy.ts` also allows `/api/health(.*)` publicly - codex-2026-06-15
- Deployment runbook lives at `/Users/naomiivie/cortex/DEPLOYMENT_RUNBOOK.md`; use it as the authoritative external-service checklist before claiming production readiness - codex-2026-06-15
- Root operational scripts live in `/Users/naomiivie/cortex/package.json` and `/Users/naomiivie/cortex/scripts/`: `check-readiness.mjs` parses local env files and optionally checks local health endpoints; `verify-schema.mjs` uses Supabase REST with the service key to verify required tables/columns after migrations - codex-2026-06-15
- LoRA training-data evaluation now lives in `cortex-web/lib/lora/eval-harness.ts` and is exposed through authenticated `GET /api/lora/eval`; it reuses the formatter, reports aggregate quality/style/readiness metrics, and only returns truncated redacted examples when `include_examples=1` is requested - codex-2026-06-15
- LoRA training submission in `cortex-web/lib/lora/training-client.ts` now uses `evaluateTrainingExamples` before creating adapter jobs; RunPod submission requires `NEXT_PUBLIC_APP_URL`, and production requires `LORA_WEBHOOK_SECRET` so webhook callbacks can be authenticated - codex-2026-06-15
- The RunPod callback endpoint `cortex-web/app/api/lora/webhook/route.ts` accepts the shared secret via bearer auth, `x-lora-webhook-secret`, or `?secret=...`; no secret is required only outside Vercel production for local/dev testing - codex-2026-06-15
- Production aliases as of 2026-06-15 are `https://cortex-web-one.vercel.app` for cortex-web and `https://voice-email-app.vercel.app` for voice-email; Vercel Hobby cron limits force `sync-all` to daily unless the project upgrades or uses an external scheduler - codex-2026-06-15
- Cron route convention: every route under `cortex-web/app/api/cron/*` and `voice-email/app/api/cron/*` exports both `GET` and `POST` through one shared handler because Vercel cron invokes `GET`, while manual operator triggers use authenticated `POST` - codex-2026-06-15
- Clerk user-sync webhook at `cortex-web/app/api/webhooks/clerk/route.ts` now verifies Svix/Clerk signatures with `CLERK_WEBHOOK_SECRET` before handling `user.created`, `user.updated`, or `user.deleted`; configure the secret from the Clerk dashboard before expecting webhook delivery to succeed - codex-2026-06-15
- Migration order is now `001_initial_schema.sql`, `002_multi_account.sql`, then `003_integration_account_keys.sql`; OAuth callbacks must always write a non-null `provider_user_id` because the active integration uniqueness model is `(user_id, provider, provider_user_id)` - codex-2026-06-15
- Migration order now also includes `004_action_archive_type.sql`; `cortex_actions.action_type` includes `archive_email` so voice-email archives are audited distinctly from sent emails - codex-2026-06-15
- Migration order now also includes `005_lora_adapter_versions.sql`; `cortex_lora_adapters.adapter_version` is non-null and unique per user, and `cortex-web/lib/lora/training-client.ts` allocates the next version before adapter creation so status/inference sorting by version is meaningful across retrains - codex-2026-06-15
- Root operational scripts now include `npm run check:vercel-env`, backed by `/Users/naomiivie/cortex/scripts/check-vercel-env.mjs`; it compares required/recommended production and development env names for linked Vercel projects without exposing values, complementing local `check:readiness` - codex-2026-06-15
- Root operational scripts now include `npm run check:production-smoke`, backed by `/Users/naomiivie/cortex/scripts/check-production-smoke.mjs`; it is a no-secret deployed smoke gate for app shell availability, readiness JSON, cron auth, LoRA webhook auth, and Clerk webhook signature rejection - codex-2026-06-15
- Root operational scripts now include `npm run check:migrations`, backed by `/Users/naomiivie/cortex/scripts/check-migrations.mjs`; it statically verifies schema migration invariants before a live Supabase project is reachable - codex-2026-06-15
- Root operational scripts now include `npm run audit:production`, backed by `/Users/naomiivie/cortex/scripts/audit-production.mjs`; it runs migration, Vercel env, deployed smoke, and live schema gates together, exits nonzero until production blockers are gone, and keeps sensitive-storage warnings separate from blockers - codex-2026-06-15
- Root operational scripts now include `npm run db:migrations`, backed by `/Users/naomiivie/cortex/scripts/supabase-migrations.mjs`; it lists the canonical migration order, bundles migrations into one SQL file, or applies the bundle with `psql` using `SUPABASE_DB_URL`/`DATABASE_URL` without logging secrets - codex-2026-06-15
- LoRA adapter object cleanup now lives in `/Users/naomiivie/cortex/cortex-web/lib/lora/adapter-storage.ts`; `/api/user/delete` and Clerk `user.deleted` cleanup use it before the database delete RPC, it supports Supabase Storage URLs plus `s3://`/S3-compatible paths, and readiness/Vercel env audits include `S3_BUCKET`, `S3_REGION`, `S3_ACCESS_KEY`, and `S3_SECRET_KEY` for full LoRA production readiness - codex-2026-06-15
- The RunPod LoRA worker contract is now explicit: `cortex-web/lib/lora/training-client.ts` sends `adapter_output` with a deterministic S3 URI, `cortex-web/app/api/lora/webhook/route.ts` validates the completed `adapter_path` against that user/version target, and `DEPLOYMENT_RUNBOOK.md` documents the payload shape - codex-2026-06-15
- RunPod worker scaffold lives at `/Users/naomiivie/cortex/runpod-lora-worker/`; it follows RunPod's `runpod.serverless.start({"handler": handler})` pattern, uses Transformers/PEFT/bitsandbytes for QLoRA, uploads a single `adapter.tar.gz` object with boto3, and keeps S3 credentials in worker env rather than Cortex job payloads - codex-2026-06-15
- Billing code lives in `/Users/naomiivie/cortex/cortex-web/lib/billing/stripe.ts` plus `/api/billing/status`, `/api/billing/checkout`, `/api/billing/portal`, and `/api/webhooks/stripe`; `cortex_users` now stores Stripe customer/subscription metadata through migration `006_billing.sql`, and deletion paths cancel active Stripe subscriptions before removing user data - codex-2026-06-15
- Data-export import scripts live at `/Users/naomiivie/cortex/cortex-web/scripts/export-whatsapp-chat.mjs` and `/Users/naomiivie/cortex/cortex-web/scripts/export-instagram-data.mjs`; they emit RawItem JSONL for `whatsapp`/`instagram` with `dm_sent`/`dm_received` content types, and `/Users/naomiivie/cortex/cortex-web/app/(dashboard)/integrations/page.tsx` can upload those JSONL files through `/api/integrations/local/import` - codex-2026-06-15
- Apple Notes file import is implemented by `/Users/naomiivie/cortex/cortex-web/scripts/export-apple-notes.mjs`; it reads local text/Markdown/HTML note exports, normalizes HTML, emits `apple_notes` RawItems with `note` content type, and feeds the same `/api/integrations/local/import` JSONL path - codex-2026-06-15
- Chat action detection lives in `/Users/naomiivie/cortex/cortex-web/lib/ai/action-detector.ts` and runs after `/api/chat` streams; it queues only high-confidence explicit email/calendar requests into `cortex_actions`, while `/api/actions/[id]/approve` executes Gmail or Google Calendar through their adapters after user approval - codex-2026-06-15
- User data export lives at `/Users/naomiivie/cortex/cortex-web/app/api/user/export/route.ts`; it returns `cortex-user-export-v1` JSON for the authenticated user, excludes OAuth token ciphertext and embeddings, and is wired to the Settings page download control - codex-2026-06-15
- Production smoke coverage in `/Users/naomiivie/cortex/scripts/check-production-smoke.mjs` now treats Clerk/Vercel unauthenticated `401` or privacy-preserving `404` as acceptable for private action, billing, user export, and user deletion routes - codex-2026-06-15
- Main cortex-web personal-model wiring is in `/Users/naomiivie/cortex/cortex-web/lib/lora/router.ts`; `/api/chat` calls `tryPersonalRouteQuery` before Claude streaming, and `lib/ai/query-engine.ts` calls `routeQuery`, so deployed LoRA adapters can serve style/routine requests once LoRAX envs and an adapter exist - codex-2026-06-15
- Plan My Day note resurfacing lives in `/Users/naomiivie/cortex/cortex-web/lib/ai/day-planner.ts`; it loads `content_type = note` document heads and passes them as untrusted note/idea context so Apple Notes and other local imports can influence the day plan without becoming obligations by default - codex-2026-06-15
- Live schema verification in `/Users/naomiivie/cortex/scripts/verify-schema.mjs` now queries all 12 core tables, including `cortex_profiles` and `cortex_spheres`, via Supabase REST with the service role key - codex-2026-06-15

## External Services Configured

- Supabase project: addkjndgmbxiulpquizn.supabase.co
- Clerk: claimed, Google OAuth enabled
- Google Cloud Console: Gmail API + Calendar API enabled, OAuth consent screen set to External/Testing
- Anthropic API key: configured in .env.local

## Design System

- Jet black (#000000 / #0A0A0D background)
- Inter font
- Minimal, non-anxiety-inducing
- One thing at a time approach
- Purple accent (#8B5CF6) for spheres
- Daily briefing is now a deterministic rendering of `generateDayPlan`, so dashboard, `/api/day-plan`, cron briefing, and `/api/briefing` use the same calendar/email/open-loop/memory/note context instead of divergent planner logic - codex-2026-06-15
- Developer API uses `cortex_api_keys` with `key_hash` only, `ctx_live_` raw keys shown once, `query:read` scopes, `/api/v1/query` marked public in middleware but authenticated inside the route with Bearer API keys before calling `queryEngine` - codex-2026-06-15
