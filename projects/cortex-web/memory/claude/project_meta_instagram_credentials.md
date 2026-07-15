---
name: project-meta-instagram-credentials
description: "Meta/Instagram OAuth status — working as of 2026-07-13 using single \"Cortex\" app 782931888175092, invalid secondary app removed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 14c38de3-5375-4634-b108-3d8bfb785aca
---

Meta/Instagram OAuth — resolved 2026-07-13:

- **Working app:** "Cortex" Facebook app `782931888175092` with secret `5072ba...` — confirmed valid via Graph API. Used for BOTH Facebook Login (Page-based Instagram) AND Instagram Login flows.
- **Invalid app removed:** `META_INSTAGRAM_APP_ID=2010673032973140` returned "Cannot get application info" on Graph API regardless of secret. Removed from Vercel Production and .env.local — code in `getInstagramLoginAppId()` falls back to `META_APP_ID`.
- **Vercel Production env:** `META_APP_ID`, `META_APP_SECRET`, `META_OAUTH_STATE_SECRET`, `META_WEBHOOK_VERIFY_TOKEN` are set. `META_INSTAGRAM_APP_ID` and `META_INSTAGRAM_APP_SECRET` are intentionally absent (fallback to main app).
- **Production deployment:** `dpl_FZ53X54C83Sunpi8qoay4jnZKNvu` / `cortex-q9omplz72-naomi-ivies-projects.vercel.app` aliased to `cortex.eduforequality.org`. Callback returns `instagram_missing_oauth_state` (correct), OAuth URL redirects to Instagram consent screen (correct), webhook returns 403 (correct).
- **Other Codex's fixes (commits 560ebfc, 102e848):** Fixed auth URL (`www.instagram.com` → `api.instagram.com`), redirect URI to use canonical `NEXT_PUBLIC_APP_URL`, FormData for token exchange, `data[]` array response handling, redirectUri preserved in state.
- **Still invalid:** Both Meta system-user and personal access tokens (in files at cortex root) return OAuthException 190/460 — password change invalidated them. Need regeneration in Meta Business Manager for webhook setup automation (`/api/cron/meta-webhooks`).

**Why:** Naomi needs Instagram DM ingestion for Cortex Layer 1. OAuth is the first step to getting a Page/Instagram access token.
**How to apply:** Instagram OAuth should work end-to-end now for any user who clicks "Connect with Meta" in the Integrations UI, as long as their Instagram account is a professional/business account. The Meta app must also have App Review approval for `instagram_business_manage_messages` for non-admin users.
