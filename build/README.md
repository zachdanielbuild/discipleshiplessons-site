# DiscipleshipLessons build kit

Everything needed to rebuild the whole site. Cloudflare Pages serves the HTML files in the repo root; this folder generates them.

## Rebuild the site

```
bash build/deploy.sh
git add -A && git commit -m "..." && git push
```

Pushing to `main` deploys to https://discipleshiplessons-site.pages.dev in about a minute.

## What's here

| File | What it is |
| --- | --- |
| `buildsite.py` | Builds every page. Lesson content, the trail layout, "Why?" statements (`VISION`), content fixes (`FIXES`), page-specific layout tweaks (`layout()`), the Foundations page (`foundations()`) and the homepage. |
| `xml/items.json` | All lesson text, pulled from the old Squarespace export (Oct 20, 2026). |
| `home_frozen.dc.html` | Source of the homepage (the approved postcard design). `buildsite.py` fixes its links by line number (`HMAP`), so keep line counts the same when editing it. |
| `tree_svgs.json` | The "What's our strategy?" tree drawings on Who Should I Disciple. |
| `site/style.css` | All styles, including phone and print. Edited by hand, not generated. |
| `site/favicon.svg`, `share.png`, `apple-touch-icon.png` | Logo, link-preview image, phone home-screen icon. |
| `launchfiles.py` | Writes `_redirects`, `robots.txt`, `sitemap.xml` and `404.html`. |
| `deploy.sh` | Runs both builders and copies the results to the repo root. |

## Common changes

- **Edit a "Why?" statement:** change its entry in `VISION` in `buildsite.py` (keyed by lesson number; see `TITLES`).
- **Fix lesson wording:** add a find-and-replace pair under that lesson's address in `FIXES`.
- **Change styles:** edit `site/style.css`.
