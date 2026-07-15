---
name: Ed.it Agent Architecture Review
description: What Ed.it is, the gap between its vision and its build, the 2026 competitive whitespace, and the assemble-the-parts roadmap
type: project
sessions:
  - 3ca6f6d6-cc8f-48a7-ae98-043f8bea4484
  - 6abf9016-437c-4e72-adb6-8c48c164b163
  - e2345bc4-61a0-42d3-9b50-b4685452d6c2
---

# Ed.it — Architecture Review (2026-06-18)

**What Ed.it is:** the standalone evolution of the March DaVinci-Resolve workflow into a purpose-built desktop AI video-editing agent. Python pkg `src/edit/` on the Claude Agent SDK + Gemini + FFmpeg, FastAPI/SSE web UI, Electron shell, SQLite memory, traces DB. Lives at `/Users/naomiivie/Social Media/Ed.it`. M1–M6 shipped. - e2345bc4

**North star (Naomi's words):** "a SUPER intelligent AI agent that can edit your videos for you" that "feels like your video editing friend" — proactive ("I noticed you added clips, want to turn it into a video?"), local-first (no upload, privacy + cost), taste-learning, worship/faith-aware. - 3ca6f6d6

**The core finding — chassis built, engine missing:**
- STRONG (keep, A-grade): agent loop, curated tools w/ structured `{code,message,hint}` errors + safe_path sandbox, prompt-cache-split system prompt, memory schema (supersedes chain + FTS5), traces + budget caps, 16 tests. - e2345bc4
- MISSING (vision vs binary): the Submagic word-by-word captions Naomi asked for FIRST in March do NOT exist in code — no Whisper, no caption engine in pyproject. "Creator modes" are just FFmpeg eq/colorbalance filters; "variations" differ only by crop+contrast. No content-aware cuts, no auto-reframe, no ducking, no real LUTs. Greeting is a static client-side string. Memory is well-designed but never written in real use. - e2345bc4
- Evidence: session ec976ddd — "upgrade the video" → agent just upscaled 1080→1440p, hit disk-full, no captions/variations/Gemini/memory. Session de48c285 — project-root/upload-path confusion bug. - e2345bc4

**2026 landscape / whitespace:** market = cloud GUI auto-clippers (Opus, Submagic, Captions, Klap) + emerging agentic editors (Descript Underlord, Eddie AI, Mosaic, Cardboard, Runway) — ALL cloud. #1 complaint = "AI picks wrong moment, I fix by hand" (taste gap). Local-first + agent-native + taste-learning = unoccupied. CapCut rights backlash + Sora shutdown make privacy/local-economics a real pitch. Faith niche crowded but cloud (Pulpit AI, Sermon Shots, Choppity); they miss quiet sermon moments. - e2345bc4

**Build-by-assembly (parts are all downloadable/local):** WhisperX (word timing, BSD) → libass/ASS karaoke captions (deterministic) OR Remotion (premium) → auto-editor (silence trim) → PySceneDetect/TransNetV2 + Gemini 2.5 Flash (~$0.32/hr hook scoring) → face+TalkNet reframe (AutoFlip is dead) → loudnorm −14 LUFS + VLM frame QA. Wrap as validated EDL/JSON spec → deterministic executor → ffprobe preflight → bounded ≤3-iter self-critique (ELLMPEG: 65%→88%). The moat is the seams, which Ed.it already owns. - e2345bc4

**Recommendation:** stop widening the harness; go DEEP on talking_head end-to-end. Roadmap M7 captions (WhisperX+libass) → M8 smart cuts → M9 quality gate → M10 alive layer (project-state greeting + memory actually writing) → M11 reframe+LUTs → M12 worship mode. Depth over breadth. Full doc: `Ed.it/docs/10_architecture_review_and_roadmap.md`. - e2345bc4
