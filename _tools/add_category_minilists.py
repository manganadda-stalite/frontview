"""Add 'Top Preachers in this category' and 'Top Lectures in this category'
mini-lists inside each cat-card of shurafah_admin_waazi_categories.html.

Also:
- Rename the leftover 'Classical' card to 'Khutbah' (it was missed by the
  earlier fix script because the old card used emoji 🎻).
- Replace the song-era sub-category rows with Wa'azi sub-categories.
- Replace the song-era category filter <select> options with Wa'azi categories.

Idempotent: re-running is safe because the mini-list block has a unique sentinel
HTML comment, and the substitution helpers skip already-replaced patterns.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "shurafah_admin_waazi_categories.html"

# Top 3 preachers + top 3 lecture titles per category.
CAT_DATA = {
    "tafsir": {
        "preachers": ["Sheikh Isah Ali Ibrahim", "Sheikh Yakubu Musa", "Sheikh Aliyu Maikwaru"],
        "lectures":  ["Tafsir Suratul Baqarah", "Tafsir Juz Amma", "Tafsir Al-Fatiha"],
    },
    "aqeedah": {
        "preachers": ["Sheikh Ahmad Gumi", "Sheikh Abdallah Usman", "Sheikh Auwal Albani"],
        "lectures":  ["Hanyar Gaskiya Vol. 3", "Tauhid Rububiyyah", "Pillars of Iman"],
    },
    "fiqh": {
        "preachers": ["Dr. Aminu Daurawa", "Sheikh Yakubu Musa", "Sheikh Abdallah Usman"],
        "lectures":  ["Fiqhul Ibadah \u2014 Part 12", "Salah Rulings Explained", "Zakat in Depth"],
    },
    "seerah": {
        "preachers": ["Sheikh Ahmad Gumi", "Sheikh Isah Ali Ibrahim", "Sheikh Aliyu Maikwaru"],
        "lectures":  ["Life of the Prophet (SAW)", "Battle of Badr", "Migration to Madina"],
    },
    "hadith": {
        "preachers": ["Sheikh Auwal Albani", "Sheikh Yakubu Musa", "Dr. Aminu Daurawa"],
        "lectures":  ["40 Hadith of An-Nawawi", "Sahih Bukhari Explained", "Hadith Methodology"],
    },
    "akhlaq": {
        "preachers": ["Sheikh Abdallah Usman", "Dr. Aminu Daurawa", "Sheikh Aliyu Maikwaru"],
        "lectures":  ["Character of the Prophet", "Patience & Gratitude", "Honesty in Speech"],
    },
    "dua": {
        "preachers": ["Sheikh Muhammad Bichi", "Sheikh Isah Ali Ibrahim", "Sheikh Ahmad Gumi"],
        "lectures":  ["Tahajjud & Night Prayer", "Du'as for Difficulty", "Names of Allah"],
    },
    # The leftover Classical card gets re-keyed to "khutbah" before insertion.
    "khutbah": {
        "preachers": ["Sheikh Ahmad Gumi", "Sheikh Auwal Albani", "Dr. Aminu Daurawa"],
        "lectures":  ["Friday Khutbah Series", "Ramadan Khutbahs", "Eid Khutbah Special"],
    },
}


def build_mini_lists(cat_key: str) -> str:
    data = CAT_DATA[cat_key]
    preachers_html = "".join(
        f'<div class="cml-row"><span class="cml-dot">\U0001F399\uFE0F</span>{name}</div>'
        for name in data["preachers"]
    )
    lectures_html = "".join(
        f'<div class="cml-row"><span class="cml-dot">\U0001F4D6</span>{title}</div>'
        for title in data["lectures"]
    )
    return (
        f'        <!-- waazi-mini-lists:{cat_key} -->\n'
        f'        <div class="cat-mini-lists" data-cat-key="{cat_key}">\n'
        f'          <div class="cml-col">\n'
        f'            <div class="cml-head">Top Preachers</div>\n'
        f'            {preachers_html}\n'
        f'          </div>\n'
        f'          <div class="cml-col">\n'
        f'            <div class="cml-head">Top Lectures</div>\n'
        f'            {lectures_html}\n'
        f'          </div>\n'
        f'        </div>\n'
    )


# CSS block injected once into the <style> block.
MINI_LIST_CSS = """
/* Top Preachers / Top Lectures mini-lists inside each Wa'azi category card */
.cat-mini-lists{
  display:grid;grid-template-columns:1fr 1fr;gap:10px;
  margin:12px 0 8px;padding:10px;border-radius:10px;
  background:var(--surface2);border:1px solid var(--border);
}
.cat-mini-lists .cml-col{display:flex;flex-direction:column;gap:5px;min-width:0;}
.cat-mini-lists .cml-head{
  font-size:9.5px;font-weight:800;letter-spacing:.4px;text-transform:uppercase;
  color:var(--accent2);font-family:'Syne',sans-serif;margin-bottom:2px;
}
.cat-mini-lists .cml-row{
  display:flex;align-items:center;gap:6px;font-size:10.5px;color:var(--text2);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.4;
}
.cat-mini-lists .cml-dot{font-size:11px;flex-shrink:0;}
@media (max-width:768px){
  .cat-mini-lists{grid-template-columns:1fr;}
}
"""


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    original = text

    # 1. Rename the leftover Classical card to Khutbah.
    text = text.replace(
        '<div class="cat-card" data-name="classical">',
        '<div class="cat-card" data-name="khutbah">',
    )
    # Card emoji + body
    text = text.replace(
        '<div style="font-size:28px;">\U0001F3BB</div>',  # 🎻
        '<div style="font-size:28px;">\U0001F54B</div>',  # 🕋
    )
    text = text.replace(
        '<div class="cat-name">Classical</div>',
        '<div class="cat-name">Khutbah</div>',
    )
    text = text.replace(
        '<div class="cat-desc">Orchestral, chamber music, hymnal arrangements and sacred classical compositions</div>',
        '<div class="cat-desc">Friday khutbahs, Eid sermons and special occasion lectures by leading preachers</div>',
    )
    text = text.replace(
        "showToast('Classical hidden','info')",
        "showToast('Khutbah hidden','info')",
    )
    text = text.replace(
        "if(confirm('Delete Classical?')){showToast('Category deleted','ok')}",
        "if(confirm('Delete Khutbah?')){showToast('Category deleted','ok')}",
    )

    # 2. Inject CSS once.
    if "Top Preachers / Top Lectures mini-lists" not in text:
        text = text.replace("</style>", MINI_LIST_CSS + "</style>", 1)

    # 3. Inject mini-lists into each card, right before <div class="cat-actions"
    #    Skip cards that already contain the sentinel comment.
    card_re = re.compile(
        r'(<div class="cat-card(?: hidden-cat)?" data-name="(?P<key>[a-z]+)">.*?)'
        r'(\s*<div class="cat-actions"[^>]*>)',
        re.DOTALL,
    )

    def insert(match: re.Match) -> str:
        head, actions = match.group(1), match.group(3)
        key = match.group("key")
        if key not in CAT_DATA:
            return match.group(0)
        sentinel = f"waazi-mini-lists:{key}"
        if sentinel in head:
            return match.group(0)
        return head + "\n" + build_mini_lists(key) + actions

    text = card_re.sub(insert, text)

    # 4. Replace the song-era category filter <select> options.
    text = text.replace(
        "<option>All Categories</option><option>Gospel</option><option>Worship</option><option>Afrobeat</option><option>Hip Hop</option><option>R&amp;B</option><option>Jazz</option>",
        "<option>All Categories</option><option>Tafsir</option><option>Aqeedah</option><option>Fiqh</option><option>Seerah</option><option>Hadith</option><option>Akhlaq</option><option>Du'a</option><option>Khutbah</option>",
    )

    # 5. Replace song-era subcat-rows with Wa'azi sub-categories.
    SUBCATS = [
        # (old data-name, new data-name, new icon, new name, new parent)
        ("praise",              "tauhid rububiyyah",     "\U0001F4D6", "Tauhid Rububiyyah",     "Aqeedah"),
        ("contemporary gospel", "tauhid uluhiyyah",      "\U0001F54B", "Tauhid Uluhiyyah",      "Aqeedah"),
        ("intimate worship",    "tauhid asma was-sifat", "\u2728",     "Tauhid Asma was-Sifat", "Aqeedah"),
        ("afropop",             "salah",                 "\U0001F64C", "Salah Rulings",         "Fiqh"),
        ("trap gospel",         "zakat",                 "\U0001F4B0", "Zakat & Sadaqah",       "Fiqh"),
        ("neo soul",            "siyam",                 "\U0001F319", "Siyam (Fasting)",       "Fiqh"),
        ("smooth jazz",         "tahajjud",              "\U0001F319", "Tahajjud Du'as",        "Du'a"),
        ("prophetic worship",   "names of allah",        "\U0001F4DC", "Names of Allah",        "Du'a"),
    ]

    for old, new_dn, new_icon, new_name, new_parent in SUBCATS:
        # data-name attribute
        text = text.replace(f'data-name="{old}"', f'data-name="{new_dn}"', 1)

    # Now rewrite the human-readable parts of each sub-cat row in one pass via regex.
    # Each row: <div class="subcat-name">XXX</div><div class="subcat-parent">Parent: YYY</div>
    OLD_TO_NEW_NAME = {
        "Praise":                "Tauhid Rububiyyah",
        "Contemporary Gospel":   "Tauhid Uluhiyyah",
        "Intimate Worship":      "Tauhid Asma was-Sifat",
        "Afropop":               "Salah Rulings",
        "Trap Gospel":           "Zakat & Sadaqah",
        "Neo Soul":              "Siyam (Fasting)",
        "Smooth Jazz":           "Tahajjud Du'as",
        "Prophetic Worship":     "Names of Allah",
    }
    OLD_TO_NEW_PARENT = {
        "Gospel":   "Aqeedah",
        "Worship":  "Aqeedah",
        "Afrobeat": "Fiqh",
        "Hip Hop":  "Fiqh",
        "R&amp;B":  "Fiqh",
        "Jazz":     "Du'a",
    }

    for old_name, new_name in OLD_TO_NEW_NAME.items():
        text = text.replace(
            f'<div class="subcat-name">{old_name}</div>',
            f'<div class="subcat-name">{new_name}</div>',
        )
    # Replace parent labels (these may repeat — that's fine since replace_all is what we want).
    for old_p, new_p in OLD_TO_NEW_PARENT.items():
        text = text.replace(
            f'<div class="subcat-parent">Parent: {old_p}</div>',
            f'<div class="subcat-parent">Parent: {new_p}</div>',
        )

    # Replace song-era confirm dialog labels in actions.
    text = text.replace("if(confirm('Delete Praise?'))", "if(confirm('Delete Tauhid Rububiyyah?'))")

    # Replace song-era sub-cat emoji icons inside rows (one each, in document order).
    SUBCAT_ICON_PAIRS = [
        ('<div class="subcat-icon">\U0001F64C</div>', '<div class="subcat-icon">\U0001F4D6</div>'),  # 🙌 → 📖 (Tauhid Rububiyyah)
        ('<div class="subcat-icon">\U0001F3B5</div>', '<div class="subcat-icon">\U0001F54B</div>'),  # 🎵 → 🕋
        ('<div class="subcat-icon">\U0001F56F\uFE0F</div>', '<div class="subcat-icon">\u2728</div>'),  # 🕯️ → ✨
        ('<div class="subcat-icon">\U0001F941</div>', '<div class="subcat-icon">\U0001F64C</div>'),  # 🥁 → 🙌
        ('<div class="subcat-icon">\U0001F3A4</div>', '<div class="subcat-icon">\U0001F4B0</div>'),  # 🎤 → 💰
    ]
    for old_icon, new_icon in SUBCAT_ICON_PAIRS:
        text = text.replace(old_icon, new_icon, 1)

    if text == original:
        print("No changes applied.")
        return
    TARGET.write_text(text, encoding="utf-8", newline="")
    print(f"Updated {TARGET.name}.")


if __name__ == "__main__":
    main()
