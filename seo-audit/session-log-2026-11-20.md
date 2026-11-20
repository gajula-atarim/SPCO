# spco.ca SEO session log (20 Nov 2026), internal

Site: https://spco.ca · Atarim site `ba38265a-65d1-4625-b640-11c7844f3271` · workspace 48727 (Web Hosting Canada).
All work went through the Atarim WordPress bridge; this cloud session's network policy blocks spco.ca directly.

## Backups (outside web root)
- `/home/spcoca/spco-backup-2026-11-20-pre-seo.sql` (172 MB, complete dump)
- `/home/spcoca/spco-backup-2026-11-20-pre-seo-files.tar.gz` (/sitemap, /contactq, spco-child theme, robots.txt, .htaccess)
- Rendered HTML before: `/home/spcoca/seo-baseline-2026-11-20/`; after: `/home/spcoca/seo-after-2026-11-20/` (+ crawl.json)

## Re-verified premises (inherited findings)
- F-01/F-02/F-03 (noindex, nofollow, missing canonical): already fixed before work started. `blog_public` = 1. Not claimed.
- F-05 author page `/author/guzurebovi5293/`: 404 before work; the site was re-installed (DB prefix `iwp7690_`; an older `wpet_` table set is still in the DB).

## Changes made
1. robots.txt replaced (HestiaCP physical file): Disallow /wp-admin/, Allow admin-ajax, Sitemap line, no crawl delay.
2. Deleted `/sitemap/` (13 spam XML files, ~24 MB) and `/contactq/` (2022 spam generator, script already 0 bytes), after confirming they were in the archive.
3. Yoast: `noindex-client_resources` = true, which drops the CPT sitemap.
4. Child theme: `inc/spco-seo.php` (enqueue heading-preserve CSS; conditional dequeue of 5 UAE duplicate styles) required from functions.php; `spco-heading-preserve.css`. Copies in `seo-audit/site-changes/`.
5. Elementor tag edits (36) on posts 1697, 1698, 10, 16 and footer 1746 per the plan in the session; footer image sizes (QBO badge medium, logo medium_large).
6. Phone links: f35aec0 (post 16) and 0ea153a (post 1746) → `tel:+17057370983`.
7. Media alt text: 3682, 3674, 3673 (copied from the Elementor widget alt fields).
8. Timezone America/Toronto. Astra 4.14.2 → 4.14.3. Deleted themes twentytwentythree, twentytwentyfour.
9. LiteSpeed Cache installed (already active after install); all optimisations confirmed off; caches purged.

## Verification
- Offline render diff (Playwright, JS off, real CSS) at 1280/1000/800/600/390 px: identical apart from a 0.03 px sub-pixel difference and the footer logo box (+<1 px, image aspect ratio).
- Link, image and Elementor element counts identical on all 6 pages; 45/45 icons identical.
- page_audit fresh after; Lighthouse fresh before/after; crawl of 135 URLs; screenshots desktop/tablet/mobile.

## Mistakes / incidents
- Several execute-php calls hit Atarim's 15 s timeout (backups, page fetch, crawl). All completed server-side; the results were checked afterwards.
- First CSS pin attempt used px line-heights, which drift across Elementor breakpoints; switched to em. Links inside retagged H3 card titles inherited theme `h3 a` sizing; pinned with `inherit`. Both caught offline before going live.

## Concurrent changes NOT made by us
- Migrate Guru and WP Mail Logging removed, Elementor Pro updated to 4.4.1, WP_DEBUG turned off (between ~08:35 and 09:05 UTC).

## Open items
- Priority: submit the sitemap in GSC (Google not connected in Atarim); request removal of old spam URLs.
- Small fixes: disable author archives (`/author/spco/` live; offered, not chosen); Yoast org name "SPCO".
- Blocked on client: en-CA locale; confirm the concurrent changes.
- Out of scope: font loading (18 Montserrat styles + Roboto + Roboto Slab), WebP images, og:image on services/contact.
- Maintenance: test CPT posts and trash kept at the user's instruction; `/old/` legacy static site folder on the server.
- Ruled out, do not revisit: renaming the `client_resources` URL base (page is noindex and empty); linking resource titles to the empty single pages.

## Follow-up: favicon
- Built an SP monogram from the logo glyphs (white on #27477C), uploaded as attachment 3818, set `site_icon` = 3818, wrote `/favicon.ico` (16/32/48 px). Copies in `seo-audit/site-changes/`. Page audit no longer flags no_favicon; homepage score 95.24 → 98.17.

## Follow-up: www → non-www
- Prepended a RewriteCond/RewriteRule (www.spco.ca → https://spco.ca/$1, R=301) to .htaccess above the WordPress block; backup at /home/spcoca/htaccess-backup-2026-11-20-before-www-redirect.txt. Verified: www and http://www paths 301 with path and query kept; spco.ca pages 200.

## Follow-up: sitemap stylesheet
- Yoast 28.9 removed its sitemap stylesheet output ("removed temporarily"); its XSL is gone and Chromium has dropped XSLT. Added hook 3 to spco-child/inc/spco-seo.php: on sitemap URLs, inserts <?xml-stylesheet type="text/css" href="https://spco.ca/main-sitemap.css"?> (Yoast's own CSS) after the XML declaration, only when no stylesheet line exists. Server lint passed; backup /home/spcoca/spco-seo.php.bak-before-sitemap-css. Verified on sitemap_index.xml and page-sitemap.xml; homepage 200.
- Correction: the user's Chrome still supports XSLT (the test Chromium 157 does not). Added spco-child/main-sitemap.xsl (Yoast classic-style view, clickable links); the hook now outputs the XSL stylesheet first and /main-sitemap.css as fallback. Verified: .xsl 200 application/xml, both sitemaps carry both lines, homepage 200. Backup /home/spcoca/spco-seo.php.bak-before-sitemap-xsl.

## Follow-up: mobile speed fixes 1 and 2
- Hero: Elementor background_image_tablet = 2048x910, background_image_mobile = 1536x683 (post 1697, section dac02f0); homepage preload per breakpoint with fetchpriority=high (hook 4a). The hero has no motion effect (the background is set on the section by CSS), so nothing to disable.
- Fonts: elementor/frontend/print_google_fonts -> false, astra-google-fonts dequeued, one request for Montserrat 300-700, Rubik 300-700, Source Sans Pro 400 (hook 4b). Same woff2 files for all 8 used faces (0 mismatches); Roboto / Roboto Slab were unused.
- Verified: 200 on home/about/contact, link/img counts unchanged, phone screenshot identical. Backup /home/spcoca/spco-seo.php.bak-before-mobile-speed.
- Lighthouse cached: desktop 86 -> 91 (LCP 2.1 -> 1.5 s); mobile 71 -> 73-74 (LCP 8.8 -> 4.4-5.6 s). Remaining mobile cost: render-blocking local CSS (~1.5 s est, 36 Elementor/UAE stylesheets).

## Follow-up: client editing in parallel
- The client is editing the site through their own Claude session (this explains the plugin removals, Elementor Pro update and WP_DEBUG change).
- Integrity check after being told: robots.txt, www 301, sitemap stylesheet lines, functions.php include, main-sitemap.xsl (200) are all intact; server inc/spco-seo.php has the same sha1 as seo-audit/site-changes/spco-seo.php (b17a01e9…). No posts or pages changed since 09:15 UTC except the icon.
- Wrote seo-audit/handover-for-client-claude.md for the client's session.
