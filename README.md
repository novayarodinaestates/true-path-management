# True Path Management — site

Static site. No build step, no dependencies.

```
index.html          landing page
contact.html        contact form
faq.html            frequently asked questions
privacy.html        privacy policy
terms.html          terms of use
legal.css           shared styles for faq / privacy / terms
images/
  logo-mark.webp    nav logo + favicon (.png kept as fallback)
  logo-full.webp    hero + footer logo
  athletes/         roster photos (.webp served, .jpg kept as source)
  gallery/          drop new photos here — see images/gallery/README.txt
```

## Deploy to Vercel

Option A — drag and drop: zip this folder, drop it on vercel.com/new.
Option B — Git: push this folder to a repo and import it in Vercel.

There is no framework, so when Vercel asks, choose **Other** and leave the
build command empty with the output directory set to the project root.

## Collaborations section

Logo grid in the `#collaborations` section of `index.html` (reachable at
`/collaborations`; the old `/partners` URL redirects there via `vercel.json`).

Logos live in `images/collaborations/` as transparent `.png` files, each with a
`.webp` copy beside it. Every logo is one `<li class="clb-tile">`:

```html
<li class="clb-tile"><picture class="clb-logo">
  <source type="image/webp" srcset="images/collaborations/NAME.webp">
  <img src="images/collaborations/NAME.png" alt="Business name"
       width="PNG_WIDTH" height="PNG_HEIGHT" loading="lazy" decoding="async">
</picture></li>
```

To add one: export a transparent PNG (at least ~600px on the long edge so it stays
crisp on retina screens), make a WebP copy that keeps transparency (squoosh.app,
or `cwebp -q 90 -alpha_q 100 NAME.png -o NAME.webp`), and add an `<li>` like the
one above with the PNG's real pixel width and height. Every tile is the same size
and each logo is fitted inside the same box, so any shape lines up.

The grid is 3 across on desktop and 2 across on tablets and phones, so keep the
count even (6, 8, …) or the last row will be short.

Keep the `.clb-legal` disclaimer in place.

## Adding photos

1. Export at ~1600px on the long edge, quality 80–85.
2. Convert to WebP (https://squoosh.app — drag in, pick WebP, download).
   Keep the original JPG too, in case you want to re-crop later.
3. Drop it in `images/gallery/` and follow the comment above the gallery grid
   in `index.html`.

Always give an `<img>` a `width`, `height`, `alt`, and `loading="lazy"` (except
anything visible before scrolling — that one gets `loading="eager"`). The width
and height stop the page from jumping around while images load.

## Editing testimonials

In `index.html`, find the `#testimonials` section. Each card is one `<figure>`.
Replace the quote, name, initials, and role — then delete the word `todo` from
`class="tst rise todo"` so the card stops rendering greyed out.

## The standalone pages

`faq.html`, `privacy.html`, and `terms.html` share `legal.css`, which is a copy of
the site chrome (nav, footer, tokens) plus the prose and accordion styles. They are
linked from the Legal column in the footer of every page.

Two things to know if you edit them:

- The footer markup is duplicated in `index.html`, `contact.html`, and mirrored in
  `legal.css`. Change the footer in one place and change it in all of them, including
  the `.foot-in` grid column count if you add or remove a column.
- The FAQ accordion is native `<details>`/`<summary>` — no JavaScript. Adding a
  question means copying one `<details class="faq">` block.

`faq.html` also carries FAQPage structured data in a `<script type="application/ld+json">`
block at the bottom. If you change the first four answers materially, update it to match
or remove it — mismatched structured data is worse than none.

**Before launch, two answers in `faq.html` need confirming.** They are marked with
`REPLACE` comments: the fee question, and the certified-contract-advisor question.
Both are written conservatively but neither has been verified.

## Checking the site before you deploy

```bash
python3 qa-check.py              # static checks, nothing to install
python3 qa-check.py --browser    # + real browser tests at 3 screen sizes
```

The browser pass needs Playwright once:

```bash
pip install playwright && playwright install chromium
```

It checks: every file path resolves with exact case (Mac is case-insensitive,
Vercel is not — this is the #1 cause of images working locally and breaking
live), no dead anchors, no leftover placeholder text, no broken images, no
sideways scrolling on mobile, no JS console errors, gallery photos never
cropped, tap targets big enough on phones, and that the lightbox opens and
closes. Exit code is 0 on pass, 1 on failure.

## Deploying

```bash
npx vercel          # preview URL
npx vercel --prod   # production
```

Framework preset: Other. Leave the build command empty — there is nothing to
compile.
