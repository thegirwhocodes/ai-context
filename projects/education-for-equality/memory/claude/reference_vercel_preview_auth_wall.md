---
name: reference-vercel-preview-auth-wall
description: "E4E Vercel project gates PREVIEW deploys behind Vercel Authentication — can't verify preview UI without SSO; verify on prod"
metadata:
  node_type: memory
  type: reference
  originSessionId: 3656ec2d-babd-4f3e-9b97-a7cb9f9d17be
---

The Vercel project `curriculum-app` (team `naomi-ivies-projects`, deployment domain `education-for-equality-*.vercel.app`, prod alias `eduforequality.org`) has **Deployment Protection / Vercel Authentication ON for Preview deploys**.

- Hitting a preview URL (e.g. `education-for-equality-<hash>-naomi-ivies-projects.vercel.app`) returns Vercel's own **SSO login page**, not the app. Tell it's the wall (not the app) by `data-testid="login/google-button"` in the HTML and the absence of app copy like "Welcome back". So **curl/Browser-pane cannot verify preview UI** without authenticating through Vercel SSO.
- **Verify on production instead** — `https://eduforequality.org/...` is public. Push to `main` → prod deploy → curl/read the live page. (Prod also has the Supabase/Resend env vars that Preview lacks.)
- Preview builds ALSO fail if any module calls `createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, …)` at import time, because Preview env has no `NEXT_PUBLIC_SUPABASE_URL`. Guard module-level Supabase clients with placeholder fallbacks (see `lib/auth/browser.ts`, `lib/auth/server.ts`, and now `lib/supabase.ts`). — session 3656ec2d

To truly verify a preview UI you'd have to disable protection in Vercel project settings (Deployment Protection) — don't do that unprompted. [[reference_e4e]]
