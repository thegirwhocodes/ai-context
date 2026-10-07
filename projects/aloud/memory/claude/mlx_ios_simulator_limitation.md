---
name: mlx-ios-simulator-limitation
description: "MLX/Kokoro on-device TTS cannot build-link or run on iOS Simulator; must test on a physical device, and MLX's Metal buffer cache must be bounded to avoid jetsam kills"
metadata:
  node_type: memory
  type: project
  originSessionId: cac78b5e-38db-444f-a68b-01a33f14f4e4
  modified: 2026-08-24T17:11:53.538Z
---

Aloud's on-device natural voice (Kokoro-82M via mlx-swift) cannot be built or run
on the iOS Simulator on this machine. The `Cmlx` target fails to link with
undefined Metal symbols (`MTLIOErrorDomain`, `MTLTensorDomain`) against the
iOS 26.5 Simulator SDK — confirmed pre-existing on a clean `main` checkout, not
caused by any Aloud code change. mlx-swift's own docs (`running-on-ios.md` in
the checked-out package) confirm MLX requires a real Metal GPU family the
Simulator doesn't provide.

**Why:** MLX/Metal compute (matmul, conv, attention) isn't supported in the iOS
Simulator's Metal implementation at all — this is a hard platform limitation,
not a project bug. `KokoroSpeechEngine.isSupported` already returns `false`
under `targetEnvironment(simulator)` for this reason.

**How to apply:** Any future work on the Kokoro/MLX speech path must be
verified by building straight to a physical iPhone (`xcodebuild -destination
"id=<device-udid>"`), never the Simulator. See [[devicectl-wireless-testing]]
for how to reach the device even when it looks offline.

Separately: MLX's Metal buffer cache is unbounded by default and grows fastest
exactly with TTS-shaped workloads (variable-length utterances don't reuse
fixed-size buffers the way LLM token generation does). Left uncapped, this
caused a real on-device SIGKILL (jetsam) after ~2s of playback the first time
synthesis actually ran end-to-end. Fix applied in
`Aloud/Speech/KokoroSpeechEngine.swift`: set `MLX.Memory.cacheLimit` once after
model load (32 MB) and call `MLX.Memory.clearCache()` after each render once
samples are copied out. If memory pressure resurfaces, tune the cache limit
value or add the "Increased Memory Limit" entitlement — both are documented in
mlx-swift's `running-on-ios.md`.
