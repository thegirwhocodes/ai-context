---
name: Session & Memory Infrastructure
description: The cross-project session export, memory, and backup system built during the Bethel session
type: project
sessions: [e59a15e2-07e1-441a-b5e1-74b37c995b59, efd7d7d2-3b94-4e82-bb2d-7a045a3e9736]
---

## Overview
A comprehensive system for persisting context across Claude sessions, built during the first Bethel session. It works across ALL projects, not just Bethel.

## Components

### 1. Session Transcript Export
- Global hook in `~/.claude/settings.json` fires `hook_export_session.sh` on every user message
- Converts `.jsonl` session logs to readable `.txt` files in `.claude-sessions/` within each project folder
- Uses mtime-based skip logic -- only re-exports changed sessions
- Creates `INDEX.txt` per project listing all sessions with timestamps and first-message previews

### 2. Agent Research Export
- `export_agent_research.py` extracts Agent, WebSearch, and WebFetch outputs from `.jsonl` files
- Saves them as individual `.txt` files in `~/.claude/projects/<PROJECT>/agent-research/`
- Creates `INDEX.txt` per project
- Filenames include session ID prefix + description (e.g., `e59a15e2-07e_WebSearch_TaRL_curriculum.txt`)

### 3. Memory Files
- Live at `~/.claude/projects/<PROJECT>/memory/`
- `MEMORY.md` is the index, loaded automatically into every new Claude session
- Individual memory files have frontmatter (name, description, type, sessions)
- Types: user, feedback, project, reference
- Session IDs in frontmatter link memories back to source transcripts

### 4. CLAUDE.md Instructions (in every project folder)
Two modes:
- **Basic context**: Read memory -> last 5 transcripts -> memory-linked transcripts -> Agent research (not WebSearch/WebFetch)
- **Deep research**: All of above + WebSearch/WebFetch files + full codebase + Grep older sessions
- If user asks about something unrecognized: Grep across `.claude-sessions/` before saying "I don't know"

### 5. OneDrive Backup
- `sync_claude_to_onedrive.py` copies `~/.claude/` to OneDrive hourly
- Runs as macOS launchd agent (survives reboots)
- Skips cache, debug, telemetry -- only syncs important data
- Backup location: `~/Library/CloudStorage/OneDrive-wesleyan.edu/claude-backup/`

### 6. Bootstrap (New Machine Setup)
```
python3 ~/bethel/scripts/bootstrap.py
```
Copies scripts to `~/.claude/scripts/`, sets up hooks, creates memory folders, updates CLAUDE.md, exports all sessions.

## Key Design Decisions
- Session `.txt` files go in project folders (viewable in IDE/Finder), not hidden in `~/.claude/`
- Agent research goes in `~/.claude/` (hidden, not cluttering workspace)
- Memory is the curated summary; transcripts are raw reference
- No summary layer needed -- memory IS the summary
- Scripts are git-tracked in bethel repo so they survive
- `.claude-sessions/` is gitignored (regenerated from `.jsonl`)

## System Metrics (from stress test)
- Hook fires in ~0.03s
- Full export across all projects: ~0.08s
- 71 transcripts, 6.6MB total across all projects
- 709 research files, 3.6MB total
- OneDrive backup: ~637MB
- RAM: ~20-30MB for a split second per hook fire, then exits
