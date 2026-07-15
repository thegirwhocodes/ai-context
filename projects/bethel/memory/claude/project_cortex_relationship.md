---
name: Cortex-Bethel Relationship
description: How Bethel relates to Cortex (personal AI agent), shared architecture patterns, and why they are separate projects
type: project
sessions: [efd7d7d2-3b94-4e82-bb2d-7a045a3e9736, 0d91dd3c-6d8d-4983-b72b-a1df57377021, e59a15e2-07e1-441a-b5e1-74b37c995b59]
---

## Cortex Overview

Cortex is Naomi's personal AI agent startup -- "your second brain." It is a SEPARATE product from Bethel. Key facts:

- **Not a personal project** -- Naomi corrected Claude explicitly: "this is not a 'personal project' -- I want to build a startup with this product"
- Originally called Spheres (a SwiftUI macOS app Naomi already built), evolved into Cortex as the web/mobile version
- Name chosen from: Spheres, Orb, Nexus, Pulse, Aura, Mantle, Helm, Lumen, **Cortex** (winner), Weave
- Web app built at `/Users/naomiivie/cortex-web/` (Next.js + Supabase + Clerk + Claude API)
- Full plan at `/Users/naomiivie/cortex/CORTEX_FULL_PLAN.md`

## Shared Architecture Pattern

Bethel and Cortex share the same 4-layer hybrid architecture, discovered in session 0d91dd3c:

| Layer | Cortex | Bethel |
|-------|--------|--------|
| **1. Personal Context** | User's emails, messages, calendar (RAG) | User's dream journal, past interpretations (RAG) |
| **2. Per-user LoRA** | Trained on user's communication patterns | Trained on user's dream symbolism (500+ dreams) |
| **3. Knowledge Base** | N/A (general purpose) | Full NKJV + theological training data (RAG) |
| **4. Cloud Fallback** | Claude Sonnet for complex reasoning | Claude Haiku for complex interpretation |

Plus the **Bethel Base LoRA** (layer between 2 and 3) -- trained on Bible + Hagin + Kuhlman + Jackson + dream frameworks. Same for all users.

## Why They Are Separate

- Different domains: personal productivity vs spiritual life
- Different user bases: everyone (Cortex) vs spiritually curious Christians (Bethel)
- Different infrastructure: Cortex on Vercel, Bethel on dedicated Hetzner GPU
- Different monetization: Cortex is B2B/B2C subscription ($20/mo), Bethel is free with no ads
- Bethel was described as potentially a "Cortex vertical" ("Cortex for Christians") but is being built standalone

## Key Technical Crossovers

- Both use Supabase pgvector with all-MiniLM-L6-v2 (384-dim embeddings)
- Both use Clerk for authentication
- Both validated via LoRAX for serving per-user LoRA adapters
- Both use the same phased deployment: API-first -> train LoRA on Mac -> buy GPU server when ready
- LoRA training validated in Cortex session: $0.22-$1.44/user cloud, ~$0.02 on Mac with MLX
- Fine-tuned 3B > prompted 70B on 85% of domain tasks

## Cortex Current State (as of March 18, 2026)

Built in session 0d91dd3c:
- Next.js web app with Clerk auth, Supabase schema, Gmail OAuth integration
- Email agent (ingest, prioritize, draft replies in user's tone)
- Sphere generator (auto-creates life areas from data)
- Daily briefing
- Query engine (profile + memory + RAG -> Claude Haiku)
- Memory extractor
- LoRA training pipeline (data formatter, RunPod client, LoRAX inference client)
- Phase 1 done, Phase 2 ~80%, Phase 3 code written but untested
