---
name: Bethel Vision and Architecture
description: Complete vision, architecture, and technical spec for Bethel - the Bible + Dreams + AI app
type: project
sessions: [e59a15e2-07e1-441a-b5e1-74b37c995b59, efd7d7d2-3b94-4e82-bb2d-7a045a3e9736, 86c89090-9d07-4f5c-ac46-50629db75b25, 0d91dd3c-6d8d-4983-b72b-a1df57377021]
---

**Bethel** = "House of God" (Genesis 28) -- a mobile app that treats Bible reading, dream journaling, and AI-powered interpretation as one connected spiritual journey. Named after where Jacob dreamed and set up a memorial stone.

**Why:** The founder (Naomi) believes dreams are words from God that need stewarding, not just journaling. No existing app combines chronological Bible reading + dream journal + AI interpretation + personal notes.

**How to apply:** Every feature decision should serve this unified spiritual journey. Dreams connect to scripture. Scripture illuminates dreams. The AI ties it all together.

## 4-Layer AI Architecture
1. **Personal Context (RAG)** -- user's dream journal, past interpretations, personal symbol dictionary. Updated instantly.
2. **Bethel LoRA** -- fine-tuned adapter (~16-20MB) on Phi-3.5 Mini (3.8B params) or possibly Qwen3-4B. Trained on Bible + Hagin + Kuhlman + Jackson + Virkler + dream frameworks. Monthly retrain.
3. **Biblical Knowledge Base (RAG)** -- full NKJV (31,102 verses) in Supabase pgvector with 384-dim embeddings (all-MiniLM-L6-v2), dream symbol dictionary, cross-references.
4. **Cloud Model Fallback** -- Claude Haiku API (~$0.0045/call) for complex reasoning.

## Tech Stack Decision History
- **Originally:** Expo / React Native + TypeScript (chosen for QR code hot-reload)
- **Switched to:** Native Swift/SwiftUI (iOS only) after research showed every premium Bible/journal app is native
- Also created Expo web-preview for desktop UI prototyping
- Backend: Supabase (pgvector) for database
- Claude API (Haiku) for cloud model layer
- Clerk for auth
- LoRAX on dedicated Hetzner GEX44 (~$200/mo) for serving LoRA -- SEPARATE from Sabi server

## Tab Structure (evolved)
Originally 5 tabs: Home | Bible | Journal | Bethel AI | Profile
Naomi refined to 4 tabs: **Chronological Bible | Bethel (AI) | Dreams | Journals**
- Structured around the AI, not around sections
- "Surfacing today" page desired
- No generic home/profile tab clutter -- settings go in a gear icon

## Key Features
- **Bible Reader**: Full chronological NKJV, premium e-reader quality, swipe navigation, 3 themes (Midnight/Warm Night/OLED), highlights in 4 colors, notes, cross-references. Font: Literata 18px default.
- **Dream Journal**: Text entry with AI-generated titles, mood picker (abstract colored circles), clarity rating, Bible verse linking, auto-save, moon phase display, AI interpretation, pattern matching, dream-to-scripture connection, LLM-driven resurfacing.
- **Ask Bethel**: Chat with scripture citation blocks, suggested prompts, gold stone/pillar avatar, lavender pulsing "thinking" state, every response cites scripture.
- **Daily Devotional**: Hagin's 3-part structure (Scripture > Teaching > Confession).
- **Future**: OCR to scan handwritten dream journals via camera.

## Critical Mandates
- The LLM decides everything -- NO hardcoded algorithms for dream resurfacing/interpretation
- Per-user LoRA training is non-negotiable (for power users with 500+ dreams, later)
- Dreams are words from God, not journal entries
- Bible (NKJV) is ground truth that validates all other sources
- Training data validation: Aligned / Extrapolated / Testimony / Contradicts scoring

## LoRA Training Approach
- **Shared base LoRA**: Bible + all theological training, same for all users. Cost: ~$0.02 on Mac.
- **Personal RAG**: Per-user dreams/notes stored in pgvector (instant updates). No per-user fine-tuning at launch.
- **Per-user LoRA**: Only when a user has 500+ dreams with complex personal symbolism. Way later.
- Training on Mac with MLX (free, 15-30 min) or RunPod spot ($0.22)
- ~8,500 training examples from research files

## Server / Infrastructure
- Bethel gets its own dedicated Hetzner GEX44 (~$200/mo) -- NOT shared with Sabi
- Phased approach: Claude Haiku API for MVP -> train LoRA on Mac -> buy server when ready to serve users
- Possible newer base model: Qwen3-4B (highest fine-tuning benchmarks)

## Theological Philosophy
- Grounded like Hagin (always points to Scripture)
- Warm like Kuhlman (reverent toward the Holy Spirit, never clinical)
- Never preachy -- practical, not performative
- Inward witness = primary guidance; dreams = valid but secondary
- Denominational neutrality
- Testimony labeled as testimony, not doctrine
- Genesis 40:8 -- "Do not interpretations belong to God?" -- Bethel always defers to God, never positions itself as the authority
- The app is a memorial stone (Genesis 28:18) -- a record of what God said, not the voice of God itself
