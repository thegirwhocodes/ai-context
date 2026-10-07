---
name: project-e4e-workspace-free-paths
description: "The three routes to a free Google Workspace on eduforequality.org, which are open/closed, and the Jan 2027 Gmail send-as deadline that kills the current free workaround."
metadata:
  node_type: memory
  type: project
  originSessionId: 9686b9ea-08c0-4b7f-b1a3-0fb871e10883
---

# Free Google Workspace for E4E — the three routes (researched 18 Aug 2026)

**1. Google for Startups Cloud — ❌ REJECTED 18 Aug 2026. Structurally ineligible, do not retry.** Google's own FAQ: *"Google Cloud may not accept companies that have IPO'd or been acquired, **educational institutions**, government entities, **nonprofits**, personal blogs or content, dev shops, consultancies, agencies, cryptocurrency mining companies..."* E4E hits two of those named exclusions and `eduforequality.org` says "nonprofit" and "free" on the homepage. This was a category rejection, not a fixable application — reapplying with a better site will not change it. Escalation contact if ever needed: `cloudstartupsupport@google.com`. Original terms, now moot: Approval unlocks **Workspace Business Plus free 12 months**, redeemed via a separate benefit-request form after acceptance. Condition: the domain must not carry a paid Workspace subscription (Google states this as 90 days in the benefits copy, 31 days elsewhere — safe read: **buy nothing on `eduforequality.org` until redeemed**). Must be a **monthly** plan, not annual. Start tier = founded <5 yrs, no institutional funding, no prior GCP credits beyond free trial — E4E qualifies. Applied 12 Aug 2026, see [[project-google-startups-cloud]]. Time-boxed: 12 months only.

**2. Google for Nonprofits — NOW THE ONLY REAL PATH. Free forever, blocked on incorporation.** Workspace for Nonprofits edition = $0, 100 TB pooled storage, Gemini + NotebookLM, up to 300 users (2,000 on request), 4 secondary domains. Requires a registered charity verified by **Goodstack** (renamed from Percent). US = own IRS 501(c)(3) determination; **fiscally sponsored orgs without their own 501(c)(3) are explicitly ineligible** — no shortcut. Nigeria is an eligible country; Goodstack accepts a **CAC Certificate of Incorporation** (Incorporated Trustee). E4E has filed neither — `7. Legal & IP/LEGAL_ROADMAP.md` is still all `[ ] Not started`. ⚠️ Exclusion risk: "A school, academic institution, or university (philanthropic arms of educational organizations are eligible)" — apply as a charity that provides free learning, never as a school/tutoring service.

**3. Google Workspace for Education — CLOSED.** Requires "government-recognized, accredited schools delivering instruction"; tutoring programs, supplemental/non-formal providers, language schools and for-profit education companies are explicitly excluded. Consistent with [[project-curriculum-accreditation]] (nobody accredits a self-authored curriculum).

## ⚠️ The current free workaround has an expiry date
Today's setup — Cloud Identity Free + Cloudflare Email Routing forwarding `naomi.i@eduforequality.org` to Gmail, with Gmail "Send mail as" for outbound — **dies in January 2027**. Google is retiring "Send as" for third-party addresses (plus Gmailify and web POP fetch); the notice period runs through Q3/Q4 2026 and **new send-as configurations are already being blocked**. Receiving/forwarding into Gmail is unaffected; Workspace "Send as" is unaffected. So set up any send-as NOW or lose the option, and treat a real Workspace (route 1 or 2) as the destination rather than a nice-to-have.

Cloud Identity Free does **not** count as paid Workspace and does not jeopardise route 1 — adding a Workspace subscription to the existing Cloud Identity org is the normal upgrade path (Admin console → Billing).

Related: [[project-google-startups-cloud]], [[reference-e4e]], [[project-e4e-vision]]


## Consequences of the 18 Aug 2026 rejection
- The "**don't buy Workspace**" handcuff is **gone** — it only ever existed to protect the startup benefit. Buying now costs nothing strategically.
- If she buys an interim paid plan, it **must be Business Starter**. Only Nonprofits-trial, **Business Starter**, or legacy G Suite Basic convert to Workspace for Nonprofits; Business Standard/Plus/Enterprise must be downgraded to Starter first (or negotiated via Workspace Support).
- Google Cloud credits for nonprofits: third parties cite ~$10k/yr, but Google's own nonprofit Cloud-credits page states no dollar figure — **unverified, don't quote it in applications**.
- Incorporation (EIN → CT 501(c)(3), or Nigerian CAC Incorporated Trustee) is now the gate on free Workspace, not just a legal chore.
