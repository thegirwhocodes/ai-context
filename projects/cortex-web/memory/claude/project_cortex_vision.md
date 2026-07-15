---
name: Cortex vision and architecture
description: What Cortex is, the 3-layer architecture, Naomi's full vision for a personal AI agent
type: project
sessions: [0d91dd3c-6d8d-4983-b72b-a1df57377021]
---

## What Cortex Is

Cortex is a personal AI agent that ingests ALL of a user's digital data, trains a per-user LoRA model on it, and acts on their behalf. It evolved from Spheres (a SwiftUI Mac app for life management) into a full web platform. The name comes from Naomi's vision of an AI that truly KNOWS you — not just retrieves your documents.

## The 3-Layer Architecture

**Layer 1 (Bottom — Roots / Ingestion):**
All the ways the app gets your personal data. Connected to every branch of your personal life. Gmail, Calendar, Instagram DMs, GroupMe, WhatsApp, iMessage, Notes, bank transactions. All ingested, chunked, embedded into Supabase pgvector (384-dim, all-MiniLM-L6-v2).

**Layer 2 (Middle — Interface):**
Where you sit. Ask "what do I have to do today?" and get a list. The LLM automatically creates spheres (life areas) from your data patterns. You see progress with spheres, things you might be forgetting. Chat interface, daily briefing, email agent. Voice-driven interaction ("Cortex starts talking to you").

**Layer 3 (Top — Action / Agentic):**
Cortex does things FOR you. Sends emails in your tone, replies to DMs, buys groceries (Apple Pay + Face ID confirmation for purchases). All actions require user approval before execution.

## The Brain (4-Layer Query Flow)

```
Personal LoRA (tone, style, patterns — KNOWS you)
+ RAG (today's specific data — real-time retrieval)
+ User Profile (deep Sonnet analysis of 200+ data points)
+ Claude (heavy reasoning when needed)
→ answer that sounds like YOU and knows YOUR life
```

## Key Vision Points From Naomi

- NOT just RAG. She pushed back 3 times when a previous Claude tried to steer her to "just use RAG." Her instinct was right — per-user LoRA is feasible at $0.22-$1.44/user.
- The LLM should CREATE spheres itself — not suggest them, not have an algorithm around them. Truly an LLM decision.
- Non-anxiety-inducing: "4 emails need your reply" instead of "247 unread."
- Everything encrypted, privacy-first. Delete the LoRA adapter = fully forget the user (GDPR solved).
- Start consumer ($19/mo), then API platform, then enterprise. Recommended path is Plan D (hybrid).

## Spheres (Predecessor)

Spheres was a production-ready macOS SwiftUI app with AI-powered life management — GTD-based task management, energy intelligence, chronotype detection, values-based personalization, Smart Setup that auto-generates spheres by scanning Reminders, Mail, Notes, Voice Memos, iMessage, Calendar. Cortex is the web/mobile evolution.

## Business Vision

- B2C consumer app ($19/mo, 98% margins)
- B2B enterprise ($15-35/user/mo)
- API platform ("Stripe for personal AI")
- Holding company with multiple products
- "This is gonna reach the ends of the earth"
