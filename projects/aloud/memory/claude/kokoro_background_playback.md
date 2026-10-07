---
name: kokoro-background-playback
description: "Why Kokoro-82M natural voice can't keep synthesizing once Aloud/PDF Voice is backgrounded, what was tried, and why the CoreML/ANE route is also blocked"
metadata:
  node_type: memory
  type: project
  originSessionId: cac78b5e-38db-444f-a68b-01a33f14f4e4
  modified: 2026-08-28T00:00:56.173Z
---

Natural voice (Kokoro-82M) synthesis cannot continue once the app is backgrounded,
and this is not fixable from application code. Two independent walls, both dead
ends, investigated 2026-08-24:

**MLX/Metal (the shipped path):** iOS unconditionally refuses to let a
backgrounded app submit Metal command buffers — confirmed via a real crash log:
`libc++abi: ... [METAL] Command buffer execution failed: Insufficient Permission
(to submit GPU work from background) (kIOGPUCommandBufferCallbackErrorBackground
ExecutionNotPermitted)`. The "audio" `UIBackgroundModes` entitlement only grants
continued *CPU* execution, never GPU. Forcing MLX to run inference on CPU
(`MLX.Device.setDefault(device: Device(.cpu))`) does avoid the crash — measured
~114s of CPU compute for 2.7s of audio, ~43x slower than realtime — completely
unusable. (An earlier "CPU renders at ~4x realtime in the background" reading
was a measurement artifact: the old fallback-to-system-voice code was still
active during that test and pre-empted the render before the app was actually
backgrounded, so it was silently measuring GPU work, not CPU.)

**CoreML/ANE (investigated as the "real" fix, then abandoned):** Apple's Neural
Engine via Core ML *is* explicitly permitted to keep running in the background
(this is how Speechify and similar apps do on-device background narration).
Several community CoreML ports of Kokoro-82M exist (`mweinbach/kokoro-swift`,
`FluidInference/FluidAudio`'s `KokoroAneManager`, `mattmireles/kokoro-coreml`),
and FluidAudio even declares proper `.iOS(.v17)` support and is used in
production by a very similar app ("Local Narrator"). It was integrated far
enough to resolve/build cleanly via SPM before this was found in FluidAudio's
own source: `KokoroAneManager.isBnnsCrashProneOS` returns `true` for **all**
iOS 26.4+ (their comment: "on iOS the 26.6 line still crashes"). Confirmed via
three separate FluidAudio GitHub issues (#328, #587, #817) that this is a
**crash inside Apple's own `libBNNS.dylib`** (`BnnsCpuInferenceOperation`),
not a FluidAudio bug — Kokoro's StyleTTS2 architecture uses LSTM layers that
CoreML routes through this same OS framework on iOS regardless of which Swift
wrapper is used, so switching to a different CoreML port would not have
avoided it. Issue #817's most damning finding: the *identical binary* on the
*identical device* flipped between 100% pass and 100% crash across the same
day with no identifiable trigger (not thermal, not memory — "environmental
state we could not identify"). Not something an app can test around or contain.

**Shipped fix instead:** `Narrator.handleDidEnterBackground()` /
`handleDidBecomeActive()` (wired from `AloudApp.swift`'s `scenePhase`
handling) seamlessly switches to the system voice the instant the app
backgrounds, and back to Kokoro when foregrounded again. No dead air, no
crash; natural-voice quality just isn't available while backgrounded.

**Correction, 2026-08-24 (same day, follow-up): there IS a without-FluidAudio
path that plausibly works — ONNX Runtime, CPU execution provider.**
Both MLX-CPU (~43x slower than realtime, measured in this repo) and
CoreML/ANE (crashes) were ruled out above, but both are Metal/BNNS-specific
dead ends, not proof CPU synthesis in general is too slow. Found via an
independent app (`dfakkeldy/Echo`, a similar EPUB/audiobook reader) that hit
the *same* CoreML/ANE Kokoro wall (crashes + ~20min on-device AOT compile on
an A14) and pivoted entirely off CoreML to ONNX Runtime CPU EP
(`docs/superpowers/research/2026-06-19-kokoro-onnx-pivot-decision.md` in that
repo, a 30-agent research brief). Their measured result on an **iPhone 12
Pro / A14 (2020, weaker than any device this app targets)**: RTF ≈ 0.8 (i.e.
close to realtime) using `onnx-community/Kokoro-82M-v1.0-ONNX`'s
`model_fp16.onnx` (163 MB, confirmed live on HuggingFace, Apache-2.0,
includes every English/British voice this app already lists) via
`microsoft/onnxruntime-swift-package-manager` (confirmed live, MIT, iOS 16
floor). Key mechanism: ORT's CoreML execution provider can't handle Kokoro's
dynamic shapes and falls back to the CPU EP **by construction** — the model
physically cannot touch the ANE/BNNS crash path, and critically, pure CPU
compute is exactly what the `audio` UIBackgroundModes CPU grant already
permits indefinitely (that's the same grant this app's existing
foreground/background system-voice swap already relies on). This app already
depends on MisakiSwift for G2P (front-end phonemization), which Echo reused
verbatim for its ONNX engine too — so the front-end doesn't need to change,
only the model-execution runtime (MLX → ONNX Runtime CPU EP), and FluidAudio
can be dropped entirely.

**Not yet verified for this app specifically:** the single gating unknown
Echo's own brief flags is on-device RTF, which is device-specific — needs a
real on-device spike on the actual target hardware before committing,
exactly as their brief did before adopting it. Also unverified: whether ORT
CPU synthesis running from a background queue while AVAudioEngine holds the
audio session actually avoids iOS's background CPU throttling long enough
for sustained multi-minute narration (plausible given the `audio` background
mode's indefinite-execution grant, but not yet confirmed against a real
device in this repo).

**2026-08-27 update: shipped anyway, then flagged pre-submission.** A
different concurrent session (`aloud-00`) committed `dff5973` ("Replace MLX
natural voice with CoreML (background-capable)") — deleted the MLX engine
entirely, replaced it with FluidAudio's Kokoro-ANE forced to `.cpuOnly`,
commit message claims "verified on-device across dozens of consecutive
renders and multiple voices while backgrounded, no crash." This directly
contradicts issue #587 (cpuOnly crashes identically to default routing) and
ignores #817's own finding that the bug is time/environment-gated — a clean
test session is exactly what precedes a flip to crashing, not evidence of a
fix. Surfaced this to `aloud-00` via cross-session message before Naomi's
first App Store submission (with a paid lifetime-unlock IAP) archives a
build on this commit. **If you're reading this in a future session: check
whether dff5973 (or whatever superseded it) actually shipped, and whether
any post-launch crash reports came in from iOS 26.4-26.6 users during
background narration** — that would be the real-world verdict on this
argument. Also found: 3 other Claude sessions (`aloud-7d`, `aloud-00`,
`aloud-0f`) were concurrently editing this same working tree same evening —
worth checking with Naomi whether multiple sessions on one repo is
intentional collaboration or accidental overlap before assuming a clean
working tree.

**How to apply:** Don't re-attempt CoreML/ANE for Kokoro specifically unless
Apple ships a fixed iOS release (check FluidAudio's `isBnnsCrashProneOS` for
the current cutoff) — the underlying OS bug, not the wrapper library, is the
blocker. A genuinely different TTS architecture without LSTM/BNNS-routed
CoreML layers (e.g. FluidAudio's separate PocketTTS backend) is a real,
separate research question if background natural voice is revisited.

**Follow-up research, 2026-08-24 (live GitHub check against FluidAudio
main/v0.15.6, still current):**

- `isBnnsCrashProneOS` (Sources/FluidAudio/TTS/KokoroAne/KokoroAneManager.swift)
  confirms macOS 26.6 fixed the bug but **iOS stays flagged for the entire
  26.4+ line with no ceiling** (`onMacOS ? version.minorVersion <= 5 : true`),
  reconfirmed by a newer issue #844 that iOS 26.6 still reproduces the exact
  same libBNNS SIGSEGV macOS 26.6 fixed. This app's target platform (iOS) has
  no fixed build to wait for yet — the memory's original conclusion still
  holds, not just an inference from March/July issues.
- **The loophole itself has a posted expiration date.** Apple's iOS 27
  release notes (surfaced via FluidAudio issue #738, quoting
  developer.apple.com/documentation/macos-release-notes/macos-27-release-notes):
  "The system now restricts background access to the Neural Engine, similar
  to GPU usage restrictions." I.e. the ANE-in-background exemption this whole
  research question hinges on is being closed by Apple itself, independent of
  the libBNNS crash. Any CoreML/ANE background investment made now is
  building against a wall Apple is already erecting.
- **PocketTTS (Kyutai, via FluidAudio) is a real different-architecture
  candidate but not a clean win:** its own docs
  (Documentation/TTS/PocketTTS.md) say only `flow_decoder_fused` actually
  runs on ANE — `cond_step`/`flowlm_step` run on **GPU** (their rank-5
  KV-cache `scatter` op is rejected by the ANE compiler at any precision) and
  `mimi_decoder` runs on CPU. A GPU-routed CoreML submodel likely hits the
  exact same `kIOGPUCommandBufferCallbackErrorBackgroundExecutionNotPermitted`
  wall as MLX — CoreML routing to GPU still means Metal command buffers under
  the hood. Unverified in this repo; would need an on-device background test
  before trusting it, same as Kokoro was.
- **The practically buildable win found instead: deepen the pre-render
  lookahead.** Today `Narrator.prepareNext(after:)` in Narrator.swift:320
  renders exactly one sentence ahead. PCM at 24kHz mono float32 is ~96 KB/s,
  so buffering several minutes ahead (render a whole paragraph/chapter while
  foregrounded, e.g. while the screen is on or charging) costs single-digit
  MB of RAM. Since *playing* already-rendered audio via AVAudioEngine needs
  no GPU/ANE work at all — only the existing `audio` UIBackgroundModes CPU
  grant — a deep-enough buffer makes the common case (lock the screen while
  listening, background for a few minutes) invisible without touching Metal
  or Core ML during the background window at all. The shipped
  `handleDidEnterBackground()`/`handleDidBecomeActive()` system-voice swap
  remains the correct fallback for whenever the buffer runs dry, not
  something this replaces.
