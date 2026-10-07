---
name: project-sabi-tester-round
description: "The 5-Nigerian-adult / 5-day Sabi tester round being prepared Aug 18-20 2026 — the docs, the research behind them, what Naomi corrected, and what still blocks day one."
metadata:
  node_type: memory
  type: project
  originSessionId: e254ca93-523b-4315-b81f-b5801478e21f
  modified: 2026-08-20T19:40:50.773Z
---

# The 5-adult tester round (prepared Aug 18–20 2026)

**Shape.** Five testers, five days, minimum one call a day, extras unlimited; **Sabi calls them, they
pay nothing.** Day 1 baseline → Day 2 memory + the shared-phone "no, this is someone else" test
(72-hour return call) → Day 3 noise → Day 4 the number-stress list → Day 5 break her. Adapted from
the 10-child pre-pilot plan. Docs: `pilot/testing/SABI_5_ADULT_TESTER_PLAN_2026-08.md` (+ branded PDF,
artifact "Five Days With Sabi"), `SABI_TESTER_BRIEF_COLD_START.md`, `SABI_USER_TESTING_PLAN_2026-08.md`,
`SABI_NIGERIAN_TESTER_GUIDE.md` (v3, superseded-banner removed on her instruction),
`SABI_TESTER_GUIDE_v4_CURRENT_BUILD.md`, `HOW_TOP_STARTUPS_TEST_RESEARCH_2026-08.md`.

**The number-stress list must come from the real deck** — the question bank tops out at **48**, so the
answers to stress are **13/30, 15/50, 32, 35, 36, 42, 48**. The v3 guide's 30/40/45/15/50/5 list
includes numbers Sabi never asks for.

**The question that matters most:** *"did she mark you wrong when you were right?"* — the silent-failure
class. Happy-path calls never surface it.

**Research behind the plan (Aug 20).** Top US software startups have almost no QA department and no
test plan; they have four things instead — a small team with a high personal bar, founders touching
every early user by hand, **scheduled time to fix instead of ship**, and a cheap written artifact per
change. The last two are what Sabi's plan lacks. Linear: ~25 engineers, no QA, cut scope not quality.
Figma: **Quality Week** — a week shipping nothing, only fixing, plus a company-wide bug bash (free,
and it's exactly the gap between Round 1 and Round 2). Stripe: bug-finding as an interview round,
optimising for the *subtle* class. Superhuman: the copyable bit isn't the 40% question, it's that
**~40 respondents** is the floor for a directional PMF read — 5-per-group finds usability bugs and
will never produce a PMF number; also Vohra personally onboarded every user by video, which is what
Sonia-in-the-room already is. Duolingo: ~30 experiments/week, but the copyable bit is the **one-page
memo** (hypothesis, expected outcome, audience, specs) — there is no artifact today for "I changed the
greeting, did it help?". Voice-AI eval 2026: LLM-judge on 5–10% of traffic, cheap heuristics on 100%,
but at this volume the advice is *just listen to the calls*; what's missing is running
`numeric_sidecar_report.py` as a regression check on prompt edits. Appendix kept for funders: Rori's
RCT won at 2 × 30 min/week (effect size 0.37) — Sabi is 2 × 5–7 min/day, defensible but unmeasured.

**⚠️ Naomi's corrections to the cold-start brief — treat every one of these as FALSE if it resurfaces
(they were my inferences from config, stated as fact):** "there is no Nigerian number" · "the callback
line is dead / AT has no trunk" · "numeracy only, no literacy" · "no `*` feedback key" · the
`SABI_GEMINI_LIVE_PHONES` registration prerequisite and "two versions, you'll reach the wrong one" ·
"she picks up directly, no menu, no callback" · "recordings stored in Germany/Hetzner". And the one
that would have damaged the round: **"she will mishear numbers — don't report it."** Backwards —
mishearing is exactly what testers must report, in detail. She also cut the proxy-for-a-child framing,
the accent paragraph, the no-real-child and no-crisis-phrase rules, withdrawal rights and the
emergency numbers. Two of her annotations she was right on: **no PMF question this early** (it belongs
after a tester's third or fourth call), and **real personal information is encouraged** because that's
what real callers do — the only carve-out being realistic-but-fake bank/address details, since the
call is recorded and transcribed.

**Feedback strategy, settled Aug 20.** WhatsApp voice note is right *for how it felt* — they already
live in WhatsApp, talking beats typing, tone survives, 25 notes over five days is manageable. It is
wrong for **misheard numbers**: ask for one typed line each, literally *"I said thirty, she heard
thirteen."* It stops working around 15–20 testers or with parents rather than volunteers. Her real
objection was organisation — she wants it on the cloud, and `/admin/feedback` already is that
(note glued to the exact `call_uuid` and second, audio + transcript, auto-redacted, and
`SABI_ADMIN_PIN` gives read-only `/admin/*` access so **Sonia can triage without holding the write
key**). See [[project-sabi-live-lane-to-production]] for the Live-lane capture that unblocks it.
Nothing can be recorded *after* the caller hangs up — the carrier tears the leg down and Asterisk's
`h` extension cannot play audio or collect input. So feedback must happen before the goodbye.

**How testers get their calls, without Naomi being a human pager:** flash callback is on by default
(`SABI_FLASH_CALLBACK_ALL=1` in `main.py` — "EVERY inbound caller is flash-called back so the child is
never charged"), 4-second delay, 45-second de-dupe cooldown — ring and hang up, Sabi rings back free.
Plus one scheduled nudge a day per tester via `/admin/asterisk/direct-call`, skipped if they already
called. ⚠️ `FLASH_CALLBACK_RETRY_ENABLED=0`, max attempts 1 — a callback into voicemail is simply gone.

**Still blocking day one:** tester numbers must go into `SABI_CALL_REQUEST_ALLOWLIST` (hers only today)
and, while the lane is opt-in, `SABI_GEMINI_LIVE_PHONES`; no compensation line has been decided; the
Google Form link is still `[Naomi to add link]`; and **nobody has yet heard Sabi over the Africa's
Talking leg** — the carrier switch fixed cost, not the audio problem that drove her to Twilio.

Related: [[project-sabi-text-to-call]], [[project-e4e-africas-talking]], [[project-sabi-gemini-live]]
