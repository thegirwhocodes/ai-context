---
name: Social Media Tech Stack
description: Tools, DaVinci Resolve setup, automation scripts, MCP integration, and AI video pipeline
type: project
sessions:
  - 4db243fe-8c53-4a06-b646-3267aa36c54d
---

# Social Media Tech Stack

## Recording Studio Gear (Final Decision)
| Category | Item | Cost |
|----------|------|------|
| Audio Interface | Focusrite Scarlett Solo 4th Gen | ~$130 |
| Music Mic | Audio-Technica AT2020 (XLR, condenser, needs phantom power) | ~$99 |
| YouTube Mic | Samson Q2U (USB+XLR dual, dynamic) | ~$70 |
| Headphones | Sony MDR-7506 | ~$80 |
| Camera | DJI Osmo Pocket 3 (buy used ~$400-500, tariff inflated to $799 new) | ~$400-500 |
| Camera Mount | AMAZEAR magnetic wall mount + adhesive iron plates | ~$20 |
| Video Editor | DaVinci Resolve Studio ($295 one-time, purchased) | $295 |
| DAW | GarageBand (free on Mac) | Free |
| Total | | ~$1,125-1,240 |

### Why These Choices
- AT2020 over Q2U for music: condenser captures 20Hz-20kHz (vs dynamic 50Hz-15kHz), more detail for vocals + acoustic guitar
- Q2U for YouTube: USB direct to computer, no interface needed, rejects room noise
- Pocket 3 over GoPro/Action 5: 1-inch sensor, face tracking, flip screen, cinematic look for indoor talking-head content
- DaVinci Resolve Studio over free: enables external scripting (Claude MCP), AI captions, neural engine features

## DaVinci Resolve Setup
- **Version**: DaVinci Resolve Studio 20.3.2
- **License**: Purchased ($295 one-time), activated after email verification issue
- **External Scripting**: Enabled (Preferences > System > General > "Local")
- **Installed Fonts**: Montserrat (all 18 weights), Cormorant Garamond (from Google Fonts)
- **Python Version for Scripting**: Python 3.12.6 (`/usr/local/bin/python3.12`) — Resolve requires 3.10-3.12, user has 3.14.3 as default

## MCP Server (Claude <-> Resolve)
- **Repo**: samuelgursky/davinci-resolve-mcp (cloned to `/Users/naomiivie/Downloads/App/Social Media/davinci-resolve-mcp/`)
- **Config**: `.mcp.json` configured for Claude Code
- **Venv**: Python 3.12 virtualenv with all dependencies
- **Capabilities**: 342 tools covering full Resolve API — project management, timeline editing, color grading, Fusion compositions, rendering

## AI Video Pipeline
Three tools installed in the venv at `Social Media/davinci-resolve-mcp/.venv/`:

### 1. WhisperX (free)
- Sub-50ms word-level timestamps
- Better than regular Whisper for precise caption timing
- Usage: `get_captions("video.mov", prompt="lyrics hint")`

### 2. Gemini 2.5 Flash
- Can literally WATCH video and describe scenes, find edit points, compare caption styles
- API key stored in shell profile as `GEMINI_API_KEY`
- Cost: ~$0.054 per 10-minute video
- Used to analyze Submagic reference clips and verify caption styling matches

### 3. CrisperWhisper (free)
- Detects filler words ("um", "uh") and pauses
- Useful for talking-head auto-editing
- Cloned to Social Media folder

### Unified Script
- `/Users/naomiivie/Downloads/App/Social Media/ai_video_pipeline.py` — imports all three tools

## Color Grading Presets
Saved as `.cube` LUT files at `/Users/naomiivie/Downloads/App/Social Media/presets/`:
- `Naomi_Base_Warm.cube` — talking head videos
- `Naomi_Worship_Warm.cube` — worship/music (deeper golden warmth)
- `Naomi_Lifestyle_Bright.cube` — lifestyle (warm but brighter)

### Worship CDL Settings (Corrected)
- Slope: R:1.05 G:1.00 B:0.88
- Offset: R:0.01 G:0.005 B:-0.01
- Fusion effects: Film Grain 10%, Soft Glow (blend 5%, gain 1.0, threshold 0.7), Vignette 80%

## Caption Templates
- `/Users/naomiivie/Downloads/App/Social Media/presets/worship_caption_template_v2.comp`
- `/Users/naomiivie/Downloads/App/Social Media/presets/worship_effects_chain.comp`
- `/Users/naomiivie/Downloads/App/Social Media/presets/submagic_style_specs.md`

## Key Reference Files
- `/Users/naomiivie/Downloads/App/Social Media/claude-davinci-resolve-workflow.md` — full MCP setup and workflow docs
- `/Users/naomiivie/Downloads/App/Social Media/davinci-resolve-complete-reference.md` — 1,159-line reference covering all Fusion Text+ params, CDL API, rendering, batch export
- `/Users/naomiivie/Downloads/App/Social Media/ai-video-tools-research.md` — research on AI video analysis tools

## Known Issues
- Resolve crashes when too many complex Fusion compositions (multiple Text+ with Merge nodes) are on the timeline — solution: render captions as transparent video overlay with Python, import as single file on track 2
- Subtitle styling (font, color, position) cannot be set via Resolve API — must use Fusion Text+ comps or manual Inspector styling
- SRT import via API places subtitles at wrong frame offset — workaround: add 1-hour timecode offset to SRT or use CreateSubtitlesFromAudio then fix text
- Whisper misses soft "Oh"s against guitar — Gemini video analysis catches them better