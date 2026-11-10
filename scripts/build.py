#!/usr/bin/env python3
"""Build the site into _site/.

Every app in apps/ becomes a card on the home page:
  apps/some-app.html          -> _site/apps/some-app/index.html
  apps/some-app/index.html    -> _site/apps/some-app/ (whole folder copied)

Card details come from each app's own HTML:
  <title>                          card title (falls back to the file name)
  <meta name="description">        card description
  <meta name="app:category">       filter category (default "Other")
  <meta name="app:icon">           emoji icon (default 🧩)
  <meta name="app:hidden" content="true">   don't list it (still reachable by link)
  <meta name="app:backlink" content="false"> don't add the "All apps" bar

Standard library only, so it runs anywhere with Python 3.
"""
import html
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPS = ROOT / "apps"
OUT = ROOT / "_site"
TEMPLATE = ROOT / "scripts" / "home.template.html"


class Meta(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.meta, self._in_title = "", {}, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name"):
            self.meta[a["name"].strip().lower()] = (a.get("content") or "").strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "app"


def nice_title(slug: str) -> str:
    return slug.replace("-", " ").strip().capitalize()


BACKLINK = (
    '<div id="gpt-bar" style="display:block;width:100%;box-sizing:border-box;margin:0;'
    'padding:8px 16px;background:#0f766e;'
    'font:600 13px/1.4 system-ui,-apple-system,Segoe UI,Roboto,sans-serif">'
    '<a href="../../" id="gpt-back" style="color:#fff;text-decoration:none">'
    '&larr; All apps</a></div>'
    '<style>@media print{#gpt-bar{display:none!important}}</style>'
)


def add_backlink(text: str) -> str:
    m = re.search(r"<body[^>]*>", text, re.I)
    if m:
        return text[: m.end()] + BACKLINK + text[m.end():]
    return BACKLINK + text


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "apps").mkdir(parents=True)
    site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))

    entries, used = [], set()
    sources = sorted(p for p in APPS.iterdir() if not p.name.startswith(".")) if APPS.exists() else []
    for src in sources:
        if src.is_file() and src.suffix.lower() in (".html", ".htm"):
            entry_file = src
        elif src.is_dir() and (src / "index.html").exists():
            entry_file = src / "index.html"
        else:
            continue

        slug = slugify(src.stem if src.is_file() else src.name)
        base, n = slug, 2
        while slug in used:
            slug, n = f"{base}-{n}", n + 1
        used.add(slug)

        raw = entry_file.read_text(encoding="utf-8", errors="replace")
        p = Meta()
        try:
            p.feed(raw)
        except Exception:
            pass
        meta = p.meta

        dest = OUT / "apps" / slug
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            dest.mkdir(parents=True)
        out_text = raw if meta.get("app:backlink", "").lower() == "false" else add_backlink(raw)
        (dest / "index.html").write_text(out_text, encoding="utf-8")

        if meta.get("app:hidden", "").lower() == "true":
            print(f"  hidden  apps/{slug}/")
            continue

        entries.append({
            "title": html.unescape(p.title.strip()) or nice_title(slug),
            "description": meta.get("description", ""),
            "category": meta.get("app:category") or "Other",
            "icon": meta.get("app:icon") or "🧩",
            "url": f"apps/{slug}/",
        })
        print(f"  listed  apps/{slug}/  ({entries[-1]['title']})")

    order = site.get("categoryOrder", [])
    rank = lambda c: order.index(c) if c in order else len(order)
    entries.sort(key=lambda e: (rank(e["category"]), e["title"].lower()))

    page = TEMPLATE.read_text(encoding="utf-8")
    data = json.dumps({"site": site, "apps": entries}, ensure_ascii=False).replace("</", "<\\/")
    page = page.replace("/*__DATA__*/null", data)
    page = page.replace("__SITE_NAME__", html.escape(site.get("name", "Apps")))
    page = page.replace("__BUILT__", datetime.now(timezone.utc).strftime("%-d %b %Y"))
    (OUT / "index.html").write_text(page, encoding="utf-8")
    shutil.copy(ROOT / "scripts" / "404.html", OUT / "404.html")
    (OUT / ".nojekyll").write_text("")
    print(f"Built {len(entries)} app(s) into _site/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
