---
name: kai-theme-system
description: "Kai's 35-theme system — portrait photos rendered blur-extended, per-theme measured scrim, and how to add a theme"
metadata:
  node_type: memory
  type: project
  originSessionId: bfcc8fd6-7858-418f-9aeb-0bc28332b184
  modified: 2026-08-12
---

Built 2026-08-12 to close the theme gap against Flocus. Everything lives in `src/lib/backgrounds.ts` (`THEMES`), rendered by the `Scene` component in `src/app/app/page.tsx` and styled in `globals.css`.

**35 themes in 5 categories** — 25 photo scenes (WebP, ~115KB average, 3.4MB total), 4 animated CSS ambient worlds, 6 static gradients. 19 of the photos are Naomi's own Pinterest picks; see [[kai-pinterest-assets]] for that decision.

**Shape matters more than resolution — learned the hard way.** Flocus ships **2160×1350 landscape** JPEGs (verified by reading their live page). Naomi's pins are **736×1300 portrait**. Filling a 2560px ultrawide from a portrait source means a 3.5× upscale *and* discarding ~74% of the picture; raising resolution does nothing, because the problem is the aspect ratio. I first shipped a blur-extend renderer (sharp portrait centred, blurred copy filling the sides) and Naomi rejected it on sight on her ultrawide — it read as a phone screenshot floating in mush.

**The fix was better source images**, not better CSS: 22 landscape scenes at 2560×1600 sourced from Unsplash, which lead every category, and one of them (`night-study`) is the default. Themes carry `portrait?: boolean`; only portrait ones respond to `settings.backgroundFit` ("fill" crops, "fit" blur-extends). Landscape always covers. **If you add photo themes, source them landscape at ≥2400px wide.**

**Sourcing that works** (verified): WebFetch `unsplash.com/s/photos/<query>?orientation=landscape` returns photo IDs; `curl -sIL unsplash.com/photos/<id>/download?force=true` gives the CDN URL in the Location header; then `<cdn>?w=2560&h=1600&fit=crop&crop=entropy&q=82` returns an exact landscape crop (~280KB). Plain curl on Unsplash *search* 401s — use WebFetch for the ID step.

**Picker uses thumbnails.** 47 full-size photos in a grid is 7MB; `public/backgrounds/thumbs/*.webp` at 420px is 480KB for the lot. `thumbFor(value)` resolves them.

**Scrim is measured, not guessed.** Each theme carries `scrim: soft | medium | strong`, derived from the mean luminance of the image's top third (where the clock sits) using PIL. The veil is a soft ellipse behind the centre column rather than a flat wash, so text gets contrast while the edges keep their colour — a flat wash drained the art. Verified by driving all 25 themes in Playwright and sampling pixels behind the *hidden* clock digits (hide them first, or you just measure white text): every theme lands 38–96 luma.

**Users bring their own** three ways: upload a file (data URL, capped at 2.5MB so localStorage doesn't get evicted), paste an image URL, or paste a YouTube link. Video is stored as `youtube:<id>` and rendered as a muted, looped, chrome-free iframe sized `max(100vw, 177.78vh)` — `object-fit` does nothing to an iframe.

**To add a photo theme:** drop `slug.webp` in `public/backgrounds/`, add one `photo("slug", "Name", category, scrim)` line. Measure the scrim rather than guessing.

**Sourcing more images:** Pinterest can't be scraped (JS-rendered search, 403 on their API and on CDN paths without a real hash). Unsplash's `unsplash.com/photos/<id>/download?force=true&w=2400` works if you have photo ids. **Bing image scraping was tried and abandoned** — `murl` extraction returns content wildly unrelated to the query, including pornography. Don't retry it. The reliable path is Naomi picking images herself.

**How to apply:** timer modes (`pomodoro | countdown | stopwatch`) live in `src/components/TimerModes.tsx`; countdown blocks are marked `standalone` so autopilot doesn't chain a break. Related: [[kai-status-aug2026]], [[kai-timing-model]].
