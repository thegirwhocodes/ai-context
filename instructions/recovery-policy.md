# GitHub-backed AI context recovery policy

The private GitHub repository `thegirwhocodes/ai-context` is the source of truth for redacted Codex and Claude context. `~/ai-context` is only its working clone.

## Normal recovery

1. Use the exact `session_id`, transcript path, and working directory supplied by the installed session hook.
2. Read `RECOVERY.md`, then the matching project `INDEX.md` and only the recovery records or curated memory/research needed for the current request.
3. Search with `rg` when a topic is unfamiliar. Do not report missing context until the archive has been searched.
4. Do not read every transcript at the start of an ordinary task. Full-project reading is reserved for explicit deep-familiarization requests.

## Compaction recovery

Recover the exact current task by its hook-provided `session_id`. Never choose a transcript by latest modification time: concurrent Codex or Claude tasks can update other files after the current task.

## Archive and cleanup safety

- Export human-readable user/assistant conversation and curated memory/research only.
- Never commit raw `.jsonl`, SQLite/databases, logs, tool arguments or output, thinking traces, attachments, credentials, auth/config files, or secrets.
- Before raw local history is removed, require a successful archive verification, secret scan, GitHub push, and clean-clone restore verification.
- Raw transcripts, downloaded runtimes, and caches are disposable after those checks. Secrets remain local and encrypted through the separate secrets-backup workflow.

## Durable decisions

Store important architectural decisions in project documentation or curated memory with the originating session ID beside each decision. The scheduled sync will add redacted copies to this repository.
