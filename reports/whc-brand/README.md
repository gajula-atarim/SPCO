# WHC report style

The house style for every client SEO report from this repo (baselines, results, audits).
It matches the WHC "SEO Foundation" PDF reports (reference: Rebuts, 10 November 2026; earlier RSLL, 3 November 2026).

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
5. PDF: `node reports/whc-brand/pdf.js path/report.html path/report.pdf none` (Rebuts style, no page footer;
   pass a label instead of `none` for a page-numbered footer). A4, 14 mm margins. Headings stay with the block after them, small blocks never split,
   long tables break only between rows with the header repeated. Check the page thumbnails before sending.

## Look

- **Fonts:** Inter 400/700/800 for text and headings; IBM Plex Mono 400/500 for labels, data and the footer.
- **Colours:** ink `#1a1f2e`, body `#363d4d`, muted `#6b707c`, green `#0b8a55` (after values, Fixed), navy `#1f3a5c` (Healthy),
  grey fill `#f6f7f9`, borders `#e5e6e8`. WHC red `#c32127` only for the report-type line under the logo.
- **Header:** WHC logo with the report type under it in red mono (left); site in bold, "Prepared by Web Hosting Canada",
  date "2026 November 20 · verified live" (right, mono).
- **Title:** "`Client` SEO results" in ink, Inter 800, with a mono subtitle (site · pages in scope).
- **Status strip:** grey box, one mono line of the headline counts. Then a one-paragraph lede.
- **Sections 01–15:** mono label `01 — Executive summary`, then a bold one-sentence heading ending in a full stop.
  Order: 01 Executive summary (+4 stat cards, then "-- — Delivered and verified / What changed in this round" bullets),
  02 Website SEO health overview (4-across cards, ● Fixed green / ● Healthy navy), 03 Key improvements,
  04 Technical SEO audit (Lighthouse table + "Core metrics"), 05 Crawlability & indexability, 06 On-page SEO analysis,
  07 Metadata, 08 Heading structure, 09 URL & canonical, 10 Redirects & HTTP status codes, 11 Internal linking,
  12 Image SEO, 13 Duplicate & thin content, 14 Issues resolved, 15 Baseline vs. now.
- **Tables:** grey mono header, light row rules, numbers centred, after values bold green. No captions.
- **Footer:** rule, then one mono paragraph: "**site — SEO after report.** Prepared by Web Hosting Canada, date. Pages in scope.
  Every figure was measured on the live site; none is estimated or projected. …"
- **Leave out:** timestamps, process narrative ("how the look was kept", how the site was protected), recommendations
  sections, open/partly/not-needed rows, operational items that are not SEO (timezone, theme clean-up).

## Report types

- **Baseline audit** (before work): chip "SEO baseline audit · before any change", findings F-01…, a baseline table with an empty "Now" column.
- **Results report** (after work): chip "SEO after report · fixes delivered", the 15 sections above.
