---
name: sleep-well-intent
description: "Founding spec/intent for the \"Sleep Well\" (ShutdownApp) digital-bedtime app"
metadata:
  node_type: memory
  type: project
  originSessionId: 4b7a31d6-b579-4a4a-a44c-63b602b3158c
---

"Sleep Well" (dir: /Users/naomiivie/Downloads/App/Sleep) is a native Apple digital-bedtime / screen-time-discipline app. Founding intent, voice-dictated by Naomi 2026-06-05:

- Runs across **all her devices** (iPhone, iPad, Mac), **synced** like Apple settings sync.
- At a scheduled bedtime it **shuts down / blocks everything**.
- Early unlock is gated by an **AI agent ("Sage")**: a "key" giving ~**3 tries per week**. To unlock early you must **prove/verify your reason**; Sage **reads her Gmail** to judge whether the reason is genuine/urgent, then grants/challenges/denies.
- Sage reuses the **bethel/email-agent** backend (`~/bethel/email-agent`, endpoint `POST /api/verify-unlock`, prompt `prompts/unlock-gatekeeper.md`). Backend stays **local only** (holds API key + reads email) — reachable via LAN/Tailscale, never public.

Architecture: macOS app `ShutdownApp` ("Sleep Well") + iOS app `SleepWelliOS` + 3 Screen Time extensions (DeviceActivityMonitor, ShieldConfiguration, ShieldAction). Cross-device state via iCloud `NSUbiquitousKeyValueStore` mirrored to App Group `group.com.sleepwell.shared` ([[sleep-well-architecture]]). Team `7RTTC5R7ZQ`. Not a web app — **git applies, Vercel/Sentry do not**.
