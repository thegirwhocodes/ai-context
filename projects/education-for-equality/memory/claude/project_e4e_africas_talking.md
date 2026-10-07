---
name: project-e4e-africas-talking
description: "Naomi's Africa's Talking account is LIVE (username EduForEquality). The sabi-server container's AT_USERNAME=sandbox is stale voice config, not the account state — stop repeating the sandbox claim."
metadata:
  node_type: memory
  type: project
  originSessionId: e254ca93-523b-4315-b81f-b5801478e21f
  modified: 2026-08-21T19:51:35.327Z
---

# Africa's Talking — the account is live. Stop saying sandbox.

**Verified Aug 20 2026 - e254ca93.** Vercel production for `curriculum-app` holds
`AT_USERNAME="EduForEquality"` (set ~73 days ago) plus a real `AT_API_KEY`. Because
`lib/voice/sms.ts:getSMSProvider()` picks Africa's Talking whenever both exist, **SMS from
the web app already routes through AT, not Twilio.**

**Where the "sandbox" myth comes from, and why it is wrong.** Three sources say sandbox and
none of them is the account:
1. `sabi-server/.env.example` — an example file.
2. The **running sabi-server container** on 136.243.8.51 (`docker exec sabi-server env`) — this is
   the *voice* box. It reads sandbox because **Naomi deliberately moved voice onto the Twilio
   number when Sabi could not hear her on the AT line** (`SABI_SIP_PROVIDER=twilio`,
   caller ID `+17153122345`). That is a product decision she made, not a broken account.
3. `COFOUNDER_BRIEF_THE_LAGOS_SEAT.html` repeated #2.

The voice container's env and the Africa's Talking account are **different systems**. So are the
voice box and Vercel — SMS never touches the Hetzner container at all. Check the system that
actually performs the action before describing its state.

**There IS a Nigerian number.** `NEXT_PUBLIC_SABI_LINE="+234 201 700 1459"`. Naomi's words, Aug 2026:
*"there is a nigerian number, I am just choosing not to use it in this moment, that could change
tomorrow - do not assume you know everything."*

**Two real config defects found Aug 20 2026 - e254ca93** (unfixed at time of writing):
- `AT_USERNAME` value is literally `EduForEquality\n` — a trailing newline is baked into the
  Vercel value and will be sent in the AT auth header.
- `AT_SENDER_ID` is the placeholder string `(leave empty for sandbox)`. `cleanSenderId()` in
  `lib/voice/sms.ts` already strips placeholders (commit `0f747ea`), so sends go out with no
  sender ID rather than failing.

Related: [[feedback-dont-assert-inferences]], [[project-sabi-gemini-live]], [[project-e4e-tech]]

## ⚠️ 20 Aug 2026 — the number is OURS, but dialling it reaches a hospital - 2f1d5115

**Naomi, directly: _"the number is ours - I have an africa's talking account."_** `+234 201 700 1459`
is provisioned to her Africa's Talking account. I briefly concluded the opposite from the outside and
was wrong to — she can see the dashboard and I cannot. Do not repeat that inference.

**The unexplained part:** she dialled it twice today and got a recorded message saying it is a
hospital telephone line. Both facts stand together and the cause is not yet known. Candidates, none
confirmed: the number's voice callback may not point at `trunk:136.243.8.51` so AT never routes the
call to us; the international dialling format may be landing on a neighbouring Lagos landline (the
national form is 020 1700 1459, which the grouping "+234 201 700 1459" invites misdialling); or the
originating leg (she has been calling via Yolla) may be producing the announcement.

**What the server says, and it is consistent with "AT never routes to us":** the Asterisk CDR back to
7 Aug holds 41 inbound calls and every one is `+18604367048` over the **Twilio** leg into
`sabi-inbound`. There has never been SIP traffic from Africa's Talking in the Asterisk log, and
`/asterisk/inbound-route` has never been hit. The box itself is correctly configured to receive:
`at-identify` matches `102.223.37.68`, endpoint `africastalking`, `context=from-at` — the context
that carries flash callback.

**The one test that splits it:** watch the trunk while she dials. An INVITE arriving from
102.223.37.68 means the number is routed to us and the hospital message came from the dialling side.
No INVITE means the number is not pointed at the trunk yet — which is step 1 of
`8. Partnerships & Outreach/AT_SIP_Trunk_Details_2026-06-11.md`, never confirmed as done.

**Still true and still worth fixing before any tester round:** flash callback exists only on the
`from-at` context, so it cannot work until inbound over AT works.

## ✅ 20 Aug 2026, 21:50 UTC — CORRECTION: AT inbound DOES work. The break was outbound. - 1b5d89b4

Verified myself on the box, not from another agent's report.

**AT routes the DID to us. Proven.** `docker logs sabi-asterisk` shows the `from-at` context firing
four times today on `PJSIP/africastalking-*` channels, all dialled to `+2342017001459`:
12:03:39 from `+2349044218460`, then 17:17:46 / 17:18:07 / 17:18:24 from `+2348124724459`.
**Delete the claim "there has never been SIP traffic from Africa's Talking" — it is false.**

**Why that was missed:** the earlier check read the CDR. `/etc/asterisk/cdr.conf` leaves
`unanswered = no` (the default), and every AT leg so far is a flash ring-and-hangup or an
unanswered outbound — none of which writes a CDR row. All 41 CDR rows are Twilio because Twilio
legs are the only ones ever *answered*. **Read the Asterisk log, not the CDR, for AT.**

**The real failure — the callback went out on the wrong carrier.** Each AT flash triggered
`Called +2349044218460@twilio` / `Called +2348124724459@twilio`. Twilio is a **Trial** account with
one verified caller ID (`+18604367048`), so it cannot dial a Nigerian number at all. Those three
callers rang in, hung up, and were never called back.

**Config is now right** (`.env` + container both rewritten 21:16 UTC): `SABI_SIP_PROVIDER=africastalking`,
`SABI_CALLER_ID=+2342017001459`. Trunk plumbing is sound — endpoint `africastalking`, identify match
`102.223.37.68`, `context=from-at`, alaw; ufw allows 5060/udp and RTP 10000-10100 from that IP; zero
auth failures in `/var/log/asterisk/messages`.

**Still unproven: audio over AT.** The only AT outbound ever placed is 18:14:59 →
`Called +18604367048@africastalking` → ringing → making progress → **never answered**. There is no
answered AT call anywhere in the logs, so nobody has yet heard Sabi over this carrier.

**AT account is healthy, not the blocker:** `EduForEquality`, balance **NGN 6,369.07** (queried live).
⚠️ The `AT_API_KEY` in `curriculum-app/.env.local` is dead (401) — only the Vercel **production** key works.

**Side defect found:** the voice box has **no `AT_API_KEY` at all**, so `emergency_alert._send_at_sms()`
returns "not configured" and safeguarding SMS falls through to Twilio trial — i.e. it can only ever
reach her own verified US number.

**The one test that closes this:** with the provider now on AT, have a Nigerian number flash the line
and watch for `Called +234…@africastalking` followed by an *answered* leg.

## ✅❌ 21 Aug 2026, 18:56 UTC — FIRST-EVER ANSWERED AT CALL. She heard silence, not Sabi. - de04c6a7

Verified myself on the box (Asterisk + sabi-server logs), same day, ~1hr before this note.

**A real Nigerian caller, `+2348124724459`, flashed the line and answered the callback.** This is the
first AT leg ever to reach `answered` — proof the whole trunk→flash→callback→AudioSocket chain works
end to end on Africa's Talking. `AS_UUID=fc0727b8…`, new Supabase student row created
(`e2dec2c7-f4e9-401f-979f-2eb2cbdb871b`), realtime session started (not Gemini Live — she's not on
`SABI_GEMINI_LIVE_PHONES`, so she landed in the older `voice_realtime.py` lane).

**Then it broke on TTS, not telephony.** `ElevenLabs TTS failed: 402 Payment Required` (the lapsed
account, confirmed live) → fell back to YarnGPT → `YarnGPT TTS failed: The read operation timed out` →
`RuntimeError: All TTS providers failed`. She got 8 seconds of dead air, AudioSocket then errored
(`Failed to receive frame`), Asterisk hung up. `duration=16 billsec=9 user_turns=0 assistant_turns=1`.
Two minutes later the system auto-retried a second callback (post-hangup trigger) — she didn't answer
this one, presumably having just been burned by silence.

**So: audio over AT is proven to connect. It is not proven to work.** The blocker is exactly what memory
already flagged — `SABI_TTS_PRIMARY=elevenlabs` on a dead account — but this is the first time it cost
an actual Nigerian caller a real (bad) experience, not a hypothetical. Fixing TTS fallback (or flipping
primary off ElevenLabs) is now the single highest-priority item before any tester round starts, since
real inbound traffic is already arriving whether or not testers are recruited yet.

Also noted in passing, not urgent: routine internet vulnerability-scanner noise hit the box around
19:23 UTC (`phpunit eval-stdin.php` probes, dozens of paths) — all correctly 401'd, this is a FastAPI
app with no PHP surface, no action needed.
