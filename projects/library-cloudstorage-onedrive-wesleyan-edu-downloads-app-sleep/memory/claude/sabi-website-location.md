---
name: sabi-website-location
description: The Sabi website lives in the curriculum-app repo and serves two hosts with a split canonical scheme
metadata:
  node_type: memory
  type: project
  originSessionId: fe7c445d-a859-4c67-8815-a00089db9f42
  modified: 2026-08-17T20:58:50.033Z
---

The Sabi website is `~/Education for Equality/curriculum-app` (GitHub:
`thegirwhocodes/Education-for-Equality`, Vercel project `education-for-equality`).
The repo name gives no hint that it is the Sabi site.

One Next.js app serves two hosts, and `middleware.ts` rewrites paths on the
subdomain (`/` → `/sabi`, `/pricing` → `/sabi/pricing`, `/demo` → `/sabi-voice`,
`/chat` → `/sabi-demo`):

- `eduforequality.org` — the Education for Equality organisation site
- `sabi.eduforequality.org` — the Sabi product site (canonical home for Sabi)

**Why:** Both hosts serve the same Sabi pages, so canonical URLs are split by
purpose — Sabi pages canonicalise to the subdomain, org pages to the apex.
Shared hosts, canonical URLs and structured data live in `lib/seo.ts`.

**How to apply:** Never set `alternates.canonical` in `app/layout.tsx` — Next
inherits root metadata down the whole tree, which previously pointed every route
at the homepage and kept the site out of Google's index. Set canonicals per page,
and remember `middleware.ts` must keep exempting `/robots.txt` and `/sitemap.xml`
from the subdomain catch-all redirect.

Related: [[sabi-brand-query-competition]]
