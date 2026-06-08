# True Structure Landing Page

Static HTML/CSS landing page for the True Structure Mission Assurance Platform.
Designed for direct upload to Bluehost shared hosting — no build step required.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Full single-page HTML5 landing page |
| `styles.css` | All styles (Google Fonts via @import, no other CDN dependencies) |

---

## Deploy to Bluehost (FTP)

1. Log in to Bluehost → **Files** → **File Manager**, or connect via FTP (Filezilla / Cyberduck).
2. Navigate to `public_html/` (or a subdirectory such as `public_html/landing/`).
3. Upload both `index.html` and `styles.css` to the same directory.
4. The page is live immediately — no build, no npm, no server configuration required.

**FTP credentials:** Bluehost cPanel → **FTP Accounts**.

---

## Connect the Contact Form to Formspree

The form currently uses `action="#"` (no-op). To receive submissions by email:

1. Create a free account at [formspree.io](https://formspree.io).
2. Create a new form and copy the endpoint, e.g. `https://formspree.io/f/xrgvabcd`.
3. In `index.html`, replace the form opening tag:
   ```html
   <!-- before -->
   <form class="form" action="#" method="POST">

   <!-- after -->
   <form class="form" action="https://formspree.io/f/xrgvabcd" method="POST">
   ```
4. Formspree will forward submissions to `marko.pribisalic@gmail.com` (configure the destination in Formspree dashboard).
5. Add a hidden `_subject` field inside the form if you want a custom email subject:
   ```html
   <input type="hidden" name="_subject" value="True Structure — Pilot Request" />
   ```

---

## Point a Custom Domain / App Subdomain to Vercel

If the main platform (`app.truestructure.io`) is deployed on Vercel:

1. In Bluehost cPanel → **Domains** → **Zone Editor**, add a CNAME record:
   - **Name:** `app` (creates `app.yourdomain.com`)
   - **Value:** `cname.vercel-dns.com`
   - **TTL:** 3600
2. In your Vercel project → **Settings** → **Domains**, add `app.yourdomain.com`.
3. Vercel will provision a TLS certificate automatically.

The static landing page continues to be served from Bluehost at the root domain (`yourdomain.com` / `www.yourdomain.com`).

---

## Local Preview

Open `index.html` directly in a browser — no local server needed.

For a local server (optional):
```bash
python3 -m http.server 8080
# then visit http://localhost:8080
```
