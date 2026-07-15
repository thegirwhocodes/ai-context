# Spheres App - Memory Index

## Project
- [Spheres vision & architecture](project_spheres_vision.md) -- What Spheres is, life management, sphere/loop model, AI integration, Life Orientations, startup vision
- [Spheres tech stack](project_spheres_tech.md) -- SwiftUI, SwiftData, CloudKit, Claude API, auto-deploy, auto-update, preview infrastructure
- [Spheres build status](project_spheres_status.md) -- What's built v1.0-v3.0, what's pending, known bugs, bug fixes applied
- [Spheres design system](project_spheres_design.md) -- Dark liquid glass UI, bouncy balls, theme colors, component patterns, AI chat tone

## Feedback
- [Be patient with work](feedback_patience.md) -- Do not rush, do not shortcut, take the time to do it right
- [MUST re-read after compaction](feedback_compaction_reread.md) -- Re-read ENTIRE session .txt after compaction, no exceptions
- [Spheres user feedback](feedback_spheres.md) -- Parallel Claude issues, undo patterns, design preferences, iterative refinement style

## Quick Reference

### App Identity
- **App**: Spheres - Smart Life Manager (macOS)
- **Bundle ID**: com.naomiivie.SpheresMultiplatform
- **GitHub**: thegirwhocodes/spheres-app (private)
- **Developer**: Naomi Ivie (naomiivie06@gmail.com)

### Deployment Protocol
- Auto-deploy on topic change: `python3 auto_deploy.py "message"`
- Don't deploy mid-feature
- Commit prefixes: `feat:`, `fix:`, `refactor:`, `chore:`
- In-app Update button triggers `auto_update.py --force`

### AI Models
- Chat: Claude Sonnet 4.6 (500 max tokens)
- Background: Claude Haiku 4.5
- Smart Setup: Claude Sonnet (~$0.04/user onboarding)

### Key Patterns
- `@AppStorage` for UserDefaults
- `@Environment(\.modelContext)` for SwiftData
- CloudKit-compatible models need default values
- Priority: 1 = highest, 5 = lowest
- Multiple Claude instances may run in parallel -- always re-read before editing