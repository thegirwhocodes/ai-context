---
name: project-e4e-google-oauth
description: E4E curriculum-app Google sign-in runs through Supabase Auth (not Clerk); OAuth client + callback config
metadata: 
  node_type: memory
  type: project
  originSessionId: 3656ec2d-babd-4f3e-9b97-a7cb9f9d17be
---

The **curriculum-app** (eduforequality.org) sign-in uses **Supabase Auth**, project ref **`ffrezdtqagwdacvqcqgn`** (`ffrezdtqagwdacvqcqgn.supabase.co`). Google "Continue with Google" goes app → `supabase.auth.signInWithOAuth('google')` → Supabase → Google → `/auth/callback` (`exchangeCodeForSession`, same path as magic links).

**Google OAuth configured & verified working Jul 14 2026 (session 3656ec2d):**
- Google Cloud OAuth client ID `406778631456-…apps.googleusercontent.com` (secret `GOCSPX-…`, stored in gitignored `curriculum-app/.env.supabase-management.local`, and set in Supabase via Management API — `external_google_enabled=true`).
- Required Google-side **Authorized redirect URI**: `https://ffrezdtqagwdacvqcqgn.supabase.co/auth/v1/callback` (the Supabase callback, NOT the app URL). Verified: authorize endpoint 302s to Google's real sign-in screen, no `redirect_uri_mismatch`.

**⚠️ Red herring:** that OAuth client was initially registered with only a **Clerk** redirect URI (`https://clerk.eduforequality.org/v1/oauth_callback`) — but the app is on **Supabase, not Clerk**. Don't let the `clerk.eduforequality.org` domain mislead you. Gotcha we hit: Naomi first pasted the callback into Google's **Authorized JavaScript origins** field (origins only, strips the path); the full callback path must go in **Authorized redirect URIs** (the field that already listed the clerk URL).

Supabase management token lives in `curriculum-app/.env.supabase-management.local` (`SUPABASE_ACCESS_TOKEN`), usable for `PATCH https://api.supabase.com/v1/projects/ffrezdtqagwdacvqcqgn/config/auth`. Cortex's separate Google creds (`138689267057-…`, localhost redirect URIs) are a DIFFERENT app — never mix them in. [[reference_e4e]] [[feedback_verify_by_driving]]
