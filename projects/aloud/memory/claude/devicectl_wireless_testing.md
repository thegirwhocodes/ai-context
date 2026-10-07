---
name: devicectl-wireless-testing
description: "How to build-install-launch on Naomi's iPhone from this Mac when it looks offline, and how to actually capture crash output since no coreutils timeout exists"
metadata:
  node_type: memory
  type: reference
  originSessionId: cac78b5e-38db-444f-a68b-01a33f14f4e4
  modified: 2026-08-24T17:12:23.266Z
---

"Naomi's iPhone" pairs with this Mac over Wi-Fi (wireless debugging), not USB —
`system_profiler SPUSBDataType` shows nothing for it. `xcrun xctrace list
devices` reports it under "Devices Offline" even when it's fully reachable and
usable; that listing is unreliable for this device. The command that actually
works is:

```
xcrun devicectl list devices
```

which shows it as `available (paired)` with a `.coredevice.local` hostname and
gives the UDID to use everywhere else (as of 2026-08-24:
`00008120-000A3C182146601E`, but re-check since it can rotate).

**Build/install/run loop that works:**
```
xcodebuild -project Aloud.xcodeproj -scheme Aloud -destination "id=<udid>" build
xcrun devicectl device install app --device <udid> <path>/Aloud.app
xcrun devicectl device process launch --device <udid> --console --terminate-existing com.naomiivie.aloud
```

**Why this matters:** this Mac has no GNU coreutils `timeout` installed, so
piping the `--console` launch through `timeout N` fails silently with
"command not found" and captures nothing. Instead run the launch command in
the background (redirected to a log file) and just read the log file after
the user reproduces the behavior — the console session naturally ends when
the app terminates (crash, force-quit, or `App terminated due to signal 9`),
so no manual timeout is needed. Each reproduction needs a fresh
`--terminate-existing` launch since the previous console stream already
exited.

**How to apply:** default to `devicectl`, not `xctrace`/`instruments`, for
anything involving this iPhone. Never trust an "offline" status from `xctrace`
alone before checking `devicectl list devices`.
