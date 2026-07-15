---
name: Never delete without backup
description: Always backup or commit code before deleting anything - user was upset about losing Expo codebase
type: feedback
sessions: [e59a15e2-07e1-441a-b5e1-74b37c995b59, efd7d7d2-3b94-4e82-bb2d-7a045a3e9736]
---

NEVER delete code without backing it up first (git commit or copy to a backup folder).

**What happened:** Deleted the entire Expo codebase without committing or backing up first when switching to native Swift. The user was rightfully upset -- "bro you just deleted without any backup??" Even when switching frameworks, the old code has value as reference.

**How to apply:** Before any `rm -rf` or major deletion, always `git add && git commit` first, or copy to a backup directory. Ask the user before destructive operations.
