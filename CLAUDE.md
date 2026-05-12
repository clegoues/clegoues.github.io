# Notes for Claude

Project-specific guidance for working on this Jekyll site. The user's global Claude instructions (workflow, writing rules, style) still apply.

## What this site is

clairelegoues.com, built with Jekyll, originally Academic Pages template, heavily customized in May 2026. The deploy story is a GitHub Action on the `source` branch that builds and force-pushes `_site/` to `master`; GitHub Pages serves `master`. No `--safe`-mode Pages build, so all plugins (especially `jekyll-scholar`) work.

The design system is documented in `docs/superpowers/specs/2026-05-11-academic-site-modernization-design.md` — read that if doing visual work.

## Running it locally

Always pass the dev config overlay:

```bash
bundle exec jekyll serve \
  --config _config.yml,_config.dev.yml \
  --port 4040 --host 127.0.0.1 --livereload
```

Without `_config.dev.yml`, nav links render with the production URL (`https://www.clairelegoues.com/...`) and clicking them from the local preview jumps to the live site. This is unintuitive and wastes time.

`_config.yml` changes do not auto-reload. Restart the server.

## File map (where things live)

| Want to change | Edit |
|---|---|
| Homepage bio | `_pages/about.md` (body). Frontmatter has `homepage: true` which triggers extras. |
| Homepage news | `_data/news.yml` |
| Group block | `_includes/group-block.html` (content is hardcoded; short, changes rarely) |
| Top nav | `_data/navigation.yml` (`main:` list) |
| Footer secondary nav | `_data/navigation.yml` (`secondary:` list) |
| Sidebar (avatar, name, social links) | `_config.yml` `author:` block; markup in `_includes/author-profile.html` |
| Design tokens (colors, palette) | `_sass/_theme.scss` |
| Type sizes, base styles | `_sass/_base.scss`, `_sass/_variables.scss` |
| Sidebar styling | `_sass/_sidebar.scss` |
| Masthead / nav / theme-toggle styling | `_sass/_masthead.scss`, `_sass/_navigation.scss` |
| Theme-toggle markup / behavior | `_includes/theme-toggle.html`, `_includes/theme-init.html` |
| Publication bib rendering | `_layouts/bib_template.html` and `_sass/_archive.scss` (.refs-row, .reference, .refs-link, .abbrv) |
| Add a publication (lab-coauthored) | Add to the **lab repo**, not here. The weekly sync picks it up. See "Publications sync" below. |
| Add a publication (personal-only, no lab) | `_bibliography/references.bib` below the END AUTO-SYNCED REGION marker; drop PDF in `assets/papers/`. |
| Override a synced entry | `_data/personal_overrides.yml` (light) or move below END marker (full hand control). |
| Exclude a synced entry | Add bibkey to `_data/personal_skip.yml`. |

## Conventions specific to this site

- **CSS custom properties everywhere.** Tokens live in `_sass/_theme.scss`. Light values on `:root`, dark on `[data-theme="dark"]`. Consume via `var(--token)`. When restyling, do not introduce new hex codes — extend the token set instead.
- **Font stacks are Sass aliases** (`$inter`, `$source-serif`, `$monospace`) so partials read cleanly. The actual `@font-face` lives in `_theme.scss`.
- **`@import "theme"` must come right after `@import "variables"`** in `assets/css/main.scss`. Other partials assume tokens are defined.
- **Susy grid is preserved.** Don't replace `span(N of 12)` / `span(N of 12 last)` calls with CSS Grid — too much downstream churn. Tweak via padding/margin instead.
- **Greedy-nav (jQuery plugin) auto-collapses overflowing nav items into a hamburger menu.** Anything you want kept visible (e.g., the theme toggle) must live *outside* `#site-nav`.
- **The compiled CSS uses unicode glyphs (UTF-8) for Font Awesome icon `content:` values.** They look invisible in plain text but they're real. Don't "fix" them.

## Publications sync (auto from lab repo)

The publications page is mostly auto-synced from the lab repo at `squaresLab/squareslab.github.io` (branch `update`). Workflow:

1. **Students add new papers to the lab repo.** They write a normal BibTeX entry into `_bibliography/publications.bib` and drop the PDF at `public/materials/<bibkey>.pdf` (plus optional `<bibkey>.slides.pdf`, `.poster.pdf`).
2. **Weekly cron** (Mondays 08:17 UTC) and **manual workflow_dispatch** trigger `.github/workflows/sync-publications.yml` here, which runs `bin/sync_publications.py`.
3. The transformer:
   - Fetches the lab bib + materials directory listing.
   - Keeps only entries where the author field substring-matches `le goues` / `le~goues` / `le-goues`.
   - Applies `_data/venue_rules.yml` to infer `pubtype` (0=full, 1=short) and `abbrv` (venue short name) from the BibTeX entry type + venue substrings.
   - Downloads matching PDFs/slides/posters into `assets/papers/<bibkey>.<ext>`.
   - Splices the result into `_bibliography/references.bib` between the `% BEGIN AUTO-SYNCED REGION` and `% END AUTO-SYNCED REGION` markers.
4. **Opens a PR** on the `bot/pub-sync` branch. User reviews and merges.

### When to touch what

- **New lab-coauthored paper:** Add to the lab repo. Wait for sync.
- **Personal-only paper (pre-CMU, solo, etc.):** Add directly to `_bibliography/references.bib` *below* the END marker. Drop PDF in `assets/papers/`. The sync never touches the hand-maintained region.
- **Override one synced field (e.g. wrong abbrv):** `_data/personal_overrides.yml`, keyed by bibkey. Fields here win over rule-inferred values.
- **Full hand control over a synced entry:** Move the entry from the synced region to below the END marker and edit. The transformer detects the duplicate bibkey and skips the synced version with a warning.
- **Drop a synced entry entirely:** Add bibkey to `_data/personal_skip.yml` under `skip:`.

### Sync mechanics gotchas

- **Bibkey is the canonical key.** Personal and lab bibs were aligned in a one-time cleanup pass. If you ever add a paper manually here that's also in the lab bib, use the lab's bibkey to avoid duplicates.
- **PyYAML is required.** Locally: `pip install pyyaml`. CI: handled by the workflow.
- **Idempotency**: running `python3 bin/sync_publications.py` twice on the same lab state produces no diff. If it doesn't, that's a bug in the transformer.
- **Local dry-run**: `python3 bin/sync_publications.py` then `git diff _bibliography/references.bib` and `git status assets/papers/`. Revert with `git checkout -- _bibliography/references.bib assets/papers/`.
- **Venue rules** live in `_data/venue_rules.yml`. First-match-wins. Adding a new venue (e.g., a new conference abbreviation) is just adding a line to the appropriate `*_map` table.

## Gotchas (things that surprised this session)

- **Font Awesome `far` (Regular) variant is not imported** — only `solid` and `brands` are wired up in `assets/css/main.scss`. Using `class="far fa-foo"` will render an empty box. Use `fas` (solid) equivalents. FA v6 keeps the v5 aliases (`fa-file-alt`, `fa-list-alt`, etc.) so most renames are unnecessary; just switch the family prefix.
- **`_config.yml` changes need a server restart.** All other files livereload fine.
- **The `cv/legoues-cv.pdf` symlink** in the repo root (if it exists) may resolve to a path outside the project that the sandbox can't read. If you need to read the CV, ask the user to drop the actual file (`legoues-cv.pdf` + optionally `legoues-cv.tex`) at the repo root. Those are gitignored in spirit (the user has said they won't blindly `git add` them) but check `.gitignore` if unsure.
- **The deployed CV** is `assets/files/cv/legoues-cv.pdf` — that's what the nav points at. The root-level `legoues-cv.pdf` is the user's working copy, not the deployed artifact.
- **The site title in `_config.yml` is empty** (`title: ""`). The masthead uses `site.title | default: site.name` to fall through. Don't "fix" the empty title.
- **Some Susy code emits Sass deprecation warnings** ("Using / for division outside of calc()"). These are from vendor code in `_sass/vendor/susy/`. Leave them alone.

## Deployment safety

- The deploy workflow runs on push to `source`. It uses `JamesIves/github-pages-deploy-action@4.1.5` to force-push `_site/` to `master`. Do not push directly to `master`.
- Anything generated (e.g. `_site/`) is gitignored on `source`. The Action regenerates it on the runner.
- `Gemfile.lock` is gitignored. The Action runs `bundle install` fresh.

## When changing the visual layer

1. Read `docs/superpowers/specs/2026-05-11-academic-site-modernization-design.md` for context.
2. Make changes in `_sass/`, never in compiled `_site/assets/css/`.
3. Run `bundle exec jekyll build` to verify no Sass errors.
4. Use the live dev server to eyeball at multiple widths (375, 768, 1280) and in both themes.
5. If introducing new colors, add them as tokens in `_theme.scss` (both light and dark) first.

## When committing

The user prefers small, scoped commits with a 1–2-sentence "why" in the body. Trailer:

```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```
