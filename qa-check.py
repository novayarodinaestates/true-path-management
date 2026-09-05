#!/usr/bin/env python3
"""
True Path Management — pre-flight check.

Run from inside the site folder:      python3 qa-check.py
Add live browser tests (optional):    python3 qa-check.py --browser

Static checks need nothing installed. --browser needs playwright:
    pip install playwright && playwright install chromium
"""
import os, re, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ["index.html", "team.html", "contact.html", "faq.html", "privacy.html", "terms.html"]
fails, warns, notes = [], [], []


def disk_files():
    out = set()
    for base, _, files in os.walk(ROOT):
        for f in files:
            out.add(os.path.relpath(os.path.join(base, f), ROOT).replace("\\", "/"))
    return out


def check():
    disk = disk_files()
    lower = {d.lower(): d for d in disk}

    for page in PAGES:
        if page not in disk:
            fails.append(f"{page} is missing")
            continue
        html = open(os.path.join(ROOT, page), encoding="utf-8").read()

        # 1. every local reference resolves, with EXACT case (Vercel is case-sensitive)
        for ref in re.findall(r'(?:src|href)="([^"]+)"', html):
            if ref.startswith(("http", "mailto:", "tel:", "#", "data:")):
                continue
            path = ref.split("#")[0].split("?")[0]
            if not path:
                continue
            # vercel.json sets cleanUrls, so "/team" is served from team.html
            # and "/" from index.html. Resolve those before checking disk.
            if path.startswith("/"):
                path = "index.html" if path == "/" else path.lstrip("/")
                if path and "." not in os.path.basename(path):
                    path += ".html"
            if path in disk:
                continue
            if path.lower() in lower:
                fails.append(f"{page}: CASE MISMATCH '{path}' -> real file is '{lower[path.lower()]}' "
                             f"(works on Mac, 404s on Vercel)")
            else:
                fails.append(f"{page}: missing file '{path}'")

        # 2. anchors point at sections that exist
        ids = set(re.findall(r'id="([^"]+)"', html))
        for a in re.findall(r'href="#([^"]+)"', html):
            if a and a not in ids:
                fails.append(f"{page}: dead anchor '#{a}'")

        # 3. images need alt + dimensions (accessibility + no layout jump)
        for tag in re.findall(r"<img[^>]*>", html):
            m = re.search(r'src="([^"]+)"', tag)
            if not m:
                continue          # empty shell, e.g. the lightbox <img> filled by JS
            src = m.group(1)
            if 'alt="' not in tag:
                warns.append(f"{page}: <img> without alt — {src}")
            if not ("width=" in tag and "height=" in tag):
                warns.append(f"{page}: <img> without width/height — {src}")

        # 4. nothing unfinished left in the copy
        for word in ["Placeholder", "placeholder copy", "Lorem ipsum", "TODO", "FIXME"]:
            if word in html:
                fails.append(f"{page}: leftover text '{word}'")

        # 5. mobile viewport tag
        if "width=device-width" not in html:
            fails.append(f"{page}: missing responsive viewport meta tag")

        # 6. share tags need absolute URLs to work
        for prop in ["og:image", "og:url"]:
            m = re.search(rf'property="{prop}" content="([^"]+)"', html)
            if m and not m.group(1).startswith("http"):
                warns.append(f"{page}: {prop} is relative ('{m.group(1)}') — link previews "
                             f"won't render until it's a full https:// URL")

        # 7. page weight
        kb = os.path.getsize(os.path.join(ROOT, page)) / 1024
        notes.append(f"{page}: {kb:.0f} KB of HTML")
        if kb > 400:
            warns.append(f"{page} is {kb:.0f} KB — are images base64-inlined again?")

    imgs = [d for d in disk if d.startswith("images/") and d.endswith((".webp", ".jpg", ".png"))]
    mb = sum(os.path.getsize(os.path.join(ROOT, i)) for i in imgs) / 1024 / 1024
    notes.append(f"{len(imgs)} image files, {mb:.1f} MB total")
    for i in imgs:
        size = os.path.getsize(os.path.join(ROOT, i)) / 1024
        if size > 600:
            warns.append(f"{i} is {size:.0f} KB — consider re-exporting smaller")


def browser():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        notes.append("--browser skipped: playwright not installed")
        return
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w, label in [(1440, "desktop"), (820, "tablet"), (390, "mobile")]:
            for page in PAGES:
                pg = b.new_page(viewport={"width": w, "height": 900})
                errors, reqfail = [], []
                pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                pg.on("requestfailed", lambda r: reqfail.append(r.url.split("/")[-1]))
                pg.goto("file://" + os.path.join(ROOT, page))
                pg.wait_for_timeout(1000)
                for _ in range(20):
                    pg.mouse.wheel(0, 800); pg.wait_for_timeout(200)
                pg.wait_for_timeout(1200)
                pg.evaluate("async()=>{await Promise.all([...document.images]"
                            ".map(i=>i.decode().catch(()=>{})))}")

                broken = pg.evaluate("[...document.images].filter(i=>i.getAttribute('src')"
                                     "&&i.naturalWidth===0).map(i=>i.getAttribute('src'))")
                for s in broken:
                    fails.append(f"{page} @{w}px: image never loaded — {s}")

                # nothing may spill outside the viewport (horizontal scroll = broken mobile)
                overflow = pg.evaluate("document.documentElement.scrollWidth - "
                                       "document.documentElement.clientWidth")
                if overflow > 2:
                    fails.append(f"{page} @{w}px: page scrolls sideways by {overflow}px")

                # gallery photos must keep their true proportions (no cropped heads)
                cropped = pg.evaluate("""() => [...document.querySelectorAll('.gal-item img')]
                    .filter(i=>{const r=i.getBoundingClientRect();
                    return Math.abs(r.width/r.height - i.naturalWidth/i.naturalHeight)>0.02;})
                    .map(i=>i.getAttribute('src'))""")
                for c in cropped:
                    fails.append(f"{page} @{w}px: gallery photo is being cropped — {c}")

                # tap targets big enough on phones
                if w == 390:
                    small = pg.evaluate("""() => [...document.querySelectorAll('a,button')]
                        .filter(e=>{const r=e.getBoundingClientRect();
                        return r.width>0 && r.height>0 && r.height<24;}).length""")
                    if small:
                        warns.append(f"{page} @{w}px: {small} tap targets under 24px tall")

                for e in set(errors):
                    fails.append(f"{page} @{w}px: JS console error — {e[:90]}")
                for r in set(reqfail):
                    fails.append(f"{page} @{w}px: request failed — {r}")
                pg.close()

        # lightbox opens and closes
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto("file://" + os.path.join(ROOT, "index.html")); pg.wait_for_timeout(1200)
        pg.evaluate("document.querySelector('#gallery').scrollIntoView()"); pg.wait_for_timeout(1200)
        img = pg.query_selector(".gal-item.shot img")
        if img:
            img.click(); pg.wait_for_timeout(500)
            if not pg.eval_on_selector("#lb", "e=>e.classList.contains('on')"):
                fails.append("lightbox did not open on click")
            pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
            if pg.eval_on_selector("#lb", "e=>e.classList.contains('on')"):
                fails.append("lightbox did not close on Escape")
        else:
            warns.append("no gallery photos found to test the lightbox")
        pg.close()
        b.close()


if __name__ == "__main__":
    check()
    if "--browser" in sys.argv:
        browser()

    print("\n" + "=" * 62)
    print("  TRUE PATH MANAGEMENT — PRE-FLIGHT")
    print("=" * 62)
    for n in notes:
        print(f"  ·  {n}")
    if warns:
        print(f"\n  {len(warns)} WARNING(S) — review, not necessarily blocking:")
        for w in warns:
            print(f"     ! {w}")
    if fails:
        print(f"\n  {len(fails)} PROBLEM(S) — fix before going live:")
        for f in fails:
            print(f"     X {f}")
        print("\n  RESULT: NOT READY\n")
        sys.exit(1)
    print("\n  RESULT: PASS — safe to deploy\n")
    sys.exit(0)
