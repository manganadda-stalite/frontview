"""Follow-up cleanup for Wa'azi admin pages.

Replaces the residual Song-era data (artist names, song titles, song-category
names like Nasheed / Maulud / Shuhada, etc.) with Wa'azi-appropriate values
across three admin pages:

  - shurafah_admin_waazi_management.html
  - shurafah_admin_preacher_management.html
  - shurafah_admin_waazi_categories.html

This file is rerunnable; the substitutions are case-sensitive whole-string
replacements. They affect display labels, dropdown <option>s, and the inline
SAMPLE DATA arrays.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────────────
# 1.  shurafah_admin_waazi_management.html
#     Add/Edit lecture modal dropdowns + filter dropdown + SAMPLE DATA.
# ─────────────────────────────────────────────────────────────────────
WAAZI_MGMT = [
    # The Artist label inside the Add/Edit modal stays as id="songArtist"
    # internally but the visible label becomes "Preacher".
    ('<div class="form-label">Artist <span class="req">*</span></div>',
     '<div class="form-label">Preacher <span class="req">*</span></div>'),
    # Add-lecture modal artist dropdown
    ('<option value="">Select artist…</option>\n          <option>Uzairu Badamasi</option>\n          <option>Shamsudden Fudiyya</option>\n          <option>Maishurafah</option>\n          <option>Ahmad Isah</option>\n          <option>Yusuf Badamasi</option>',
     '<option value="">Select preacher…</option>\n          <option>Sheikh Ahmad Gumi</option>\n          <option>Sheikh Isah Ali Ibrahim</option>\n          <option>Dr. Aminu Daurawa</option>\n          <option>Sheikh Abdallah Usman</option>\n          <option>Sheikh Aliyu Maikwaru</option>\n          <option>Sheikh Yakubu Musa</option>\n          <option>Sheikh Auwal Albani</option>'),
    # Edit-lecture modal artist dropdown (different surrounding markup —
    # use a different distinctive snippet)
    ('<option value="">Select…</option>\n            <option selected>Uzairu Badamasi</option>\n            <option>Ahmad Isah</option>\n            <option>Shamsudden Fudiyya</option>',
     '<option value="">Select…</option>\n            <option selected>Sheikh Ahmad Gumi</option>\n            <option>Sheikh Isah Ali Ibrahim</option>\n            <option>Dr. Aminu Daurawa</option>'),
    # Add-lecture modal category dropdown
    ('<option value="">Select category…</option>\n          <option>Shairai</option>\n          <option>Ashura</option>\n          <option>Ahlul-baiti</option>\n          <option>Maulud</option>\n          <option selected>Shuhada</option>\n          <option>Shurafah</option>',
     '<option value="">Select category…</option>\n          <option>Tafsir</option>\n          <option selected>Aqeedah</option>\n          <option>Fiqh</option>\n          <option>Seerah</option>\n          <option>Hadith</option>\n          <option>Akhlaq</option>\n          <option>Du\'a</option>\n          <option>Khutbah</option>'),
    # Add-lecture modal sub-category dropdown
    ('<select class="form-select" id="songSubcat">\n          <option>General</option>\n          <option>Nasheed</option>\n          <option>Madahu</option>\n          <option>Manqaba</option>\n          <option>Kasidu</option>\n        </select>',
     '<select class="form-select" id="songSubcat">\n          <option>General</option>\n          <option>Tauhid Rububiyyah</option>\n          <option>Tauhid Uluhiyyah</option>\n          <option>Tauhid Asma was-Sifat</option>\n          <option>Iman in the Unseen</option>\n        </select>'),
    # Lyrics summary → just a regular description
    ('<div class="form-label">Description / Lyrics Summary</div>',
     '<div class="form-label">Description</div>'),
    ('placeholder="Brief description of the lecture, themes, or partial lyrics…"',
     'placeholder="Brief description of the lecture, topics covered, or key takeaways…"'),
    # Top filter — "All Artists"
    ('<option value="">All Artists</option>',
     '<option value="">All Preachers</option>'),
    # filter dropdown options (artist names)
    ('          <option>Uzairu Badamasi</option>\n          <option>Shamsudden Fudiyya</option>\n          <option>Maishurafah</option>\n          <option>Ahmad Isah</option>\n          <option>Yusuf Badamasi</option>\n        </select>',
     '          <option>Sheikh Ahmad Gumi</option>\n          <option>Sheikh Isah Ali Ibrahim</option>\n          <option>Dr. Aminu Daurawa</option>\n          <option>Sheikh Abdallah Usman</option>\n          <option>Sheikh Aliyu Maikwaru</option>\n          <option>Sheikh Yakubu Musa</option>\n          <option>Sheikh Auwal Albani</option>\n        </select>'),
    # Top filter — "All Categories" already says lectures; replace category option list
    ('<option value="">All Categories</option>\n          <option>Shairai</option>\n          <option>Ashura</option>\n          <option>Ahlul-baiti</option>\n          <option>Maulud</option>\n          <option>Shuhada</option>\n          <option>Shurafah</option>',
     '<option value="">All Categories</option>\n          <option>Tafsir</option>\n          <option>Aqeedah</option>\n          <option>Fiqh</option>\n          <option>Seerah</option>\n          <option>Hadith</option>\n          <option>Akhlaq</option>\n          <option>Du\'a</option>\n          <option>Khutbah</option>'),
    # Sample lecture data — replace whole rows
    ("  {id:1,title:'Kurmus',artist:'Uzairu Badamasi',category:'Shuhada',duration:'3:42',quality:'320 kbps',plays:48200,downloads:12100,status:'Live',featured:false,date:'Mar 12, 2025',art:'g1',emoji:'🎵',thumbnail:null},",
     "  {id:1,title:'Hanyar Gaskiya Vol. 3',artist:'Sheikh Ahmad Gumi',category:'Aqeedah',duration:'1:04:38',quality:'320 kbps',plays:1820000,downloads:540000,status:'Live',featured:true,date:'Mar 12, 2025',art:'g1',emoji:'🎙️',thumbnail:null},"),
    ("  {id:2,title:'Juyin Juya Hali',artist:'Uzairu Badamasi',category:'Shuhada',duration:'5:33',quality:'320 kbps',plays:2400000,downloads:830000,status:'Live',featured:true,date:'Jan 5, 2025',art:'g2',emoji:'🎶',thumbnail:null},",
     "  {id:2,title:'Tafsir Suratul Baqarah',artist:'Sheikh Isah Ali Ibrahim',category:'Tafsir',duration:'1:32:14',quality:'320 kbps',plays:1500000,downloads:410000,status:'Live',featured:true,date:'Jan 5, 2025',art:'g2',emoji:'📖',thumbnail:null},"),
    ("  {id:3,title:'Yan Siyasa',artist:'Uzairu Badamasi',category:'Shurafah',duration:'4:48',quality:'128 kbps',plays:1900000,downloads:610000,status:'Live',featured:false,date:'Nov 18, 2024',art:'g3',emoji:'🎸',thumbnail:null},",
     "  {id:3,title:'Fiqhul Ibadah — Part 12',artist:'Dr. Aminu Daurawa',category:'Fiqh',duration:'56:18',quality:'320 kbps',plays:1100000,downloads:320000,status:'Live',featured:false,date:'Nov 18, 2024',art:'g3',emoji:'⚖️',thumbnail:null},"),
    ("  {id:4,title:'Qudus Remix',artist:'Uzairu Badamasi',category:'Shuhada',duration:'5:01',quality:'320 kbps',plays:1400000,downloads:490000,status:'Live',featured:false,date:'Oct 2, 2024',art:'g4',emoji:'🎼',thumbnail:null},",
     "  {id:4,title:'Du\\'as for Difficulty',artist:'Sheikh Ahmad Gumi',category:'Du\\'a',duration:'32:08',quality:'320 kbps',plays:980000,downloads:280000,status:'Live',featured:false,date:'Oct 2, 2024',art:'g4',emoji:'🤲',thumbnail:null},"),
    ("  {id:5,title:'Motar Sayyidi',artist:'Uzairu Badamasi',category:'Maulud',duration:'6:20',quality:'128 kbps',plays:980000,downloads:312000,status:'Live',featured:true,date:'Sep 14, 2024',art:'g5',emoji:'🎙️',thumbnail:null},",
     "  {id:5,title:'Seerah of the Prophet',artist:'Sheikh Abdallah Usman',category:'Seerah',duration:'1:18:00',quality:'320 kbps',plays:880000,downloads:260000,status:'Live',featured:true,date:'Sep 14, 2024',art:'g5',emoji:'🕊️',thumbnail:null},"),
    ("  {id:6,title:'Fallen Stars',artist:'Amara Soul',category:'Shurafah',duration:'3:42',quality:'128 kbps',plays:48200,downloads:12100,status:'Live',featured:true,date:'Mar 1, 2025',art:'g7',emoji:'🎵',thumbnail:null},",
     "  {id:6,title:'Akhlaq al-Mu\\'min',artist:'Sheikh Yakubu Musa',category:'Akhlaq',duration:'42:55',quality:'320 kbps',plays:910000,downloads:240000,status:'Live',featured:true,date:'Mar 1, 2025',art:'g7',emoji:'🌿',thumbnail:null},"),
    ("  {id:7,title:'Way Maker',artist:'Sinach',category:'Shairai',duration:'5:33',quality:'320 kbps',plays:2400000,downloads:830000,status:'Live',featured:false,date:'Feb 20, 2025',art:'g1',emoji:'🎶',thumbnail:null},",
     "  {id:7,title:'Manners in Islam',artist:'Sheikh Aliyu Maikwaru',category:'Akhlaq',duration:'44:10',quality:'320 kbps',plays:820000,downloads:220000,status:'Live',featured:false,date:'Feb 20, 2025',art:'g1',emoji:'💫',thumbnail:null},"),
    ("  {id:8,title:'Holy Ground',artist:'Nathaniel Bassey',category:'Ashura',duration:'4:48',quality:'320 kbps',plays:1900000,downloads:610000,status:'Live',featured:false,date:'Feb 14, 2025',art:'g4',emoji:'🎸',thumbnail:null},",
     "  {id:8,title:'Hanyar Gaskiya Vol. 2',artist:'Sheikh Ahmad Gumi',category:'Aqeedah',duration:'58:14',quality:'320 kbps',plays:770000,downloads:200000,status:'Live',featured:false,date:'Feb 14, 2025',art:'g4',emoji:'📖',thumbnail:null},"),
    ("  {id:9,title:'Open Heaven',artist:'Nathaniel Bassey',category:'Ahlul-baiti',duration:'4:55',quality:'128 kbps',plays:750000,downloads:210000,status:'In Review',featured:false,date:'Apr 1, 2025',art:'g5',emoji:'🎼',thumbnail:null},",
     "  {id:9,title:'Ramadan Reminders',artist:'Sheikh Auwal Albani',category:'Du\\'a',duration:'38:42',quality:'128 kbps',plays:690000,downloads:180000,status:'In Review',featured:false,date:'Apr 1, 2025',art:'g5',emoji:'🌙',thumbnail:null},"),
    ("  {id:10,title:'Grace Overflow',artist:'Tope Alabi',category:'Maulud',duration:'4:15',quality:'320 kbps',plays:920000,downloads:280000,status:'Live',featured:false,date:'Dec 22, 2024',art:'g6',emoji:'🎹',thumbnail:null},",
     "  {id:10,title:'The Path of Sincerity',artist:'Sheikh Ahmad Gumi',category:'Aqeedah',duration:'52:18',quality:'320 kbps',plays:650000,downloads:170000,status:'Live',featured:false,date:'Dec 22, 2024',art:'g6',emoji:'✨',thumbnail:null},"),
    ("  {id:11,title:'Higher Ground',artist:'Frank Edwards',category:'Shuhada',duration:'5:01',quality:'320 kbps',plays:1400000,downloads:490000,status:'Live',featured:false,date:'Nov 5, 2024',art:'g2',emoji:'🎤',thumbnail:null},",
     "  {id:11,title:'Tafsir Suratul Yaseen',artist:'Sheikh Isah Ali Ibrahim',category:'Tafsir',duration:'1:08:22',quality:'320 kbps',plays:610000,downloads:160000,status:'Live',featured:false,date:'Nov 5, 2024',art:'g2',emoji:'📖',thumbnail:null},"),
    ("  {id:12,title:'I See Miracles',artist:'Dunsin Oyekan',category:'Shurafah',duration:'4:38',quality:'128 kbps',plays:680000,downloads:190000,status:'Live',featured:false,date:'Oct 15, 2024',art:'g3',emoji:'🎵',thumbnail:null},",
     "  {id:12,title:'Patience in Hardship',artist:'Sheikh Isah Ali Ibrahim',category:'Akhlaq',duration:'44:30',quality:'320 kbps',plays:580000,downloads:140000,status:'Live',featured:false,date:'Oct 15, 2024',art:'g3',emoji:'🌿',thumbnail:null},"),
    ("  {id:13,title:'You Are Holy',artist:'Mercy Chinwo',category:'Shairai',duration:'4:20',quality:'320 kbps',plays:1100000,downloads:350000,status:'Live',featured:true,date:'Sep 8, 2024',art:'g7',emoji:'🎶',thumbnail:null},",
     "  {id:13,title:'The Six Pillars',artist:'Sheikh Abdallah Usman',category:'Aqeedah',duration:'47:14',quality:'320 kbps',plays:540000,downloads:130000,status:'Live',featured:true,date:'Sep 8, 2024',art:'g7',emoji:'🕌',thumbnail:null},"),
    ("  {id:14,title:'Come Alive',artist:'Lauren Daigle',category:'Ahlul-baiti',duration:'3:55',quality:'128 kbps',plays:420000,downloads:120000,status:'Live',featured:false,date:'Aug 12, 2024',art:'g4',emoji:'🎸',thumbnail:null},",
     "  {id:14,title:'Daily Adhkar',artist:'Sheikh Yakubu Musa',category:'Du\\'a',duration:'28:55',quality:'320 kbps',plays:480000,downloads:120000,status:'Live',featured:false,date:'Aug 12, 2024',art:'g4',emoji:'🤲',thumbnail:null},"),
    ("  {id:15,title:'My Worship',artist:'Sinach',category:'Maulud',duration:'5:15',quality:'320 kbps',plays:1200000,downloads:380000,status:'Live',featured:false,date:'Jul 20, 2024',art:'g6',emoji:'🎼',thumbnail:null},",
     "  {id:15,title:'The Companions',artist:'Sheikh Auwal Albani',category:'Seerah',duration:'1:14:18',quality:'320 kbps',plays:420000,downloads:110000,status:'Live',featured:false,date:'Jul 20, 2024',art:'g6',emoji:'🕊️',thumbnail:null},"),
    # Hide remaining song-era emojis used as default art
    ("emoji:'🎵',thumbnail", "emoji:'🎙️',thumbnail"),
    ("emoji:'🎶',thumbnail", "emoji:'📖',thumbnail"),
    ("emoji:'🎸',thumbnail", "emoji:'⚖️',thumbnail"),
    ("emoji:'🎼',thumbnail", "emoji:'🕊️',thumbnail"),
    ("emoji:'🎤',thumbnail", "emoji:'🎙️',thumbnail"),
    ("emoji:'🎹',thumbnail", "emoji:'🌿',thumbnail"),
    # Visible "All Artists" label in chips, etc.
    ("All Artists", "All Preachers"),
    # Sample lectures 11-25 — rewrite each row in one shot
    ("  {id:11,title:'Grace Overflow',artist:'Tope Alabi',category:'Shurafah',duration:'4:15',quality:'320 kbps',plays:920000,downloads:280000,status:'Live',featured:false,date:'Mar 5, 2025',art:'g6',emoji:'🌿',thumbnail:null},",
     "  {id:11,title:'Tahajjud & Night Prayer',artist:'Sheikh Muhammad Bichi',category:'Du\\'a',duration:'38:14',quality:'320 kbps',plays:380000,downloads:90000,status:'Live',featured:false,date:'Mar 5, 2025',art:'g6',emoji:'🌙',thumbnail:null},"),
    ("  {id:12,title:'Come Alive',artist:'Lauren Daigle',category:'Shairai',duration:'4:52',quality:'320 kbps',plays:3100000,downloads:1200000,status:'Live',featured:true,date:'Dec 10, 2024',art:'g7',emoji:'🎙️',thumbnail:null},",
     "  {id:12,title:'Building Iman',artist:'Sheikh Ja\\'afar Mahmud',category:'Aqeedah',duration:'52:42',quality:'320 kbps',plays:340000,downloads:80000,status:'Live',featured:true,date:'Dec 10, 2024',art:'g7',emoji:'🕌',thumbnail:null},"),
    ("  {id:13,title:'Miracles',artist:'Dunsin Oyekan',category:'Ashura',duration:'6:20',quality:'64 kbps',plays:640000,downloads:180000,status:'In Review',featured:false,date:'Apr 1, 2025',art:'g8',emoji:'📖',thumbnail:null},",
     "  {id:13,title:'The Final Hour',artist:'Sheikh Sani Yahaya',category:'Aqeedah',duration:'44:55',quality:'128 kbps',plays:300000,downloads:70000,status:'In Review',featured:false,date:'Apr 1, 2025',art:'g8',emoji:'🌅',thumbnail:null},"),
    ("  {id:14,title:'River Flow',artist:'Sinach',category:'Shurafah',duration:'5:10',quality:'128 kbps',plays:510000,downloads:145000,status:'Offline',featured:false,date:'Nov 3, 2024',art:'g2',emoji:'⚖️',thumbnail:null},",
     "  {id:14,title:'Charity in Islam',artist:'Sheikh Ibrahim Khalil',category:'Fiqh',duration:'32:08',quality:'128 kbps',plays:270000,downloads:60000,status:'Offline',featured:false,date:'Nov 3, 2024',art:'g2',emoji:'💝',thumbnail:null},"),
    ("  {id:15,title:'A Kasar nan',artist:'Uzairu Badamasi',category:'Shuhada',duration:'4:10',quality:'320 kbps',plays:320000,downloads:88000,status:'Live',featured:false,date:'Feb 2, 2025',art:'g1',emoji:'🕊️',thumbnail:null},",
     "  {id:15,title:'Hadith Number 41',artist:'Sheikh Bashir Aliyu',category:'Hadith',duration:'28:18',quality:'320 kbps',plays:240000,downloads:55000,status:'Live',featured:false,date:'Feb 2, 2025',art:'g1',emoji:'📜',thumbnail:null},"),
    ("  {id:16,title:'Kubra Shahida ce',artist:'Uzairu Badamasi',category:'Shuhada',duration:'6:20',quality:'320 kbps',plays:980000,downloads:312000,status:'Live',featured:false,date:'Mar 28, 2025',art:'g3',emoji:'🎙️',thumbnail:null},",
     "  {id:16,title:'Khutbatul Jumu\\'ah Live',artist:'Sheikh Isah Ali Ibrahim',category:'Khutbah',duration:'38:22',quality:'320 kbps',plays:200000,downloads:48000,status:'Live',featured:false,date:'Mar 28, 2025',art:'g3',emoji:'🎤',thumbnail:null},"),
    ("  {id:17,title:'Salatin Awliya',artist:'Ahmad Isah',category:'Shurafah',duration:'5:14',quality:'128 kbps',plays:420000,downloads:98000,status:'In Review',featured:false,date:'Mar 30, 2025',art:'g6',emoji:'🎙️',thumbnail:null},",
     "  {id:17,title:'Children\\'s Tarbiyya',artist:'Sheikh Aliyu Maikwaru',category:'Akhlaq',duration:'44:18',quality:'128 kbps',plays:170000,downloads:40000,status:'In Review',featured:false,date:'Mar 30, 2025',art:'g6',emoji:'👨‍👩‍👧',thumbnail:null},"),
    ("  {id:18,title:'Zaman Lafiya',artist:'Yusuf Badamasi',category:'Maulud',duration:'4:33',quality:'128 kbps',plays:180000,downloads:42000,status:'Live',featured:false,date:'Mar 25, 2025',art:'g4',emoji:'📖',thumbnail:null},",
     "  {id:18,title:'Money Matters in Islam',artist:'Dr. Aminu Daurawa',category:'Fiqh',duration:'52:55',quality:'128 kbps',plays:150000,downloads:38000,status:'Live',featured:false,date:'Mar 25, 2025',art:'g4',emoji:'💰',thumbnail:null},"),
    ("  {id:19,title:'Ta Sayyida Masuma',artist:'Uzairu Badamasi',category:'Ahlul-baiti',duration:'4:28',quality:'320 kbps',plays:750000,downloads:210000,status:'Live',featured:false,date:'Oct 15, 2024',art:'g5',emoji:'⚖️',thumbnail:null},",
     "  {id:19,title:'Women in Islam',artist:'Sheikh Auwal Albani',category:'Tarbiyya',duration:'48:30',quality:'320 kbps',plays:140000,downloads:34000,status:'Live',featured:false,date:'Oct 15, 2024',art:'g5',emoji:'🌸',thumbnail:null},"),
    ("  {id:20,title:'Morning Dew',artist:'Amara Soul',category:'Shurafah',duration:'3:55',quality:'64 kbps',plays:120000,downloads:32000,status:'Offline',featured:false,date:'Aug 20, 2024',art:'g7',emoji:'🕊️',thumbnail:null},",
     "  {id:20,title:'Death & The Hereafter',artist:'Sheikh Yakubu Musa',category:'Aqeedah',duration:'1:12:14',quality:'64 kbps',plays:120000,downloads:30000,status:'Offline',featured:false,date:'Aug 20, 2024',art:'g7',emoji:'🌅',thumbnail:null},"),
    ("  {id:21,title:'Deep Calls',artist:'Amara Soul',category:'Shairai',duration:'4:28',quality:'128 kbps',plays:140000,downloads:38000,status:'Live',featured:false,date:'Sep 5, 2024',art:'g8',emoji:'🎙️',thumbnail:null},",
     "  {id:21,title:'Faith in Modern Times',artist:'Sheikh Ahmad Gumi',category:'Aqeedah',duration:'49:12',quality:'128 kbps',plays:110000,downloads:28000,status:'Live',featured:false,date:'Sep 5, 2024',art:'g8',emoji:'✨',thumbnail:null},"),
    ("  {id:22,title:'Overflow',artist:'Amara Soul',category:'Shurafah',duration:'5:02',quality:'320 kbps',plays:228000,downloads:64000,status:'Live',featured:false,date:'Oct 28, 2024',art:'g1',emoji:'🎙️',thumbnail:null},",
     "  {id:22,title:'Halal & Haram',artist:'Dr. Aminu Daurawa',category:'Fiqh',duration:'58:48',quality:'320 kbps',plays:100000,downloads:25000,status:'Live',featured:false,date:'Oct 28, 2024',art:'g1',emoji:'⚖️',thumbnail:null},"),
    ("  {id:23,title:'Grace Rain',artist:'Amara Soul',category:'Shairai',duration:'4:10',quality:'320 kbps',plays:314000,downloads:92000,status:'Live',featured:false,date:'Dec 18, 2024',art:'g2',emoji:'📖',thumbnail:null},",
     "  {id:23,title:'The Companions of Badr',artist:'Sheikh Abdallah Usman',category:'Seerah',duration:'1:08:00',quality:'320 kbps',plays:95000,downloads:22000,status:'Live',featured:false,date:'Dec 18, 2024',art:'g2',emoji:'🕊️',thumbnail:null},"),
    ("  {id:24,title:'Taba ku lashe',artist:'Uzairu Badamasi',category:'Shuhada',duration:'4:10',quality:'128 kbps',plays:180000,downloads:48000,status:'Live',featured:false,date:'Nov 22, 2024',art:'g3',emoji:'⚖️',thumbnail:null},",
     "  {id:24,title:'Sahih al-Bukhari Hadith 1',artist:'Sheikh Bashir Aliyu',category:'Hadith',duration:'42:10',quality:'128 kbps',plays:85000,downloads:20000,status:'Live',featured:false,date:'Nov 22, 2024',art:'g3',emoji:'📜',thumbnail:null},"),
    ("  {id:25,title:'Zunar Jini',artist:'Uzairu Badamasi',category:'Maulud',duration:'3:55',quality:'64 kbps',plays:90000,downloads:22000,status:'In Review',featured:false,date:'Mar 29, 2025',art:'g6',emoji:'🕊️',thumbnail:null},",
     "  {id:25,title:'Tafsir Suratul Fatihah',artist:'Sheikh Isah Ali Ibrahim',category:'Tafsir',duration:'1:08:22',quality:'64 kbps',plays:80000,downloads:18000,status:'In Review',featured:false,date:'Mar 29, 2025',art:'g6',emoji:'📖',thumbnail:null},"),
    # catColor map — replace with Wa'azi categories
    ("function catColor(c){const m={Shairai:'rgba(255,107,53,.15);color:var(--accent)',Ashura:'rgba(255,77,143,.15);color:var(--pink)',Shurafah:'rgba(155,107,255,.15);color:var(--purple)',Maulud:'rgba(77,159,255,.15);color:var(--blue)',Shuhada:'rgba(46,204,143,.15);color:var(--green)','Ahlul-baiti':'rgba(255,209,102,.1);color:var(--yellow)'};return m[c]||'rgba(255,255,255,.06);color:var(--text2)';}",
     "function catColor(c){const m={Aqeedah:'rgba(200,134,10,.15);color:var(--accent)',Tafsir:'rgba(232,160,32,.15);color:var(--accent2)',Fiqh:'rgba(77,159,255,.15);color:var(--blue)',Seerah:'rgba(155,107,255,.15);color:var(--purple)',Hadith:'rgba(46,204,143,.15);color:var(--green)',Akhlaq:'rgba(255,209,102,.1);color:var(--yellow)','Du\\'a':'rgba(255,77,143,.15);color:var(--pink)',Khutbah:'rgba(245,200,66,.15);color:var(--accent3)',Tarbiyya:'rgba(255,179,71,.1);color:var(--accent2)'};return m[c]||'rgba(255,255,255,.06);color:var(--text2)';}"),
    # R2 mock file browser entries
    ("'Kurmus - Uzairu Badamasi.mp3','8.4 MB'", "'Hanyar Gaskiya Vol 3 - Sh Ahmad Gumi.mp3','46.2 MB'"),
    ("Kurmus - Uzairu Badamasi.mp3", "Hanyar Gaskiya Vol 3 - Sh Ahmad Gumi.mp3"),
    ("'Qudus Remix - Uzairu.mp3','6.1 MB'", "'Tafsir Surah Baqarah - Sh Isah Ali.mp3','61.5 MB'"),
    ("Qudus Remix - Uzairu.mp3", "Tafsir Surah Baqarah - Sh Isah Ali.mp3"),
    ("'Yan Siyasa - Uzairu.wav','18.7 MB'", "'Fiqhul Ibadah Part 12 - Dr Aminu.wav','58.4 MB'"),
    ("Yan Siyasa - Uzairu.wav", "Fiqhul Ibadah Part 12 - Dr Aminu.wav"),
    ("'Juyin Juya Haki - Uzairu.flac','22.3 MB'", "'Akhlaq al-Mumin - Sh Yakubu.flac','68.1 MB'"),
    ("Juyin Juya Haki - Uzairu.flac", "Akhlaq al-Mumin - Sh Yakubu.flac"),
    # YouTube import preview
    ("Uzairu Badamasi - Kurmus (Official Audio)", "Sheikh Ahmad Gumi — Hanyar Gaskiya Vol. 3 (Full Lecture)"),
    ("Uzairu Badamasi Official", "Sheikh Ahmad Gumi Official"),
    # Edit modal currently-loaded lecture preview
    ("Kurmus · Uzairu Badamasi", "Hanyar Gaskiya Vol. 3 · Sheikh Ahmad Gumi"),
    ("Uzairu Badamasi · 8.4 MB · MP3 · 320kbps", "Sheikh Ahmad Gumi · 46.2 MB · MP3 · 320kbps"),
    # Form input default value for edit modal
    ('<input class="form-input" type="text" value="Kurmus">',
     '<input class="form-input" type="text" value="Hanyar Gaskiya Vol. 3">'),
]

# ─────────────────────────────────────────────────────────────────────
# 2.  shurafah_admin_preacher_management.html
#     Replace residual song-era category names + song-catalogue language.
# ─────────────────────────────────────────────────────────────────────
PREACHER_MGMT = [
    # Bio + descriptions
    ("song catalogue", "lecture catalogue"),
    ("song catalog", "lecture catalog"),
    ("initial song", "initial lecture"),
    ("first single", "first lecture"),
    ("song count", "lecture count"),
    ("Songs Catalogue", "Lectures Catalogue"),
    # Genre / category strings
    ("Nasheed · Maulud", "Aqeedah · Akhlaq"),
    ("Shuhada · Maulud", "Aqeedah · Tafsir"),
    ("Maulud · Shuhada", "Tafsir · Aqeedah"),
    ("Shuhada · Shairai", "Aqeedah · Hadith"),
    ("Shurafah · Shuhada", "Seerah · Aqeedah"),
    ("Ashura · Shuhada", "Tafsir · Aqeedah"),
    ("Shairai · Ahlul-baiti", "Hadith · Akhlaq"),
    ("Ahlul-baiti · Maulud", "Akhlaq · Tafsir"),
    ("Maulud · Ahlul-baiti", "Tafsir · Akhlaq"),
    ("Nasheed", "Tafsir"),
    ("Shuhada", "Aqeedah"),
    ("Maulud", "Tafsir"),
    ("Shurafah", "Seerah"),
    ("Ashura", "Hadith"),
    ("Shairai", "Akhlaq"),
    ("Ahlul-baiti", "Du'a"),
    # tags arrays
    ("tags:['Tafsir','Aqeedah']", "tags:['Tafsir','Aqeedah']"),  # safe-noop, but exists
]

# ─────────────────────────────────────────────────────────────────────
# 3.  shurafah_admin_waazi_categories.html
#     Replace the song-era category cards with Wa'azi ones (Tafsir,
#     Aqeedah, etc.), each with an inline "Top preachers" mini-list.
# ─────────────────────────────────────────────────────────────────────
WAAZI_CATS = [
    # Card headings + names
    ('data-name="gospel">', 'data-name="tafsir">'),
    ('data-name="worship">', 'data-name="aqeedah">'),
    ('data-name="afrobeat">', 'data-name="fiqh">'),
    ('data-name="hip hop">', 'data-name="seerah">'),
    ('data-name="r&b">', 'data-name="hadith">'),
    ('data-name="jazz">', 'data-name="akhlaq">'),
    ('data-name="highlife">', 'data-name="dua">'),
    # data-name display labels in the badges/lists
    ('<div class="cat-name">Gospel</div>', '<div class="cat-name">Tafsir</div>'),
    ('<div class="cat-name">Worship</div>', '<div class="cat-name">Aqeedah</div>'),
    ('<div class="cat-name">Afrobeat</div>', '<div class="cat-name">Fiqh</div>'),
    ('<div class="cat-name">Hip Hop</div>', '<div class="cat-name">Seerah</div>'),
    ('<div class="cat-name">R&B</div>', '<div class="cat-name">Hadith</div>'),
    ('<div class="cat-name">Jazz</div>', '<div class="cat-name">Akhlaq</div>'),
    ('<div class="cat-name">Highlife</div>', '<div class="cat-name">Du\'a</div>'),
    # Descriptions
    ('Contemporary Christian music, praise, worship and church hymns',
     'Qur\'anic exegesis covering the meaning, context, and reflections of every surah.'),
    ('Intimate worship, corporate praise, prophetic and spontaneous worship',
     'Islamic creed — the six pillars of faith, tauhid and the unseen.'),
    ('Afrobeat fusion with gospel — uplifting, danceable worship for the African church',
     'Islamic jurisprudence — Halal & Haram, daily acts of worship and practical fiqh.'),
    ('Hip Hop, rap and spoken word gospel music for the new generation',
     'The biography of the Prophet ﷺ — his life, struggle and example.'),
    ('Rhythm & Blues, soul and contemporary gospel ballads',
     'Prophetic traditions — selected ahadith from the major collections.'),
    ('Jazz inspired gospel — instrumental, vocal and contemplative',
     'Manners, character and inward refinement — Akhlaq al-Mu\'min.'),
    ('Highlife guitar gospel — West African heritage praise music',
     'Supplications — du\'as for daily life, hardship, and the night prayer.'),
    # Toast strings for hide/show
    ("'Gospel hidden from app'", "'Tafsir hidden from app'"),
    ("'Worship hidden'", "'Aqeedah hidden'"),
    ("'Afrobeat hidden'", "'Fiqh hidden'"),
    ("'Hip Hop hidden'", "'Seerah hidden'"),
    ("'R&B hidden'", "'Hadith hidden'"),
    ("'Highlife hidden'", "'Du\\'a hidden'"),
    ("'Jazz is now visible ✓'", "'Akhlaq is now visible ✓'"),
    # Emojis – replace the song-era hand/keyboard/etc with appropriate ones
    ('<div style="font-size:28px;">🙏</div>', '<div style="font-size:28px;">📖</div>'),     # Gospel→Tafsir
    ('<div style="font-size:28px;">🎹</div>', '<div style="font-size:28px;">🕌</div>'),     # Worship→Aqeedah
    ('<div style="font-size:28px;">🎷</div>', '<div style="font-size:28px;">⚖️</div>'),     # Afrobeat→Fiqh
    ('<div style="font-size:28px;">🎤</div>', '<div style="font-size:28px;">🕊️</div>'),    # Hip Hop→Seerah
    ('<div style="font-size:28px;">🎶</div>', '<div style="font-size:28px;">📜</div>'),     # R&B→Hadith
    ('<div style="font-size:28px;">🎺</div>', '<div style="font-size:28px;">🌿</div>'),     # Jazz→Akhlaq
    ('<div style="font-size:28px;">🪕</div>', '<div style="font-size:28px;">🤲</div>'),     # Highlife→Du'a
]


def apply(path: Path, subs: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    before = text
    hits = 0
    for old, new in subs:
        if old in text:
            text = text.replace(old, new)
            hits += 1
    if text != before:
        path.write_text(text, encoding="utf-8", newline="")
        print(f"  ok {path.name} ({hits}/{len(subs)} subs applied)")
    else:
        print(f"  -- {path.name} (no changes)")


def main() -> None:
    apply(ROOT / "shurafah_admin_waazi_management.html", WAAZI_MGMT)
    apply(ROOT / "shurafah_admin_preacher_management.html", PREACHER_MGMT)
    apply(ROOT / "shurafah_admin_waazi_categories.html", WAAZI_CATS)


if __name__ == "__main__":
    main()
