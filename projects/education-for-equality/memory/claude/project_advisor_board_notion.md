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

**Related:** [[project-e4e-tech]], [[project-sonia-coordinator]]
