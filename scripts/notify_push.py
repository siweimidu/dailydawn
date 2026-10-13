"""把当日日报推送到 Telegram 和邮箱（纯标准库）。

需要环境变量：
  TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID          缺失则跳过 Telegram
  SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, MAIL_TO   缺失则跳过邮件
  SITE_BASE_URL                                 链接前缀（默认 Pages 地址）
"""
from __future__ import annotations

import json
import os
import re
import smtplib
import ssl
import sys
import urllib.request
from datetime import datetime, timezone
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_BASE_URL = os.getenv("SITE_BASE_URL", "https://siweimidu.github.io/dailydawn").rstrip("/")
TG_API = "https://api.telegram.org/bot{token}/{method}"
MAX_TG_LEN = 4000


def today() -> str:
    return os.getenv("REPORT_DATE") or datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_report(lang: str, date: str) -> str | None:
    path = ROOT / lang / date[:4] / f"{date}.md"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def top_signals(markdown: str, limit: int = 3) -> list[str]:
    """抽取 Top N 信号那一行的正文，去掉加粗标记。"""
    block = re.search(r">\s*\*\*📍.*?\n((?:>.*\n)+)", markdown)
    if not block:
        return []
    items: list[str] = []
    for line in block.group(1).splitlines():
        m = re.match(r"^>\s*(?:\d+\.)?\s*(.+)$", line.strip())
        if not m:
            continue
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", m.group(1)).strip()
        if text.startswith("高置信度") or text.startswith("外部发现") or text.startswith("双重验证"):
            items.append(text)
        if len(items) >= limit:
            break
    return items


def tg_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def send_telegram(markdown_zh: str, date: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        print("⚠ telegram skipped (no TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID)")
        return False

    url = f"{SITE_BASE_URL}/zh/{date[:4]}/{date}.html"
    head = (
        f"<b>🌅 DailyDawn · {date}</b>\n\n"
        f"<a href=\"{url}\">📖 完整日报（中英双语）</a>\n"
        f"<a href=\"{SITE_BASE_URL}/feed/zh.xml\">📡 RSS</a>\n"
    )
    signals = top_signals(markdown_zh)
    if signals:
        head += "\n<b>今日 Top 信号</b>\n"
        for i, s in enumerate(signals, 1):
            short = s if len(s) <= 300 else s[:297] + "…"
            head += f"\n{i}. {tg_escape(short)}"

    chunks = [head]
    if os.getenv("TG_FULL", "").strip().lower() in ("1", "true", "yes"):
        body = re.sub(r"^#.*\n", "", markdown_zh, count=1)
        for para in re.split(r"\n(?=## )", body):
            p = para.strip()
            if not p:
                continue
            p = tg_escape(p)
            for j in range(0, len(p), MAX_TG_LEN):
                chunks.append(p[j : j + MAX_TG_LEN])

    sent = 0
    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        req = urllib.request.Request(
            TG_API.format(token=token, method="sendMessage"),
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                ok = json.loads(resp.read()).get("ok")
            if not ok:
                raise RuntimeError(f"telegram api not ok for chunk {i}")
            sent += 1
        except Exception as err:  # noqa: BLE001
            print(f"✗ telegram chunk {i} failed: {type(err).__name__}: {str(err)[:200]}")
            return sent > 0
    print(f"✓ telegram sent ({sent} messages)")
    return True


def send_email(markdown_zh: str, date: str) -> bool:
    host = os.getenv("SMTP_HOST", "").strip()
    user = os.getenv("SMTP_USERNAME", "").strip()
    password = os.getenv("SMTP_PASSWORD", "").strip()
    to_raw = os.getenv("MAIL_TO", "").strip()
    if not all([host, user, password, to_raw]):
        print("⚠ email skipped (missing SMTP_HOST/SMTP_USERNAME/SMTP_PASSWORD/MAIL_TO)")
        return False

    port = int(os.getenv("SMTP_PORT", "465") or 465)
    recipients = [x.strip() for x in re.split(r"[,;]", to_raw) if x.strip()]
    url = f"{SITE_BASE_URL}/zh/{date[:4]}/{date}.html"

    try:
        from scripts.build_site import md_to_html  # 复用 Pages 的渲染器

        html_body = md_to_html(markdown_zh)
    except Exception:  # noqa: BLE001
        html_body = "<pre>" + (
            markdown_zh.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        ) + "</pre>"

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,'Segoe UI','PingFang SC',sans-serif;max-width:760px;margin:0 auto;padding:20px;color:#222">
<h1 style="font-size:1.5em">🌅 DailyDawn · {date}</h1>
<p><a href="{url}" style="display:inline-block;background:#0b62d6;color:#fff;padding:10px 18px;border-radius:6px;text-decoration:none">在浏览器打开完整日报 →</a></p>
<hr style="border:none;border-top:1px solid #eee;margin:24px 0">
{html_body}
<hr style="border:none;border-top:1px solid #eee;margin:24px 0">
<p style="color:#888;font-size:12px">RSS：<a href="{SITE_BASE_URL}/feed/zh.xml">{SITE_BASE_URL}/feed/zh.xml</a> · 由 GitHub Actions 自动生成</p>
</body></html>"""

    msg = MIMEText(html, "html", "utf-8")
    msg["Subject"] = Header(f"DailyDawn · {date} AI 趋势日报", "utf-8")
    msg["From"] = formataddr(("DailyDawn", user))
    msg["To"] = ", ".join(recipients)

    ctx = ssl.create_default_context()
    try:
        if port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=60, context=ctx)
        else:
            server = smtplib.SMTP(host, port, timeout=60)
            server.ehlo()
            server.starttls(ctx)
        with server:
            server.login(user, password)
            server.sendmail(user, recipients, msg.as_string())
        print(f"✓ email sent to {len(recipients)} recipient(s)")
        return True
    except Exception as err:  # noqa: BLE001
        print(f"✗ email failed: {type(err).__name__}: {str(err)[:200]}")
        return False


def main() -> int:
    date = today()
    zh = load_report("zh", date)
    if not zh:
        print(f"✗ no report for {date} (expected zh/{date[:4]}/{date}.md)")
        return 1

    results = []
    if os.getenv("TELEGRAM_BOT_TOKEN", "").strip():
        results.append(send_telegram(zh, date))
    if os.getenv("SMTP_HOST", "").strip():
        results.append(send_email(zh, date))
    if not results:
        print("⚠ nothing configured (both Telegram and SMTP missing)")
        return 0
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    raise SystemExit(main())
