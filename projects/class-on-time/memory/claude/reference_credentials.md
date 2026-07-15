---
name: Reusable credentials live in cortex-web
description: When the user needs OAuth/API keys for any new project, check `/Users/naomiivie/cortex/cortex-web/.env.local` first — it has Google OAuth (Calendar scope), Anthropic, Supabase, Clerk, etc.
type: reference
originSessionId: a8c172f1-a7d4-4624-8ac2-b31c78a6f870
---
The user actively prefers to **reuse credentials from her existing projects** rather than creating new accounts. Always audit before asking her to set anything up.

Primary trove: `/Users/naomiivie/cortex/cortex-web/.env.local`. As of 2026-05-09 it contained real values for:

- Google OAuth (`GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`) — has calendar.readonly + calendar.events scope, redirect URIs at `http://localhost:3000/api/integrations/{gmail,calendar}/callback`. **Match these exact paths in new code so no Google Cloud Console changes are needed.**
- Anthropic API key.
- Supabase project (`addkjndgmbxiulpquizn.supabase.co`) — service role + anon keys present. Don't dump new app tables into the cortex schema; create a new Supabase project for clean separation.
- Clerk test keys.
- ElevenLabs, Groq, Cerebras (other LLM/voice work).

Secondary: `/Users/naomiivie/cortex/.env.vercel` — production keys (Clerk live, Twilio, Africa's Talking, separate Supabase).

Other troves found in the 2026-05-09 audit:
- **Stripe test keys** (account prefix `51S995F...`) — `~/Downloads/server.js`, `~/Downloads/preorder-form V3.html`. From the Nigerian preorder form she built. Test mode only.
- **Apple Developer Team ID `7RTTC5R7ZQ`** — set in `~/Downloads/App/Bethel/Bethel.xcodeproj/project.pbxproj` and `~/Downloads/App/Sleep/ShutdownApp.xcodeproj/project.pbxproj`. She IS enrolled in the Apple Developer Program.
- **Mapbox token** (account `naomi-ivie`) — she provided it directly during the build session.

**Not on disk anywhere:** Plaid (covered by Stripe Financial Connections), OpenAI, Vercel CLI token. Don't ask her to create these — there's an existing alternative for each.

When wiring a reused credential, leave a comment in code (or in the `.env.local`) noting which file it came from, so a future read of the codebase can trace it.
