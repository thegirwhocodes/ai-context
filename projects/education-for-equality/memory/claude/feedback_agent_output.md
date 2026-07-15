---
name: Agents must return 90%+ of content, not summaries
description: When spawning agents to read files, they must return at least 90% of the substance — no summaries, no compression
type: feedback
originSessionId: 1b27663d-8ea5-4b35-8186-373ddb166724
---
Agents must return at least 90% of the substantive content they read. No summaries. No "key findings." The actual data.

**Why:** Previous Claudes delegated file reading to agents and got back 10-line summaries of 500-line files. Critical details (costs, names, dates, stats, decisions) were lost. Naomi had to re-explain things that were already in the research files. The point of reading is to have the full picture.

**How to apply:** Every agent prompt that involves reading must include: "Return AT LEAST 90% of the substantive content — every stat, every name, every cost figure, every decision, every date, every technical detail. Do NOT summarize." This applies to all agent calls — research, session readers, file readers. No exceptions.
