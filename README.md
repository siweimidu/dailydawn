<p align="center">
  <img src="./logo.svg" width="96" alt="DailyDawn logo" />
</p>

<h1 align="center">DailyDawn · 独立开发者的 AI 趋势日报</h1>

<p align="center">
  每天自动抓 7 个技术信号源 → 多 agent 分析 → 生成中英双语日报 → 推到网页 / RSS / Telegram / 邮箱
</p>

<p align="center"><b>🌐 <a href="./README.md">中文</a> · <a href="./README.en.md">English</a></b></p>

<p align="center">
  <a href="https://github.com/siweimidu/dailydawn/actions/workflows/daily-report.yml"><img src="https://github.com/siweimidu/dailydawn/actions/workflows/daily-report.yml/badge.svg" alt="Daily Report" /></a>
  <a href="https://siweimidu.github.io/dailydawn/"><img src="https://img.shields.io/badge/日报站点-GitHub%20Pages-blue" alt="Pages" /></a>
  <a href="https://siweimidu.github.io/dailydawn/feed/zh.xml"><img src="https://img.shields.io/badge/RSS-订阅-orange" alt="RSS" /></a>
</p>

> **每天清晨 30 分钟，看清今天值得做什么、要避开什么、谁在颠覆谁。**

---

<!-- LATEST_ISSUES_START -->

## 最近 3 期日报

- [2026-10-19 · AI求职代理 / 开源语音合成 / 开源编码代理](https://siweimidu.github.io/dailydawn/zh/2026/2026-10-19.html)
  > 开源语音驱动开发与求职代理登顶 GitHub，独立开发者正快速抢占任务外包工具链
- [2026-10-17 · 语音合成工具链 / 本地优先软件 / 代理插件化架构](https://siweimidu.github.io/dailydawn/zh/2026/2026-10-17.html)
  > 独立开发者正通过垂直化工具链抢占通用模型留下的性能与隐私缝隙
- [2026-10-16 · 开源逆向智能代理 / 开源语音合成工具 / 科学研究代理技能](https://siweimidu.github.io/dailydawn/zh/2026/2026-10-16.html)
  > 开源语音合成与科研代理技能库今日登顶 GitHub，垂直工具链正在替代通用大模型

[全部归档 →](https://siweimidu.github.io/dailydawn/zh/)

<!-- LATEST_ISSUES_END -->

## 📖 在线地址

| 用途 | 地址 |
|---|---|
| 日报首页 | <https://siweimidu.github.io/dailydawn/> |
| 中文归档 | <https://siweimidu.github.io/dailydawn/zh/> |
| 英文归档 | <https://siweimidu.github.io/dailydawn/en/> |
| RSS（中文） | <https://siweimidu.github.io/dailydawn/feed/zh.xml> |
| JSON Feed | <https://siweimidu.github.io/dailydawn/feed/zh.json> |
| Markdown 原文 | `https://raw.githubusercontent.com/siweimidu/dailydawn/main/zh/<年>/<日期>.md` |
| Telegram | [@dailydawn_bot](https://t.me/dailydawn_bot) 每天 08:00 推送摘要 |
| 邮箱 | 每天 08:00 收到 HTML 全文 |

每天北京时间 **08:00**（UTC 00:00）自动生成，无需人工干预。

---

## 🤔 这是什么

每天早上你可能要在 Hacker News、Product Hunt、Reddit、HuggingFace、GitHub Trending、V2EX 之间来回翻，手工拼出「今天到底发生了什么」。

DailyDawn 把这活儿交给 LLM：抓 150+ 条原始信号 → 跨源去重 → 分进 5 个维度 → 每个维度派一个 agent 深挖 → 主笔合成一篇结构化日报。

**每篇约 5000 中文字，包含：**

- **20 个今日专属深度小节** —— 问题基于当日实际信号动态生成，每天都不一样
- **三级构建建议** —— 今日 2 小时构建 / 周末扩展 / 本周更长线的赌注 / 本周风险
- **跨源关键词涨幅** —— Google Trends 7 日上升的搜索词，捕获买家意图
- 整体围绕「**独立开发者本周该做什么**」组织，不是新闻搬运

5 个分析维度（也是日报的 5 个大章节）：

| 维度 | 回答什么问题 |
|---|---|
| 🔍 发现机会 | 今天冒出来的新需求、新玩法 |
| 🧰 技术选型 | 该用什么栈、该避开什么坑 |
| ⚔️ 竞争情报 | 谁在做什么、谁的护城河在塌 |
| 📡 需求雷达 | 用户真实在搜什么、抱怨什么 |
| 📈 趋势判断 | 哪些是噪音、哪些是拐点 |

---

## 🚀 怎么用

### 方式 1：直接看网页

打开 <https://siweimidu.github.io/dailydawn/>，每天 08:00 后自动更新。

### 方式 2：RSS 订阅（推荐给 n8n / 阅读器）

```
https://siweimidu.github.io/dailydawn/feed/zh.xml
```

喂给 Feedly、Inoreader、FreshRSS，或者 n8n 的 **RSS Read** 节点。

### 方式 3：Telegram

给 [@dailydawn_bot](https://t.me/dailydawn_bot) 发一句 `/start`，之后每天 08:00 自动收到摘要卡片（今日 Top 3 信号 + 网页链接）。

### 方式 4：邮箱

每天 08:00 收到 HTML 全文，直接转发给任何人看都不需要登录。

---

## 🔌 接入 n8n（做你自己的二次日报）

日报本身已经是成品，接 n8n 通常是为了**再加工**：跨源合并、翻译、改写成小红书/公众号文案、入库。

### 最小工作流

```
Cron (每天 08:30, Asia/Shanghai)
   ↓
RSS Read  → URL: https://siweimidu.github.io/dailydawn/feed/zh.xml
             Max Items: 1
   ↓
HTTP Request → URL: {{ $json.link }}       # 抓当日网页全文
   ↓
AI Agent / LLM 节点 → 你的改写提示词
   ↓
飞书 / Notion / 公众号 / 数据库
```

### RSS 节点字段说明

| 字段 | 内容 |
|---|---|
| `title` | `DailyDawn · 2026-10-13` |
| `link` | 当日网页地址 |
| `pubDate` | 当日 00:00 UTC |
| `description` | 今日 Top 3 信号摘要（一句话版） |

### 想要结构化 JSON

用 JSON Feed 更省事（无需解析 XML）：

```
https://siweimidu.github.io/dailydawn/feed/zh.json
```

→ n8n 用 **HTTP Request** 节点拿，字段：`items[].title / url / date_published / content_text`。

### 想要原始 Markdown

```
https://raw.githubusercontent.com/siweimidu/dailydawn/main/zh/2026/2026-10-13.md
```

→ n8n 用 **HTTP Request** + **Markdown** 节点转 HTML，或者直接丢给 LLM。

> ⚠️ Cron 建议设在 **08:30** 之后。日报流水线本身要跑 3–8 分钟，设太早会拿到昨天的内容。

---

## ⚙️ 它是怎么跑起来的

```
GitHub Actions cron · 每天 UTC 00:00（北京 08:00）
    │
    ├─ fetchers/*          并发抓 150+ 条原始信号（约 30 秒）
    │   Hacker News · GitHub Trending · Product Hunt · Reddit
    │   HuggingFace · V2EX · Google Trends
    │
    ├─ aggregator          跨源去重（canonical URL）+ 分数叠加 → Top 60
    │
    ├─ classifier          分进 5 个维度
    ├─ question_generator  为今天生成 20 个专属问题（zh + en）
    ├─ source_digest       每源聚类摘要
    │
    ├─ experts × 5 × 2     5 个专家 × 中英双语深度分析
    └─ editor × 2          主笔合成：POV 开篇 + Top 3 + 三级构建建议
        │
        ├─ renderer   → zh/YYYY/YYYY-MM-DD.md + en/...
        ├─ build_feed → feed/zh.xml · feed/zh.json · en 同
        ├─ git push   → 触发 GitHub Pages 部署
        └─ notify     → Telegram 摘要 + 邮箱全文（可选）
```

**技术栈**：Python 3.12 · `httpx` / `asyncio` 全异步 · OpenAI 兼容 SDK · GitHub Actions 调度 · GitHub Pages 托管 · 零数据库、零服务器。

**成本**：GitHub Actions 免费额度 + LLM 免费档，日常运行 **0 元**。

---

## 🔧 部署与维护

### 仓库结构

```
dailydawn/
├── .github/workflows/
│   ├── daily-report.yml    每日生成 + 提交 + 推送
│   └── deploy-pages.yml    把 zh/ en/ 渲染成网页并发布
├── prompts/                LLM 提示词（改这里就能调内容风格）
│   ├── analyze.zh.md
│   └── analyze.en.md
├── scripts/
│   ├── main.py             入口：抓取 → 聚合 → LLM → 落盘
│   ├── aggregator.py       跨源去重 + 排序
│   ├── renderer.py         JSON → Markdown
│   ├── build_feed.py       Markdown → RSS / JSON Feed
│   ├── build_site.py       Markdown → 静态网页
│   ├── notify_push.py      Telegram + 邮件推送
│   ├── update_readme.py   把最近 3 期注入本文件
│   └── fetchers/ pipeline/ 数据源与多 agent 流水线
├── zh/YYYY/YYYY-MM-DD.md   中文日报产出
├── en/YYYY/YYYY-MM-DD.md   英文日报产出
└── feed/                   RSS / JSON Feed 产出
```

### 必需的 Secrets / Variables

在 `Settings → Secrets and variables → Actions` 配置：

**Secrets（加密）**

| 名称 | 说明 |
|---|---|
| `LLM_API_KEY` | LLM 的 API Key |
| `LLM_BASE_URL` | OpenAI 兼容端点，如 `https://generativelanguage.googleapis.com/v1beta/openai` |
| `TELEGRAM_BOT_TOKEN` | 可选，不填则跳过 Telegram |
| `TELEGRAM_CHAT_ID` | 可选，你的 chat id |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USERNAME` / `SMTP_PASSWORD` | 可选，不填则跳过邮件（QQ 邮箱用 `smtp.qq.com` / `465` + 授权码） |
| `MAIL_TO` | 可选，收件人，多个用逗号分隔 |

**Variables（明文）**

| 名称 | 当前值 | 说明 |
|---|---|---|
| `LLM_MODEL` | `gemini-3.1-flash-lite` | 主模型 |
| `LLM_FALLBACK_MODELS` | `gemini-3.5-flash-lite,gemini-3-flash-preview` | 限流时依次降级 |
| `SITE_BASE_URL` | `https://siweimidu.github.io/dailydawn` | 生成链接用的站点地址 |

### 换模型

只改 Variables，不用改代码：

| 想用 | `LLM_MODEL` | `LLM_BASE_URL` |
|---|---|---|
| Gemini | `gemini-3.1-flash-lite` | `https://generativelanguage.googleapis.com/v1beta/openai` |
| Groq | `openai/gpt-oss-120b` | `https://api.groq.com/openai/v1` |
| DeepSeek | `deepseek-chat` | `https://api.deepseek.com` |

### 改日报内容

改 `prompts/analyze.zh.md`（中文）和 `prompts/analyze.en.md`（英文），不要改代码：

- 输出太水 → 加「每个趋势必须引用至少 2 个具体 URL」
- 中文不自然 → 加「口语化，避免学术腔」
- 小节数量不稳定 → 用「恰好 N 个」代替「3-5 个」

改完 commit，下次运行自动生效。

### 手动跑一次

`Actions → Daily Report → Run workflow`。跑完会自动 commit 日报、更新 Feed、部署网页、推送 Telegram 和邮箱。

---

## 💻 本地运行

```bash
git clone https://github.com/siweimidu/dailydawn.git
cd dailydawn
pip install -r requirements.txt
cp .env.example .env      # 填 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL
python scripts/main.py    # 产出 zh/2026/今日.md + en/2026/今日.md
```

只生成网页和 Feed（不调 LLM，不花钱）：

```bash
python scripts/build_feed.py    # → feed/*.xml, feed/*.json
python scripts/build_site.py    # → _site/（本地预览用）
python -m http.server -d _site 8000
```

本地推送测试（需要 `TELEGRAM_BOT_TOKEN` 等环境变量）：

```bash
python scripts/notify_push.py
```

---

## ❓ 常见问题

**Q：报错 `429 RESOURCE_EXHAUSTED` / `Quota exceeded`？**
Gemini 免费档按模型计费，flash-lite 是 **500 次请求/天**。流水线一次约 18–40 次调用，正常情况下够用；但同一把 Key 被别的项目共用时会被打满。
本仓库已配降级链：主模型 429 时自动切 `gemini-3.5-flash-lite`，再切 `gemini-3-flash-preview`。日志里出现 `⚠ rate limited on [...]; trying next model in chain` 就是降级生效了，日报仍会正常产出。
配额每天 UTC 00:00 重置。全部模型都用尽才会失败。

**Q：想让 Telegram 发全文而不是摘要？**
在 workflow 的推送步骤加环境变量 `TG_FULL: "1"`（会分成多条消息发送）。

**Q：为什么 cron 设在 UTC 00:00？**
按需求自定，改 `.github/workflows/daily-report.yml` 的 `cron` 即可。注意 GitHub 的定时任务在仓库不活跃时可能延迟几分钟到几十分钟。

**Q：数据源抓不到？**
单个源失败会自动跳过、不阻塞流水线。GitHub Trending 是 HTML 爬取，页面结构变化会失效；Reddit 公开 JSON 高峰期可能 429。

**Q：会重复吗？**
不会。`meta/recent-taglines.jsonl` 保存最近 7 天主题，主笔在 prompt 里被硬约束禁止主题重合。

---

## 🙏 上游与许可

本仓库 fork 自 [TangSY/dailydawn](https://github.com/TangSY/dailydawn)（MIT），在内容引擎基础上增加了：

- RSS 2.0 / JSON Feed 生成（`scripts/build_feed.py`）
- GitHub Pages 静态站点（`scripts/build_site.py` + `deploy-pages.yml`）
- Telegram + 邮件推送（`scripts/notify_push.py`）
- 限流模型降级链（`scripts/pipeline/llm.py`）

感谢原作者 [@TangSY](https://github.com/TangSY) 开源。

[License: MIT](./LICENSE)
