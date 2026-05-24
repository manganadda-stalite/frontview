"""Replace the existing bottom nav with a 5-item nav: Home / Wa'azi / Explore / Favourites / Profile.

Wraps each item in an anchor tag so navigation works. Sets the `active` state per page.
The existing CSS (`.ni`, `.ni.on`, `.bnav`, etc.) works on anchors just as well as on divs.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Per-page mapping: file -> active key (one of: home, waazi, explore, favourites, profile, none)
# `none` = no item highlighted (used for sub-pages and "see all" pages)
PAGE_ACTIVE = {
    "song_portal_web.html":            "home",
    "shurafah_waazi.html":             "waazi",
    "shurafah_explore.html":           "explore",
    "favourites_page.html":            "favourites",
    "user_profile_page.html":          "profile",

    # Sub-pages — no item highlighted; user navigated here from a section above.
    "song_detail_page.html":           "none",
    "artist_profile_page.html":        "none",
    "shurafah_waazi_detail.html":      "none",
    "shurafah_preacher_profile.html":  "none",

    # "See all" listing pages for songs — highlight Home (they belong to the songs flow).
    "all_categories.html":             "home",
    "all_featured_songs.html":         "home",
    "all_recently_added.html":         "home",
    "all_subcategories.html":          "home",
    "all_top_artists.html":            "home",
    "all_top_songs.html":              "home",
    "all_trending_songs.html":         "home",

    # "See all" listing pages for Wa'azi — highlight Wa'azi.
    "all_top_preachers.html":          "waazi",
    "all_top_lectures.html":           "waazi",
    "all_trending_lectures.html":      "waazi",
    "all_featured_lectures.html":      "waazi",
    "all_recent_lectures.html":        "waazi",
    "all_waazi_categories.html":       "waazi",
    "all_waazi_subcategories.html":    "waazi",
}

HOME_SVG    = '<svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>'
WAAZI_SVG   = '<svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>'
EXPLORE_SVG = '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
FAV_SVG     = '<svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'
PROFILE_SVG = '<svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'

ITEMS = [
    ("home",       "song_portal_web.html",  HOME_SVG,    "Home"),
    ("waazi",      "shurafah_waazi.html",   WAAZI_SVG,   "Wa'azi"),
    ("explore",    "shurafah_explore.html", EXPLORE_SVG, "Explore"),
    ("favourites", "favourites_page.html",  FAV_SVG,     "Favourites"),
    ("profile",    "user_profile_page.html",PROFILE_SVG, "Profile"),
]

ANCHOR_STYLE = 'text-decoration:none;color:inherit;'


def build_bnav(active_key: str) -> str:
    parts = ['  <!-- BOTTOM NAV (Home · Wa\'azi · Explore · Favourites · Profile) -->',
             '  <div class="bnav">']
    for key, href, svg, label in ITEMS:
        on = " on" if key == active_key else ""
        parts.append(
            f'    <a class="ni{on}" href="{href}" style="{ANCHOR_STYLE}">'
            f'{svg}'
            f'<div class="nl">{label}</div>'
            f'</a>'
        )
    parts.append('  </div>')
    return "\n".join(parts) + "\n"


OPEN_DIV_RE = re.compile(r"<div\b", re.IGNORECASE)
CLOSE_DIV_RE = re.compile(r"</div>", re.IGNORECASE)


def find_balanced_close(text: str, start: int) -> int:
    """Given `start` pointing at the `<` of an opening `<div ...>`, return the index
    immediately *after* its matching `</div>`."""
    depth = 0
    i = start
    n = len(text)
    while i < n:
        op = OPEN_DIV_RE.search(text, i)
        cl = CLOSE_DIV_RE.search(text, i)
        if cl is None:
            raise ValueError("unbalanced <div> — no closing tag found")
        if op is not None and op.start() < cl.start():
            depth += 1
            i = op.end()
        else:
            depth -= 1
            i = cl.end()
            if depth == 0:
                return i
    raise ValueError("unbalanced <div> — reached EOF")


def update_file(path: Path, active: str) -> bool:
    text = path.read_text(encoding="utf-8")
    new_block = build_bnav(active)

    # Find the opening tag, including any leading comment on the same line / above.
    m = re.search(r'<div class="bnav">', text)
    if not m:
        print(f"  !! could not locate <div class=\"bnav\"> in {path.name}")
        return False

    # Determine the byte to start replacing — include indentation and a leading
    # `<!-- BOTTOM NAV ... -->` comment on the previous non-empty line, if present.
    start = m.start()
    line_start = text.rfind("\n", 0, start) + 1
    # If the line above is a "BOTTOM NAV" comment, swallow it (and its newline) too.
    prev_line_end = line_start - 1  # index of '\n' or -1 if at top
    if prev_line_end > 0:
        prev_line_start = text.rfind("\n", 0, prev_line_end) + 1
        prev_line = text[prev_line_start:prev_line_end]
        if "BOTTOM NAV" in prev_line.upper() or "<!--" in prev_line and "NAV" in prev_line.upper():
            line_start = prev_line_start

    end = find_balanced_close(text, m.start())
    # Swallow the trailing newline that follows the closing </div>, if any, to keep file tidy.
    if end < len(text) and text[end] == "\n":
        end += 1

    new_text = text[:line_start] + new_block + text[end:]

    if new_text == text:
        print(f"  -- no change for {path.name}")
        return False
    path.write_text(new_text, encoding="utf-8", newline="")
    print(f"  ok updated {path.name} (active={active})")
    return True


def main():
    failed = []
    for filename, active in PAGE_ACTIVE.items():
        path = ROOT / filename
        if not path.exists():
            print(f"  skip (missing): {filename}")
            continue
        if not update_file(path, active):
            failed.append(filename)
    if failed:
        print(f"\nFAILED: {failed}")
        sys.exit(1)
    print("\nAll bnav updates completed.")


if __name__ == "__main__":
    main()
