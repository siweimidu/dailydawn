"""Static site generator for DailyDawn reports (stdlib only).

Reads zh/**.md and en/**.md, writes a GitHub Pages site to _site/:
  _site/index.html            landing (links to zh/en)
  _site/zh/index.html         archive list (latest first)
  _site/zh/2026/01-01.html    per-day pages (also copy md as .md)
  _site/en/...                same for English
"""
from __future__ import annotations

import html as html_mod
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

CSS = """
body{font-family:-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
max-width:860px;margin:0 auto;padding:24px;line-height:1.75;color:#222;background:#fafafa}
a{color:#0b62d6;text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:1.6em;border-bottom:2px solid #eee;padding-bottom:.3em}
h2{font-size:1.25em;margin-top:1.8em}h3{font-size:1.05em}
blockquote{border-left:4px solid #f0a500;margin:1em 0;padding:.4em 1em;
background:#fffbe8;color:#555;border-radius:0 6px 6px 0}
pre{background:#111;color:#eee;padding:14px;border-radius:8px;overflow-x:auto}
code{background:#eee;padding:2px 5px;border-radius:4px}
pre code{background:none;padding:0;color:inherit}
table{border-collapse:collapse;margin:1em 0}td,th{border:1px solid #ddd;padding:6px 12px}
.nav{margin-bottom:20px;font-size:.9em}.day{margin:2px 0}
"""


def md_to_html(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_code = in_quote = in_ul = in_table = False
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            out.append(html_mod.escape(raw))
            continue
        if line.startswith("| ") and "|" in line[2:]:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
                continue
            tag = "th" if not in_table else "td"
            if not in_table:
                out.append("<table>")
                in_table = True
                tag = "th"
            out.append("<tr>" + "".join(f"<{tag}>{inline(escape(c))}</{tag}>" for c in cells) + "</tr>")
            continue
        elif in_table:
            out.append("</table>")
            in_table = False
        if not line.strip():
            if in_quote:
                out.append("</blockquote>")
                in_quote = False
            if in_ul:
                out.append("</ul>")
                in_ul = False
            continue
        if line.startswith(">"):
            if not in_quote:
                out.append("<blockquote>")
                in_quote = True
            out.append(inline(escape(line.lstrip("> "))))
            continue
        if in_quote:
            out.append("</blockquote>")
            in_quote = False
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(escape(m.group(2)))}</h{lvl}>")
            continue
        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(escape(m.group(1)))}</li>")
            continue
        if in_ul:
            out.append("</ul>")
            in_ul = False
        out.append(f"<p>{inline(escape(line))}</p>")
    for open_tag in (("</code></pre>") if in_code else None, ("</blockquote>") if in_quote else None, ("</ul>") if in_ul else None, ("</table>") if in_table else None):
        if open_tag:
            out.append(open_tag)
    return "\n".join(out)


def escape(s: str) -> str:
    return html_mod.escape(s, quote=False)


def inline(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def page(title: str, body: str, rel_prefix: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html_mod.escape(title)}</title><link rel="stylesheet" href="{rel_prefix}style.css">
<link rel="alternate" type="application/rss+xml" title="DailyDawn RSS (zh)" href="{rel_prefix}feed/zh.xml">
</head><body>
<div class="nav"><a href="{rel_prefix}">首页</a> · <a href="{rel_prefix}zh/">中文日报</a> · <a href="{rel_prefix}en/">EN Reports</a> · <a href="https://github.com/siweimidu/dailydawn">GitHub</a></div>
{body}
</body></html>
"""


def list_page(lang: str, entries: list[tuple[str, str, str]]) -> str:
    lis = "\n".join(f'<div class="day">📰 <a href="{href}">{label}</a></div>' for href, label, _ in entries)
    title = f"DailyDawn {'中文' if lang == 'zh' else 'EN'} 归档"
    body = f"<h1>{title}</h1>\n{lis}\n<p><a href=\"../feed/{lang}.xml\">RSS</a> · <a href=\"../feed/{lang}.json\">JSON Feed</a></p>"
    return page(title, body, "../")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "zh").mkdir(parents=True)
    (OUT / "en").mkdir(parents=True)
    (OUT / "style.css").write_text(CSS.strip(), encoding="utf-8")

    all_entries: dict[str, list[tuple[str, str, str]]] = {}
    for lang in ("zh", "en"):
        entries = []
        for path in sorted((ROOT / lang).rglob("*.md"), reverse=True):
            stem = path.stem
            if not DATE_RE.match(stem):
                continue
            year = path.parent.name
            text = path.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"^#\s+(.+)$", text, re.M)
            title = m.group(1).strip() if m else stem
            rel_dir = OUT / lang / year
            rel_dir.mkdir(exist_ok=True)
            (rel_dir / f"{stem}.html").write_text(
                page(title, md_to_html(text), "../../"), encoding="utf-8"
            )
            (rel_dir / f"{stem}.md").write_text(text, encoding="utf-8")
            entries.append((f"{year}/{stem}.html", f"{stem} · {title}", title))
        if entries:
            (OUT / lang / "index.html").write_text(list_page(lang, entries), encoding="utf-8")
        all_entries[lang] = entries

    latest_zh = all_entries["zh"][0] if all_entries.get("zh") else None
    body = "<h1>DailyDawn · 独立开发者的 AI 趋势日报</h1>"
    if latest_zh:
        body += f"<p>最新：<a href=\"zh/{latest_zh[0]}\">{latest_zh[1]}</a></p>"
    body += "<p><a href=\"zh/\">全部中文日报 →</a> · <a href=\"en/\">All EN reports →</a></p>"
    body += '<p>Feed：<a href="feed/zh.xml">RSS 中文</a> · <a href="feed/zh.json">JSON</a> · <a href="feed/en.xml">RSS EN</a></p>'
    (OUT / "index.html").write_text(page("DailyDawn", body, ""), encoding="utf-8")
    if (ROOT / "feed").exists():
        shutil.copytree(ROOT / "feed", OUT / "feed", dirs_exist_ok=True)
    counts = {k: len(v) for k, v in all_entries.items()}
    print(f"✓ _site generated: {counts}")


if __name__ == "__main__":
    main()
