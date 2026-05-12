#!/usr/bin/env python3
"""
Sync publications from the squaresLab lab bib into the personal site's bib.

Fetches the lab bibliography and materials directory, filters to entries
where Claire Le Goues is a co-author, applies venue rules to fill in the
personal-site-specific `pubtype` / `abbrv` fields, downloads each entry's
PDF/slides/poster into assets/papers/, and splices the result into the
AUTO-SYNCED region of _bibliography/references.bib.

Run with no arguments to perform a sync:

    python3 bin/sync_publications.py

The script is idempotent: a second run when the lab bib hasn't changed
should produce no diff.

Dependencies: PyYAML (`pip install pyyaml` if missing).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("error: PyYAML not installed. Run: pip install pyyaml\n")
    sys.exit(2)


# --- Configuration ---------------------------------------------------------

LAB_BIB_URL = "https://raw.githubusercontent.com/squaresLab/squareslab.github.io/update/_bibliography/publications.bib"
LAB_MATERIALS_API = "https://api.github.com/repos/squaresLab/squareslab.github.io/contents/public/materials?ref=update"
LAB_MATERIALS_RAW = "https://raw.githubusercontent.com/squaresLab/squareslab.github.io/update/public/materials/{filename}"

PERSONAL_BIB = Path("_bibliography/references.bib")
PAPERS_DIR = Path("assets/papers")
VENUE_RULES = Path("_data/venue_rules.yml")
OVERRIDES_FILE = Path("_data/personal_overrides.yml")
SKIP_FILE = Path("_data/personal_skip.yml")

AUTHOR_MATCH = ["le goues", "le~goues", "le-goues"]

BEGIN_MARKER = "% BEGIN AUTO-SYNCED REGION"
END_MARKER = "% END AUTO-SYNCED REGION"

# Fields we KEEP on the synced entry (everything else from the lab is dropped).
KEEP_FIELDS = {
    "author", "title", "year", "month", "booktitle", "journal", "series",
    "volume", "number", "pages", "publisher", "address", "location",
    "doi", "isbn", "issn", "editor", "edition", "url",
    "code", "data", "tool", "website", "video", "results", "poster",
    "pdf", "slides", "abbrv", "pubtype",
}

# Material file suffixes we probe and the bib field each maps to.
# Order: more-specific first so "luo2026.slides.pdf" doesn't get classified
# as a plain pdf by a too-eager startswith.
MATERIAL_SUFFIXES = [
    (".slides.pdf",  "slides"),
    (".slides.pptx", "slides"),
    (".slides.key",  "slides"),
    (".slides.odp",  "slides"),
    (".poster.pdf",  "poster"),
    (".pdf",         "pdf"),
]


# --- BibTeX parser (tolerant; reused from oneshot) -------------------------

def parse_bib(text):
    """Yield (entry_type, key, fields_dict, raw_field_order) tuples.

    `raw_field_order` is the list of field names as they appeared in source,
    used to preserve ordering on re-serialization.
    """
    text = re.sub(r"\A---\s*\n---\s*\n", "", text)
    text = re.sub(r"(?m)^\s*%.*$", "", text)

    i = 0
    n = len(text)
    while i < n:
        m = re.compile(r"@([a-zA-Z]+)\s*\{").search(text, i)
        if not m:
            break
        entry_type = m.group(1).lower()
        i = m.end()

        key_end = text.find(",", i)
        if key_end < 0:
            break
        key = text[i:key_end].strip()
        i = key_end + 1

        fields: dict[str, str] = {}
        order: list[str] = []
        depth = 1
        while i < n and depth > 0:
            while i < n and text[i] in " \t\n\r,":
                i += 1
            if i >= n:
                break
            if text[i] == "}":
                depth -= 1
                i += 1
                break
            fname_match = re.match(r"([a-zA-Z][\w-]*)\s*=\s*", text[i:])
            if not fname_match:
                while i < n and depth > 0:
                    if text[i] == "{":
                        depth += 1
                    elif text[i] == "}":
                        depth -= 1
                    i += 1
                break
            fname = fname_match.group(1).lower()
            i += fname_match.end()
            if i >= n:
                break
            ch = text[i]
            if ch == "{":
                bd = 1
                i += 1
                start = i
                while i < n and bd > 0:
                    if text[i] == "{":
                        bd += 1
                    elif text[i] == "}":
                        bd -= 1
                    if bd > 0:
                        i += 1
                value = text[start:i]
                i += 1
            elif ch == '"':
                i += 1
                start = i
                while i < n and text[i] != '"':
                    i += 1
                value = text[start:i]
                if i < n:
                    i += 1
            else:
                start = i
                while i < n and text[i] not in ",}":
                    i += 1
                value = text[start:i].strip()
            if fname not in fields:
                order.append(fname)
            fields[fname] = value
        yield entry_type, key, fields, order


# --- HTTP helpers ----------------------------------------------------------

def http_get(url, binary=False, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "publications-sync"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read()
    return body if binary else body.decode("utf-8")


def fetch_lab_bib():
    print(f"  fetching lab bib from {LAB_BIB_URL}", file=sys.stderr)
    return http_get(LAB_BIB_URL)


def fetch_materials_index():
    """Return dict[key, dict[suffix, filename]] from the lab materials listing."""
    print(f"  fetching materials index from GitHub API", file=sys.stderr)
    data = json.loads(http_get(LAB_MATERIALS_API))
    by_key: dict[str, dict[str, str]] = {}
    for item in data:
        if item.get("type") != "file":
            continue
        name = item["name"]
        # Match against suffix list, longest-suffix-first.
        for suffix, _field in MATERIAL_SUFFIXES:
            if name.endswith(suffix):
                key = name[: -len(suffix)]
                by_key.setdefault(key, {})[suffix] = name
                break
    return by_key


# --- Filtering & transformation -------------------------------------------

def is_authored(fields):
    """Case-insensitive substring match for any AUTHOR_MATCH in the author field."""
    authors = fields.get("author", "")
    # Lower-case and remove BibTeX braces for matching.
    clean = re.sub(r"[{}]", "", authors).lower()
    return any(needle in clean for needle in AUTHOR_MATCH)


def normalize_author(authors):
    """Convert `Claire {Le Goues}` -> `Claire {Le~Goues}` to match personal style."""
    return authors.replace("{Le Goues}", "{Le~Goues}")


def _flat(s):
    """Normalize a venue/booktitle/journal string for substring matching.

    Lower-cases, drops BibTeX braces (used to suppress kerning/capitalization
    on acronyms like {AAAI} or {IEEE}), drops most punctuation (commas,
    periods, parentheses, brackets, colons, slashes, ampersands), and
    collapses any whitespace run to a single space. The point is that the
    rule lookup tables can write a single canonical phrase like

        software analysis evolution and reengineering

    and match every BibTeX dialect: "Software Analysis, Evolution, and
    Reengineering", "Software Analysis, Evolution and Reengineering" with
    or without an Oxford comma, braced acronyms, line-wrapped values, etc.
    """
    s = s.lower()
    # Drop braces and the common punctuation that varies between dialects.
    # Keep letters, digits, spaces, and a handful of helpful separators
    # (@ for tracks like AST@ICSE, # for nothing in particular, apostrophes
    # for "GI '18" style suffixes).
    s = re.sub(r"[{}()\[\],.:/;&\"]", " ", s)
    # Collapse all whitespace.
    return re.sub(r"\s+", " ", s).strip()


def apply_venue_rules(entry_type, fields, rules_data):
    """Return dict of fields to set (pubtype, abbrv) based on rules."""
    rules = rules_data.get("rules", [])
    for rule in rules:
        match = rule.get("match", {})
        if match.get("entry_type") != entry_type:
            continue
        # Check all field-contains constraints (whitespace-normalized).
        all_field_matches = True
        for field_name, needles in match.get("field_contains_any", {}).items():
            haystack = _flat(fields.get(field_name, ""))
            if not any(_flat(n) in haystack for n in needles):
                all_field_matches = False
                break
        if not all_field_matches:
            continue

        # Match — compute the set.
        result = {}
        setblock = rule.get("set", {})
        if "pubtype" in setblock:
            result["pubtype"] = str(setblock["pubtype"])
        if "abbrv" in setblock:
            result["abbrv"] = setblock["abbrv"]
        if "abbrv_from" in setblock:
            table = rules_data.get(setblock["abbrv_from"], {})
            # Search booktitle then journal for first matching substring
            # (whitespace-normalized; lab bib often wraps venue names).
            for haystack_field in ("booktitle", "journal"):
                haystack = _flat(fields.get(haystack_field, ""))
                for needle, value in table.items():
                    if _flat(needle) in haystack:
                        result["abbrv"] = value
                        break
                if "abbrv" in result:
                    break
        return result
    return {}


# --- PDF download helpers --------------------------------------------------

def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(64 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def md5_of_bytes(b):
    return hashlib.md5(b).hexdigest()


def download_materials(key, materials_for_key, papers_dir):
    """Download all materials for `key`, return dict[bib_field, filename_only]."""
    field_map: dict[str, str] = {}
    for suffix, field in MATERIAL_SUFFIXES:
        if suffix not in materials_for_key:
            continue
        remote_name = materials_for_key[suffix]
        local_name = f"{key}{suffix}"
        local_path = papers_dir / local_name
        url = LAB_MATERIALS_RAW.format(filename=remote_name)
        try:
            content = http_get(url, binary=True)
        except urllib.error.HTTPError as e:
            print(f"    HTTP {e.code} for {url}; skipping", file=sys.stderr)
            continue
        # Idempotency: only write if content actually differs.
        if local_path.exists() and md5_of(local_path) == md5_of_bytes(content):
            pass  # no change
        else:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(content)
            print(f"    wrote {local_path} ({len(content)} bytes)", file=sys.stderr)
        # Only set the bib field once per suffix-family
        # (e.g., slides.pdf wins over slides.pptx if both exist).
        if field not in field_map:
            field_map[field] = local_name
    return field_map


# --- Serialization ---------------------------------------------------------

# Preferred output order. Anything not listed here gets appended in original
# bib order.
FIELD_ORDER_PREFIX = [
    "author", "title", "booktitle", "journal", "series", "volume", "number",
    "pages", "year", "month", "publisher", "address", "location",
    "editor", "edition", "doi", "url", "isbn", "issn",
    "abbrv", "pubtype",
    "pdf", "slides", "poster", "code", "data", "tool", "website", "video", "results",
]


def serialize_entry(entry_type, key, fields, raw_order):
    """Render a single bibtex entry as a string."""
    # Build output field order.
    seen = set()
    ordered_fields: list[str] = []
    for f in FIELD_ORDER_PREFIX:
        if f in fields and f not in seen:
            ordered_fields.append(f)
            seen.add(f)
    for f in raw_order:
        if f in fields and f not in seen and f in KEEP_FIELDS:
            ordered_fields.append(f)
            seen.add(f)
    # Any remaining fields we kept that weren't in either list (shouldn't happen).
    for f in fields:
        if f not in seen and f in KEEP_FIELDS:
            ordered_fields.append(f)
            seen.add(f)

    lines = [f"@{entry_type}{{{key},"]
    for f in ordered_fields:
        lines.append(f"  {f} = {{{fields[f]}}},")
    # Strip trailing comma from last field line for cleanliness.
    if lines[-1].endswith(","):
        lines[-1] = lines[-1][:-1]
    lines.append("}")
    return "\n".join(lines)


# --- Main ------------------------------------------------------------------

def load_yaml(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def hand_maintained_keys(bib_text):
    """Return the set of bibkeys defined below the END marker."""
    parts = bib_text.split(END_MARKER, 1)
    if len(parts) < 2:
        return set()
    hand_section = parts[1]
    return {key for _et, key, _f, _o in parse_bib(hand_section)}


def splice_into_bib(bib_text, synced_text):
    """Replace the region between BEGIN_MARKER and END_MARKER with synced_text."""
    if BEGIN_MARKER not in bib_text or END_MARKER not in bib_text:
        raise RuntimeError(
            f"missing markers in {PERSONAL_BIB}; expected '{BEGIN_MARKER}' "
            f"and '{END_MARKER}'. Re-run Step 2 of the implementation plan."
        )
    before, rest = bib_text.split(BEGIN_MARKER, 1)
    _, after = rest.split(END_MARKER, 1)
    return f"{before}{BEGIN_MARKER}\n\n{synced_text}\n\n{END_MARKER}{after}"


def main():
    if not PERSONAL_BIB.exists():
        sys.exit(f"error: {PERSONAL_BIB} not found")

    rules_data = load_yaml(VENUE_RULES)
    overrides_data = load_yaml(OVERRIDES_FILE)
    skip_data = load_yaml(SKIP_FILE)
    skip_keys = set((skip_data or {}).get("skip", []) or [])

    print(f"loaded rules:    {VENUE_RULES} ({len(rules_data.get('rules', []))} rules)", file=sys.stderr)
    print(f"loaded overrides:{OVERRIDES_FILE} ({len(overrides_data or {})} keys)", file=sys.stderr)
    print(f"loaded skip:     {SKIP_FILE} ({len(skip_keys)} keys)", file=sys.stderr)

    lab_text = fetch_lab_bib()
    materials_index = fetch_materials_index()
    print(f"  materials: {len(materials_index)} keys with at least one file", file=sys.stderr)

    # Read personal bib up front to know hand-maintained keys.
    with open(PERSONAL_BIB) as f:
        personal_text = f.read()
    hand_keys = hand_maintained_keys(personal_text)
    print(f"  hand-maintained keys: {len(hand_keys)}", file=sys.stderr)

    PAPERS_DIR.mkdir(parents=True, exist_ok=True)

    synced_entries: list[tuple[str, str, dict, list[str]]] = []
    skipped_by_filter = 0
    skipped_by_skiplist = 0
    skipped_by_handwins = 0
    downloaded_files = []
    missing_materials = []

    for entry_type, key, fields, raw_order in parse_bib(lab_text):
        if not is_authored(fields):
            skipped_by_filter += 1
            continue
        if key in skip_keys:
            print(f"  skip (in personal_skip.yml): {key}", file=sys.stderr)
            skipped_by_skiplist += 1
            continue
        if key in hand_keys:
            print(f"  skip (hand-maintained wins): {key}", file=sys.stderr)
            skipped_by_handwins += 1
            continue

        # Strip unwanted fields.
        kept = {k: v for k, v in fields.items() if k in KEEP_FIELDS}

        # Normalize author convention.
        if "author" in kept:
            kept["author"] = normalize_author(kept["author"])

        # Apply venue rules.
        rule_set = apply_venue_rules(entry_type, kept, rules_data)
        kept.update(rule_set)

        # Apply per-bibkey overrides (these win). A value of `null` in the
        # override drops the field entirely — useful for suppressing a field
        # that venue_rules.yml inferred but you want absent (e.g., abbrv on
        # a guest-editorial pubtype=2 entry).
        if overrides_data and key in overrides_data:
            for ofield, oval in (overrides_data[key] or {}).items():
                if oval is None:
                    kept.pop(ofield, None)
                else:
                    kept[ofield] = oval if isinstance(oval, str) else str(oval)

        # Download materials if present.
        if key in materials_index:
            file_fields = download_materials(key, materials_index[key], PAPERS_DIR)
            for f, name in file_fields.items():
                kept[f] = name
                downloaded_files.append(name)
        else:
            missing_materials.append(key)

        synced_entries.append((entry_type, key, kept, raw_order))

    # Sort: year desc, then key.
    def sort_key(entry):
        et, key, fields, _ = entry
        try:
            yr = int(fields.get("year", "0"))
        except ValueError:
            yr = 0
        return (-yr, key)
    synced_entries.sort(key=sort_key)

    # Serialize.
    body = "\n\n".join(
        serialize_entry(et, key, f, raw)
        for et, key, f, raw in synced_entries
    )
    new_bib = splice_into_bib(personal_text, body)

    if new_bib != personal_text:
        with open(PERSONAL_BIB, "w") as f:
            f.write(new_bib)
        print(f"\nwrote {PERSONAL_BIB} ({len(synced_entries)} synced entries)")
    else:
        print(f"\nno changes to {PERSONAL_BIB}")

    # Summary report.
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"synced entries:        {len(synced_entries)}")
    print(f"skipped (not authored):{skipped_by_filter}")
    print(f"skipped (skip-list):   {skipped_by_skiplist}")
    print(f"skipped (hand-wins):   {skipped_by_handwins}")
    print(f"PDFs/materials written:{len(downloaded_files)}")
    if missing_materials:
        print(f"entries without materials in lab: {len(missing_materials)}")
        for k in missing_materials[:10]:
            print(f"  - {k}")
        if len(missing_materials) > 10:
            print(f"  ... and {len(missing_materials) - 10} more")

    return 0


if __name__ == "__main__":
    sys.exit(main())
