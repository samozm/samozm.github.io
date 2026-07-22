# samozm.github.io

Source for my personal website. Content lives in plain HTML fragments and is
assembled into a static site by a small stdlib-only Python build script —
there's no Jekyll, no npm, no build tooling to install.

## Building locally

Requirements: Python 3 (no third-party packages — `build.py` only uses the
standard library).

```bash
python3 build.py
```

This deletes and regenerates `dist/`, the folder that gets deployed. To
preview it in a browser:

```bash
python3 -m http.server -d dist 8000
```

Then open `http://localhost:8000`.

`dist/` is gitignored — it's build output, not source. It's rebuilt from
scratch by GitHub Actions (`.github/workflows/deploy-pages.yml`) and pushed
to GitHub Pages whenever `build.py`, `content/`, `templates/`, `assets/`,
`styles.css`, or the workflow file itself change on `master` (or via a
manual "Run workflow" dispatch).

## What's in `dist/`

Everything in `dist/` is generated; don't edit it by hand, your changes will
be wiped out on the next build.

- `index.html`, `talks.html`, `software.html`, `honors.html`,
  `teaching.html`, `publications.html` — one rendered page per entry in the
  `PAGES` list in `build.py`, each produced by wrapping the matching file in
  `content/` with `templates/shell.html`.
- `styles.css` — copied verbatim from the top-level `styles.css`.
- `assets/` — copied verbatim from the top-level `assets/` (images, PDFs,
  `publications.bib`), minus `.DS_Store`.

## What's in `templates/`

These are the page "chrome" — the parts shared by every page. `build.py`
loads them with Python's `string.Template`, so `$name` placeholders inside
them get substituted with actual content.

- `shell.html` — the outer HTML document (`<head>`, `<body>`, footer). Has
  placeholders `$title`, `$nav`, `$aside`, and `$main`, filled in with the
  page title, `nav.html`, `aside.html`, and the page's `content/*.html` file,
  respectively.
- `nav.html` — the top navigation bar (About / Education / Publications /
  Talks & Posters / Software / Honors & Awards / Teaching / CV). Included
  as-is on every page.
- `aside.html` — the left sidebar (photo, name, affiliation, and contact
  links: email, GitHub, LinkedIn, Google Scholar, ORCiD). Included as-is on
  every page.

## Editing an existing page

Each page's body lives in `content/<page>.html` as a plain HTML fragment
(just the `<section>`s that go inside `<main>` — no `<head>`/`<body>`
boilerplate). Edit the fragment, then run `python3 build.py` and check the
result in `dist/`.

- `content/index.html` → `index.html` (About + Education)
- `content/talks.html` → `talks.html`
- `content/software.html` → `software.html`
- `content/honors.html` → `honors.html`
- `content/teaching.html` → `teaching.html`
- `content/publications.html` → `publications.html` — special-cased: this
  file contains `$pubs_article`, `$pubs_misc`, and `$pubs_unpublished`
  placeholders. `build.py` parses `assets/publications.bib` itself (a small
  hand-rolled BibTeX parser — no external bibtex library) and fills each
  placeholder with the rendered `<li>` entries for that BibTeX type
  (`article`, `misc`, `unpublished`). **To add/edit a publication, edit
  `assets/publications.bib`, not `content/publications.html`.**

To change the sidebar (photo, contact links) or top nav (links, CV),
edit `templates/aside.html` / `templates/nav.html` — those affect every
page. To change global look and feel, edit the top-level `styles.css`
(copied into `dist/styles.css` on every build, not edited directly).

## Adding a new page

1. Create `content/<newpage>.html` with just the body fragment, e.g.:

   ```html
       <section id="something">
         <div class="sec-head"><h2>Something</h2><div class="rule"></div></div>
         <p>...</p>
       </section>
   ```

2. Register it in `PAGES` in `build.py`:

   ```python
   PAGES = [
       ("index.html", "Samuel Ozminkowski"),
       ...
       ("newpage.html", "Something — Samuel Ozminkowski"),
   ]
   ```

   The first element is the output filename (used for both the
   `content/` source and the `dist/` output), the second is the `<title>`
   for that page.

3. Add a link to it in `templates/nav.html` so it's reachable from every
   page:

   ```html
   <a href="newpage.html#something">Something</a>
   ```

4. Run `python3 build.py` and confirm `dist/newpage.html` looks right.

If the new page needs its own generated content (like `publications.html`
does), follow that pattern: give the fragment `$placeholder` names, build a
`Template` for it in `main()`, `.substitute(...)` your data in, and render
it through `render_page()` — then add the page to the `PAGES` loop or handle
it separately, as `publications.html` is handled.
