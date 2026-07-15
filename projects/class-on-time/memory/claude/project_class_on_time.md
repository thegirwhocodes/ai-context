---
name: Class on Time project
description: Personal commitment-device app — reads calendar, alerts user to leave for class 30 min early, charges $100 via Stripe when late
type: project
originSessionId: a8c172f1-a7d4-4624-8ac2-b31c78a6f870
---
**App concept:** "Uber for walking to class" — when a calendar event with a different physical location is approaching, the app pops up "start heading to your destination" early enough that the user can arrive **30 minutes before** the event starts. Every time she arrives less than 30 minutes early, the app automatically charges **$100** to a configured destination (charity / external wallet — exact recipient TBD by user).

**Why:** Commitment device for personal punctuality. The penalty is the entire point — the app is useless if she can dodge it. So anti-escape design (lockups, can't easily delete payment method) is a first-class feature, not an afterthought.

**How to apply:**
- Architecture: Expo mobile app (iOS first) + Next.js on Vercel + Postgres + Stripe (Apple Pay + Plaid/Financial Connections for Bank of America ACH). Blockchain (Base/USDC) is a **stretch goal**, not MVP — user okayed dropping it in favor of Stripe for speed.
- Anti-escape: 7-day lockup before a connected payment method can be removed. User explicitly asked for this — design every "remove / disconnect / disable" path with a delay, not an instant action.
- Visual style: cute sprite avatar walking on an illustrated/cartoon-styled map (Mapbox custom style), Pokemon-Go feel. Do not ship an "adult-looking" Uber-style UI.
- Trigger logic: `departure_time = event_start - 30min - walking_eta`. Vercel Cron checks every minute; Expo Push fires when departure_time ≤ now.
- "On time" = physically arrived (geofence) at event location ≥ 30 minutes before event_start. Anything less = late = $100 charge.
- iOS first — Apple Pay was specifically requested.
