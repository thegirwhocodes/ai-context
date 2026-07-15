---
name: Read docs/API specs upfront, avoid trial-and-error iteration
description: Prefer 5 min of reading docs over 20 min of blind iteration. Look up Vercel/Stripe/Supabase/GitHub API surfaces before running commands that might fail.
type: feedback
originSessionId: a8c172f1-a7d4-4624-8ac2-b31c78a6f870
---
When working with a third-party API or platform setting, read the relevant docs first instead of iterating blindly. Each failed command costs more time than reading the spec.

**Why:** Naomi explicitly said: *"work much faster - maybe read all the docs before working."* During the Vercel deploy setup we burned several round-trips: tried `vercel link --yes` (failed because of directory name), set `rootDirectory=apps/server` (broke `--workspace` build), un-set it again — each of which she had to wait through. Reading Vercel monorepo docs first would've saved all of those.

**How to apply:**
- Before any non-trivial integration step, use `WebFetch` against the official docs URL (or invoke the matching skill like `vercel:nextjs`, `stripe-best-practices`, `supabase`) and confirm the exact shape, flags, required headers, ordering of operations, etc.
- For Vercel monorepos specifically: with framework explicitly set via API + `vercel.json` defining `buildCommand`/`installCommand`/`outputDirectory`, the cleanest is Root Directory = repo root and let the workspace-aware build command handle the rest. Don't set rootDirectory to the subdir unless commands are also rewritten.
- Skill triggers exist for a reason: invoke them at the start of a task, not as recovery.
- If you do hit a failure: don't blindly retry — read the actual error, understand it, then form one specific hypothesis before issuing the next command.

This is a general taste preference: she values "one careful try" over "fast loop of small tries that surface to her as multiple failures."
