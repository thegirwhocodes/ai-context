---
name: Cortex feedback and corrections
description: Naomi's corrections, preferences, and working style for the Cortex project
type: feedback
sessions: [0d91dd3c-6d8d-4983-b72b-a1df57377021]
---

## Critical Corrections

1. **Do NOT dismiss per-user LoRA fine-tuning.** A previous Claude steered Naomi to "just use RAG" three times. She pushed back each time and was right. Per-user LoRA is feasible ($0.22-$1.44/user). Never suggest RAG as a replacement for the LoRA vision.

2. **"DON'T JUST WRITE AN ALGORITHM AROUND THIS!!!"** — When she says the AI should decide something, she means a real LLM inference, not a hardcoded heuristic or scoring algorithm. The LLM is the brain.

3. **Always research + plan + get approval before coding.** Naomi wants research on best practices first, then a plan update, then explicit permission before writing code. She said "do deep research on best practices so you don't go and just write wonky code — before making edits, update the plan first — and you'll need to ask for permission to update the plan."

4. **Email agent has pending feedback.** Don't modify the email agent until Naomi shares her specific feedback in a dedicated session. She saw it in action and has opinions.

## Design Preferences

- Jet black (#000000), minimal, non-anxiety-inducing, Inter font
- One thing at a time (email agent shows one email at a time, not a list)
- "Non-anxiety-inducing" is a key differentiator — "4 emails need your reply" instead of "247 unread"
- No clutter, no overwhelm

## Working Style

- Fast-paced, wants to see things working quickly
- Gives feedback in bursts, prefers to address specific items later in dedicated sessions
- Gets excited when things work well ("I'M LOVING THIS APP ALREADY", "YESSSSSS AI WORKING")
- Shares API keys and credentials directly in chat — be careful about security reminders
- Likes to keep building momentum ("keep building" is a frequent directive)
- Sends voice-note-style transcriptions with raw unfiltered ideas

## Technical Context

- Naomi knows Next.js, Supabase, pgvector, Claude API, Clerk, Vercel well
- Built the Sabi voice AI tutor (self-hosted Whisper + Asterisk PBX + YarnGPT)
- Has a Hetzner GPU server running Sabi — keep it separate from Cortex
- Wesleyan student, founder of Education for Equality
