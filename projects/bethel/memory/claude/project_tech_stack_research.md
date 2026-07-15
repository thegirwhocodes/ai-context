---
name: Tech Stack Research & Platform Decision
description: Research on native vs cross-platform, decision to go iOS-first in Swift/SwiftUI
type: project
sessions: [e59a15e2-07e1-441a-b5e1-74b37c995b59, efd7d7d2-3b94-4e82-bb2d-7a045a3e9736]
---

## Research Finding: Every Premium App in This Space is Native

| App | Built With | Why |
|-----|-----------|-----|
| Glorify | Swift (iOS), Kotlin (Android) | Premium feel, glassmorphism, reader quality |
| YouVersion | SwiftUI + Kotlin with KMP shared logic | Best of both worlds |
| Bear Notes | Native Swift (Apple Design Award) | Apple-level text editing |
| Day One | Native Swift | Journal polish, rich editing |
| ChatGPT/Claude mobile | Native | Deep platform integration |
| Dreamnl | Likely cross-platform (solo dev) | Not in "premium" tier |

## Why React Native/Expo Falls Short for Bethel
1. **Text rendering** -- RN cannot match native TextKit 2 for e-reader quality (ligatures, hyphenation, widows/orphans)
2. **Rich text editing** -- RN's weakest area; dream journal editor won't feel like Bear or Day One
3. **The last 5% of polish** -- possible but fighting the framework constantly

## Decision Path
1. Started with Expo/React Native (for QR code hot-reload)
2. Built initial Expo scaffolding (all 5 tabs, theme, services)
3. Research revealed native is the right choice for premium quality
4. Naomi decided: "let's do native"
5. Deleted Expo code (without backup -- led to feedback about always backing up)
6. Built 12 Swift files: BethelApp, ContentView, BethelTheme, MoonPhase, GlassTabBar, HomeView, BibleView, ChapterReaderView, JournalView, NewDreamView, BethelChatView, ProfileView
7. Also created Expo web-preview project for desktop prototyping
8. Naomi confirmed: iOS only, no multiplatform (causes crashes)

## Current Codebase State
- Native iOS app at `/Users/naomiivie/Downloads/App/Bethel/` (Xcode project)
- Source code at `/Users/naomiivie/bethel/Bethel/` (12 Swift files)
- Expo web-preview at `/Users/naomiivie/bethel/web-preview/` (basic setup)
- Build succeeded, ran on iPhone 17 Pro simulator
- Scaffolding only -- real feature implementation has not begun

## SwiftUI Development Workflow
- Xcode Preview canvas for instant visual feedback (no phone needed)
- Cable first time for phone, then wireless debugging
- No need for Expo Go or QR code -- Xcode handles everything
- Build takes ~15s first time, 3-5s incremental
