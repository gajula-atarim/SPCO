# spco.ca: changes made on 20 Nov 2026 (please keep)

For anyone else editing spco.ca, including another Claude session. These changes fix SEO and speed problems on the live site. Please don't revert or overwrite them, and check before editing the files listed.

## Files that must stay
| Where | What it does |
|---|---|
| `wp-content/themes/spco-child/functions.php` (last 4 lines) | Loads `inc/spco-seo.php`. Keep the lines if you edit functions.php. |
| `wp-content/themes/spco-child/inc/spco-seo.php` | Heading styles, removal of duplicate CSS, sitemap stylesheet, hero image preload, single Google Fonts request. |
| `wp-content/themes/spco-child/spco-heading-preserve.css` | Keeps headings looking the same after their tags were corrected (H1/H2/H3 order). |
| `wp-content/themes/spco-child/main-sitemap.xsl` | Readable sitemap with clickable links. |
| `robots.txt` (site root, physical file) | Blocks /wp-admin/, points to `https://spco.ca/sitemap_index.xml`. |
| `.htaccess`, block `# BEGIN SPCO www to non-www` | 301 from www.spco.ca to spco.ca. Keep it above the WordPress block. |
| `/favicon.ico` and Site Icon (media 3818) | Favicon and site icon. |

## Settings that must stay
- Yoast: Client Resources set to noindex (`noindex-client_resources`).
- LiteSpeed Cache: page cache on. CSS/JS/image optimisations are off on purpose; turn them on only after testing the layout.
- Timezone: America/Toronto.
- Elementor, home page section `dac02f0`: tablet and mobile background images use the smaller 2048px and 1536px files.
- Elementor heading tags on Home, About, Services, Contact and the footer were changed to fix heading order. If a heading tag is changed back, its look stays the same but the SEO fix is lost.
- Phone links use `tel:+17057370983`.

## Before you edit
- Save the theme before replacing the child theme or functions.php. Re-adding the include line is enough to restore everything.
- Purge LiteSpeed Cache after edits.
- Backups from before the work are in `/home/spcoca/` (outside the web root): the database dump and the files archive from 20 Nov 2026.
