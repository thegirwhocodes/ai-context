---
name: sleep-well-architecture
description: "How the Sleep Well app is wired (targets, sync, Sage, key files, ceilings)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b7a31d6-b579-4a4a-a44c-63b602b3158c
---

Sleep Well architecture (see [[sleep-well-intent]] for the why). ~5,100 LOC Swift, now a git repo.

**Targets:** `ShutdownApp/` (macOS) · `SleepWelliOS/` (iOS/iPadOS) · 3 Screen Time extensions (`DeviceActivityMonitorExtension`, `ShieldConfigurationExtension`, `ShieldActionExtension`).

**State/sync:** `SyncedStore.swift` (hand-copied identical in `ShutdownApp/` and `SleepWelliOS/Shared/` — keep in sync) is the one source of truth. Dual-writes iCloud `NSUbiquitousKeyValueStore` (cross-device) + App Group `group.com.sleepwell.shared` (so extensions read it). Weekly unlock ceiling = 3, enforced client-side + by the Sage backend.

**Sage unlock flow:** `UnlockAgentClient.swift` POSTs reason → `{agentBaseURL}/api/verify-unlock` (backend = extended `~/bethel/email-agent`, runs locally). Fail-SAFE: any error/unknown verdict → lock holds. On `grant`: `recordGrantedUnlock(minutes:)` sets `activeUnlockUntil`, all devices unblock for the window.

**iOS limit workarounds:** DeviceActivity "heartbeat" slices (now capped 17, leaving room for `.bedtime` + `.relockAfterUnlock` under Apple's 20-activity ceiling) because iCloud KVS doesn't wake the app. `ScheduleManager.swift` schedules; `SleepWellMonitor.swift` applies/clears shields.

**Hard platform ceilings:** macOS has NO Family Controls API → Mac block is a userland window + optional CGSession login-window drop (bypassable by force-quit; only a privileged LaunchDaemon/MDM fixes it). iOS auth is one-toggle-revocable; no silent remote unlock (APNs best-effort only).

**Plan/roadmap + full findings:** `ARCHITECTURE_AND_PLAN.md` in the repo. Blockers to shipping: Xcode account login rejected for naomiivie06@gmail.com; iOS 26.2 platform (~8.4GB) not installed; App Store needs distribution Family Controls entitlement from Apple.
