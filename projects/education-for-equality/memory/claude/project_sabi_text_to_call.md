---
name: project-sabi-text-to-call
description: "Text or WhatsApp CALL and Sabi rings you back — built Aug 20 2026. Guards fail closed; allowlist is Naomi's number only. Proven working end to end over the Africa's Talking trunk."
metadata:
  node_type: memory
  type: project
  originSessionId: e254ca93-523b-4315-b81f-b5801478e21f
---

# "Text CALL and Sabi rings you" (built Aug 20 2026 - e254ca93)

**Why it exists.** The Twilio inbound leg answers immediately, so a Nigerian tester dialling the
US line pays international rates, and Asterisk's flash-callback route is wired only into the
`from-at` context. A text was the only free way for a tester to ask for a lesson.

**Shape.** `curriculum-app/lib/voice/call-request.ts` — `requestSabiCall()` POSTs to the voice
server's `/admin/asterisk/direct-call` with `X-API-Key`. Channel-agnostic on purpose. Two webhooks
call it: `app/api/sabi/sms/incoming` (Africa's Talking) and `app/api/sabi/whatsapp/incoming`
(Twilio, replies in TwiML). Intent classification + keyword stripping live in
`lib/voice/inbound-intent.ts` so the channels cannot drift. Keywords: CALL / CALL ME / RING / LESSON / TEACH.

**Guards fail CLOSED — each accepted message spends money on a call.**
`SABI_CALL_REQUEST_ALLOWLIST` unset authorises nobody; cooldown `SABI_CALL_REQUEST_COOLDOWN_SECONDS`
(default 180); daily cap `SABI_CALL_REQUEST_DAILY_LIMIT` (default 8). Both counted from
`sabi_sms_log` rows of type `call_request_dispatched`, NOT process memory — the webhook runs on
serverless instances that do not share state. The dispatch row is written only after the voice
server accepts, so a refusal does not burn the caller's allowance.

**Vercel prod env set this session:** `SABI_SERVER_URL=https://api.eduforequality.org`,
`SABI_CALL_REQUEST_ALLOWLIST=+18604367048` (her number only). `SABI_API_KEY` already existed and
its hash matches the box's `secrets/SABI_API_KEY`.

**PROVEN end to end Aug 20 2026.** Simulated inbound WhatsApp → `call_request` → dispatch →
`Direct Sabi call requested ... provider=africastalking` → `Called +18604367048@africastalking` →
`PJSIP/africastalking-00000030 is ringing`. **Africa's Talking accepted an international leg to a
US number** — I predicted it might refuse; it did not. Not answered (her number was down), so the
lesson audio itself is still unproven on this path.

**Twilio config I changed via the Senders API** (creds are NOT readable from Vercel — marked
Sensitive there; they live on the Hetzner box at `secrets/TWILIO_AUTH_TOKEN` + `.env`):
- WhatsApp sandbox sender `XE5ba2ae54ac9df8ed909a7b01a7e16af8` (`whatsapp:+14155238886`) inbound
  webhook was still Twilio's stock demo (`timberwolf-mastiff-9776.twil.io/demo-reply`) → now the
  Sabi route. Sender flipped `OFFLINE` → `ONLINE`.
- `+17153122345` `sms_url` had no `?key=`, so every inbound SMS was being 403'd → fixed.

**Twilio account facts (Aug 20 2026):** type **Trial**, balance **$5.08**, exactly one verified
caller ID (`+18604367048`) — a trial account dials only verified numbers, so Twilio could never
have called a Nigerian tester. Nigeria termination is **$0.2263/min** (Elastic SIP) /
**$0.2349/min** (Programmable Voice). 5 testers × 5 days × 1 call × 7 min ≈ $40; at the 8/day cap
≈ $317. This cost is what drove the switch back to AT.

**No real inbound SMS has ever reached the webhook** — every inbound row in `sabi_sms_log` before
today was a synthetic smoke test from Jul 6. If the AT shortcode is *shared*, `SABI_SMS_KEYWORD`
must be set or "SABI CALL" never matches the trigger.

Related: [[project-e4e-africas-talking]], [[project-sabi-gemini-live]], [[project-sabi-identity]]
