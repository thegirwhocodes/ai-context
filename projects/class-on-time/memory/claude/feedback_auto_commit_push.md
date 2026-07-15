---
name: Auto-commit and push at every natural checkpoint
description: Don't leave local edits unpushed. Commit + push to GitHub at every meaningful checkpoint without being asked.
type: feedback
originSessionId: a8c172f1-a7d4-4624-8ac2-b31c78a6f870
---
After any meaningful edit batch — typically when typecheck passes, a feature is wired end-to-end, or a self-contained chore is done — commit and push to `origin` without asking.

**Why:** Naomi said: *"I want you to push every time we edit something (within session)."* She doesn't want to micromanage version control and doesn't want the GitHub repo / Vercel deploy to drift behind local state. Vercel auto-deploys on push, so every push is also a deploy — keeps the prod URL fresh.

**How to apply:**
- **Trigger points:** end of each feature, after typecheck passes, after a successful migration, after a new doc is written. Not after every single Edit tool call.
- **Commit messages:** descriptive, focus on the why. Group related edits together. End with the `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` line per existing project pattern.
- **Push without asking:** push to `origin main` straight away. Don't pause for confirmation.
- **Skip if:** there are unresolved typecheck errors, partially-implemented work, or staged secrets — fix or unstage first.
- **Visibility:** end-of-turn summary should mention what was pushed and the new commit short SHA, so she can spot what just landed.

Pair this with the proactive git+Vercel setup memory — once linked, every push deploys to Vercel automatically and she sees changes live.
