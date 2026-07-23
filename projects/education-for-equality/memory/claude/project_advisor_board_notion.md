---
name: project-advisor-board-notion
description: "/advisor-board Notion integration — Codex-built org OS in Notion, wired into curriculum-app as 5-tab dashboard (Tasks/Docs/Team/Advisors/Pre-pilot)"
metadata:
  node_type: memory
  type: project
  originSessionId: 71aa2a37-5145-44bd-be9f-09de500267a0
---

The /advisor-board route at curriculum-app/app/advisor-board/ is Naomi's control room for her advisors + core team (Sonia, Richard, Joshua, herself). As of 2026-07-14 it is Notion-backed for the Tasks / Docs / Team tabs.

**Why:** Naomi needed one place where board members can see what needs doing, who's assigned what, and get task-assignment emails — without having to learn Notion. She already had a Codex-built Notion "Sabi Command Center" with fully-designed DBs (Tasks, People, Docs & Assets, Contacts, Org CRM, Opportunities, Roadmap, Risks, Metrics, Pilots, etc.). Rather than duplicate that in Supabase, the /advisor-board tabs read/write directly against Notion.

**How to apply:**
- Notion integration token = "Codex" bot owned by Naomi (naomi.u.ivie@tuck.dartmouth.edu). Full workspace access. Env: `NOTION_TOKEN` in curriculum-app/.env.local. All DB IDs live in same env file (NOTION_TASKS_DB_ID, NOTION_PEOPLE_DB_ID, etc.).
- Server-only wrappers at `curriculum-app/lib/notion/` (client.ts, tasks.ts, people.ts, docs.ts, types.ts). Uses raw fetch + Next.js `revalidate` for caching (30s tasks, 60s docs, 5min users) — no `@notionhq/client` dep.
- Route handlers at `curriculum-app/app/api/notion/` — every one is guarded by `isBoardMemberUser()` from `lib/board-access.ts`.
- `isBoardMemberUser` extended 2026-07-14 to include Joshua Ivie (joshua.ivie@velocitypathways.com) and Naomi's Tuck email.
- Task assignment uses Notion's native `Owner` people field. Sonia/Richard/Joshua must be added as **Notion Guests** to appear in the assignment dropdown — Naomi does this in Notion Settings → People → Add. They never need to open Notion; they just exist as assignable names.
- Client tabs: `components/advisor-board/{TasksTab,DocsTab,TeamTab}.tsx` — all client components, fetch on mount, optimistic updates.
- 5-tab nav: Tasks (default) / Docs / Team / Advisors / Pre-pilot. Active tab stored in localStorage.
- Task-assignment Resend emails: PENDING — will fire on `POST /api/notion/tasks` and on `PATCH /api/notion/tasks/[id]` when Owner changes.

## Task sign-off — "sign our work from the backend" (2026-07-23, session 818cc1ed)
Naomi's described vision: board/team members **sign off** their assigned work from the backend. Built + verified live on prod:
- **Notion Tasks DB** got two new columns via API: `Signed Off By` (rich_text) + `Signed Off At` (date). A signed-off task = Status `Done` + signer name + timestamp. Reopening a task (status → non-Done) auto-clears the stale signature (`updateTask` in `lib/notion/tasks.ts`; new `signOffTask()`).
- **In-app:** `POST /api/notion/tasks/[id]/sign-off` (guarded by `isBoardMemberUser`) stamps the signed-in member's display name (`boardUserDisplayName()` in lib/board-access.ts). Tasks tab shows a green **"Sign off ✓"** button per task → becomes **"✍️ Signed by X · date"** once signed.
- **One-click from email (no login)** = the non-technical-board UX win (backed by the board-software research: Boardable/OnBoard "My Tasks" + Gmail/Outlook one-click-action pattern). `lib/notion/task-tokens.ts` mints HMAC-signed 30-day tokens (secret = `[REDACTED:sensitive-label]` || `SUPABASE_SERVICE_ROLE_KEY`, which IS set on Vercel prod). `GET/POST /api/tasks/sign-off` is **public** (not in middleware's gated lists): GET renders a branded confirm page (never mutates — safe from email link-scanners), POST verifies token + signs off. The assignment email now leads with a green **"✅ Sign off — mark this done"** button carrying a per-recipient token.
- Deploy: repo is **manual `vercel` CLI deploy, NOT auto-deploy from GitHub** (push updates GitHub only). Shipped to prod, E2E verified (create task → public link → Done+signature in Notion → forged token rejected).

**Related:** [[project-e4e-tech]], [[project-sonia-coordinator]]
