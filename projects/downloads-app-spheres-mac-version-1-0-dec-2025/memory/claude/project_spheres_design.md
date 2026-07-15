---
name: Spheres Design System
description: Dark liquid glass UI, bouncy balls, Life Orientations, theme colors, UI rules
type: project
sessions:
  - 89ec22a2-55b3-4862-869f-ec4fe25f17c1
  - f53a9a0a-123b-49ad-9161-16f55671c32c
  - 5e7d8445-6c7b-458a-8369-6947f64d2c1b
---

# Spheres Design System

## Design Philosophy
- **Dark liquid glass UI** with translucent aesthetic
- Minimalist but functional
- Privacy-first
- Subtly Christian-influenced (truth-based framework without being preachy)
- No religious iconography

## Theme Colors (SpheresTheme)
- **Accent**: Purple `Color(red: 0.55, green: 0.36, blue: 0.96)`
- **Background**: Very dark
- **Surface**: 5% white opacity
- **Text**: White primary, muted secondary
- **Border**: Subtle dividers

## Sphere Visualization
- **BouncySphereOrb**: Animated bouncy ball view with physics-like hover effects
- Spheres have individual colors (red, blue, orange, purple, etc.)
- Two view modes: bouncy orb grid and card grid
- Morphing corner radius on interaction
- `.onTapGesture` (not `Button`) to allow right-click context menus

## UI Component Patterns

### Dialogs (Add/Edit Loop, Add/Edit Sphere)
- `.ultraThinMaterial` glass background (not flat grey `SpheresTheme.surface`)
- Subtle border overlay
- Translucent accent-tinted buttons
- Enter key submits via `.onSubmit`

### Buttons
- **AccentButtonStyle**: For primary actions, translucent purple tint
- **SmallAccentButtonStyle**: For inline actions (Done, Stop) -- translucent purple
- **SmallGhostButtonStyle**: For secondary actions (Edit, Delete) -- soft translucent fill
- **GhostButtonStyle**: Bordered outline for less prominent actions

### Loop Cards (DetailLoopCard)
- 22px completion circle (tap to complete, shows progress arc when partial, checkmark when done)
- 5-dot priority indicator (more filled dots = higher priority, uses sphere color)
- Progress percentage shown inline only when > 0% and not complete
- No progress pie chart (removed per user preference)
- No pencil hover icon on detail header

### Sidebar
- Sign-in capsule: green checkmark, text expands on hover
- Update capsule: purple accent (`SpheresTheme.accent`), arrows icon, text expands on hover
- Both left-aligned, side by side
- `.lineLimit(1).fixedSize()` to prevent text wrapping

### Add Loop Button (Sphere Detail Header)
- Bigger than default (font 13/14, padding 18x10)
- Translucent purple tint (12% opacity) with purple text
- Not solid purple background

## Typography
- System font throughout
- Small UI elements: 11pt
- Standard labels: 12-13pt
- Headers: larger system sizes

## Hover States
- No pencil icons on sphere detail header or sidebar rows
- Pencil icon kept on calendar event hover
- Capsule buttons expand text on hover with slide animation
- `.transition(.opacity.combined(with: .move(edge:)))` for hover reveals

## Onboarding UI (v3.0 Smart Setup)
- 4-step flow: Welcome -> Permissions -> AI Scan -> Review
- Animated scan progress during AI processing
- Expandable sphere cards in review step
- Toggle/rename spheres before confirming

## AI Chat Tone
- Natural LLM conversational style
- Not "gentle companion" or restricted to 2-3 sentences
- Smart, thoughtful friend persona
- Markdown formatting supported
- Not too long, not too short