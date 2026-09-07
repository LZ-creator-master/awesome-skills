"""Build the public navigation from an explicit allowlist; no private files copied."""
from pathlib import Path
from urllib.parse import quote
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist' / 'pages'


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    html = (ROOT / '00-技能导航.html').read_text(encoding='utf-8')
    def link(match):
        target = match.group(1)
        if target.endswith('.md'):
            return 'href="https://github.com/LZ-creator-master/awesome-skills/blob/main/' + quote(target, safe='/') + '"'
        return match.group(0)
    html = re.sub(r'href="([^"]+)"', link, html)
    (OUT / 'index.html').write_text(html, encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')
    print('Built public navigation: dist/pages/index.html')


if __name__ == '__main__':
    build()
