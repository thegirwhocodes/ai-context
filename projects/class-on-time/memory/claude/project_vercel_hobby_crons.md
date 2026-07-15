---
name: Class on Time Vercel deployment quirks
description: Hobby plan blocks sub-daily crons; frequent jobs run via GitHub Actions instead. Root Directory must be set to `apps/server` in dashboard.
type: project
originSessionId: a8c172f1-a7d4-4624-8ac2-b31c78a6f870
---
The `go` Vercel project (`prj_J3nKeJIt49EmTgiTrproul8YdbE5` under `naomi-ivies-projects` team) is on the Hobby plan. Two operational constraints:

1. **Crons** — Hobby only allows daily-or-less crons. `vercel.ts` registers only the two daily ones (`morning-rollcall` 7am ET, `lockup-sweep` 3am). The three frequent ones (`calendar-sync`, `departure-tick`, `penalty-charges`) are triggered by `.github/workflows/cron.yml` (GitHub Actions every 5 min, free). Each endpoint is idempotent so over-firing is harmless.
2. **Root Directory** — the repo is a monorepo. The Vercel project's Root Directory setting must be `apps/server` (set via dashboard → Project Settings → General → Root Directory), or deploys fail with "No Next.js version detected" because Vercel's pre-check looks at the root `package.json` for `next` instead of `apps/server/package.json`.

**Why:** Naomi is solo-building this and doesn't want to pay Pro ($20/mo) before there's revenue. The GitHub Actions workaround is free and works fine for her scale. Upgrade to Pro and we can put everything back in Vercel, but no reason yet.

**How to apply:**
- When changing cron schedules, edit either `vercel.ts` (daily-or-less only) or `.github/workflows/cron.yml` (anything more frequent). Don't put a sub-daily expression in `vercel.ts` — it'll block the deploy.
- The workflow file requires the GitHub repo to have:
  - **Secret** `VERCEL_CRON_SECRET` = same as `CRON_SECRET` env var on Vercel.
  - **Variable** `APP_URL` = the Vercel production URL.
- Pushing `.github/workflows/*` requires the local `gh` token to have `workflow` scope. If a push is rejected with "refusing to allow an OAuth App to create or update workflow", run `gh auth refresh -s workflow` once.
