---
name: Set up git + Vercel proactively
description: When starting any new project, init git repo, create GitHub repo, link Vercel project automatically — don't wait to be asked.
type: feedback
originSessionId: a8c172f1-a7d4-4624-8ac2-b31c78a6f870
---
When building anything new (a new app, a new project, a fresh scaffold), set up the deployment infrastructure proactively as part of bootstrapping:

1. Ensure `.gitignore` is present and covers `.env*`, `node_modules`, `.next`, `.expo`, build artifacts.
2. Make a first commit if the repo has none.
3. Create a GitHub repo via `gh repo create <name> --private --source . --remote origin`.
4. Link/create a Vercel project via `vercel link` or `vercel` CLI.
5. Push to remote.

**Why:** Naomi explicitly said: *"this should be automatic for you when we're building something - I shouldn't have to tell you."* She doesn't want to micromanage scaffolding chores — she wants the working infrastructure to "just be there" by default.

**How to apply:**
- Trigger on: first commit-worthy moment in a new project, OR when she names a project and starts implementation.
- Don't ask permission for routine scaffolding (init, .gitignore, first commit) — just do it and report what was set up.
- DO confirm before pushing if anything looks sensitive (env files staged, credentials in code) or before making the repo public.
- The pattern: provision quietly → tell her the URLs/short status at the end.
