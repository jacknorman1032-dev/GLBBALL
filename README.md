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
- `site-build/audit_schedules.py` — schedule check: `python3 -I audit_schedules.py ../site/index.html [school-id] [--season 1975-76] [--out audit_report.md]`. Flags odd regular-season counts, league opponents played only once, league regulars missing from a season, tournament runs that don't end in a loss, long mid-season gaps, and games or scores that don't match another school's log. Run it after every new batch of schedules; the latest output is `site-build/audit_report.md`.

To publish changes: patch `site/index.html` (or rebuild), then republish it to the existing artifact URL.

Note (Nov 13, 2026): `site/index.html` starts with the publish service's wrapper (`<!doctype html>...<style>...</style></head><body>`). The service rebuilds that wrapper on every publish, so anything placed in its first `<style>` is lost. Patch scripts must add CSS to the page's own stylesheet (the `</style>` after `/* Layout: a gym`); patch_mobile_seasons.py, patch_records_cards.py and patch_opponents.py were fixed to do that.
