# 🌅 Morning Briefing AI

> Personal AI-powered morning briefing that automatically collects real-time news about Indonesian stocks (IHSG) and AI/tech, then summarizes and analyzes it — all displayed in a clean web dashboard.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=flat-square&logo=windows)

---

## 📌 About The Project

Every morning, this tool automatically:
1. **Fetches real-time news** from multiple RSS feed sources (IHSG, BEI, global markets, AI & tech)
2. **Analyzes the news** using Google Gemini AI to generate insights and market predictions
3. **Opens a beautiful HTML dashboard** in your browser with a full morning briefing

Built for personal use as a **daily investment learning tool** — especially for beginners who want to stay updated on the Indonesian stock market and AI developments.

---

## ✨ Features

- 📈 **IHSG & Stock Market News** — Real-time Indonesian stock market updates
- 🌍 **Global Market Sentiment** — Wall Street, Nasdaq, Asian markets overview  
- 🤖 **AI & Tech News** — Latest developments in artificial intelligence
- 🧠 **AI-Generated Insights** — Market predictions and actionable tips powered by Gemini
- 👁️ **Stocks to Watch** — Daily recommendations with bullish/bearish outlook
- 🎨 **Clean Dashboard UI** — Beautiful HTML report that opens in your browser
- ⚡ **One-Click Launch** — Just double-click `run.bat` and everything works
- 🕖 **Auto-Schedule** — Runs automatically every morning via Windows Task Scheduler

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.8+ | Core scripting |
| Google Gemini API (`google-genai`) | AI analysis & summarization |
| RSS Feed Parsing (`urllib`, `xml`) | Real-time news collection |
| HTML/CSS | Dashboard UI generation |
| Windows Task Scheduler | Automation |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free tier) — get it at [aistudio.google.com](https://aistudio.google.com/apikey)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/morning-briefing-ai.git
cd morning-briefing-ai
```

**2. Install dependencies**
```bash
pip install google-genai
```

**3. Add your API key**

Open `briefing.py` and replace the placeholder:
```python
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

**4. Run it**
```bash
python briefing.py
```
Or on Windows, just double-click `run.bat`

---

## 📅 Auto-Schedule (Windows)

To run automatically every morning:

1. Open **Task Scheduler** → Create Basic Task
2. Set trigger: **Daily at 07:00 AM**
3. Action: Start `run.bat`
4. Done — your briefing runs itself every morning!

---

## 📸 Preview

```
================================
  MORNING BRIEFING AI
================================

🔍 Mengumpulkan berita dari RSS feed...

  📡 Mengambil berita saham Indonesia...
  📡 Mengambil berita ekonomi...
  📡 Mengambil berita AI & Tech...
  📡 Mengambil berita pasar global...

✅ Terkumpul 14 berita
🧠 Menganalisis dengan AI...
✅ Selesai! Browser opening... 🚀
```

*Dashboard opens automatically in your default browser.*

---

## 📁 Project Structure

```
morning-briefing-ai/
├── briefing.py      # Main script — fetches news & generates dashboard
├── run.bat          # Windows launcher (double-click to run)
├── briefing.html    # Generated dashboard (auto-created on each run)
└── README.md        # You are here
```

---

## 🗺️ Roadmap

- [x] RSS feed news collection
- [x] AI-powered analysis & summarization
- [x] HTML dashboard generation
- [x] Windows Task Scheduler integration
- [ ] Add stock price data (Yahoo Finance API)
- [ ] Email/WhatsApp delivery option
- [ ] Mobile-friendly dashboard
- [ ] Multi-language support (EN/ID)

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

Built with ❤️ by a Computer Science student learning to combine AI and personal finance.

> *"The best investment you can make is in yourself."* — Warren Buffett
