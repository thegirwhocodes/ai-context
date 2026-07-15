---
name: E4E Feedback & Corrections
description: Naomi's corrections, preferences, and important clarifications for how Claude should work on this project
type: feedback
sessions: [ff1faa52, f19ca767, efd7d7d2, 7464be26, 296c88b8, d72670bf]
---

# E4E — Feedback & Corrections

## Critical Corrections

### "Sabi is the delivery channel"
- **Wrong**: "Sabi is the product" or "Sabi is the AI tutor platform"
- **Right**: "Sabi IS the voice delivery channel" — one of two channels under Education for Equality
- Naomi corrected this directly: "Sabi is the delivery channel - you are my technical co-founder ensure you understand absolutely everything about what we're building"

### Bakame is NOT a partner
- Initially explored as partner, then discovered IP tension
- Naomi chose independence — do not reference Bakame as a partner or co-creator
- Replace all "Bakame" references with "Sabi" in any document
- De-emphasize "Cambridge-aligned" framing — focus on foundational literacy/numeracy via AI voice

### EKOEXCEL Attribution
- Dr. Sonia Ivie works at EKOEXCEL and is on E4E's board, but E4E did NOT conduct EKOEXCEL's research
- Always attribute EKOEXCEL data to EKOEXCEL/NewGlobe, not to E4E

### Don't use Rasa
- Claude independently concluded Rasa is wrong: Classic dying, Pro costs $35K+/year
- Use lightweight script engine + Ollama fallback instead

## Work Preferences

### Thoroughness
- "search THOROUGHLY", "every nook and cranny" — Naomi expects exhaustive research, not surface-level
- Read ALL context before making recommendations
- Check all files, all folders, all conversation history

### Build Quality
- "bro - please build everything properly please" — no shortcuts, no half-deployments
- If deploying something (like a voice), make sure it actually works end-to-end
- Don't deploy a reference voice file path without confirming the file is on the server
- When Naomi asks to build something new in the curriculum app/site, push/deploy it to Vercel as part of the work, not just localhost. - codex-20260615

### Document Style
- CSS-styled markdown for PDF export (12pt body, 13pt headings, 9pt tables, 8pt paragraphs)
- Protect IP in external-facing documents — describe WHAT, not HOW
- Keep copyright briefs to 2-3 pages max
- When adding Naomi's own text to documents, use it directly — "whether paraphrased or not"

### Don't Over-Research
- When Naomi says "ENOUGH" — stop immediately
- Don't run 15 WebSearch calls when 3 would suffice
- Get to building, not endlessly planning

### Cost Consciousness
- Always show cost breakdowns in tables
- Compare to alternatives (Twilio vs AT, USPTO vs Nigeria trademark)
- Naomi notices when costs are high and pushes back
