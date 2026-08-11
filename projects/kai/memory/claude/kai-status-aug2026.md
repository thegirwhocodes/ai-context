---
name: kai-status-aug2026
description: "Kai state as of Aug 11 2026 — shipped, deployed, single-user; the launch blockers are auth/DB + Google OAuth verification"
metadata:
  node_type: memory
  type: project
  originSessionId: bfcc8fd6-7858-418f-9aeb-0bc28332b184
  modified: 2026-08-11
---

Kai ("Kai Focus") = adaptive AI focus coach at `/Users/naomiivie/kai`, live on `https://heykai.vercel.app` (Vercel project `naomi-ivies-projects/kai` — note `.vercel/project.json` still says the old name `pomodoro-agent`). Repo `github.com/thegirwhocodes/kai`.

**State on 2026-08-11:** last commit `c842652` (2026-07-23, pre-release testing research), working tree clean, `main` in sync with origin, last prod deploy 19 days old and Ready = deployed code == HEAD. No Kai work since Jul 23. `node_modules` was cleaned off the laptop, so `npm test` fails with "vitest: command not found" until `npm install` — the 22 unit tests themselves are fine.

**Shipped:** Next.js 16 / React 19 / TS strict / Tailwind 4 / Zustand; landing `/` + app `/app` + pricing/privacy/terms/support/changelog/testers; Claude Haiku 4.5 agent with 25 tools (`src/lib/agent/`), Groq Whisper STT + ElevenLabs TTS; Google Calendar (read/write/reschedule), Gmail (search + draft-only, never sends), Spotify library-first playback, 5-provider web search, Alexa skill webhook, "Hey Kai" wake listening; classic-Pomodoro timing + lock-in planner + adaptive engine (see [[kai-timing-model]]).

**Real gaps (in priority order, from `docs/COMPETITIVE_AND_ARCHITECTURE_REVIEW.md` + `docs/PRE_RELEASE_TESTING_RESEARCH.md`):**
1. Single-user by design — no auth, no DB, all Google/Spotify tokens are Naomi's own. Testers literally cannot use it. #1 blocker.
2. Google OAuth verification not started — the only weeks-long external dependency; unverified caps at ~100 users + scary consent screen. Minimize scopes to dodge the annual CASA assessment that full Gmail content triggers.
3. No Sentry, no analytics (PostHog), no E2E/smoke tests, no branch protection on `main`, no feature flags.
4. Prod env has only Anthropic/Groq/ElevenLabs/Calendar/Spotify/`ALEXA_VERIFY_SIGNATURES`. **No Gmail creds, no web-search keys, no KV/Upstash, no `ALEXA_SKILL_ID`, no `NEXT_PUBLIC_SITE_URL`** — so on prod: Gmail + web search are dead, and waitlist emails are only recoverable from Vercel logs (`/api/waitlist` falls back to `console.log`).
5. Spotify extended API is closed to new indie apps (post-2024-11-27) — never depend on Recommendations/Audio Features; user playlists + Kai-curated tags only.

**Business framing:** pricing plan is $9/mo / $72/yr with a $99-lifetime founding tier under consideration; ambient-focus band is $5–9/mo so the AI planning + voice layer must be the headline, not the backgrounds. In the Aug 1 2026 "$200/user" strategy conversation the conclusion was that **Cortex, not Kai, is the $200/mo vehicle** — Kai is a consumer app in the $5–15/mo band.

**Why it matters:** the craft is done; what's missing is the multi-user foundation and the OAuth clock. Any "launch Kai" work should start with auth+DB and starting Google verification, not more features.

**How to apply:** work in `/Users/naomiivie/kai` (see its `AGENTS.md`), `npm install` first, lint+build+`npm test` before shipping, push `main`, deploy prod. Related: [[kai-timing-model]].
