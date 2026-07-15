---
name: project-sabi-identity
description: "Sabi lesson timing (2 calls/day) + shared-phone per-child identity design, the research moat behind it, and the pipeline-routing flag"
metadata:
  node_type: memory
  type: project
  originSessionId: 3b8ddd08-9e23-4598-83dd-60902b9107f3
---

# Sabi — Lesson Timing & Shared-Phone Identity (decided Jun 2026, session 3b8ddd08)

Full design + research: **`pilot/infrastructure/SABI_SHARED_PHONE_IDENTITY.md`**.

## Decisions (Naomi)
- **Two calls/day, NOT one combined call.** Literacy and numeracy are **separate calls** (~5–7 min each). The consent form's "short break between lessons" = two calls, not one session. (I initially argued combined-call; Naomi corrected — it's two.)
- **Subject routing = day-anchored "what hasn't this child done today,"** not the blind cross-call alternation that's currently coded (alternation drifts the moment a kid calls an odd number of times).
- **Identity on a shared phone:** Sabi greets with a **best-guess name** (only when confident) → if wrong, the child **corrects her** → Sabi **mints a new learner** → once a phone has **≥2 learners, Sabi confirms who's calling first** ("Is this Amara, or someone else?").

## Already built (don't re-build)
- **Literacy/numeracy split is DONE in `sabi-server/`**: `learning_state.course` (numeracy|literacy), nested literacy sub-state, auto-alternation (`route_next_course_after_session`), never mid-call. ⚠️ **The Next.js Africa's-Talking webhook path is NUMERACY-ONLY** (ignores `course`) — confirm the pilot routes through the **Python/Asterisk** server or literacy won't deliver despite the consent promising it.
- **Shared-phone identity schema is DONE**: `curriculum-app/supabase-sabi-shared-phone-identity.sql` — `phone_household_key` + **`learner_key = phone_number_normalized || '::' || child_name_normalized`** (UNIQUE); one phone (household) → many learners; old one-row-per-phone constraints dropped. Hook: `sabi-server/diagnostic_flow.py → build_opening_turn()` (~line 373). So the work is runtime behaviour + the prompt, not new schema.

## Research verdict (deep: Viamo/3-2-1, Bakame, Eneza/Shupavu291, M-Shule, Rori, GeoPoll, Gram Vaani, Avaaj Otalo, Burrell)
- **Nobody solves per-child identity on a shared phone** — all key on the phone NUMBER, one account per number (Bakame "it remembers you" breaks when a sibling picks up; Eneza markets sharing as a reach multiplier ~8.6 kids/account but data sees one). → Sabi's per-child identity is **whitespace = a fundable differentiator + equity angle** (shared-number defaults to the dominant member; one India forum 7% female).
- It's the **field-proven pattern automated** — Avaaj Otalo users spontaneously said names aloud (65% of recordings) because the system couldn't disambiguate.
- **Per-child memory requires an enrolment step** (maternal mHealth, Avaaj Otalo allow-list) — Sabi's **coordinator sign-up IS it**; capture name + class at enrolment.
- **Hardening (now in the note):** one-step confirm not open "who are you"; fuzzy-match + playback-confirm names; greet-by-name only when confident; treat profiles as SOFT identity (flag shared-phone data lower-confidence in eval); never reward a bare number (Gram Vaani referral fraud); human onboarding is the biggest lever on low-literacy success.

## Pending
- Wire the drop-in prompt into Sabi's opening (left for Naomi/Codex to avoid colliding with the production prompt).
- Decide caregiver-mediated handoff for under-8s in the pilot.
- Confirm pilot telephony routes via the Python/Asterisk server (literacy path).

Related: [[project_e4e_tech]] [[project_sabi_guardrails]] [[project_sabi_brand]]
