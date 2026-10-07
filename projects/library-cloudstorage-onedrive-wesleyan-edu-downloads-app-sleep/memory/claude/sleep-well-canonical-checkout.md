---
name: sleep-well-canonical-checkout
description: "Sleep Well's working copy is ~/dev/sleep-well on local disk; the OneDrive checkout is dead and must not be read"
metadata:
  node_type: memory
  type: project
  originSessionId: 7ded354b-7e8f-4a5f-8a3c-8765a916a55d
  modified: 2026-08-15T20:32:49.238Z
---

The canonical Sleep Well working copy is **`~/dev/sleep-well`** on local disk. Multiple agent
sessions (Claude and Cursor) work in it concurrently, so expect uncommitted changes and unfamiliar
branches that belong to someone else.

The older checkout at `~/Library/CloudStorage/OneDrive-wesleyan.edu/Downloads/App/Sleep` is
**dead** as of 2026-08-15. OneDrive dehydrated its git objects, so `git` exits 128 or fails with
`mmap failed: Operation timed out` there. Do not build from it, and do not run `find`/`du`/`grep`
across it — walking a dehydrated tree forces OneDrive to re-download everything touched, which
burned ~13 GB of a nearly-full disk in one afternoon. See the storage ledger for details.

Note the session cwd may still *be* the OneDrive path even though the real repo is elsewhere;
`cd ~/dev/sleep-well` explicitly rather than trusting the working directory.

Related: [[sleep-well-ios-bundle-id]]
