---
name: Visual aesthetic for Class on Time
description: Naomi's reference screenshots for the Mapbox look — illustrated 3D Standard style with dusk lighting, low-poly cartoon trees
type: feedback
originSessionId: a8c172f1-a7d4-4624-8ac2-b31c78a6f870
---
She loves the **Mapbox Standard 3D** style with the illustrated/cartoon look (low-poly trees, soft pastel shadows, stylized road textures — the kind shown in the Mapbox 3D Live Navigation marketing videos).

**Specifically:** the German autobahn / Munich Petuelring screenshots, and the SF Van Ness Ave dark version. Both are the same **`mapbox://styles/mapbox/standard`** engine with different config — the cartoon look is `lightPreset: "dusk"` + `show3dObjects: true`; the SF dark one is `lightPreset: "night"`.

**Why:** She explicitly described the desired feel earlier as "cute, child-like, sprite-based, Pokemon Go meets Uber, like a kids' app" — and these reference shots are exactly that. **Don't ship a flat / muted / "adult Uber" map** for this app — that gets the project wrong.

**How to apply:**
- Default to the cartoon dusk look. Offer night as a stretch toggle for late classes.
- 3D pitch ~55° (not 0° / top-down).
- Zoom ~17 when showing user position; zoom out when showing route.
- Sprite avatar on top of the puck — rendering as an emoji is fine for MVP, but upgrade to a Lottie/Skia walking animation as polish.
- Use `@rnmapbox/maps` (NOT `react-native-maps` — Apple Maps cannot be styled this way). Requires EAS dev client build, which is OK because she has Apple Developer enrollment.

**Concrete reference apps to steal from (see `docs/UI_REFERENCES.md`):**
- **Pikmin Bloom** for the map (flower trail behind avatar, golden-hour bake)
- **Pokemon Go** for the camera angle (rear 3/4) + stationary fidget loop
- **Citymapper** for the "leave now" Live Activity countdown
- **Sunsama** for the morning roll-call screen layout (single column, big rows)
- **Day One** for the voice-record UI (waveform + auto-stop + live transcript)
- **Cold Turkey** for the "you're late, charging $100" lockup screen (brutalist black, no dismiss)
- **Habitica** for the depleting HP-bar metaphor on today's stake
