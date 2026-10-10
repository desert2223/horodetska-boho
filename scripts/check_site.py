"""Check local static site links and images. Run: python scripts/check_site.py"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

SITE = Path(__file__).resolve().parent.parent

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for attr, value in attrs:
            if attr in {"href", "src"} and value:
                self.refs.append((tag, attr, value))

errors = []
html_files = list(SITE.rglob("*.html"))
for html in html_files:
    parser = References()
    parser.feed(html.read_text(encoding="utf-8"))
    for tag, attr, raw in parser.refs:
        url = urlsplit(raw)
        if url.scheme or url.netloc or raw.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
            continue
        path = unquote(url.path)
        if not path:
            continue
        target = (SITE / path.lstrip("/")) if path.startswith("/") else (html.parent / path)
        if target.is_dir():
            target /= "index.html"
        if not target.exists():
            errors.append(f"{html.relative_to(SITE)}: missing {attr}={raw}")

if not (SITE / 'index.html').exists():
    errors.append('Site root is missing index.html')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'OK: validated {len(html_files)} HTML files and their local references')
