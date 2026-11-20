# WHC report style

The house style for every client SEO report from this repo (baselines, results, audits).
It matches the WHC "SEO Foundations" PDF reports (reference: RSLL, 3 November 2026).

## Files

| File | Purpose |
|---|---|
| `whc-report.css` | All colours, fonts and components. Single light theme by design. |
| `whc-logo.png` | Web Hosting Canada logo, transparent background. |
| `build.py` | Inlines the CSS and logo into a report source file. |
| `pdf.js` | Renders a built report to a print-ready A4 PDF with page numbers. |

## Making a report

1. Copy `seo-audit/spco-seo-audit.src.html` as the starting point.
2. Keep `<!--WHC:CSS-->` in the head and `src="WHC_LOGO_SRC"` on the logo.
3. Build: `python3 reports/whc-brand/build.py path/report.src.html path/report.html`
4. Publish the built `.html` as an artifact. Commit both files.
5. PDF: `node reports/whc-brand/pdf.js path/report.html path/report.pdf "Web Hosting Canada · site · date"`.
   A4, 14 mm margins, page-numbered footer. Headings stay with the block after them, small blocks never split,
   long tables break only between rows with the header repeated. Check the page thumbnails before sending.

## Look

- **Fonts:** Inter 400/700/800 for text and headings; IBM Plex Mono 400/500 for labels, captions and figures.
- **Colours:** ink `#1a1f2e`, body `#363d4d`, muted `#6b707c`, navy accent `#1f3a5c`,
  green `#0b8a55` (fixed / after), red `#a3343d` (baseline problems / critical),
  ochre `#8a6414` (worth knowing / medium), table fill `#f6f7f9`, borders `#e5e6e8`.
  Logo red `#c32127` is used only for the short rule under the logo.
- **Header:** logo, a mono chip naming the report type, site and date top right, navy rule with a red tick.
- **Status strip:** one bordered mono line of the headline counts, with a dot (green for results, red for a baseline with critical issues).
- **Title:** `site.tld` in ink + report name in navy, Inter 800.
- **Sections:** mono label `—— 01 — Section name`, then a bold one-sentence heading ending in a full stop that states the finding.
- **Components:** big-number cards (navy top rule) in two columns; category cards with status pills;
  tables with a mono caption row and a left rail per row (`tr.flag` ochre, `tr.crit` red);
  callouts with a coloured left border (`.co`, `.co.ochre`, `.co.red`, `.co.navy`);
  finding blocks (`.f`) with ref, title, pill and a status / affected / impact / action grid.
- **Pills:** `p-good` Fixed/Healthy, `p-crit`/`p-high` red, `p-med` ochre, `p-low` navy, `p-gap` No data.

## Report types

- **Baseline audit** (before work): chip "SEO baseline audit · before any change", red strip dot, findings F-01…, a baseline table with an empty "Now" column.
- **Results report** (after work): chip "SEO after report · fixes delivered", green strip dot, Before / After columns with after values in green and baseline values in red.
