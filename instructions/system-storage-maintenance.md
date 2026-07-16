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

Voice Memos is a special case: iCloud sync keeps recordings consistent across devices but macOS does not provide a supported per-recording cloud-only mode. To reclaim its local space durably, export recordings to a verified OneDrive archive, make that archive cloud-only, and only then delete the recordings from Voice Memos. Deleting in Voice Memos also deletes the iCloud-synced originals, so obtain explicit confirmation at that final content-deletion step.

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

Latest completed whole-volume measurement during the audit: approximately **66.8 GB APFS physical free** at 15:51 EDT, leaving about **13.2 GB** to reach the 80 GB floor. Re-measure before relying on this number.

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
| UNIQUE LOCAL WORK | `/Users/naomiivie/ai-context` | `origin/main`; `https://github.com/thegirwhocodes/ai-context.git` | Local automation/session record updates plus this ledger change; commit and push required before cleanup. |
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
- Voice Memos, about 4.87 GB: iCloud sync is on, but recordings remain local. Do not delete; use the archive/export protocol above if Naomi approves removing the iCloud originals.
- Downloads, about 5.5 GB: mostly class recordings, PDFs, photos, media, and app/project folders. Archive important material to OneDrive, verify, evict, then remove local originals. Exclude secrets and source that is not otherwise recoverable.
- Pictures, about 5.14 GB: Photos Library about 3.72 GB and Photo Booth Library about 1.41 GB. Treat Photos as an active database; use Photos' supported iCloud optimization, not manual package deletion. Photo Booth media can be archived after verification.
- Music, about 4.77 GB: GarageBand projects about 3.15 GB, Music library about 1.31 GB, plus local recordings. These are user creations, not cache. Archive projects/media before any deletion.
- Movies/CapCut, about 1.68 GB: user video projects/exports. Archive completed projects and exports before removing local copies. Do not assume CapCut data is disposable.
- User-installed Docker app, about 2.23 GB, plus any Docker data: uninstall only if Naomi confirms it is unused and there are no unique containers/volumes.
- OneNote app, about 1.37 GB: candidate for uninstall only after the notebook sync gate above passes. Notes must persist.
- Developer dependencies/build outputs: at least several GB across Cortex worktrees, E4E, Downloads app projects, `.next`, `node_modules`, Rust `target`, and standalone Python environments. They are regenerable and safe after Git/GitHub verification, but do not count them as guaranteed persistent free space if active work will immediately recreate them.
- Homebrew occupies about 6.1 GB; its normal cleanup dry run found only about 125 MB. Do not remove required formulae solely for size. Audit unused top-level formulae before uninstalling them.
- `/private/var` is mostly system state, diagnostics, caches, and temporary data. It is not a durable 26 GB solution. Never remove live database or swap contents manually.

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
