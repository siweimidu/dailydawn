<p align="center">
  <img src="./logo.svg" width="96" alt="DailyDawn logo" />
</p>

<h1 align="center">DailyDawn · Daily AI brief for indie builders</h1>

<p align="center">
  Pulls 7 tech signal sources every day → multi-agent analysis → bilingual report → web / RSS / Telegram / email
</p>

<p align="center"><b>🌐 <a href="./README.en.md">English</a> · <a href="./README.md">中文</a></b></p>

<p align="center">
  <a href="https://github.com/siweimidu/dailydawn/actions/workflows/daily-report.yml"><img src="https://github.com/siweimidu/dailydawn/actions/workflows/daily-report.yml/badge.svg" alt="Daily Report" /></a>
  <a href="https://siweimidu.github.io/dailydawn/"><img src="https://img.shields.io/badge/site-GitHub%20Pages-blue" alt="Pages" /></a>
  <a href="https://siweimidu.github.io/dailydawn/feed/en.xml"><img src="https://img.shields.io/badge/RSS-subscribe-orange" alt="RSS" /></a>
</p>

> **30 minutes every morning to see what to ship, what to skip, who's eating whose lunch.**

---

<!-- LATEST_ISSUES_START -->

## Latest 3 issues

- [2026-10-19 · AI job search automation / Open source code analysis / Local voice synthesis infrastructure](https://siweimidu.github.io/dailydawn/en/2026/2026-10-19.html)
  > AI job search and voice studio tools dominate today as developers pivot to automated career and audio pipelines
- [2026-10-17 · Local voice synthesis / Modular CLI daemons / Plugin-driven agent workflows](https://siweimidu.github.io/dailydawn/en/2026/2026-10-17.html)
  > Anthropic plugin integration and private voice studio tools signal a shift toward modular local developer infrastructure
- [2026-10-16 · Local Voice Synthesis / Scientific Agent Frameworks / Private Infrastructure Shift](https://siweimidu.github.io/dailydawn/en/2026/2026-10-16.html)
  > Voice synthesis and scientific agent frameworks dominate developer activity as open source infrastructure shifts toward specialized local execution

[Full archive →](https://siweimidu.github.io/dailydawn/en/)

<!-- LATEST_ISSUES_END -->

## 📖 Where to read

| What | URL |
|---|---|
| Site home | <https://siweimidu.github.io/dailydawn/> |
| Chinese archive | <https://siweimidu.github.io/dailydawn/zh/> |
| English archive | <https://siweimidu.github.io/dailydawn/en/> |
| RSS (English) | <https://siweimidu.github.io/dailydawn/feed/en.xml> |
| JSON Feed | <https://siweimidu.github.io/dailydawn/feed/en.json> |
| Raw Markdown | `https://raw.githubusercontent.com/siweimidu/dailydawn/main/en/<year>/<date>.md` |
| Telegram | [@dailydawn_bot](https://t.me/dailydawn_bot) — digest pushed daily at 08:00 CST |
| Email | Full HTML issue delivered daily at 08:00 CST |

Generated automatically every day at **00:00 UTC** (08:00 Beijing time). No manual work.

---

## 🤔 What this is

Every morning you probably bounce between Hacker News, Product Hunt, Reddit, HuggingFace, GitHub Trending and V2EX, manually piecing together "what actually happened today." DailyDawn hands that to an LLM: pull 150+ raw signals → dedupe across sources → sort into 5 dimensions → one agent per dimension digs deep → an editor-in-chief synthesizes the report.

**Each issue is ~5,500 English words and contains:**

- **20 today-specific deep sections** — questions are generated from today's actual signals, so they change every day
- **Three-tier build advice** — today's 2-hour build / weekend extension / this week's longer bet / weekly risk
- **Cross-source keyword growth** — Google Trends 7-day rising queries that surface buyer intent
- Organized around "**what should an indie builder do this week**" — not news regurgitation

The 5 dimensions (also the 5 chapters of each issue):

| Dimension | Question it answers |
|---|---|
| 🔍 Launch discoveries | What new demand or play just appeared |
| 🧰 Tech stack | What to build with, what to avoid |
| ⚔️ Competitive intel | Who is doing what, whose moat is crumbling |
| 📡 Demand radar | What users actually search for and complain about |
| 📈 Trend verdict | What is noise, what is an inflection point |

---

## 🚀 How to use it

### 1. Just read the site

Open <https://siweimidu.github.io/dailydawn/>, updated daily after 08:00 CST.

### 2. RSS (best for n8n / readers)

```
https://siweimidu.github.io/dailydawn/feed/en.xml
```

Works with Feedly, Inoreader, FreshRSS, or n8n's **RSS Read** node.

### 3. Telegram

Message `/start` to [@dailydawn_bot](https://t.me/dailydawn_bot) and you get a daily digest card (top 3 signals + link).

### 4. Email

An HTML issue lands in your inbox daily at 08:00 CST — forwardable to anyone, no login needed.

---

## 🔌 Plug it into n8n

The report is already finished; n8n is for **re-processing** it — merging sources, translating, rewriting for social, or storing it.

```
Cron (daily 08:30, Asia/Shanghai)
   ↓
RSS Read  → URL: https://siweimidu.github.io/dailydawn/feed/en.xml
             Max Items: 1
   ↓
HTTP Request → URL: {{ $json.link }}       # fetch the full daily page
   ↓
AI Agent / LLM node → your rewrite prompt
   ↓
Slack / Notion / database
```

**RSS item fields**: `title` (`DailyDawn · 2026-10-13`), `link` (daily page), `pubDate`, `description` (top-3 digest line).

**Prefer structured JSON?** Use <https://siweimidu.github.io/dailydawn/feed/en.json> with an HTTP Request node — fields `items[].title / url / date_published / content_text`.

> ⚠️ Set your cron after **08:30 CST**. The pipeline itself takes 3–8 minutes; fire too early and you get yesterday's issue.

---

## ⚙️ How it works

```
GitHub Actions cron · daily 00:00 UTC
    │
    ├─ fetchers/*          pull 150+ raw signals concurrently (~30s)
    │   Hacker News · GitHub Trending · Product Hunt · Reddit
    │   HuggingFace · V2EX · Google Trends
    ├─ aggregator          cross-source dedupe (canonical URL) + score merge → top 60
    ├─ classifier          sort into 5 dimensions
    ├─ question_generator  20 today-specific questions (zh + en)
    ├─ source_digest       per-source clustered digest
    ├─ experts × 5 × 2     five expert agents × two languages
    └─ editor × 2          editor-in-chief synthesis
        │
        ├─ renderer   → zh/YYYY/YYYY-MM-DD.md + en/...
        ├─ build_feed → feed/*.xml · feed/*.json
        ├─ git push   → triggers GitHub Pages deploy
        └─ notify     → Telegram digest + email (optional)
```

**Stack**: Python 3.12 · fully async `httpx` / `asyncio` · OpenAI-compatible SDK · GitHub Actions scheduling · GitHub Pages hosting · no database, no server.

**Cost**: GitHub Actions free tier + LLM free tier — **$0** in normal operation.

---

## 🔧 Configuration & maintenance

### Secrets (encrypted)

| Name | Purpose |
|---|---|
| `LLM_API_KEY` | LLM API key |
| `LLM_BASE_URL` | OpenAI-compatible endpoint |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | Optional Telegram push |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USERNAME` / `SMTP_PASSWORD` / `MAIL_TO` | Optional email push |

### Variables (plain)

| Name | Current value | Purpose |
|---|---|---|
| `LLM_MODEL` | `gemini-3.1-flash-lite` | Primary model |
| `LLM_FALLBACK_MODELS` | `gemini-3.5-flash-lite,gemini-3-flash-preview` | Fallback chain on rate limit |
| `SITE_BASE_URL` | `https://siweimidu.github.io/dailydawn` | Base URL used in generated links |

### Switch models (no code change)

| Provider | `LLM_MODEL` | `LLM_BASE_URL` |
|---|---|---|
| Gemini | `gemini-3.1-flash-lite` | `https://generativelanguage.googleapis.com/v1beta/openai` |
| Groq | `openai/gpt-oss-120b` | `https://api.groq.com/openai/v1` |
| DeepSeek | `deepseek-chat` | `https://api.deepseek.com` |

### Tune the writing

Edit `prompts/analyze.en.md` (English) and `prompts/analyze.zh.md` (Chinese) — not the code. Commit and the next run picks it up.

---

## 💻 Run locally

```bash
git clone https://github.com/siweimidu/dailydawn.git
cd dailydawn
pip install -r requirements.txt
cp .env.example .env      # fill LLM_API_KEY / LLM_BASE_URL / LLM_MODEL
python scripts/main.py    # → zh/2026/<today>.md + en/2026/<today>.md
```

Build site and feeds only (no LLM calls, no cost):

```bash
python scripts/build_feed.py    # → feed/*.xml, feed/*.json
python scripts/build_site.py    # → _site/ (preview locally)
python -m http.server -d _site 8000
```

---

## ❓ FAQ

**`429 RESOURCE_EXHAUSTED` / `Quota exceeded`?**
Gemini's free tier is per-model: flash-lite allows **500 requests/day**. One pipeline run costs ~18–40 calls. This repo ships a fallback chain — when the primary model 429s it moves to `gemini-3.5-flash-lite`, then `gemini-3-flash-preview`. Seeing `⚠ rate limited on [...]; trying next model in chain` in the logs means fallback worked and the report still generated. Quotas reset at 00:00 UTC.

**Want the full text on Telegram instead of the digest?**
Add `TG_FULL: "1"` to the notify step's env in the workflow (sends multiple messages).

**Single source failing?**
Failures are skipped per source and never block the pipeline. GitHub Trending is HTML scraping (breaks if the page changes); Reddit's public JSON may 429 at peak times.

**Will topics repeat?**
No. `meta/recent-taglines.jsonl` keeps the last 7 days of themes and the prompt hard-forbids repeats.

---

## 🙏 Upstream & license

Forked from [TangSY/dailydawn](https://github.com/TangSY/dailydawn) (MIT). This fork adds:

- RSS 2.0 / JSON Feed generation (`scripts/build_feed.py`)
- GitHub Pages static site (`scripts/build_site.py` + `deploy-pages.yml`)
- Telegram + email push (`scripts/notify_push.py`)
- Rate-limit model fallback chain (`scripts/pipeline/llm.py`)

Thanks to [@TangSY](https://github.com/TangSY) for the original project.

[License: MIT](./LICENSE)
