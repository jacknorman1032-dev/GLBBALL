# Greater Lansing Hoops

Data, build scripts and source material for the Greater Lansing high school basketball history site.
This repo replaced the claude.ai Project's file storage on Nov 3, 2026, when the Project ran out of room.

## Layout
- `site/index.html` — the live page exactly as published (with every patch applied). Logos and uniforms are published next to it from `site-build/logos/` and `site-build/uniforms/`.
- `site-build/` — `build.py` + `template.html` + `overrides.json` build the page; then the patches in `POST_BUILD_PATCHES.md` run in order. `README.md` there documents the build.
- `site-build/logos/*.png` — school logos (real PNGs; the Project kept them as `.png.b64`).
- `site-build/uniforms/*.svg` — uniform drawings (see `UNIFORMS.md`).
- `honors/` — BCAM all-state (`bcam_allstate.json`), all-conference (`all_conference.json`) and the Lansing State Journal Dream Team / all-area teams (`lsj_all_area.json`).
- `game-logs/` — parsed season-by-season game logs and corrections.
- `research/` — per-school research files.

To publish changes: patch `site/index.html` (or rebuild), then republish it to the existing artifact URL.
