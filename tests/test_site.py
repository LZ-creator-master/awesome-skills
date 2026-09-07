"""Validate the public allowlist and local page links, without a browser."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import importlib.util
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_pages', ROOT / 'scripts/build_pages.py')
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src', 'poster') and value:
                self.links.append(value)


class PublicSiteTests(unittest.TestCase):
    def test_public_files_and_relative_links(self):
        with tempfile.TemporaryDirectory() as directory:
            old_output = site.OUT
            site.OUT = Path(directory)
            try:
                site.build()
                expected = set(site.PUBLIC_FILES + site.MEDIA_FILES + ['index.html', '.nojekyll'])
                self.assertEqual({p.relative_to(site.OUT).as_posix() for p in site.OUT.rglob('*') if p.is_file()}, expected)
                for page in site.OUT.rglob('*.html'):
                    parser = LinkParser()
                    parser.feed(page.read_text(encoding='utf-8'))
                    for link in parser.links:
                        url = urlsplit(link)
                        if url.scheme or url.netloc or not url.path:
                            continue
                        target = (page.parent / unquote(url.path)).resolve()
                        self.assertTrue(target.is_relative_to(site.OUT.resolve()), link)
                        self.assertTrue(target.is_file(), f'{page.name}: {link}')
            finally:
                site.OUT = old_output


if __name__ == '__main__':
    unittest.main()
