# True Path Management — site

Static site. No build step, no dependencies.

```
index.html          landing page
contact.html        contact form
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

## Partners section

Partner brands are named in the site's own typography — no logo files, nothing to
source or license. Each name is one `<li class="ptname">` in the `#partners`
section of `index.html`, tinted by an inline custom property:

```html
<li class="ptname" style="--pt-c:#D11920">Raising Cane's</li>
```

Colors in use:

| Brand | Value | Source |
| --- | --- | --- |
| Raising Cane's | `#D11920` | Published (Pantone 485 C) |
| Jersey Mike's | `#134A7C` | Published |
| HOW Water | `#0B7C8A` aqua | Chosen for legibility, not from a brand guide |
| Bear's | `#B3271E` red | Chosen for legibility, not from a brand guide |
| Smokehouse BBQ | `#5A6577` grey | Second tone, set via `--pt-c2` |

A name can carry two colors by wrapping part of it in `<span class="pt-sub">`,
which picks up `--pt-c2`.

Every name sits inside a single `<span class="pt-t">` so multi-word names wrap as
text. Remove that wrapper and the tile's flex layout splits the words into
separate columns instead of wrapping them.

All values clear 4.4:1 contrast against the cream background.

To add or remove a partner, add or delete an `<li>`. The row is a 4-up grid on
desktop, 2-up on tablet, stacked on phones, so any count reflows on its own.

Keep the `.pt-legal` disclaimer in place, and describe the relationship
accurately — "brands our athletes have partnered with" is a different claim from
"our partners."

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
