---
name: feedback-dont-assert-inferences
description: "Do not state inferences from env vars, config, or code as verified build facts — especially in tester-facing docs. Ask Naomi what is actually live."
metadata:
  type: feedback
---

Aug 20 2026 (session `7e3c69b7`): I wrote a Nigerian tester brief, led it with "**Verified against the running code**", and asserted that there was **no Nigerian number**, no callback, numeracy-only, and no `*` feedback key. Naomi deleted all of it: *"false — there is a Nigerian number, I am just choosing not to use it in this moment, that could change tomorrow — do not assume you know everything."*

Then: **"do not lead with assumptions. follow what I say."**

**Why:** I inferred "the AT line is dead" from `AT_USERNAME="sandbox"` plus a stale line in `SABI_USER_TESTING_PLAN_2026-08.md`, and reported it as present-tense fact. The code says otherwise — `main.py` defaults `SABI_SIP_PROVIDER=africastalking`, ships `DEFAULT_SIP_CALLER_IDS["africastalking"] = "+2342017001459"`, mounts the AT router at `/voice`, and defaults `SABI_FLASH_CALLBACK_ALL=1` ("EVERY inbound caller is flash-called back so the child is never charged"). Config state ≠ deployment state ≠ Naomi's current intent, and she switches lanes deliberately.

**How to apply:**
- A config value tells me what a default *is*, never what is *live* or what she *intends*. Ask her which lane/number is active before writing it down.
- Never write "verified" unless I ran the thing. Reading source is not verification.
- In tester-facing or partner-facing docs, omit anything I can't confirm rather than stating it confidently — a wrong instruction to a volunteer wastes a whole round.
- One more caught the same day: I told testers *not* to report misheard numbers ("that's what we're measuring"). Backwards — mishearing is the single signal the round exists to collect. Never instruct a tester to suppress the thing under test.

Related: [[feedback-verify-by-driving]], [[feedback-e4e]], [[project-sabi-gemini-live]]

**I made the same mistake again on Aug 20 2026 - e254ca93**, which is why this memory now names the
specific trap. I read `AT_USERNAME=sandbox` off the running sabi-server container and told her the
Nigerian SMS path "isn't live." Her account is live (`EduForEquality`); the container is the *voice*
box and reads sandbox only because she moved voice to Twilio herself. The rule that would have caught
it: **before describing a capability as unavailable, check the system that actually performs it** —
SMS sends from Vercel, not from the Hetzner container, and I never looked at Vercel's env. One config
value from an adjacent system is not evidence about an account, a vendor relationship, or her intent.
See [[project-e4e-africas-talking]].
