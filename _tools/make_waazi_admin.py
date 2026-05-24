"""Generate the four Wa'azi admin pages by cloning the existing Song admin pages
and applying terminology + theme transforms.

Source → Destination map:
  shurafah_admin_artist_management.html   → shurafah_admin_preacher_management.html
  shurafah_song_management.html           → shurafah_admin_waazi_management.html
  shurafah_admin_categories.html          → shurafah_admin_waazi_categories.html
  shurafah_admin_playlist_management.html → shurafah_admin_waazi_series.html

The transforms are case-sensitive word substitutions for terminology
("Artist" → "Preacher", "Song" → "Lecture", etc). We also update the <title> tag
and any visible H1/H2 page headings via an annotation rule.

The bottom of each generated file gets a banner that links to its Song
equivalent so admins can switch contexts.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Order matters: longer / more specific phrases first so they win the substitution.
COMMON_SUBS_PREACHER = [
    # Title / nav
    ("Artist Management", "Preacher Management"),
    ("Manage Artists", "Manage Preachers"),
    ("Add Artist", "Add Preacher"),
    ("Edit Artist", "Edit Preacher"),
    ("Delete Artist", "Delete Preacher"),
    ("artist profile", "preacher profile"),
    ("Artist Profile", "Preacher Profile"),
    ("Artists", "Preachers"),
    ("Artist", "Preacher"),
    ("artists", "preachers"),
    ("artist", "preacher"),
    # Songs → Lectures
    ("Song Management", "Lecture Management"),
    ("Songs", "Lectures"),
    ("song count", "lecture count"),
    ("Total Songs", "Total Lectures"),
    ("songs", "lectures"),
    # Emojis (visual cues)
    ("🎤", "🎙️"),
]

COMMON_SUBS_WAAZI = [
    ("Song Management", "Wa'azi Management"),
    ("Add Song", "Add Lecture"),
    ("Add New Song", "Add New Lecture"),
    ("Edit Song", "Edit Lecture"),
    ("Delete Song", "Delete Lecture"),
    ("Manage Songs", "Manage Lectures"),
    ("Total Songs", "Total Lectures"),
    ("All Songs", "All Lectures"),
    ("Trending Songs", "Trending Lectures"),
    ("Top Songs", "Top Lectures"),
    ("Featured Songs", "Featured Lectures"),
    ("Recently Added Songs", "Recently Added Lectures"),
    ("songs", "lectures"),
    ("Songs", "Lectures"),
    ("a song", "a lecture"),
    ("the song", "the lecture"),
    ("this song", "this lecture"),
    ("a Song", "a Lecture"),
    ("the Song", "the Lecture"),
    ("Song?", "Lecture?"),
    ("Song ", "Lecture "),  # generic — must come AFTER multi-word
    (" song ", " lecture "),
    (" song.", " lecture."),
    (" song,", " lecture,"),
    ("Audio file", "Audio lecture"),
    # Reusing the same iconography but with mic
    ("🎤", "🎙️"),
]

COMMON_SUBS_CATEGORIES = [
    # Make this page Wa'azi-categories-specific
    ("Categories Management", "Wa'azi Categories"),
    ("Song Categories", "Lecture Categories"),
    ("Manage Categories", "Manage Wa'azi Categories"),
    ("category of songs", "category of lectures"),
    ("songs in this category", "lectures in this category"),
    ("Songs", "Lectures"),
    ("songs", "lectures"),
    # Replace existing categories with Wa'azi ones inline where they appear as strings
    ("Ashura", "Tafsir"),
    ("Maulud", "Aqeedah"),
    ("Shuhada", "Fiqh"),
    ("Shurafah", "Seerah"),
    ("Shairai", "Hadith"),
    ("Ahlul-baiti", "Akhlaq"),
]

COMMON_SUBS_SERIES = [
    ("Playlist Management", "Wa'azi Series Management"),
    ("Playlists", "Series"),
    ("Playlist", "Series"),
    ("playlists", "series"),
    ("playlist", "series"),
    ("Songs", "Lectures"),
    ("songs", "lectures"),
]

# Tasks
TASKS = [
    {
        "src": "shurafah_admin_artist_management.html",
        "dst": "shurafah_admin_preacher_management.html",
        "subs": COMMON_SUBS_PREACHER,
        "title": "Shurafah Admin — Preacher Management",
        "banner_other": ("Songs view: Artist Management", "shurafah_admin_artist_management.html"),
    },
    {
        "src": "shurafah_song_management.html",
        "dst": "shurafah_admin_waazi_management.html",
        "subs": COMMON_SUBS_WAAZI,
        "title": "Shurafah Admin — Wa'azi Management",
        "banner_other": ("Songs view: Song Management", "shurafah_song_management.html"),
    },
    {
        "src": "shurafah_admin_categories.html",
        "dst": "shurafah_admin_waazi_categories.html",
        "subs": COMMON_SUBS_CATEGORIES,
        "title": "Shurafah Admin — Wa'azi Categories",
        "banner_other": ("Songs view: Categories", "shurafah_admin_categories.html"),
    },
    {
        "src": "shurafah_admin_playlist_management.html",
        "dst": "shurafah_admin_waazi_series.html",
        "subs": COMMON_SUBS_SERIES,
        "title": "Shurafah Admin — Wa'azi Series",
        "banner_other": ("Songs view: Playlists", "shurafah_admin_playlist_management.html"),
    },
]


def apply_subs(text: str, subs: list[tuple[str, str]]) -> str:
    for old, new in subs:
        text = text.replace(old, new)
    return text


def patch_title(text: str, title: str) -> str:
    return re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", text, count=1)


def add_context_banner(text: str, label: str, href: str, scope: str = "Wa'azi") -> str:
    """Inject a small 'Songs ↔ Wa'azi' scope toggle just after the opening <body>."""
    banner = (
        '<div id="waazi-scope-banner" style="position:fixed;top:8px;left:50%;'
        'transform:translateX(-50%);z-index:9999;background:linear-gradient(135deg,#C8860A,#E8A020);'
        'color:#1A0800;padding:5px 14px 5px 12px;border-radius:50px;'
        'font-family:\'Syne\',sans-serif;font-size:11px;font-weight:700;'
        'box-shadow:0 6px 20px rgba(200,134,10,.35);display:flex;align-items:center;gap:8px;'
        'pointer-events:auto;">'
        f'<span>🎙️ {scope} Admin</span>'
        f'<a href="{href}" style="color:#1A0800;text-decoration:underline;font-weight:600;">'
        f'Switch &rarr; {label}</a>'
        '<span onclick="document.getElementById(\'waazi-scope-banner\').remove()" '
        'style="cursor:pointer;padding-left:6px;opacity:.7;">✕</span>'
        '</div>\n'
    )
    return text.replace("<body>", "<body>\n" + banner, 1)


def run():
    for t in TASKS:
        src = ROOT / t["src"]
        dst = ROOT / t["dst"]
        if not src.exists():
            print(f"  skip (no source): {t['src']}")
            continue
        text = src.read_text(encoding="utf-8")
        text = apply_subs(text, t["subs"])
        text = patch_title(text, t["title"])
        label, href = t["banner_other"]
        text = add_context_banner(text, label, href)
        dst.write_text(text, encoding="utf-8", newline="")
        print(f"  ok wrote {t['dst']} ({len(text):,} chars)")


if __name__ == "__main__":
    run()
