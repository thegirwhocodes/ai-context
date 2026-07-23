---
name: project-sabi-monitoring
description: "Sabi 'never miss a user error' monitoring — Phase 1 live: user-facing error capture + daily WhatsApp/email health digest; plan doc + what's still pending"
metadata:
  node_type: memory
  type: project
  originSessionId: 818cc1ed-6045-471b-857a-9578e15ba868
---

# Sabi Monitoring — "no user error ever slips" (session 818cc1ed, Jul 23 2026)

Goal: autonomous monitoring for a **non-technical owner** — every user-facing failure captured,
brought to Naomi in plain English, agent does the work. Plan doc:
`curriculum-app/docs/SABI_NEVER_MISS_AN_ERROR_PLAN.md` (auto-heal-first, interrupt-rarely, lock-proof).

**Core insight:** the login bug that started this was NOT a crash — the app just showed "wrong
password." So capture must include *handled* user-facing errors, plus a synthetic "robot user", plus
a self-watching dead-man's switch. (The login account itself was a June shell with no login identity;
deleted so Naomi re-signs up clean. Real-user signup→confirm→login was verified working end-to-end.)

## Phase 1 — LIVE on prod (curriculum-app)
- `lib/monitoring/report.ts` `reportUserFacingError(flow, msg, extra)` → Sentry `captureMessage`
  tagged `user_facing:true` + `flow`. Wired into sign-in (password / magic-link / Google) — the exact
  silent-failure class. (Sign-up + sign-off still TODO to wire.)
- `lib/monitoring/alert.ts` `sendAlert(title, body, severity)` → **dual channel: WhatsApp (Twilio) +
  email (Resend)**. One channel failing can't lose an alert (lock-proof backup).
- `app/api/monitoring/daily-digest/route.ts` + `vercel.json` cron `0 13 * * *` (Vercel **Hobby** =
  once/day max). Reads BOTH Sentry projects, pings uptime, sends plain-English digest. Cron-secret
  protected; `?test=1` to trigger manually. **Verified end-to-end Jul 23: email delivered, WhatsApp
  delivered + read.**

## Keys / config (Vercel prod env, set this session)
- `MONITORING_SENTRY_TOKEN` = Naomi's personal token `sntryu_…` (scopes issues:read + alerts:write +
  project:write; user naomi.ivie04@gmail.com). ⚠️ was pasted in chat — consider rotating.
- Sentry org = **`sabi-43`**; projects = **`javascript-nextjs`** (website/sign-in) + **`sabi-server`**
  (phone pipeline, python-fastapi). Also cortex-web in same org.
- `MONITORING_ALERT_EMAIL` = naomi.ivie04@gmail.com. `CRON_SECRET` set (value in session scratchpad).
- Twilio (from curriculum-app/.env.local): `TWILIO_ACCOUNT_SID`/`TWILIO_AUTH_TOKEN`, number
  +17153122345. WhatsApp via **sandbox**: `TWILIO_WHATSAPP_FROM=whatsapp:+14155238886`,
  `MONITORING_WHATSAPP_TO=whatsapp:+18604367048` (Naomi joined the sandbox; delivery confirmed).
- The pre-existing `SENTRY_AUTH_TOKEN` on Vercel is **source-maps-only** (401 on issues) — that's why
  we added the separate personal token.

## Pending (Phase 2/3)
- Wire sign-up + sign-off + dashboard error paths to `reportUserFacingError`.
- **Real-time** alerting (Hobby cron is daily-only): Sentry alert rule/webhook → `/api/monitoring/…`
  → `sendAlert`, OR a scheduled cloud agent polling every ~30min. Token can create alert rules.
- **Robot user** synthetic journey (signup→login→dashboard→sign-off) + phone canary + email-delivery
  check. **Uptime** frequent pings need a free cloud monitor (Hobby can't do minute-by-minute).
- **Two-way WhatsApp**: Twilio receives replies (confirmed) → inbound webhook → "reply OK to approve
  a fix" one-tap loop.
- **Dead-man's switch** (alert if the monitor itself stops) + **auto-heal** (restart/rollback) — the
  lock-proof + "don't rely on Naomi watching" layers she explicitly asked for.
- Upgrade WhatsApp sandbox → production sender before the real pilot (sandbox session can lapse).

Related: [[project-e4e-tech]] [[project-sabi-status-jul2026]] [[feedback-verify-by-driving]]
