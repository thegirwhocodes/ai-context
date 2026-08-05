---
name: project-overview
description: "Naomi's personal accelerator + operating system built in /Users/naomiivie/businesses — research corpus, 24-month curriculum, Holdco Command tool"
metadata:
  node_type: memory
  type: project
  originSessionId: 88dee036-7369-4428-8d47-834e770d417b
  modified: 2026-08-05T00:48:11.474Z
---

The `businesses` project is Naomi's personal "become a world-class founder" system, built after the 2026-08-04 deep-research session.

**Repo:** `thegirwhocodes/businesses` (private) at `/Users/naomiivie/businesses`

**Structure:**
- `research/` — six deep-research corpora (~39k words) — MBA canon, YC/founder essay canon, founder mental models, company operating systems, canonical reading list, modern learning ecosystem
- `curriculum/` — 24-month sequenced curriculum + product concepts doc (~14k words)
- `apps/curriculum/` — Next.js site rendering research + curriculum → deployed at **https://founder-accelerator.vercel.app** (Vercel project: `founder-accelerator`)
- `apps/holdco/` — Next.js "Holdco Command" multi-business operating dashboard → deployed at **https://holdco-command.vercel.app** (Vercel project: `holdco-command`), Basic Auth gated

**Holdco Command default password:** `founders-only-2026` — override via `vercel env add HOLDCO_PASSWORD production` on the `holdco-command` project.

**Storage today (v1):** browser localStorage. Real backend (Supabase — reuse creds from `/Users/naomiivie/cortex/cortex-web/.env.local`, prefixed tables) is planned for weeks 3-4 of the [[holdco-6-week-plan]].

**Why:** She's a first-time founder running multiple operating businesses in parallel. Ambition = "build a company like Amazon." She rejected generic productivity advice; she wanted rigorous synthesis of what top founders, MBA programs, and YC actually teach — plus a tool to install the mechanisms in her own week.

**Load-bearing insight from the whole corpus:** great operators convert principles into mechanisms. Every artifact here exists to install one mechanism that survives her mood.

**How to apply:** When she asks about anything founder / business / curriculum related, this is the working system to point back to. When editing the source markdown (`research/*.md` or `curriculum/*.md`), the curriculum site's copy at `apps/curriculum/content/` also needs to be re-synced (currently manual `cp -r`; TODO: prebuild script). The holdco tool's schema lives in `apps/holdco/src/lib/store.ts`.
