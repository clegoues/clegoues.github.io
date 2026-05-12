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
| Add a publication | `_bibliography/papers.bib` (`jekyll-scholar` does the rest) |

## Conventions specific to this site

- **CSS custom properties everywhere.** Tokens live in `_sass/_theme.scss`. Light values on `:root`, dark on `[data-theme="dark"]`. Consume via `var(--token)`. When restyling, do not introduce new hex codes — extend the token set instead.
- **Font stacks are Sass aliases** (`$inter`, `$source-serif`, `$monospace`) so partials read cleanly. The actual `@font-face` lives in `_theme.scss`.
- **`@import "theme"` must come right after `@import "variables"`** in `assets/css/main.scss`. Other partials assume tokens are defined.
- **Susy grid is preserved.** Don't replace `span(N of 12)` / `span(N of 12 last)` calls with CSS Grid — too much downstream churn. Tweak via padding/margin instead.
- **Greedy-nav (jQuery plugin) auto-collapses overflowing nav items into a hamburger menu.** Anything you want kept visible (e.g., the theme toggle) must live *outside* `#site-nav`.
- **The compiled CSS uses unicode glyphs (UTF-8) for Font Awesome icon `content:` values.** They look invisible in plain text but they're real. Don't "fix" them.

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
