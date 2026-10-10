# Horodetska Boho — Editorial Showroom v2

Static editorial fashion website for designer Svitlana Horodetska. The project includes a homepage, collections preview, 12 editorial look pages, archive, Our Story, Atelier, Runway & Press, FAQ, and Contact.

## Current status

- **GitHub repository:** public, `main` branch.
- **Photography:** user-approved images for this site; 34 optimized photographs are included.
- **Deployment:** Cloudflare Pages Git integration is the planned hosting approach. **Not yet connected by this repository.**
- **Site:** design / catalogue preview, not an active ecommerce storefront.
- **Catalogue data:** prices, stock status, sizes, fabrics and historical sold status await final confirmation.
- **Enquiries:** the form prepares a message for the visitor to copy to Instagram; it does not send email or accept payments.
- **Analytics:** not yet installed. Tracking handlers in `assets/js/app.js` do not send events until an analytics setup and consent flow are configured.

## Files

- `index.html` — homepage with the designer portrait.
- `collections/` and `looks/` — photo catalogue and look pages.
- `archive/` — photo archive; no unverified sold claims.
- `our-story/`, `atelier/`, `runway-press/` — editorial pages.
- `faq/` and `contact/` — informational pages.
- `assets/` — shared CSS/JavaScript, optimized photography and favicon.
- `data/` — look grouping and photo inventory for future curation.
- `EDITORIAL_NOTES_UK.md` — missing business information and content to confirm.
- `scripts/check_site.py` — local links and assets check.

## Run locally

Run from the repository root:

```bash
python -m http.server 8080
```

Then open http://localhost:8080 . Root-relative asset paths mean opening individual HTML files directly from disk is not the intended preview method.

## Validate

```bash
python scripts/check_site.py
```

GitHub Actions also runs the check after pushes to `main` and pull requests.

## Deploy to Cloudflare Pages

In Cloudflare Dashboard → Workers & Pages → Create application → Pages → Connect to Git (or Import an existing Git repository):

| Setting | Value |
|---|---|
| GitHub repo | `desert2223/horodetska-boho` |
| Production branch | `main` |
| Project name | `horodetska-boho` (if available) |
| Framework preset | `None` |
| Build command | `exit 0` |
| Build output directory | `.` |
| Root directory | repository root / default |
| Environment variables | none |

Select **Save and Deploy / Deploy**, then check the generated `*.pages.dev` URL. Pushing new commits to `main` automatically triggers subsequent deployments.

### Preview indexing and access

The project includes a `noindex` meta tag, a `robots.txt` file, and `_headers` with `X-Robots-Tag` intended to discourage indexing during the design-preview stage. **These do not hide the site:** `*.pages.dev` is publicly reachable unless access protection is separately configured. Remove preview indexing restrictions only when the commercial site is ready.

## Before a commerce launch

Confirm product availability, descriptions, prices, measurements and materials, consumer terms (delivery, returns), the contact email, functional enquiry processing / payment arrangements and privacy / cookie compliance. The current prototype is not a live online shop.
