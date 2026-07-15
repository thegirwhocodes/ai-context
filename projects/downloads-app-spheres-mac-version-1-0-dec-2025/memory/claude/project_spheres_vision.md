---
name: Spheres Vision & Architecture
description: What Spheres is, life management philosophy, sphere/loop model, AI integration strategy
type: project
sessions:
  - 89ec22a2-55b3-4862-869f-ec4fe25f17c1
  - 15944261-45ae-4311-949e-cfe3cd9f63a5
  - f53a9a0a-123b-49ad-9161-16f55671c32c
  - 5e7d8445-6c7b-458a-8369-6947f64d2c1b
---

# Spheres Vision & Architecture

## What Spheres Is
Spheres is a **Smart Life Manager** for macOS -- a productivity app that organizes all areas of life into visual "spheres" (categories) containing "loops" (tasks/habits). It uses AI to help users manage, prioritize, and schedule their life holistically.

- **Bundle ID**: com.naomiivie.SpheresMultiplatform
- **GitHub**: thegirwhocodes/spheres-app (private)
- **Target**: macOS (iOS/iPad planned but not started)

## Core Mental Model

### Spheres
Top-level life categories. Originally 7 defaults (Spiritual, Health, Family, Work, Finances, Community, Growth) but v3.0 removed all defaults in favor of AI-generated personalized spheres from user data.

### Loops (Open Loops)
Tasks or habits within a sphere. Each has:
- Content (description)
- Priority (1-5, where 1 = highest)
- Estimated time
- Progress tracking (0-100%)
- Streaks (for habits)
- Source tracking (manual, calendar, AI-generated, etc.)

### 5 Main Views
1. **Home** -- Dashboard overview
2. **Spheres** -- Visual sphere management (bouncy orb + card views)
3. **Schedule** -- Calendar timeline with smart scheduling
4. **Inbox** -- Quick capture / unsorted items
5. **Mind** -- AI chat companion

## AI Integration Strategy

### Model Split (Cost Optimized)
- **Chat (user-facing)**: Claude Sonnet 4.6 ($3/$15 per 1M tokens), 500 max tokens
- **Background tasks**: Claude Haiku 4.5 ($1/$5 per 1M tokens) for categorization, loop processing, resurfacing, classification
- **Smart Setup onboarding**: Claude Sonnet (~$0.04 one-time per user)
- Estimated cost: ~$2.70/month per active user (split approach)

### AI Capabilities
- Task extraction from natural language
- Smart sphere assignment
- Priority and time estimation
- Resurfacing suggestions (things users should revisit)
- Pattern recognition
- Mind chat (conversational AI companion)
- Smart Setup: scans Mac ecosystem to auto-generate spheres

## Life Orientations Model (Psychological Foundation)

### 4 Dimensions (biblically-grounded tensions)
| Dimension | Left <-> Right | Biblical Basis |
|-----------|----------------|----------------|
| Renewal | Solitude <-> Community | Luke 5:16 <-> Heb 10:25 |
| Expression | Being <-> Doing | Mary <-> Martha (Luke 10) |
| Care Focus | Inner <-> Outer | 1 Tim 5:8 <-> Matt 28:19 |
| Time Horizon | Present <-> Future | Matt 6:34 <-> Prov 21:5 |

### 7 Archetypes
Contemplative, Activist, Relational, Visionary, Steward, Seeker, Balanced

### 7 Life Areas (everyone gets all, priority varies)
Faith, Family, Health, Work, Finances, Community, Growth

### How It Personalizes
1. Sphere priorities from orientation scores
2. AI prompt guidelines tuned to archetype
3. Insights surfaced based on type
4. Scheduling prioritizes aligned tasks

## Adaptive Profile Evolution (Spotify-Inspired)
- Thompson Sampling (Beta distributions for each life area)
- Implicit signal tracking: task completions, skips, engagement time, suggestion acceptance
- Time decay (14-day half-life)
- Contextual bandits (time-of-day, weekday/weekend patterns)
- Bounded adjustments (max +/-0.05 per cycle, 0.6 confidence threshold)

## Startup Vision
Naomi envisions Spheres as a startup product. Key strategy:
- Frictionless onboarding: AI scans user's Mac ecosystem and auto-creates personalized spheres
- End-to-end encrypted data
- Subtly Christian-influenced (truth-based framework without being preachy)
- Privacy-first (analysis on-device where possible)

## Research Basis
- Schwartz Theory of Basic Values (structural tensions)
- Harvard Human Flourishing Program (VanderWeele)
- Time Perspective Theory (Zimbardo)
- Self-Determination Theory (Ryan & Deci)
- Spotify recommendation algorithms (collaborative filtering, reinforcement learning)
- Multi-Armed Bandits (exploration-exploitation)
