from google import genai
from google.genai import types
import urllib.request
import xml.etree.ElementTree as ET
import webbrowser
import json
import os
from datetime import datetime

API_KEY = "MASUKKAN_API_KEY_LO_DISINI"

RSS_FEEDS = {
    "saham_indonesia": [
        "https://news.google.com/rss/search?q=IHSG+saham+bursa+efek+Indonesia&hl=id&gl=ID&ceid=ID:id",
        "https://news.google.com/rss/search?q=saham+BEI+IDX+investasi+Indonesia&hl=id&gl=ID&ceid=ID:id",
        "https://www.cnbcindonesia.com/rss/tag/ihsg",
        "https://www.cnbcindonesia.com/rss/tag/bursa-saham",
        "https://investasi.kontan.co.id/rss",
        "https://finance.detik.com/rss",
        "https://kumparan.com/kumparanbisnis/rss",
    ],
    "ekonomi": [
        "https://news.google.com/rss/search?q=ekonomi+Indonesia+rupiah+BI&hl=id&gl=ID&ceid=ID:id",
        "https://www.cnbcindonesia.com/rss/tag/ekonomi-indonesia",
        "https://www.antaranews.com/rss/ekonomi",
        "https://www.cnnindonesia.com/ekonomi/rss",
    ],
    "ai_tech": [
        "https://news.google.com/rss/search?q=artificial+intelligence+AI+technology&hl=en&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=AI+machine+learning+LLM+2025&hl=en&gl=US&ceid=US:en",
        "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "https://feeds.arstechnica.com/arstechnica/technology-lab",
    ],
    "global_market": [
        "https://news.google.com/rss/search?q=stock+market+NYSE+NASDAQ+S%26P500&hl=en&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=Wall+Street+Dow+Jones+market+today&hl=en&gl=US&ceid=US:en",
        "https://feeds.content.dowjones.io/public/rss/mw_topstories",
        "https://www.investing.com/rss/news_25.rss",
    ]
}

def fetch_rss(url, max_items=5):
    items = []
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Referer': 'https://www.google.com/',
        })
        with urllib.request.urlopen(req, timeout=8) as r:
            root = ET.fromstring(r.read())
        
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        # RSS format
        for item in root.findall('.//item')[:max_items]:
            title = item.findtext('title', '').strip()
            desc = item.findtext('description', '').strip()
            link = item.findtext('link', '').strip()
            pub = item.findtext('pubDate', '').strip()
            if title:
                items.append(f"- {title}: {desc[:200] if desc else ''} ({pub})")
        
        # Atom format
        if not items:
            for entry in root.findall('.//atom:entry', ns)[:max_items]:
                title = entry.findtext('atom:title', '', ns).strip()
                summary = entry.findtext('atom:summary', '', ns).strip()
                if title:
                    items.append(f"- {title}: {summary[:200] if summary else ''}")
    except Exception as e:
        pass
    return items

def collect_news():
    print("  📡 Mengambil berita saham Indonesia...")
    saham = []
    for url in RSS_FEEDS["saham_indonesia"]:
        saham += fetch_rss(url, 4)
        if len(saham) >= 8: break

    print("  📡 Mengambil berita ekonomi...")
    ekonomi = []
    for url in RSS_FEEDS["ekonomi"]:
        ekonomi += fetch_rss(url, 3)
        if len(ekonomi) >= 5: break

    print("  📡 Mengambil berita AI & Tech...")
    tech = []
    for url in RSS_FEEDS["ai_tech"]:
        tech += fetch_rss(url, 4)
        if len(tech) >= 8: break

    print("  📡 Mengambil berita pasar global...")
    global_news = []
    for url in RSS_FEEDS["global_market"]:
        global_news += fetch_rss(url, 3)
        if len(global_news) >= 5: break

    return saham, ekonomi, tech, global_news

def analyze_with_gemini(saham, ekonomi, tech, global_news):
    client = genai.Client(api_key=API_KEY)
    today = datetime.now().strftime("%A, %d %B %Y")
    waktu = datetime.now().strftime("%H:%M")

    berita_text = f"""
=== BERITA SAHAM & IHSG ===
{chr(10).join(saham[:8]) if saham else "Tidak ada berita tersedia"}

=== BERITA EKONOMI INDONESIA ===
{chr(10).join(ekonomi[:5]) if ekonomi else "Tidak ada berita tersedia"}

=== BERITA PASAR GLOBAL ===
{chr(10).join(global_news[:5]) if global_news else "Tidak ada berita tersedia"}

=== BERITA AI & TEKNOLOGI ===
{chr(10).join(tech[:8]) if tech else "Tidak ada berita tersedia"}
"""

    prompt = f"""Hari ini {today}, pukul {waktu} WIB.

Kamu adalah analis finansial dan tech expert yang membantu mahasiswa CS Indonesia belajar investasi saham.

Berikut berita terbaru yang baru dikumpulkan dari berbagai sumber:

{berita_text}

Berdasarkan berita di atas, buat morning briefing dalam format JSON berikut.
HANYA balas dengan JSON, tanpa markdown, tanpa backtick, tanpa penjelasan apapun di luar JSON.

{{
  "tanggal": "{today}",
  "waktu_update": "{waktu} WIB",
  "market_summary": {{
    "ihsg": {{
      "status": "naik/turun/sideways/belum_buka",
      "nilai": "perkiraan nilai atau 'Cek real-time'",
      "perubahan": "persentase jika ada atau '-'",
      "sentimen": "positif/negatif/netral",
      "narasi": "1-2 kalimat kondisi IHSG hari ini"
    }},
    "global": {{
      "wall_street": "kondisi Wall Street berdasarkan berita",
      "asia": "kondisi pasar Asia"
    }}
  }},
  "berita_saham": [
    {{
      "judul": "judul berita singkat",
      "ringkasan": "2-3 kalimat ringkasan mudah dipahami pemula",
      "dampak": "positif/negatif/netral",
      "saham_terkait": "kode/nama saham jika ada atau kosong"
    }}
  ],
  "saham_pantau": [
    {{
      "kode": "kode saham misal BBCA",
      "nama": "nama perusahaan",
      "alasan": "kenapa patut dipantau berdasarkan berita hari ini",
      "outlook": "bullish/bearish/netral"
    }}
  ],
  "berita_ai_tech": [
    {{
      "judul": "judul berita",
      "ringkasan": "2-3 kalimat ringkasan",
      "relevansi": "kenapa penting buat mahasiswa CS"
    }}
  ],
  "insight_hari_ini": {{
    "prediksi_pasar": "analisis dan prediksi pasar hari ini berdasarkan semua berita",
    "tips": "satu tips investasi actionable untuk pemula",
    "mood_pasar": "bullish/bearish/mixed",
    "kata_bijak": "satu quote atau insight finansial yang relevan"
  }}
}}"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.5)
    )
    return response.text

def clean_json(raw):
    text = raw.strip()
    if "```" in text:
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        text = text[start:end+1]
    return text.strip()

def generate_html(data, raw_counts):
    mood = data.get("insight_hari_ini", {}).get("mood_pasar", "mixed").lower()
    mood_color = {"bullish": "#10b981", "bearish": "#ef4444", "mixed": "#f59e0b"}.get(mood, "#6366f1")
    mood_bg = {"bullish": "#d1fae5", "bearish": "#fee2e2", "mixed": "#fef3c7"}.get(mood, "#ede9fe")
    mood_emoji = {"bullish": "📈", "bearish": "📉", "mixed": "〰️"}.get(mood, "📊")

    ihsg = data.get("market_summary", {}).get("ihsg", {})
    global_market = data.get("market_summary", {}).get("global", {})
    insight = data.get("insight_hari_ini", {})
    berita_saham = data.get("berita_saham", [])
    saham_pantau = data.get("saham_pantau", [])
    berita_ai = data.get("berita_ai_tech", [])

    sentimen_color = {"positif": "#10b981", "negatif": "#ef4444", "netral": "#6b7280"}.get(
        ihsg.get("sentimen", "netral"), "#6b7280")

    def dampak_badge(dampak):
        cfg = {
            "positif": ("background:#d1fae5;color:#065f46", "↑ Positif"),
            "negatif": ("background:#fee2e2;color:#991b1b", "↓ Negatif"),
            "netral": ("background:#f3f4f6;color:#374151", "→ Netral")
        }
        s, l = cfg.get(dampak, cfg["netral"])
        return f'<span style="font-size:11px;font-weight:600;padding:2px 10px;border-radius:20px;{s}">{l}</span>'

    def outlook_badge(outlook):
        cfg = {
            "bullish": ("background:#d1fae5;color:#065f46", "📈 Bullish"),
            "bearish": ("background:#fee2e2;color:#991b1b", "📉 Bearish"),
            "netral": ("background:#f3f4f6;color:#374151", "〰️ Netral")
        }
        s, l = cfg.get(outlook.lower() if outlook else "netral", cfg["netral"])
        return f'<span style="font-size:11px;font-weight:600;padding:2px 10px;border-radius:20px;{s}">{l}</span>'

    berita_html = ""
    for b in berita_saham:
        berita_html += f"""
        <div style="border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:8px;">
                <span style="font-weight:600;color:#111827;font-size:14px;flex:1;">{b.get('judul','')}</span>
                {dampak_badge(b.get('dampak','netral'))}
            </div>
            <p style="color:#6b7280;font-size:13px;line-height:1.6;margin:0 0 6px;">{b.get('ringkasan','')}</p>
            {f'<span style="font-size:12px;color:#6366f1;font-weight:500;">🏢 {b.get("saham_terkait")}</span>' if b.get('saham_terkait') else ''}
        </div>"""

    pantau_html = ""
    for s in saham_pantau:
        pantau_html += f"""
        <div style="border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <div>
                    <span style="font-size:18px;font-weight:800;color:#111827;">{s.get('kode','')}</span>
                    <span style="font-size:13px;color:#9ca3af;margin-left:8px;">{s.get('nama','')}</span>
                </div>
                {outlook_badge(s.get('outlook','netral'))}
            </div>
            <p style="color:#6b7280;font-size:13px;line-height:1.6;margin:0;">{s.get('alasan','')}</p>
        </div>"""

    tech_html = ""
    for a in berita_ai:
        tech_html += f"""
        <div style="border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin-bottom:10px;">
            <p style="font-weight:600;color:#111827;font-size:14px;margin:0 0 8px;">🤖 {a.get('judul','')}</p>
            <p style="color:#6b7280;font-size:13px;line-height:1.6;margin:0 0 8px;">{a.get('ringkasan','')}</p>
            <p style="color:#6366f1;font-size:12px;margin:0;font-style:italic;">💡 {a.get('relevansi','')}</p>
        </div>"""

    total_berita = sum(raw_counts.values())

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Morning Briefing — {data.get('tanggal','')}</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Plus Jakarta Sans',sans-serif;background:#f3f4f6;min-height:100vh;padding:28px 16px;color:#111827}}
.wrap{{max-width:780px;margin:0 auto}}
.header{{background:linear-gradient(135deg,#1e1b4b,#4338ca);border-radius:20px;padding:32px;margin-bottom:20px;color:#fff;position:relative;overflow:hidden}}
.header::before{{content:'';position:absolute;top:-60px;right:-60px;width:220px;height:220px;background:rgba(255,255,255,0.05);border-radius:50%}}
.card{{background:#fff;border-radius:16px;padding:22px;margin-bottom:16px;border:1px solid #e5e7eb}}
.card-title{{font-size:15px;font-weight:700;margin-bottom:14px;display:flex;align-items:center;gap:8px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.stat{{background:#f9fafb;border-radius:12px;padding:14px;border:1px solid #e5e7eb}}
.stat-label{{font-size:11px;color:#9ca3af;font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}}
.stat-value{{font-size:22px;font-weight:800;color:{sentimen_color}}}
.stat-sub{{font-size:12px;color:#9ca3af;margin-top:2px}}
.insight{{background:linear-gradient(135deg,#ede9fe,#ddd6fe);border-radius:12px;padding:18px;border:1px solid #c4b5fd}}
.insight-label{{font-size:11px;font-weight:700;color:#5b21b6;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}}
.insight-text{{font-size:14px;color:#4c1d95;line-height:1.7}}
.tips{{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-radius:12px;padding:14px;border:1px solid #a7f3d0;margin-top:10px}}
.quote{{background:linear-gradient(135deg,#fff7ed,#fed7aa);border-radius:12px;padding:14px;border:1px solid #fdba74;margin-top:10px;font-style:italic;color:#92400e;font-size:14px;line-height:1.6}}
.badge-mood{{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:30px;font-size:13px;font-weight:700;margin-top:14px;background:{mood_bg};color:{mood_color}}}
.source-info{{font-size:11px;color:rgba(255,255,255,0.6);margin-top:8px}}
.footer{{text-align:center;color:#9ca3af;font-size:12px;padding:16px 0}}
</style>
</head>
<body>
<div class="wrap">

<div class="header">
    <div style="font-size:12px;opacity:.6;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">🌅 Selamat Pagi</div>
    <div style="font-size:26px;font-weight:800">Morning Briefing</div>
    <div style="font-size:13px;opacity:.7;margin-top:4px">{data.get('tanggal','')} · {data.get('waktu_update','')}</div>
    <div class="source-info">📡 {total_berita} berita dikumpulkan dari {len(raw_counts)} kategori sumber</div>
    <div class="badge-mood">{mood_emoji} Pasar {mood.capitalize()}</div>
</div>

<div class="card">
    <div class="card-title">📊 Market Overview</div>
    <div class="grid2">
        <div class="stat">
            <div class="stat-label">IHSG</div>
            <div class="stat-value">{ihsg.get('nilai','—')}</div>
            <div class="stat-sub">{ihsg.get('perubahan','')} · {ihsg.get('status','').replace('_',' ').title()}</div>
            <div style="font-size:12px;color:#6b7280;margin-top:6px;line-height:1.5">{ihsg.get('narasi','')}</div>
        </div>
        <div class="stat" style="background:#f9fafb">
            <div class="stat-label">Global</div>
            <div style="font-size:13px;font-weight:600;color:#111827;margin-top:4px">{global_market.get('wall_street','—')}</div>
            <div style="font-size:12px;color:#6b7280;margin-top:6px">{global_market.get('asia','')}</div>
        </div>
    </div>
</div>

<div class="card">
    <div class="card-title">📰 Berita Saham & Ekonomi</div>
    {berita_html if berita_html else '<p style="color:#9ca3af;font-size:13px">Tidak ada berita tersedia saat ini.</p>'}
</div>

<div class="card">
    <div class="card-title">👁️ Saham yang Patut Dipantau</div>
    {pantau_html if pantau_html else '<p style="color:#9ca3af;font-size:13px">Tidak ada rekomendasi saat ini.</p>'}
</div>

<div class="card">
    <div class="card-title">🤖 AI & Teknologi</div>
    {tech_html if tech_html else '<p style="color:#9ca3af;font-size:13px">Tidak ada berita tersedia saat ini.</p>'}
</div>

<div class="card">
    <div class="card-title">🧠 Insight & Prediksi Hari Ini</div>
    <div class="insight">
        <div class="insight-label">📡 Analisis Pasar</div>
        <div class="insight-text">{insight.get('prediksi_pasar','')}</div>
    </div>
    <div class="tips">
        <div style="font-size:11px;font-weight:700;color:#065f46;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">💡 Tips Hari Ini</div>
        <div style="font-size:14px;color:#065f46;line-height:1.6">{insight.get('tips','')}</div>
    </div>
    <div class="quote">✨ "{insight.get('kata_bijak','')}"</div>
</div>

<div class="footer">Morning Briefing AI · Dibuat otomatis dari RSS feed · {data.get('waktu_update','')}</div>

</div>
</body>
</html>"""

def main():
    print("=" * 45)
    print("  MORNING BRIEFING AI")
    print("=" * 45)
    print()
    print("🔍 Mengumpulkan berita dari RSS feed...")
    print()

    saham, ekonomi, tech, global_news = collect_news()

    counts = {
        "saham": len(saham),
        "ekonomi": len(ekonomi),
        "tech": len(tech),
        "global": len(global_news)
    }

    total = sum(counts.values())
    print(f"\n✅ Terkumpul {total} berita:")
    print(f"   📈 Saham: {counts['saham']} | 🌍 Global: {counts['global']}")
    print(f"   💼 Ekonomi: {counts['ekonomi']} | 🤖 Tech: {counts['tech']}")
    print()
    print("🧠 Menganalisis dengan AI...")
    print("   (tunggu 15-30 detik)\n")

    try:
        raw = analyze_with_gemini(saham, ekonomi, tech, global_news)
        cleaned = clean_json(raw)
        data = json.loads(cleaned)

        print("✅ Analisis selesai!")
        print("🎨 Membuat halaman briefing...\n")

        html = generate_html(data, counts)
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "briefing.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ Tersimpan: {out}")
        print("🌐 Membuka browser...\n")
        webbrowser.open(f"file:///{out}")
        print("✅ Selesai! Selamat memulai hari 🚀")

    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        print("Response mentah:")
        print(raw[:800])
    except Exception as e:
        print(f"❌ Error: {e}")

    input("\nTekan Enter untuk menutup...")

if __name__ == "__main__":
    main()
