# Publication Sync — Design Spec

**Status:** IMPLEMENTED (May 2026)
**Scope:** Automated sync of publication bibtex entries and PDFs from the lab repo (`squaresLab/squareslab.github.io`) into the personal site (`clegoues/clegoues.github.io`).

## Problem

The user maintains two academic websites with overlapping publication lists:

- **Personal** (`clegoues/clegoues.github.io`) — Jekyll + `jekyll-scholar`. Bib at `_bibliography/references.bib`, PDFs at `assets/papers/<key>.pdf`. Custom fields: `pubtype` (0=full, 1=short), `abbrv` (venue short name), plus `code`/`data`/`tool`/`doi` links.
- **Lab** (`squaresLab/squareslab.github.io`) — Astro/npm. Bib at `_bibliography/publications.bib`, materials at `public/materials/<key>.<ext>`. Custom fields: `project` (comma-separated research-area tags).

Maintaining entries in both bibs was tedious and error-prone. Students could add to the lab repo but not the personal repo; access boundaries didn't match the natural workflow.

## Goal

Lab repo is canonical. Personal site auto-syncs.

## Design decisions

### Approach: Lab canonical, personal pulls

Considered four alternatives (personal-canonical, third-repo, submodule, manual tooling); rejected each. Lab-canonical is the only option that:

1. Keeps the existing student-facing workflow (no change for students).
2. Doesn't grant students write access to the personal repo.
3. Avoids cross-org secret management (lab repo is public; reading it requires no token).
4. Handles divergent custom fields cleanly via a transformer.

### Bib organization: marker-separated regions

`_bibliography/references.bib` is split into two regions by marker comments:

```bibtex
% BEGIN AUTO-SYNCED REGION
<synced entries>
% END AUTO-SYNCED REGION
<hand-maintained entries>
```

The transformer replaces only the synced region. Hand-maintained entries (pre-CMU papers, solo papers, anything personal-only) survive every sync.

### Pubtype and abbrv inference

Students should never need to know about the personal site's `pubtype` and `abbrv` fields. The transformer infers them from BibTeX entry type + venue substrings. Rules live in `_data/venue_rules.yml` (first-match-wins). Lookup tables (`journal_map`, `conference_map`, `workshop_map`, `short_track_map`) map venue substrings to clean abbreviations.

Fallback for unknown venues: empty `abbrv` (renders without a venue tag), which is visually obvious so the user adds a line to the appropriate map.

### Author-match filter

Substring match on "le goues" / "le~goues" / "le-goues" anywhere in the joined author field, case-insensitive. The user is a co-author on everything that should appear; no further filtering needed.

### PDFs: download and commit (not hot-link)

For each synced entry, the transformer probes the lab repo's raw URL for each expected extension (`<key>.pdf`, `<key>.slides.pdf`, `<key>.slides.pptx`, `<key>.slides.key`, `<key>.slides.odp`, `<key>.poster.pdf`). For each that returns 200, downloads into `assets/papers/` and sets the corresponding bib field.

Rationale: self-hosted PDFs keep the personal site resilient to lab-repo restructuring or rate-limiting. Storage stays well under GitHub Pages' 1GB limit even with growth.

Orphans (PDFs whose entry has been removed) are left in place; the transformer reports them but doesn't delete. Manual cleanup if desired.

### Override mechanisms

Three escape hatches, in order of weight:

1. **`_data/personal_overrides.yml`** — keyed by bibkey, fields merge over the synced entry. Light touch.
2. **Move below END marker** — full hand control over a specific entry. Duplicate-bibkey detection means hand-region wins; synced version is dropped with a warning.
3. **`_data/personal_skip.yml`** — list of bibkeys to exclude entirely from the personal site.

### Personal-only entries

For papers the user wants on the personal site but NOT the lab site (pre-CMU, solo, invited pieces): just don't put them in the lab bib. Add directly to the hand-maintained region. No new mechanism needed.

## Trigger and trust model

**GitHub Actions workflow** on the personal repo:
- `on: schedule` — weekly cron (Mondays 08:17 UTC).
- `on: workflow_dispatch` — manual trigger button.
- Output: opens or updates a PR on a `bot/pub-sync` branch against `source`.

PR mode (not auto-commit) for the first few months until trust builds. Switching to direct-commit is a one-line workflow change.

No secrets required. Lab repo is public; transformer uses `urllib.request` to fetch raw files. PR creation uses GitHub's auto-provided `GITHUB_TOKEN`.

## Deferred — phase 2 candidates

- **Cross-repo `repository_dispatch` trigger.** A workflow on the lab repo that fires a `repository_dispatch` event at the personal repo on pushes touching the bib or materials. Reduces sync latency from "up to a week" to "minutes." Trade-off: a fine-grained PAT lives as a secret on the lab repo, which has student write access. Mitigations exist (scope PAT minimally; require reviews on lab workflow changes), but defer until weekly cron proves insufficient.
- **Auto-commit mode** (instead of PR mode). Defer until 1-3 months of clean PRs build confidence.
- **Reverse-direction sync** (personal → lab) for personal-only papers that should appear on the lab site. Not needed; personal-only is personal-only by definition.

## File inventory

### Files created

- `bin/sync_publications.py` — the transformer (~480 lines, Python 3 + PyYAML).
- `_data/venue_rules.yml` — pubtype/abbrv inference rules + lookup tables.
- `_data/personal_overrides.yml` — per-bibkey field overrides (empty by default).
- `_data/personal_skip.yml` — list of bibkeys to exclude (empty by default).
- `.github/workflows/sync-publications.yml` — weekly cron + manual trigger; opens PR on changes.

### Files modified

- `_bibliography/references.bib` — added BEGIN/END marker comments at top. After first sync, 107 entries that were also in the lab bib were promoted from the hand region into the synced region.
- `CLAUDE.md` — new "Publications sync" section; file-map updated.
- `README.md` — "A new publication" subsection rewritten around the three workflows.
- `.gitignore` — added `__pycache__/` and `*.pyc`.

### One-time cleanup (not committed permanently)

Before adding the markers, a one-shot script (`bin/cleanup_keys_oneshot.py`, deleted after use) renamed 71 personal-bib entries (and their corresponding PDFs in `assets/papers/`) to match the lab's canonical bibkeys. Matches via DOI-exact (56) and title-normalized-equal (14), plus one manually confirmed rename (gi18 → AfzalTuringTest2018).

URL breakage trade-off: per-paper URLs like `/publications/<old_key>/` now 404. Accepted as the cost of having bibkey equality serve as the canonical match.

## Verification

End-to-end tests run during implementation:

1. **Local sync run**: 109 synced entries, 118 PDFs downloaded.
2. **Build clean**: `bundle exec jekyll build --config _config.yml,_config.dev.yml` produces no errors.
3. **Idempotency**: second sync run produces no diff.
4. **Override mechanism**: tested by adding `widder2024whatisabug: {abbrv: TEST-VALUE}` to `personal_overrides.yml`, re-running, observing TEST-VALUE in the rendered bib, reverting.
5. **Hand-wins-over-sync**: tested by leaving entries in the hand region during the first run; transformer correctly emitted "skip (hand-maintained wins)" for all 107.

Pending validation (post-merge):

6. **Workflow dispatch**: manually trigger the GH Action from the Actions tab; verify it opens (or no-ops) a PR.
7. **Real lab-side update**: after a future lab repo push, verify the weekly cron picks it up cleanly.
