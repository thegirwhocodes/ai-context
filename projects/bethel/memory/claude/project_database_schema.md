---
name: Database Schema
description: Supabase PostgreSQL schema with pgvector for Bethel - tables, embeddings, and data model
type: project
sessions: [e59a15e2-07e1-441a-b5e1-74b37c995b59, efd7d7d2-3b94-4e82-bb2d-7a045a3e9736]
---

## Backend: Supabase (PostgreSQL + pgvector)
- Free tier to start, then ~$25/mo
- Auth: Clerk
- Embeddings: all-MiniLM-L6-v2 (384-dim, run locally)

## Tables (from BETHEL_APP_PLAN.md)

### bible_verses
- book, chapter, verse, text (full NKJV)
- embedding VECTOR(384) for semantic search
- themes, is_dream_related
- chronological_order (for chronological reading mode)

### dream_symbols
- symbol, biblical_meaning (from Troy Brewer's 200+ symbols)
- scripture_refs, cultural_note
- embedding VECTOR(384)

### user_dreams
- user_id, title (LLM-generated), dream_text, dream_date/time
- emotions[], mood (abstract), clarity (vivid/clear/hazy/fragmentary)
- symbols_detected[] (AI-extracted)
- interpretation (AI-generated), user_notes
- scripture_refs[] (relevant verses surfaced)
- jackson_category (one of 20 categories, labeled as framework)
- connected_dream_ids[] (AI-detected connections)
- moon_phase, embedding VECTOR(384)

### user_notes
- note_text, note_type (bible_study/prayer/reflection)
- linked_verse, linked_dream_id
- embedding VECTOR(384)

### reading_progress
- book, chapter, completed_at
- reading_mode (chronological/standard)

### highlights
- book, chapter, verse_start, verse_end
- color (gold/lavender/teal/rose)
- note

### chat_messages
- conversation_id, role (user/assistant)
- content, scripture_refs[], model_used
- dream_context_used (boolean)

### devotionals
- date, scripture_ref, teaching_text, confession_text
- theme, source_inspiration
