---
name: Spheres Tech Stack & Infrastructure
description: SwiftUI, SwiftData, CloudKit, Claude API, auto-deploy, auto-update systems
type: project
sessions:
  - 89ec22a2-55b3-4862-869f-ec4fe25f17c1
  - 15944261-45ae-4311-949e-cfe3cd9f63a5
  - f53a9a0a-123b-49ad-9161-16f55671c32c
  - 5e7d8445-6c7b-458a-8369-6947f64d2c1b
---

# Spheres Tech Stack & Infrastructure

## Core Stack
- **UI**: SwiftUI (macOS)
- **Data**: SwiftData with `@Model` classes
- **Sync**: CloudKit (private database) via `ModelConfiguration(cloudKitDatabase: .private(...))`
- **Calendar**: EventKit (Apple + Google Calendar)
- **AI**: Claude API (Anthropic) -- Haiku 4.5 + Sonnet 4.6
- **Language**: Swift
- **IDE**: Xcode

## Key Patterns
- `@AppStorage` for UserDefaults persistence
- `@Environment(\.modelContext)` for SwiftData access
- `@Query` for SwiftData fetches in views
- CloudKit-compatible models need default values
- Priority: 1 = highest, 5 = lowest
- `.windowStyle(.hiddenTitleBar)` -- traffic lights float over content

## Key Files
| File | Purpose | Size |
|------|---------|------|
| ContentView.swift | Main UI, sidebar, navigation, ~5000 lines | Large |
| SphereDetailView.swift | Sphere detail, loop cards, add/edit sheets | Large |
| SpheresView.swift | Sphere grid (bouncy orbs + card views) | Medium |
| AIService.swift | Claude API integration, all AI methods | Medium |
| Models.swift | SphereModel, OpenLoopModel, InboxItemModel | Medium |
| DataManager.swift | Data seeding, cleanup, management | Medium |
| SmartSetupService.swift | v3.0 AI-powered onboarding scan service | Medium |
| SmartSetupOnboardingFlow.swift | 4-step onboarding UI | Medium |
| PersonalizationService.swift | Profile + AI coordination, prompt building | Medium |
| AdaptiveProfileService.swift | Thompson Sampling algorithm | Medium |
| UserProfileModel.swift | Values, preferences, orientation profile | Medium |
| CalendarService.swift | EventKit integration, smart scheduling | Medium |
| EnergyIntelligence.swift | Chronotype, energy-based scheduling | Medium |
| SmartScheduleView.swift | Schedule timeline view | Medium |
| SharedComponents.swift | Reusable button styles, theme components | Small |
| SpheresApp.swift | App entry, SwiftData container config | Small |
| PreviewContent.swift | In-memory ModelContainer for Xcode previews | Small |

## CloudKit / iCloud Sync
- Container: `iCloud.com.naomiivie.SpheresMultiplatform`
- Entitlements file: `Spheres_Multiplatform.entitlements`
- Apple Developer account enrolled (naomiivie06@gmail.com, cert FL5RL9AY66)
- SwiftData auto-creates CloudKit schema on first run
- CloudKitService.swift handles sync status

## Auto-Deploy System (GitHub)
- **Script**: `auto_deploy.py` at project root
- **Hook**: `.claude/settings.local.json` PreCompact hook (both auto + manual)
- Stages all changes, commits with timestamp, pushes to GitHub
- Runs before Claude Code context compaction to prevent work loss
- No co-author tag (removed per Naomi's request)

## Auto-Update System
- **Script**: `auto_update.py` at project root
- **LaunchAgent**: `~/Library/LaunchAgents/com.naomiivie.spheres-autoupdate.plist` (every 2 hours)
- Pulls latest from GitHub, checks for Swift file changes
- Builds with `xcodebuild` using real developer certificate
- Staged approach: build -> stage to `.staged_app/` -> spawn detached bash script -> quit -> swap -> relaunch
- Uses `ditto` (not `cp -R`) to preserve code signatures
- Uses `osascript` for graceful quit (not `pkill`)

## In-App Update Button
- `AppUpdateButton` component in sidebar, next to `EnhancedSignInStatus`
- Purple accent color (`SpheresTheme.accent`), left-aligned
- Hover-expand: arrows icon only by default, "Update" text slides out on hover
- Triggers `auto_update.py --force` via detached Process

## Xcode Project
- `.xcodeproj` based (not SPM)
- New Swift files must be added to pbxproj manually or via script
- Permissions auto-allowed: `xcodebuild`, `open`

## SwiftUI Preview Infrastructure
- `PreviewContent.swift` with in-memory ModelContainer
- Sample data: 4 spheres (Health, Career, Family, Faith) with loops at various states
- `#Preview` blocks added to 10+ view files
- Schema includes: SphereModel, OpenLoopModel, InboxItemModel