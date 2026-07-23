---
name: kai-timing-model
description: "Kai's focus timing = classic Pomodoro by default + lock-in budget as the headline flow"
metadata:
  node_type: memory
  type: project
  originSessionId: b3fd697b-dd3d-4bcd-aed8-b72e974fe3c6
  modified: 2026-07-23T20:20:33.348Z
---

Naomi's direction for Kai's focus timing (decided 2026-07-23, shipped):

- **Classic Pomodoro is the default.** `DEFAULT_SETTINGS.adaptive = false`. Block lengths come from the user's own focus/break settings, fixed and predictable. The adaptive engine (time-of-day + focus-rating shaping in `src/lib/adaptive.ts`) is an opt-in "let Kai tune it" toggle, NOT the default. Do not flip it back to adaptive-by-default.
- **Lock-in budget is the headline feature.** User commits to a total stretch ("lock in for 2 hours"); `planLockIn` in `src/lib/lockIn.ts` lays out the whole focus+break sequence, always ending on a focus block, absorbing slack into the final focus so the budget is exact. Runs hands-free via autopilot; `start_lock_in` voice tool. This is the primary focus flow — an endless focus/break treadmill is the anti-pattern.
- **Never invent durations.** The old "Kai always says 15-minute break" bug was because the agent state snapshot didn't include the user's break lengths, so Haiku fell back to textbook Pomodoro's 15. State now carries all block lengths + mode + lock-in progress; the prompt forbids stating any duration not in state or a tool result.

**Why:** Naomi wanted the true Pomodoro spirit (commit to a chunk, see it through) and full user control over lengths, not a canned adaptive treadmill.

**How to apply:** Keep classic controllable timing as the floor; lock-in as the hero. Any new timing logic must surface real numbers from settings, never templated/invented values.
