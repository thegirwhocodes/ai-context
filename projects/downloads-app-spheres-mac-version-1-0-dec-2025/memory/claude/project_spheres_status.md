---
name: Spheres Build Status
description: What's built v1.0-v3.0, what's pending, known bugs and fixes
type: project
sessions:
  - 89ec22a2-55b3-4862-869f-ec4fe25f17c1
  - 15944261-45ae-4311-949e-cfe3cd9f63a5
  - f53a9a0a-123b-49ad-9161-16f55671c32c
  - 5e7d8445-6c7b-458a-8369-6947f64d2c1b
---

# Spheres Build Status

## Version History

### v1.0 (Dec 2025) -- COMPLETE
- 5 main views: Home, Spheres, Schedule, Inbox, Mind (AI chat)
- Sphere/Loop CRUD with drag-to-reorder, progress tracking, time tracking, streaks
- AI Integration: Claude API for task classification, smart resurfacing, chat, pattern recognition
- Calendar: Apple + Google via EventKit, 24-hour timeline, time blocking
- Energy Intelligence: chronotype profiling, energy drawing, smart time block suggestions
- Quick Capture (Cmd+N, menu bar icon)
- Notifications (due reminders, habit reminders)
- Export/Backup (JSON, CSV, timestamped)
- Dark liquid glass UI

### v2.0 (Feb 2025) -- COMPLETE
- Life Orientations Model (4 dimensions, 7 archetypes, 7 life areas)
- 5-question orientation quiz with dimensional scoring
- Personalization: sphere priorities, AI prompt guidelines, scheduling alignment
- Values-aware scheduling (30% boost for value-aligned tasks)

### v2.1 (Feb 2025) -- COMPLETE
- Adaptive Profile Evolution (Spotify-style Thompson Sampling)
- Implicit signal tracking (completions, skips, engagement time, suggestion acceptance)
- Time decay (14-day half-life), contextual bandits (time-of-day, weekday/weekend)
- Profile Insights ("Wrapped" style UI)

### v3.0 Smart Setup (Feb 2026) -- COMPLETE
- AI-powered onboarding replacing 10-step flow with 4 steps: Welcome -> Permissions -> AI Scan -> Review
- SmartSetupService scans Mac ecosystem: Calendar, Mail, Notes, Reminders, Voice Memos, iMessage
- Sends summarized data to Claude Sonnet (~$0.04/user)
- AI generates personalized spheres + tasks from user's actual data
- Removed all default sphere seeding
- Values Quiz deferred to optional "Refine Profile" after 1 week

### Infrastructure (Feb 2026) -- COMPLETE
- Auto-deploy to GitHub (auto_deploy.py + PreCompact hook)
- Auto-update from GitHub (auto_update.py + LaunchAgent every 2 hours)
- In-app Update button (sidebar, purple accent, hover-expand)
- iCloud CloudKit sync configured and working
- SwiftUI #Preview blocks for all major views

## UI Polish Applied (Feb 2026 Sessions)
- Pencil hover icons removed from sphere detail header and sidebar rows
- DetailLoopCard: progress pie replaced with 22px completion circle + 5-dot priority indicator
- Add Loop button: bigger with translucent accent style
- Add/Edit Loop dialogs: `.ultraThinMaterial` glass background instead of flat grey
- Enter key submits all dialogs (Add/Edit Loop, Add/Edit Sphere)
- AI chat tone updated to natural LLM style (not "gentle companion")
- AI model split: Sonnet for chat, Haiku 4.5 for background
- Privacy Dashboard moved from Home to Settings only
- Sample loops cleaned up (no more "Call mom about Thanksgiving")
- Right-click to delete spheres fixed (Button wrapper -> .onTapGesture + .contentShape)
- Update button: purple accent, left-aligned, hover-expand, next to sign-in capsule

## Partially Done
- iCloud CloudKit Sync -- framework works, needs real-world multi-device testing
- Source Adapters -- NotesAdapter partially works; Mail and VoiceMemos stubbed
- Widgets -- bundle/framework present, implementation incomplete
- Privacy Dashboard -- basic structure only
- SmallAccentButtonStyle/SmallGhostButtonStyle -- may still be in modified translucent state (user asked to undo but got redirected)

## Not Started
- iOS/iPad version
- Siri Shortcuts
- Unit tests
- App Store submission (requires screenshots, descriptions, privacy policy, App Review)
- Subscription/pro plan pricing
- Multi-email/SSO support
- Integration marketplace

## Known Bugs & Issues (from sessions)
- Build DB lock conflicts when multiple Claude instances build simultaneously
- Calendar events from EventKit show in Schedule (expected behavior, not a bug)
- Instruction backlog files (Instrutions.md, Instruction History.md) contain ~60 unaddressed feature requests

## Bug Fixes Applied
| Bug | Root Cause | Fix |
|-----|-----------|-----|
| Energy button loop | Missing `hasCompletedEnergyOnboarding` check | Added check |
| Skip buttons not advancing | Not calling `onSkip()` callback | Added callback |
| App crashes on update | `pkill` sends SIGTERM -> crash dialog | osascript graceful quit |
| App won't launch after update | Ad-hoc code signing (`CODE_SIGN_IDENTITY="-"`) | Use real developer cert |
| Code signatures stripped on copy | `cp -R` / `shutil.copytree` | Use `ditto` |
| Self-update crash | App quits itself while script runs | Detached shell script (stage -> quit -> swap -> relaunch) |
| GitHub push auth failure | `gh` not linked to git | `gh auth setup-git` |
| CloudKit container ID typo | `"iCloud.sunc"` in code | Fixed to `"iCloud.com.naomiivie.SpheresMultiplatform"` |
| Right-click delete not working | `Button` wrapper consuming right-click | Replaced with `.onTapGesture` + `.contentShape` |
| `run()` function error | Local `run()` doesn't accept `check` kwarg | Use `subprocess.run()` directly |