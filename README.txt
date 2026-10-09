TANG VASCULAR RESEARCH LAB — LOCAL WEBSITE

Build:
  python3 build.py

Preview locally:
  python3 -m http.server 4173 --bind 127.0.0.1 --directory public
  Open http://127.0.0.1:4173

The finished static website lives in public/. It has no runtime dependencies,
database, analytics, remote fonts, or external image requests.

Edit publication and people records in data/site.json, then rebuild.
Edit layouts and page copy in build.py.
Edit styling and behavior in assets/site.css and assets/site.js, then rebuild.
Research source notes and items requiring later confirmation are recorded in
data/sources.json. These notes are not included in the public website.

This site is a design preview, published using GitHub Pages.
Preview URL: https://vicdus.github.io/tang-vascular-lab/
Repository: https://github.com/vicdus/tang-vascular-lab

Pushing the main branch automatically builds and publishes the site using
.github/workflows/pages.yml. Only public/ is uploaded as the website artifact.
The generated public/ directory is not committed to the source repository.

The lab name is provisional. Current membership must be supplied by the lab.
The UW portrait is an older public profile image with its source credited.
Replace it with a lab-provided current image before the final launch.
The historical contributors are clearly separated from the current PI and from
the collaborators listed in the UW research profile. No coauthor is assumed
to be a current employee. The bibliography is explicitly selected, not complete.

Future Cloudflare deployment (only when requested):
  python3 build.py
  npx wrangler deploy

The included configuration serves static assets only; no Worker script or
database is required. Connect the purchased domain in Cloudflare when ready.
