---
name: project_cortex_design_system
description: "cortex-web UI design system — \"Quiet Intelligence\" — tokens, fonts, ambient signature, conventions"
metadata: 
  node_type: memory
  type: project
  originSessionId: e7c30dbb-f6d3-4ebc-abda-711a816710f2
---

cortex-web got a major UI redesign — codename **"Quiet Intelligence"** — session e7c30dbb (2026-06-30). Keeps Naomi's dark / calm / one-thing-at-a-time DNA but lifts craft to Linear/Anthropic tier. Built so the WHOLE app inherits it (token names were preserved, only values changed).

**Design tokens** live in `cortex-web/app/globals.css` under Tailwind v4 `@theme`. To change the look, change tokens here — do NOT hardcode colors in components.
- Surfaces: warm near-black `--color-bg #08080a` → `--color-bg-elevated #16161a` (layered depth, not flat).
- Text: warm cream `--color-text #f4f1ea` (not cold white).
- THE accent = warm **gold** `--color-accent #e3a857` (dropped the old generic-AI violet `#8B5CF6`). One accent only — used for active/focus/CTA. Dark text on gold = `--color-on-accent`. To pivot the whole app's accent, change this ONE token.
- Semantic colors are hue-shifted off the accent (warm sage success, clay error), never pure.
- Named motion curves: `--ease-decel/-accel/-standard/-spring`.

**Typography** (loaded in `app/layout.tsx` via next/font/google):
- `--font-geist` (Geist) = all UI chrome.
- `--font-instrument-serif` (Instrument Serif) = the assistant's "literate voice" — display headings + AI chat responses. Use the `.serif` class. This is the "two voices on one surface" Granola pattern.
- `--font-geist-mono` = data/code.

**Signature visual** = the ambient aurora: `components/layout/ambient.tsx` (`<Ambient/>`, CSS class `.cortex-ambient`). One slow breathing warm field behind a surface — the ONLY moving decorative element. Respects prefers-reduced-motion. Used in dashboard layout + landing.

**Reusable primitives** in `cortex-web/components/ui/`: `Button`/`ButtonLink` (button.tsx), `Card`/`CardLabel` (card.tsx), `Badge` (badge.tsx). Prefer these over ad-hoc styled divs.

**Redesigned surfaces:** globals.css, layout.tsx (fonts + Clerk theming), landing `app/page.tsx`, sidebar (grouped nav Think/Act/Know + gold active bar), dashboard layout (+ambient), stats-bar (live status strip), chat page (two-voice serif assistant + glass composer). Other dashboard pages inherit the palette/fonts automatically and still work — they're candidates for hands-on polish next.

**Status:** typecheck clean, **shipped to production** 2026-06-30 — live at https://cortex-web-one.vercel.app (200). Naomi OK'd promoting after I confirmed concurrent agents had gone quiet (~12 min) + full tree built clean. Inner pages (spheres/actions/integrations/memory/profile) also got hands-on polish (PageHeader/Button/Card/Badge primitives). cortex root is NOT a git repo.

**Gotcha — git vs raw upload (cost Naomi a scare 2026-06-30):** `cortex-web` IS its own git repo (`github.com/thegirwhocodes/cortex-web`, branch `main`) wired to Vercel. A Vercel "Redeploy" rebuilds from the LAST GIT COMMIT. `vercel deploy` from CLI uploads local *uncommitted* files — so UI shipped that way VANISHES on any git-triggered redeploy. ALWAYS commit + `git push origin main` your work (push auto-deploys prod from git). The redesign is now committed (2b0ad91) + pushed. Other agents commit their backend work to the same repo, so only your own files are typically dirty — safe to `git add` just yours.

**Gotcha for future deploys:** Vercel **Preview**-scoped env vars are MISSING the core keys (CLERK_SECRET_KEY, NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, ANTHROPIC_API_KEY, SUPABASE_*, TOKEN_ENCRYPTION_KEY are Production+Development only). So **preview deploys 500 on every page** (Clerk middleware throws). To use preview URLs, copy those keys into the Preview scope first. Production is fine. See [[project_cortex_status]] [[project_cortex_tech]] [[user_naomi]].

**Current visual direction after Naomi feedback:** sidebar navigation labels are back to clean Geist sans while the Cortex wordmark and assistant/display voice keep Instrument Serif; this was the de-"game menu" move. The gold ambient glow is restored at medium strength, not the very dim pass and not the original heavy pass. Preserve this balance unless Naomi explicitly asks for "more gold" or a heavier/fancier side pane. - 019f179c-85e8-74b1-bce9-023948aad650

**Logo decision after Naomi rejected the old mark:** retire the glowing dot/orb and teal-gold loop icon; Cortex now uses a restrained "Cortical Fold C" monogram: cream outer open C + warm-gold inner fold on dark, implemented as `components/brand/cortex-brand.tsx` and generated into `src-tauri/icons/*`. Preserve the serious personal-OS feel: no cute mascot, no bokeh/orb, no over-purple, no sci-fi/game logo. - 019f1b51-1449-7d92-9920-9e409363d63c / 019f1b53-00b4-7332-91a9-5ad2a4ef6fc2

**Logo update after Naomi still disliked the mark:** a Codex logo subagent replaced the "Cortical Fold C" with an abstract command-frame/aperture mark: four cream corner blocks around a single warm-gold vertical index line on dark. Source of truth is still `components/brand/cortex-brand.tsx` plus `scripts/generate-brand-assets.mjs`; generated Tauri icons in `src-tauri/icons/*` must be regenerated after any logo edit. Keep it serious and personal-OS: no orb, mascot, generic AI sparkle, purple gradient, or game icon. - 019f1572-44cf-7e12-8e4a-ab2fd29640fb
