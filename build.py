#!/usr/bin/env python3
"""Build the static site in dist/ from templates/, content/, and assets/publications.bib."""

import re
import shutil
from pathlib import Path
from string import Template

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
CONTENT_DIR = BASE_DIR / "content"
ASSETS_DIR = BASE_DIR / "assets"
STYLES_PATH = BASE_DIR / "styles.css"
CNAME_PATH = BASE_DIR / "CNAME"
DIST_DIR = BASE_DIR / "dist"
BIB_PATH = ASSETS_DIR / "publications.bib"

PAGES = [
    ("index.html", "Samuel Ozminkowski"),
    ("talks.html", "Talks & Posters — Samuel Ozminkowski"),
    ("software.html", "Software — Samuel Ozminkowski"),
    ("honors.html", "Honors & Awards — Samuel Ozminkowski"),
    ("teaching.html", "Teaching — Samuel Ozminkowski"),
]

ACCENTS = {
    "'": {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "n": "ń", "y": "ý",
          "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú"},
    "`": {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù",
          "A": "À", "E": "È", "I": "Ì", "O": "Ò", "U": "Ù"},
    '"': {"a": "ä", "e": "ë", "i": "ï", "o": "ö", "u": "ü",
          "A": "Ä", "E": "Ë", "I": "Ï", "O": "Ö", "U": "Ü"},
    "^": {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û",
          "A": "Â", "E": "Ê", "I": "Î", "O": "Ô", "U": "Û"},
    "~": {"a": "ã", "n": "ñ", "o": "õ", "A": "Ã", "N": "Ñ", "O": "Õ"},
}

_BRACED_ACCENT_RE = re.compile(r"""\{\\(['`"^~])\{?([a-zA-Z])\}?\}""")
_BARE_ACCENT_RE = re.compile(r"""\\(['`"^~])\{?([a-zA-Z])\}?""")
_AND_SPLIT_RE = re.compile(r"\s+and\s+")
_WS_SPLIT_RE = re.compile(r"\s+")
_INITIAL_RE = re.compile(r"^[A-Z]\.$")
_FIELD_SEP_RE = re.compile(r"[\s,]")


def parse_bibtex(text):
    """Brace-depth-aware BibTeX entry/field scanner, ported from the former parseBibtex() in index.html."""
    entries = []
    i = 0
    n = len(text)
    while i < n:
        at = text.find("@", i)
        if at == -1:
            break
        brace_open = text.find("{", at)
        if brace_open == -1:
            break
        entry_type = text[at + 1:brace_open].strip().lower()
        depth = 1
        j = brace_open + 1
        while j < n and depth > 0:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        body = text[brace_open + 1:j - 1]
        i = j

        comma_idx = body.find(",")
        key = body[:comma_idx].strip()
        fields_str = body[comma_idx + 1:]
        fields = {}
        k = 0
        m = len(fields_str)
        while k < m:
            while k < m and _FIELD_SEP_RE.match(fields_str[k]):
                k += 1
            if k >= m:
                break
            eq_idx = fields_str.find("=", k)
            if eq_idx == -1:
                break
            name = fields_str[k:eq_idx].strip().lower()
            v = eq_idx + 1
            while v < m and fields_str[v].isspace():
                v += 1
            value = ""
            if v < m and fields_str[v] == "{":
                d = 1
                w = v + 1
                while w < m and d > 0:
                    if fields_str[w] == "{":
                        d += 1
                    elif fields_str[w] == "}":
                        d -= 1
                        if d == 0:
                            w += 1
                            break
                    value += fields_str[w]
                    w += 1
                k = w
            elif v < m and fields_str[v] == '"':
                w2 = v + 1
                while w2 < m and fields_str[w2] != '"':
                    value += fields_str[w2]
                    w2 += 1
                k = w2 + 1
            else:
                w3 = v
                while w3 < m and fields_str[w3] != ",":
                    value += fields_str[w3]
                    w3 += 1
                k = w3
            fields[name] = value.strip()

        entries.append({"type": entry_type, "key": key, "fields": fields})
    return entries


def _accent_sub(match):
    acc, ch = match.group(1), match.group(2)
    return ACCENTS.get(acc, {}).get(ch, ch)


def clean_latex(s):
    s = _BRACED_ACCENT_RE.sub(_accent_sub, s)
    s = _BARE_ACCENT_RE.sub(_accent_sub, s)
    return s.replace("{", "").replace("}", "")


def format_authors(raw):
    if not raw:
        return ""
    authors = [clean_latex(a.strip()) for a in _AND_SPLIT_RE.split(raw)]
    parsed = []
    for a in authors:
        parts = [p.strip() for p in a.split(",")]
        if len(parts) >= 3:
            last, suffix, first = parts[0], parts[1], parts[2]
        else:
            last = parts[0] if len(parts) > 0 else ""
            first = parts[1] if len(parts) > 1 else ""
            suffix = ""
        tokens = [t for t in _WS_SPLIT_RE.split(first) if t]
        initials_tokens = [
            tok if _INITIAL_RE.match(tok) else (tok[0].upper() + ".")
            for tok in tokens
        ]
        initials = " ".join(initials_tokens)
        display = (initials + " " + last) if initials else last
        if suffix:
            display += ", " + suffix
        is_me = last == "Ozminkowski" and initials == "S."
        parsed.append({"display": display, "is_me": is_me})

    me_idx = -1
    for idx, p in enumerate(parsed):
        if p["is_me"]:
            me_idx = idx
            break

    def wrap(p):
        return f'<span class="me">{p["display"]}</span>' if p["is_me"] else p["display"]

    if len(parsed) > 4 and me_idx != -1:
        truncated = parsed[:me_idx + 1]
        return ", ".join(wrap(p) for p in truncated) + ", et al."

    names = [wrap(p) for p in parsed]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return names[0] + " and " + names[1]
    return ", ".join(names[:-1]) + ", and " + names[-1]


def render_entry(entry):
    f = entry["fields"]
    title = clean_latex(f.get("title", ""))
    authors = format_authors(f.get("author", ""))
    html = authors + ", &ldquo;" + title + ",&rdquo;"

    if entry["type"] == "article":
        venue = clean_latex(f.get("journal", ""))
        html += ' <span class="venue">' + venue + "</span>"
        if f.get("volume"):
            html += ", vol. " + f["volume"]
        html += ", " + f.get("year", "")
        if f.get("note"):
            html += " (" + f["note"] + ")"
        html += "."
        if f.get("doi"):
            html += (
                ' <span class="meta"><a href="https://doi.org/' + f["doi"]
                + '" target="_blank" rel="noopener">doi:' + f["doi"] + "</a></span>"
            )
    elif entry["type"] == "misc":
        html += " " + f.get("year", "") + "."
        if f.get("award"):
            # Honors moved to its own page, so the badge link is no longer an in-page "#honors" anchor.
            html += ' <a class="badge" href="honors.html#honors">' + f["award"] + "</a>"
        if f.get("eprint"):
            html += (
                ' <span class="meta"><a href="https://doi.org/10.48550/arXiv.' + f["eprint"]
                + '" target="_blank" rel="noopener">arXiv:' + f["eprint"] + "</a></span>"
            )
    else:
        html += " " + f.get("note", "in preparation") + "."

    return "<li>" + html + "</li>"


def collect_publication_entries(bib_path):
    text = bib_path.read_text(encoding="utf-8")
    entries = parse_bibtex(text)
    groups = {"article": [], "misc": [], "unpublished": []}
    # Preserve .bib file order within each type, matching the original JS (no sort-by-year).
    for entry in entries:
        if entry["type"] in groups:
            groups[entry["type"]].append(render_entry(entry))
    return groups


def load_text(path):
    return path.read_text(encoding="utf-8")


def render_page(shell_tmpl, nav_html, aside_html, title, main_html):
    return shell_tmpl.substitute(title=title, nav=nav_html, aside=aside_html, main=main_html)


def copy_static(dist_dir):
    shutil.copytree(ASSETS_DIR, dist_dir / "assets", ignore=shutil.ignore_patterns(".DS_Store"))
    shutil.copy(STYLES_PATH, dist_dir / "styles.css")
    shutil.copy(CNAME_PATH, dist_dir / "CNAME")


def main():
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)
    copy_static(DIST_DIR)

    shell_tmpl = Template(load_text(TEMPLATES_DIR / "shell.html"))
    nav_html = load_text(TEMPLATES_DIR / "nav.html")
    aside_html = load_text(TEMPLATES_DIR / "aside.html")

    pub_groups = collect_publication_entries(BIB_PATH)

    pubs_tmpl = Template(load_text(CONTENT_DIR / "publications.html"))
    pubs_main = pubs_tmpl.substitute(
        pubs_article="".join(pub_groups["article"]),
        pubs_misc="".join(pub_groups["misc"]),
        pubs_unpublished="".join(pub_groups["unpublished"]),
    )
    pubs_page = render_page(shell_tmpl, nav_html, aside_html, "Publications — Samuel Ozminkowski", pubs_main)
    (DIST_DIR / "publications.html").write_text(pubs_page, encoding="utf-8")

    for filename, title in PAGES:
        main_html = load_text(CONTENT_DIR / filename)
        page_html = render_page(shell_tmpl, nav_html, aside_html, title, main_html)
        (DIST_DIR / filename).write_text(page_html, encoding="utf-8")

    total_pages = len(PAGES) + 1
    print(f"Built {total_pages} pages into {DIST_DIR}")
    print(
        "Publications: {article} article, {misc} misc, {unpublished} unpublished".format(
            article=len(pub_groups["article"]),
            misc=len(pub_groups["misc"]),
            unpublished=len(pub_groups["unpublished"]),
        )
    )


if __name__ == "__main__":
    main()
