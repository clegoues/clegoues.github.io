# Academic Site Modernization — Design Spec

**Status:** DRAFT — pending user review
**Date:** 2026-05-11
**Scope:** Modernize clairelegoues.com (Jekyll / Academic Pages template) — homepage layout, typography, color, dark mode.

## Goal

The current site uses the Academic Pages Jekyll template with its default styling. The bones (Jekyll, content collections, bibliography rendering) work well. The visual layer feels dated: muted gray/teal palette, system-default typography, narrow content column, washed-out link color, and a homepage that shows only a bio paragraph beside a sidebar of icons.

Goal of this work: a modern visual layer (typography, color, layout polish) and a real homepage that introduces the site visitor to Claire and her group, without disrupting the underlying content or template.

## Non-goals

- No template migration. We stay on Academic Pages.
- No content authoring beyond a small `news.yml` data file (2–3 starter items).
- No publication-page restructure. Publications, Talks, Teaching, CV, Posts pages inherit new type/color but keep their existing rendering.
- No backend, analytics, or comments-system changes.
- No "selected publications" block on the homepage. The Publications page handles that.

## Decisions locked during brainstorming

### Top-level navigation

Five items, in this order: **Publications · Talks · Teaching · CV · Posts**.

Removed from nav: Portfolio (files preserved but unlinked). Advising and Calendar were never in the nav; they remain reachable via inline links in the bio prose and via the footer.

### Homepage content blocks

Top to bottom on desktop, in the main (right) column:

1. **About** — the existing `about.md` bio prose, verbatim. The squaresLab / REUSE / advising / pronunciation content is good as-is.
2. **News / Recent** — 3–5 short items, each with date and one-line description. Sourced from a new `_data/news.yml` file.
3. **Group · squaresLab** — short block, 2–3 lines, with link to squareslab.github.io.

The bio paragraph's inline links to Advising and Calendar stay.

### Layout — option B (refined sidebar)

- **Desktop (≥925px, the existing `$large` breakpoint):** two columns. Left sidebar (identity) ~170–200px wide. Right column (main content).
- **Tablet / phone (<925px):** sidebar collapses. Identity becomes a compact horizontal hero (avatar + name beside it on tablet; avatar above name on phone). Main content fills full width.
- **Top nav:** horizontal on tablet and desktop; collapses to a hamburger menu at the existing `$small` breakpoint (≤600px).
- **Footer:** secondary links (Advising, Calendar, Sitemap, ©) on every page.

### Headshot

- **File:** `/headshot-2025.jpeg` (already in `_config.yml`).
- **Shape:** square with 8px rounded corners.
- **Placement:** every page, in the persistent sidebar. On tablet/phone, in the compact hero.
- **Sizes:** ~180px desktop sidebar; ~64–72px tablet hero; ~56px phone hero.

### Typography — editorial

- **Headings:** Source Serif 4 (weights 400, 600, 700). Self-hosted.
- **Body, UI, navigation, pills:** Inter (weights 400, 500, 600, 700). Self-hosted.
- **Monospace (code blocks):** unchanged system stack `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`.
- **Type scale:**
  - Name (homepage hero): 32–40px Source Serif, weight 700, letter-spacing -0.01em.
  - h2: ~24px Source Serif, weight 700.
  - h3: ~18px Source Serif, weight 600.
  - Body: 16px Inter, line-height 1.65.
  - Section labels (e.g., "About", "Recent"): 11px Inter, weight 600, uppercase, letter-spacing 0.1em, muted color.

### Palette

CSS custom properties on `:root` with `[data-theme="dark"]` overrides.

| Token | Light | Dark |
|---|---|---|
| `--bg` | `#FBF9F4` (warm cream) | `#14110D` (warm dark) |
| `--surface` | `#FFFFFF` | `#1C1916` |
| `--ink` | `#1A1A1A` | `#F2EFE9` |
| `--ink-mute` | `#4A4A4A` | `#B8B0A1` |
| `--rule` | `#E8E3D7` | `#2E2A23` |
| `--accent` | `#B0152E` | `#E0556B` |
| `--accent-hover` | `#8B1024` | `#E66980` |

Rationale: warm cream paper instead of pure white pairs with serif type and reads as "modern academic" rather than "default web template." Near-black ink (not the current muted gray) increases presence. CMU-adjacent red accent; slightly desaturated in light mode to work with cream, lifted in dark mode for legibility without sliding into pink.

### Dark mode

- Default: follow `prefers-color-scheme` OS preference.
- Manual override: small icon-only toggle button in the masthead. Persisted in `localStorage` under key `theme` with values `light` / `dark` / `auto`.
- Flash-prevention: inline script in `<head>` that reads `localStorage` and sets `data-theme` on `<html>` before paint. No FOUC.

## Architecture and files

### New files

- `_data/news.yml` — list of news/recent items. Schema: `- date: YYYY-MM-DD`, `text: "..."`, `link: (optional URL)`. Starter file contains 2–3 illustrative entries that the user replaces with real content.
- `_sass/_theme.scss` — CSS custom properties for light and dark palettes, plus the dark-mode override block.
- `_includes/news-feed.html` — renders the news block from `_data/news.yml`.
- `_includes/group-block.html` — renders the squaresLab block. Content (2–3 lines + link to squareslab.github.io) is hardcoded in the include since it is short and changes rarely.
- `_includes/theme-toggle.html` — the dark-mode toggle button (icon + script for click handler).
- `_includes/theme-init.html` — the inline flash-prevention script, included at the top of `<head>`.

### Modified files

- `_config.yml` — verify the existing config still references the right headshot file; no schema changes expected.
- `_sass/_variables.scss` — replace color tokens to reference CSS custom properties; replace font stacks; adjust type scale to the new sizes.
- `_sass/_base.scss` — body background to `var(--bg)`, text to `var(--ink)`, line-height to 1.65.
- `_sass/_masthead.scss` — restyle top nav (cleaner spacing, new type, accent color on hover); add the theme-toggle slot; collapse to hamburger ≤600px.
- `_sass/_sidebar.scss` — restyle the author profile sidebar (rounded-square avatar, tighter spacing, smaller scholar-link icons, modern pill links).
- `_sass/_archive.scss` — restyle archive lists (publication entries, talk entries) to use the new type and accent color for links.
- `_sass/_buttons.scss` — pill-style buttons consistent with the design.
- `_sass/_footer.scss` — new minimal footer with secondary links.
- `_includes/head.html` — add font preconnects, font CSS, theme-init include.
- `_includes/masthead.html` — new nav structure (5 items), hamburger trigger, theme-toggle slot.
- `_includes/footer.html` — new footer markup with secondary nav.
- `_includes/author-profile.html` — refined sidebar markup; rounded-square avatar; pill social links.
- `_layouts/default.html` — verify wrapping divs match new sidebar/content grid structure.
- `_layouts/single.html` — homepage uses this layout. Add conditional render of news + group blocks when page frontmatter has `homepage: true`.
- `_pages/about.md` — add `homepage: true` to frontmatter. Body content (bio prose) stays unchanged.
- `.gitignore` — already updated for `.superpowers/`.

### Component boundaries

- **Theme tokens** live in one place (`_theme.scss`) and are consumed via `var(--...)` everywhere else. Changing a color means editing one file.
- **News and group content** live in `_data/`, not in templates. Editing news doesn't require touching markup.
- **Theme toggle logic** is isolated to two small files (init + toggle). No global JS.
- **Page templates** (`_layouts/single.html`, `_layouts/default.html`) declare structure; they don't know about specific colors or fonts.

### Asset loading

- **Fonts:** self-hosted Source Serif 4 and Inter (woff2). Preload the two weights used in the hero (Source Serif 700, Inter 400). Other weights load with `font-display: swap`.
- **Images:** existing `/headshot-2025.jpeg` only; no new image assets required for the modernization itself.
- **No new JS frameworks.** A small (~30-line) inline script for the theme toggle.

## Behavior details

### Responsive breakpoints

Existing breakpoints in `_variables.scss` are reasonable and will be preserved:

- `$small: 600px` — phone / desktop boundary for hamburger menu and pill wrapping.
- `$medium: 768px` — tablet
- `$large: 925px` — sidebar/single-column boundary (≥900px shows sidebar)
- `$x-large: 1280px` — max content width

### News data schema

```yaml
# _data/news.yml — illustrative entries; user replaces with real content
- date: 2026-03-01
  text: "Example news item."
- date: 2026-01-15
  text: "Example news item with a link."
  link: "/publications/some-paper/"
```

Rendering: most recent first, dates formatted as "Month YYYY", optional `link` makes the text a link. Show all items by default (no pagination — short list).

### Theme toggle states

Three user preferences, cycled by the toggle button: `auto` → `light` → `dark` → `auto`. The button icon reflects the current preference.

The preference is stored in `localStorage` under key `theme` with one of those three values. The applied theme on `<html>` is always `data-theme="light"` or `data-theme="dark"` (resolved attribute, never `auto`). When preference is `auto`, the init script reads `prefers-color-scheme` to pick which of the two resolved values to apply.

### Accessibility

- Color contrast: all text/background combinations in the palette must meet WCAG AA (4.5:1 for body text, 3:1 for large text). Verify with a contrast checker during implementation.
- Focus states: visible focus ring (`outline: 2px solid var(--accent)`) on all interactive elements.
- The theme toggle button has `aria-label="Toggle color theme"` and reflects state via `aria-pressed`.
- The nav hamburger has `aria-expanded` reflecting its state.
- Headshot has `alt="Claire Le Goues"`.

## Testing

- **Local Jekyll build** with `bundle exec jekyll serve` — verify no Liquid errors, no broken includes.
- **Manual verification** in browser at three viewports (375px, 768px, 1280px) — homepage, Publications, Talks, Teaching, CV, Posts, Advising, Calendar, and one publication detail page.
- **Dark mode verification** at each viewport — toggle between auto/light/dark, verify no flash of wrong theme on reload.
- **Existing link integrity** — verify all bio inline links, scholar links, footer links resolve.
- No automated test suite is added. The site has no tests today; adding one is out of scope.

## Risks and mitigations

- **Risk:** Self-hosted font files add bundle size. *Mitigation:* only ship the four Inter weights and three Source Serif weights actually used; preload only the hero weights.
- **Risk:** CSS custom property changes ripple to inherited Academic Pages styles in unexpected ways. *Mitigation:* sweep all `_sass/` partials, not just the ones I've named; manually verify each page type renders.
- **Risk:** Dark-mode flash on initial paint. *Mitigation:* inline `theme-init.html` script in `<head>` before any stylesheet link.
- **Risk:** Headshot file is JPEG and may be large. *Mitigation:* check file size; if >200KB, recommend resizing offline (not part of this work).

## Deferred / future work

- A `featured: true` field in bib entries to enable a "Selected publications" homepage block later.
- Portfolio page visual cleanup (currently unlinked from nav).
- Talkmap page visual cleanup.
- Selected publications block on homepage.
- News RSS feed.

## Out-of-scope confirmation

The user has explicitly asked for: modernized look, dark mode (auto + toggle), keep on Academic Pages, surprise-me palette (resolved to warm cream + CMU-adjacent red). No other features were requested. If new requirements surface during implementation, they go into a follow-up.
