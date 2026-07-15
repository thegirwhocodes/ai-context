---
name: Social Media Status
description: Current state of what has been built, what works, and what is in progress
type: project
sessions:
  - 4db243fe-8c53-4a06-b646-3267aa36c54d
  - c8aa3c78-c5c9-4c6d-89e7-e4fac7cbd5d3
---

# Social Media Project Status

## Completed
- Full recording studio gear research with tiered recommendations and final decision
- DaVinci Resolve Studio purchased and activated (after email verification troubleshooting)
- MCP server (davinci-resolve-mcp) cloned, configured, and tested — Claude can control Resolve
- Python 3.12 venv set up with all dependencies
- AI video pipeline installed: WhisperX, Gemini 2.5 Flash (API key configured), CrisperWhisper
- Brand identity defined: 5-color palette, 3 content modes, font choices, caption styles
- Instagram brand guide written with profile picture direction, bio, highlight covers
- Color grading presets saved as .cube LUT files (3 modes)
- Comprehensive DaVinci Resolve reference file created (1,159 lines)
- Montserrat and Cormorant Garamond fonts installed for Resolve
- macOS system storage issue diagnosed (Xcode 35GB, OneDrive screen recordings, caches) and ~45GB freed

## First Video: "King of All My Life" Worship Song
- **Source file**: `IMG_9180_new.MOV`
- **Resolve project**: "Video", timeline: "Final Worship Edit"
- **Color grade**: Worship Warm CDL applied (golden warmth, grain, glow, vignette)
- **Captions**: 55 Submagic-styled segments built with Gemini timestamps
  - Montserrat SemiBold, ALL CAPS, white text, black outline, dark background pill
  - Gemini confirmed visual match to Submagic reference
- **Word-by-word highlighting**: Attempted but caused Resolve crashes due to complex Fusion comps

## In Progress / Not Yet Done
- **Word-by-word yellow highlight animation** — the Submagic style where the active word turns yellow (#FFCE34) as it's spoken. Approach pivot: render captions as transparent video overlay using Python (PIL + moviepy) instead of Fusion comps to avoid crashes. Was installing dependencies when session ended.
- **Caption timing refinement** — Gemini timestamps are better than Whisper but user hasn't fully previewed/approved all 55 segments
- **Actual gear purchase** — research is done but no indication gear has been bought yet
- **DJI Osmo Pocket 3** — not yet purchased

## Files Created
| File | Purpose |
|------|---------|
| `studio-setup-research.md` | Gear research with all tiers and final decision |
| `claude-davinci-resolve-workflow.md` | MCP setup instructions and editing workflows |
| `instagram-brand-guide.md` | Full brand system for Instagram |
| `viral-faith-brand-research.md` | Color theory, creator analysis, viral strategy |
| `naomi-profile-for-claude.md` | Comprehensive profile for sharing with new Claude sessions |
| `davinci-resolve-complete-reference.md` | 1,159-line Resolve API + Fusion reference |
| `ai-video-tools-research.md` | Research on AI video analysis tools |
| `ai_video_pipeline.py` | Unified script for WhisperX + Gemini + CrisperWhisper |
| `worship_captions.py` | Original caption generation script using Whisper |
| `IMG_9180_new_captions.srt` | Corrected lyrics SRT file |
| `presets/` | LUT files, caption templates, Submagic style specs |
| `davinci-resolve-mcp/` | Cloned MCP server repo |
| `Resolve-OpenCaptions/` | Cloned caption tool (used for reference on Text+ API approach) |

## Session 2 (c8aa3c78): Storage Cleanup
- Diagnosed 110GB macOS "System Data" — found Xcode at 35GB, OneDrive screen recordings, caches
- Cleared ~45GB: Xcode contents, caches (Spotify, Homebrew, Brave), DerivedData
- Identified it as partly a known macOS bug — Safe Mode reboot helped
- Session ended with API overload error while doing thorough Library analysis
