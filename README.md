# AI Context (private)

GitHub-backed, redacted recovery context for Naomi's Claude Code and Codex
projects. GitHub is the source of truth; `~/ai-context` is the local working
clone.

## What belongs here

- Readable user/assistant conversation transcripts
- Final Codex subagent reports
- Curated project memory and research exports
- Generated indexes and recovery instructions
- Export, verification, hook, synchronization, and restore tooling

## What never belongs here

- Raw Claude or Codex JSONL
- Tool outputs, shell snapshots, attachments, or application databases
- Auth/configuration files or credentials
- Unredacted API keys, tokens, passwords, cookies, or private keys

## Commands

```bash
python3 scripts/export_context.py --all
python3 scripts/verify_archive.py
python3 scripts/sync_context.py
python3 scripts/install.py
```

Every export is redacted before it is written. Verification must pass before a
commit or push. See `RECOVERY.md` for the generated project/session index.
