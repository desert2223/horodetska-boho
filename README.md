# Horodetska Boho — editorial showroom (v2)

A **private, not-yet-approved** static preview of an independent designer atelier site. The source includes a homepage, collections preview, 12 editorial look pages, archive, story, atelier, runway & press, FAQ and contact page.

**This is not an active shop.** Availability, prices, sizes, fabric compositions and sold status are not verified. The enquiry form copies a draft message; it **does not send** email, store inquiries, or accept payments. Visitor analytics are **not** connected.

## Project structure

- `index.html` — homepage, portrait of the designer.
- `collections/`, `looks/`, `archive/` — editorial lookbook.
- `our-story/`, `atelier/`, `runway-press/` — brand presentation.
- `faq/`, `contact/` — customer information / enquiry prototype.
- `assets/css/styles.css` — layout and editorial look.
- `assets/js/app.js` — interactive menu, category filters and form text preparation.
- `assets/img/` — optimized retouched photographs (not generative redesigns).
- `data/looks.json`, `data/photo_inventory.csv` — draft grouping and content review.
- `EDITORIAL_NOTES_UK.md` — required confirmations before public launch.
- `build.py`, `build_v2.py` — development scripts used to generate site pages. They require Python with Jinja2 and may overwrite HTML / CSS / README; keep a git commit before using them. **No build step is required for deployment.**

## Preview locally

In the project folder run:

```bash
python -m http.server 8080
```

Open http://localhost:8080 — opening HTML directly from disk is not supported because asset routes are root-relative.

Check all local asset links:

```bash
python scripts/check_site.py
```

## Version control (private repository)

1. In GitHub, create a new **Private** empty repository named `horodetska-boho` in the `desert2223` account. **Do not** generate a README, license or .gitignore: they are included here.
2. Put the **contents of this folder** in the repository root (so `index.html` is directly in the repo root, not inside a nested folder).
3. With Git installed, from the extracted project folder:

```bash
git init -b main
git add .
git commit -m "Initial Horodetska Boho editorial preview v2"
git remote add origin https://github.com/desert2223/horodetska-boho.git
git push -u origin main
```

If using GitHub's browser upload, navigate to the new repository, choose **Add file → Upload files**, and drop the contents of the extracted folder into the upload area; verify nested directories were preserved before committing. You can use GitHub Desktop as a graphical alternative.

## Cloudflare Pages (only after photo / rights review)

- Create a **separate Pages project** (do not use the ResponseHarbor project).
- Choose **Connect to Git** and authorize the `desert2223/horodetska-boho` repository.
- Production branch `main`.
- Framework preset: `None` (plain static site).
- Build command: leave **empty**.
- Build output directory: `.` (repository root).
- No environment variables needed yet.

Every push to `main` can then redeploy the site automatically, subject to Cloudflare project settings. A private GitHub repo does **not** make the Cloudflare Pages URL private: treat any deployed Pages preview as publicly reachable. This preview has a `noindex` meta tag, `robots.txt`, and a Cloudflare `_headers` rule with `X-Robots-Tag`, which discourage indexing but **do not restrict access**. Use Cloudflare Access if genuine access control is needed.

## Prelaunch checklist

- [ ] Owner confirms brand name, founder biography, studio location and rights to photo assets.
- [ ] Get photographer / model permissions, especially for editorial looks shot with other people.
- [ ] Confirm prices, statuses, measurements, materials and care instructions.
- [ ] Define contact email and inquiry delivery method, international shipping and return policy.
- [ ] Replace placeholder legal/privacy sections with approved documents.
- [ ] Test checkout or enquiry solution if commerce is enabled later.
- [ ] Set up analytics only after appropriate consent configuration.
- [ ] Remove `noindex`, `_headers` robots directive and `robots.txt` disallow when officially launching.

Do not publish as an operational commerce website until these items are complete.
