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

Latest completed whole-volume measurement during this continuation: `df` reported **52,191,380 KiB (about 53.4 GB decimal) physically available** at 20:02 EDT, leaving about **26.6 GB** to reach the 80 GB target. Naomi ended the manual cleanup at that point. The Mac remained above the 50 GB reserve, but by only about 3.4 GB. Free space had fluctuated downward while iCloud/OneDrive, Photos, swap, and other background services were active; `~/Library/Caches/CloudKit` alone had exceeded 11 GB. Do not claim that background drift or cache purge as persistent cleanup savings.

### Continuation cleanup and verification at 17:56 EDT

- Voice Memos remains fully protected and playable. The live library passed SQLite `quick_check`, contains 375 finished root recordings plus five old `.composition/fragments` editing files, and allocates about 4.87 GB. The separate iCloud export contains all 375 finished recordings and allocates about 4.56 GB locally. Evict only that downloaded backup copy after action-time confirmation; never touch the working library.
- Cleared 3,303,056 KiB of verified unused refillable caches: stale `/private/var/tmp/SpeechModelCache`, npm cache, npx staging, Cargo registry downloads, and Codex artifact runtimes. No process had files open in those paths. These are useful immediate savings but not durable progress toward the 80 GB target.
- Removed the absent email-assistant Chromium profile `~/.email-agent-app` after confirming the app was absent, no process or launch item referenced it, and no files were open. It reclaimed about 155,768 KiB of persistent abandoned-app state.
- Removed remaining BlockerX containers/scripts/content-rule state and small verified orphan state from SwiftAI, The Video Converter, Capital One EWA, JetBrains/PyCharm 2024.2, Linphone, Ollama, MediaHuman, and other already-absent apps. Shared macOS databases were preserved.
- Uninstalled the unused Homebrew `gemini-cli` leaf and its now-unneeded Homebrew dependency stack. This removed the Homebrew Node executable that an already-broken OpenClaw launch item referenced. OpenClaw `2026.2.6-3` was restored into the protected NVM Node 24.13.0 installation, the launch item was changed to the NVM Node path, and the gateway now listens on `127.0.0.1:18789` with a zero-byte error log.
- Rotated the OpenClaw local gateway token after it was exposed during a diagnostic. The launch plist and all current OpenClaw config/backup copies match the new token; never reproduce either token in a report or command output.
- Photos still reports `Syncing Paused for 325 Items — Low Battery`. Pressing Photos' supported `Sync Now` control immediately returned to the low-battery pause. The Mac is at 7% and the attached adapter supplies only 15 W; connect a proper higher-wattage USB-C charger before Messages or Photo Booth cleanup.
- The weekly audit remains Wednesday at 2:00 PM. The completion watchdog remains active Wednesday and Thursday at 3:00 PM and 5:00 PM.
- Removed three clean, upstream-recoverable third-party Social Media clones after fetching their remotes, proving clean working trees, proving each HEAD existed remotely, checking ignored files, excluding secrets, and confirming no process used them: `CrisperWhisper` (9,096 KiB), `Resolve-OpenCaptions` (852 KiB), and the duplicate `davinci-resolve-mcp` clone (about 32,240 KiB). The separate root `~/davinci-resolve-mcp` clone with unique local context was preserved.
- Removed a 5,548 KiB `.next` build from clean/pushed `~/naomi-home`, an empty 16 KiB Desktop `Dactyl-Final` shell containing only `.DS_Store`/empty directories, and about 7,368 KiB of June NGL logs/markers after proving the app, processes, and launch items were absent.
- A local-only SHA-256 duplicate audit skipped dataless cloud placeholders and found about 757,428,994 logical duplicate bytes. Most are identical WAV files embedded separately in four GarageBand project bundles; they were preserved because deleting project-internal media could break self-contained projects. A duplicate `Adonai Pt1.m4a` also remains pending user choice. No personal media was deleted.
- User ended the manual cleanup after these checks. Voice Memos remained protected and playable, and no pending cloud-only eviction, Messages/Photos deletion, Homebrew Whisper removal, Safari site-data removal, app uninstall, or admin log erasure was performed without confirmation.

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

## Coding-task cleanup on 2026-07-20 — Sleep Well iPhone Cold Block

- Repository result: **PASS** for `/Users/naomiivie/Downloads/App/Sleep`. The working tree was clean after commit `c18dcf6e041db368dcda4ad2606eefaf44dcf5af`, and `git ls-remote` proved the exact commit was present on `origin/codex/cold-turkey-enforcement` at `https://github.com/thegirwhocodes/sleep-well.git`. GitHub CI passed both the iOS and macOS builds.
- Removed only task-created disposable outputs after that proof: `/tmp/sleepwell-coldblock-derived`, `/tmp/sleepwell-coldblock-device`, `/tmp/sleepwell-coldblock-macos`, and `/tmp/sleepwell-coldblock-module.Aukb77`. Their allocated `du -sk` total was 114,096 KiB. No source, installed app, secrets, sessions, dependencies, or user data were removed.
- APFS physical free space was 47,440,494,592 bytes at 16:05:30 EDT before cleanup and 47,560,564,736 bytes at 16:05:49 EDT afterward. `df -k /System/Volumes/Data` increased from 46,328,676 KiB to 46,446,132 KiB available. Treat the approximately 120 MB recovery as disposable build-output savings, not durable capacity.
- Reserve status: the final 47.6 GB APFS physical free measurement was about 2.4 GB below the 50 GB standing reserve and about 32.4 GB below the 80 GB target. No unrelated cleanup was performed during the coding task; a dedicated storage continuation is needed to restore the reserve safely.

## Coding-task cleanup on 2026-07-20 — Cortex Supabase scheduler verification

- Repository result: **PASS** for `thegirwhocodes/cortex-web`. `git ls-remote` proved exact candidate `6ea044b79775bc27f6c0f40684086f02b1ab4fb1` on `origin/agent/final-integration-redo`; its direct parent `b70153f48c9f939302d48abc7eb16eb90d65fe52` owns the verified Supabase scheduler correction. PR #32 had two successful CI runs (`29778981934` and `29778978997`). Local verification passed 836 tests, static launch checks with zero failures, lint, TypeScript, production build, and a zero-vulnerability npm audit at the exact remote candidate.
- Removed only two task-created disposable worktrees after that proof: `/Users/naomiivie/cortex/.worktrees/cortex-scheduler-hobby-audit` and `/Users/naomiivie/cortex/.worktrees/cortex-supabase-runtime-cron-v1`. The first contained only the remote-exact detached source plus regenerated `node_modules`/`.next`; the second contained an uncommitted independent duplicate implementation created by this task and superseded by the already-pushed, independently verified `b70153f` implementation. Neither contained secrets or user-authored unique work.
- The removed paths allocated 1,310,956 KiB at the final pre-cleanup scan (1,198,464 KiB dependencies, 104,064 KiB build output, and 8,428 KiB duplicate worktree source before overlap/accounting). Treat this as disposable coding-task recovery, not durable capacity.
- APFS physical free space was 38,252,154,880 bytes at 17:11:33 EDT before cleanup and 40,924,741,632 bytes at 17:12:18 EDT afterward. `df -k /System/Volumes/Data` increased from 37,356,036 KiB to 39,965,568 KiB available. The physical increase exceeded the final allocated scan, so do not attribute the difference to persistent savings; APFS/background reclamation contributed.
- Naomi explicitly set a **30 GB release-task floor** for this Cortex release. The final 40.9 GB APFS physical-free measurement was about 10.9 GB above that temporary release floor, while remaining about 9.1 GB below the canonical 50 GB standing reserve and 39.1 GB below the 80 GB maintenance target. No unrelated cleanup or cloud offload was performed.

## Coding-task cleanup on 2026-07-20 — Cortex Actions acceptance corrections

- Repository result: **PASS** for both Cortex correction branches. `git ls-remote` proved exact product head `d8d4432bae595ae6c1fbf971fea56a6ebae15ca1` on `origin/agent/acceptance-corrections-v1` (draft PR #36) and exact harness head `8ae32eaea8e3205678628c2d80be3db0a5b077b9` on `origin/agent/acceptance-receipt-ui-proof-v1` (draft PR #37). Both worktrees were clean before cleanup. The product lane passed 118 files / 846 tests, TypeScript, ESLint, zero-vulnerability npm audit, and a 120-route production build; the harness lane passed 2 files / 29 tests, TypeScript, and targeted ESLint.
- Removed only task-created disposable outputs after that proof: `node_modules` and `.next` from `/Users/naomiivie/cortex/.worktrees/cortex-acceptance-corrections-v1`, plus the temporary `node_modules` symlink from `/Users/naomiivie/cortex/.worktrees/cortex-acceptance-receipt-ui-proof-v1`. The pre-cleanup allocated scan was 1,300,040 KiB (1,196,056 KiB dependencies and 103,984 KiB build output); the symlink itself did not own another dependency copy. No source, secrets, sessions, provider state, or user data were removed. The release-progress dashboard dependencies remain active because its localhost server is running.
- APFS physical free space was 40,215,117,824 bytes at 18:26:08 EDT before cleanup and 40,818,774,016 bytes at 18:26:45 EDT afterward. `df -k /System/Volumes/Data` increased from 39,272,572 KiB to 39,771,368 KiB available. Treat the measured approximately 604 MB physical increase as disposable build/dependency recovery, not durable capacity; APFS allocation and background activity explain why it is smaller than the allocated directory scan.
- Naomi's explicit **30 GB release-task floor** remains the governing reserve for this Cortex release. The final 40.8 GB APFS physical-free measurement was about 10.8 GB above that temporary floor, while remaining about 9.2 GB below the canonical 50 GB standing reserve and 39.2 GB below the 80 GB maintenance target. No unrelated cleanup, cloud offload, provider mutation, or live release action occurred.

## Coding-task cleanup follow-up on 2026-07-20 — Cortex Actions proof hardening

- Repository result: **PASS** for both updated correction branches. Exact product head `17b86cc8f423a4e1e2ded91faf2a877e9c666752` is remotely present on `origin/agent/acceptance-corrections-v1` (draft PR #36), and exact harness head `a3308f79baa3baff03f6f0f14375f15e473303d9` is remotely present on `origin/agent/acceptance-receipt-ui-proof-v1` (draft PR #37). Both worktrees were clean and matched their upstreams. PR #36 passed 118 files / 846 tests, TypeScript, ESLint, audit 0, the 120-route production build, GitHub CI, Vercel, and independent clean-archive review. PR #37 passed focused tests, TypeScript, ESLint, and independent review; its CI audit failure is inherited from historical PR #8 and remains intentionally deferred until the harness is repinned to the final integrated SHA.
- Removed only regenerated disposable outputs after exact remote recoverability proof: about 1.1 GB `node_modules` and 102 MB `.next` from `/Users/naomiivie/cortex/.worktrees/cortex-acceptance-corrections-v1`, plus the temporary `node_modules` symlink from `/Users/naomiivie/cortex/.worktrees/cortex-acceptance-receipt-ui-proof-v1`. No source, secrets, sessions, provider state, database state, or user data were removed. The localhost release-progress dashboard dependencies remain active while its server is running.
- This follow-up continues from the prior ledger's 40,818,774,016-byte post-cleanup baseline. After the temporary verification install/build and its removal, APFS physical free measured 42,348,896,256 bytes; `df -k /System/Volumes/Data` reported 41,359,940 KiB available. Treat the reclaimed dependency/build space as refillable disposable capacity, not durable savings; APFS/background reclamation also contributed to the higher final physical measurement.
- Naomi's explicit **30 GB release-task floor** remains satisfied by about 12.3 GB. The canonical 50 GB standing reserve and 80 GB maintenance target remain unmet; no unrelated cleanup, cloud offload, provider mutation, live acceptance, merge, or deployment occurred.

## Coding-task cleanup on 2026-07-20 — Cortex protected staging readiness

- Repository result: **PASS** for `/Users/naomiivie/cortex/.worktrees/cortex-protected-staging-readiness-v1`. Exact head `a188553abc147ce0f26cad7eb7b1bb594ac3f143` is present on `origin/agent/protected-staging-readiness-v1` and draft PR #40. The worktree was clean and matched its upstream after 97 acceptance tests, TypeScript no-emit, focused ESLint, and a zero-vulnerability npm audit.
- Removed only the task-created disposable `node_modules` symlink in that worktree after remote recoverability proof. It pointed to the active final-integration worktree dependency tree and owned no dependency copy; the target and all source were preserved. No source, secrets, sessions, provider state, database state, auth state, or user data were removed.
- APFS physical free space was 41,125,732,352 bytes at 18:58:44 EDT before unlinking and 41,129,795,584 bytes at 18:58:54 EDT afterward. `df -k /System/Volumes/Data` increased from 40,161,820 KiB to 40,165,808 KiB available. The roughly 4 MB drift is background/APFS activity and is not claimed as recovery; persistent savings and refillable-cache savings are both 0.
- Naomi's explicit **30 GB release-task floor** remains satisfied by about 11.1 GB. The canonical 50 GB standing reserve and 80 GB maintenance target remain unmet. No unrelated cleanup, cloud offload, Vercel/Clerk/Supabase mutation, live acceptance, merge, alias, migration, provider action, or deployment occurred.

## Read-only measurement on 2026-07-20 — Cortex sealed-harness handoff

- At 20:56 EDT, `diskutil apfs list` reported **31,739,092,992 bytes (31.7 GB) APFS physical free**; `df -h /System/Volumes/Data` corroborated **30 GiB available**.
- Naomi's explicit **30 GB Cortex release-task floor** remains satisfied by about 1.7 GB, with limited headroom. The canonical 50 GB standing reserve and 80 GB maintenance target remain unmet.
- This was a read-only measurement used to keep the Cortex localhost release board truthful. No files, caches, dependencies, cloud data, secrets, sessions, provider state, database state, device settings, aliases, merge state, or deployment state were removed or mutated for storage.

## Read-only measurement on 2026-07-21 — Cortex STAGE-OPS-1 handoff

- At 10:07 EDT, `diskutil apfs list` reported **30,244,962,304 bytes (30.2 GB) APFS physical free**; `df -h /System/Volumes/Data` corroborated **28 GiB available**.
- Naomi's explicit **30 GB Cortex release-task floor** remains satisfied by only about 0.2 GB. The canonical 50 GB standing reserve and 80 GB maintenance target remain unmet. Do not begin a large dependency/browser install or disposable build until more headroom exists.
- This was a read-only measurement used to keep the Cortex localhost release board truthful. No files, caches, dependencies, cloud data, secrets, sessions, provider state, database state, device settings, aliases, merge state, or deployment state were removed or mutated for storage.

## Weekly audit watchdog on 2026-07-23 — current-week completion recovery

- No successful `weekly-mac-storage-audit` run for the current calendar week (Monday, July 20, 2026 through Thursday, July 23, 2026) was present in this ledger before this watchdog pass. The last fully compliant weekly watchdog success recorded here was Thursday, July 16, 2026, which is outside the current week. This run closes the gap.
- Start measurement at 12:20:48 EDT: `diskutil apfs list` reported **24,390,959,104 bytes (24.4 GB) APFS physical free** and `df -k /System/Volumes/Data` reported **23,819,892 KiB available**. Mounted simulator/runtime images on separate APFS containers were observed but excluded from claimed recovery per policy.
- Final measurement at 12:21:46 EDT after cleanup and a short APFS settle: `diskutil apfs list` reported **27,674,263,552 bytes (27.7 GB) APFS physical free** and `df -k /System/Volumes/Data` reported **27,025,840 KiB available**.
- Reserve/target status at the final measurement: the Mac remained **22.3 GB below** the 50 GB standing reserve and **52.3 GB below** the 80 GB maintenance target. This watchdog improved headroom but did not restore the reserve.
- Persistent savings: **0 GB**. Refillable/disposable dependency savings: the removed directories allocated **4,328,392 KiB** before deletion, while whole-volume APFS physical free space improved by about **3.28 GB** during the measured window. Treat the recovery as disposable dependency/build relief, not durable capacity.
- Files changed during this watchdog run:
  - Removed `/Users/naomiivie/cortex/.worktrees/cortex-final-integration-db2-fix/node_modules` after proving a clean worktree, `origin/agent/final-integration-acceptance-active-fixtures` containment of exact head `f5203c71f691e7b1c7b0454d2dcae3d5cd9cbe92`, and no open files in the directory.
  - Removed `/Users/naomiivie/cortex/.worktrees/cortex-final-union-proof/node_modules` after proving a clean worktree, `origin/agent/final-candidate-union-v1` containment of exact head `279b414649a8dcfd35e81bf5a1dde550f8310849`, and no open files in the directory.
  - Removed `/Users/naomiivie/cortex/.worktrees/cortex-acceptance-e09-audit/node_modules` after proving a clean worktree, `origin/agent/adm-zip-security-fix` containment of exact head `b546a91bfdb622826cf5a21b24d15375074da38c`, and no open files in the directory.
  - Removed `/Users/naomiivie/.codex/visualizations/2026/07/20/019f812b-557f-7493-8908-766ad681ebe6/cortex-release-progress/node_modules` after proving a clean worktree, `origin/main` containment of exact head `03250fa5b753cef10254437ad029a0cc9009c016`, and no open files in the directory.
  - Updated this maintenance ledger only; no personal documents, provider data, native AI sessions, app databases, secrets, or unique local repository state were deleted.
- Declined/preserved items:
  - Preserved `/Users/naomiivie/cortex/cortex-web/node_modules` because the repository still has a local modification in `app/onboarding/page.tsx`.
  - Preserved `/Users/naomiivie/bethel` because the repository contains multiple untracked and modified local work items, including `bethel-web/` and research/training assets.
  - Preserved `/Users/naomiivie/davinci-resolve-mcp` because it still has untracked local work (`SLASH-COMMANDS-CHEATSHEET.md`) and trails upstream.
  - Preserved `/Users/naomiivie/Documents/git-test` because the working directory still contains local-only `.DS_Store` state and did not require cleanup.
  - Preserved `/Users/naomiivie/.openclaw/workspace` because it is an active local workspace with no usable Git remote/upstream and many untracked files.
  - No cloud-offload actions, app uninstalls, simulator removals, cache purges outside the proved dependency trees, or user-data deletions were performed during this watchdog pass.

### Coding-task hygiene for repositories touched in the last 7 days

| Result | Repository | Remote / upstream | Notes |
| --- | --- | --- | --- |
| ACTIVE/KEPT | `/Users/naomiivie/.nvm` | `https://github.com/nvm-sh/nvm.git`; no branch upstream | Tool-managed dependency checkout; preserved. |
| ACTIVE/KEPT | `/Users/naomiivie/.openclaw/workspace` | no usable git remote/upstream | Active local workspace with untracked files and no safe recoverability proof; preserved. |
| PASS | `/Users/naomiivie/.codex/visualizations/2026/07/20/019f812b-557f-7493-8908-766ad681ebe6/cortex-release-progress` | `origin/main`; `https://github.com/thegirwhocodes/cortex-release-progress.git` | Clean worktree; not ahead of origin; disposable `node_modules` removed after remote containment proof. |
| PASS | `/Users/naomiivie/Class on Time` | `origin/main`; `https://github.com/thegirwhocodes/Go.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Dactyl-Final` | `origin/main`; `https://github.com/thegirwhocodes/Dactyl-Final.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Education for Equality/curriculum-app` | `origin/feature/advisor-board-notion`; `https://github.com/thegirwhocodes/Education-for-Equality.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Education for Equality/sabi-server` | `origin/main`; `https://github.com/thegirwhocodes/sabi-server.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Index` | `origin/main`; `https://github.com/thegirwhocodes/Index.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Rings` | `origin/main`; `https://github.com/thegirwhocodes/Rings.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/Social Media/Ed.it` | `origin/main`; `https://github.com/thegirwhocodes/edit.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/ai-context` | `origin/main`; `https://github.com/thegirwhocodes/ai-context.git` | This watchdog updates the ledger and will commit/push the result to `origin/main`. |
| PASS | `/Users/naomiivie/bin/downloads-cleaner` | `origin/main`; `https://github.com/thegirwhocodes/downloads-cleaner.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/cortex/runpod-lora-worker` | `origin/main`; `https://github.com/thegirwhocodes/cortex-runpod-lora-worker.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/cortex/voice-email` | `origin/main`; `https://github.com/thegirwhocodes/email.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/devsync` | `origin/main`; `https://github.com/thegirwhocodes/devsync.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/e4e-knowledge` | `origin/main`; `https://github.com/thegirwhocodes/e4e-knowledge.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/kai` | `origin/main`; `https://github.com/thegirwhocodes/kai.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/naomi-home` | `origin/main`; `https://github.com/thegirwhocodes/naomi-home.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/portfolio` | `origin/main`; `https://github.com/thegirwhocodes/portfolio.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/sage` | `origin/main`; `https://github.com/thegirwhocodes/sage.git` | Clean working tree; not ahead of origin. |
| PASS | `/Users/naomiivie/thegirwhocodes` | `origin/main`; `https://github.com/thegirwhocodes/thegirwhocodes.git` | Clean working tree; not ahead of origin. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/Documents/git-test` | remote/upstream inspection previously showed `origin/editreadme-NI`; current working directory still contains local-only `.DS_Store` state | Preserved; no cleanup performed. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/bethel` | `origin/backend-foundation`; `https://github.com/thegirwhocodes/bethel.git` | Modified `.gitignore` plus multiple untracked work items; preserved. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/cortex/cortex-web` | `origin/main`; `https://github.com/thegirwhocodes/cortex-web.git` | Modified `app/onboarding/page.tsx`; large local `node_modules` preserved until the coding task is finished and pushed. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/davinci-resolve-mcp` | `origin/main`; `https://github.com/samuelgursky/davinci-resolve-mcp.git` | Untracked `SLASH-COMMANDS-CHEATSHEET.md`; branch also trails upstream by 4 commits; preserved. |

- Repositories marked `NEEDS PUSH`: **none** during this watchdog pass.
- Weekly audit watchdog status: **completed successfully on Thursday, July 23, 2026**, because this run now records the current-week APFS start/end measurements, before/after cleanup report, durable-versus-refillable distinction, reserve/target status, and the required 7-day repository hygiene table.

## Coding-task cleanup on 2026-07-27 — Sage weekly dependency security review

- Repository result: **PASS** for `/Users/naomiivie/sage`. `git pull --ff-only` reported `Already up to date.`, the working tree stayed clean throughout the review, and no source changes were required because the security report already matched the tracked state. No commit or push was needed.
- Required validation completed against the lockfile dependency set after a temporary `npm ci`: `npm run ops:security-review -- --write`, `npm run ops:security-review:json`, `npm test`, and `npm run typecheck` all succeeded. The generated review reported **0 vulnerabilities** across all severities. Outdated direct dependencies remained limited to `@sentry/node` (`10.59.0 -> 10.68.0`), `stripe` (`22.2.2 -> 22.3.2`), dev-only `@types/node` (`22.19.20 -> 22.20.1`), and `tsx` (`4.22.4 -> 4.23.1`); no automatic upgrades were applied because Phase 0 stability remains the priority.
- Removed only the disposable `/Users/naomiivie/sage/node_modules` directory after the checks completed, `lsof +D node_modules` returned no open files, and the repository had already been proved recoverable from `origin/main`. The pre-cleanup allocated scan was **116,308 KiB**. No source files, secrets, reports, customer data, native AI session history, or ignored irreplaceable work were removed.
- APFS physical free space measured **46,087,684,096 bytes (46.1 GB)** at 16:59:35 EDT before cleanup and **47,241,469,952 bytes (47.2 GB)** at 17:00:01 EDT afterward. `df -k /System/Volumes/Data` increased from **45,007,504 KiB** available to **46,134,252 KiB** available. Treat the roughly **1.15 GB** increase as disposable dependency recovery, not durable capacity.
- Reserve status: the final **47.2 GB** APFS physical-free measurement remains about **2.8 GB below** the 50 GB standing reserve and about **32.8 GB below** the 80 GB maintenance target. No unrelated cleanup, cloud-offload action, or app-data deletion occurred during this coding task.

## Weekly audit watchdog on 2026-07-27 — current-week completion recovery

- No successful `weekly-mac-storage-audit` run for the current calendar week (**Monday, July 27, 2026 through Sunday, August 2, 2026**) was present in this ledger before this watchdog pass. The most recent compliant weekly entry here was Thursday, July 23, 2026, which is outside the current week. This run closes the gap.
- Exact measured cleanup batch:
  - Start measurement at **17:02:53 EDT**: `diskutil apfs list` reported **47,663,378,432 bytes (47.7 GB) APFS physical free** and `df -k /System/Volumes/Data` reported **46,545,300 KiB available**.
  - Final measurement at **17:03:28 EDT** after cleanup and a short APFS settle: `diskutil apfs list` reported **52,090,494,976 bytes (52.1 GB) APFS physical free** and `df -k /System/Volumes/Data` reported **50,869,624 KiB available**.
  - Mounted simulator/runtime images on separate APFS containers were observed but excluded from claimed recovery per policy.
- Reserve/target status at the final measurement: the Mac finished **2.1 GB above** the 50 GB standing reserve and **27.9 GB below** the 80 GB maintenance target.
- Persistent durable savings: **0 GB**. Refillable/disposable savings only:
  - Earlier in this watchdog run, after exact remote-containment proof and `lsof +D` checks, I removed clean/pushed repo artifacts from `/Users/naomiivie/design-portfolio` (`node_modules` and `.next`, **471,656 KiB**) and `/Users/naomiivie/kai` (`node_modules` and `.next`, **513,812 KiB**). Background APFS activity more than offset that early batch, so I do **not** attribute any physical free-space increase to it.
  - In the exact measured batch above, I removed only idle refillable caches: `/Users/naomiivie/.npm` (**2,107,364 KiB**), `/Users/naomiivie/.cache` (**1,584,828 KiB**, almost entirely `codex-runtimes`), `/Users/naomiivie/Library/Caches/ms-playwright` (**551,424 KiB**), and `/Users/naomiivie/Library/Caches/node-gyp` (**65,356 KiB**).
  - Total removed allocated bytes across the full watchdog run: **5,294,440 KiB**. Whole-volume APFS physical free space increased by about **4.43 GB** across the measured cache batch and by about **2.84 GB** from the run's first observed whole-volume measurement to the final measurement. Treat all reclaimed space as refillable/disposable relief, not durable capacity.
- Files changed during this watchdog run:
  - Removed `/Users/naomiivie/design-portfolio/node_modules` and `/Users/naomiivie/design-portfolio/.next` only after proving clean `origin/main` containment of exact head `0ff54181d767ad5f364007731ccb9f82216e8497` at `https://github.com/thegirwhocodes/design-portfolio.git` and confirming no open files in those paths.
  - Removed `/Users/naomiivie/kai/node_modules` and `/Users/naomiivie/kai/.next` only after proving clean `origin/main` containment of exact head `c842652ec1346712cbadb032e8edcbdb777064fe` at `https://github.com/thegirwhocodes/kai.git` and confirming no open files in those paths.
  - Removed `/Users/naomiivie/.npm`, `/Users/naomiivie/.cache`, `/Users/naomiivie/Library/Caches/ms-playwright`, and `/Users/naomiivie/Library/Caches/node-gyp` only after confirming they were idle cache/runtime directories with no open files. No source, secrets, app databases, native AI session history, personal documents, or cloud-provider indexes were removed.
  - Updated this maintenance ledger only; no app uninstalls, cloud-offload actions, provider mutations, mounted-image removals, or personal-data deletions were performed.
- Declined/preserved items:
  - Preserved `/Users/naomiivie/cortex/cortex-web/node_modules` because `/Users/naomiivie/cortex/cortex-web` still contains unique local work (`shot.mjs`) and therefore does not meet the recoverability bar for dependency cleanup.
  - Preserved `/Users/naomiivie/bethel` because the repository contains modified and untracked local work, including `bethel-web/`, research assets, and tests/training directories.
  - Preserved `/Users/naomiivie/davinci-resolve-mcp` because it still has untracked local work (`SLASH-COMMANDS-CHEATSHEET.md`) and trails upstream by four commits.
  - Preserved `/Users/naomiivie/.openclaw/workspace` because it has no usable Git remote/upstream and contains active local-only files.
  - Left `~/Library/Caches/Codex`, `~/Library/Caches/com.openai.codex`, Spark caches, Spotify caches, and Claude ShipIt staging untouched because they were either actively open in running apps or explicitly deferred by policy/tradeoff.
  - No cloud placeholders, Voice Memos data, Photos data, Messages data, credentials, native AI sessions, `/System` assets, `/private/var/db`, or `/private/var/vm` contents were touched.

### Coding-task hygiene for repositories touched in the last 7 days

| Result | Repository | Remote / upstream | Notes |
| --- | --- | --- | --- |
| ACTIVE/KEPT | `/Users/naomiivie/.codex/.tmp/plugins` | no usable git remote/upstream | Local plugin scratch checkout with no remote/upstream; preserved. |
| ACTIVE/KEPT | `/Users/naomiivie/.nvm` | `https://github.com/nvm-sh/nvm.git`; detached HEAD; no branch upstream | Tool-managed dependency checkout; preserved. |
| CLEANED | `/Users/naomiivie/design-portfolio` | `origin/main`; `https://github.com/thegirwhocodes/design-portfolio.git` | Clean worktree; exact head matched remote; removed `node_modules` and `.next`. |
| PASS | `/Users/naomiivie/.codex/visualizations/2026/07/20/019f812b-557f-7493-8908-766ad681ebe6/cortex-release-progress` | `origin/main`; `https://github.com/thegirwhocodes/cortex-release-progress.git` | Clean worktree; not ahead of origin. Small `dist`/`build` remain and were not needed for reserve recovery. |
| PASS | `/Users/naomiivie/Class on Time` | `origin/main`; `https://github.com/thegirwhocodes/Go.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/Dactyl-Final` | `origin/main`; `https://github.com/thegirwhocodes/Dactyl-Final.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/Education for Equality/curriculum-app` | `origin/main`; `https://github.com/thegirwhocodes/Education-for-Equality.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/Education for Equality/sabi-server` | `origin/main`; `https://github.com/thegirwhocodes/sabi-server.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/Index` | `origin/main`; `https://github.com/thegirwhocodes/Index.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/Rings` | `origin/main`; `https://github.com/thegirwhocodes/Rings.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/Social Media/Ed.it` | `origin/main`; `https://github.com/thegirwhocodes/edit.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/ai-context` | `origin/main`; `https://github.com/thegirwhocodes/ai-context.git` | This watchdog updates the ledger; the same pass commits and pushes the result to `origin/main`. |
| PASS | `/Users/naomiivie/bin/downloads-cleaner` | `origin/main`; `https://github.com/thegirwhocodes/downloads-cleaner.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/cortex/runpod-lora-worker` | `origin/main`; `https://github.com/thegirwhocodes/cortex-runpod-lora-worker.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/cortex/voice-email` | `origin/main`; `https://github.com/thegirwhocodes/email.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/devsync` | `origin/main`; `https://github.com/thegirwhocodes/devsync.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/e4e-knowledge` | `origin/main`; `https://github.com/thegirwhocodes/e4e-knowledge.git` | Clean worktree; not ahead of origin. |
| CLEANED | `/Users/naomiivie/kai` | `origin/main`; `https://github.com/thegirwhocodes/kai.git` | Clean worktree; exact head matched remote; removed `node_modules` and `.next`. |
| PASS | `/Users/naomiivie/naomi-home` | `origin/main`; `https://github.com/thegirwhocodes/naomi-home.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/portfolio` | `origin/main`; `https://github.com/thegirwhocodes/portfolio.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/sage` | `origin/main`; `https://github.com/thegirwhocodes/sage.git` | Clean worktree; not ahead of origin. |
| PASS | `/Users/naomiivie/thegirwhocodes` | `origin/main`; `https://github.com/thegirwhocodes/thegirwhocodes.git` | Clean worktree; not ahead of origin. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/.openclaw/workspace` | no usable git remote/upstream | Many untracked local files; preserved. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/bethel` | `origin/backend-foundation`; `https://github.com/thegirwhocodes/bethel.git` | Modified `.gitignore` plus multiple untracked work items; preserved. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/cortex/cortex-web` | `origin/main`; `https://github.com/thegirwhocodes/cortex-web.git` | Untracked `shot.mjs`; large local `node_modules` preserved until the coding task is finished and pushed. |
| UNIQUE LOCAL WORK | `/Users/naomiivie/davinci-resolve-mcp` | `origin/main`; `https://github.com/samuelgursky/davinci-resolve-mcp.git` | Untracked `SLASH-COMMANDS-CHEATSHEET.md`; branch also trails upstream by 4 commits; preserved. |

- Repositories marked `NEEDS PUSH`: **none** during this watchdog pass.
- Weekly audit watchdog status: **completed successfully on Monday, July 27, 2026**, because this run now records the current-week APFS start/end measurements, a before/after cleanup report, the durable-versus-refillable distinction, explicit reserve/target status, and the required 7-day repository hygiene table.

## Coding-task cleanup on 2026-07-27 — Cortex end-to-end quality and polish

- Repository result: **PASS** for `/Users/naomiivie/cortex/.worktrees/hour-quality`. Exact head `7d9daa3a28828c54d2e52fcefdc63b6f3da9c1b5` is present on `origin/agent/hour-quality` and draft PR #47. The worktree was clean and matched its upstream before and after cleanup. The final head includes separate commit `7d9daa3` repairing the inherited realtor-page Next lint failure after remote CI exposed it.
- No duplicate dependency install was created. Validation reused `/Users/naomiivie/cortex/cortex-web/node_modules` through a task-created symlink. After exact remote recoverability proof, removed only that zero-allocation symlink and the task-created `.next` output, which allocated **80 KiB**. No source, secrets, auth state, native AI sessions, provider/database state, personal data, or shared dependencies were removed.
- Start measurement at **19:04:50 EDT**: `diskutil apfs list` reported **36,410,318,848 bytes (36.4 GB) APFS physical free** and `df -k /System/Volumes/Data` reported **35,557,988 KiB available**.
- Final measurement at **19:05:41 EDT**: `diskutil apfs list` reported **36,408,844,288 bytes (36.4 GB) APFS physical free** and `df -k /System/Volumes/Data` reported **35,555,680 KiB available**. The small downward drift is background APFS/VM activity and is not attributed to the 80 KiB artifact cleanup.
- Persistent savings: **0 GB**. Refillable/disposable relief: **80 KiB allocated build output plus a zero-allocation dependency symlink**. The canonical 50 GB reserve remains unmet by about **13.6 GB**, the 80 GB target remains unmet by about **43.6 GB**, and the temporary 30 GB Cortex floor remains satisfied by about **6.4 GB**.
- Preserved the shared checkout dependency tree because `/Users/naomiivie/cortex/cortex-web` still contains unique local work (`shot.mjs`) and other active Cortex agents reuse those dependencies. No unrelated cleanup, cache purge, cloud offload, provider mutation, merge, or deployment occurred.

## Coding-task cleanup on 2026-07-27 — Cortex onboarding and activation

- Repository result: **PASS** for `/Users/naomiivie/cortex/.worktrees/hour-onboarding`. Exact head `9cc84271c2f313483c2063b41910f761d8e62b77` is present on `origin/agent/hour-onboarding` and draft PR #46. The worktree is clean and matches its upstream. Validation passed 3 focused test files / 16 tests, TypeScript no-emit, focused ESLint, and `git diff --check`; no dependency install or full duplicate build was run.
- Removed only task-created disposable artifacts after exact remote recoverability proof: the 47-byte `/Users/naomiivie/cortex/.worktrees/hour-onboarding/node_modules` symlink, which pointed to the preserved shared Cortex dependency tree, and the 660 KiB `tsconfig.tsbuildinfo` cache. The task created no `.next`, build, dist, coverage, or duplicated dependency directory. No source, secrets, sessions, provider state, database state, auth state, personal data, or user-owned artifacts were removed.
- APFS physical free space measured **36,406,894,592 bytes (36.4 GB)** at 19:04:17 EDT before cleanup and **36,408,864,768 bytes (36.4 GB)** at 19:04:34 EDT afterward. `df -k /System/Volumes/Data` increased from **35,553,576 KiB** available to **35,555,636 KiB** available. The roughly 2 MB drift exceeds the task artifact allocation and is not claimed as recovered capacity; persistent savings are 0, and the removed TypeScript cache was disposable/refillable.
- Reserve status: the final 36.4 GB APFS physical-free measurement is about **13.6 GB below** the canonical 50 GB standing reserve and **43.6 GB below** the 80 GB target, while remaining about **6.4 GB above** Naomi's temporary 30 GB Cortex floor. No unrelated cleanup, cloud offload, provider mutation, live deployment, merge, or application-data deletion occurred.
- Preserved `/Users/naomiivie/cortex/cortex-web/node_modules` because it is the shared dependency tree, other agent checks may still use it, and the shared checkout contains user-owned untracked `shot.mjs`. Only this task's symlink to that tree was removed.

## Coding-task cleanup on 2026-07-27 — Cortex beta launch and tester acquisition

- Repository result: **PASS** for `/Users/naomiivie/cortex/.worktrees/hour-beta-launch`. Exact head `f25fe9187faaf68e907eb92db4ea9a954ca5fa36` is present on `origin/agent/hour-beta-launch` and draft PR #48. The worktree is clean and matches its upstream. Targeted validation passed the five beta-tool tests, syntax checks, focused ESLint, GitHub issue-form YAML parsing, Markdown link checks, `git diff --check`, secret scanning, and the protected-scope guard. No dependency install or full duplicate build was run; the Vercel preview passed remotely.
- No task-created `node_modules`, `.next`, `build`, `dist`, or `coverage` directory existed in the isolated beta worktree after recoverability proof, so there was nothing disposable to remove. Persistent savings: **0 GB**. Refillable/disposable savings: **0 GB**. No source, secrets, sessions, provider/database state, auth state, personal data, or user-owned artifacts were removed.
- Naomi reported **37.1 GB APFS physical free** when assigning the storage constraint. The exact end measurement at **19:10:21 EDT** reported **36,277,051,392 bytes (36.3 GB) APFS physical free** and `df -k /System/Volumes/Data` reported **35,426,792 KiB available**. Because this task created no disposable dependency/build tree, the intervening decline is treated as background APFS/VM activity and no capacity recovery is claimed.
- Reserve status: the final 36.3 GB APFS physical-free measurement is about **13.7 GB below** the canonical 50 GB standing reserve and **43.7 GB below** the 80 GB target, while remaining about **6.3 GB above** Naomi's temporary 30 GB Cortex floor.
- Preserved the pre-existing shared `/Users/naomiivie/cortex/cortex-web/node_modules` tree because it was not created by this task, other active Cortex work may reuse it, and the shared checkout contains user-owned untracked `shot.mjs`. No unrelated cleanup, cache purge, cloud offload, provider mutation, live deployment, merge, outreach, or application-data deletion occurred.
