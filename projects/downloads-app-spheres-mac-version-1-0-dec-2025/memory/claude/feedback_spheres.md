---
name: Spheres User Feedback & Preferences
description: Parallel Claude issues, undo requests, design preferences, Naomi's working style
type: feedback
sessions:
  - 89ec22a2-55b3-4862-869f-ec4fe25f17c1
  - 15944261-45ae-4311-949e-cfe3cd9f63a5
  - f53a9a0a-123b-49ad-9161-16f55671c32c
  - 5e7d8445-6c7b-458a-8369-6947f64d2c1b
---

# Spheres User Feedback & Preferences

## Working Style
- Naomi runs **multiple Claude instances in parallel** on the same codebase (up to 3-4 simultaneously)
- This causes file conflicts -- one Claude's changes can be overwritten by another
- Must always re-read files before editing and verify changes weren't reverted
- Build DB lock conflicts can occur when multiple instances try to build

## Undo Pattern
Naomi frequently says "undo" when a change is too broad or targets the wrong element:
- "Remove pencil from hover" -> removed from 3 places -> "undo - only remove from sphere detail header"
- "Resize Add Loop button" -> changed global button styles -> "Undo - I meant the open add open loop dialogue box" -> "not the button - the entire grey pop up"
- Must ask for clarification about scope before making sweeping changes
- When she says "undo", restore the specific parts she didn't want changed

## Design Preferences
- **Hates**: Progress pie charts, "Priority N" text labels, flat grey dialog backgrounds, loud/solid colored buttons, "shouty" colors
- **Loves**: Clean completion circles, dot indicators, glass material backgrounds, translucent/subtle button styles, hover-expand animations
- **Color preference**: Wants things to align with the app's purple theme, not arbitrary colors. When asked for red, went through red -> dusty rose -> plum -> "just use the app's purple"
- **Placement**: Prefers left-aligned UI elements, side-by-side capsule buttons
- **No pencil icons** on hover (except calendar events)
- **Enter key** should submit/close all dialog forms

## AI Preferences
- "Let it be LLM style - forget about the costs" -- wants natural, conversational AI
- "Not too long, not too short" -- balanced response length
- Initially said forget costs, then asked for the math, then wanted cost optimization
- Final decision: Sonnet for chat (quality), Haiku for background (cost)
- Removed the old "gentle companion, 2-3 sentences" prompt style

## Update Button Iteration (Instructive Pattern)
Naomi went through many iterations on the update button placement/style:
1. "Don't put in settings!" (moved to sidebar)
2. "Top right please" (overlay)
3. "Just arrows and update - not a whole pane" (simplified)
4. "Next to signed in button" (sidebar bottom)
5. "Same style as signed in, hover expand" (matching capsules)
6. "Side by side, expand on hover" (combined SidebarStatusBar)
7. "Undo the combined" (back to separate buttons)
8. "Make it red" -> "a red that aligns with theme" -> "leaning more to purple" -> "just use the app's purple"
9. "Left aligned"

**Lesson**: Expect iterative refinement. Start simple, let her guide the details.

## Feature Requests Pattern
- Naomi thinks big ("make this into a startup")
- Then immediately asks for practical implementation
- Values frictionless UX over feature completeness
- "AWESOME!! THANK YOU FINALLY" when sample data was finally cleaned up -- she noticed persistent issues

## Parallel Claude Management
- She explicitly warns: "be aware that 3 other claudes are running in parallel with you"
- She asks to "verify your changes weren't overwritten by another claude"
- She sometimes says "assume the other claude undid all your changes - verify and put them in again"
- Must always re-read before editing

## Deployment Preferences
- Auto-deploy on topic change, use `auto_deploy.py`
- Don't deploy mid-feature
- Commit message format: `feat:`, `fix:`, `refactor:`, `chore:` prefixes
- No co-author tags (removed)
- Prefers in-app update over App Store (for now)