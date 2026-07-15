---
name: Vercel project bootstrap — known gotchas and the right order
description: Checklist + workarounds learned the hard way during the Go project bootstrap. Follow this checklist instead of trial-and-error on future projects.
type: project
originSessionId: a8c172f1-a7d4-4624-8ac2-b31c78a6f870
---
When bootstrapping a new Vercel project from this codebase (or any npm-workspaces monorepo), apply these once, in this order:

### 1. Naming
- Vercel project names must be lowercase letters, digits, `.`, `_`, `-` — no spaces, no `---`. The local directory name "Class on Time" is illegal as a Vercel name; `vercel link --yes` will fail. Pass `--project <name>` explicitly when linking.
- Naomi prefers `go-*` URLs. The default `go-<team-slug>.vercel.app` alias is acceptable. Don't claim short custom aliases like `go-class.vercel.app` without explicit confirmation — she pushed back on this.

### 2. Framework detection (the "No Next.js version detected" trap)
- Vercel's framework detection scans the ROOT `package.json`. It does **not** follow npm workspaces. If `next` is only in `apps/server/package.json`, detection fails.
- **Fix:** hoist `next` (matching version) into the root `package.json` `devDependencies`. Nothing actually consumes it at root, but Vercel's pre-check now passes.
- **Don't** set `rootDirectory` to `apps/server` as the "fix" — it breaks `--workspace` build flags because npm no longer sees the parent monorepo. Keep Root Directory = repo root.

### 3. Hobby plan cron limit
- Hobby blocks sub-daily cron expressions. Keep only daily-or-less crons in `vercel.ts`. Run frequent jobs via GitHub Actions (`.github/workflows/cron.yml`), `*/5 * * * *`. Each cron endpoint must be idempotent.

### 4. Deployment Protection is ON by default
- New Vercel projects ship with Vercel Authentication enabled → every URL returns 401.
- **Disable via API:** `PATCH /v9/projects/{id}` body `{"ssoProtection": null}`. Also clear `passwordProtection` if set.
- **Edge cache caveat:** after disabling, the edge can serve cached 401s for ~30s. Cache-bust with a query string to verify.

### 5. Vercel API authentication
- The CLI token lives at `~/Library/Application Support/com.vercel.cli/auth.json` (key: `token`). Read it once at the start of an automation block, reuse for every call.
- Team ID isn't shown by `vercel teams ls` — that prints the slug. Resolve with `GET /v2/teams?slug=<slug>` → `id` field. For Naomi: slug `naomi-ivies-projects`, id `team_kHocFRxccHQd19iVWl4NB2Zv`.

### 6. Env var updates
- `vercel env add KEY env` errors with `ENV_CONFLICT` if the var already exists.
- **Right order:** `vercel env rm KEY production --yes` → `printf '%s' VALUE | vercel env add KEY production`.
- Don't use `echo` to pipe values (adds newline). Always `printf '%s'`.

### 7. Pushing `.github/workflows/*`
- The default `gh auth login` scope doesn't include `workflow`. Push is rejected.
- **Fix (user must run):** `gh auth refresh -s workflow` once. Then workflow files can be pushed. Don't try to bundle workflow files in the initial push.

### 8. Monorepo `vercel.json` shape that works
```ts
{
  framework: 'nextjs',
  buildCommand: 'npm --workspace apps/server run build',
  installCommand: 'npm install',
  outputDirectory: 'apps/server/.next',
  crons: [/* daily-or-less only on Hobby */]
}
```

### 9. Production URL
- The current Go project uses `https://go-naomi-ivies-projects.vercel.app` as the production alias (auto-generated, follows `<project>-<team-slug>` pattern). This is what to put in `NEXT_PUBLIC_APP_URL` and `GOOGLE_REDIRECT_URI` env vars on Vercel Production.

### Why all this matters
Naomi explicitly said *"work much faster - maybe read all the docs before working"*. The fastest path is: read this memory first, apply in order, no trial-and-error.
