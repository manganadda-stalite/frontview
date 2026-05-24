"""Inject a 'Songs ↔ Wa'azi' scope banner near the top of each shared admin page.

The banner is purely additive — it does not modify any existing content. It defaults
to the Songs scope (existing behaviour) and provides a quick link to the matching
Wa'azi page for pages that have one. For pages that already cover both content types
(dashboard, comments, activity, ads, downloads), it shows an info note.

Pages skipped: pages that are themselves Wa'azi pages, or that don't render in the
admin shell (login_page, register_page, etc).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (song-side-file, optional Wa'azi-equivalent, label)
# When the Wa'azi equivalent is None, we mark the page as "covers both".
TARGETS = [
    # Direct Wa'azi parallels
    ("shurafah_song_management.html",          "shurafah_admin_waazi_management.html",  "Wa'azi Management"),
    ("shurafah_admin_artist_management.html",  "shurafah_admin_preacher_management.html","Preacher Management"),
    ("shurafah_admin_categories.html",         "shurafah_admin_waazi_categories.html",  "Wa'azi Categories"),
    ("shurafah_admin_playlist_management.html","shurafah_admin_waazi_series.html",      "Wa'azi Series"),
    # Shared / covers-both
    ("shurafah_admin_dashboard.html",          None, None),
    ("shurafah_admin_featured_trending.html",  None, None),
    ("shurafah_admin_comments_reports.html",   None, None),
    ("shurafah_admin_activity_logs.html",      None, None),
    ("shurafah_ads_management.html",           None, None),
    ("shurafah_download_analytics.html",       None, None),
]

BANNER_ID = "shurafah-scope-banner"


def banner_html(waazi_href: str | None, waazi_label: str | None) -> str:
    if waazi_href:
        # Switchable banner with link to the Wa'azi version.
        right = (
            f'<a href="{waazi_href}" '
            'style="display:flex;align-items:center;gap:5px;background:linear-gradient(135deg,#C8860A,#E8A020);'
            'color:#1A0800;text-decoration:none;padding:4px 10px;border-radius:50px;font-weight:700;">'
            f'🎙️ Switch &rarr; {waazi_label}</a>'
        )
    else:
        right = (
            '<span style="background:rgba(200,134,10,.15);color:#E8A020;border:1px solid rgba(200,134,10,.3);'
            'padding:3px 9px;border-radius:50px;font-weight:700;font-size:10px;">'
            '🎙️ Includes Wa\'azi data</span>'
        )

    return (
        f'<div id="{BANNER_ID}" '
        'style="position:fixed;top:8px;left:50%;transform:translateX(-50%);z-index:9999;'
        'background:rgba(15,20,32,.92);backdrop-filter:blur(10px);'
        'border:1px solid rgba(255,255,255,.08);border-radius:50px;'
        'padding:5px 10px 5px 12px;font-family:\'Syne\',sans-serif;font-size:11px;font-weight:700;'
        'color:#F0F4FF;box-shadow:0 8px 24px rgba(0,0,0,.45);'
        'display:flex;align-items:center;gap:8px;pointer-events:auto;">'
        '<span style="display:flex;align-items:center;gap:5px;color:#FFB347;">'
        '<span style="font-size:13px;">🎵</span>Songs Admin</span>'
        f'{right}'
        f'<span onclick="document.getElementById(\'{BANNER_ID}\').remove()" '
        'style="cursor:pointer;padding:0 4px;opacity:.55;font-size:13px;">✕</span>'
        '</div>'
    )


def inject(path: Path, waazi_href: str | None, waazi_label: str | None) -> bool:
    text = path.read_text(encoding="utf-8")

    # Idempotent: if banner already present, replace it in place.
    pattern = re.compile(
        r'<div id="' + re.escape(BANNER_ID) + r'"[^<]*?(?:<[^>]+>[^<]*?)*?</div>',
        re.DOTALL,
    )
    new_banner = banner_html(waazi_href, waazi_label)

    if BANNER_ID in text:
        # Remove the previous banner first; we'll re-inject fresh.
        text = pattern.sub("", text, count=1)

    # Insert right after the opening <body> tag.
    new_text, n = re.subn(r"<body([^>]*)>", lambda m: f"<body{m.group(1)}>\n" + new_banner + "\n", text, count=1)
    if n != 1:
        print(f"  !! could not find <body> in {path.name}")
        return False

    path.write_text(new_text, encoding="utf-8", newline="")
    print(f"  ok injected scope banner into {path.name}")
    return True


def main():
    for src_file, waazi_href, waazi_label in TARGETS:
        p = ROOT / src_file
        if not p.exists():
            print(f"  skip (missing): {src_file}")
            continue
        inject(p, waazi_href, waazi_label)


if __name__ == "__main__":
    main()
