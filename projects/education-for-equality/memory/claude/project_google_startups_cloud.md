---
name: project-google-startups-cloud
description: "E4E's Google for Startups Cloud Program application — submitted 12 Aug 2026; what it's worth, what the domain/billing setup was, and what to watch for."
metadata:
  node_type: memory
  type: project
  originSessionId: 1f5e4922-dac1-47db-927f-e6ffa3f36d07
  modified: 2026-08-12T16:17:22.144Z
---

# Google for Startups Cloud Program — submitted 12 Aug 2026

**Status: application submitted.** Google says expect a response in **3–5 business days**, or **7–10 extra days** if the billing account ID was newly created.

**What it's worth:** up to $200k in cloud credits over 2 years ($350k for AI startups), covering Google models like Gemini and Gemma — directly relevant now that Sabi's phone lane runs on Gemini Live. Acceptance also unlocks **Google Workspace Business Plus free for 12 months**, redeemed separately after approval. ⚠️ Do **not** buy a paid Workspace plan — the domain must not have had paid Workspace from 31 days before the application until the benefit is requested, or the perk is forfeited.

**Setup done to satisfy the domain-match rule (Aug 8, codex `019fe2d7`):** the form requires the Cloud Billing admin's email domain to match the startup website domain (`eduforequality.org`). Created **Cloud Identity Free** (not Workspace) for the domain, made `naomi.i@eduforequality.org` a **Billing Account Administrator**, and used Cloudflare Email Routing to forward that address to her Gmail, since Cloud Identity gives a login but no mailbox.

**Open risk to check on approval:** the original billing account `01EFFF-8F65FD-23AC6E` was created under her **Wesleyan-managed** Google identity, so Google treats it as Wesleyan's — it could not be migrated to an E4E organisation, and the advice was to create a fresh company billing account under the `eduforequality.org` org and link only E4E/Sabi projects. That account also contained unrelated projects (`qac386-class`, Spheres App, Cortex, Calendar Scheduler) which would otherwise consume startup credits. **Confirm which billing account the submission used** — if it was the Wesleyan-parented one, the credits land somewhere she loses at graduation. Same trap flagged for Azure in [[project-sabi-numeric-sidecar]].

Related: [[project-e4e-vision]], [[reference-e4e]]
