Gallery photos live here.

Current set (referenced from the #gallery section of index.html):
  01-panel            SINC Conference panel
  02-school-visit     community appearance
  03-radio-k104       radio appearance
  04-brand-event      brand partnership
  05-football-camp    Nyheim Hines Camp 2025
  06-browns-camp      Cleveland Browns training camp
  07-conference-gw    George Washington University
  08-sinc-stage       SINC 2026 stage
  09-stadium          Highmark Stadium postgame
  10-youth-outreach   elementary school visit

Each exists as .webp (what the page loads) and .jpg (backup / re-crop source).

To add another: export ~1500px on the long edge, convert to WebP at
squoosh.app, drop it here, then copy an existing <figure> in index.html and
update src, alt, width, height, and caption.

If a photo's subject sits off to one side and the tile crop cuts them out, add
an inline style to that img, e.g. style="object-position:78% center" — that is
how the SINC stage photo is handled.
