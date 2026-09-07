"""Build the public navigation from an explicit allowlist; no private files copied."""
from pathlib import Path
from urllib.parse import quote
import re
import shutil
import argparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist' / 'pages'
PUBLIC_FILES = [
    'examples/attention-is-all-you-need/index.html',
    'examples/lightgcn/index.html',
    'examples/lightgcn/outline.md',
    'assets/learning.css', 'assets/learning.js', 'assets/quickstart.js',
]
MEDIA_FILES = ['media/skills-demo.mp4', 'media/demo-poster.png', 'media/demo-zh.vtt']


def build(with_media=True):
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
    # Explicitly reviewed files only; the complete workspace is never uploaded.
    for relative in PUBLIC_FILES + (MEDIA_FILES if with_media else []):
        source = ROOT / relative
        if not source.is_file() or source.is_symlink():
            raise ValueError(f'Missing or unsafe public file: {relative}')
        (OUT / relative).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, OUT / relative)
    print('Built public navigation: dist/pages/index.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--without-media', action='store_true', help='Local preview before recording; never used in deployment')
    args = parser.parse_args()
    build(with_media=not args.without_media)
