---
name: businesses-portfolio-governance
description: "Full multi-business governance mechanism (Owner's Manual, Accountability Chart, Scorecard, Monthly Report per business + holdco-level manual) built 2026-08-25 for all 11 of Naomi's active businesses"
metadata:
  node_type: memory
  type: reference
  originSessionId: 575a89df-83e2-48ea-a7b9-8b60336e9a8f
  modified: 2026-08-25T19:27:28.035Z
---

On 2026-08-25, a full governance mechanism was built for Naomi's business portfolio, following the framework in [[operating-systems-multi-business-framework]] (`/Users/naomiivie/businesses/research/04-operating-systems.md` §13). Lives at `/Users/naomiivie/businesses/portfolio/` in the `thegirwhocodes/businesses` repo (committed + pushed).

**Structure:** `portfolio/<business-id>/{OWNERS-MANUAL,ACCOUNTABILITY-CHART,SCORECARD,MONTHLY-REPORT-TEMPLATE}.md` for each of 11 businesses, plus `portfolio/HOLDCO-OWNERS-MANUAL.md` at the top level synthesizing across all of them. `portfolio/_FRAMEWORK.md` is the spec all 11 were built against — read it before adding a 12th business or updating an existing one.

**The 11 businesses (id: name):** cortex (Cortex + Sage Mail), kai (Kai), sabi-e4e (Sabi/Education for Equality), design-portfolio (naomiivie-design), go (Go/Class on Time), sage-desktop (Sage desktop), bethel (Bethel), edit (Ed.it), adjutant (Adjutant), aloud (Aloud/ReadOut — newly discovered, not in the older Holdco Command seed), motivation-alarm (Motivation Alarm — newly discovered).

**Older, 3-weeks-stale source still worth knowing about:** `/Users/naomiivie/businesses/apps/holdco/src/lib/store.ts` has an Aug 4 2026 hardcoded seed (`realPortfolio()`) for 9 of these businesses (missing aloud and motivation-alarm) — used to bootstrap Holdco Command's localStorage dashboard. It was the starting point for this research but has since been superseded by the fresher per-business docs above.

**Cross-portfolio pattern found (the actual headline finding, not just documentation):** every one of the 11 businesses had a decision correctly identified weeks earlier that still hadn't been acted on by 2026-08-25 — the portfolio's bottleneck is follow-through, not analysis. Concrete unresolved items as of this date, most urgent first:
- **Cortex:** plaintext credentials (Meta/Stripe/S3/Sentry/RunPod/Vercel) still sitting in `~/cortex/*.rtf`, flagged URGENT on Aug 4, still unrotated. Also an unfixed cross-tenant bug where Meta/Instagram webhook messages can misroute to the wrong user.
- **Sabi/E4E:** no written kill-the-pilot safety criteria; backup child-safeguarding contact (Dr. Sonia Ivie) hasn't signed the DPIA.
- **Sage (desktop) vs. Sage Mail (Cortex):** naming collision between two live products, unresolved.
- **Go:** the "pick a ship-or-shelve date now" instruction was never acted on; the $100 auto-charge mechanism has no confirmed legal/consumer-protection review.
- **Bethel:** "business or personal" still unanswered; scope grew anyway (3 new uncommitted side-experiments).
- **Ed.it:** was marked "parked" based on a stale read of its own git history — its actual last commit shipped real progress on Naomi's top-priority feature (word-by-word captions).
- **Design Portfolio:** hours/week cap still undecided — the one business with real revenue is also the one silently eating time the pre-revenue ventures need.

**How to apply:** When Naomi asks about any of these 11 businesses, check the relevant `portfolio/<id>/` docs first — they're fresher and more grounded than the Aug 4 seed. When she asks about portfolio-wide strategy, time allocation, or "what should I focus on," the holdco manual's synthesis (the follow-through pattern above) is the load-bearing insight, not any single business's status.
