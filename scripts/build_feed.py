"""Generate RSS 2.0 + JSON Feed from zh/ en/ daily reports.

Outputs:
  feed/zh.xml, feed/en.xml   RSS 2.0
  feed/zh.json, feed/en.json JSON Feed 1.1
Base URL for links: GitHub Pages site (configurable via env SITE_BASE_URL).
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = os.getenv("SITE_BASE_URL", "https://siweimidu.github.io/dailydawn").rstrip("/")
SITE_NAME = {"zh": "DailyDawn · 独立开发者 AI 趋势日报", "en": "DailyDawn · AI Trend Daily"}
MAX_ITEMS = 30

TITLE_RE = re.compile(r"^#\s+(.+)$", re.M)
TAGLINE_RE = re.compile(r"^>\s*(.+)$", re.M)


def collect(lang: str) -> list[dict]:
    entries = []
    for path in sorted((ROOT / lang).rglob("*.md"), reverse=True)[:MAX_ITEMS]:
        stem = path.stem
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", stem):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        m = TITLE_RE.search(text)
        title = m.group(1).strip() if m else f"DailyDawn {stem}"
        m2 = TAGLINE_RE.search(text)
        desc = m2.group(1).strip() if m2 else title
        url = f"{BASE_URL}/{lang}/{stem}.html"
        try:
            dt = datetime.strptime(stem, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        entries.append(
            {
                "title": title,
                "url": url,
                "description": desc,
                "date": stem,
                "iso": dt.strftime("%a, %d %b %Y 00:00:00 GMT"),
                "iso8601": dt.strftime("%Y-%m-%dT00:00:00Z"),
            }
        )
    return entries


def build_rss(lang: str, entries: list[dict]) -> str:
    items = "\n".join(
        "    <item>\n"
        f"      <title>{escape(e['title'])}</title>\n"
        f"      <link>{e['url']}</link>\n"
        f"      <guid isPermaLink=\"true\">{e['url']}</guid>\n"
        f"      <pubDate>{e['iso']}</pubDate>\n"
        f"      <description>{escape(e['description'])}</description>\n"
        "    </item>"
        for e in entries
    )
    latest = entries[0]["iso"] if entries else ""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        f"    <title>{escape(SITE_NAME[lang])}</title>\n"
        f"    <link>{BASE_URL}/</link>\n"
        f"    <atom:link href=\"{BASE_URL}/feed/{lang}.xml\" rel=\"self\" type=\"application/rss+xml\"/>\n"
        f"    <description>DailyDawn daily AI trend report ({lang})</description>\n"
        "    <language>zh-CN</language>\n"
        "    <docs>https://www.RSS.org/specifications/rss-2.0/</docs>\n"
        f"    <lastBuildDate>{latest}</lastBuildDate>\n"
        f"{items}\n"
        "  </channel>\n"
        "</rss>\n"
    )


def build_jsonfeed(lang: str, entries: list[dict]) -> str:
    return json.dumps(
        {
            "version": "https://jsonfeed.org/version/1.1",
            "title": SITE_NAME[lang],
            "home_page_url": f"{BASE_URL}/",
            "feed_url": f"{BASE_URL}/feed/{lang}.json",
            "items": [
                {
                    "id": e["url"],
                    "title": e["title"],
                    "url": e["url"],
                    "date_published": e["iso8601"],
                    "content_text": e["description"],
                }
                for e in entries
            ],
        },
        ensure_ascii=False,
        indent=2,
    )


def main() -> None:
    feed_dir = ROOT / "feed"
    feed_dir.mkdir(exist_ok=True)
    for lang in ("zh", "en"):
        entries = collect(lang)
        if not entries:
            print(f"⚠ feed[{lang}]: no reports found, skipped")
            continue
        (feed_dir / f"{lang}.xml").write_text(build_rss(lang, entries), encoding="utf-8")
        (feed_dir / f"{lang}.json").write_text(build_jsonfeed(lang, entries), encoding="utf-8")
        print(f"✓ feed[{lang}]: {len(entries)} items -> feed/{lang}.xml + feed/{lang}.json")


if __name__ == "__main__":
    main()
