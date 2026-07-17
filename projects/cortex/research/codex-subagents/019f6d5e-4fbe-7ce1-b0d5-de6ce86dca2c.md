---
session_id: "019f6d5e-4fbe-7ce1-b0d5-de6ce86dca2c"
source: "codex-subagent"
project: "cortex"
parent_session_id: "019f6256-8920-7483-b5d7-771d17c11780"
agent_path: ""
nickname: "Averroes"
ended: "2026-07-17T00:18:40.015Z"
---

# Codex subagent report: Averroes

Audit complete at exact clean checkout `935871481e532bd05b928d625d63d068c3355498`. No files were edited, so no new commit or tests were necessary. Issue [#22](https://github.com/thegirwhocodes/cortex-web/issues/22) remains open and PR [#28](https://github.com/thegirwhocodes/cortex-web/pull/28) remains draft/unmerged.

## Required names

Dedicated staging and production both need separate values under the same names.

Application baseline, enforced by [readiness.ts](/Users/naomiivie/cortex/.worktrees/cortex-integration-held/lib/config/readiness.ts:17):

```text
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
CLERK_SECRET_KEY
TOKEN_ENCRYPTION_KEY
ANTHROPIC_API_KEY
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI
```

Release and signed-in operation:

```text
NEXT_PUBLIC_APP_URL
CRON_SECRET
CLERK_WEBHOOK_SECRET
CORTEX_RELEASE_MAINTENANCE_MODE
```

Operator process only—not Vercel application variables:

```text
VERCEL_TOKEN
CORTEX_DATABASE_URL
CORTEX_PRODUCTION_DOMAIN
CORTEX_EXPECTED_DEPLOY_SHA
```

Supabase Vault names:

```text
cortex_agent_runtime_endpoint
cortex_agent_runtime_cron_secret
```

Production provider gates not fully covered by general readiness:

```text
GOOGLE_OAUTH_STATE_SECRET
META_APP_ID
META_APP_SECRET
META_OAUTH_STATE_SECRET
META_WEBHOOK_VERIFY_TOKEN
META_INSTAGRAM_APP_ID
META_INSTAGRAM_APP_SECRET
META_INSTAGRAM_CONFIG_ID
META_WHATSAPP_CONFIG_ID
META_WHATSAPP_SOLUTION_ID
META_GRAPH_VERSION
GROUPME_CLIENT_ID
```

Repository production-readiness recommendations, when those surfaces are in launch scope:

```text
RUNPOD_API_KEY
RUNPOD_ENDPOINT_ID
RUNPOD_LORA_INFERENCE_ENDPOINT_ID
LORA_WEBHOOK_SECRET
S3_BUCKET
S3_REGION
S3_ACCESS_KEY
S3_SECRET_KEY
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
STRIPE_PRO_PRICE_ID
COMPOSIO_API_KEY
```

## Dedicated staging checklist

1. Provision dedicated staging Vercel, Clerk, and Supabase environments. Do not reuse production identity, database, OAuth, Vault, or encryption credentials.
2. Establish the staging database through migration 013.
3. Configure all baseline and release names above.
4. Create the two staging Vault entries. The endpoint must use the staging canonical HTTPS host and end exactly in `/api/cron/agent-runtime`; the Vault cron secret must correspond to staging `CRON_SECRET`.
5. Stage two Production-target deployments from exact `935871481e532bd05b928d625d63d068c3355498`:

   - candidate with maintenance disabled;
   - separate maintenance deployment with `CORTEX_RELEASE_MAINTENANCE_MODE` enabled.

6. Run `candidate-staged` with the full 40-character SHA and without `--allow-drift`.
7. Move the staging canonical alias to maintenance. Run the maintenance checker, then separately prove representative browser, mutation, webhook, OAuth callback, and cron routes return retryable 503 responses. Stop all staging workers that bypass Vercel.
8. Apply `014→022` in one stop-on-error outer transaction, including migration-history recording. Migration 022 must finish with exactly one inactive job.
9. Retain proof of all nine migration versions, quarantine review, zero tenant-composite orphans, service-role-only RPC privileges, and inactive scheduler readiness.
10. Run `candidate-ready` against the staged candidate. Require exact SHA, Production target, candidate/canonical isolation, HTTP 200 readiness, one valid job, and `active=false`.
11. Promote the same candidate deployment ID without rebuilding. Run `promoted`; require canonical readiness with the scheduler still inactive.
12. Activate through `activate_cortex_agent_runtime_scheduler()`.
13. Run `first-tick` after the next boundary. Retain cron, request-ID/HTTP-response, runtime-run, queue-depth, trace, account-isolation, and Action-receipt evidence.
14. Complete signed-in desktop, 390px mobile, accessibility, account-isolation, copy, and Action-receipt acceptance before production authorization.

## Final production checklist

1. Obtain explicit coordinated approval and freeze exact SHA `935871481e532bd05b928d625d63d068c3355498`.
2. Confirm backup/PITR, migration hashes, baseline through 013, no in-flight Action executions, rollback deployment IDs, and a complete inventory of bypass workers.
3. Configure production application names and the two production Vault names. Verify only masked/name/boolean evidence; never expose values.
4. Confirm the Vault endpoint host is the actual production canonical host—not merely any syntactically valid HTTPS host.
5. Stage exact-SHA candidate and maintenance deployments separately.
6. Pass `candidate-staged`; retain the candidate deployment ID.
7. Promote maintenance, pass its checker, run independent 503 negative probes, pause bypass workers, and timestamp the write freeze.
8. Apply `014–022` atomically with migration-history bookkeeping. Any failure before commit must roll back the entire operation.
9. After commit, never return to the pre-cutover app. Keep maintenance canonical and the scheduler inactive.
10. Prove migration history, quarantines, orphan checks, privileges, exactly one five-minute job, and `active=false`.
11. Pass `candidate-ready`.
12. Promote the previously recorded candidate deployment ID—no rebuild—and pass `promoted`.
13. Activate once through the service-role-only RPC.
14. Pass `first-tick` within 15 minutes and inspect runtime/queue/trace evidence.
15. Preserve all deployment IDs, SHA, migration output/history, readiness reports, activation result, first-tick evidence, and recovery actions.

Safe recovery is correctly defined in the [runbook](/Users/naomiivie/cortex/.worktrees/cortex-integration-held/docs/AGENT_RUNTIME_RELEASE_RUNBOOK.md:163):

- Before database commit: roll back the transaction and restore the previous deployment.
- After commit: deactivate the scheduler and use only the new app, schema-compatible maintenance, or a forward fix. Never restore the old app.
- After a bad first tick: deactivate immediately; the new app may remain canonical only if its non-runtime smokes remain healthy.

## Contradictions and missing proof

The original deployment-versus-migration ordering contradiction is resolved: [migration 022](/Users/naomiivie/cortex/.worktrees/cortex-integration-held/supabase/migrations/022_agent_runtime_scheduler.sql:155) installs inactive, readiness is GET-only, promotion precedes activation, and POST alone executes work.

Remaining gaps:

- The runbook’s sample atomic command does not show Supabase migration-history writes inside the transaction. “Reconcile afterward” is weaker than atomic schema-plus-history bookkeeping.
- The maintenance checker validates one self-reporting endpoint; it does not independently prove blocked mutation/webhook/cron routes or stopped bypass workers.
- Vault endpoint validation checks URL shape but not that its hostname is the intended canonical environment.
- Candidate readiness proves the checker secret matches the deployed app secret, but not that the Vault cron secret matches it. That equality is only exercised by the first scheduler POST.
- Promotion does not bind to the candidate deployment ID recorded earlier. A same-SHA rebuild could pass, despite the runbook requiring promotion without rebuilding.
- Exact-SHA checking accepts SHA prefixes and offers `--allow-drift`; operators must provide the full SHA and omit drift allowance.
- First-tick proof binds a `pg_net` request ID to its HTTP response, but cron status and request evidence are selected independently without a strict run/timestamp correlation.
- Protected staged deployments may block the direct checker request; the checker has no Vercel protection-bypass support.
- General readiness does not cover all Meta/provider launch variables, so a green readiness response is not proof that the Issue #22 provider gates are complete.

Changed files: none. Tests run: none. Dependencies installed: none. Remaining owner blockers are dedicated staging provisioning and signed-in acceptance, Full Disk Access evidence, Meta and Google production approval, production Vault configuration, retained choreography proofs, and explicit production authorization.
