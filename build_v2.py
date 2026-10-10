from pathlib import Path
from urllib.parse import quote
import json
from jinja2 import Template
import build as v1
ROOT=Path(__file__).resolve().parent
looks=json.loads((ROOT/'data'/'looks.json').read_text(encoding='utf-8'))
BASE=v1.BASE.replace('Independent designer atelier · Slovenia','Horodetska Boho · Designer Atelier · Slovenia')
# All pages still intentionally de-indexed during private review.
BASE=BASE.replace('This is a concept showroom. Availability, prices and ordering are not yet enabled.','Photographic showroom preview · Catalogue details and ordering are pending designer approval.')
BASE=BASE.replace('A world of singular garments','A world of singular garments')
BASE=BASE.replace('Our online catalogue is being curated; enquiries are currently handled through the official Instagram profile.','Our visual catalogue is available for preview. Enquiries are currently handled through the official Instagram profile.')
CONTENT=dict(v1.CONTENT)
h=CONTENT['home']
h=h.replace('Independent designer atelier · Est. 2016','HORODETSKA BOHO · SVITLANA HORODETSKA')
h=h.replace('Artful silhouettes, expressive textures and distinctive hand-knitted details. A fashion world shaped by individuality, not uniformity.','One-of-a-kind designer clothing by Svitlana Horodetska. Ukrainian design roots, an independent atelier in Slovenia, and handcrafted detail in every look.')
h=h.replace('/assets/img/editorial-portrait.webp','/assets/img/photo-07.webp')
h=h.replace('alt="Editorial portrait with colorful handcrafted textile necklace and textured light coat"','alt="Svitlana Horodetska in a long pale-grey embroidered outfit"')
h=h.replace('Horodetska / Editorial Study','SVITLANA HORODETSKA / FOUNDER')
h=h.replace('Portrait & textile study<br/>Horodetska Boho','Svitlana Horodetska<br/>Founder & designer')
h=h.replace('Art in every detail.','Made with individuality.')
h=h.replace('Editorial looks</span>','Signature looks</span>')
h=h.replace('Portraits · Art direction','Selected designs · Photo collection')
h=h.replace('src="/assets/img/textile-detail.webp"','src="/assets/img/photo-12.webp"')
h=h.replace('src="/assets/img/handwork-detail.webp"','src="/assets/img/photo-13.webp"')
h=h.replace('<div class="art-frame"></div>','<img src="/assets/img/photo-24.webp" alt="Pink embroidered outer layer with a white dress" loading="lazy"/>')
h=h.replace('Past collections · Coming soon','A visual record · In curation')
h=h.replace('Full product listings will follow after inventory confirmation.','Browse real photographs from the atelier. Prices, sizes and availability will be confirmed before orders open.')
h=h.replace('A fashion world shaped by individuality, not uniformity.','A fashion world shaped by individuality.')
# Place a studio model shot in first collection tile instead of founder repeat.
h=h.replace('<img src="/assets/img/photo-07.webp" alt="Editorial portrait showing a textured coat and colorful handcrafted accessory" loading="lazy"/>','<img src="/assets/img/photo-02.webp" alt="Olive-green embroidered ensemble photographed in the studio" loading="lazy"/>')
CONTENT['home']=h
# Actual collection lookbook, without misrepresenting sales or inventory.
cat_cards=[]
for look in looks:
 pic=look['photos'][0]
 ident=look['id']
 cat_cards.append(f'''<article class="product-tile" data-category="{look['filter']}">
 <a href="/looks/hb-{ident}/" class="visual product-link" data-track="look_{ident}_open"><img src="/assets/img/photo-{pic:02d}.webp" alt="{look['title']} — Horodetska Boho editorial photo" loading="lazy"/><span class="photo-stamp">Look HB-{ident} · Preview</span></a>
 <h3>{look['title']}</h3><p>{look['description']} Catalogue details await confirmation.</p>
 <a href="/looks/hb-{ident}/" class="text-link" data-track="look_{ident}_details">View the look ↗</a></article>''')
CONTENT['collections']='''<section class="page-hero center"><div class="page-width"><span class="eyebrow">The Horodetska Boho lookbook</span><h1>Selected <em>looks.</em></h1><p>Explore original photographs of the atelier’s designs. This is a curated photographic preview, not a verified stock list. Pricing, sizes and availability are being confirmed.</p></div></section>
<section class="sct-tight"><div class="page-width"><div class="filter-controls" role="group" aria-label="Lookbook filters"><button type="button" class="filter-btn active" data-filter="all">All looks</button><button type="button" class="filter-btn" data-filter="editorial">Editorial</button><button type="button" class="filter-btn" data-filter="layers">Layers</button><button type="button" class="filter-btn" data-filter="dresses">Dresses</button></div><p class="status-legend">Photographic preview · Nothing here is labeled available or sold until verified by the designer. Look grouping and product specifications are provisional.</p>
<div class="catalog-grid">'''+''.join(cat_cards)+'''</div></div></section>
<section class="soft-section sct-tight"><div class="page-width quote-section"><span class="eyebrow">From the designer</span><blockquote>Clothing with a signature of its own.</blockquote><p class="muted">Made individually. Documented thoughtfully. Always ask the atelier about the current possibility of a particular look.</p><a href="/contact/" class="btn btn-outline">Contact the atelier ↗</a></div></section>'''
# An honest photo archive, not an unsupported sold record.
archive=[(9,'Lavender draped silhouette'),(18,'Ivory dress with embroidered detail'),(19,'Light embroidered two-piece'),(21,'Ivory flowing layers'),(22,'Black elongated silhouette'),(26,'Dark layered outerwear'),(29,'Vivid pink embroidered layer'),(30,'Soft pink embroidered tunic')]
arch_cards=''.join(f'''<figure class="archive-card"><img src="/assets/img/photo-{n:02d}.webp" alt="{title} from Horodetska Boho photography archive" loading="lazy"/><figcaption><b>{title}</b><span>Archive candidate · Status unverified</span></figcaption></figure>''' for n,title in archive)
CONTENT['archive']='''<section class="page-hero center"><div class="page-width"><span class="eyebrow">Photographic archive · In curation</span><h1>The <em>archive.</em></h1><p>A selection of photographs from the atelier’s collection history. Individual dates, names and sold statuses will be added after confirmation by the designer.</p></div></section>
<section class="sct-tight"><div class="page-width"><div class="archive-photo-grid">'''+arch_cards+'''</div><div class="info-band"><span class="eyebrow">A visual record, not a stock list</span><p>The photographed works shown here are not marked “sold” or “available” until verified. For requests about a particular design, contact the atelier directly.</p><a href="/contact/" class="text-link">Ask about a design ↗</a></div></div></section>'''
s=CONTENT['our-story']
s=s.replace('/assets/img/editorial-portrait.webp','/assets/img/photo-15.webp')
s=s.replace('Editorial portrait wearing expressive handcrafted textile details; the person depicted must be confirmed before publication','Svitlana Horodetska wearing an embroidered blue outer layer with a white dress')
CONTENT['our-story']=s
s=CONTENT['atelier']
s=s.replace('/assets/img/textile-detail.webp','/assets/img/photo-12.webp')
s=s.replace('/assets/img/handwork-detail.webp','/assets/img/photo-13.webp')
s=s.replace('Close-up studies from the first editorial test. Additional studio and process imagery is still to come.','Actual close-up photographs of embroidery, lace and textile details. Studio process documentation can be added later.')
CONTENT['atelier']=s
# Separate detail pages with original photo sets and no price assertions.
for look in looks:
 ident=look['id']; slug=f'hb-{ident}'
 v1.pages[slug]=(f'looks/{slug}',f"{look['title']} — Horodetska Boho",look['description'])
 pictures=''.join(f'<img src="/assets/img/photo-{n:02d}.webp" alt="{look["title"]} — photograph {idx+1}" loading="lazy"/>' for idx,n in enumerate(look['photos']))
 requesturl='/contact/?piece='+quote(f"Look HB-{ident}: {look['title']}")
 CONTENT[slug]=f'''<section class="page-hero"><div class="page-width"><a href="/collections/" class="tiny-meta">← Back to looks</a><h1>{look['title']}</h1><p>Look HB-{ident} · Photographic preview</p></div></section>
 <section class="sct-tight"><div class="page-width look-detail-grid"><div class="look-detail-images">{pictures}</div><div class="look-details"><span class="eyebrow">One-of-a-kind design · Preview</span><h2 class="display">The <em>details.</em></h2><p class="copy">{look['description']}</p><dl class="spec-list"><div><dt>Availability</dt><dd>Awaiting atelier confirmation</dd></div><div><dt>Price</dt><dd>Not yet confirmed</dd></div><div><dt>Size</dt><dd>Measurements on request</dd></div><div><dt>Materials</dt><dd>Composition to be confirmed</dd></div></dl><a href="{requesturl}" class="btn btn-dark" data-track="request_look_{ident}">Enquire about this look ↗</a><p class="muted" style="font-size:12px;line-height:1.8;margin-top:25px">Images may show a coordinated outfit rather than one purchasable item. Grouping, availability and individual garment specifications will be confirmed before the public shop launches.</p></div></div></section>'''
# Asset file can be visited without shipping an image library to external host.
layout=Template(BASE)
for name,(folder,title,desc) in v1.pages.items():
 filename=ROOT/(folder or '.')/'index.html'
 filename.parent.mkdir(parents=True,exist_ok=True)
 filename.write_text(layout.render(title=title,desc=desc,page=name,content=CONTENT[name]),encoding='utf-8')
# Keep the demo trackable in a future permissioned implementation, without initializing GA4 prematurely.
app=(ROOT/'assets'/'js'/'app.js')
js=app.read_text(encoding='utf-8')
js=js.replace('  const enquiry=document.querySelector', '''  // View-item can fire only if analytics has been enabled after appropriate consent.
  if (document.body.dataset.page.startsWith('hb-')) {
    consentedEvent('view_item', {item_id: document.body.dataset.page});
  }
  const enquiry=document.querySelector''')
app.write_text(js,encoding='utf-8')
css=ROOT/'assets'/'css'/'styles.css'
css.write_text(css.read_text(encoding='utf-8')+'''
/* V2 — new photographic catalogue */
.archive-photo-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:21px}
.archive-card{margin:0;min-width:0}.archive-card img{aspect-ratio:3/4;object-fit:cover;object-position:center 25%;background:#e1d8cb}.archive-card figcaption{padding:16px 0 24px;display:flex;flex-direction:column;gap:5px}.archive-card figcaption b{font-family:var(--display);font-weight:400;font-size:21px}.archive-card figcaption span{font-size:10px;color:var(--muted);letter-spacing:.09em}
.look-detail-grid{display:grid;grid-template-columns:1.25fr .75fr;gap:8%;align-items:start}.look-detail-images{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.look-detail-images img{height:auto;object-fit:cover;aspect-ratio:3/4;width:100%;background:#e0d8c9}.look-detail-images img:first-child{grid-column:1/-1;max-height:770px;object-position:center 23%}.look-details{position:sticky;top:35px}.look-details .display{font-size:clamp(46px,5vw,72px);line-height:1.1;margin:20px 0}.spec-list{border-top:1px solid var(--line);margin:35px 0}.spec-list div{display:grid;grid-template-columns:130px 1fr;gap:20px;border-bottom:1px solid var(--line);padding:17px 0}.spec-list dt{font-size:10px;letter-spacing:.13em;text-transform:uppercase;font-weight:700}.spec-list dd{margin:0;font-size:13px;color:var(--muted)}
@media(max-width:900px){.archive-photo-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.look-detail-grid{grid-template-columns:1fr;gap:45px}.look-details{position:static}}
@media(max-width:560px){.archive-photo-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.archive-card figcaption b{font-size:18px}.archive-card figcaption span{font-size:9px}.look-detail-images{gap:8px}.spec-list div{grid-template-columns:105px 1fr}}
''',encoding='utf-8')
(ROOT/'README.md').write_text('''# Horodetska Boho — Editorial Preview v2\n\n22+ pages: Home, Collections, 12 individual look pages, Archive, Our Story, Atelier, Runway & Press, FAQ, Contact. Built with HTML/CSS/JS; no build process required for publishing.\n\n## Local preview\n\nFrom this directory: `python -m http.server 8080`, then open `http://localhost:8080`. Do not double-click `index.html`: root-relative routes expect a web server.\n\n## Deploy\n\nCloudflare Pages: use **direct upload** of the site directory or upload to GitHub and connect Pages. The output root is this folder. Leave the `noindex,nofollow` tag while reviewing. Set up a preview domain before going public.\n\n## Content and legal\n\nData for 34 original photos and review sheet: `data/photo_inventory.csv`. Grouping of photos into looks is provisional, and all prices/stock/sale statuses are unknown. Original source photographs are kept in user's supplied archive; the `/assets/img/photo-XX.webp` copies are exposure-adjusted and optimized. Generated/stylized images from past experiments are not used for the new catalogue.\n\nThe enquiry form **copies an enquiry to clipboard only**, then the user manually messages Instagram. No analytics, tracking or form storage enabled. Do not public-launch without approval of images, model rights, claims, terms, privacy, and contact method. See `EDITORIAL_NOTES_UK.md`.\n''',encoding='utf-8')
print('Generated',len(v1.pages),'pages; all photographs prepared.')
