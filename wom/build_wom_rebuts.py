"""Build the SPCO Website Owner's Manual on the Rebuts WOM (.docx) template.
Every style, colour, font, border and page setting comes from the reference; only text and rows change.
Usage: python3 wom/build_wom_rebuts.py <rebuts-reference.docx> <out.docx>"""
import sys, copy, docx
from docx.oxml.ns import qn

ref, out = sys.argv[1:3]
d = docx.Document(ref)
P = list(d.paragraphs)      # body-level paragraphs, numbered as in the reference dump
T = list(d.tables)          # body-level tables T0..T36

def _set(el, text):
    runs = list(el.iter(qn('w:r')))
    if not runs:
        r = el.makeelement(qn('w:r'), {}); el.append(r); runs = [r]
    first = runs[0]
    for child in list(el):
        if child.tag in (qn('w:r'), qn('w:hyperlink')) and child is not first and not any(r is first for r in child.iter(qn('w:r'))):
            el.remove(child)
    par = first.getparent()
    if par is not el:
        for r in list(par):
            if r is not first and r.tag == qn('w:r'): par.remove(r)
    for t in list(first):
        if t.tag in (qn('w:t'), qn('w:tab'), qn('w:br')): first.remove(t)
    tt = first.makeelement(qn('w:t'), {}); tt.text = text
    tt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); first.append(tt)

def setp(i, text): _set(P[i]._p, text)
def delp(i): P[i]._p.getparent().remove(P[i]._p)

def bullets(first, last, items):
    """Replace reference paragraphs first..last (a list of same-styled items) with `items`."""
    els = [P[i]._p for i in range(first, last + 1)]
    while len(els) < len(items):
        n = copy.deepcopy(els[-1]); els[-1].addnext(n); els.append(n)
    for e in els[len(items):]: e.getparent().remove(e)
    for e, t in zip(els, items): _set(e, t)

def cell(tr, c, text):
    tcs = tr.findall(qn('w:tc'))
    ps = tcs[c].findall(qn('w:p'))
    _set(ps[0], text)
    for extra in ps[1:]: tcs[c].remove(extra)

def rows(t, data, start=1):
    tbl = T[t]._tbl
    body = tbl.findall(qn('w:tr'))[start:]
    while len(body) < len(data):
        n = copy.deepcopy(body[-1]); body[-1].addnext(n); body.append(n)
    for e in body[len(data):]: tbl.remove(e)
    for tr, row in zip(body, data):
        for j, v in enumerate(row): cell(tr, j, v)

def kv(t, values): rows(t, [[r.cells[0].text, v] for r, v in zip(T[t].rows, values)], start=0)

D = '2026 November 20'
WHC = 'Web Hosting Canada'
# ---------- Cover
kv(0, ['Strathdee Polley & Co (SPCO)', 'https://spco.ca', WHC, D, '-', D])
# ---------- 2. What we delivered
kv(2, ['SPCO — spco.ca live site launch',
       '5-page English WordPress site for Strathdee Polley & Co, built with Elementor Pro on an Astra child theme, with Ultimate Addons for Elementor header and footer templates, a Gravity Forms enquiry form, a Google reviews carousel, Yoast SEO and LiteSpeed page caching.',
       'Home, About, Services, Client Resources, Contact. One client resource page (2026 Intake and Checklist) is published but kept out of search results.',
       'Client', D, 'Tarun, Pujitha , Web Hosting Canada , ' + D])
bullets(40, 46, [
    'Design and build of the 5 pages listed above',
    'Mobile and tablet layouts compared element by element at 1280, 1000, 800, 600 and 390 px on ' + D + ' — no layout change and no horizontal scroll at any width',
    'Enquiry form on the Contact page, with email notifications to info@spco.ca, tested on ' + D + '. Every submission is also stored in WordPress under Forms → Entries.',
    'On-page SEO: unique titles and meta descriptions on all 5 pages, heading levels in order on every page, XML sitemap generated and declared in robots.txt, and 13 spam sitemap files left by a 2022 hack removed',
    'Alt text on every rendered image, and a site icon for browser tabs, bookmarks and phone home screens',
    'All plugins and the active theme updated to their current versions; unused default themes removed',
    'Desktop performance 91 against a 90+ target, and a Lighthouse SEO score of 100',
])
bullets(49, 56, [
    'Ongoing content writing or blog posts',
    'Ongoing SEO campaign work',
    'Paid advertising setup or management',
    'Email hosting migration',
    'Google Search Console and Google Analytics setup — both need the owner’s own Google account',
    'Website backup schedule — not configured at launch, see Section 8',
    'Privacy policy and terms pages — none is published at launch, see Section 11',
    'Ongoing maintenance — see Section 16',
])
# ---------- 3. Access and ownership
rows(3, [
    ['Domain name — spco.ca', 'WHC Online Solutions Inc. (whc.ca)', 'Client', 'Client, Web Hosting Canada'],
    ['Web hosting', 'Web Hosting Canada (whc.ca)', 'Client', 'Client, Web Hosting Canada'],
    ['WordPress admin', 'https://spco.ca/wp-admin', 'Administrator — see Section 9', 'Client, Web Hosting Canada'],
    ['Email', 'Web Hosting Canada — mail server mx.spco.ca', 'Client', 'Client'],
    ['Google Analytics', 'Google', 'Client need to setup', '—'],
    ['Google Search Console', 'Google', 'Client — a Google verification file is already on the server', 'Client to confirm the property and submit the sitemap'],
    ['Google Business Profile', 'Google', '-', 'Client to claim and set up'],
    ['Premium plugin licences', 'Elementor Pro, Gravity Forms', 'Client', 'Client'],
    ['DNS management', 'Web Hosting Canada (ns1.whc.ca, ns2.whc.ca, ns3.whc.ca)', 'Client', 'Client, Web Hosting Canada'],
])
kv(4, ['Sent to you separately. Avoid usernames that match your business name or a public staff name.',
       'The site owner account (spco) uses the firm’s own email address, info@spco.ca, and the password was sent separately',
       'Not enabled on WordPress admin accounts',
       'Use the “Lost your password?” link on the login screen.'])
# ---------- 4. Technical details
kv(6, ['https://spco.ca', 'https://spco.ca/wp-admin', '-',
       'HestiaCP, or through the WHC Client Area at https://clients.whc.ca', 'https://spco.ca/sitemap_index.xml'])
kv(7, ['WordPress 7.1.5', 'English (en-US)', 'Astra 4.14.3 (child theme: Yes — Astra Child 02, folder spco-child)',
       'Elementor 4.4.1 with Elementor Pro 4.4.1 and Ultimate Addons for Elementor (UAE) 2.9.8',
       'Gravity Forms 3.2.3.1 — one enquiry form', 'MariaDB 10.11.19', '8.4.28', 'See Appendix B'])
rows(7, [[r.cells[0].text, r.cells[1].text] for r in T[7].rows][:4] + [['Forms', 'Gravity Forms 3.2.3.1 — one enquiry form'], ['Database', 'MariaDB 10.11.19'], ['PHP version', '8.4.28'], ['Full plugin list', 'See Appendix B']], start=0)
kv(8, ['Web Hosting Canada — https://www.whc.ca', 'Canada', '198.50.215.64 (srv5.swhc.ca)',
       'LiteSpeed, managed through HestiaCP', 'https://www.whc.ca/contact-us , client area: https://clients.whc.ca'])
kv(9, ['LiteSpeed Cache 7.9.3 — page cache only. CSS/JS minification, combine and the other optimisations were deliberately left off, because those are the settings that break builder layouts.',
       'Let’s Encrypt wildcard for *.spco.ca — expires 2026 December 25, auto-renew Yes'])
setp(73, 'Held back at the time of writing: none. Every plugin and theme was on its current version on ' + D + '.')
# ---------- 5. Domain, DNS and email
rows(10, [
    ['DNS', WHC, 'The phone book that points your domain at the right servers. See Appendix A for your records.'],
    ['Web hosting', WHC, 'The server your website files and database sit on.'],
    ['Email', WHC, 'Mail for spco.ca is handled by Web Hosting Canada on mx.spco.ca.'],
])
rows(11, [['spco.ca', 'WHC Online Solutions Inc.', '2026 November 27', 'ns1.whc.ca, ns2.whc.ca, ns3.whc.ca']])
rows(12, [['info@spco.ca', 'Mailbox', 'The WordPress administration address, the sender address and the recipient for enquiry form notifications.']])
setp(80, 'Three DNS records decide whether your email lands in an inbox or a spam folder. They also stop other people sending email that pretends to be you. These apply to spco.ca.')
rows(13, [
    ['SPF', 'Lists the servers allowed to send email as your domain.', 'Configured — v=spf1 +a +mx +ip4:148.113.170.105 include:spf.web-dns1.com +ip4:198.50.215.64 +ip4:54.39.101.30 +ip4:158.69.26.68 ~all'],
    ['DKIM', 'Signs your outgoing mail so a receiving server can prove it was not altered.', 'Configured — published on the default selector'],
    ['DMARC', 'Tells receiving servers what to do with mail that fails SPF or DKIM.', 'Configured — p=none, with no reporting address set'],
])
kv(14, ['The WordPress administration email (Settings → General) — info@spco.ca',
        'WP Mail SMTP 4.10.4, using the server’s own mail function. No email log is installed.',
        'info@spco.ca, set on the Gravity Forms Enquiry form notification'])
# ---------- 6. Renewals
rows(15, [
    ['Domain — spco.ca', 'WHC Online Solutions Inc.', '-', 'Annual', '2026 November 27', 'Client'],
    ['Web hosting', WHC, '-', '-', '-', 'Client'],
    ['SSL certificate', 'Let’s Encrypt', 'Free', 'Auto', '2026 December 25', 'n/a'],
    ['Elementor Pro licence', 'Elementor.com', '-', 'Annual', '-', 'Client'],
    ['Gravity Forms licence', 'Rocketgenius (gravityforms.com)', '-', 'Annual', '-', 'Client'],
    ['Care plan', 'None', 'n/a', 'n/a', 'n/a', 'n/a'],
])
# ---------- 7. Premium software
rows(16, [
    ['Elementor Pro', '4.4.1', 'Builds the page layouts with the Pro widgets.', 'Without it the Pro widgets used across the site stop updating.'],
    ['Gravity Forms', '3.2.3.1', 'Runs the enquiry form on the Contact page and stores every submission.', 'Without an active licence the form stops receiving updates, including security fixes.'],
])
# ---------- 8. Backups
kv(17, ['Files and database', 'No backup plugin is installed — host-level backups at Web Hosting Canada, to be confirmed',
        'Not configured — to be confirmed with Web Hosting Canada',
        'A one-off full backup (database and key files) was taken on ' + D + ' and is stored on the server, outside the website folder'])
# ---------- 9. Security
rows(19, [['spco', 'Administrator', 'info@spco.ca', '2026 November 6'],
          ['design', 'Administrator', 'service@pro.whc.ca', D]])
# ---------- 10. Search, analytics and tracking
rows(20, [
    ['Search engine indexing enabled', 'Confirmed — 5 of 5 public pages', D],
    ['XML sitemap generated and declared in robots.txt', 'Confirmed — 1 sitemap index, declared by absolute URL, readable with clickable links', D],
    ['XML sitemap submitted to Google', 'Owner — needs the client’s Search Console account', D],
    ['robots.txt reviewed', 'Confirmed — rewritten, Crawl-delay: 10 removed, original backed up', D],
    ['Redirects from the old website mapped and tested', 'n/a — page addresses unchanged', D],
    ['Page titles and meta descriptions set on all pages', 'Confirmed — 5 of 5', D],
    ['Broken links, images and empty URLs checked', 'Confirmed — 135 links and images checked, 0 broken', D],
    ['Analytics tracking verified as recording', 'Not connected — client to set up GA4', D],
])
kv(21, ['Not connected — no GA4 or Tag Manager tag found on the site',
        'Verification file on the server (googlec483ecf891827b1e.html) — client to confirm the property and submit the sitemap',
        'Not connected — client to create the container', 'Yoast SEO 28.9', 'https://spco.ca/sitemap_index.xml',
        'WebPage, WebSite and Organization, published on every page by Yoast'])
setp(109, 'Recorded so that future changes can be measured against a known starting point. Every figure was measured on the live site on ' + D + '.')
rows(22, [
    ['Lighthouse performance (desktop)', '91', '84', '90+'],
    ['Lighthouse performance (mobile)', '74', '67', '90+'],
    ['Lighthouse SEO (mobile)', '100', '100', '90+'],
    ['Lighthouse accessibility (mobile)', '100', '98', '90+'],
    ['Lighthouse best practices', '96', '96', '90+'],
    ['First Contentful Paint (desktop)', '1.3 s', '1.2 s', 'under 1.8 s'],
    ['First Contentful Paint (mobile)', '3.0 s', '2.7 s', 'under 1.8 s'],
    ['Largest Contentful Paint (desktop)', '1.5 s', '2.1 s', 'under 2.5 s'],
    ['Largest Contentful Paint (mobile)', '5.6 s', '9.3 s', 'under 2.5 s'],
    ['Speed Index (desktop)', '1.3 s', '2.0 s', 'under 3.4 s'],
    ['Total Blocking Time (mobile)', '30 ms', '30 ms', 'under 200 ms'],
    ['Cumulative Layout Shift (mobile)', '0.005', '0.007', 'under 0.1'],
    ['Home page server response', '6 ms (cached)', '1.21 s', 'as low as possible'],
    ['Pages with a title and meta description', '5 of 5', '5 of 5', '5 of 5'],
    ['Pages with skipped heading levels', '0 of 6', '7 of 7', '0'],
    ['Pages with an og:image', '3 of 5', '3 of 5', '5 of 5'],
    ['Pages returning HTTP 200', '5 of 5', '5 of 5', '5 of 5'],
    ['Images without alt text, all pages', '0', '3', '0'],
    ['Pages with horizontal scroll (1280 / 1000 / 800 / 600 / 390 px)', '0', '0', '0'],
    ['PHP errors in page HTML', '0', '0', '0'],
])
setp(110, 'Mobile performance is the one measure still short of the 90+ target, at 74. The limit is Largest Contentful Paint at 5.6 s, held back by about 1.5 s of stylesheets that Elementor and its add-ons load before the page can draw. Reducing them changes how the page builder loads its styles, so it needs a separate, visually checked pass.')
# ---------- 11. Legal
rows(23, [
    ['Privacy policy', 'Not published', 'Required when you collect personal information — the enquiry form collects names, email addresses and phone numbers.'],
    ['Cookie / tracking consent', 'Not required at present', 'No analytics, advertising or tracking cookies are set by the site itself.'],
    ['Business details displayed', 'Yes', 'Firm name, address (149 Welham Rd Unit 16, Barrie ON L4N 8Y3), telephone ((705) 737-0983) and email (info@spco.ca) are shown in the footer of every page.'],
    ['Copyright notice', 'Not present', 'There is no copyright line in the footer.'],
    ['Site language', 'English', 'Pages declare en-US. en-CA would match a Canadian firm; it changes one setting site-wide.'],
])
# ---------- 12. Using your website
setp(115, 'Go to https://spco.ca/wp-admin')
rows(24, [
    ['Edit text or an image on a page', 'Pages → hover the page → Edit with Elementor → click the element → edit → Update'],
    ['Edit the header or footer', 'The header and footer are Ultimate Addons for Elementor templates shared by every page. Open the template with Edit with Elementor; a change shows on all pages.'],
    ['Change a menu item', 'Appearance → Menus'],
    ['See enquiry form submissions', 'Forms → Entries → Enquiry. Notifications are also emailed to info@spco.ca.'],
    ['Change who form emails go to', 'Forms → Enquiry → Settings → Notifications. It currently sends to the WordPress administration email.'],
    ['Update a client resource or PDF', 'Pages → Client Resources → Edit with Elementor → replace the link or file'],
    ['Add a user', 'Users → Add New → choose the lowest suitable role'],
    ['Remove a user', 'Users → hover → Delete → attribute their content to another user'],
    ['Update your own password', 'Users → Profile'],
    ['Clear the cache after a change', 'LiteSpeed Cache → Toolbox → Purge All, if an edit does not appear straight away'],
])
bullets(122, 128, [
    'Deactivate or delete plugins without asking — several of them hold the site together, and Elementor Pro and Ultimate Addons hold the header and footer.',
    'Switch or update the theme. It will undo the design. The customisations live in the spco-child theme, including the stylesheet that keeps headings looking as designed.',
    'Edit theme or plugin files through Appearance → Theme File Editor.',
    'Turn on CSS/JS minify, combine or the other optimisations in LiteSpeed Cache. Those settings break Elementor layouts, which is why they are off.',
    'Install plugins found through a web search, or “nulled” paid plugins offered free. This is the most common way a small business website gets infected.',
    'Change the Site Address or WordPress Address under Settings → General. It will lock you out.',
    'Delete pages that look empty — the three draft service pages (Accounting Services, Tax Services, Financial Advisory) are kept on purpose.',
])
# ---------- 13. Maintenance schedule
rows(26, [
    ['Plugin, theme and core updates', 'Most WordPress compromises exploit a vulnerability that had already been patched.'],
    ['Malware scan', 'Detects injected files and modified core files.'],
    ['Visual inspection of key pages', 'Automated updates occasionally break a layout. A person has to look.'],
    ['Enquiry form test', 'Confirms enquiries are still arriving by email.'],
])
rows(27, [
    ['Review traffic and search rankings', 'Shows whether the website is doing its job.'],
    ['Check Search Console for errors', 'Surfaces indexing and crawl problems early.'],
    ['Review content for accuracy', 'Out-of-date services, hours and staff details lose you clients.'],
    ['Database cleanup', 'Removes revision bloat and keeps the site quick.'],
    ['Page speed test', 'Catches gradual slowdown. Compare against the baseline in Section 10.'],
    ['Broken link scan', 'Dead links frustrate visitors and hurt search performance.'],
    ['Review user accounts', 'Removes access that is no longer needed.'],
])
rows(28, [
    ['Test a backup restore', 'An untested backup is only a hope.'],
    ['Review plugin list', 'Remove anything unused; replace anything abandoned by its developer.'],
    ['Check PHP version', 'Unsupported PHP versions stop receiving security fixes.'],
    ['Check premium licences', 'Elementor Pro and Gravity Forms stop updating when a licence lapses.'],
])
# ---------- 15. Support
setp(141, 'The page address where you saw the problem')
rows(31, [
    ['Critical', 'Website offline or compromised.', '2 hours', 'Extended'],
    ['High', 'A key function broken — the enquiry form, a main page.', '1 business day', 'Business'],
    ['Normal', 'Something not working as expected, with a workaround.', '2 business days', 'Business'],
    ['Low', 'Content changes, questions, small improvements.', '3–5 business days', 'Business'],
])
setp(149, 'For 30 days after launch — to 2026 December 20 — we fix, at no charge, anything that does not work as it was specified and approved. New requests, additional pages and changes of mind sit outside the warranty and are quoted separately.')
# ---------- 18. Troubleshooting
setp(161, 'Either the email address on your user account is wrong, or the website is not able to send email at all. Both need your Technical support contact — see Section 5 for how your website sends email.')
setp(164, 'This is usually a conflict introduced by a recent update. Note exactly what you were doing, on which page, and roughly when it last worked, then contact your Technical support contact. Resist the urge to start changing settings — it makes the cause harder to find.')
setp(165, 'Enquiry notifications are not arriving.')
setp(166, 'Check Forms → Entries first: if the enquiry is listed, the form worked and only the email failed. Then check the spam folder of info@spco.ca. The site keeps no email log, so a test submission is the quickest check. Test the form yourself once a month — failures are silent.')
setp(167, 'The header or footer looks wrong on every page.')
setp(168, 'The header and footer are shared Ultimate Addons for Elementor templates, so one change shows everywhere. Contact your Technical support contact rather than editing the template under time pressure.')
setp(185, 'Email is a separate service from your website, so the website being fine tells you nothing about email. Check whether the mailbox is full, then contact Web Hosting Canada.')
setp(187, 'SPF, DKIM and DMARC are all configured on spco.ca (Section 5), but DMARC is set to p=none, which only monitors. If the problem persists, consider a dedicated email provider such as Google Workspace or Microsoft 365.')
setp(192, 'Check it against Section 6. “Domain slamming” notices are designed to look like renewal invoices from your real registrar but transfer your domain elsewhere, usually at several times the price. If it is not on the list in Section 6, do not pay it — send it to us.')
# ---------- 19. Glossary
gl = {
 'Theme': 'Controls how your website looks. Yours is Astra, with a child theme named Astra Child 02 (spco-child).',
 'Plugin': 'An add-on that gives WordPress extra abilities — forms, SEO, caching, reviews.',
 'Registrar': 'The company you license your domain from. spco.ca is with WHC Online Solutions.',
}
glossary = []
for r in T[34].rows[1:]:
    k, v = r.cells[0].text, r.cells[1].text
    if k == 'WPML': k, v = 'Gravity Forms', 'The plugin that runs your enquiry form and stores every submission.'
    elif k == 'hreflang': k, v = 'Header and footer templates', 'Layouts shared by every page, built with Ultimate Addons for Elementor.'
    else: v = gl.get(k, v)
    glossary.append([k, v])
rows(34, glossary)
# ---------- Appendix A
setp(195, 'Your DNS records for spco.ca as at ' + D + '. Changing these incorrectly will take down your website, your email, or both. Always keep a copy of the current records before making a change.')
rows(35, [
    ['A', '@', '198.50.215.64', '3600'],
    ['CNAME', 'www', 'spco.ca.', '3600'],
    ['NS', '@', 'ns1.whc.ca.', '3600'],
    ['NS', '@', 'ns2.whc.ca.', '3600'],
    ['NS', '@', 'ns3.whc.ca.', '3600'],
    ['MX', '@', '0 mx.spco.ca.', '3600'],
    ['TXT', '@', 'v=spf1 +a +mx +ip4:148.113.170.105 include:spf.web-dns1.com +ip4:198.50.215.64 +ip4:54.39.101.30 +ip4:158.69.26.68 ~all', '3600'],
    ['TXT', 'default._domainkey', 'v=DKIM1; k=rsa; p=… (2048-bit key published)', '3600'],
    ['TXT', '_dmarc', 'v=DMARC1; p=none;', '3600'],
])
delp(196)
# ---------- Appendix B
setp(198, 'Everything installed at launch, on ' + D + '. Keep this current — an unexplained plugin appearing here is worth investigating.')
rows(36, [
    ['Elementor', '4.4.1', 'Page builder', 'Free'],
    ['Elementor Pro', '4.4.1', 'Pro widgets used across the page layouts', 'Paid'],
    ['Ultimate Addons for Elementor (UAE)', '2.9.8', 'Elementor header and footer templates', 'Free'],
    ['Gravity Forms', '3.2.3.1', 'Enquiry form and stored submissions', 'Paid'],
    ['Advanced Custom Fields', '6.8.12', 'Custom fields for the client resources', 'Free'],
    ['Widgets for Google Reviews', '15.0', 'Google reviews carousel', 'Free'],
    ['Yoast SEO', '28.9', 'SEO titles, meta descriptions, structured data and XML sitemap', 'Free'],
    ['LiteSpeed Cache', '7.9.3', 'Page caching', 'Free'],
    ['WP Mail SMTP', '4.10.4', 'Outgoing email delivery', 'Free'],
    ['Atarim', '5.2.0', 'Site management connection used by Web Hosting Canada', 'Free'],
    ['Astra (parent theme)', '4.14.3', 'Base theme', 'Free'],
    ['Astra Child 02 — active theme', '4.13.0', 'Child theme holding site customisations, including the heading styles and the sitemap stylesheet', 'Free'],
])
d.save(out)
print('saved', out)
