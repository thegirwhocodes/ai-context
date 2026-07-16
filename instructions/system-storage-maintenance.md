# Mac storage maintenance policy and cleanup ledger

Last updated: 2026-07-16

This file is the canonical handoff for any Codex or Claude session that audits or changes storage on Naomi's Mac. Read it before deleting, offloading, uninstalling, or moving anything for a storage task.

## Standing objective

- Keep at least **50 GB physically free at all times** as the operating reserve for apps, macOS, and swap.
- Use **80 GB physically free** as the immediate cleanup and weekly headroom target, so normal work does not immediately fall through the 50 GB floor.
- Measure real APFS physical availability, not Finder's optimistic/purgeable number and not logical file sizes.
- Do not claim ordinary caches as durable savings when they will predictably refill. Caches may still be cleaned when useful, but report them separately from persistent savings.
- Audit folder by folder. Classify each meaningful item as: protected/keep, active app data, disposable dependency/build, cloud-evictable, archive-to-cloud, abandoned-app leftover, or uninstall candidate.

## Measurement rules

1. Record APFS physical free space before and after each meaningful batch with `diskutil apfs list` and corroborate with `df -h /System/Volumes/Data`.
2. Use allocated, same-filesystem scans such as `du -skx`; do not sum logical file sizes.
3. Exclude mounted simulator/runtime images and other child mounts or they can be double-counted.
4. Treat `dataless` cloud placeholders as zero local bytes even if their logical size is large.
5. Re-measure after background APFS cleanup settles. Report both the measured free space and the exact measurement time.

## Non-negotiable safeguards

- Never directly delete or move `/System`, `/System/Volumes/Preboot`, `/System/Volumes/Recovery`, live `/private/var/db`, live swap/VM files, or macOS boot/security assets.
- `/System/Volumes/Preboot` was measured around 17.3 GB on 2026-07-16. It contains active boot, security, and update assets. It is not a duplicate of `/Library` and must not be moved to OneDrive or deleted manually.
- `/Library` and `~/Library` are different by design: the first is shared machine-level support; the second is Naomi's per-user app data. Similar folder names are not duplicates.
- Do not delete native history under `~/.codex/sessions`, `~/.codex/archived_sessions`, or `~/.claude/projects` merely because readable context is GitHub-backed. Follow `instructions/recovery-policy.md`.
- Never upload `.env*`, tokens, credential files, SSH/GPG material, `~/.secrets`, or unreviewed archives that may contain secrets to OneDrive/iCloud/GitHub.
- Before deleting a project or clone, verify the GitHub remote, clean/pushed status, remote commit, and ignored/untracked contents. Preserve secrets. `node_modules`, `.venv`, `.next`, `dist`, `build`, and Rust `target` are disposable only after the source is proved recoverable.
- Do not remove active application databases or sync indexes as if they were caches. Examples: Spark's mail database, OneDrive/File Provider indexes, Notes, Messages `chat.db`, and Photos library databases.

## Cloud-offload protocol

For user documents or abandoned-app projects that should persist:

1. Identify the actual user documents separately from cache/database state.
2. Copy or export them into a clearly named OneDrive archive folder. Do not include secrets.
3. Produce a manifest with file count, byte count, and hashes for irreplaceable files or archives.
4. Wait until the File Provider reports upload complete (`isUploaded=1`, `isUploading=0`) and the item is not pinned (`isKeepDownloaded=0`).
5. Verify the cloud copy independently when practical.
6. Only then remove the original local source.
7. Use OneDrive **Free Up Space** to make the archive cloud-only, then verify `isDownloaded=0`/`dataless` and zero allocated blocks.
8. Leave a recovery note next to the archive explaining what it contains and how to restore it.

Deleting an app is not the same as deleting its cloud data. For OneNote, uninstall the app only after every notebook is confirmed fully synced to OneDrive/SharePoint and visible from OneNote on the web. Never delete OneNote's container first; it may contain unsynced changes.

Voice Memos is a protected special case. Naomi explicitly decided on 2026-07-16 that every recording must remain playable inside the Voice Memos app. System Settings was checked directly and Apple's native **Voice Memos iCloud switch is on**. Keep the working library at `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings`; do not delete, move, evict, or count its roughly 4.87 GB as cleanup capacity. The verified iCloud Drive export at `Storage Archives/Voice Memos Export - 2026-07-16` is backup-only. Its *downloaded backup copy* may be evicted after upload verification and action-time confirmation, but this must never be confused with deleting the working library. Deleting recordings in Voice Memos also deletes the iCloud-synced originals.

## Cleanup completed on 2026-07-16

- Removed VN Video Editor and its verified orphan data.
- Cleared Safari cache only; browsing history/cookies were not treated as disposable.
- Verified Goodnotes recovery archive, ZIP integrity, SHA-256, and iCloud upload; made it dataless/cloud-only; then removed the local Goodnotes container. Recovery note and archive live in iCloud Drive under `Goodnotes Backup - Recovery`.
- Cleared Apple Mail local data after confirming Naomi uses Spark and Mail sync was disabled for known accounts. Spark's active database was preserved.
- Cleared Messages preview cache without touching attachments, `chat.db`, or iCloud message history. The preview cache fell from about 785 MB to essentially empty; it may regenerate and is not durable strategy.
- Removed unused Slack application leftovers after confirming Slack was not installed/used.
- Removed Cold Turkey leftovers after confirming the app was absent.
- Used supported Xcode tooling to remove the unused iOS 18.6 simulator runtime and unavailable devices. Apparent `du` savings were much larger than physical savings because mounted images had been double-counted; never repeat that reporting error.
- Removed downloaded Command Line Tools update packages and safe shared logs/caches. Kept current Command Line Tools, Python/R frameworks, audio content, system extensions, and active drivers.
- Goodnotes, OneDrive Classes, and other cloud placeholders were evaluated by allocated bytes, not logical size.
- Weekly audit automation moved to Wednesday at 2:00 PM local. A watchdog checks/retries Wednesday and Thursday at 3:00 PM and 5:00 PM because local scheduled work requires the Mac and Codex app to be running.
- Removed abandoned Chrome, OpenAI Atlas, Granola, qBittorrent, old Antigravity, BlockerX, Microsoft Office, Capital One Shopping/Wikibuy, Aiko, VN, Slack, Goodnotes-local, and related verified orphan state. Current Antigravity IDE, OneDrive integration, and iCloud Goodnotes data were preserved.
- Created and verified uploaded iCloud archives for Aiko recordings, Chrome bookmarks, removed-app data, BlockerX settings, Microsoft Office recovery data, and generated E4E fake-child-harness outputs. Exact archive hashes and recovery notes are stored beside the archives.
- Compacted `~/.codex/logs_2.sqlite` from about 392 MB to about 64 MB with SQLite integrity check `ok`; no native sessions or log records were intentionally deleted.
- Removed generated E4E document-render temp files and the generated 878-item fake-child harness only after verified archive upload; final source and legal deliverables were preserved.
- Removed a healthy-but-redundant 202 MB Cursor state-database backup after the live database passed `quick_check`; preserved the live Cursor database.
- Removed about 192 MB of inactive Codex marketplace staging, a 64 MB orphaned `nano-pdf` environment, a 67 MB Xcode DerivedData index, and a 26 MB NVM installer cache. Active Codex/Claude history, current developer runtimes, and live NVM Node remained protected.
- Removed 23 clean Cortex Git worktrees only after fetching GitHub, proving each exact commit existed on a remote branch, proving a clean worktree, and confirming no process used the paths. Preserved main plus four worktrees with local-only or uncommitted state.
- Secured nine credential-named files that were in OneDrive Downloads/Desktop into `~/.secrets/imported-2026-07-16/` with mode `0600`, stopping eight active unencrypted OneDrive uploads. A tenth OAuth credential remains a cloud-only OneDrive placeholder inside `Classes/Qac 386 - Text Mining/Project Pdfs`; do not delete it without first obtaining a verified protected copy. The existing encrypted-backup script exited 2 and does not include these JSON/TXT files, so encrypted backup remains pending and must not be falsely claimed complete.
- Deleted the redundant OneDrive Chrome-bookmarks upload only after proving both files were byte-identical to fully uploaded iCloud copies. The iCloud archive remains.

## Read-only audit on 2026-07-16 — `/Library/Developer`

- Audit ran from 15:44 to 15:51 EDT. APFS physical free space measured 68.7 GB at the start and 66.8 GB at the final check; the change occurred without mutations to `/Library/Developer` and is attributable to normal background/VM activity. The machine remained above the 50 GB reserve and about 13.2 GB below the 80 GB target.
- No files were deleted, moved, or otherwise changed. Persistent savings: 0. Refillable-cache savings: 0.
- The current same-filesystem allocated scan was 2,095,172 KiB (about 2.00 GiB), not the cleaner's earlier 5.93 GB figure. The folder's logical file-byte sum was about 4.81 GiB. The earlier reading likely predates removal of the iOS 18.6 simulator runtime or came from a stale/different accounting view.
- Allocated breakdown: `CommandLineTools` 1,912,596 KiB; `DeveloperDiskImages` 74,064 KiB; `CoreDevice` 72,888 KiB; `PrivateFrameworks` 25,232 KiB; `DeviceKit` 5,304 KiB; and `CoreSimulator` 5,088 KiB.
- Xcode 26.2 is installed and selected at `/Applications/Xcode.app/Contents/Developer`. Package receipts identify `CommandLineTools` as Apple's CLT 26.2 package and most shared device/simulator files as Xcode 26.2 system resources. There were no installed simulator runtimes or devices. Simulator/CoreSimulator processes were actively loading the shared frameworks during the audit.
- Classification: the Xcode device, simulator, framework, and disk-image folders are protected/keep active app data. The separate CLT installation is an active developer dependency/keep while Homebrew is in use; Apple says full Xcode includes command-line tools, but current Homebrew Tier-1 support expects a current standalone CLT and some bottles/source builds can require it.
- Do not move any part of this root-owned, package-managed tree to OneDrive. Fixed paths, permissions, code signing, and immediate local availability are required. Do not delete the whole folder manually; doing so can break Simulator, device debugging/support, Xcode first-launch resources, Homebrew builds, and command-line compilation.
- Supported cleanup route: manage optional runtimes/platforms in Xcode > Settings > Components. None are currently installed here to remove. If Naomi explicitly accepts the Homebrew/tooling tradeoff later, only the 1.82 GiB standalone `CommandLineTools` subtree is a candidate via Apple's documented uninstall procedure, followed by verification that Xcode remains selected and builds/Homebrew still work.
- The Wednesday 2:00 PM weekly audit and Wednesday/Thursday watchdog schedule remain unchanged.

## Current state and pending work from the 2026-07-16 audit

Latest completed whole-volume measurement during this continuation: `df` reported **57,294,248 KiB (about 58.7 GB decimal) physically available** at 17:56 EDT, leaving about **21.3 GB** to reach the 80 GB target. The Mac remains above the 50 GB reserve, but by only about 8.7 GB. Free space is fluctuating while iCloud/OneDrive and Photos are active; `~/Library/Caches/CloudKit` alone reached 11,049,288 KiB. Re-measure after providers become idle; do not claim background drift or cache purge as persistent savings.

### Continuation cleanup and verification at 17:56 EDT

- Voice Memos remains fully protected and playable. The live library passed SQLite `quick_check`, contains 375 finished root recordings plus five old `.composition/fragments` editing files, and allocates about 4.87 GB. The separate iCloud export contains all 375 finished recordings and allocates about 4.56 GB locally. Evict only that downloaded backup copy after action-time confirmation; never touch the working library.
- Cleared 3,303,056 KiB of verified unused refillable caches: stale `/private/var/tmp/SpeechModelCache`, npm cache, npx staging, Cargo registry downloads, and Codex artifact runtimes. No process had files open in those paths. These are useful immediate savings but not durable progress toward the 80 GB target.
- Removed the absent email-assistant Chromium profile `~/.email-agent-app` after confirming the app was absent, no process or launch item referenced it, and no files were open. It reclaimed about 155,768 KiB of persistent abandoned-app state.
- Removed remaining BlockerX containers/scripts/content-rule state and small verified orphan state from SwiftAI, The Video Converter, Capital One EWA, JetBrains/PyCharm 2024.2, Linphone, Ollama, MediaHuman, and other already-absent apps. Shared macOS databases were preserved.
- Uninstalled the unused Homebrew `gemini-cli` leaf and its now-unneeded Homebrew dependency stack. This removed the Homebrew Node executable that an already-broken OpenClaw launch item referenced. OpenClaw `2026.2.6-3` was restored into the protected NVM Node 24.13.0 installation, the launch item was changed to the NVM Node path, and the gateway now listens on `127.0.0.1:18789` with a zero-byte error log.
- Rotated the OpenClaw local gateway token after it was exposed during a diagnostic. The launch plist and all current OpenClaw config/backup copies match the new token; never reproduce either token in a report or command output.
- Photos still reports `Syncing Paused for 325 Items — Low Battery`. Pressing Photos' supported `Sync Now` control immediately returned to the low-battery pause. The Mac is at 7% and the attached adapter supplies only 15 W; connect a proper higher-wattage USB-C charger before Messages or Photo Booth cleanup.
- The weekly audit remains Wednesday at 2:00 PM. The completion watchdog remains active Wednesday and Thursday at 3:00 PM and 5:00 PM.

## Watchdog completion on 2026-07-16 — weekly audit completion check

- The Wednesday weekly audit was not complete enough for watchdog success because it lacked the required 7-day repository hygiene table. This watchdog run completed that missing verification and re-measured whole-volume APFS physical free space.
- Start measurement at 17:01 EDT: `diskutil apfs list` reported **62.7 GB APFS physical free** and `df -h /System/Volumes/Data` reported **58 GiB available**.
- Final measurement at 17:12 EDT: `diskutil apfs list` reported **62.1 GB APFS physical free** and `df -h /System/Volumes/Data` reported **58 GiB available**.
- Reserve/target status at the final measurement: the Mac remained **12.1 GB above** the 50 GB standing reserve and **17.9 GB below** the 80 GB maintenance target.
- Files changed during this watchdog run: this ledger only. No storage cleanup mutations were made elsewhere.
- Persistent savings: **0 GB**. Refillable-cache savings: **0 GB**. The 0.6 GB free-space drift across the run was background APFS/VM activity, not claimed recovery.
- Disposable build-artifact review: `cortex/cortex-web` still holds about 1.12 GiB of `node_modules` and about 0.64 GiB of Rust `target`, but that repository currently has unpushed local source edits and was preserved. Other touched repositories exposed only negligible disposable artifacts during this watchdog pass.

### Coding-task hygiene for repositories touched in the last 7 days

| Result | Repository | Remote / upstream | Notes |
| --- | --- | --- | --- |
| ACTIVE/KEPT | `/Users/naomiivie/.nvm` | `https://github.com/nvm-sh/nvm.git`; no branch upstream | Tool-managed dependency checkout; left untouched. |
| PASS | `/Users/naomiivie/Class on Time` | `origin/main`; `https://github.com/thegirwhocodes/Go.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Dactyl-Final` | `origin/main`; `https://github.com/thegirwhocodes/Dactyl-Final.git` | Clean working tree; not ahead of origin. |
| ACTIVE/KEPT | `/Users/naomiivie/Desktop/Dactyl-Final` | no usable git remote/upstream | Duplicate desktop copy with incomplete `.git` metadata; preserved and not cleaned. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/Documents/git-test` | `origin/editreadme-NI`; `https://github.com/thegirwhocodes/git-test.git` | Untracked `.DS_Store`; no cleanup performed. |
| PASS | `/Users/naomiivie/Education for Equality/curriculum-app` | `origin/feature/advisor-board-notion`; `https://github.com/thegirwhocodes/Education-for-Equality.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Education for Equality/sabi-server` | `origin/main`; `https://github.com/thegirwhocodes/sabi-server.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Rings` | `origin/main`; `https://github.com/thegirwhocodes/Rings.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Social Media/Ed.it` | `origin/main`; `https://github.com/thegirwhocodes/edit.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Social Media/Resolve-OpenCaptions` | `origin/main`; `https://github.com/david-ca6/Resolve-OpenCaptions.git` | Clean working tree; local branch is behind upstream by 5 commits; no unique local work. |
| PASS | `/Users/naomiivie/Social Media/davinci-resolve-mcp` | `origin/main`; `https://github.com/samuelgursky/davinci-resolve-mcp.git` | Clean working tree; local branch is behind upstream by 199 commits; no unique local work. |
| PASS | `/Users/naomiivie/ai-context` | `origin/main`; `https://github.com/thegirwhocodes/ai-context.git` | Watchdog ledger/context updates were committed and pushed to `origin/main` as `5a3c4ce`. |
| PASS | `/Users/naomiivie/bethel` | `origin/backend-foundation`; `https://github.com/thegirwhocodes/bethel.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/bin/downloads-cleaner` | `origin/main`; `https://github.com/thegirwhocodes/downloads-cleaner.git` | Clean working tree; not ahead of origin. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/cortex/cortex-web` | `origin/main`; `https://github.com/thegirwhocodes/cortex-web.git` | Modified `app/onboarding/page.tsx`; large disposable build outputs preserved because source work is still local. |
| PASS | `/Users/naomiivie/cortex/runpod-lora-worker` | `origin/main`; `https://github.com/thegirwhocodes/cortex-runpod-lora-worker.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/cortex/voice-email` | `origin/main`; `https://github.com/thegirwhocodes/email.git` | Clean working tree; not ahead of origin. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/davinci-resolve-mcp` | `origin/main`; `https://github.com/samuelgursky/davinci-resolve-mcp.git` | Untracked `SLASH-COMMANDS-CHEATSHEET.md`; branch also trails upstream by 4 commits. |
| PASS | `/Users/naomiivie/devsync` | `origin/main`; `https://github.com/thegirwhocodes/devsync.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/e4e-knowledge` | `origin/main`; `https://github.com/thegirwhocodes/e4e-knowledge.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/kai` | `origin/main`; `https://github.com/thegirwhocodes/kai.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/naomi-home` | `origin/main`; `https://github.com/thegirwhocodes/naomi-home.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/portfolio` | `origin/main`; `https://github.com/thegirwhocodes/portfolio.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/sage` | `origin/main`; `https://github.com/thegirwhocodes/sage.git` | Clean working tree; not ahead of origin. |

- Weekly audit watchdog status: **completed successfully on Thursday, 2026-07-16**, because the required final APFS physical measurement and per-repository hygiene results are now recorded.

Known pending items:

- OneDrive worship video, about 2.41 GB: upload verified, local copy still downloaded, not pinned. Finder's **Free Up Space** action is ready but requires action-time confirmation before clicking. Verify dataless state afterward.
- OneDrive `Classes`: visible folder is cloud-only in Finder, but OneDrive's hidden File Provider reconciliation backing still allocates about 2.42 GB. Never delete the `.noindex` backing manually. Use Finder **Free Up Space** after action-time confirmation, then wait for provider reconciliation and verify physical recovery.
- Voice Memos, about 4.87 GB: protected/keep by explicit decision. The working library stays local and playable. The uploaded backup export may be made cloud-only, but that is not permission to delete working recordings.
- iCloud Drive archive ZIPs and the downloaded Voice Memos *backup export*: uploads were verified, but Finder preview/download activity eventually materialized the backup to about 4.56 GB locally and grew the CloudKit cache above 11 GB. Finder windows were closed. After action-time confirmation, use **Remove Download** on backup/archive copies only.
- OneDrive is processing a large queue and the battery remained at 7% on a 15 W adapter. Photos reports `Syncing Paused for 325 Items` due low battery, even after the supported `Sync Now` control was pressed. Do not start Photo Booth/CapCut uploads or delete Messages attachments until power is stable and both providers prove sync complete.
- OneDrive credential hygiene: retry materializing the 414-byte `Classes/.../client_secret_8165....json` only after OneDrive is healthy, then move it into `~/.secrets`; improve the encrypted backup to include protected JSON/TXT files and complete it with Naomi's local passphrase interaction. Never print credential contents.
- Messages attachments, about 1.27 GB: 415 unique media items were imported into the Photos album `Messages Attachments Archive — 2026-07-16`, but Photos still has 326 items pending. Do not delete the attachment originals until Photos/iCloud sync is complete, then obtain fresh confirmation because deletion also removes them from Messages/iCloud conversation history.
- Pictures, about 6.84 GB: active optimized Photos Library about 5.27 GB and Photo Booth Library about 1.41 GB. Photo Booth has 57 media files and none matched current Photos originals by exact hash. Import via Photos, verify iCloud completion, then ask before removing the Photo Booth library.
- Music, about 4.77 GB: GarageBand projects about 3.15 GB, Music library about 1.31 GB, plus local recordings. These are user creations, not cache. Archive projects/media before any deletion.
- Movies/CapCut, about 1.42 GB: active user projects plus roughly 1.06 GB of completed exports. No export matched a current Photos original. Import/archive and verify before removal; do not assume project data is disposable.
- Docker and OneNote applications are absent. OneNote notebooks remain OneDrive/SharePoint cloud data; do not delete notebook cloud folders. OneDrive support/index data is active, not the OneNote app.
- Developer dependencies/build outputs: at least several GB across Cortex worktrees, E4E, Downloads app projects, `.next`, `node_modules`, Rust `target`, and standalone Python environments. They are regenerable and safe after Git/GitHub verification, but do not count them as guaranteed persistent free space if active work will immediately recreate them.
- `cortex/cortex-web` still has an uncommitted `app/onboarding/page.tsx` edit, about 1.18 GB `node_modules`, and about 673 MB Rust `target`. Preserve them until the coding task is finished and pushed, then remove only the disposable dependency/build outputs.
- Homebrew `gemini-cli` and its unneeded dependency stack were removed. `openai-whisper` remains a leaf with a private transcription dependency stack of roughly 2.5–2.8 GB. Removing it would disable the Homebrew Whisper CLI until reinstall but would not affect Voice Memos playback; the running VoiceMode Whisper service uses its own `~/.voicemode` service path and has no open Homebrew Whisper files. Await Naomi's explicit choice.
- Safari WebKit website data is about 1.33 GB. TikTok IndexedDB alone contains a 388,743,731-byte exact SHA-256 match of a preserved CapCut export. Removing TikTok site data can log Safari out of TikTok and discard browser-local drafts, so await explicit/action-time confirmation; the CapCut original stays.
- `/private/var/db/diagnostics` plus `uuidtext` hold about 2.55 GB of accumulated system diagnostics. Use only the supported admin command `sudo log erase --all` with Naomi present; never delete database files manually. `/private/var/vm/sleepimage` is expected and must remain.
- Claude has about 759 MB of legitimate staged update data under its ShipIt temp directory. Let Claude finish the update by supported quit/reopen, or delete only if Naomi accepts redownload/update tradeoffs. Do not confuse this with macOS Preboot data.

## App-leftover decision rule

An app folder is removable only when all are true:

1. The app is uninstalled or Naomi confirms it is no longer used.
2. The folder is not shared with another app and is not a macOS component.
3. Real user documents have been exported/archived and verified, or the folder is demonstrably disposable state.
4. Sync has completed and no upload/conflict is pending.
5. A before/after allocated-size measurement is recorded.

When uncertain, report the folder, dependency, failure mode, and supported cleanup route rather than deleting it.

## Handoff format for future audits

Every storage task should leave an update in this file or a dated ledger linked from it containing:

- starting and ending APFS physical free space;
- persistent savings versus refillable-cache savings;
- every path changed and why it was safe;
- cloud verification evidence and recovery location;
- protected/declined items and what would break;
- items awaiting Naomi's confirmation;
- the next scheduled audit and whether its watchdog completed.

## End-of-coding storage hygiene

Every Codex or Claude coding task must finish by proving intended source changes are committed and pushed to the correct GitHub remote. It must then inspect the artifacts it created. Once the source is recoverable and the task no longer needs them, remove disposable `node_modules`, `.venv`/`venv`, `.next`, `dist`, `build`, `coverage`, `DerivedData`, and Rust `target` outputs that are filling the Mac. Never delete unique untracked/ignored work or secrets. If work is incomplete or not safely pushed, report that explicitly and preserve it.

The weekly storage automation must audit repositories touched during the previous seven days and record a per-repository result: `PASS`, `NEEDS PUSH`, `UNIQUE LOCAL WORK`, `ACTIVE/KEPT`, or `CLEANED`. Its watchdog treats the run as incomplete if this check or the final APFS measurement is missing.
