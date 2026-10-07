---
name: project-sabi-live-lane-to-production
description: "Aug 20 2026 — the Gemini Live lane is being moved from Naomi-only canary to the production default: feedback capture wired in, crisis guard being ported, allowlist to become opt-out."
metadata:
  node_type: memory
  type: project
  originSessionId: 7e3c69b7-d1ba-4ba2-b7d1-edb6520a98f1
  modified: 2026-08-20T19:40:15.248Z
---

# Gemini Live is being promoted to the production lane (Aug 20 2026)

Naomi's framing: *"i had seperate lane because we were wokring on it - but had every intention to
port it to the new lane."* Her instruction at 19:34 UTC: **"leave literacy for now do 1-4."**

**The four steps she approved, in order:**
1. Port `guard_input` + `raise_safeguarding_incident` into `gemini_live.py` — non-negotiable with children.
2. Literacy — **deferred** on her instruction (stays as it is; the Live lane has no literacy content:
   19 multiplication problems, numeracy tools, "numeracy tutor" prompt).
3. Flip `phone_uses_gemini_live()` from an opt-**in** allowlist to opt-**out**, keeping a per-number escape hatch.
4. Measure cost for a week — native audio bills differently from the Haiku + Groq chain and nobody knows the number.

**In flight and UNCOMMITTED in `sabi-server/` as of 15:37 ET** (do not clobber): `gemini_live.py`
(+231 lines), `call_admin.py`, `phone_utils.py`, `gemini_live_regression.py`, plus untracked
`scripts/gemini_live_cost_report.py` (totals `usage_metadata` from the call sidecars; prices passed
in, never baked). Last commit on main is `eccabf0`.

**Feedback capture is already wired into the Live lane** — caller says "I want to leave feedback" /
complain / report a problem / leave a note → Sabi goes silent, the **same beep** plays, their next
turn is stored as the note (not graded, does not touch learning state) and lands in `/admin/feedback`
in the identical format as the turn-based lane, so the dashboard needed no changes. Cues:
`FEEDBACK_OPEN_CUE`, `FEEDBACK_SAVED_CUE`, `SAFEGUARDING_CUE`. 20 regressions passed at the time.

**The `*` star key was never broken on the Live lane — it was never there.** The star key and the
spoken trigger live in `voice_realtime.py:245`; `gemini_live.py` had zero feedback references. Any
star-key test from Naomi's own number was testing a lane where the feature did not exist. Spoken
triggers beat the star key anyway: no keypad signalling, works on any handset, and a child holding a
phone to their ear cannot hunt for `*`.

**⚠️ `guard_output` cannot be ported as-is.** On the turn-based lane you filter the model's text
before a word is spoken. On native audio the speech streams as it is generated, so by the time you
have the transcript the child has already heard it. The nearest equivalent is what the early-wrap
guard does — detect on the streaming transcript and drop the *unplayed* remainder from the queue,
truncating a bad answer mid-sentence rather than preventing it. `guard_input` ports cleanly.

**What else the Live lane loses versus the old one**, worth accepting deliberately: no provider
fallback (the old lane runs Cerebras → Claude → Groq → local; Gemini Live is one vendor, so Google
down = call down), and literacy disappears while `force_numeracy_course()` is unconditional.
Automatic fallback the other way already exists — the routing is a single `elif` at
`voice_realtime.py:2825`, and a failed Gemini connect drops to the old pipeline without losing the call.

⚠️ **The whole `pilot/` tree is in NO git repo** (only `curriculum-app/` and `sabi-server/` are repos).
Every testing doc, the DPIA, the pre-pilot plans exist on this laptop only — against her own
GitHub-first rule, and `DPIA_SABI.md` is cited by 15 other docs.

Related: [[project-sabi-gemini-live]], [[project-sabi-guardrails]], [[project-sabi-tester-round]]
