import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from install import install
from library import load_catalog


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.skills = load_catalog()

    def run_quiet(self, skills, dest, dry_run=False):
        with contextlib.redirect_stdout(io.StringIO()):
            return install(skills, dest, dry_run)

    def test_preview_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / 'skills'
            self.run_quiet(self.skills, dest, True)
            self.assertFalse(dest.exists())

    def test_full_install_and_repeat(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / 'skills'
            first = self.run_quiet(self.skills, dest)
            self.assertEqual(len(first), 17)
            second = self.run_quiet(self.skills, dest)
            self.assertTrue(all(row[3] == 'unchanged' for row in second))
            self.assertEqual(len(list(dest.rglob('SKILL.md'))), 17)

    def test_conflict_stops_batch_before_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            conflict = dest / self.skills[-1]['id']
            conflict.mkdir()
            marker = conflict / 'personal.txt'
            marker.write_text('keep me', encoding='utf-8')
            with self.assertRaises(ValueError):
                self.run_quiet(self.skills, dest)
            self.assertEqual(marker.read_text(encoding='utf-8'), 'keep me')
            self.assertFalse((dest / self.skills[0]['id']).exists())

    def test_selected_skill_only(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            self.run_quiet([self.skills[0]], dest)
            self.assertEqual([p.name for p in dest.iterdir()], [self.skills[0]['id']])


if __name__ == '__main__':
    unittest.main()
