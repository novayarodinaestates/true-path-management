TRUE PATH MANAGEMENT — UPDATE PACKAGE
=====================================

This contains only the NEW and CHANGED files. Your existing images
(logos, the other athlete photos, gallery 01-10, Jamond's avatar)
are untouched and stay where they are.

Drop this on top of your repo, keeping the folder structure exactly:

  index.html                      <- REPLACES your current one
  team.html                       <- NEW page

  images/gallery/
    IMG_0822.jpeg                 Bear's Smokehouse BBQ
    IMG_0843.jpeg                 Jason Pinnock Football Camp
    IMG_0820.jpeg                 Jason Pinnock Football Camp (crowd)
    DSC04953_copy.jpeg            Gainbridge Fieldhouse
    C1854EBB-31E9-44AB-8E3A-19204A6D4D5C.png   Jersey Mike's
    IMG_4236.jpeg                 Carolina Hurricanes

  images/athletes/
    IMG_2568.jpeg                 Navonn Barrett
    IMG_6584.jpeg                 Kaleb Brown

  images/team/                    <- this folder is NEW
    image__13_.png                Khalil Baker
    taylorheadshot.png            Taylor Wilson


FILENAMES ARE CASE-SENSITIVE
----------------------------
GitHub Pages runs on Linux. Upload these exactly as named. In
particular the Jersey Mike's file needs the hex in CAPS and the
.png extension in lowercase.


STILL OUTSTANDING
-----------------
1. Jamond's avatar is images/founder/jamond-dubose-avatar.webp, the
   same file your homepage Founder section already uses. Nothing to
   upload for him; it resolves once these files are live.

2. Two internal build comments are still in the source of both HTML
   files. Anyone can read them with View Source. One names Brandy and
   describes a testimonial positioning conflict.

3. The stat block reads "Nine athletes represented across the NFL,
   NBA, and Division I." Confirm that number with Jamond.


AFTER UPLOADING
---------------
Hard-refresh: Cmd/Ctrl + Shift + R. GitHub Pages caches hard and a
normal refresh will often still serve the old page.
