---
name: project-meta-provider-readiness
description: Meta (WhatsApp Cloud API + Instagram) provider-readiness lane — deliverables and the tenant-isolation routing risk
metadata: 
  node_type: memory
  type: project
  originSessionId: 02d60305-9513-4d94-857b-0af9ae81a089
---

Lane `claude/meta-provider-readiness` (cortex-web PR #4, 2026-07-14) audited the WhatsApp Business Cloud API + multi-account Instagram code for provider verification readiness.

Deliverables (all in cortex-web): `scripts/check-meta-provider-readiness.ts` (independent, network-free behavioural checker — distinct from the source-grep/live `check-meta-messaging.ts`), `tests/fixtures/meta/*`, `tests/meta-provider-readiness.test.ts`, `docs/META_PROVIDER_RELEASE.md`. Baseline positives verified: signed-webhook verify (prod fails closed), OAuth-state CSRF, idempotent multi-account webhook routing, AES-256-GCM token-at-rest, lawful export/import boundary (no scraping).

**Non-obvious risk (F1, High) — webhook routing keys are not globally unique.** `cortex_integrations` is `UNIQUE(user_id, provider, provider_user_id)` (scoped per user, migration 008), so two Cortex users can each register the same WhatsApp `phone_number_id` / Instagram `instagramAccountId`/`pageId`. WhatsApp webhook `findIntegration` uses `.maybeSingle()` → throws/500s the whole webhook on a duplicate; Instagram webhook returns the FIRST active match → cross-tenant DM misroute. Root enabler: `whatsapp/connect` + `instagram/connect` POST accept an unverified identifier. Fix belongs in Codex 01 (whatsapp-core) + 02 (messaging-roots): verify asset ownership at connect + partial unique index `(provider, provider_user_id) WHERE status='active'` + deterministic routing.

Other gaps: F2 Instagram Login long-lived tokens never refreshed (no `ig_refresh_token` cron → reconnect every ~60d); F3 Facebook-Page IG route stores ~1h short-lived tokens (skips `fb_exchange_token`); F4 `total_items_synced` inflates on webhook retries. Full detail in docs/META_PROVIDER_RELEASE.md §9. Meta login/app/App-Review are Naomi-owned; nothing submitted. Related: [[project_meta_instagram_credentials]], [[project_cortex_tech]].
