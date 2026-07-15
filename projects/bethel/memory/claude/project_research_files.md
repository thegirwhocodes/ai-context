---
name: Research Files Summary
description: Index and summary of all 7 research documents that form Bethel's knowledge foundation
type: reference
sessions: [e59a15e2-07e1-441a-b5e1-74b37c995b59, efd7d7d2-3b94-4e82-bb2d-7a045a3e9736]
---

All research files live at `/Users/naomiivie/bethel/research/`.

## 1. BETHEL_BIBLICAL_RESEARCH.md (~1,355 lines)
- All 52+ dreams/visions in the Bible, organized chronologically Genesis to Revelation
- Full NKJV text, interpretations, fulfillment records, categorization
- 22 key theological scriptures about dreams
- Complete interpretation framework from Joseph and Daniel
- Hebrew/Greek terminology tables
- Every mention of "Bethel" in scripture

## 2. BETHEL_HAGIN_RESEARCH.md (~273 lines)
- Kenneth Hagin biography and theological framework
- Hierarchy of divine guidance: inward witness > inward voice > voice of the Spirit > visions/dreams
- Spirit-soul-body distinction
- Logos vs. rhema framework
- Four steps to train the human spirit
- Faith Food devotional structure: Scripture > Teaching > Confession
- Bibliography of 139 titles

## 3. BETHEL_KUHLMAN_RESEARCH.md (~262 lines)
- Kathryn Kuhlman biography and theology
- Holy Spirit as a Person (not just a force)
- Surrender/yielding theology
- Her dream about three men and Jesus
- Approach to hearing God
- Key quotes and 14+ books
- Synthesis: Kuhlman complements Hagin (Word + Spirit)

## 4. BETHEL_DREAM_MANAGEMENT_RESEARCH.md (~628 lines)
12 parts covering:
- John Paul Jackson's 20 dream categories
- Mark Virkler's 4 Keys to Hearing God's Voice
- Charity Kayembe's methodology
- Stephanie Ike Okafor's framework
- Adrian Beale's 8 steps
- Troy Brewer's 200+ dream symbols with biblical references
- Spurgeon on dreams, C.S. Lewis on supernatural, Smith Wigglesworth on visions
- Best practices for prophetic dream journaling
- 10+ key scriptures for LoRA training data

## 5. BETHEL_COMPETITIVE_ANALYSIS.md (~153 lines)
- YouVersion, Glorify, Logos, Bible Project, Bible Chat
- FaithGuide, Bible.ai, CrossTalk, Illuminate Bible
- Dreamnl, Dream Keys, Biblical Dreams App
- General dream journal apps
- Bethel's unique positioning: "first app that treats dreams and Bible reading as one connected journey"

## 6. BETHEL_UI_RESEARCH.md (~307 lines)
- Full dark-mode design system with color tokens
- Typography specifications
- Screen-by-screen wireframes
- Animation specifications
- Design references (Glorify, Bear, Arc, Apple Books, Claude, Day One)

## 7. BETHEL_LORA_ARCHITECTURE.md (~718 lines)
- Complete 4-layer AI pipeline specification
- Training data validation pipeline (Aligned/Extrapolated/Testimony/Contradicts)
- Serving infrastructure (LoRAX, VRAM budgets)
- Cost analysis
- 6-phase implementation plan

## Additional: BETHEL_TECH_STACK_RESEARCH.md (created during session)
- Research on what premium Bible/journal apps are built with
- Native vs cross-platform analysis
- Led to the decision to switch from Expo to native Swift/SwiftUI

## Naomi's Plan: Bethel naomi plan.md (root)
- Core LLM trained on Bible + dream interpretation experts
- Agentic layer where the LLM creates tasks itself
- Build dependencies for the agentic layer
- Long-term: LoRA on Bible for accuracy validation, LoRA on Daniel for cross-book pattern recognition

## Cross-Project Research (relevant to Bethel)

### PERSONAL_LLM_RESEARCH.md (from Cortex session 0d91dd3c)
- Located: `/Users/naomiivie/cortex/PERSONAL_LLM_RESEARCH.md`
- Written when Claude finally validated per-user LoRA feasibility
- Contains: LoRA costs ($0.22-$1.44/user cloud, $0.02 Mac), base model comparisons, training formats, serving infrastructure, privacy analysis
- Directly informs Bethel's per-user LoRA plan for power users with 500+ dreams

### RAW_TRANSCRIPTION_NOTES.md (original voice memos)
- Located: `/Users/naomiivie/cortex/RAW_TRANSCRIPTION_NOTES.md`
- Contains Naomi's original voice-transcribed ideas for Bethel (Chronological Bible + Dreams + Notes)
- Section on dreams: "Log dreams God gives you, with interpretation notes. Smart resurfacing -- the right dream surfaces at the right time."

### Life LLM IDEA files
- Located: `/Users/naomiivie/Life LLM/`
- 7 IDEA.md files covering all Naomi's app concepts
- `1-chronological-bible-app/IDEA.md` and `2-dream-and-notes-manager/IDEA.md` are the direct Bethel precursors
