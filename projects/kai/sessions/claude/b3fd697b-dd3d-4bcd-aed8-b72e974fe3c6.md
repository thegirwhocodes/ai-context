---
session_id: "b3fd697b-dd3d-4bcd-aed8-b72e974fe3c6"
source: "claude"
project: "kai"
started: "2026-07-23T17:04:09.330Z"
ended: "2026-07-23T22:27:36.950Z"
cwd: "-Users-naomiivie-kai"
thread_source: "user"
---

# Session b3fd697b-dd3d-4bcd-aed8-b72e974fe3c6

## Naomi · 2026-07-23T17:04:09.330Z

<ide_opened_file>The user opened the file /Users/naomiivie/kai/package-lock.json in the IDE. This may or may not be related to the current task.</ide_opened_file>
update me on Kai so far

## Claude · 2026-07-23T17:04:14.229Z

[Tool: Bash]

## Claude · 2026-07-23T17:04:14.847Z

[Tool: Bash]

## Claude · 2026-07-23T17:04:21.136Z

[Tool: Bash]

## Claude · 2026-07-23T17:04:33.113Z

## Kai status

**Where it stands** (last commit July 7, ~2 weeks ago; `main` is clean and in sync with GitHub, deployed at https://heykai.vercel.app):

- **Product**: Landing page + early-access waitlist shipped, plus the focus app at `/app`, pricing, testers, support, privacy/terms pages. Ambient backgrounds and branding polished.
- **Agent**: Kai's agent prompt was "leveled up" and the focus-music module completed in the latest feature commit. Energy/low-focus rationale is now data-grounded (no fake "energy dips" claims), and adaptive timing was cleaned up.
- **Integrations wired** (per `src/app/api/`): agent, calendar, email, Spotify, Alexa (with signature-env fix), web search with hardened fallback, transcribe + TTS (voice), recommendations, waitlist.
- **Business docs** in place: [BUSINESS_PLAN.md](docs/BUSINESS_PLAN.md), ads/testing, AI-music/Spotify, brand/visual research, competitive review, and an [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md).

**Likely next steps**: whatever's unfinished in the implementation plan — I can diff that doc against the code to give you a precise "done vs. remaining" list if you want.

## And me

Fresh session — Opus 4.8 (1M context) in your VSCode extension, rooted at `/Users/naomiivie/kai`, bypass-permissions on. My persistent memory for this project is empty so far (nothing saved from prior sessions), but I have your global config, the Kai AGENTS.md, and the ai-context recovery setup available. One housekeeping note: several claude.ai connectors (Gmail, Google Calendar, Drive, Zapier, Vercel MCP) need re-auth before I can use them, and the Vercel CLI has an update available (`npm i -g vercel@latest`).

Want the done-vs-remaining breakdown, or is there something specific to pick up?

## Naomi · 2026-07-23T17:07:59.766Z

how do we make sure this transcirpty gets saved to github, not her

## Claude · 2026-07-23T17:08:12.624Z

[Tool: Bash]

## Claude · 2026-07-23T17:08:13.217Z

[Tool: Bash]

## Claude · 2026-07-23T17:08:18.554Z

[Tool: Bash]

## Claude · 2026-07-23T17:08:23.304Z

[Tool: Bash]

## Claude · 2026-07-23T17:08:28.935Z

[Tool: Bash]

## Claude · 2026-07-23T17:08:30.087Z

[Tool: Bash]

## Claude · 2026-07-23T17:08:37.832Z

[Tool: Bash]

## Claude · 2026-07-23T17:08:38.992Z

[Tool: Bash]

## Claude · 2026-07-23T17:09:00.239Z

[Tool: Bash]

## Claude · 2026-07-23T17:09:43.245Z

Synced: commit `18ff54d` pushed, `main` clean and even with origin. This transcript (and every future one) lands on GitHub automatically every 30 minutes — worst case you lose the last half-hour of a session, and even that only until the next login-triggered sync.

## Naomi · 2026-07-23T17:42:03.593Z

I described I wanted the kai Agent to be genuinely smart - I can tlak to it and it tlaks back - right now the times forthe pomodoro is 20 minutes then it says somethign predeterministic and then 15 minute braak - it doesnt follow the true spirit of pomodoor no where for the user to set how long they want to use Kai pomodoro for

## Claude · 2026-07-23T17:42:08.855Z

[Tool: Bash]

## Claude · 2026-07-23T17:42:11.122Z

[Tool: Read]

## Claude · 2026-07-23T17:42:14.351Z

[Tool: Read]

## Claude · 2026-07-23T17:42:17.423Z

[Tool: Read]

## Claude · 2026-07-23T17:42:17.725Z

[Tool: Read]

## Claude · 2026-07-23T17:42:20.949Z

Now let me see what the user can actually control today (SettingsPanel) and how the conversational agent works.

## Claude · 2026-07-23T17:42:21.929Z

[Tool: Read]

## Claude · 2026-07-23T17:42:21.938Z

[Tool: Read]

## Claude · 2026-07-23T17:42:25.312Z

[Tool: Bash]

## Claude · 2026-07-23T17:42:27.940Z

[Tool: Read]

## Claude · 2026-07-23T17:42:28.400Z

[Tool: Read]

## Claude · 2026-07-23T17:46:47.528Z

[Tool: Read]

## Claude · 2026-07-23T17:46:50.633Z

[Tool: Read]

## Claude · 2026-07-23T17:47:27.448Z

I dug through the actual timing engine, settings, and the conversational agent. Here's what's really going on — and it matches your complaint precisely:

**Why it feels "predeterministic":** the block lengths and the little line Kai says are *not* the LLM thinking. [adaptive.ts](src/lib/adaptive.ts) computes the number with fixed math (baseline × time-of-day × recent ratings), then hands the agent a **template string** like `"Let's do a clean 20 minute focus block."` The Haiku agent just reads that back. So even though you can talk to Kai, the *timing decision and its explanation are canned*. That's the robotic feel.

**Why there's "nowhere to set how long":** [SettingsPanel](src/components/SettingsPanel.tsx) lets you set a *default per-block* focus length buried in settings — but there is **no concept of a total session / "lock-in" budget.** You can't say "I want to lock in for 2 hours" and have Kai lay out the pomodoro plan across it and show progress. The idle screen just offers "Start focus" → one adaptive block → break → repeat forever. No commitment, no finish line. That's the opposite of the Pomodoro spirit (commit to a chunk, work it in intervals, see it through).

Before I build, two decisions shape it — and they genuinely branch, so I want to get them right rather than guess:

## Claude · 2026-07-23T17:47:41.529Z

[Tool: AskUserQuestion]

## Claude · 2026-07-23T20:06:53.830Z

Clear. Lock-in budget is the headline, Flocus-style length pickers in settings, classic pomodoro as the controllable default with adaptive opt-in. Let me check the autopilot loop and the executeTool bridge before I plan the build.

## Claude · 2026-07-23T20:06:54.804Z

[Tool: Read]

## Claude · 2026-07-23T20:06:55.281Z

[Tool: Read]

## Claude · 2026-07-23T20:07:28.441Z

Good catch — let me hunt that "always 15" bug specifically before I build on top of it.

## Claude · 2026-07-23T20:07:30.560Z

[Tool: Bash]

## Claude · 2026-07-23T20:08:07.147Z

Found the root cause of the "always 15" bug. Let me confirm it and read the last pieces I need.

## Claude · 2026-07-23T20:08:08.119Z

[Tool: Read]

## Claude · 2026-07-23T20:08:09.199Z

[Tool: Read]

## Claude · 2026-07-23T20:08:09.204Z

[Tool: Read]

## Claude · 2026-07-23T20:09:33.238Z

Confirmed the bug. The state snapshot sent to the agent ([executeTool.ts:445-449](src/lib/agent/executeTool.ts#L445-L449)) includes focus lengths but **never the break lengths** — so when you talk to Kai about a break, Haiku has nothing to read and falls back to textbook Pomodoro's famous "15-minute break." That's the "always 15."

Here's my build plan, then I'll execute it:

## Claude · 2026-07-23T20:09:33.279Z

[Tool: ToolSearch]

## Claude · 2026-07-23T20:09:40.056Z

[Tool: TodoWrite]

## Claude · 2026-07-23T20:09:43.027Z

Now building. Starting with the data model.

## Claude · 2026-07-23T20:09:50.409Z

[Tool: Edit]

## Claude · 2026-07-23T20:09:59.283Z

[Tool: Edit]

## Claude · 2026-07-23T20:10:02.316Z

Now the lock-in plan generator:

## Claude · 2026-07-23T20:10:15.148Z

[Tool: Write]

## Claude · 2026-07-23T20:10:18.523Z

Now the classic (non-adaptive) break path in adaptive.ts:

## Claude · 2026-07-23T20:10:24.841Z

[Tool: Edit]

## Claude · 2026-07-23T20:10:32.139Z

[Tool: TodoWrite]

## Claude · 2026-07-23T20:11:25.493Z

Now the store — lock-in state, actions, and autopilot integration:

## Claude · 2026-07-23T20:11:30.654Z

[Tool: Edit]

## Claude · 2026-07-23T20:11:42.092Z

[Tool: Edit]

## Claude · 2026-07-23T20:11:45.260Z

Now the state initializer and the action implementations:

## Claude · 2026-07-23T20:11:46.902Z

[Tool: Edit]

## Claude · 2026-07-23T20:11:59.603Z

[Tool: Edit]

## Claude · 2026-07-23T20:12:03.274Z

Now make Skip advance the lock-in, and add the `beginPlannedBlock` helper:

## Claude · 2026-07-23T20:12:05.937Z

[Tool: Edit]

## Claude · 2026-07-23T20:12:18.037Z

[Tool: Edit]

## Claude · 2026-07-23T20:12:27.199Z

Now wire the autopilot to advance the lock-in instead of the open-ended treadmill:

## Claude · 2026-07-23T20:12:31.882Z

[Tool: Edit]

## Claude · 2026-07-23T20:12:57.386Z

Lock-in engine done. Now the UI components:

## Claude · 2026-07-23T20:13:15.145Z

[Tool: Write]

## Claude · 2026-07-23T20:13:38.115Z

Now integrate into the app page:

## Claude · 2026-07-23T20:13:40.297Z

[Tool: Edit]

## Claude · 2026-07-23T20:13:45.782Z

[Tool: Edit]

## Claude · 2026-07-23T20:13:51.217Z

[Tool: Edit]

## Claude · 2026-07-23T20:13:54.436Z

Now the idle-view render branch:

## Claude · 2026-07-23T20:14:02.757Z

[Tool: Edit]

## Claude · 2026-07-23T20:14:05.733Z

Now add the progress bar to the running view:

## Claude · 2026-07-23T20:14:08.042Z

[Tool: Edit]

## Claude · 2026-07-23T20:14:15.412Z

[Tool: TodoWrite]

## Claude · 2026-07-23T20:14:22.122Z

Now the Flocus-style settings pickers with an adaptive toggle:

## Claude · 2026-07-23T20:14:38.295Z

[Tool: Edit]

## Claude · 2026-07-23T20:14:41.481Z

Now add the `PresetRow` component:

## Claude · 2026-07-23T20:14:48.383Z

[Tool: Edit]

## Claude · 2026-07-23T20:14:55.604Z

[Tool: TodoWrite]

## Claude · 2026-07-23T20:15:01.271Z

Now the agent side. First the state snapshot the agent reads:

## Claude · 2026-07-23T20:15:05.241Z

[Tool: Edit]

## Claude · 2026-07-23T20:15:08.721Z

Now update `renderStateContext` and the system prompt:

## Claude · 2026-07-23T20:15:20.446Z

[Tool: Edit]

## Claude · 2026-07-23T20:15:31.451Z

[Tool: Edit]

## Claude · 2026-07-23T20:15:36.122Z

Now add the lock-in tools and their handlers:

## Claude · 2026-07-23T20:15:41.593Z

[Tool: Edit]

## Claude · 2026-07-23T20:15:50.783Z

[Tool: Edit]

## Claude · 2026-07-23T20:16:15.280Z

Let me fix a React-safety issue: a selector that returns a fresh object (`s.lockInProgress()`) breaks `useSyncExternalStore`. I'll make progress a pure function over stable state. Move the type and add a pure helper:

## Claude · 2026-07-23T20:16:18.199Z

[Tool: Edit]

## Claude · 2026-07-23T20:16:21.767Z

Add the pure progress helper to lockIn.ts:

## Claude · 2026-07-23T20:16:23.666Z

[Tool: Edit]

## Claude · 2026-07-23T20:16:32.995Z

[Tool: Edit]

## Claude · 2026-07-23T20:16:35.845Z

Now simplify the store to reuse the pure helper and import the type from types:

## Claude · 2026-07-23T20:16:40.141Z

[Tool: Edit]

## Claude · 2026-07-23T20:16:47.793Z

[Tool: Edit]

## Claude · 2026-07-23T20:16:50.755Z

Now update the LockIn components to use stable selectors + the pure helper:

## Claude · 2026-07-23T20:16:53.466Z

[Tool: Edit]

## Claude · 2026-07-23T20:17:02.728Z

[Tool: Edit]

## Claude · 2026-07-23T20:17:09.635Z

[Tool: Edit]

## Claude · 2026-07-23T20:17:14.762Z

Now lint and build:

## Claude · 2026-07-23T20:17:15.309Z

[Tool: Bash]

## Claude · 2026-07-23T20:17:20.421Z

[Tool: Bash]

## Claude · 2026-07-23T20:17:24.190Z

node_modules is stripped (lean laptop policy). Installing:

## Claude · 2026-07-23T20:17:24.564Z

[Tool: Bash]

## Claude · 2026-07-23T20:17:46.385Z

[Tool: Bash]

## Claude · 2026-07-23T20:17:56.039Z

Lint clean. Now build:

## Claude · 2026-07-23T20:17:56.332Z

[Tool: Bash]

## Claude · 2026-07-23T20:18:10.064Z

Build is green. Let me quickly sanity-check the plan generator with the real defaults before shipping:

## Claude · 2026-07-23T20:18:19.589Z

[Tool: Bash]

## Claude · 2026-07-23T20:18:29.668Z

Planner is exact and always ends focused. Marking the agent work done and shipping:

## Claude · 2026-07-23T20:18:33.703Z

[Tool: TodoWrite]

## Claude · 2026-07-23T20:18:36.529Z

[Tool: Bash]

## Claude · 2026-07-23T20:18:41.127Z

[Tool: Bash]

## Claude · 2026-07-23T20:18:44.347Z

Legitimate lockfile sync (name + resolutions). Committing and pushing:

## Claude · 2026-07-23T20:18:50.324Z

[Tool: Bash]

## Claude · 2026-07-23T20:18:54.565Z

Pushed. Now deploy to Vercel production (this is a user-facing feature you asked me to build):

## Claude · 2026-07-23T20:18:55.283Z

[Tool: Bash]

## Claude · 2026-07-23T20:20:09.356Z

[Tool: Bash]

## Claude · 2026-07-23T20:20:16.106Z

[Tool: TodoWrite]

## Claude · 2026-07-23T20:20:23.521Z

Shipped and live (200 on https://heykai.vercel.app/app). Let me record the product decision so future sessions don't undo it:

## Claude · 2026-07-23T20:20:32.982Z

[Tool: Write]

## Claude · 2026-07-23T20:20:37.243Z

[Tool: Bash]

## Claude · 2026-07-23T20:20:40.771Z

[Tool: Write]

## Claude · 2026-07-23T20:20:54.869Z

Done — built, verified, shipped to production.

## What changed

**1. Fixed the "always 15-minute break" bug (root cause found).** The agent's state snapshot sent focus lengths but *never break lengths*, so Haiku fell back to textbook Pomodoro's famous 15. Now the snapshot carries every block length, the long-break cadence, the mode, and lock-in progress — and the prompt forbids stating any duration it can't see. Kai will now say your actual 5.

**2. Lock-in budget — the headline feature.** On the idle screen there's now **"How long are we locking in?"** with 25m / 50m / 90m / 2h chips + custom. You commit to a total, and Kai lays out the whole Pomodoro plan across it (focus + breaks, **always ending focused**, budget honored exactly), runs it hands-free, and shows a live progress bar (`40 / 120 min · block 2 of 4`). By voice: *"lock in for two hours"* → Kai builds and starts the plan. Verified the planner hits the exact budget every time:
- `50min → 25 · 5 · 20`
- `120min → 25·5·25·5·25·5·30`
- `180min → …·long 15·…` (long break lands on the 4th block)

**3. Classic Pomodoro is now the default, adaptive is opt-in.** Block lengths use *your* exact settings — predictable, controllable — instead of the adaptive math that produced the "predeterministic" feel. Adaptive ("let Kai tune it") is a toggle in Settings.

**4. Flocus-style length pickers** in Settings — clickable focus/break chips + custom, instead of buried number fields.

Live at **https://heykai.vercel.app/app** (pushed to `main`, deployed to production). One thing worth a look in the browser when you can: the idle screen now leads with the lock-in card, with "Quick focus" / "Take a break" demoted to secondary — tell me if you want lock-in to take over the whole hero instead.

## Naomi · 2026-07-23T21:30:29.205Z

no undo - I meant like a settings section

## Claude · 2026-07-23T21:30:52.367Z

Nothing undone — everything I built stays. And yes, the length picker *is* a settings section already:

- **Settings → Timing** now has clickable Flocus-style chips for **Focus** (15/25/30/45/50/60/90), **Short break** (3/5/10/15), and **Long break** (10/15/20/30), each with a "custom" option. That's the "place in settings where users click and choose length of focus and break" you described.
- The **lock-in budget** is the separate headline feature on the idle screen.

Both live, both shipped. No changes needed unless you want me to tweak the presets or move something.

## Naomi · 2026-07-23T21:31:57.167Z

where do I find settings

## Claude · 2026-07-23T21:32:02.546Z

[Tool: Read]

## Claude · 2026-07-23T21:32:08.537Z

In the app at **https://heykai.vercel.app/app**, look at the **bottom-right corner** — there's a row of small round buttons (the dock). The settings one is the **✦ ("Customize")** button, the last icon before the fullscreen ⛶ button. Click it and the panel opens at the bottom-left with the **Timing** section (the focus/break length chips) and the adaptive toggle.

## Naomi · 2026-07-23T21:34:09.628Z

is the random chooser proken? it qalways so "lets' do 20miutes, a touch shorter to stay fresh"
actually you tell me veryhting people do before shipping a prodcut - do deep research - and test kai on that - run a bynch of tests

## Claude · 2026-07-23T21:34:31.751Z

Good catch — that's not randomness, it's a real bug. Let me confirm the root cause and check the test setup.

## Claude · 2026-07-23T21:34:32.173Z

[Tool: Read]

## Claude · 2026-07-23T21:35:11.198Z

Confirmed on both counts. Here's the real bug:

That "let's do 20 minutes, a touch shorter to stay fresh" is the **adaptive engine's** line. When I switched the default to classic, it only affected *new* users — your browser's saved settings still have `adaptive: true` (the old default), and zustand's merge keeps your saved value. Since the adaptive toggle never existed in the old UI, **nobody** turned it on deliberately, so it's safe to migrate everyone off. And there are **zero automated tests** in this repo. Let me fix both, properly.

## Claude · 2026-07-23T21:35:15.235Z

[Tool: TodoWrite]

## Claude · 2026-07-23T21:35:18.302Z

[Tool: Read]

## Claude · 2026-07-23T21:35:21.870Z

[Tool: Read]

## Claude · 2026-07-23T21:35:30.275Z

[Tool: Edit]

## Claude · 2026-07-23T21:35:37.948Z

[Tool: Edit]

## Claude · 2026-07-23T21:35:40.875Z

Now warm up the classic focus rationale:

## Claude · 2026-07-23T21:35:43.870Z

[Tool: Edit]

## Claude · 2026-07-23T21:35:50.153Z

[Tool: TodoWrite]

## Claude · 2026-07-23T21:35:52.422Z

Now set up a real test suite. Installing vitest:

## Claude · 2026-07-23T21:35:53.026Z

[Tool: Bash]

## Claude · 2026-07-23T21:36:05.891Z

[Tool: Edit]

## Claude · 2026-07-23T21:36:19.260Z

Now the test suite — covering the timing engine, the lock-in planner, and the migration:

## Claude · 2026-07-23T21:36:36.479Z

[Tool: Write]

## Claude · 2026-07-23T21:36:53.440Z

[Tool: Write]

## Claude · 2026-07-23T21:37:01.239Z

[Tool: Write]

## Claude · 2026-07-23T21:37:04.625Z

[Tool: Bash]

## Claude · 2026-07-23T21:37:10.995Z

Need to teach vitest the `@/` path alias. Adding a config:

## Claude · 2026-07-23T21:37:12.262Z

[Tool: Write]

## Claude · 2026-07-23T21:37:16.140Z

[Tool: Bash]

## Claude · 2026-07-23T21:37:30.327Z

All 22 tests pass. Now lint + build to confirm nothing regressed:

## Claude · 2026-07-23T21:37:31.380Z

[Tool: Bash]

## Claude · 2026-07-23T21:37:59.776Z

[Tool: Bash]

## Claude · 2026-07-23T21:38:31.530Z

Type mismatch — the migrate return needs the persisted shape. Cast it (merge fills defaults at runtime):

## Claude · 2026-07-23T21:38:34.011Z

[Tool: Edit]

## Claude · 2026-07-23T21:38:40.209Z

[Tool: Bash]

## Claude · 2026-07-23T21:39:21.875Z

Build green. Re-running the full suite to be sure the type-fix didn't disturb anything:

## Claude · 2026-07-23T21:39:22.501Z

[Tool: Bash]

## Claude · 2026-07-23T21:39:33.513Z

Now committing, pushing, and deploying the fixes:

## Claude · 2026-07-23T21:39:38.850Z

[Tool: Bash]

## Claude · 2026-07-23T21:39:44.526Z

[Tool: Bash]

## Claude · 2026-07-23T21:41:06.677Z

[Tool: TodoWrite]

## Claude · 2026-07-23T21:41:27.369Z

Fixed and shipped. First, the direct answer:

**The "always 20 min, a touch shorter" was a real bug, not randomness.** Your browser had `adaptive: true` saved from the old default, and my classic-default switch only hit *new* users — the saved value stuck. There was never an adaptive toggle in the old UI, so nobody chose it on purpose. A one-time migration now flips it off. **Hard-refresh https://heykai.vercel.app/app** (Cmd-Shift-R) and you'll get clean "Let's do a 25 minute focus block" with your exact settings. It's live now.

---

## What people do before shipping — and where Kai stands

I actually ran this against Kai, didn't just describe it.

| Pre-ship discipline | What it means | Kai status |
|---|---|---|
| **Automated unit tests** | Lock the core logic so bugs can't silently return | ✅ **Added — 22 tests, all passing.** Covers the lock-in planner + the exact bugs you hit |
| **Regression tests** | A test that fails if a fixed bug comes back | ✅ One test asserts a short break is *exactly your 5 min, never "15"* |
| **Typecheck + lint** | Catch broken code before users do | ✅ `npm run build` + `eslint` both clean |
| **Data migrations** | Existing users' saved state upgrades safely | ✅ Added + tested (this was your bug) |
| **Manual smoke test** | A human clicks the real flows | ⚠️ Partial — logic verified, but I haven't driven the live UI in a browser |
| **Cross-browser / device** | Chrome, Safari, mobile | ❌ Not done — voice/"Hey Kai" is especially browser-dependent |
| **End-to-end tests** | Simulate a full user journey (Playwright) | ❌ None yet |
| **Error monitoring** | Sentry catches crashes in production | ❌ Not wired (your global config wants this) |
| **Analytics** | See what users actually do | ❌ Not wired |

**What the 22 tests actually prove:** every lock-in budget (5 min → 4 hrs) fills exactly, always ends on a focus block, never stacks two breaks, and drops a long break only on the right cadence — plus classic vs. adaptive block decisions stay in bounds and snap to whole minutes (no rogue 24-min blocks). Run them yourself anytime with `npm test`.

**The honest gaps, ranked by what I'd do next:**
1. **Sentry** — your own rules call for it; right now a production crash is invisible.
2. **A browser smoke/E2E pass** — I can drive the real app (start a lock-in, run a block, open settings, talk to Kai) and screenshot each step. I have a tool for exactly this.
3. **Beta testers** — your `docs/testers` scaffold exists; real users surface things tests never will.

Want me to knock out #1 (wire Sentry) and #2 (run a real browser walkthrough with screenshots) next?

## Naomi · 2026-07-23T22:19:21.100Z

do deep research into what software coders/ entreprenerus do to test a product nefore releasing fully

## Claude · 2026-07-23T22:19:42.366Z

Good call — this should be grounded in current practice, not memory. Let me first check what research already exists in the repo, then go deep on the web.

## Claude · 2026-07-23T22:19:43.945Z

[Tool: Bash]

## Claude · 2026-07-23T22:20:02.442Z

The repo's testing doc is all beta-recruitment and ads — nothing on the engineering QA + product-validation playbook you're asking about. I'll research that properly. Spinning up parallel researchers across the two halves (how *coders* test, how *founders* validate) plus tooling specifics:

## Claude · 2026-07-23T22:20:15.132Z

[Tool: Agent]

## Claude · 2026-07-23T22:20:28.893Z

[Tool: Agent]

## Claude · 2026-07-23T22:20:36.037Z

Two researchers are running in the background (engineering QA + founder validation). I'll synthesize their findings into a repo doc when they finish. Give it a few minutes — I'll be notified automatically.

## Claude · 2026-07-23T22:20:40.552Z

[Tool: TodoWrite]

## Claude · 2026-07-23T22:20:47.094Z

Both research agents are underway. I'll pull their findings together into a `docs/PRE_RELEASE_TESTING_RESEARCH.md` — a full pre-release testing playbook (engineering QA + founder validation) mapped to Kai's actual state — as soon as they report back.

## Naomi · 2026-07-23T22:24:09.292Z

<task-notification>
<task-id>aa6ec819ca8e90cf4</task-id>
<tool-use-id>toolu_01N1K3tW1mZgVUaeHjFqoGWv</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-naomiivie-kai/b3fd697b-dd3d-4bcd-aed8-b72e974fe3c6/tasks/aa6ec819ca8e90cf4.output</output-file>
<status>completed</status>
<summary>Agent "Research engineering QA practices" finished</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
<result># How Professional Engineering Teams Test Before Full Release — A Deep Reference (2024–2026)

Scoped for a solo-founder Next.js/React app (Kai) on Vercel. Each section covers **what it is, why it matters, when in the lifecycle it runs, concrete tools**, and a **Solo verdict** (Essential / Worth it / Overkill for now).

---

## 0. The mental model: shift-left + the release funnel

Professional teams don't "test at the end." They run a graduated funnel where each stage is cheaper to fail than the next: static checks (ms) → unit tests (ms–s) → integration (s) → E2E (min) → preview/staging smoke → canary/percentage rollout → full release, with observability catching whatever leaked through. The economic logic — cheaper tests as the default, expensive ones reserved for the flows that most need them — is the core of Martin Fowler's test pyramid ([martinfowler.com/articles/practical-test-pyramid.html](https://martinfowler.com/articles/practical-test-pyramid.html)).

---

## 1. The Testing Pyramid (unit / integration / E2E)

**What.** A balanced portfolio of automated tests at different granularities. Fowler's two rules: *"Write tests with different granularity"* and *"The more high-level you get, the fewer tests you should have."* Avoid the inverted "ice-cream cone" (mostly slow UI tests). ([martinfowler.com](https://martinfowler.com/articles/practical-test-pyramid.html))

| Layer | What it catches | Speed | Share (rough) | Tools |
|---|---|---|---|---|
| **Unit** | Logic in a single function/component in isolation (collaborators mocked) | ms | ~70% | **Vitest**, Jest, React Testing Library |
| **Integration** | One integration point at a time — component ↔ DB/API/route — with test doubles for others | s | ~20% | Vitest + MSW, Supertest, Testcontainers |
| **E2E / broad-stack** | Full user journeys through the real UI + API + data | min | ~10% | **Playwright**, Cypress |

**Key guidance.** *"Push your tests as far down the pyramid as you can"* — if a lower layer can verify it, do it there to keep the suite fast and stable ([martinfowler.com](https://martinfowler.com/articles/practical-test-pyramid.html)).

**React specifics (Kent C. Dodds).** *"The more your tests resemble the way your software is used, the more confidence they can give you."* Test behavior, **not implementation details** (state vars, handlers) — query the DOM by label/role/text as a user would ([Testing Implementation Details](https://kentcdodds.com/blog/testing-implementation-details), [Common mistakes with RTL](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)).

**Google's size model** (an alternative axis to the pyramid): **Small** (≤60s, no network/DB/filesystem, single process), **Medium** (≤300s, localhost only), **Large** (≤900s, unrestricted). Smaller = faster + less flaky ([Google Testing Blog: Test Sizes](https://testing.googleblog.com/2010/12/test-sizes.html); [SWE at Google, ch.14](https://abseil.io/resources/swe-book/html/ch14.html)).

**When.** Unit + integration run locally on save and on every PR; E2E on PR and/or against the preview deploy before merge.

**Solo verdict.** **Essential** — but tilt the ratio to your risk. For Kai: unit-test the pomodoro timing math, calendar-spacing/reschedule logic, and any AI-response parsing (these are your correctness core and match AGENTS.md's "clean and explainable timing" rule). A handful of Playwright E2E flows (start a focus session, sign in, connect calendar). Don't chase a giant integration layer solo.

---

## 2. Regression, Snapshot &amp; Contract testing

**Regression testing.** Re-running existing tests to confirm new changes didn't break old behavior. In practice this *is* your CI suite — the value compounds: every bug you fix should get a test so it can never silently return. **Essential** (it's emergent, not a separate tool).

**Snapshot testing.** Serialize rendered output; fail if it changes. Powerful but abused. Dodds/RTL guidance: **keep snapshots small and focused (~20–30 lines), verifiable by a human**; prefer explicit assertions for anything larger — big snapshots get rubber-stamped and rot ([Snapshot testing in RTL](https://thesametech.com/snapshot-testing-in-rtl/); [dev.to snapshot in RTL](https://dev.to/srshifu/snapshot-testing-in-react-testing-library-4gkc)). **Worth it sparingly** for small presentational components; overkill as a primary strategy.

**Contract testing.** Consumer-Driven Contracts (CDC): the consumer declares expectations of an API, the provider verifies them in CI — catches breaking API changes without slow full-integration runs. Tool: **Pact** ([martinfowler.com — CDC section](https://martinfowler.com/articles/practical-test-pyramid.html)). **Overkill for a solo founder** with one codebase; it earns its keep across teams/microservices. If Kai grows a separate mobile/Alexa client hitting your API, revisit.

---

## 3. CI/CD Quality Gates (what runs on every PR)

**What.** Automated checks that must pass before code merges, enforced by **branch protection / required status checks**. PRs cannot merge unless required workflows pass — a hard gate against broken code reaching `main` ([GitHub branch protection guide](https://oneuptime.com/blog/post/2026-01-28-github-actions-branch-protection/view); [status checks guide](https://oneuptime.com/blog/post/2026-01-26-status-checks-github-actions/view)).

**Standard gate on every PR:** typecheck → lint → unit/integration tests → build → (optionally) E2E on preview + coverage threshold. Layer in required reviews and a CODEOWNERS file for team defense-in-depth ([Microsoft Engineering Playbook](https://microsoft.github.io/code-with-engineering-playbook/agile-development/branching-and-cicd/)).

**Gotcha.** Branch protection matches the **exact job name string**; reusable/nested workflows can report a different name than configured, silently un-gating checks ([devActivity](https://devactivity.com/posts/apps-tools/unlocking-cicd-flow-resolving-github-actions-required-status-check-mismatches/)).

**When.** On every push/PR, pre-merge.

**Tools.** GitHub Actions (native for a GitHub repo), plus Vercel's own build check.

**Solo verdict.** **Essential — and cheap.** Even solo, protect `main` and require: `tsc --noEmit`, `next lint`, `vitest run`, `next build`. The build gate alone catches most "works on my machine" breakage. A green PR you review yourself still beats pushing straight to `main`.

---

## 4. Test Coverage — meaning, targets, limits

**What.** % of code executed by tests (line/branch/statement/function). A *proxy*, not a goal.

**Realistic targets.** Google's median is ~**78%**; 75th pct ~85%, 90th pct ~90%; **75% is considered "commendable"** ([Code Coverage at Google, ResearchGate](https://www.researchgate.net/publication/334259697_Code_Coverage_at_Google)). Mature orgs sit **70–85% line coverage** ([Sonar](https://www.sonarsource.com/resources/library/code-coverage-unit-tests/); [em-tools benchmarks](https://www.em-tools.io/engineering-metrics/code-coverage)).

**Limits.** Beyond ~85%, cost rises sharply for shrinking benefit; 100% forces brittle, superficial tests that raise coverage without raising confidence ([NDepend: against 100%](https://blog.ndepend.com/aim-100-percent-test-coverage/)). Better: **risk-tiered** — auth/payments/data-integrity ≥90%, UI/admin 60–70% ([em-tools](https://www.em-tools.io/engineering-metrics/code-coverage)). Coverage tells you what *ran*, never whether assertions were meaningful.

**Tools.** Vitest/Jest `--coverage` (built on c8/istanbul); Codecov for PR reporting.

**Solo verdict.** **Worth it, un-obsessively.** Track coverage, don't gate hard on a high number. Put your assertions where a bug costs Kai users trust: timer accuracy, calendar mutations, billing if/when added. Ignore coverage on glue/UI scaffolding.

---

## 5. Static analysis, type safety, linting, dependency/security scanning

**What &amp; tools.**
- **Type safety** — TypeScript `strict` + `tsc --noEmit` in CI. Your cheapest, highest-leverage "test." **Essential.**
- **Linting** — ESLint (`next lint`) + Prettier for consistency and a class of bug prevention. **Essential.**
- **SAST** — static analysis for vuln patterns: **CodeQL** (GitHub code scanning). Note ~34% false-positive rate in one study — triage, don't trust blindly ([GHAS overview](https://www.systemshardening.com/articles/cicd/github-advanced-security/)).
- **Dependency scanning (SCA)** — **Dependabot** auto-PRs for vulnerable direct deps (transitive ones alerted but not auto-fixed); `npm audit` (noisy on dev-only deps) ([GHAS at scale](https://www.systemshardening.com/articles/cicd/github-advanced-security/)).
- **Secret scanning** — detects committed API keys/tokens; **free on public repos** ([GHAS](https://www.microsoft.com/en-us/securityengineering/sdl/ghas)).

**When.** Type/lint on every save + PR; Dependabot on a schedule; secret scanning continuously.

**Solo verdict.** **Essential (the free tier).** For Kai: TS strict, ESLint, **turn on Dependabot + GitHub secret scanning + push protection** (free, one click) — critical given Kai handles Google Calendar/Gmail/Spotify OAuth tokens. CodeQL is nice-to-have; enable it (free-ish for public repos), triage findings, don't let false positives block you.

---

## 6. Pre-production environments: staging, previews, smoke tests

**What.**
- **Preview / ephemeral environments** — per-PR, auto-deployed, unique URL, torn down on merge. **Vercel does this natively** on every push — production-like infra, catches deploy/config bugs localhost can't ([Vercel Academy: Preview Deployments](https://vercel.com/academy/svelte-on-vercel/preview-deployments); [Autonoma: Vercel preview testing](https://getautonoma.com/blog/vercel-preview-deployments)).
- **Staging** — one long-lived shared QA environment. Preview deploys largely *replace* the need for classic staging for frontend work ([Autonoma: staging vs preview](https://getautonoma.com/blog/staging-environment-vs-preview-environment)).
- **Smoke tests** — a tiny, fast "is it fundamentally alive?" suite (home page loads, auth works, timer starts) run against the deployed URL before promoting.

**Ideal stack per PR:** visual review + CI checks + live E2E against the preview URL ([Autonoma: E2E on preview](https://getautonoma.com/blog/e2e-testing-preview-environments-pipeline)).

**When.** Preview on every push; smoke test post-deploy, pre-promote-to-prod.

**Solo verdict.** **Essential — and mostly free/automatic on Vercel.** You already get previews. Add a 3–5 test Playwright smoke suite run against the preview URL. You likely **don't need a separate staging environment** — preview + a smoke check on production after promotion is enough solo.

---

## 7. Progressive delivery: flags, canary, staged rollout, blue-green, rollback, dark launch

**What.** Decouple *deploy* from *release*; expose changes gradually to subsets and roll back instantly.
- **Feature flags** — ship code dark, toggle on for %/segments. Per LaunchDarkly's 2024 report, **89% of engineering orgs use feature flags**; DORA links them to faster lead times ([LaunchDarkly: What is Progressive Delivery](https://launchdarkly.com/blog/what-is-progressive-delivery-all-about/)).
- **Canary** — release to a small % (e.g. 1→5→20→100), watch error/latency, then widen.
- **Staged/percentage rollout** — same idea, e.g. Google Play's 1%→5%→20%→100% ([Play staged rollout](https://primetestlab.com/blog/google-play-internal-vs-closed-vs-open-testing)).
- **Blue-green** — two identical envs, flip traffic; instant rollback by flipping back.
- **Dark launch** — run new code in prod without exposing output (e.g. shadow traffic).
- **Rollback** — revert to the last-good version fast.

**When.** At release time, post-merge.

**Tools.** LaunchDarkly, Flagsmith, Unleash, PostHog feature flags; Vercel **Instant Rollback** (one-click revert to prior production deploy); Vercel **Rolling Releases** for percentage traffic shifting.

**Solo verdict.** **Mostly Overkill — with two Essential exceptions.** Skip canary infra, blue-green, dark launches solo. But: (1) **use Vercel's instant rollback** — free, and your real safety net; (2) **a lightweight feature-flag mechanism** (env var, PostHog free tier, or a simple flag) so you can ship Kai features dark and un-break users without a redeploy. Simple flags, not a LaunchDarkly contract.

---

## 8. Dogfooding / internal alpha / beta tracks

**What.** Use your own product daily (dogfooding); then graduated tester rings. Mobile has formal tracks:
- **TestFlight (iOS)** — internal (≤100), closed (email-invited, up to ~10K), open (public beta) ([MWM: TestFlight](https://mwm.ai/glossary/testflight)).
- **Play Console (Android)** — internal → closed → open → production, all in one interface, with **promote-without-re-upload** between tracks ([Play Console Help](https://support.google.com/googleplay/android-developer/answer/9845334?hl=en); [primetestlab](https://primetestlab.com/blog/google-play-internal-vs-closed-vs-open-testing)).

**When.** After internal QA, before/at public launch.

**Solo verdict.** **Dogfooding = Essential** (you're building a focus app — use it for your own focus sessions; it surfaces the timing/UX issues AGENTS.md cares about). Formal TestFlight/Play tracks are **N/A** for a Vercel web app — the web equivalent is a **private beta via a waitlist + feature-flagged access + preview links** (Kai already has an early-access waitlist per the git log). Worth it: a small closed web-beta group before you promote big features to all users.

---

## 9. Load / performance / stress testing + chaos

**What.**
- **Load testing** — simulate concurrent users; find the breaking point. **k6** (Grafana; k6 1.0 shipped May 2025, JS scripts, clean CI integration) is the modern default ([k6 guide](https://agmazon.com/blog/articles/technology/202602/k6-load-testing-complete-guide-en.html); [Grafana: k6 vs Lighthouse](https://grafana.com/blog/2023/06/01/web-performance-testing-compare-grafana-k6-browser-vs.-google-lighthouse/)).
- **Frontend perf / Core Web Vitals** — **Lighthouse / Lighthouse CI**; measure **LCP, INP, CLS** (INP replaced FID as an official Core Web Vital in **March 2024**) ([Grafana blog](https://grafana.com/blog/2023/06/01/web-performance-testing-compare-grafana-k6-browser-vs.-google-lighthouse/)).
- **Chaos engineering** — deliberately inject failure (kill instances, add latency) to prove resilience. LitmusChaos + k6 for load-chaos ([LitmusChaos + k6](https://dev.to/litmus-chaos/introduction-to-k6-load-chaos-in-litmuschaos-4l2k)).

**When.** Perf budgets in CI (Lighthouse CI on PRs); load tests before anticipated traffic spikes / launch; chaos in mature production orgs.

**Solo verdict.** **Lighthouse CI = Worth it** (Core Web Vitals directly affect Kai's SEO and the "calm, fast on first load" bar in AGENTS.md — cheap to add on main pages). **Load testing = Overkill until you have real traffic** — Vercel serverless autoscales; a quick k6 run before a launch push is enough. **Chaos engineering = Overkill** for a solo Vercel app.

---

## 10. Security testing

**What &amp; tools.**
- **Dependency audits** — Dependabot + `npm audit` (see §5).
- **Secret scanning + push protection** — block committed credentials.
- **SAST/DAST** — CodeQL (static); DAST scans the running app.
- **OWASP** — the **OWASP Top 10** is the baseline vuln checklist (injection, broken auth, XSS, SSRF, etc.); OWASP ZAP for DAST.
- **Pen testing** — manual/third-party adversarial testing, typically pre-launch for apps handling sensitive data ([CI/CD security: SAST/DAST/secrets](https://zeonedge.com/blog/cicd-pipeline-security-sast-dast-secrets-scanning-dependency-audit)).

**When.** Scanning continuously/in CI; pen test before a major launch or when handling payments/PII.

**Solo verdict.** **Baseline = Essential.** Kai holds OAuth tokens for Google Calendar/Gmail and Spotify — treat that seriously: secret scanning + push protection ON, Dependabot ON, review the OWASP Top 10 against your API routes (authz on every route that touches a user's calendar/email, no tokens in client bundles/logs). **Professional pen test = Overkill now**, but revisit before charging money or scaling users. Store secrets only in Vercel env vars (never committed) — aligns with your global CLAUDE.md secret-handling rules.

---

## 11. Observability as a release safety net

**What.** You can't test everything pre-release; instrument prod so you *see* problems fast.
- **Error monitoring** — **Sentry**: exceptions with stack traces, aggregation, **release health** (crash-free sessions/users per release), source maps for Next.js ([Sentry guide 2025](https://www.baytechconsulting.com/blog/sentry-io-comprehensive-guide-2025)). Your global CLAUDE.md explicitly says **"use Sentry to debug."**
- **Logging / tracing** — structured logs; OpenTelemetry is now the default for traces/metrics/logs ([Observability 2025](https://bixtech.ai/observability-in-2025-how-sentry-grafana-and-opentelemetry-are-shaping-the-next-era-of-reliable-software/)).
- **SLOs / error budgets** — define reliability targets (e.g. 99.9% success), alert on **SLO burn**, not infra noise (which causes pager fatigue); Sentry now supports error-budget tracking ([Observability 2025](https://bixtech.ai/observability-in-2025-how-sentry-grafana-and-opentelemetry-are-shaping-the-next-era-of-reliable-software/)).
- **Alerting** — route real regressions somewhere you'll see them.

**When.** Wired before launch; watched *especially* during and after each release (canary/rollout decisions read these signals).

**Tools.** Sentry, Vercel Analytics + Speed Insights, Vercel Log Drains, PostHog (product analytics).

**Solo verdict.** **Essential — arguably your single highest-value non-test safety net solo.** You don't have a QA team, so production telemetry *is* your QA. For Kai: wire **Sentry** (frontend + API routes, with release tagging so you know which deploy broke), plus **Vercel Analytics/Speed Insights** for Core Web Vitals. Skip formal SLO/error-budget machinery for now — just alert on error spikes.

---

## 12. Accessibility testing

**What.** Verify against **WCAG 2.2 AA**. Automated tools (**axe-core**) catch ~**up to 50%** of issues; roughly **30% of WCAG criteria are machine-testable** — the rest need human judgment (keyboard nav, screen-reader, focus order) ([Playwright a11y docs](https://playwright.dev/docs/accessibility-testing); [rishikc: axe + Playwright + Actions](https://rishikc.com/articles/accessibility-testing-ci-integration/)).

**Tools.** `@axe-core/playwright` (E2E scans), `jest-axe` (component-level), Lighthouse a11y audit, plus manual keyboard/screen-reader passes.

**When.** In CI (fail build on new violations) + manual spot-checks on key screens.

**Solo verdict.** **Worth it, lightweight.** Add one `@axe-core/playwright` scan over Kai's main screens and the Lighthouse a11y score — minutes to set up, and it protects the "clear on mobile and desktop, no overlapping text" bar in AGENTS.md. Do one manual keyboard pass on the timer + voice UI. Full manual audits are overkill pre-scale.

---

## 13. Manual / exploratory testing + release checklist (go/no-go)

**What.** Automated tests confirm known behavior; **exploratory testing** finds the unknown-unknowns by a human poking at the product with intent. A **release checklist / go-no-go** is the final gate — production-readiness (from Google's SRE book) covering security, reliability, rollback, monitoring, and migrations ([Cortex release checklist](https://www.cortex.io/post/software-release-checklist); [DX production-readiness](https://getdx.com/blog/production-readiness-checklist/)).

**Typical go/no-go items:** all CI checks green; preview smoke-tested; DB migrations tested **and reversible**; feature flags/config reviewed; monitoring + alerts live; **rollback plan** defined; owner available to watch post-deploy ([Port checklist](https://www.port.io/blog/production-readiness-checklist-ensuring-smooth-deployments); [IPM go/no-go](https://instituteprojectmanagement.com/blog/go-no-go-production-readiness-checklist/)).

**Solo verdict.** **Essential, but keep it a one-pager.** You are the whole go/no-go committee — so make it a literal checklist you run before promoting Kai to production, so you don't forget the boring things at 1am.

---

## Recommended Kai testing stack (solo-founder, right-sized)

**Do now (Essential, low cost):**
1. **Static gate:** TypeScript `strict` + `tsc --noEmit`, ESLint (`next lint`), Prettier.
2. **Branch protection on `main`** requiring: typecheck, lint, `vitest run`, `next build`.
3. **Unit tests** on the correctness core: pomodoro timing/session math, calendar reschedule-with-spacing logic, AI-response/tool-output parsing.
4. **3–5 Playwright E2E/smoke tests** (sign in, start focus session, connect calendar) run against the **Vercel preview URL** per PR, and against prod after promotion.
5. **Security baseline:** Dependabot + GitHub secret scanning + **push protection** ON; audit API routes against OWASP Top 10 (authz on every calendar/email route; no tokens client-side/in logs).
6. **Observability:** **Sentry** (frontend + API, [REDACTED:sensitive-label]) + Vercel Analytics/Speed Insights.
7. **Vercel Instant Rollback** as your rollback plan; a simple **feature-flag** mechanism to ship dark.
8. A **one-page go/no-go checklist** before every production promote.

**Add opportunistically (Worth it):**
- Coverage reporting (informational, risk-tiered — not a hard high-number gate).
- **Lighthouse CI** for Core Web Vitals on main pages.
- One **axe-core** a11y scan + a manual keyboard pass.
- A small **closed web beta** (waitlist + flagged access) before big feature launches.
- Snapshot tests only for a few small presentational components.

**Skip for now (Overkill solo):**
- Contract testing (Pact), dedicated staging environment, canary/blue-green infrastructure, k6 load testing at scale, chaos engineering, formal SLO/error-budget tooling, third-party pen testing, TestFlight/Play tracks (web app). Revisit each when Kai has paying users, real traffic, or multiple clients.

---

### Primary / authoritative sources
- Martin Fowler — The Practical Test Pyramid: https://martinfowler.com/articles/practical-test-pyramid.html
- Google Testing Blog — Test Sizes: https://testing.googleblog.com/2010/12/test-sizes.html
- Software Engineering at Google, Ch.14 (Larger Testing): https://abseil.io/resources/swe-book/html/ch14.html
- Kent C. Dodds — Testing Implementation Details: https://kentcdodds.com/blog/testing-implementation-details
- Kent C. Dodds — Common Mistakes with React Testing Library: https://kentcdodds.com/blog/common-mistakes-with-react-testing-library
- Playwright — Accessibility Testing: https://playwright.dev/docs/accessibility-testing
- Microsoft Engineering Playbook — Branching &amp; CI/CD: https://microsoft.github.io/code-with-engineering-playbook/agile-development/branching-and-cicd/
- LaunchDarkly — What Is Progressive Delivery: https://launchdarkly.com/blog/what-is-progressive-delivery-all-about/
- Code Coverage at Google (paper): https://www.researchgate.net/publication/334259697_Code_Coverage_at_Google
- Sonar — Code Coverage with Effective Unit Tests: https://www.sonarsource.com/resources/library/code-coverage-unit-tests/
- GitHub Advanced Security (Secret Scanning, CodeQL, Dependabot): https://www.systemshardening.com/articles/cicd/github-advanced-security/
- Grafana — k6 browser vs Lighthouse (Web Vitals): https://grafana.com/blog/2023/06/01/web-performance-testing-compare-grafana-k6-browser-vs.-google-lighthouse/
- Vercel Academy — Preview Deployments: https://vercel.com/academy/svelte-on-vercel/preview-deployments
- Google Play — Set up open/closed/internal test: https://support.google.com/googleplay/android-developer/answer/9845334?hl=en
- Sentry Comprehensive Guide 2025: https://www.baytechconsulting.com/blog/sentry-io-comprehensive-guide-2025
- Cortex — Software Release Checklist: https://www.cortex.io/post/software-release-checklist
- DX — Production Readiness Checklist: https://getdx.com/blog/production-readiness-checklist/

Note: several supporting stats above (e.g. LaunchDarkly's "89%", DORA lead-time claims, the 30%/50% axe figures) come from secondary summaries of primary reports; treat exact percentages as directional and verify against the original report before quoting them in Kai's business/marketing docs.</result>
<usage><subagent_tokens>43304</subagent_tokens><tool_uses>15</tool_uses><duration_ms>232378</duration_ms></usage>
</task-notification>

## Claude · 2026-07-23T22:24:30.868Z

Engineering QA research is in and it's thorough. The founder-validation researcher is still running — I'll synthesize both together once it lands.

## Claude · 2026-07-23T22:24:32.909Z

[Tool: TodoWrite]

## Claude · 2026-07-23T22:24:36.341Z

The engineering-side research came back rich (testing pyramid, CI gates, progressive delivery, observability, security, all mapped to Kai as a solo Vercel app). Waiting on the founder-validation half now, then I'll write it all into the repo doc.

## Naomi · 2026-07-23T22:25:42.012Z

<task-notification>
<task-id>a5ac96c86b3977e0a</task-id>
<tool-use-id>toolu_01Dp1uafTuKLewcFz4dp4HRg</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-naomiivie-kai/b3fd697b-dd3d-4bcd-aed8-b72e974fe3c6/tasks/a5ac96c86b3977e0a.output</output-file>
<status>completed</status>
<summary>Agent "Research startup product validation" finished</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
<result>I have enough well-sourced material across all 12 topics. Here is the deliverable.

---

# How Founders Validate &amp; Test a Product Before Public Launch
### A field guide for a solo founder shipping Kai (AI pomodoro/focus app: Google Calendar + Gmail + Spotify; students + productivity users)

Research window: 2024–2026, weighted to primary/authoritative sources. Every section gives **what it is → why it matters → how to do it**, then a **Kai priority flag**. A solo-founder priority stack sits at the very end.

---

## 0. The mental model: validate demand and value *before* you validate the build

Two frameworks anchor everything below.

**Marty Cagan / SVPG — The Four Big Risks.** Before you commit to building, you must retire four risks: **Value** (will they use/buy it?), **Usability** (can they figure it out?), **Feasibility** (can you build it?), **Business Viability** (does it work for legal/finance/brand?). "Discovery exists to kill all four before delivery starts," and most shipped-product failures trace to a risk the team skipped or deferred. Value is the risk founders most often skip.
- https://www.svpg.com/four-big-risks/
- https://www.svpg.com/product-risk-taxonomy/

**Eric Ries — Lean Startup / Build-Measure-Learn.** Form a hypothesis → build the *smallest* test of it → measure real behavior → learn (persevere, pivot, or kill). The unit of progress is **validated learning** — evidence of what the market values enough to pay for — not lines of code. A **pivot** is a structured change in strategy while keeping the vision. Note the deliberate ordering: you *think* Build→Measure→Learn, but you *plan backwards* — decide what you need to Learn, then what to Measure, then the minimum to Build.
- https://theleanstartup.com/principles
- https://www.strategyzer.com/library/dont-build-when-you-build-measure-learn

**Kai flag:** Kai's Value + Viability risks are the dangerous ones. The build is largely feasible (calendar/Gmail/Spotify APIs + an LLM), and Flocus proves the usability pattern. What's unproven: *will students pay for an AI that plans their pomodoros from real calendar/email signals, versus using a free timer + Spotify?* Spend validation effort there, not on the timer UI.

---

## 1. Lean Startup: MVP, Build-Measure-Learn, validated learning, pivots

**What it is.** The MVP is the *smallest* version that lets you start the learning loop — "the version that allows a team to collect the maximum amount of validated learning with the least effort." It is a test of a hypothesis, not a small version of the finished product. Common MVP forms: landing page, concierge, Wizard-of-Oz, single-feature build.

**Why it matters.** It caps the cost of being wrong and forces you to define, in advance, the metric that would confirm or kill the hypothesis. Without a pre-committed metric, you'll rationalize any result (confirmation bias).

**How to do it.**
1. Write the riskiest assumption as a falsifiable hypothesis ("Students will connect their Google Calendar to get AI-planned focus blocks").
2. Pick the leap-of-faith metric and threshold *before* building.
3. Build the cheapest artifact that produces that metric.
4. Decide the pivot/persevere rule in advance.

- https://theleanstartup.com/principles
- https://userpilot.com/blog/build-measure-learn/

**Kai flag:** Your MVP is *not* "the whole app polished." It's the thinnest slice that proves someone will hand Kai their calendar and let it plan their day. Everything else (Spotify modes, Alexa, wake word) is downstream of that.

---

## 2. Problem/solution validation BEFORE building

### 2a. Customer interviews — The Mom Test (Rob Fitzpatrick)
**What.** A method for extracting *truth* from conversations. Three rules: (1) talk about *their life*, not your idea; (2) ask about *specifics in the past*, not hypotheticals about the future; (3) talk less, listen more. Ignore the three kinds of "bad data": compliments, hypotheticals/fluff, and wishlist statements.
**Why.** People lie to be nice ("even your mom will lie to you"). Interviews *designed to get validation* produce false positives that lead you to build the wrong thing.
**How.** Ask: "Walk me through the last time you tried to focus/study and it fell apart." "What do you use today?" "What did you do last time — what did it cost you (time/money/emotion)?" Good signals are *past behaviors and prior spending*, not "I would totally use that." Aim for ~15–30 conversations before building.
- https://www.momtestbook.com/
- https://www.looppanel.com/blog/customer-interviews

### 2b. Landing-page / waitlist / smoke tests
**What.** A page describing the finished product with a single CTA (email signup, waitlist, or fake "Start free"). Conversion = your demand signal.
**Why.** Fast, cheap, *quantitative* proof a market exists before you write product code.
**How &amp; benchmarks.** Drive ~100 minimum (ideally 300+) targeted visitors for statistical relevance. Rough reads: cold-traffic landing pages convert ~2–5%; well-targeted waitlists 15–40%; a "smoke test" that mimics *purchase intent* (fake checkout) converts far lower but the signal is ~10–15× stronger. On a genuine purchase-intent CTA, ~10–15% is strong demand, under 5% means refine or pivot.
- https://dowhatmatter.com/guides/smoke-test-startup
- https://craftuplearn.com/blog/waitlist-landing-page-anatomy-incentives-benchmarks
- https://www.userintuition.ai/reference-guides/landing-page-tests-measuring-demand-before-building/

### 2c. Fake-door test
**What.** A real-looking entry point (button/menu/ad) for a feature that doesn't exist yet; clickers hit a "coming soon" + email capture. Measures demand per feature.
**Why.** AI features are expensive to build well, so float a fake "Ask AI"/"Plan my day" door and measure click-through before investing.
**How.** Instrument the click, show an honest "we're building this — want early access?" capture, compare CTR across placements.
- https://mvpdevelopment.company/blog/fake-door-mvp
- https://learningloop.io/plays/concierge

### 2d. Concierge &amp; Wizard-of-Oz MVPs
**What.** **Concierge** = deliver the outcome *manually and openly* to a few users (behind the desk, in plain view). **Wizard-of-Oz** = users think it's automated software, but a human does the work behind the curtain. Concierge tests *what customers need*; Wizard-of-Oz tests *whether the automated solution is valued*.
**Why.** You learn the real workflow and value before building automation. Airbnb, Food on the Table, and dozens of YC companies de-risked their core hypothesis this way with zero production code. The natural pairing: fake door proves they want the AI outcome → Wizard-of-Oz delivers it by hand → then you automate.
**How for Kai.** Recruit 5–10 students. Each morning, *you* look at their (shared) calendar + task list and message them a hand-crafted pomodoro plan + a Spotify playlist link. If they follow it and ask for it again tomorrow, that's validated demand for the AI planner — before you build the planner.
- https://www.mindtheproduct.com/wizard-of-oz-vs-concierge-testing-behind-the-curtain-or-behind-the-desk/
- https://www.exponentially.com/wizard-of-oz-mvp

**Kai flag — HIGHEST-LEVERAGE PRE-BUILD STEP.** The concierge/Wizard-of-Oz plan above is the single best use of your next two weeks. It validates the exact thing that's risky (AI-planned focus from real signals) at near-zero build cost, and it doubles as your first design partners and testimonials.

---

## 3. Usability testing

**What.** Watching real users attempt real tasks to find where the interface fails them. **Moderated** = live facilitator, real-time, can probe "why" with follow-ups (best for early/complex flows). **Unmoderated** = participant completes pre-written tasks alone on a platform that records screen/clicks/time-on-task (cheaper, faster, scales). The **think-aloud protocol** = participant narrates their thoughts while working, revealing *why*, not just *what*.

**Why.** Retires Cagan's Usability risk. Catches confusion an analytics funnel can only *count*, not *explain*.

**How many — Nielsen's "5 users."** Jakob Nielsen (NN/g): 5 users in *qualitative/formative* testing surface ~85% of usability problems; the marginal user after ~5 mostly repeats findings. Better to run *more small tests across iterations* than one big test. Caveats: the rule holds only for a *homogeneous* user group and *qualitative* testing — distinct user segments need ~5 each, and *quantitative* benchmarking needs ~40 users.
- https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
- https://www.nngroup.com/articles/how-many-test-users/

**Tools.** Maze (unmoderated only, fast, prototype testing), UserTesting (both moderated + unmoderated, webcam + verbal think-aloud + sentiment), Hotjar/session-replay for passive observation.
- https://maze.co/guides/usability-testing/moderated-vs-unmoderated/

**Kai flag:** Run 5 moderated, think-aloud sessions on the *first-run flow* specifically: landing → "Hey Kai" prompt → Google OAuth consent → first suggested pomodoro. The OAuth consent screen (scary Google permission warnings for Calendar/Gmail) is a known drop-off; watch faces there. This is cheap and high-yield; do it before any paid launch.

---

## 4. Alpha vs. beta testing

**What.**
- **Alpha** = internal, in a lab/staging environment, to remove obvious defects before external exposure.
- **Closed/private beta** = invite-only, small, curated real users; qualitative, high-touch feedback; good for sensitive/unfinished features.
- **Open beta** = public; scale, stress-test infrastructure, broad bug discovery, gauge market appeal.
- **Beta cohorts** = overlapping waves gated by feature flags with kill switches (the modern continuous-rollout model that has largely replaced the rigid alpha→beta→GA line).

**Why.** Lets real usage answer questions your dev environment can't, while limiting blast radius.

**What to instrument** (the pattern across all stages: *limit the audience, instrument everything*): activation/first-value completion, funnel drop-off, retention cohorts, error/crash rates, API failure rates (critical for you — Google/Spotify token expiry &amp; rate limits), latency, and a lightweight in-app feedback channel. Add feature flags so you can dark-launch and roll back per cohort.
- https://www.startups.com/lexicon/beta-testing
- https://launchdarkly.com/blog/beta-testing-programs/

**Kai flag:** Go **closed beta first** (20–50 students, invite via the waitlist). You need qualitative depth and — importantly — you'll be under Google's OAuth *unverified-app* 100-user cap anyway (see §11). Don't do a big open beta until OAuth verification clears and retention looks healthy.

---

## 5. Dogfooding (founder uses own product daily)

**What.** "Eating your own dog food" — using your product yourself, every day. (Term traces to a 1976 Alpo ad; popularized by Microsoft's 1988 "eating our own dogfood" memo.)
**Why.** Closes the empathy gap, surfaces bugs/UX friction before users hit them, produces fast feedback, and makes you a credible, confident spokesperson.
**How.** Commit to running your *own* real workday through Kai — plan your build sessions with it, connect *your* Google Calendar and Gmail, use its Spotify focus modes while coding. Log friction daily.
- https://en.wikipedia.org/wiki/Eating_your_own_dog_food
- https://maddevs.io/blog/dogfooding/

**Kai flag — DO THIS STARTING NOW, it's free.** You are the target user (a productivity-obsessed builder). Kai should be the tool you use to build Kai. If you won't use it daily, that's your first, cheapest validation failure — and your global CLAUDE.md "GitHub-first, ship-as-you-build" workflow is itself a dogfooding-friendly cadence.

---

## 6. Product-Market-Fit measurement

### 6a. Sean Ellis test — the 40% rule
**What.** Survey engaged users: *"How would you feel if you could no longer use [product]?"* → Very disappointed / Somewhat / Not disappointed. **≥40% "very disappointed" ⇒ product-market fit.** 25–40% = close, build toward the "very disappointed" segment. &lt;25% = keep iterating or rethink the market.
**How.** Survey ~40–50 users who hit core value in the last ~2 weeks. Follow-ups: main benefit, who benefits most, how to improve, acquisition channel.
- https://learningloop.io/glossary/sean-ellis-score
- https://formbricks.com/blog/product-market-fit-survey-questions

### 6b. Superhuman's PMF Engine (Rahul Vohra, First Round) — the operational version
Turns the 40% metric into a growth *engine*. Superhuman went **22% → 58% "very disappointed" in three quarters.** Four steps:
1. **Segment.** Filter to "very disappointed" users, cluster personas, and define your **High-Expectation Customer (HXC)** in their own words. *Segmentation alone took the score 22% → 33%.*
2. **Analyze.** "Politely disregard" the not-disappointed (lost cause). Study what the *very*-disappointed love, and what blocks the *somewhat*-disappointed **where your core benefit already resonates**.
3. **Roadmap 50/50.** Half the roadmap doubles down on what fans love; half removes the top blockers for fence-sitters. (Only doubling down → score stalls; only fixing blockers → competitors pass you.) Prioritize by cost×impact matrix, low-cost/high-impact first.
4. **Repeat.** Survey new users on a rolling basis; make "very disappointed %" the primary OKR.
- https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/

### 6c. Retention cohorts — the behavioral truth (Lenny Rachitsky, Andrew Chen, Sequoia)
**What.** The strongest PMF signal is a **retention curve that flattens** (reaches a stable asymptote) rather than decaying to zero — the shape, not any single number, tells you if it's sticky. D1/D7/D30 are the leading indicators; **D7 is the earliest *reliable* one** (D1 is easily gamed with onboarding friction/push).
**Benchmarks.** Lenny: strong **D30 ≥ ~25% consumer, ~35%+ B2B**. Daily-use consumer apps: **D1/D7/D30 around 60/30/15** indicates true daily frequency; D7≈2×D30 is typical. Great retention is *the* best indicator of PMF and the base of LTV and every good acquisition loop.
- https://www.lennysnewsletter.com/p/what-is-good-retention-issue-29
- https://articles.sequoiacap.com/retention
- https://prooflytics.io/blog/d7-d30-retention-benchmarks-by-app-category

### 6d. Activation rate, leading indicators, NPS
- **Activation** = % of new users reaching first value; fix new-user retention/activation *first* — that's where the most users leak (Lenny). https://www.linkedin.com/posts/lennyrachitsky_what-is-a-good-activation-rate-activity-6990690292412665856-S_du
- **NPS** ("how likely to recommend, 0–10") is a *relationship/sentiment* metric, useful as a trend and diagnostic, but it is **not** a substitute for the Sean Ellis test or retention for PMF. Use it secondarily.

**Kai flag:** Your PMF dashboard = **(1) Sean Ellis 40% survey** run continuously (Superhuman-style), **(2) weekly cohort retention** watching for a flattening curve, **(3) activation = % who complete a first full pomodoro *with a Kai-suggested plan*.** For a daily focus tool, aim to watch D1/D7 closely — a focus app should be a *daily habit* or it isn't working. Do **not** invent "energy dips" (per your AGENTS.md); only claim patterns your retention/session data actually show.

---

## 7. Analytics &amp; instrumentation for launch

**What.** Event tracking → funnels → activation → retention, plus session replay to *see* the confusion. Core tools: **PostHog** (all-in-one: analytics + session replay + feature flags + experiments + surveys, generous free tier, ~$50k startup credit), **Amplitude** (deep behavioral analytics, Compass finds retention predictors), **Mixpanel** (fast funnel/retention query builder, now with native session replay; 1-yr free startup program). Note: Amplitude/Mixpanel historically needed a separate replay tool (Hotjar/FullStory/LogRocket); PostHog and now Mixpanel bundle it.

**Why.** You cannot improve activation/retention you don't measure. Replay tells you *why* a funnel step drops.

**How.** Instrument a small, deliberate event taxonomy from day one: `signup`, `google_oauth_started/completed/failed`, `spotify_connected`, `first_plan_generated`, `pomodoro_started/completed`, `voice_wake_triggered`. Build funnels for signup→activation and define the single activation event. Watch cohort retention weekly.
- https://posthog.com/blog/posthog-vs-mixpanel
- https://productgrowth.in/insights/ai-ml/mixpanel-vs-amplitude-vs-posthog/

**Kai flag — pick PostHog.** For a solo founder it collapses analytics + funnels + session replay + feature flags + A/B + surveys into one free tool, so you can run the Sean Ellis survey, cohort retention, onboarding replay, and beta feature flags without stitching four vendors. Instrument OAuth-step drop-off explicitly.

---

## 8. A/B testing &amp; experimentation (onboarding &amp; pricing)

**What.** Randomized comparison of two variants against one metric. Apply to onboarding checklists, default settings, upgrade prompts, and price points.
**Why.** Removes opinion from onboarding/pricing decisions that heavily move activation and revenue.
**How &amp; the solo-founder caveat.** Standard threshold is **95% confidence.** But **early-stage traffic is usually too thin for trustworthy A/B tests** — effect size matters more than raw sample size, and pricing tests specifically need roughly **250–500 visitors per variant and 30–60 days** to reach significance. Below that, prefer *sequential* qualitative iteration (ship, watch replays, interview) over underpowered A/Bs. Reserve true A/B tests for your highest-traffic surfaces (landing page, pricing page) once volume allows.
- https://www.statsig.com/blog/you-dont-need-large-sample-sizes-ab-tests
- https://www.getmonetizely.com/articles/pricing-experimentation-tools-a-guide-to-ab-testing-prices-with-software

**Kai flag:** Don't A/B test yet — you won't have the traffic for significance. Optimize onboarding via 5-user usability tests + session replay now; save A/B testing for the pricing page and landing page after launch traffic builds.

---

## 9. Staged/soft launch vs. big-bang; launch checklists; GTM for a beta

**What.** **Soft/staged launch** = release quietly to a small audience, learn, iterate, widen — vs. **big-bang** = one large coordinated splash. YC's stance: **launch early, even if mediocre**, because until you launch you're designing for *hypothetical* users; after, real reactions teach you what to build. Then **do things that don't scale** (hand-hold early users).
**Why.** A big-bang on an unvalidated product wastes your one first impression and buries you in undiagnosable feedback. Staged launches compound learning.
**How — beta GTM &amp; Product Hunt.**
- Build a waitlist *before* launch; document the build publicly (X/LinkedIn/Indie Hackers) to accrue supporters who later upvote.
- **Product Hunt checklist:** study past launches; prep professional assets (gallery, tagline, demo GIF); launch 12:01am PT; post a maker comment + pinned FAQ; tell your real audience but **never ask for upvotes** (PH rules); reply to *every* comment fast; days 1–2 track traffic sources, days 3–7 follow up with warm leads and reviewers.
- Note (2025 data): niche communities like Indie Hackers/Reddit can convert 3–8× better than Product Hunt for the *right* audience — for students, that may mean student subreddits, Discords, and campus channels over PH.
- https://www.ycombinator.com/library/4D-yc-s-essential-startup-advice
- https://www.indiehackers.com/post/the-product-hunt-launch-guide-dc4fed11ae
- https://awesome-directories.com/blog/indie-hackers-launch-strategy-guide-2025/

**Kai flag:** **Staged, not big-bang.** Sequence: waitlist (done) → concierge/WoZ (§2d) → closed beta 20–50 (§4) → OAuth verification (§11) → wider beta → Product Hunt + student-community launch once retention curve flattens. A Product Hunt splash *before* OAuth verification is actively risky — new users would hit the "Google hasn't verified this app" scary screen.

---

## 10. Pricing &amp; willingness-to-pay validation

**What.** **Van Westendorp Price Sensitivity Meter (PSM)** — 4 questions per respondent: at what price is it *too cheap* (doubt quality), *cheap* (bargain), *expensive*, *too expensive* (won't buy)? Plotting the curves yields an acceptable price *corridor* and an optimal point. Complement with **fake pricing pages** (a real pricing page with plans; clicking "Subscribe" leads to "coming soon"/waitlist to measure *behavioral* intent).
**Why.** Customer-informed pricing correlates with materially higher growth than cost-plus or competitor-copy pricing. Van Westendorp elicits WTP with predictive quality comparable to incentive-aligned methods — *but* it's hypothetical and biased toward minimizing resistance, so triangulate with the fake pricing page (real clicks).
**How.** Run PSM on 40+ target users to set a starting corridor; publish 2–3 fake pricing tiers and measure plan-selection clicks; validate with actual paid conversions in beta.
- https://conjointly.com/products/van-westendorp/
- https://www.getmonetizely.com/articles/how-to-implement-van-westendorp-price-sensitivity-meter-for-saas-research

**Kai flag:** Students are price-sensitive — WTP validation is *not* optional. Use Van Westendorp in your beta survey to find the corridor, then a fake pricing page to test real click-intent, then test an actual paywall/trial in the closed beta. Expect student pricing to sit well below prosumer; consider a free tier + cheap student plan. (Per your global config: do not commit to paid infra/domains without confirmation.)

---

## 11. Legal / trust readiness before public launch — *the gating item for Kai*

**What.** Baseline: a **Privacy Policy**, **Terms of Service**, and (if GDPR/CCPA users) **DPAs with sub-processors**, a lawful basis for processing, consent capture, and a 72-hour breach-response plan.
**Why — and the Kai-specific blocker:** Kai requests **Google restricted/sensitive OAuth scopes** (Gmail, Calendar). Google's rules:
- **Sensitive scopes** (e.g., Calendar, Gmail *metadata*) → require **OAuth app verification** (brand review, verified domain, homepage, privacy policy, demo video).
- **Restricted scopes** (full Gmail read/content) → require verification **plus an annual independent security assessment (CASA)** by a Google-empanelled assessor if you store/transmit that data on your servers.
- **Until verified, an app is capped at ~100 users** and shows an **"unverified app" warning screen** on the consent flow — a major trust/conversion killer at public launch.
- Timelines: verification/CASA can take **weeks to months** and CASA has real cost; **start early.**
- https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification
- https://developers.google.com/identity/protocols/oauth2/production-readiness/restricted-scope-verification
- https://sprinto.com/blog/gdpr-for-saas/

**How for Kai.**
1. **Minimize scopes** — request the *narrowest* scope that works (e.g., `calendar.events` not full Gmail; use Gmail *metadata*/send scopes rather than full-content read if the feature allows). This can drop you from *restricted+CASA* to *sensitive-only*, avoiding the annual security audit.
2. Publish a Privacy Policy + ToS **before** the OAuth submission (Google requires them and checks that the policy discloses the Google data use).
3. Stand up verified domain, homepage, and a demo video of the OAuth flow.
4. Submit verification during closed beta (you're under 100 users then anyway).
5. Be explicit in-product about what data you touch and why (your AGENTS.md "trust" ethos + Google's "limited use" requirements align here).

**Kai flag — START OAUTH VERIFICATION NOW; it's the long pole.** This is the one item with a multi-week external dependency you can't compress. Everything else can move fast; Google's review can't. Minimize scopes to avoid CASA if at all possible. Do **not** schedule a public/Product Hunt launch date until verification is confirmed.

---

## 12. Common founder mistakes to avoid

- **Not talking to users / "validating while building."** Writing code and interviewing simultaneously breeds confirmation bias — you hear what you want because you're already committed. Interview *before* you build (§2). Only ~18% of first-time founders succeed; building something nobody wants is the top killer. https://tafhub.medium.com/why-most-founders-validate-their-startup-idea-wrong-and-what-actually-works-b332e719471e
- **Vanity metrics.** Signups, installs, page views, social followers *look* like traction but hide weak retention/economics. One cited case: traffic tripled while revenue *fell*. Track *actionable* metrics — activation, retention, revenue, "very disappointed %." https://www.epirus.vc/blog/vanity-metrics-vs-actionable-metrics-how-startup-founders-can-focus-on-what-actually-drives-growth
- **Launching too late (perfectionism).** Until you launch you're building for hypothetical users; late testers feel judged, early testers feel heard (YC). https://www.ycombinator.com/library/4D-yc-s-essential-startup-advice
- **Launching too early on the wrong thing / big-bang before validation** — wastes the one first impression.
- **Skipping the Value &amp; Viability risks** while over-investing in polish (Cagan): the two risks founders most often defer are the two that kill products.

**Kai flag:** Your two realistic traps are (a) **polishing the Flocus-grade UI before proving anyone will connect calendar+Gmail and follow AI plans**, and (b) **celebrating waitlist signups as validation** — those are the definitional vanity metric until they convert to activated, retained, paying users.

---

## Solo-founder priority stack for Kai (do in this order)

| # | Action | Cost | Why first |
|---|--------|------|-----------|
| 1 | **Start Google OAuth verification; minimize scopes to dodge CASA** (§11) | Low effort, long wall-clock | Only item with a weeks-long external dependency; gates public launch |
| 2 | **Dogfood Kai daily** — use it to build Kai (§5) | Free | You're the target user; instant friction feedback |
| 3 | **Concierge / Wizard-of-Oz** hand-planned pomodoros for 5–10 students (§2d) | Low | Validates the *risky* core (AI planning from real signals) before building it |
| 4 | **10–20 Mom Test interviews** + fake pricing page + Van Westendorp (§2a, §10) | Low | Truth on demand + WTP for price-sensitive students |
| 5 | **Instrument with PostHog**; define the single activation event (§7) | Low | Nothing below is measurable without this |
| 6 | **5-user moderated usability tests on the OAuth-consent onboarding** (§3) | Low | Retire the biggest drop-off; cheap, high-yield |
| 7 | **Closed beta, 20–50 students, feature-flagged** (§4) | Med | Qualitative depth; stays under the 100-user unverified cap |
| 8 | **Run Sean Ellis 40% survey + weekly cohort retention continuously** (§6) | Low | Your real go/no-go for widening |
| 9 | **Staged public launch** (student communities + Product Hunt) *only after* verification clears and retention flattens (§9) | Med | Don't spend your one splash on an unverified, unretained product |
| 10 | **A/B test** landing + pricing pages *after* traffic supports significance (§8) | Med | Underpowered tests earlier mislead |

**The one-line version:** Prove — with hand-run concierge plans and real interviews — that students will connect their Google data and *follow Kai's AI focus plans* daily, get OAuth verification moving in parallel because it's the long pole, and don't confuse a growing waitlist with product-market fit. PMF is the retention curve flattening and ≥40% saying they'd be "very disappointed" without Kai — not signups.

---

### Full source list
**Lean Startup / discovery:** https://theleanstartup.com/principles · https://www.strategyzer.com/library/dont-build-when-you-build-measure-learn · https://www.svpg.com/four-big-risks/ · https://www.svpg.com/product-risk-taxonomy/
**Interviews / pre-build validation:** https://www.momtestbook.com/ · https://www.looppanel.com/blog/customer-interviews · https://dowhatmatter.com/guides/smoke-test-startup · https://craftuplearn.com/blog/waitlist-landing-page-anatomy-incentives-benchmarks · https://www.userintuition.ai/reference-guides/landing-page-tests-measuring-demand-before-building/ · https://mvpdevelopment.company/blog/fake-door-mvp · https://learningloop.io/plays/concierge · https://www.mindtheproduct.com/wizard-of-oz-vs-concierge-testing-behind-the-curtain-or-behind-the-desk/ · https://www.exponentially.com/wizard-of-oz-mvp
**Usability:** https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/ · https://www.nngroup.com/articles/how-many-test-users/ · https://maze.co/guides/usability-testing/moderated-vs-unmoderated/
**Alpha/beta:** https://www.startups.com/lexicon/beta-testing · https://launchdarkly.com/blog/beta-testing-programs/
**Dogfooding:** https://en.wikipedia.org/wiki/Eating_your_own_dog_food · https://maddevs.io/blog/dogfooding/
**PMF:** https://learningloop.io/glossary/sean-ellis-score · https://formbricks.com/blog/product-market-fit-survey-questions · https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/ · https://www.lennysnewsletter.com/p/what-is-good-retention-issue-29 · https://articles.sequoiacap.com/retention · https://prooflytics.io/blog/d7-d30-retention-benchmarks-by-app-category
**Analytics:** https://posthog.com/blog/posthog-vs-mixpanel · https://productgrowth.in/insights/ai-ml/mixpanel-vs-amplitude-vs-posthog/
**A/B &amp; pricing:** https://www.statsig.com/blog/you-dont-need-large-sample-sizes-ab-tests · https://www.getmonetizely.com/articles/how-to-implement-van-westendorp-price-sensitivity-meter-for-saas-research · https://conjointly.com/products/van-westendorp/
**Launch:** https://www.ycombinator.com/library/4D-yc-s-essential-startup-advice · https://www.indiehackers.com/post/the-product-hunt-launch-guide-dc4fed11ae · https://awesome-directories.com/blog/indie-hackers-launch-strategy-guide-2025/
**Legal/OAuth:** https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification · https://developers.google.com/identity/protocols/oauth2/production-readiness/restricted-scope-verification · https://sprinto.com/blog/gdpr-for-saas/
**Mistakes:** https://www.epirus.vc/blog/vanity-metrics-vs-actionable-metrics-how-startup-founders-can-focus-on-what-actually-drives-growth · https://tafhub.medium.com/why-most-founders-validate-their-startup-idea-wrong-and-what-actually-works-b332e719471e

*Note: I did not write this to a file (per instructions not to create report/summary .md files). If you want it saved into `docs/` in the Kai repo — it fits naturally alongside `BUSINESS_PLAN.md` — say the word and I'll add it as a proper doc and commit it.*</result>
<usage><subagent_tokens>55008</subagent_tokens><tool_uses>23</tool_uses><duration_ms>310327</duration_ms></usage>
</task-notification>

## Claude · 2026-07-23T22:26:05.237Z

Both reports are in — thorough and well-sourced. Writing the synthesis into the repo now:

## Claude · 2026-07-23T22:27:36.950Z

[Tool: Write]
