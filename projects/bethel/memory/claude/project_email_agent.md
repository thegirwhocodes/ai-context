---
name: email-agent-project
description: "Naomi's personal AI email agent Sage (standalone project under ~/sage) — status & architecture"
metadata:
  node_type: memory
  type: project
  originSessionId: a63e3b98-52ea-48e0-89eb-2340b73532b6
---

`/Users/naomiivie/sage/` is **Sage's standalone project/repo**, moved out of Bethel on 2026-06-22. It is "Claude on a loop" for her Gmail: triage + draft in her voice, with current local runtime still in Tier 1 draft/review mode. Built in sessions after the Mar-29 export, so the docs/code are the source of truth, not `.claude-sessions/`.

**Two layers:** (1) `desktop/` = the real running product — FastAPI backend (`backend/server.py`, port 8765) over the local `gmail.modify` token + a React/Vite dashboard (port 1420). (2) `src/` = a pure-TS two-pass (CaMeL-style quarantine) reference design.

**Completed 2026-06-08 (the autonomous loop — the thing the project is named for, previously missing):**
- `backend/server.py`: added `run_cycle()` + `POST /api/cycle` + `GET /api/digest`; refactored drafting into `_compose_reply` / `_stage_draft`. Cycle = fetch unread → Claude classify (untrusted email as data) → stage a draft per needs-reply → write `triage/triage-<date>.md` + `logs/audit-*.jsonl`. Dedup via `_existing_draft_threads` (never double-drafts). Kill switch = a `STOP` file in the project root.
- `backend/agent_loop.py`: headless runner (`--watch <min>`, `--limit`, `--dry-run`).
- `src/run.ts`: makes `npm run cycle` work (spawns agent_loop.py); fixed `src/agent.ts` classification bug + bound `src/tools.ts` to the backend.
- Dashboard: ⚡ "Auto-draft replies" button (`App.tsx`) calls `/api/cycle`.
- `voice/sage.py`: implemented `--wake` always-on (continuous listen; optional `hey_sage.onnx` OpenWakeWord model gates the spoken trigger).
- Verified: dry-run + live cycle against her real inbox classify correctly; compose produces in-voice replies (and correctly declines to fake-reply to marketing, using `[[Naomi: …]]`); `src/` + frontend typecheck, frontend builds.

**Shipped as a finished app 2026-06-08 (second pass):**
- **`Email Agent.app`** (double-click launcher at project root, custom icon): builds the dashboard, starts the backend, opens a Chrome `--app` window. One process on `:8765` — backend serves the built frontend (`StaticFiles` mount) AND runs the loop. No Rust/Tauri (not installed; chose the lighter `.app`+Chrome route).
- **Always-on scheduler** in `server.py` (`AGENT` dict + daemon thread): auto-runs a live cycle every `interval_min` (default 30), 12s after boot. `GET/POST /api/control` to toggle enabled / set interval / run-now / flip kill switch. Honors `STOP` file live.
- **Dashboard agent bar** (`App.tsx`): autopilot on/off, interval picker, ⚡ Draft-now, Pause/Resume, Kill switch, last-run/next-due status. Polls `/api/control` every 15s.
- Verified live: app opens, autopilot ran, **staged 2 real drafts** in her Gmail (5 needs-reply, 3 already drafted → dedup held); digest + audit written. Frontend typechecks + builds.

**Third pass 2026-06-08 — black ambient UI + native Tauri app (she asked for both):**
- **Black "companion" UI is now the default** (`frontend/src/App.tsx`): full-black screen, one breathing orb, a single agent-voiced line synthesized from cycle counts (e.g. "2 replies are drafted and waiting · 4 things only you should handle"). NO inbox/triage/buttons by default — she explicitly does not want to interface with emails. Mouse-move reveals Pause/Sweep-now/Stop/Details. The old rich dashboard is preserved as `frontend/src/Dashboard.tsx`, reachable via "Details".
- **Native Tauri v2 app** in `desktop/src-tauri/` (Rust). `tauri build` → `Email Agent.app` (custom icon), installed at project root AND `/Applications`. Rust `main.rs` spawns the FastAPI backend on launch (checks :8765 first, no double-bind); window loads the bundled dist; backend serves UI + runs the loop. Installed Rust via rustup (was absent). Verified: app launches, spawns backend in ~5s, native window shows the companion, autopilot sweeps.
- Chrome-`--app` launcher `.app` from pass 2 was REPLACED by the Tauri app (superseded).

**Still open (need her input/hardware):** trained "Hey Sage" wake model (continuous-listen `--wake` works now); iPhone/iPad clients + all-devices sync (PRODUCT_DIRECTION.md PWA/backend-as-service — needs hosting decision). Related: [[project_bethel_vision]].

**Codex completion pass 2026-06-15:**
- Found `oauth/token.json` missing, with only `oauth/token.revoked.20260612-124841.json` present; Gmail actions are correctly blocked until Naomi reauthorizes, while Anthropic is configured. - codex-2026-06-15
- Added Gmail auth/status spine to `desktop/backend/server.py`: secret-safe auth status in `/api/control`, `GET /api/auth/gmail`, `POST /api/auth/gmail/start` to launch the existing local OAuth helper, clean 409 JSON for Gmail-dependent endpoints, and `run_cycle()` now returns a safe setup error instead of stack-tracing when token is missing. - codex-2026-06-15
- Updated the black ambient UI and Details dashboard so Sage says “Gmail needs reconnecting,” disables draft-now while disconnected, exposes Connect Gmail, and keeps typed Sage answers visible when TTS/audio is unavailable. - codex-2026-06-15
- Fixed Sage tool behavior so old `last-digest.json` counts are not spoken as current while Gmail is disconnected; status/walkthrough now give the exact reconnect prompt until auth is restored. - codex-2026-06-15
- Rebuilt and reinstalled the Tauri `Email Agent.app` at both `/Users/naomiivie/bethel/email-agent/Email Agent.app` and `/Applications/Email Agent.app`; previous app bundles backed up under `email-agent/.build-backups/20260615-135051/`. - codex-2026-06-15
- Reloaded `~/Library/LaunchAgents/com.naomi.sleepwell.sage.plist` so the managed backend is single-process, `AGENT_AUTOSTART=0`, and bound to `127.0.0.1:8765` instead of `0.0.0.0`; verified one listener and Sage text status. - codex-2026-06-15
- Added multi-Gmail-account support: legacy `oauth/token.json` still works, new tokens are saved in `oauth/accounts/<safe-email>.json` with registry `oauth/accounts.json`, `POST /api/auth/gmail/start` uses `authorize.py --multi` so Naomi can add more Gmail accounts one by one, and the default desired account hint includes `princessoftheking`. Triage, dry-run/live cycles, drafts, archives, digest output, Sage tool calls, and unlock evidence now carry `accountId` so actions stay in the originating mailbox. - codex-2026-06-15
- Rebuilt and reinstalled the updated Tauri `Email Agent.app` at both project root and `/Applications`; verified backend compile, root TypeScript typecheck, `/api/control` paused with 1 connected mailbox (`nivie@wesleyan.edu`) and desired unconnected `princessoftheking`, `/api/triage` returning account-labelled rows, and the live UI showing Add Gmail + per-row mailbox labels. - codex-2026-06-15
- Renamed the shipped desktop product to **Sage** (`Sage.app`, bundle id `com.naomi.sage`), built a local release DMG at `email-agent/release/Sage_1.0.0_aarch64.dmg`, installed `Sage.app` in `/Applications` and the project root, backed up old `Email Agent.app` bundles under `.build-backups/20260622-132733/`, restricted the backend/launch agent to `127.0.0.1`, added a local origin guard for mutating API calls, fixed npm audit issues, and documented launch/privacy limits in `LAUNCH.md` and `PRIVACY.md`. Naomi has an Apple Developer ID / Apple Developer Program access, so future agents should not treat membership as missing; next public-distribution step is to verify/install the Developer ID Application certificate + notarization credentials and rebuild/notarize. Current DMG is local/ad-hoc signed only. - codex-2026-06-22
- Completed public Mac distribution pass after Naomi supplied Apple notary credentials: Developer ID signed, notarized, and stapled the moved-path `Sage.app` and `release/Sage_1.0.0_aarch64.dmg`; final app submission `191e844e-8c25-442c-8090-cdb4f1064f94`, final DMG submission `8e1773e2-f135-497d-8ffb-79fd1ec2cc39`, final DMG SHA-256 `323dfddc155aa322b08b0620144afd2f0f71157673f35495b3a4612786f4ec1e`; installed notarized `Sage.app` to `/Applications` and `/Users/naomiivie/sage/Sage.app`. - codex-2026-06-22
- App Store Connect notary metadata for Sage: key ID `2VYHFC4L9R`, issuer ID `17f455ea-aa46-4ff2-b066-457922429c8d`; private `.p8` was provided from `~/Downloads` during the June 22 notarization workflow and must not be copied into git, memory, Vercel, or logs. Apple notarization submission `562f137b-96d8-4e94-a06c-989c11caf649` was later checked and returned `Accepted`; stapler validation passed for `/Applications/Sage.app` and `/Users/naomiivie/sage/release/Sage_1.0.0_aarch64.dmg`. - codex-019ef058

## Move-out decision — 2026-06-22 (Claude session 50605635)

- **DONE by Codex:** Sage was moved out of `bethel/` into `/Users/naomiivie/sage`, initialized as a standalone git repo on branch `main`, committed at `8f7aaab` (`Initial standalone Sage app`), with `desktop/` source now tracked and OAuth tokens/venv/logs/release artifacts ignored. Existing `~/sage/prompt.md` was preserved in the new repo. - codex-2026-06-22
- **DONE by Codex:** recreated `oauth/.venv` at `/Users/naomiivie/sage/oauth/.venv`, rewrote `~/Library/LaunchAgents/com.naomi.sleepwell.sage.plist` to `/Users/naomiivie/sage`, rebuilt Tauri so the Rust shell embeds `/Users/naomiivie/sage/...`, reloaded the backend on `127.0.0.1:8765`, verified two Gmail accounts connected, Anthropic ready, origin guard blocking hostile writes, and a dry sweep staging 0 drafts. - codex-2026-06-22
