---
name: Cortex operator playbook
description: Concrete step-by-step instructions Naomi asked for so future Codex agents teach her exactly what to do rather than speaking abstractly
type: project
sessions: [019f1572-44cf-7e12-8e4a-ab2fd29640fb]
---

# Cortex Operator Playbook

Naomi explicitly asked that future agents teach her everything step by step: accounts to create, buttons to click, env vars to set, commands to run, and what to ask concurrent Codex/Claude agents to do. Do not say "wire up RunPod/S3/LoRAX/Vercel" without translating that into concrete steps. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

Naomi does not know how to code yet, so future agents must explicitly call out what depends on Naomi versus what an agent can do. Naomi-dependent work is usually account creation, billing/payment, OAuth consent/dashboard clicks, copying secret values, authorizing apps, and approving production changes. Agent-dependent work is code edits, terminal commands, tests, builds, migrations, docs, and smoke checks. Never hand Naomi a raw engineering task without saying whether she personally has to do it and why. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

If Naomi pastes API keys/tokens/secrets into chat, treat them as compromised and do not use them in Vercel, RunPod, Cloudflare, Docker, or local env files. Tell Naomi to revoke/rotate them, then either walk her through pasting new values directly into dashboards or have her put new values in a local private file that an agent can read without echoing. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

When using Vercel CLI with a private token, avoid commands that echo the full invocation back in pagination/help text, especially `vercel ls --token ...`; prefer `VERCEL_TOKEN="$(...)" npx vercel <command>` where supported, redirect/sanitize output for listing commands, and never paste token values into memory or final answers. - 019f174d-c012-7742-a3ea-1279f173fad2

For Composio specifically, do not treat `rpa_...` keys as Composio keys: on 2026-06-30 the supplied `rpa_...` token was rejected by Composio as invalid and appears to be RunPod-style. A real Composio `ak__...` key is now stored in `/Users/naomiivie/cortex/composio-priv.rtf`, validated with `@composio/core`, and Vercel Production has `COMPOSIO_API_KEY` plus `COMPOSIO_ENABLED=true`; the next verification is a signed-in `/integrations` Connect flow, not another env setup. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

## Current command center split

- Naomi is the operator/decision-maker. She needs exact next actions, not just architecture. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- One agent should own `voice-email` / Sage Mail stabilization because that tree is dirty and actively edited. Other agents should avoid touching it unless assigned. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- One agent should own production/Vercel/env checks. `npm run verify:schema` passed on 2026-06-29 after another agent fixed live Supabase schema drift. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- This Codex lane prepared personal-model training infrastructure: RunPod worker contract, Dockerfile, payload validator, tests, README, deployment-runbook updates, installed Docker Desktop locally, built/pushed worker images, and ultimately deployed `docker.io/nivie7/cortex-lora-worker:v0.2.0` for both training and inference on RunPod endpoint `hhsl3wgl1unt7d`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- Current personal-model state: adapter v5 is trained, uploaded to R2, marked deployed in Cortex, callable through RunPod serverless inference, and used in Cortex email drafting before Claude polish. Do not tell Naomi serving is still missing unless a fresh smoke test fails; run `npm run check:lora-serving -- 73cb5aed-9bec-4e6c-9872-5f793f8775a6` first. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

## What Naomi should do next, concretely

### 1. Stabilize Sage Mail first

Ask the agent owning Sage Mail:

> Please finish the dirty `voice-email` tree: review the uncommitted changes, run `npm --prefix voice-email run build`, run a local session if possible, verify send/archive/skip/wrap memory persistence, and tell me exactly what still fails.

Expected proof:

- `npm --prefix voice-email run build` passes. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- A real or mocked Sage Mail session can initialize a queue, draft, send/archive/skip, and persist memory/open-loop updates. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- Dirty files are either committed intentionally or listed clearly as still in-progress. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

### 2. Clear production env warnings

Ask the production/env agent:

> Please make `npm run check:launch`, `npm run redteam:guardrails`, `npm run check:energy`, `npm run check:lora-serving -- 73cb5aed-9bec-4e6c-9872-5f793f8775a6`, and `npx tsc --noEmit` as clean as possible. If a warning is intentional, explain why.

Current public production audit command:

```bash
cd /Users/naomiivie/cortex/cortex-web
npm run check:launch
```

As of commit `948eddc`, this public launch audit checks static guardrails, email-draft untrusted-context handling, Sphere Energy, live readiness, signed-out auth gates, webhook rejection, and Google callback route accessibility. It returns warn-only because `CLERK_WEBHOOK_SECRET` is still missing in Vercel Production. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

Naomi/action items in dashboards:

- In Vercel for `cortex-web`, set production envs: `NEXT_PUBLIC_APP_URL`, `CRON_SECRET`, `CLERK_WEBHOOK_SECRET`, `LORA_WEBHOOK_SECRET`, optional Stripe envs if billing is active, and later RunPod/S3/LoRAX envs when created. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- In Vercel for `voice-email`, set production `CRON_SECRET`; LoRAX envs can wait until personal-model serving exists. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- In Google Cloud Console OAuth client, make sure production redirect URIs are registered for both deployed apps if they initiate Google auth. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- In Clerk, create/configure webhook endpoint for `cortex-web` and copy the signing secret into `CLERK_WEBHOOK_SECRET`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

### 3. Create adapter storage

Naomi needs one S3-compatible bucket for LoRA adapter tarballs. Cloudflare R2 is likely easiest/cheap; AWS S3 also works.

Concrete fields Cortex needs:

```text
S3_BUCKET=
S3_REGION=
S3_ACCESS_KEY=
[REDACTED:s3-access-key]
S3_ENDPOINT= # optional; needed for R2/S3-compatible providers
```

What to do:

1. Create a bucket, e.g. `cortex-lora-adapters`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
2. Create an access key with read/write/delete permissions to that bucket. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
3. Copy bucket name, region, endpoint if provider requires it, access key, and secret. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
4. Put those values in `cortex-web` Vercel env and RunPod worker env as appropriate. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

### 4. Create/push the RunPod worker image

Naomi needs a Docker image registry: Docker Hub or GitHub Container Registry.

Current state:

- Docker Desktop was installed locally at `/Users/naomiivie/Applications/Docker.app`; use its bundled CLI or add `/Users/naomiivie/Applications/Docker.app/Contents/Resources/bin` to `PATH`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- The worker image was built and pushed to Docker Hub as `docker.io/nivie7/cortex-lora-worker:v0.1.0` on 2026-06-30, digest `sha256:a407d96c831fc68822092d7f9ba0d8697c9c24a4dddb65ec43051c03f7ffd69d`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- Future rebuild command, if code changes:

```bash
cd /Users/naomiivie/cortex/runpod-lora-worker
PATH="/Users/naomiivie/Applications/Docker.app/Contents/Resources/bin:$PATH" docker build --platform linux/amd64 \
  -t <docker-user>/cortex-lora-worker:v0.1.0 .
PATH="/Users/naomiivie/Applications/Docker.app/Contents/Resources/bin:$PATH" docker push <docker-user>/cortex-lora-worker:v0.1.0
```

### 5. Create the RunPod Serverless endpoint

Concrete steps:

1. Go to RunPod and create a Serverless endpoint from the Docker image. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
2. Pick a CUDA GPU with enough VRAM for Qwen3-4B QLoRA. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
3. Set worker env:

```text
S3_ACCESS_KEY=
[REDACTED:s3-access-key]
S3_SESSION_TOKEN= # optional
HF_TOKEN=         # optional unless the base model is gated
```

4. Copy the endpoint id. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
5. In `cortex-web` Vercel env, set:

```text
RUNPOD_API_KEY=
[REDACTED:runpod-api-key]
NEXT_PUBLIC_APP_URL=https://<cortex-web-domain>
LORA_WEBHOOK_SECRET=
[REDACTED:lora-webhook-secret]
S3_REGION=
S3_ACCESS_KEY=
[REDACTED:s3-access-key]
S3_ENDPOINT= # optional
```

### 6. Train only after data is ready

Do not spend GPU money before the data audit passes.

Concrete test sequence:

```bash
curl https://<cortex-web-domain>/api/lora/status
curl https://<cortex-web-domain>/api/lora/eval
curl "https://<cortex-web-domain>/api/lora/eval?include_examples=1&limit=25"
curl https://<cortex-web-domain>/api/lora/export
```

Only train when:

- `can_train: true`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- Examples look like received-email/thread context -> Naomi-style reply. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
- No auto-reply/unsubscribe/quoted-thread leakage. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

Then:

```bash
curl -X POST https://<cortex-web-domain>/api/lora/train
curl https://<cortex-web-domain>/api/lora/status
```

Expected status path: `formatting_data/queued/training -> deployed` after webhook completion. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

### 7. Set up adapter serving separately

RunPod training only creates the adapter. It does not automatically serve it.

Naomi needs either LoRAX, vLLM with LoRA support, or a small custom OpenAI-compatible adapter-serving service. Cortex currently expects:

```text
LORAX_API_URL=
LORAX_API_KEY=
```

Serving must accept requests with:

```json
{
  "model": "<base_model>",
  "messages": [...],
  "adapter_id": "<user-id>_v<adapter-version>",
  "adapter_source": "s3://<bucket>/users/<user-id>/lora-adapters/v<version>/adapter.tar.gz"
}
```

Before claiming personal-model readiness:

1. Start serving endpoint with same base model as training. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
2. Ensure it can fetch/cache adapter tarballs from S3/R2. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
3. Send one chat-completion request with adapter id/source. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
4. Confirm output changes from generic base-model voice and Cortex increments `inference_count`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

Current proof command after the 2026-06-30 adapter v5 training success:

```bash
cd /Users/naomiivie/cortex/cortex-web
npm run check:lora-serving
```

This now finds the latest deployed adapter automatically and returns safe diagnostics only. Earlier on 2026-06-30 it returned `missing_endpoint` when only LoRAX was supported; after RunPod inference was wired, the same smoke passed against adapter v5 through endpoint `hhsl3wgl1unt7d`. The production Settings page also exposes the same check as **Personal Model → Test Serving**. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of commit `8d2c47b`, the broader launch audit can include this proof directly:

```bash
cd /Users/naomiivie/cortex/cortex-web
RUNPOD_API_KEY="<load from secure local source>" \
RUNPOD_LORA_INFERENCE_ENDPOINT_ID="hhsl3wgl1unt7d" \
S3_REGION="auto" \
S3_ENDPOINT="<R2 endpoint>" \
CORTEX_LORA_SMOKE_USER_ID="73cb5aed-9bec-4e6c-9872-5f793f8775a6" \
npm run check:launch -- --include-slow
```

Do not print the token values. The default slow-smoke timeout is 150s and can be overridden with `CORTEX_LORA_SMOKE_TIMEOUT_MS`. Post-deploy on 2026-06-30 this returned 16 ok, 1 warn, 0 fail, with the only warning still `CLERK_WEBHOOK_SECRET`; RunPod adapter v5 responded upstream HTTP 200 in `41778ms`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

After configuring the Clerk production webhook and redeploying `dpl_3zuqJsuoS38J8FVxGEGExNLMyfKA`, canonical readiness is fully ok. Quick `npm run check:launch` still reports one warning only because it intentionally skips the deep RunPod LoRA call; the zero-warning production proof is `npm run check:launch -- --include-slow`, which returned 17 ok, 0 warn, 0 fail on 2026-06-30 with adapter v5, backend RunPod, upstream HTTP 200, and preview `The personal model endpoint is online.` - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

Clerk webhook setup is no longer a launch blocker. Vercel Production has `CLERK_WEBHOOK_SECRET`; unsigned POSTs to `https://cortex.eduforequality.org/api/webhooks/clerk` should reject with `400 Invalid webhook signature`. Do not recreate the Clerk/Svix endpoint unless Clerk delivery logs show failures or the signing secret is rotated intentionally. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of 2026-06-30, Cortex can use either LoRAX/vLLM or RunPod serverless inference, and the RunPod path is live. Endpoint `hhsl3wgl1unt7d` points to template `kzfvry1f1f`, which uses `docker.io/nivie7/cortex-lora-worker:v0.2.0` with `task: "inference"` support and R2 worker env configured. Vercel Production has `RUNPOD_LORA_INFERENCE_ENDPOINT_ID=hhsl3wgl1unt7d`, and live readiness reports `lora-serving-backend` ok - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

If the worker ever needs to be rebuilt again, use:

```bash
cd /Users/naomiivie/cortex/runpod-lora-worker
PATH="/Users/naomiivie/Applications/Docker.app/Contents/Resources/bin:$PATH" docker info
PATH="/Users/naomiivie/Applications/Docker.app/Contents/Resources/bin:$PATH" docker build --platform linux/amd64 \
  -t nivie7/cortex-lora-worker:v0.2.0 .
PATH="/Users/naomiivie/Applications/Docker.app/Contents/Resources/bin:$PATH" docker push nivie7/cortex-lora-worker:v0.2.0
```

Do not overwrite template `kzfvry1f1f` with missing env values. If creating a new RunPod serverless template, serverless templates reject `volumeInGb`; create the template without volume fields, include the worker R2 env values, then move endpoint `hhsl3wgl1unt7d` to the new template and rerun `npm run check:lora-serving -- 73cb5aed-9bec-4e6c-9872-5f793f8775a6`. The 2026-06-30 smoke passed: first cold start direct RunPod `/runsync` took ~54s, then the built-in smoke passed warm in ~1.5s - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

### 7.1. Composio Rail A state

Composio is now enabled in `cortex-web` Production. The real Composio key is stored locally in `/Users/naomiivie/cortex/composio-priv.rtf`; do not print it. Codex validated it with `@composio/core` and then set Vercel Production `COMPOSIO_API_KEY` plus `COMPOSIO_ENABLED=true`, redeploying the canonical domain `https://cortex.eduforequality.org`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

Do not reuse Naomi's `rpa_...` RunPod key as a Composio key; it is RunPod-style. The current valid Composio key is the `ak__...` value from `composio-priv.rtf`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

`/api/composio/status`, `/api/composio/connect`, and `/api/composio/tools` are Clerk-protected. A signed-out curl returning private 404 is expected. The real smoke is: sign in at `https://cortex.eduforequality.org`, open `/integrations`, and confirm the Apps section appears with Composio launch apps. Click one app's **Connect** button and verify it redirects to Composio OAuth. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

### 7.2. Sphere Energy state

Sphere Energy is live in `cortex-web` as of 2026-06-30. It is not a new external integration and does not require another OAuth app. It reads existing Cortex data: `cortex_users.timezone`, `cortex_profiles.profile_text`, ingested `calendar_event` documents, incomplete `cortex_open_loops`, and `cortex_spheres` labels/colors. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

Key files: `lib/energy/energy-model.ts`, `app/api/energy/today/route.ts`, dashboard Energy Map in `app/(dashboard)/page.tsx`, and `scripts/check-energy-model.ts`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

Verification commands:

```bash
cd /Users/naomiivie/cortex/cortex-web
npm run check:energy
npx tsc --noEmit
npm run build
npm run redteam:guardrails
```

Signed-out curl to `/api/energy/today` returns a Clerk/private 404 because the route is intentionally protected. Real smoke requires Naomi signed in at `https://cortex.eduforequality.org`; the dashboard should show **Sphere Energy** above the day plan with current energy, best focus window, calendar load, timeline bars, and open-loop suggestions. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

### 8. Final product demo sequence

Naomi should ask the team for this proof, in this order:

1. Gmail reconnects and syncs. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
2. Profile and memory rebuild from real data. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
3. Sage Mail opens a real queue. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
4. Sage Mail drafts one reply in Naomi's voice. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
5. Sage Mail can send/archive/skip/wrap and memory/open-loops update. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
6. `/api/lora/eval` confirms whether enough data exists for LoRA. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
7. If enough data exists, run first adapter training and serving smoke. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

Current state after commit `8d2c47b`: steps 1, 2, 6, and 7 have already moved past setup for Naomi's primary user; Sage Mail now has the polished review-first UI and uses the deployed personal-model drafting path, but the remaining manual demo is for Naomi to sign in at `https://cortex.eduforequality.org`, open Sage Mail, click **Sync latest** if needed, generate one reply, inspect tone, and only then choose whether to send. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of commit `a31463c`, do not reintroduce client-chosen recipients into the Sage Mail review queue. The intended contract is: `/email` sends `{emailId, body, reviewed:true}`, `/api/email-agent/send` loads the stored `email_received` source document, derives the recipient/subject/provider account server-side, requires explicit review, sanitizes headers, and logs source email/thread ids. Red-team and launch checks assert this behavior through `sage_mail_send_policy` / `sage_mail_send_guardrails`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of commit `4e63a24`, the latest zero-warning production proof is:

```bash
cd /Users/naomiivie/cortex/cortex-web
RUNPOD_API_KEY="<load from secure local source>" \
RUNPOD_LORA_INFERENCE_ENDPOINT_ID="hhsl3wgl1unt7d" \
S3_REGION="auto" \
S3_ENDPOINT="<R2 endpoint>" \
CORTEX_LORA_SMOKE_USER_ID="73cb5aed-9bec-4e6c-9872-5f793f8775a6" \
npm run check:launch -- --include-slow
```

On 2026-06-30 this returned 19 ok / 0 warn / 0 fail against `https://cortex.eduforequality.org`, including Source Health/product-contract checks, auth gates, callback-route checks, Sage Mail guardrails, and RunPod adapter v5 personal-model smoke. If a future run fails only because RunPod returns no generated text, first rerun `npm run check:lora-serving -- 73cb5aed-9bec-4e6c-9872-5f793f8775a6`; the endpoint has occasionally had cold-start/transient `/runsync` no-output behavior, but the verified healthy response is adapter v5 over endpoint `hhsl3wgl1unt7d` with preview `The personal model endpoint is online.` - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of launch hardening commit `4ad6aa3`, the same full command should return 20 ok / 0 warn / 0 fail because it now also checks live security headers on `https://cortex.eduforequality.org`. The production alias currently points to deployment `dpl_AhPz58xmg4DmFTQWeHgGQ9gmxw4a` / `https://cortex-2kq43a3x9-naomi-ivies-projects.vercel.app`; post-deploy proof on 2026-06-30 showed `live_security_headers` ok and RunPod adapter v5 deep smoke ok in `41244ms`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

Security-header policy: keep the conservative header set in `next.config.ts` unless a breaking integration is proven. It includes HSTS, `nosniff`, `strict-origin-when-cross-origin`, `camera=(), geolocation=(), microphone=(self), payment=()`, and `X-Frame-Options: DENY`. Do not add a Content-Security-Policy casually; do a dedicated CSP pass after mapping Clerk, Sentry, Google OAuth, Vercel/Next runtime scripts/styles, and Tauri/browser behavior. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of commit `d4f53ad`, the dashboard has a signed-in Cortex readiness panel backed by `/api/user/readiness`. Use it as the first manual smoke surface: it shows source health, total ingested items, document/memory counts, Sage Mail queue count, Sphere Energy inputs, and personal-model adapter state without exposing raw email/calendar content. The endpoint is intentionally protected; signed-out public audits should keep returning 404/401 for `/api/user/readiness`. Production `dpl_DPvoERmRBwZ9mtEU8zAtLiSo9wng` passed `npm run check:launch -- --include-slow` with 21 ok / 0 warn / 0 fail after this landed. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of same-origin hardening commit `0b2742a`, sensitive browser-cookie mutation routes require `requireSameOrigin(request)` after user auth. This protects signed-in sessions from third-party pages driving state changes through CSRF-style POSTs while leaving webhooks, cron, and explicit API-key routes on their own auth paths. The latest canonical production proof is deployment `dpl_5WJNyE16TvKVfedtjDAQp2tYPGHr` / `https://cortex-m84bkhp1e-naomi-ivies-projects.vercel.app`, explicitly aliased to `https://cortex.eduforequality.org`; `npm run check:launch -- --include-slow` returned 22 ok / 0 warn / 0 fail, including `mutation_origin_guardrails` and RunPod adapter v5 preview `The personal model endpoint is online.` - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of usage-quota hardening commit `dcdc9a2`, expensive user and API-key routes are guarded by `enforceUsageQuota()` in `lib/security/usage-quota.ts`. The guard records `usage:*` events in `cortex_events` with `source = "cortex_usage"` and returns `429 usage_limit_reached` plus `Retry-After`/`X-Cortex-Usage-*` headers when hourly or daily limits are exceeded. Routes covered include chat, voice STT/TTS, Sage Mail drafts, assistant-loop, LoRA train/smoke, Gmail/Calendar sync, local/GroupMe import, profile build, sphere generation, day plan, briefing, and `/api/v1/query`. The guard fail-opens if the usage ledger has an outage, so treat it as cost/abuse protection rather than the primary auth boundary. Production proof: deployment `dpl_EUjyhiwGF3FLrYTDXabaygVfsUvE` / `https://cortex-jxwwchplp-naomi-ivies-projects.vercel.app` is aliased to `https://cortex.eduforequality.org`, and `npm run check:launch -- --include-slow` returned 23 ok / 0 warn / 0 fail with `usage_quota_guardrails` ok and RunPod adapter v5 responding upstream HTTP 200 in `44054ms`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of scheduled-resync audit commit `b0e28ef`, `npm run check:launch` verifies the daily `/api/cron/sync-all` contract through `scheduled_resync_contracts`: Vercel cron schedule `0 8 * * *`, `isAuthorizedCron(request)`, Gmail/Google Calendar/GroupMe adapters, `getFreshAccessToken`, `ingestItems`, `last_sync_status` success/error tracking, `sync_cursor`, and `total_items_synced`. The live audit also checks unsigned `GET /api/cron/sync-all` rejects with 401. Production proof: deployment `dpl_89MhLYPKRFHu4xPeBBuVEDidy2jw` / `https://cortex-4hyhworxo-naomi-ivies-projects.vercel.app` is aliased to `https://cortex.eduforequality.org`, and `npm run check:launch -- --include-slow` returned 25 ok / 0 warn / 0 fail with RunPod adapter v5 responding upstream HTTP 200 in `42699ms`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of always-present voice launcher commit `57bb5f3`, every signed-in dashboard page has a floating bottom-right **Talk to Cortex** launcher (`components/voice/voice-launcher.tsx`, `data-testid="voice-launcher"`) that opens `/voice`. The `/voice` console is the real browser click-to-talk loop: user clicks Start session, grants mic permission if prompted, browser records with `getUserMedia`/`MediaRecorder`, then calls `/api/voice/stt`, `/api/chat`, and `/api/voice/tts`. This is click-to-talk, not a finished native always-on listener; Tauri wake events now route to `/voice`, but real auto-start mic is still constrained by browser gesture rules and the native wakeword Rust path remains a stub unless future work implements Picovoice C FFI or a signed sidecar. Production proof: deployment `dpl_9YP53AdiJTqsbnYt32Xj1kDr3YmY` / `https://cortex-axgyx66bd-naomi-ivies-projects.vercel.app` is aliased to `https://cortex.eduforequality.org`, and final `npm run check:launch -- --include-slow` returned 26 ok / 0 warn / 0 fail with `auth_gate:voice_console` ok and RunPod adapter v5 responding upstream HTTP 200 in `41076ms`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of voice readiness commit `49c2460`, `/voice` checks `/api/voice/health` before starting the browser mic session. The console shows "Voice ready" when Groq STT and ElevenLabs TTS are configured, shows a setup/unknown state otherwise, and blocks Start session if provider configuration is missing. The full canonical proof command is still `npm run check:launch -- --include-slow`, but it now returns 27 ok / 0 warn / 0 fail because it includes the live `live_voice_health` gate plus RunPod adapter v5 smoke. Production proof: deployment `dpl_8WuXvdWWQZmua6rVaGqnmzdxB92S` / `https://cortex-2je9juth2-naomi-ivies-projects.vercel.app` is aliased to `https://cortex.eduforequality.org`, and post-deploy slow audit returned RunPod upstream HTTP 200 in `38796ms` with preview `The personal model endpoint is online.` - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of signed-in launch-smoke commit `5672dca`, Naomi's next manual smoke should start on the dashboard readiness card. The dashboard now has `data-testid="signed-in-launch-smoke"` and shows aggregate launch checks for Sources, Data depth, Sage Mail, Sphere Energy, Personal model, Talk to Cortex, and Approval safety. Future agents should ask Naomi to sign in at `https://cortex.eduforequality.org`, look for **Signed-in launch smoke**, and report any check that is not Ready before asking her to bounce between separate pages. Production proof: deployment `dpl_AvSzzzbCeDkk5wNtNjPre2xus8RJ` / `https://cortex-ncj2pn59k-naomi-ivies-projects.vercel.app` is aliased to `https://cortex.eduforequality.org`, and post-deploy `npm run check:launch -- --include-slow` returned 27 ok / 0 warn / 0 fail with RunPod adapter v5 upstream HTTP 200 in `43249ms`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of Google OAuth verification prep commit `fa6d628`, the app-side Google review evidence is live: `https://cortex.eduforequality.org/privacy` and `/terms` are public without sign-in, the landing page links both, `docs/google-oauth-verification.md` lists the production Gmail/Calendar callbacks and scope justifications, and the full production launch audit returns 29 ok / 0 warn / 0 fail when run with slow RunPod smoke. The remaining Google verification step is a Naomi/dashboard action in Google Cloud Console: submit the OAuth app verification using the canonical home, privacy, terms, and scope-justification evidence; future agents should not tell Naomi the app lacks public policy pages unless a fresh `npm run check:launch` fails. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of Sage Mail fresh-inbox repair commit `d171a25`, do not treat the Gmail "200 items" counters as proof the recent inbox is fully ingested. The active accounts previously had 200-item capped/cursored sync state and Sage Mail could show stale March `email_received` docs. Manual **Sync** on Integrations and **Sync latest** in Sage Mail now call the Gmail sync route with `mode: "inbox"` and query `in:inbox newer_than:180d`; the queue filters to a 45-day review window and surfaces stale diagnostics instead of pretending old mail is current. If Naomi still sees March mail, ask her for the Sage Mail diagnostics cards: Gmail accounts, Latest received, and Fresh window. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

When running the full local launch audit with slow LoRA smoke, remember that Vercel sensitive Production env vars for RunPod/R2 may pull as empty strings even though the deployed app can read them. The reliable local smoke pattern is to pull non-sensitive/Supabase envs, load the RunPod API key from the secure local Codex archive without printing it, set `RUNPOD_LORA_INFERENCE_ENDPOINT_ID=hhsl3wgl1unt7d`, then run `npm run check:lora-serving -- 73cb5aed-9bec-4e6c-9872-5f793f8775a6` or `npm run check:launch -- --include-slow`. On 2026-06-30, this returned 29 ok / 0 warn / 0 fail with RunPod adapter v5 upstream HTTP 200 in `39531ms`. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of commit `2ced683`, daily assimilation no longer relies on the generic Gmail cursor alone. `/api/cron/sync-all` performs the normal cursor-based fetch and then a bounded Gmail freshness pass with `GMAIL_DAILY_INBOX_QUERY = "in:inbox newer_than:180d"` and `GMAIL_DAILY_INBOX_MAX_RESULTS = 100`, recording `gmail_daily_inbox_last_sync_at`, `gmail_daily_inbox_last_items_fetched`, and `gmail_daily_inbox_has_more` in provider metadata. Future agents should preserve this two-pass pattern unless replacing it with a stronger queue/backfill architecture; it is the production guard against Sage Mail showing stale March-era inbox data. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

For Gmail depth, distinguish three paths: **Sync latest** uses `/api/integrations/gmail/sync` with `mode: "inbox"` and `in:inbox newer_than:180d`; daily assimilation uses `/api/cron/sync-all` plus the same fresh-inbox sweep; **Backfill history** uses `mode: "backfill"` and `provider_metadata.gmail_history_backfill_cursor` to ingest older mailbox pages safely over repeated runs. The Integrations `items seen` count is activity/accounting, not a unique-document cap; training and RAG read from `cortex_documents`, while LoRA formatting assembles all ingested sent/received email documents. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

As of guardrail hardening commit `b568808`, the red-team baseline includes explicit token-prefix exfiltration and approval-bypass attempts. Do not weaken `lib/ai/guardrails.ts` patterns for `cfat_`, `dckr_pat_`, `rpa_`, Stripe/GitHub-like prefixes, provider credential inventory wording, or "send/create/delete without review/confirmation" prompts unless replacing them with a stronger parser. `PRODUCT_LAUNCH_REDTEAM_PLAN.md` is now part of `npm run check:launch` product-surface checks, and the manual smoke now explicitly includes Gmail `Sync latest` / `Backfill history` count movement. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb

If the main `cortex-web` worktree is dirty from concurrent agents, deploy production from a clean temp worktree at the intended commit and copy `.vercel/project.json` into it before `vercel deploy --prod`; this avoided shipping unrelated local Meta/Instagram edits when deploying `b568808` as `dpl_9imZq88PrukRQYUkSX4Di4kJy2Qm`. Run post-deploy `npm run check:launch` from the same clean worktree or the static checks may read unrelated dirty local files and produce false failures. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
