TRUE PATH MANAGEMENT — UPDATE PACKAGE
=====================================

Only the NEW and CHANGED files. Your existing images (logos, the other
seven athlete photos, gallery 01-10, Jamond's avatar) are untouched.

IMPORTANT: every new photo has been RENAMED since the last package.
Upload the files from THIS zip, not the originals off your phone or
desktop. The names must match exactly.


WHAT GOES WHERE
---------------
  index.html                    REPLACES your current one
  team.html                     REPLACES the previous version

  images/gallery/
    11-bears-smokehouse.jpg     Bear's Smokehouse BBQ
    12-pinnock-camp.jpg         Jason Pinnock Football Camp
    13-pinnock-camp-crowd.jpg   Jason Pinnock Football Camp (crowd)
    14-gainbridge.jpg           Gainbridge Fieldhouse   <- was broken
    15-jersey-mikes.png         Jersey Mike's
    16-hurricanes.jpg           Carolina Hurricanes
    17-texans-camp.jpg          Houston Texans training camp
    18-texans-camp-group.jpg    Houston Texans training camp (group)

  images/athletes/
    navonn-barrett.jpg          Navonn Barrett
    kaleb-brown.jpg             Kaleb Brown

  images/team/                  CREATE THIS FOLDER
    khalil-baker.png            Khalil Baker            <- was broken
    taylor-wilson.png           Taylor Wilson           <- was broken


WHY THOSE THREE WEREN'T LOADING
-------------------------------
Two different problems:

1. Mangled filenames. The Gainbridge photo was named
   "DSC04953 copy.jpeg" on your machine, with a SPACE. Khalil's was
   "image (13).png", with a space and parentheses. Those characters
   got converted to underscores somewhere in transit, so the page was
   asking for a file that didn't exist under that name. Both are now
   plain lowercase names with no spaces.

2. Missing folder. Taylor's filename was fine, which means the
   images/team/ folder itself never got created - that would break
   BOTH team headshots at once, which is exactly what you saw.

   GitHub has no "new folder" button. Use Add file > Create new file,
   type  images/team/khalil-baker.png  in the name box (the slashes
   create the folders), commit, then upload the real file over it.
   Once the folder exists, Taylor's drops in normally.


RUN THE IMAGE CHECK FIRST
-------------------------
imagecheck.html is included. Upload it, open yoursite.com/imagecheck.html
and it lists every image the site expects, marking each FOUND or MISSING.
Missing ones sort to the top. That tells you in five seconds exactly which
file or folder name is wrong, instead of hunting page by page.
Delete the file once everything passes.


ALSO IN THIS BUILD
------------------
Athlete card borders are now identical everywhere, including the scrolling
strip at the top of the homepage. That strip previously had NO border on
any card, so photos with their own background (Navonn's grey studio,
Kaleb's stadium shot) read as loose rectangles.

If an image was uploaded under an older filename from a previous package,
the page now retries that older name automatically instead of showing a
gap. Best to fix the filename anyway, but nothing will look broken.

The "Jamond DuBose / Founder / Bio" section has been REMOVED from the
bottom of the homepage. That content now lives only on Meet the Team.

Because that section was the target of the "About" nav tab, the About
tab and its footer link were removed too - they had nowhere left to
point. Nav is now: Home, Meet the Team, Athletes, The Work, Services,
Impact, Testimonials, Get in touch. If you want an About item back it
can point at the mission copy in the Roster section instead.

Athlete cards now have a proper border around the photo, not just
around the name plate. Previously the frame only showed where a photo's
own background happened to contrast, so Navonn and Kaleb looked
different from the rest. It's set in CSS, so every athlete you add from
here on gets the same frame automatically.


STILL OUTSTANDING
-----------------
1. Jamond's avatar is images/founder/jamond-dubose-avatar.webp, the
   same file your homepage Founder section already uses. Nothing to
   upload for him.

2. Two internal build comments remain in the source of both HTML
   files, readable via View Source. One names Brandy and describes a
   testimonial positioning conflict.

3. The stat block reads "Nine athletes represented across the NFL,
   NBA, and Division I." Confirm that number with Jamond.


AFTER UPLOADING
---------------
Hard-refresh: Cmd/Ctrl + Shift + R. GitHub Pages caches hard and a
normal refresh will often still serve the old page.

If something still doesn't appear, open it directly in the browser:
  yoursite.com/images/team/khalil-baker.png
A 404 means the file or folder name doesn't match. That check takes
five seconds and tells you exactly which one is wrong.
