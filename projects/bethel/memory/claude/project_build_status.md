---
name: current-build-status
description: "What has been built, what is in progress, and what is next for Bethel"
metadata: 
  node_type: memory
  type: project
  sessions: 
    - e59a15e2-07e1-441a-b5e1-74b37c995b59
    - b964802c-7753-4500-8b6e-fea84b85ad09
    - efd7d7d2-3b94-4e82-bb2d-7a045a3e9736
    - 86c89090-9d07-4f5c-ac46-50629db75b25
    - 0d91dd3c-6d8d-4983-b72b-a1df57377021
  originSessionId: 206a510c-15a9-493c-871b-756300bdb015
---

## Update — June 12, 2026 ("complete everything" session, continued in same conversation)

Naomi: "complete everything about Bethel." Built and committed (`a93a98e` on `backend-foundation`):

1. **Bible reader finished:** prev/next chapter nav crossing book boundaries (follows reading order), swipe gestures, font-size slider 14-28, **3 reading themes (Midnight/Warm Night/OLED)**, real progress bar, "Ask Bethel about this chapter" → chat. `ReadingStore` (UserDefaults) persists position/completion/streak/preferences.
2. **Chronological mode:** book-level order-of-events (`BibleOrder.swift`), toggle in Bible tab + Profile; read chapters marked gold in grid. Verse-level interleaving still future (Supabase chronological_order column).
3. **Today's Devotional:** AI-generated daily, Hagin Faith Food (Scripture→Teaching→Confession), personalized to current reading + recent dreams, cached per-day. `DevotionalStore` + `DevotionalView`.
4. **Dream pipeline complete:** AI titles untitled dreams (structured JSON output via `output_config.format json_schema` — **verified live**, returned "The Endless Golden Stairway" + Gen 28:12 reflection); **125-entry biblical dream-symbol dictionary** (`Bethel/Resources/dream_symbols.json`, scripture-ref'd, authored from biblical first-mention symbolism since the research only *described* Brewer's book) matched into AI context via `SymbolService`. Doubles as Supabase `dream_symbols` seed.
5. **Home real:** Continue Reading (real position), Today's Word = real WEB text looked up from bundled Bible rotated daily (verified on-screen: Psalms 23:1), Recent Dreams live list, streak card. **Profile real:** live stats + working theme/font/mode settings. `AppRouter` for cross-tab nav.

**⚠️ DISK CRISIS during session:** Her Mac hit 0 bytes free TWICE (228GB disk, was 99% full). Freed ~5GB by deleting (all regenerable): app caches (codex 2.1GB, ShipIt, Spotify, updaters), old build artifacts in Downloads/App/Bethel, **the torch venv `scripts/bethel/.venv` (898MB) and `~/.cache/huggingface` (551MB)** — recreate with `python3.12 -m venv scripts/bethel/.venv && .venv/bin/pip install sentence-transformers` when Supabase embedding time comes. ~4GB free at session end. **Naomi should clear more space** — this will recur.

**Still open:** Supabase go-live (blocked on her creating the project), highlights/notes in reader, custom fonts (Satoshi/Inter/Literata files), animations polish, on-device embeddings, LoRA (Phase 7), GitHub remote (repo has none; email-agent privacy consideration — another session committed email-agent code to this same repo).

## Update — June 7, 2026 (backend foundation session)

Naomi: "continue the Bethel plan, don't fail." Chose **backend foundation** as the milestone. Done this session (branch `backend-foundation`, all committed):

1. **Codebase reconciliation (important):** the real buildable Xcode project lived at `/Users/naomiivie/Downloads/App/Bethel/` and was AHEAD of the git repo — it had `Services/BibleService.swift` + `DreamStore.swift` and a BibleService-backed reader the git copy lacked. Consolidated the Xcode project INTO the git repo at `/Users/naomiivie/bethel/`. Downloads kept as backup. **Going forward, `/Users/naomiivie/bethel/` is the single source of truth.**
2. **Build fixes:** deployment target 26.2 → 18.0 (was unbuildable + unshippable); added shared scheme (xcuserdata-only before). Only iOS 18.6 simulator runtime installed; build via `xcodebuild -project Bethel.xcodeproj -target Bethel -sdk iphonesimulator build`. **App builds + launches in sim** (home screen verified).
3. **Full Bible loaded:** `scripts/bethel/ingest_bible.py` pulls all 66 books (31,095 verses) from getbible.net. Bundled `Bethel/Resources/bible.json` (4.7MB); BibleService now serves the whole Bible offline. **Translation = WEB (World English Bible, public domain).** NKJV is copyrighted (Thomas Nelson, ~500-verse quote limit) — can't ship full NKJV without a license; WEB ships now, swap later. Naomi was told this.
4. **Supabase schema:** `supabase/migrations/0001_bethel_init.sql` — all tables, `vector(384)` cols, HNSW cosine indexes, `match_verses/match_symbols/match_user_dreams` RPCs, RLS. **Auth deferred → single-user**; user data (dreams) stays LOCAL (DreamStore JSON) until auth added. Only shared knowledge (bible/symbols/devotionals) needs the DB.
5. **Swift Supabase layer:** `SupabaseConfig` (reads gitignored `Secrets.plist`) + `SupabaseService` (async REST, match RPCs). App runs fully offline until configured.
6. **Embedding pipeline:** `scripts/bethel/embed_and_load.py` — all-MiniLM-L6-v2 (384-d) via a py3.12 venv (`scripts/bethel/.venv`; py3.14 has no torch). Verified end-to-end (dry-run → 384-dim). Ready to embed + upsert once DB exists.

7. **AI BRAIN WIRED (went past backend foundation, same session):** `BethelAI.swift` calls the Claude Messages API (`claude-opus-4-8`, adaptive thinking) via raw HTTPS (Swift has no official Anthropic SDK) with a scripture-grounded system prompt (Hagin grounding + Kuhlman warmth, cites WEB Scripture, defers to God Gen 40:8). **Ask Bethel chat now uses the real model** (was a hardcoded 2s canned reply). **Dream flow fixed end-to-end:** NewDreamView now persists via DreamStore (was a no-op!), JournalView reads DreamStore (was a dead empty array!), new `DreamDetailView` shows "Bethel's Reflection" (AI interpretation generated on save). Verified against live API (cited Ecclesiastes 5:3). `Secrets.swift` reads gitignored `Secrets.plist` (ANTHROPIC_API_KEY filled from cortex trove). ⚠️ key-in-app is dev-only; needs a proxy before public release.

**BLOCKED on Naomi (for the DB/RAG layer):** create the dedicated **Bethel Supabase project** (separate from cortex per memory) or provide a `SUPABASE_ACCESS_TOKEN`. Then: run migration → `embed_and_load.py` (verse embeddings) → fill SUPABASE_URL/ANON_KEY in `Secrets.plist`. The AI works WITHOUT this (uses the model's own scripture knowledge); Supabase adds pgvector RAG (verse retrieval, dream-similarity, personal symbol dict).
**Next steps:** runtime embedding source for queries/dreams (on-device CoreML MiniLM vs Supabase Edge Function); seed `dream_symbols` (Brewer 200+) + `devotionals` from research files; premium UI polish (fonts Satoshi/Inter/Literata, 3 reading themes, animations); LoRA training (Phase 7).
Reusable creds trove: `/Users/naomiivie/cortex/cortex-web/.env.local` (has cortex's Supabase, Clerk, Anthropic keys).

## Current State (as of March 19, 2026)

### Completed
- Comprehensive app plan written at `/Users/naomiivie/bethel/BETHEL_APP_PLAN.md`
- All 7 research documents thoroughly reviewed
- Memory system set up with session export hooks, agent research export, cross-project CLAUDE.md
- Stress-tested memory system: 87 PASS, 0 FAIL across all projects
- OneDrive backup system (hourly sync via launchd agent)

### Native iOS App (Scaffolding Only)
**Location:** `/Users/naomiivie/Downloads/App/Bethel/` (Xcode project) and `/Users/naomiivie/bethel/Bethel/` (source)

12 Swift files built:
- `BethelApp.swift` -- App entry point, dark mode
- `ContentView.swift` -- Tab controller + custom tab bar
- `BethelTheme.swift` -- Full design system (colors, fonts, spacing)
- `MoonPhase.swift` -- Moon phase calculation
- `GlassTabBar.swift` -- Glassmorphic tab bar with blur
- `HomeView.swift` -- Greeting, daily verse, quick actions
- `BibleView.swift` -- OT/NT toggle, book list, chapter grid
- `ChapterReaderView.swift` -- Premium reader, auto-hiding chrome, serif font
- `JournalView.swift` -- Dream list, empty state, FAB
- `NewDreamView.swift` -- Dream editor, mood circles, clarity pills
- `BethelChatView.swift` -- AI chat, suggested prompts, thinking state
- `ProfileView.swift` -- Stats, settings, Genesis 28 quote
- `BibleService.swift` -- Bible data layer
- `DreamStore.swift` -- Dream persistence

Build: SUCCEEDED on iPhone 17 Pro simulator (iOS 26.2)
App ran in simulator successfully.

### Expo Web Preview
**Location:** `/Users/naomiivie/bethel/web-preview/`
- Basic Expo project created for desktop UI prototyping
- Not fully built out

### Session/Memory System Scripts
**Location:** `/Users/naomiivie/bethel/scripts/` (git tracked) and `~/.claude/scripts/` (active)
- `session_context_export.py` -- Per-project session exporter
- `export_all_sessions.py` -- Bulk export all projects
- `export_agent_research.py` -- Exports Agent + WebSearch + WebFetch results
- `hook_export_session.sh` -- Hook wrapper (fires on every message)
- `setup_memory_system.py` -- Creates memory folders for all projects
- `setup_all_projects.py` -- Exports + CLAUDE.md for all projects
- `update_all_claude_md.py` -- Updates CLAUDE.md everywhere
- `sync_claude_to_onedrive.py` -- Hourly OneDrive backup
- `install_sync_agent.py` -- Installs launchd agent for auto-sync
- `bootstrap.py` -- Recreates everything on a new machine
- `stress_test.py` -- Validates the entire system

## NOT Yet Built
- Real Bible text parsing (NKJV content)
- Chronological Bible ordering
- Supabase backend integration
- AI chat (Claude API or LoRA integration)
- Dream interpretation engine
- Dream resurfacing (LLM-driven)
- Daily devotional (Hagin structure)
- User authentication (Clerk)
- Personal symbol dictionary
- Bible verse embeddings in pgvector
- LoRA training data generation
- LoRA fine-tuning

## What's Next
1. Parse full NKJV into structured data
2. Build chronological ordering index
3. Connect Bible reader to real text
4. Set up Supabase backend
5. Implement dream journal with persistence
6. Integrate Claude Haiku API for AI chat
7. Build dream interpretation pipeline
8. Generate LoRA training data from research files

## Spring Break Plan (from session 86c89090, March 16, 2026)
Naomi planned 2 days of focused coding on the Bible app (Mon-Tue), followed by 3 days on Cortex (Wed-Fri). This was the intended schedule for building Bethel's core features.
