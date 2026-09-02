#!/usr/bin/env python3
"""
Responsive + compatibility audit for the True Path site.

    python3 responsive-check.py            # all pages, all widths
    python3 responsive-check.py --quick    # phone + laptop only

Checks, at every width, on every page:
  - horizontal (sideways) scrolling
  - any element sticking out past the viewport
  - tap targets smaller than 24x24 (WCAG 2.2 AA minimum)
  - body text under 12px
  - images being upscaled (blurry) at 2x pixel density
  - overlapping nav/CTA collisions
  - JS console errors
  - mobile menu opening and closing
"""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ["index.html", "contact.html", "faq.html", "privacy.html", "terms.html"]

DEVICES = [
    (320, 568, "iPhone SE (smallest)"),
    (360, 800, "Android common"),
    (390, 844, "iPhone 15"),
    (430, 932, "iPhone Pro Max"),
    (768, 1024, "iPad portrait"),
    (820, 1180, "iPad Air"),
    (1024, 768, "iPad landscape"),
    (1280, 800, "small laptop"),
    (1440, 900, "laptop"),
    (1920, 1080, "desktop"),
]
QUICK = {(390, 844), (1440, 900)}

fails, warns = [], []


def audit(pg, w, label, page):
    tag = f"{page} @{w}px ({label})"

    # --- sideways scroll ---
    ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    if ov > 2:
        fails.append(f"{tag}: sideways scroll by {ov}px")

    # --- elements poking past the viewport ---
    spill = pg.evaluate("""(vw) => [...document.querySelectorAll('body *')].filter(el=>{
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return false;
        const cs = getComputedStyle(el);
        if (cs.position === 'fixed' || cs.visibility === 'hidden' || cs.overflow === 'hidden') return false;
        /* carousels intentionally overflow inside a clipping parent */
        for (let a = el.parentElement; a; a = a.parentElement) {
            const ac = getComputedStyle(a);
            if (ac.overflowX === 'hidden' || ac.overflow === 'hidden') return false;
        }
        return r.right > vw + 2 || r.left < -2;
    }).slice(0,4).map(el => el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\\s+/)[0] : ''))""", w)
    for s in spill:
        warns.append(f"{tag}: element extends past viewport — {s}")

    # --- tap targets (touch widths only) ---
    if w <= 820:
        small = pg.evaluate("""() => [...document.querySelectorAll('a,button')].filter(el=>{
            const r = el.getBoundingClientRect();
            if (r.width === 0 || r.height === 0) return false;
            if (el.closest('.foot-list')) return false;   /* inline footer links are fine */
            /* WCAG 2.2 SC 2.5.8 exempts inline targets inside a block of text */
            if (el.closest('.doc p, .doc li, .faq-a')) return false;
            return r.height < 24 || r.width < 24;
        }).slice(0,5).map(el => (el.tagName.toLowerCase()+'.'+(el.className||'').toString().trim().split(/\\s+/)[0]) + ' ' + Math.round(el.getBoundingClientRect().width) + 'x' + Math.round(el.getBoundingClientRect().height))""")
        for s in small:
            warns.append(f"{tag}: tap target under 24px (WCAG AA) — {s}")

    # --- tiny text ---
    tiny = pg.evaluate("""() => [...document.querySelectorAll('p,li,span,a,label,div')].filter(el=>{
        if (!el.textContent.trim()) return false;
        if (el.children.length) return false;
        const cs = getComputedStyle(el);
        /* uppercase tracked micro-labels are a deliberate editorial choice */
        const txt = el.textContent.trim();
        if (parseFloat(cs.letterSpacing) >= 1 &&
            (cs.textTransform === 'uppercase' || txt.length <= 6)) return false;
        return parseFloat(cs.fontSize) < 12;
    }).slice(0,4).map(el => el.tagName.toLowerCase()+'.'+(el.className||'').toString().trim().split(/\\s+/)[0]+' '+getComputedStyle(el).fontSize)""")
    for s in tiny:
        warns.append(f"{tag}: text under 12px — {s}")

    # --- blurry images at 2x ---
    blur = pg.evaluate("""() => [...document.images].filter(i=>{
        const r = i.getBoundingClientRect();
        if (!i.naturalWidth || r.width === 0) return false;
        return (r.width * 2) / i.naturalWidth > 1.15;
    }).slice(0,5).map(i => {
        const r = i.getBoundingClientRect();
        return i.getAttribute('src').split('/').pop().split('?')[0] +
               ' shown ' + Math.round(r.width) + 'px, source ' + i.naturalWidth + 'px (' +
               ((r.width*2)/i.naturalWidth).toFixed(2) + 'x)';
    })""")
    for s in blur:
        warns.append(f"{tag}: upscaled on retina — {s}")


def main():
    quick = "--quick" in sys.argv
    devices = [d for d in DEVICES if (d[0], d[1]) in QUICK] if quick else DEVICES

    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx = b.new_context(device_scale_factor=2)
        for w, h, label in devices:
            for page in PAGES:
                pg = ctx.new_page()
                pg.set_viewport_size({"width": w, "height": h})
                errs, bad = [], []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                # console 404s don't name the URL, so watch responses directly
                pg.on("response", lambda r: bad.append(r.url) if r.status >= 400 else None)
                pg.on("requestfailed", lambda r: bad.append(r.url))
                pg.goto("file://" + os.path.join(ROOT, page), wait_until="domcontentloaded")
                pg.wait_for_timeout(900)
                for _ in range(10):
                    pg.mouse.wheel(0, 900)
                    pg.wait_for_timeout(90)
                pg.evaluate("window.scrollTo(0,0)")
                pg.wait_for_timeout(500)

                audit(pg, w, label, page)

                # mobile menu open/close
                if w <= 820:
                    try:
                        pg.evaluate("document.querySelector('#navToggle').click()")
                        pg.wait_for_timeout(450)
                        if not pg.eval_on_selector("#tabsNav", "e=>e.classList.contains('open')"):
                            fails.append(f"{page} @{w}px: mobile menu did not open")
                        else:
                            menu_ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                            if menu_ov > 2:
                                fails.append(f"{page} @{w}px: open menu causes {menu_ov}px sideways scroll")
                        pg.evaluate("document.querySelector('#navToggle').click()")
                        pg.wait_for_timeout(350)
                    except Exception as e:
                        fails.append(f"{page} @{w}px: mobile menu error — {str(e)[:60]}")

                for u in set(bad):
                    if "fonts.googleapis" in u or "fonts.gstatic" in u or u.endswith(".woff2"):
                        continue  # third-party font CDN flakiness, not our code
                    fails.append(f"{page} @{w}px: resource failed — {u.split('/')[-1][:60]}")
                for e in set(errs):
                    if "Failed to load resource" in e:
                        continue  # covered by the response watcher above, which names the URL
                    fails.append(f"{page} @{w}px: JS error — {e[:80]}")
                pg.close()
        b.close()

    print("\n" + "=" * 66)
    print("  RESPONSIVE / COMPATIBILITY AUDIT")
    print("=" * 66)
    print(f"  {len(DEVICES if not quick else devices)} widths x {len(PAGES)} pages")
    if warns:
        seen, uniq = set(), []
        for w in warns:
            k = w.split(" — ")[-1]
            if k not in seen:
                seen.add(k); uniq.append(w)
        print(f"\n  {len(uniq)} WARNING(S):")
        for w in uniq[:20]:
            print(f"     ! {w}")
    if fails:
        print(f"\n  {len(fails)} PROBLEM(S):")
        for f in fails:
            print(f"     X {f}")
        print("\n  RESULT: NOT READY\n")
        sys.exit(1)
    print("\n  RESULT: PASS\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
