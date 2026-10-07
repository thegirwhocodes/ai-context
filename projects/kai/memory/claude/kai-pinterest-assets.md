---
name: kai-pinterest-assets
description: "Naomi ships Pinterest-sourced background scenes in Kai despite the copyright risk — decided, don't re-raise"
metadata:
  node_type: memory
  type: project
  originSessionId: bfcc8fd6-7858-418f-9aeb-0bc28332b184
  modified: 2026-08-12
---

On 2026-08-12 Naomi downloaded 19 images from Pinterest and asked for them to be shipped as Kai's background themes. She was told plainly, before any of them were used, that they are other people's work, that `docs/BRAND_VISUAL_RESEARCH.md` had a standing rule against shipping pins as assets, and that publishing them in a public repo on a product she intends to charge for carries takedown and copyright exposure. She was offered a matched free-license set from Unsplash/Pexels as an alternative. **She chose to ship her own images anyway, and then explicitly said to forget the asset rule.**

That is her decision as the product owner. **Don't re-raise it, and don't quietly swap her images for stock ones.** The rule in `docs/BRAND_VISUAL_RESEARCH.md` has been struck through and annotated to record the override.

**Why it matters:** she picked these deliberately for their look, and re-litigating it wastes her time. The risk is real but it's hers to carry, and it's cheap to unwind — each scene is a single file under `public/backgrounds/` plus one `photo(...)` line in `src/lib/backgrounds.ts`, so honouring a takedown is a two-minute change.

**How to apply:** treat the shipped scenes as fixed unless she says otherwise. If she asks for more in the same style, the practical route is her picking them — Pinterest can't be scraped and the Bing workaround returns unusable and explicit content (see [[kai-theme-system]]).
