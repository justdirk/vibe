# tools/fixes — how site-wide changes are applied

This site is 40+ hand-written HTML pages in 5 languages, deployed to GitHub Pages by
`.github/workflows/pages.yml` on every push to `main`.

Two things to know before changing it:

1. **Commits made by GitHub Actions with `GITHUB_TOKEN` do not trigger other workflows.**
   A workflow that edits pages and commits them must deploy Pages itself, or the change
   never goes live (that is what happened on 1 Sep 2026). `apply-fixes.yml` does both.
2. **Bulk edits go through idempotent scripts here, not hand-retyped pages.** Push a
   Python script into `tools/fixes/` (or run the workflow manually) and
   `apply-fixes.yml` runs every script in name order, commits the result and deploys.
   Every script must be safe to run repeatedly (check before changing).

| Script | What it owns |
|---|---|
| `001-phase1.py` | bundle Stripe link, `/a.js` on every page, shared footer (site pages), hero fixes, Founder Toolkit on localized homepages, title/description lengths, speaking JSON-LD, sitemap lastmod, favicon, 404 |
| `002-contact.py` | Contact link in footers + `/contact/` in the sitemap |
| `003-speaking-i18n.py` | **generates** `/speaking/` and `/{de,es,pt,it}/speaking/` from one template + per-locale strings — edit the strings here, not the pages. v2 layout (Sep 2026): cinematic hero, count-up numbers, stage marquee, numbered talks, pull-quotes; positioning is "founder, invited to speak" (no "keynote speaker" label, CTA "Invite Dirk") |
| `004-chat-oss.py` | "Built on open source" section on `/chat/` |
| `005-chat-gate.py` | `/chat/` ↔ gate wiring (Railway fallback URL, instant sign-in after Stripe via `/api/paid`, login redirect), canonicals on the app legal pages |

Shared assets: `/site.css` (global), `/speaking.css` + `/speaking.js` (speaker + contact pages,
form submission to the Supabase `contact` function, scroll reveal + count-up), `/a.js` (first-party analytics).

Backends the pages talk to:

- Contact + speaking inquiries → `https://jbbvoajtbgzhxnbcpkcc.supabase.co/functions/v1/contact`
  → table `contact_messages` (+ email via Resend when `RESEND_API_KEY` is set on the function).
- dirk.it AI gate (`/chat/`) → `https://gate.dirk.it/api/access` (service `gate` in `justdirk/ai/gate`,
  Railway project `librechat`), `https://gate-production-51c9.up.railway.app` as fallback.
- Analytics → `.../functions/v1/track` → table `site_events`.
