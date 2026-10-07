---
name: sleep-well-ios-bundle-id
description: The iOS app ships as com.naomiivie.sleepwell because com.sleepwell.ios is unavailable in the Apple portal
metadata:
  node_type: memory
  type: project
  originSessionId: 7ded354b-7e8f-4a5f-8a3c-8765a916a55d
  modified: 2026-08-15T20:33:02.755Z
---

Sleep Well's iPhone app builds and signs as **`com.naomiivie.sleepwell`**, not `com.sleepwell.ios`.

`com.sleepwell.ios` was never registered and **cannot** be — the Apple Developer portal returns
"not available", so the name is held elsewhere. Its three Screen Time extension children *were*
auto-created by Xcode (they appear as `XC com sleepwell ios ...`), while the parent silently fell
back to the `XC Wildcard` `*`, which cannot carry the Family Controls entitlement. That mismatch is
why device builds failed for months with confusing provisioning errors.

The rename is cheap and does **not** cascade: `group.com.sleepwell.shared` and the iCloud KVS
identifier `$(TeamIdentifierPrefix)com.sleepwell.shared` are independently registered identifiers
that merely share the word "sleepwell". Neither derives from the bundle ID, so renaming the app
leaves the App Group membership and iCloud container untouched.

Apple team is `7RTTC5R7ZQ` (Naomi Ivie, Individual, paid). Family Controls **development** has been
granted since 2026-06-18. **Distribution** appears to be granted too — the portal shows its
checkbox ticked — but that was never confirmed by generating a distribution profile and inspecting
it for `com.apple.developer.family-controls`. A development profile carrying the key proves nothing.

Related: [[sleep-well-canonical-checkout]]
