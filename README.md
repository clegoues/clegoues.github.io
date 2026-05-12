# clairelegoues.com

Source for [clairelegoues.com](https://www.clairelegoues.com). Built with Jekyll, originally forked from the [Academic Pages](https://academicpages.github.io/) template and substantially customized.

## Running locally

```bash
bundle install                                          # once, after cloning
bundle exec jekyll serve \
  --config _config.yml,_config.dev.yml \
  --port 4040 --host 127.0.0.1 --livereload
```

Then open <http://127.0.0.1:4040/>. The `_config.dev.yml` overlay swaps `site.url` to localhost so nav links resolve locally instead of jumping to the production site.

If you change `_config.yml`, you have to restart the server (Jekyll doesn't auto-reload config).

## Deploying

Pushing to the `source` branch triggers `.github/workflows/build-and-deploy.yml`, which builds the site on a runner and force-pushes `_site/` to `master`. GitHub Pages serves from `master`. End-to-end deploy takes 1–2 minutes after push.

There is no GitHub-Pages-side Jekyll build, which means **all plugins work**, including `jekyll-scholar` (not whitelisted by GitHub Pages otherwise).

## Repository layout

```
_config.yml             Site settings: author info, plugins, collections, scholar config.
_config.dev.yml         Local-only overlay (URL). Used via --config _config.yml,_config.dev.yml.
_data/
  navigation.yml        Top-nav and footer-nav link lists.
  news.yml              Homepage "Recent" items. Edit this to update news.
_pages/                 Static pages. about.md is the homepage.
_publications/          Per-paper detail pages (one .md per paper).
_bibliography/          .bib files rendered into /publications/ via jekyll-scholar.
_talks/                 Per-talk pages.
_teaching/              Per-course pages.
_posts/                 Blog posts.
_layouts/               Page templates.
_includes/              Reusable template fragments.
_sass/                  SCSS partials. _theme.scss has the design tokens.
assets/
  css/main.scss         SCSS entry point.
  fonts/                Self-hosted woff2 (Inter, Source Serif 4).
  files/cv/             CV PDF lives here (linked from nav).
  papers/               PDFs of papers, referenced from .bib entries.
images/                 Site images (headshot, etc.).
```

## Updating common things

### Homepage news

Edit `_data/news.yml`. Each item:

```yaml
- date: 2026-04-15           # required, YYYY-MM-DD; controls sort order
  text: "Short description." # required
  link: "/publications/foo/" # optional; site-relative or full URL
```

Order in the file doesn't matter — the include sorts by date descending. Rendered as "Mon YYYY" on the homepage.

### Navigation

Edit `_data/navigation.yml`. Two lists:

- `main:` — top nav (Publications, Talks, etc.)
- `secondary:` — footer secondary links (Calendar, Sitemap)

Each entry has `title:` and `url:` (site-relative or absolute).

### Personal info (name, role, headshot, social links)

Edit the `author:` block in `_config.yml`. Adding a key like `linkedin: "claire-le-goues-9b39985"` makes the corresponding social link appear in the sidebar; the link templates live in `_includes/author-profile.html`. Recognized keys include `email`, `googlescholar`, `orcid`, `dblp`, `github`, `bluesky`, `linkedin`, `arxiv`, plus many more (see the include for the full list).

### A new publication

Most of the publications page is auto-synced from the lab repo at `squaresLab/squareslab.github.io`. Three workflows depending on the paper:

1. **Lab-coauthored paper (most common)**: Don't touch this repo. Add the entry to the **lab** repo's `_bibliography/publications.bib` and drop the PDF in `public/materials/<bibkey>.pdf`. A weekly GitHub Action here (`.github/workflows/sync-publications.yml`) detects the change, downloads the PDF, fills in the personal-site fields (`pubtype`/`abbrv` from `_data/venue_rules.yml`), and opens a PR. Merge the PR to publish.

2. **Personal-only paper** (pre-CMU, solo, anything not lab-relevant): Edit `_bibliography/references.bib` directly. Add the entry **below** the `% END AUTO-SYNCED REGION` marker; the sync will leave it alone. Drop the PDF in `assets/papers/<bibkey>.pdf`.

3. **Override a synced entry's field** (e.g., wrong venue abbreviation): add the bibkey + the field(s) to `_data/personal_overrides.yml`. Or move the entry below the END marker for full hand control.

To **exclude** a synced entry: add its bibkey to `_data/personal_skip.yml` under `skip:`.

Manual sync trigger: from the Actions tab on GitHub, run "Sync publications from lab repo" via the workflow_dispatch button. Or locally: `pip install pyyaml && python3 bin/sync_publications.py`.

### A new talk / course / blog post

Drop a file in `_talks/`, `_teaching/`, or `_posts/` respectively. Existing entries in those directories are templates.

### CV

The deployed CV PDF lives at `assets/files/cv/legoues-cv.pdf`. The nav points there. Replace that file to update.

## Design system

The visual layer is defined in `_sass/_theme.scss`:

- **Typography:** Source Serif 4 (headings) + Inter (body / UI), self-hosted in `assets/fonts/`.
- **Palette:** CSS custom properties on `:root` (light) with `[data-theme="dark"]` overrides. Warm cream background, near-black ink, CMU-adjacent red accent.
- **Dark mode:** auto + manual toggle in the masthead. Preference is stored in `localStorage` under key `theme` (values: `auto` / `light` / `dark`). The init script in `_includes/theme-init.html` resolves the preference before paint to prevent flash.

To change a color: edit the relevant `--token` in `_sass/_theme.scss`. Everything downstream uses `var(--token)` references.

The design spec lives at `docs/superpowers/specs/2026-05-11-academic-site-modernization-design.md`.

## License

Site content © Claire Le Goues. Original Academic Pages template is MIT-licensed (see `LICENSE`); it was forked by [Stuart Geiger](https://github.com/staeiou) from the [Minimal Mistakes Jekyll Theme](https://mmistakes.github.io/minimal-mistakes/) © 2016 Michael Rose.
