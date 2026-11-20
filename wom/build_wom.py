"""Build the SPCO Website Owner's Manual from the RSLL reference .docx (used as the template).
Only text and table rows change; every style, colour, border and page setting comes from the reference.
Usage: python3 wom/build_wom.py <reference.docx> <out.docx>"""
import sys, copy, docx
from docx.oxml.ns import qn

ref, out = sys.argv[1:3]
d = docx.Document(ref)
P = d.paragraphs           # body-level paragraphs, same order as the reference dump
T = d.tables               # body-level tables (T0..T33)

def set_par(p, text):
    el = p._p if hasattr(p, '_p') else p
    runs = list(el.iter(qn('w:r')))
    if not runs:
        p.add_run(text); return
    first = runs[0]
    # keep the first run (and its formatting); drop every other run / hyperlink
    for child in list(el):
        if child.tag in (qn('w:r'), qn('w:hyperlink')) and child is not first and not any(r is first for r in child.iter(qn('w:r'))):
            el.remove(child)
    hl = first.getparent()
    if hl.tag == qn('w:hyperlink'):
        for r in list(hl):
            if r is not first and r.tag == qn('w:r'): hl.remove(r)
    for t in list(first):
        if t.tag in (qn('w:t'), qn('w:tab'), qn('w:br')): first.remove(t)
    tt = first.makeelement(qn('w:t'), {}); tt.text = text
    tt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); first.append(tt)

def cell(t, r, c, text):
    ce = T[t].rows[r].cells[c]
    ps = ce.paragraphs
    set_par(ps[0], text)
    for extra in ps[1:]:
        extra._p.getparent().remove(extra._p)

def rows(t, data, start=1):
    """Fill table t from row `start` with data (list of lists); add or delete rows to fit."""
    tbl = T[t]._tbl
    trs = tbl.findall(qn('w:tr'))
    body = trs[start:]
    while len(body) < len(data):
        new = copy.deepcopy(body[-1]); body[-1].addnext(new); body.append(new)
    for extra in body[len(data):]:
        tbl.remove(extra)
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            cell(t, start + i, j, v)

def kv(t, values):
    for i, v in enumerate(values):
        cell(t, i, 1, v)

L = '20 November 2026'
# ---- Cover
kv(0, ['Strathdee Polley & Co', 'https://spco.ca', 'Web Hosting Canada (WHC) — https://whc.ca', L, 'Launch only', L])
# ---- 2. What we delivered
kv(1, ['SPCO — spco.ca live site launch',
       '5-page English WordPress site built with Elementor Pro on an Astra child theme, Ultimate Addons header and footer, one Gravity Forms enquiry form, a Google Reviews widget, Yoast SEO and LiteSpeed page caching',
       'Home, About, Services, Client Resources, Contact, plus one client resource page (2026 Intake and Checklist), kept out of search results.',
       'Client', L, 'Verified by Tarun and Pujitha (WHC), 20 November 2026'])
set_par(P[26], 'Design and build of the 5 pages listed above')
set_par(P[27], 'Mobile and tablet layouts, verified across devices on 20 November 2026')
set_par(P[28], 'One Gravity Forms enquiry form with email notifications to info@spco.ca')
set_par(P[29], 'SSL certificate installed and HTTPS enforced; www.spco.ca redirects to spco.ca')
set_par(P[30], 'On-page SEO: unique titles and meta descriptions on all 5 indexable pages, XML sitemap generated and declared in robots.txt')
set_par(P[31], 'Google Search Console verification file on the server — Google Analytics not connected')
# ---- 3. Access and ownership
rows(2, [
    ['Domain name', 'Web Hosting Canada (whc.ca)', 'Client, whc.ca', 'Client, whc.ca'],
    ['Web hosting', 'Web Hosting Canada (whc.ca)', 'Client, whc.ca', 'Client, whc.ca'],
    ['WordPress admin', 'https://spco.ca/wp-admin', 'Two administrator accounts', 'Client, whc.ca'],
    ['Email hosting', 'Web Hosting Canada (MX: mx.spco.ca)', 'info@spco.ca', 'Client, whc.ca'],
    ['Google Analytics', 'Google', 'Not connected', '-'],
    ['Google Search Console', 'Google', 'Verification file on the server (googlec483ecf891827b1e.html)', 'Client need to confirm the property and submit the sitemap'],
    ['Google Business Profile', 'Google', 'not checked against the site', 'Client need to confirm the Google Business Profile'],
    ['Premium plugin licences', 'See Section 7', 'To be confirmed', 'Client'],
    ['DNS management', 'Web Hosting Canada (ns1 / ns2 / ns3.whc.ca)', '-', 'Client'],
])
# ---- 4. Technical details
kv(4, ['https://spco.ca', 'https://spco.ca/wp-admin', 'None', 'HestiaCP via Web Hosting Canada — https://my.whc.ca', 'https://spco.ca/sitemap_index.xml'])
kv(5, ['WordPress 7.1.5', 'Astra 4.14.3 (child theme: Yes — Astra Child 02, spco-child)',
       'Elementor 4.4.1 with Elementor Pro 4.4.1 and Ultimate Addons for Elementor (UAE) 2.9.8',
       '8.4.28', 'MariaDB 10.11.19', 'See Appendix B'])
kv(6, ['Web Hosting Canada (WHC) — https://whc.ca', '-', 'Canada', '198.50.215.64', 'https://whc.ca / client area: my.whc.ca'])
kv(7, ['LiteSpeed Cache 7.9.3 on a LiteSpeed server (page caching only)', 'None', "Let's Encrypt   expires 25 December 2026, auto-renew Yes"])
# ---- 5. Domain, DNS and email
rows(8, [
    ['DNS', 'Web Hosting Canada', 'The phone book that points your domain at the right servers. See Appendix A for your records.'],
    ['Web hosting', 'whc.ca', 'The server your website files and database sit on.'],
    ['Email hosting', 'Web Hosting Canada (MX: mx.spco.ca)', 'The service that sends and receives your mail. Often, but not always, the same company as your web host.'],
])
kv(9, ['spco.ca', 'To be confirmed with WHC', '-', 'n/a', 'ns1.whc.ca, ns2.whc.ca, ns3.whc.ca'])
rows(10, [
    ['info@spco.ca', 'Mailbox', 'WordPress administration email, form notification and sender address'],
    ['service@pro.whc.ca', 'WHC address', 'WHC administrator account on the website'],
])
rows(11, [
    ['SPF', 'Lists the servers allowed to send email as your domain.', 'Configured'],
    ['DKIM', 'Cryptographically signs your outgoing email so it can be verified.', 'Configured'],
    ['DMARC', 'Tells receiving servers what to do with email that fails SPF or DKIM, and reports attempted spoofing.', 'Configured — p=none, with no reporting address set'],
])
kv(12, ['Server default (PHP mail) — WP Mail SMTP 4.10.4 is installed', 'info@spco.ca',
        'info@spco.ca (Enquiry form)', L])
# ---- 6. Renewals and costs
rows(13, [
    ['Domain name', 'Web Hosting Canada', 'To be confirmed with WHC', 'Annual', 'To be confirmed with WHC', 'Client'],
    ['Web hosting', 'Web Hosting Canada', 'To be confirmed with WHC', 'Annual', 'To be confirmed with WHC', 'Client'],
    ['Email hosting', 'Web Hosting Canada', 'Included with hosting', 'Annual', 'With hosting', 'Client'],
    ['SSL certificate', "Let's Encrypt", 'Auto', 'Auto', 'Auto', 'n/a'],
    ['Elementor Pro', 'Elementor', 'To be confirmed', 'Annual', 'To be confirmed', 'Client'],
    ['Gravity Forms', 'Rocketgenius', 'To be confirmed', 'Annual', 'To be confirmed', 'Client'],
    ['Care plan', '-', 'n/a', 'n/a', 'n/a', 'n/a'],
])
# ---- 7. Premium software
rows(14, [
    ['Elementor Pro 4.4.1', '-', 'Annual', '-', 'my.elementor.com'],
    ['Gravity Forms 3.2.3.1', '-', 'Annual', '-', 'gravityforms.com/my-account'],
])
# ---- 8. Backups
kv(15, ['Files and database',
        'No WordPress-level backup plugin is installed. Host-level backups at WHC.',
        'To be confirmed with WHC',
        'Host-level backups by Web Hosting Canada, to be confirmed with WHC. A one-off full backup (database and key files) was taken on 20 November 2026 and is stored on the server outside the website folder.'])
# ---- 9. Security
kv(17, ['Imunify360 (CloudLinux, host-level)', 'Imunify360 — runs continuously, at server level', 'Not enabled',
        'Enforced site-wide', 'enabled', 'None'])
rows(18, [
    ['spco', 'Administrator', 'info@spco.ca', '06/11/26'],
    ['design', 'Administrator', 'service@pro.whc.ca', '20/11/26'],
])
# ---- 10. Search, analytics and tracking
rows(19, [
    ['Search engine indexing enabled (the "Discourage search engines" setting is OFF)', 'Confirmed', '20/11/26'],
    ['XML sitemap generated and declared in robots.txt', 'Confirmed', '20/11/26'],
    ['robots.txt reviewed', 'Confirmed', '20/11/26'],
    ['Redirects from the old website mapped and tested', 'Not applicable', '20/11/26'],
    ['Page titles and meta descriptions set on all pages', 'Confirmed', '20/11/26'],
    ['Analytics tracking verified as recording', 'Client need to setup tag', '20/11/26'],
])
kv(20, ['Not connected', 'Verification file on the server (googlec483ecf891827b1e.html)', 'Not installed', 'Yoast SEO 28.9', 'https://spco.ca/sitemap_index.xml'])
rows(21, [
    ['Lighthouse Performance', '96', '90+'],
    ['Lighthouse SEO', '100', '100'],
    ['Lighthouse Accessibility', '96', '95+'],
    ['Mean on-page score (5 pages)', '97.1', '95+'],
    ['First Contentful Paint', '1.3 s', 'under 1.8 s'],
    ['Largest Contentful Paint', '1.5 s', 'under 2.5 s'],
    ['Cumulative Layout Shift', '0', 'under 0.1'],
    ['Total Blocking Time', '0 ms', 'under 200 ms'],
    ['Speed Index', '1.3 s', 'under 3.4 s'],
])
# ---- 11. Legal and compliance
rows(22, [
    ['Privacy policy', 'Not published', 'Required if you collect any personal information, including through a contact form. The enquiry form collects names and contact details.'],
    ['Terms and conditions', 'Not published', '-'],
    ['Cookie / tracking consent', '-', '-'],
    ['Business details displayed', 'Yes', 'Firm name, address, phone and email shown in the footer.'],
    ['Accessibility', 'WCAG 2.2 AA — not assessed', 'Lighthouse scored accessibility 96 on desktop and 100 on mobile, with one colour-contrast failure.'],
    ['Copyright notice', 'Not present', '-'],
])
set_par(P[111], 'One Lighthouse colour-contrast failure on the homepage (desktop)')
set_par(P[112], 'No image without alternative text was found across the 5 pages')
# ---- 12. Using your website
set_par(P[115], 'Go to https://spco.ca/wp-admin')
rows(23, [
    ['Edit text or an image on a page', 'Pages → hover the page → Edit with Elementor → click the element → edit → Update'],
    ['Add a blog post', 'Posts → Add New → write → set a featured image → Publish'],
    ['Change a menu item', 'Appearance → Menus'],
    ['See form submissions', 'Forms → Entries. Gravity Forms stores every submission; notifications are also emailed to info@spco.ca'],
    ['Add a user', 'Users → Add New → choose the lowest suitable role'],
    ['Remove a user', 'Users → hover → Delete → attribute their content to another user'],
    ['Update your own password', 'Users → Profile'],
])
# ---- 19. Glossary
cell(31, 2, 1, 'Controls how your website looks. Yours is Astra, with a child theme named Astra Child 02 (spco-child).')
# ---- Appendix A
set_par(P[203], 'Your DNS records as at 20 November 2026. Changing these incorrectly will take down your website, your email, or both. Always keep a copy of the current records before making a change.')
rows(32, [
    ['A', '@', '198.50.215.64', '3600'],
    ['CNAME', 'www', 'spco.ca.', '3600'],
    ['MX', '@', '0 mx.spco.ca.', '3600'],
    ['NS', '@', 'ns1.whc.ca.', '3600'],
    ['NS', '@', 'ns2.whc.ca. / ns3.whc.ca.', '3600'],
    ['TXT', '@', 'v=spf1 +a +mx +ip4:148.113.170.105 include:spf.web-dns1.com +ip4:198.50.215.64 +ip4:54.39.101.30 +ip4:158.69.26.68 ~all', '3600'],
    ['TXT', 'default._domainkey', 'v=DKIM1; k=rsa; p=… (2048-bit public key)', '3600'],
    ['TXT', '_dmarc', 'v=DMARC1; p=none;', '3600'],
])
# ---- Appendix B
rows(33, [
    ['Elementor', '4.4.1', 'Page builder', 'Free', 'No'],
    ['Elementor Pro', '4.4.1', 'Page builder (Pro widgets and theme builder)', 'Paid', 'No'],
    ['Ultimate Addons for Elementor (UAE)', '2.9.8', 'Elementor header / footer templates', 'Free', 'No'],
    ['Gravity Forms', '3.2.3.1', 'Enquiry form and stored entries', 'Paid', 'Yes'],
    ['Advanced Custom Fields', '6.8.12', 'Custom fields for client resources', 'Free', 'No'],
    ['Widgets for Google Reviews', '15.0', 'Google reviews carousel', 'Free', 'No'],
    ['Yoast SEO', '28.9', 'SEO titles, meta descriptions and XML sitemap', 'Free', 'No'],
    ['LiteSpeed Cache', '7.9.3', 'Page caching', 'Free', 'No'],
    ['WP Mail SMTP', '4.10.4', 'Outgoing email delivery', 'Free', 'No'],
    ['Atarim', '5.2.0', 'Site management connection for WHC', 'Free', 'No'],
    ['Astra (parent theme)', '4.14.3', 'Base theme', 'Free', 'No'],
    ['Astra Child 02 - spco-child (active theme)', '4.13.0', 'Child theme holding site customisations', 'Free', 'No'],
])
d.save(out)
print('saved', out)
