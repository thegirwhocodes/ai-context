---
name: kai-status-aug2026
description: "Kai state as of Aug 11 2026 — Flocus-grade focus app shipped to prod on Groq; selling layer (accounts + Stripe) is the next pass"
metadata:
  node_type: memory
  type: project
  originSessionId: bfcc8fd6-7858-418f-9aeb-0bc28332b184
  modified: 2026-08-11
---

Kai ("Kai Focus") = calm Pomodoro focus room at `/Users/naomiivie/kai`, live on `https://heykai.vercel.app` (Vercel project `naomi-ivies-projects/kai`; `.vercel/project.json` still carries the old name `pomodoro-agent`). Repo `github.com/thegirwhocodes/kai`.

**Direction set 2026-08-11:** build Kai to Flocus quality as a sellable standalone focus app FIRST, add the agent layer after; move the agent off Anthropic onto cheaper inference. Naomi chose "polish first, sell next pass" over wiring Stripe now, and Groq `openai/gpt-oss-120b` over Ollama (Ollama can't serve customers from Vercel).

**Shipped to prod this session** (commits `5cdf3c7`, `3947b4e`, `db1c1e2`, `1e0e22e`):
- Agent runs on **Groq** via the OpenAI-compatible API, `[REDACTED:sensitive-label]` with a `llama-3.3-70b-versatile` fallback. `@anthropic-ai/sdk` removed. The app's internal message format stays block-shaped and provider-neutral — only `src/app/api/agent/route.ts` translates, so swapping providers again is a one-file change. Verified on prod: correct tool calls, and it says the user's real 5-minute break, not the textbook 15.
- System prompt rewritten for an open-weight model (numbered hard rules for speech/durations/honesty) and de-personalized — no more hardcoded Sabi/E4E priorities.
- First-run **Welcome** (name, focus length, what you're working on), stats panel, layered **ambient sound mixer** (5 generated textures, keeps playing when the panel closes), keyboard shortcuts, widget toggles, mobile pass, landing page rewritten around "start focusing free, no account".
- Sessions now roll at midnight into a capped `history` log (store v2 migration splits existing piles) — every "today" figure was previously an all-time figure. 43 unit tests pass.

**Security fix — the app was leaking her Google data.** `/api/recommendation` was auto-fetched on page load and its response includes the owner's next calendar event and email senders/subjects, so every visitor to heykai.vercel.app was planning against — and seeing into — Naomi's accounts. Also the Alexa command queue is one shared server-side list every tab polled, so her Alexa could drive a stranger's timer. Now: planning is opt-in, calendar/email/Spotify/Alexa require `KAI_OWNER_TOKEN` (set in Vercel prod), visitors get task-only planning. **Owner token = `OEacqNwky7AS2WNS7xoK92Nl`** — paste into Customize → Connected accounts in her browser. Unset token = open in local dev, closed in production.

**Known broken (pre-existing, not from this work):**
- **ElevenLabs is unpaid** — `/api/tts` returns 401 `payment_issue` ("failed or incomplete payment"). Kai falls back to browser speech. Same account may serve Sabi.
- **Google Calendar refresh token is dead** — `invalid_grant`. Needs re-authorization; likely the 7-day expiry that applies while an OAuth app is still in "Testing" status, which ties back to the un-started verification.
- Gmail creds and web-search keys are still absent from prod entirely.

**Next pass:** accounts + Stripe (the actual selling layer), then per-user OAuth. Google OAuth verification remains the long-pole external dependency. Also unguarded and costing money on a public URL: `/api/agent`, `/api/transcribe`, `/api/tts`.

**How to apply:** work in `/Users/naomiivie/kai` (see its `AGENTS.md`), `npm install` first (node_modules gets cleaned off the laptop), then lint + build + `npx vitest run` before shipping; push `main`; `vercel --prod --yes`. Related: [[kai-timing-model]].
