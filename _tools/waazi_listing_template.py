"""Generate the six Wa'azi listing pages (all_top_preachers, all_top_lectures,
all_trending_lectures, all_featured_lectures, all_recent_lectures, all_waazi_categories,
all_waazi_subcategories) from a single compact template.

These pages mirror the structure of the existing all_*.html song pages — search bar,
filter pills, paginated grid/list — but use Wa'azi (gold) theming and lecture data.
"""

from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Shared CSS — gold-accented Wa'azi theme.
CSS = r"""
:root{
  --bg:#05070F;--surface:#0A0E1A;--surface2:#0F1525;--surface3:#141B2E;--surface4:#1A2238;
  --accent:#C8860A;--accent2:#E8A020;--accent3:#F5C842;
  --blue:#4D9FFF;--green:#2ECC8F;--purple:#9B6BFF;--pink:#FF4D8F;
  --text:#F0F4FF;--text2:#8A94B0;--text3:#4A5270;
  --border:rgba(255,255,255,0.06);
}
body.light{
  --bg:#F4F6FC;--surface:#FFFFFF;--surface2:#E8ECF7;--surface3:#D8DEEF;
  --text:#12172E;--text2:#5A6380;--text3:#9AA0BA;
  --border:rgba(0,0,0,0.07);
}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--bg);font-family:'DM Sans',sans-serif;color:var(--text);min-height:100vh;display:flex;flex-direction:column;}
.phone{width:100%;background:var(--bg);display:flex;flex-direction:column;min-height:100vh;position:relative;}
.scroll{flex:1;overflow-y:auto;overflow-x:hidden;scrollbar-width:none;padding-bottom:80px;}
.scroll::-webkit-scrollbar{display:none;}

/* HEADER */
.tbar{display:flex;align-items:center;justify-content:space-between;padding:14px 18px 4px;gap:10px;}
.tb-back{width:36px;height:36px;background:var(--surface);border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px solid var(--border);cursor:pointer;flex-shrink:0;text-decoration:none;color:inherit;}
.tb-back svg{width:14px;height:14px;fill:none;stroke:var(--text);stroke-width:2;}
.tb-title{flex:1;font-family:'Syne',sans-serif;font-size:18px;font-weight:800;letter-spacing:-.3px;text-align:center;background:linear-gradient(135deg,var(--accent),var(--accent2),var(--accent3));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.theme-toggle{display:inline-flex;align-items:center;gap:6px;background:var(--surface2);border-radius:50px;padding:5px 10px 5px 8px;border:1.5px solid var(--accent2);cursor:pointer;}
.tt-icon{font-size:13px;}
.tt-label{font-family:'Syne',sans-serif;font-size:10px;font-weight:700;color:var(--accent2);letter-spacing:.3px;}

/* SEARCH */
.sw{padding:10px 18px 0;}
.sb{background:var(--surface);border:1px solid var(--border);border-radius:14px;display:flex;align-items:center;gap:10px;padding:10px 14px;}
.sb svg{width:14px;height:14px;fill:none;stroke:var(--text3);stroke-width:2;flex-shrink:0;}
.sb input{background:transparent;border:none;outline:none;color:var(--text);font-size:13px;flex:1;}
.sb input::placeholder{color:var(--text3);}

/* FILTER PILLS */
.fp{display:flex;gap:7px;padding:12px 18px 0;overflow-x:auto;scrollbar-width:none;}
.fp::-webkit-scrollbar{display:none;}
.pill{flex-shrink:0;padding:6px 12px;border-radius:50px;font-family:'Syne',sans-serif;font-size:10px;font-weight:700;cursor:pointer;white-space:nowrap;background:var(--surface);color:var(--text2);border:1px solid var(--border);}
.pill.on{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#1A0800;border-color:transparent;box-shadow:0 3px 10px rgba(200,134,10,.3);}

/* CONTENT */
.shead{display:flex;justify-content:space-between;align-items:center;padding:16px 18px 8px;}
.shead-t{font-family:'Syne',sans-serif;font-size:13px;font-weight:700;}
.shead-c{font-size:10px;color:var(--text3);font-family:'Syne',sans-serif;font-weight:600;}

/* LIST */
.list{padding:0 18px;display:flex;flex-direction:column;gap:3px;}
.row{display:flex;align-items:center;gap:11px;padding:9px;border-radius:12px;cursor:pointer;text-decoration:none;color:inherit;}
.row:hover{background:var(--surface);}
.rank{width:24px;text-align:center;font-family:'Syne',sans-serif;font-size:13px;font-weight:800;color:var(--text3);flex-shrink:0;}
.rank.r1{color:var(--accent3);}.rank.r2{color:var(--text2);}.rank.r3{color:#CD7F32;}
.art{width:48px;height:48px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;}
.info{flex:1;min-width:0;}
.t{font-family:'Syne',sans-serif;font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:2px;}
.s{font-size:10px;color:var(--text2);}
.m{font-size:10px;color:var(--text3);font-family:'Syne',sans-serif;font-weight:700;flex-shrink:0;}

/* GRID (categories) */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:0 18px;}
.tile{border-radius:14px;padding:16px 14px;position:relative;overflow:hidden;cursor:pointer;border:1px solid rgba(255,255,255,.06);min-height:110px;display:flex;flex-direction:column;justify-content:flex-end;text-decoration:none;color:inherit;}
.tile-i{font-size:30px;position:absolute;top:11px;right:13px;opacity:.7;}
.tile-n{font-family:'Syne',sans-serif;font-size:13px;font-weight:800;position:relative;margin-bottom:3px;}
.tile-c{font-size:10px;color:var(--text2);position:relative;}

/* CIRCLE GRID (preachers) */
.pg{display:grid;grid-template-columns:repeat(3,1fr);gap:14px 10px;padding:0 18px;}
.pcard{text-align:center;cursor:pointer;text-decoration:none;color:inherit;}
.pavatar{width:80px;height:80px;border-radius:50%;margin:0 auto 7px;padding:2px;background:linear-gradient(135deg,var(--accent),var(--accent2),var(--accent3));}
.pavatar-inner{width:100%;height:100%;border-radius:50%;background:var(--bg);display:flex;align-items:center;justify-content:center;font-size:30px;}
.pname{font-family:'Syne',sans-serif;font-size:11px;font-weight:700;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.psub{font-size:9px;color:var(--text3);font-family:'Syne',sans-serif;font-weight:600;}

/* Pagination */
.pgn{display:flex;justify-content:center;align-items:center;gap:8px;padding:16px;}
.pgn-btn{padding:7px 13px;background:var(--surface);border:1px solid var(--border);border-radius:9px;font-family:'Syne',sans-serif;font-size:10px;font-weight:700;color:var(--text2);cursor:pointer;}
.pgn-btn.on{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#1A0800;border-color:transparent;}
.pgn-info{font-size:10px;color:var(--text3);font-family:'Syne',sans-serif;font-weight:600;}

/* gradients */
.g1{background:linear-gradient(135deg,#9B6BFF,#4D9FFF);}
.g2{background:linear-gradient(135deg,#C8860A,#E8A020);}
.g3{background:linear-gradient(135deg,#FF4D8F,#C8860A);}
.g4{background:linear-gradient(135deg,#2ECC8F,#4D9FFF);}
.g5{background:linear-gradient(135deg,#E8A020,#F5C842);}
.g6{background:linear-gradient(135deg,#4D9FFF,#9B6BFF);}
.g7{background:linear-gradient(135deg,#2ECC8F,#9B6BFF);}
.g8{background:linear-gradient(135deg,#F5C842,#FF4D8F);}

.c1{background:linear-gradient(135deg,#1A0E04,#3A1A06);}
.c2{background:linear-gradient(135deg,#04141A,#062A1A);}
.c3{background:linear-gradient(135deg,#100414,#2A0628);}
.c4{background:linear-gradient(135deg,#041A14,#062A28);}
.c5{background:linear-gradient(135deg,#1A0A14,#2A0E18);}
.c6{background:linear-gradient(135deg,#0A1424,#0E1E3A);}

/* BOTTOM NAV */
.bnav{display:flex;justify-content:space-around;align-items:center;padding:10px 8px 14px;background:var(--surface);border-top:1px solid var(--border);flex-shrink:0;position:sticky;bottom:0;z-index:10;}
.ni{display:flex;flex-direction:column;align-items:center;gap:3px;cursor:pointer;padding:5px 10px;border-radius:10px;}
.ni.on{background:rgba(200,134,10,.12);}
.ni svg{width:19px;height:19px;fill:none;stroke:var(--text3);stroke-width:2;}
.ni.on svg{stroke:var(--accent2);}
.nl{font-size:9px;font-family:'Syne',sans-serif;font-weight:700;color:var(--text3);}
.ni.on .nl{color:var(--accent2);}
"""

# Bottom nav with Wa'azi highlighted (since these are Wa'azi pages).
BNAV = """  <!-- BOTTOM NAV (Home · Wa'azi · Explore · Favourites) -->
  <div class="bnav">
    <a class="ni" href="song_portal_web.html" style="text-decoration:none;color:inherit;"><svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg><div class="nl">Home</div></a>
    <a class="ni on" href="shurafah_waazi.html" style="text-decoration:none;color:inherit;"><svg viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg><div class="nl">Wa'azi</div></a>
    <a class="ni" href="shurafah_explore.html" style="text-decoration:none;color:inherit;"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg><div class="nl">Explore</div></a>
    <a class="ni" href="favourites_page.html" style="text-decoration:none;color:inherit;"><svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg><div class="nl">Favourites</div></a>
  </div>"""

THEME_SCRIPT = """
  var toggle = document.getElementById('themeToggle');
  var ttIcon = document.getElementById('ttIcon');
  var ttLabel = document.getElementById('ttLabel');
  var body = document.body;
  function applyTheme(isLight){
    if(isLight){ body.classList.add('light'); ttIcon.textContent='☀️'; ttLabel.textContent='Light'; }
    else { body.classList.remove('light'); ttIcon.textContent='🌙'; ttLabel.textContent='Dark'; }
  }
  applyTheme(localStorage.getItem('shurafah-theme') === 'light');
  toggle.addEventListener('click', function(){
    var isLight = !body.classList.contains('light');
    applyTheme(isLight);
    localStorage.setItem('shurafah-theme', isLight ? 'light' : 'dark');
  });
  document.querySelectorAll('.pill').forEach(function(p){
    p.addEventListener('click', function(){
      var grp = p.parentElement;
      grp.querySelectorAll('.pill').forEach(function(x){ x.classList.remove('on'); });
      p.classList.add('on');
    });
  });
"""


def wrap_page(title: str, page_h1: str, content_html: str, filter_pills: list[tuple[str, str]] | None = None, show_search: bool = True) -> str:
    pills_html = ""
    if filter_pills:
        pills_html = '\n    <div class="fp">\n'
        for i, (key, label) in enumerate(filter_pills):
            on = " on" if i == 0 else ""
            pills_html += f'      <div class="pill{on}" data-filter="{key}">{label}</div>\n'
        pills_html += '    </div>\n'

    search_html = ""
    if show_search:
        search_html = """
    <div class="sw">
      <div class="sb">
        <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" placeholder="Search...">
      </div>
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Shurafah — {title}</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&family=Amiri:ital,wght@0,400;0,700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="phone">
  <div class="scroll">
    <div class="tbar">
      <a class="tb-back" href="shurafah_waazi.html"><svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg></a>
      <div class="tb-title">{page_h1}</div>
      <div class="theme-toggle" id="themeToggle">
        <span class="tt-icon" id="ttIcon">🌙</span>
        <span class="tt-label" id="ttLabel">Dark</span>
      </div>
    </div>
{search_html}
{pills_html}
{content_html}
    <div style="height:14px;"></div>
  </div>
{BNAV}
</div>
<script>{THEME_SCRIPT}</script>
</body>
</html>
"""


# ── Data ──────────────────────────────────────────────────────────
PREACHERS = [
    ("Sheikh Ahmad Gumi", "2.4M followers", "🎙️"),
    ("Sheikh Isah Ali Ibrahim", "1.8M followers", "📖"),
    ("Dr. Aminu Daurawa", "1.2M followers", "⚖️"),
    ("Sheikh Abdallah Usman", "980K followers", "🕌"),
    ("Dr. Auwal Albani", "910K followers", "🤲"),
    ("Sheikh Aliyu Maikwaru", "760K followers", "🌿"),
    ("Sheikh Yakubu Musa", "640K followers", "📿"),
    ("Sheikh Muhammad Bichi", "580K followers", "✨"),
    ("Sheikh Ibrahim Khalil", "490K followers", "🕋"),
    ("Sheikh Sani Yahaya", "420K followers", "🌙"),
    ("Sheikh Bashir Aliyu", "380K followers", "📚"),
    ("Sheikh Ja'afar Mahmud", "340K followers", "💫"),
]

LECTURES_TOP = [
    ("Hanyar Gaskiya Vol. 3", "Sh. Ahmad Gumi", "Aqeedah", "1:04:38", "1.8M plays", "🎙️", "g2"),
    ("Tafsir Suratul Baqarah", "Sh. Isah Ali Ibrahim", "Tafsir", "1:32:14", "1.5M plays", "📖", "g5"),
    ("Tauhid wa-l-Iman", "Sh. Ahmad Gumi", "Aqeedah", "48:22", "1.2M plays", "🕌", "g3"),
    ("Fiqhul Ibadah — Part 12", "Dr. Aminu Daurawa", "Fiqh", "56:18", "1.1M plays", "⚖️", "g6"),
    ("Du'as for Difficulty", "Sh. Ahmad Gumi", "Du'a", "32:08", "980K plays", "🤲", "g7"),
    ("Akhlaq al-Mu'min", "Sh. Yakubu Musa", "Akhlaq", "42:55", "910K plays", "🌿", "g4"),
    ("Seerah of the Prophet", "Sh. Abdallah Usman", "Seerah", "1:18:00", "880K plays", "🕊️", "g8"),
    ("Manners in Islam", "Sh. Aliyu Maikwaru", "Akhlaq", "44:10", "820K plays", "💫", "g2"),
    ("Hanyar Gaskiya Vol. 2", "Sh. Ahmad Gumi", "Aqeedah", "58:14", "770K plays", "📖", "g5"),
    ("Ramadan Reminders", "Sh. Auwal Albani", "Du'a", "38:42", "690K plays", "🌙", "g6"),
]

LECTURES_TRENDING = [
    ("The Path of Sincerity", "Sh. Ahmad Gumi", "Aqeedah", "52:18", "+45% this week", "🎙️", "g2"),
    ("Patience in Hardship", "Sh. Isah Ali", "Akhlaq", "44:30", "+38% this week", "🌿", "g4"),
    ("Tafsir Surah Ya-Sin", "Dr. Aminu Daurawa", "Tafsir", "1:08:22", "+34% this week", "📖", "g5"),
    ("The Six Pillars", "Sh. Abdallah Usman", "Aqeedah", "47:14", "+29% this week", "🕌", "g3"),
    ("Daily Adhkar", "Sh. Yakubu Musa", "Du'a", "28:55", "+26% this week", "🤲", "g7"),
    ("The Companions", "Sh. Auwal Albani", "Seerah", "1:14:18", "+22% this week", "🕊️", "g6"),
    ("Halal & Haram", "Dr. Aminu Daurawa", "Fiqh", "58:48", "+18% this week", "⚖️", "g8"),
    ("Faith in Modern Times", "Sh. Ahmad Gumi", "Aqeedah", "49:12", "+16% this week", "✨", "g2"),
]

LECTURES_FEATURED = [
    ("Editor's Pick: Hanyar Gaskiya", "Sh. Ahmad Gumi", "Aqeedah", "1:04:38", "Featured", "⭐", "g2"),
    ("Khutbatul Jumu'ah Live", "Sh. Isah Ali", "Khutbah", "38:22", "Featured", "🎤", "g5"),
    ("Children's Tarbiyya", "Sh. Aliyu Maikwaru", "Tarbiyya", "44:18", "Featured", "👨‍👩‍👧", "g4"),
    ("Money Matters in Islam", "Dr. Aminu Daurawa", "Fiqh", "52:55", "Featured", "💰", "g8"),
    ("Women in Islam", "Sh. Auwal Albani", "Tarbiyya", "48:30", "Featured", "🌸", "g3"),
    ("Death & The Hereafter", "Sh. Yakubu Musa", "Aqeedah", "1:12:14", "Featured", "🌅", "g6"),
]

LECTURES_RECENT = [
    ("Du'a of the 10 Days", "Dr. Auwal Albani", "Du'a", "32:44", "2 hours ago", "🤲", "g7"),
    ("Manners in Islam", "Sh. Aliyu Maikwaru", "Akhlaq", "44:10", "5 hours ago", "🌿", "g4"),
    ("Tafsir Suratul Fatihah", "Sh. Isah Ali Ibrahim", "Tafsir", "1:08:22", "Yesterday", "📖", "g5"),
    ("Hadith Number 41", "Sh. Bashir Aliyu", "Hadith", "28:18", "Yesterday", "📜", "g6"),
    ("Building Iman", "Sh. Ja'afar Mahmud", "Aqeedah", "52:42", "2 days ago", "🕌", "g3"),
    ("The Final Hour", "Sh. Sani Yahaya", "Aqeedah", "44:55", "2 days ago", "🌅", "g2"),
    ("Tahajjud & Night Prayer", "Sh. Muhammad Bichi", "Du'a", "38:14", "3 days ago", "🌙", "g7"),
    ("Charity in Islam", "Sh. Ibrahim Khalil", "Fiqh", "32:08", "3 days ago", "💝", "g8"),
]

CATEGORIES_W = [
    ("Tafsir", "Qur'anic exegesis", 312, "📖", "c1"),
    ("Aqeedah", "Islamic creed", 248, "🕌", "c2"),
    ("Fiqh", "Islamic jurisprudence", 189, "⚖️", "c3"),
    ("Seerah", "Prophetic biography", 142, "🕊️", "c4"),
    ("Hadith", "Prophetic traditions", 168, "📜", "c5"),
    ("Akhlaq", "Manners & character", 134, "🌿", "c6"),
    ("Du'a", "Supplications", 96, "🤲", "c2"),
    ("Tarbiyya", "Personal development", 108, "✨", "c3"),
    ("Khutbah", "Friday sermons", 84, "🎤", "c4"),
    ("Tasawwuf", "Spiritual purification", 72, "🌙", "c5"),
]

SUBCATEGORIES_W = [
    ("Tafsir Surah Al-Fatiha", "Tafsir", 24, "📖", "c1"),
    ("Tafsir Surah Al-Baqarah", "Tafsir", 48, "📖", "c1"),
    ("Tafsir Suratul Yaseen", "Tafsir", 22, "📖", "c1"),
    ("Tauhid Rububiyyah", "Aqeedah", 32, "🕌", "c2"),
    ("Tauhid Uluhiyyah", "Aqeedah", 28, "🕌", "c2"),
    ("Tauhid Asma was-Sifat", "Aqeedah", 18, "🕌", "c2"),
    ("Fiqh as-Salah", "Fiqh", 42, "⚖️", "c3"),
    ("Fiqh az-Zakah", "Fiqh", 36, "⚖️", "c3"),
    ("Fiqh as-Siyam", "Fiqh", 28, "⚖️", "c3"),
    ("Sahih al-Bukhari", "Hadith", 54, "📜", "c5"),
    ("Sahih Muslim", "Hadith", 42, "📜", "c5"),
    ("Forty Hadith Nawawi", "Hadith", 41, "📜", "c5"),
]


def gen_row(idx: int, item: tuple, with_rank: bool, href: str = "shurafah_waazi_detail.html") -> str:
    title, sub_a, sub_b, dur, meta, emoji, grad = item
    rank_class = "r1" if idx == 0 else "r2" if idx == 1 else "r3" if idx == 2 else ""
    rank = f'<div class="rank {rank_class}">{idx + 1}</div>' if with_rank else ""
    sub = f"{sub_a} · {sub_b} · {dur}"
    return f"""      <a class="row" href="{href}">{rank}<div class="art {grad}">{emoji}</div><div class="info"><div class="t">{title}</div><div class="s">{sub}</div></div><div class="m">{meta}</div></a>"""


def gen_lecture_list(items: list, with_rank: bool = True) -> str:
    rows = "\n".join(gen_row(i, it, with_rank) for i, it in enumerate(items))
    return f'    <div class="list">\n{rows}\n    </div>'


def gen_preacher_grid(items: list) -> str:
    cards = []
    for name, sub, emoji in items:
        cards.append(f"""      <a class="pcard" href="shurafah_preacher_profile.html">
        <div class="pavatar"><div class="pavatar-inner">{emoji}</div></div>
        <div class="pname">{name}</div>
        <div class="psub">{sub}</div>
      </a>""")
    return '    <div class="pg">\n' + "\n".join(cards) + "\n    </div>"


def gen_category_grid(items: list) -> str:
    cards = []
    for name, desc, count, emoji, bg in items:
        cards.append(f"""      <a class="tile {bg}" href="all_waazi_subcategories.html">
        <div class="tile-i">{emoji}</div>
        <div class="tile-n">{name}</div>
        <div class="tile-c">{count} lectures · {desc}</div>
      </a>""")
    return '    <div class="grid">\n' + "\n".join(cards) + "\n    </div>"


# ── Generate pages ────────────────────────────────────────────────

PAGES = {
    "all_top_preachers.html": dict(
        title="Top Preachers",
        h1="🏆 Top Preachers",
        filter_pills=[("all", "All"), ("week", "This Week"), ("month", "This Month"), ("year", "This Year"), ("alltime", "All Time")],
        content=f"""    <div class="shead"><div class="shead-t">All Preachers</div><div class="shead-c">Showing 1–12 of 248</div></div>
{gen_preacher_grid(PREACHERS)}
    <div class="pgn">
      <div class="pgn-btn">‹</div>
      <div class="pgn-btn on">1</div>
      <div class="pgn-btn">2</div>
      <div class="pgn-btn">3</div>
      <div class="pgn-info">…</div>
      <div class="pgn-btn">21</div>
      <div class="pgn-btn">›</div>
    </div>""",
    ),

    "all_top_lectures.html": dict(
        title="Top Lectures",
        h1="🏆 Top Lectures",
        filter_pills=[("all", "All"), ("aqeedah", "Aqeedah"), ("tafsir", "Tafsir"), ("fiqh", "Fiqh"), ("seerah", "Seerah"), ("hadith", "Hadith"), ("akhlaq", "Akhlaq"), ("dua", "Du'a")],
        content=f"""    <div class="shead"><div class="shead-t">Top Lectures</div><div class="shead-c">Showing 1–10 of 1,248</div></div>
{gen_lecture_list(LECTURES_TOP, with_rank=True)}
    <div class="pgn">
      <div class="pgn-btn">‹</div>
      <div class="pgn-btn on">1</div>
      <div class="pgn-btn">2</div>
      <div class="pgn-btn">3</div>
      <div class="pgn-info">…</div>
      <div class="pgn-btn">125</div>
      <div class="pgn-btn">›</div>
    </div>""",
    ),

    "all_trending_lectures.html": dict(
        title="Trending Lectures",
        h1="🔥 Trending Lectures",
        filter_pills=[("week", "This Week"), ("month", "This Month"), ("rising", "Rising Fast"), ("viral", "Viral")],
        content=f"""    <div class="shead"><div class="shead-t">Trending Now</div><div class="shead-c">Showing 1–8 of 142</div></div>
{gen_lecture_list(LECTURES_TRENDING, with_rank=True)}
    <div class="pgn">
      <div class="pgn-btn">‹</div>
      <div class="pgn-btn on">1</div>
      <div class="pgn-btn">2</div>
      <div class="pgn-btn">3</div>
      <div class="pgn-btn">›</div>
    </div>""",
    ),

    "all_featured_lectures.html": dict(
        title="Featured Lectures",
        h1="⭐ Featured Lectures",
        filter_pills=[("all", "All"), ("editor", "Editor's Picks"), ("staff", "Staff Picks"), ("season", "Seasonal")],
        content=f"""    <div class="shead"><div class="shead-t">Featured by Shurafah</div><div class="shead-c">Showing 1–6 of 48</div></div>
{gen_lecture_list(LECTURES_FEATURED, with_rank=False)}
    <div class="pgn">
      <div class="pgn-btn">‹</div>
      <div class="pgn-btn on">1</div>
      <div class="pgn-btn">2</div>
      <div class="pgn-btn">3</div>
      <div class="pgn-btn">›</div>
    </div>""",
    ),

    "all_recent_lectures.html": dict(
        title="Recently Added",
        h1="🆕 Recently Added",
        filter_pills=[("today", "Today"), ("week", "This Week"), ("month", "This Month")],
        content=f"""    <div class="shead"><div class="shead-t">Latest Uploads</div><div class="shead-c">Showing 1–8 of 86</div></div>
{gen_lecture_list(LECTURES_RECENT, with_rank=False)}
    <div class="pgn">
      <div class="pgn-btn">‹</div>
      <div class="pgn-btn on">1</div>
      <div class="pgn-btn">2</div>
      <div class="pgn-btn">3</div>
      <div class="pgn-btn">›</div>
    </div>""",
    ),

    "all_waazi_categories.html": dict(
        title="Wa'azi Categories",
        h1="📚 Wa'azi Categories",
        filter_pills=[("all", "All"), ("popular", "Most Popular"), ("new", "Newest"), ("az", "A–Z")],
        content=f"""    <div class="shead"><div class="shead-t">Browse all categories</div><div class="shead-c">{len(CATEGORIES_W)} categories</div></div>
{gen_category_grid(CATEGORIES_W)}""",
    ),

    "all_waazi_subcategories.html": dict(
        title="Wa'azi Subcategories",
        h1="📂 Subcategories",
        filter_pills=[("all", "All"), ("tafsir", "Tafsir"), ("aqeedah", "Aqeedah"), ("fiqh", "Fiqh"), ("hadith", "Hadith")],
        content=f"""    <div class="shead"><div class="shead-t">Subcategories under Wa'azi</div><div class="shead-c">{len(SUBCATEGORIES_W)} subcategories</div></div>
{gen_category_grid(SUBCATEGORIES_W)}""",
    ),
}


def main():
    for filename, conf in PAGES.items():
        html = wrap_page(conf["title"], conf["h1"], conf["content"], conf.get("filter_pills"))
        path = ROOT / filename
        path.write_text(html, encoding="utf-8", newline="")
        print(f"  ok wrote {filename} ({len(html):,} chars)")


if __name__ == "__main__":
    main()
