"""Refresh package file inventories after an intentional edit."""
import json
from library import ROOT, child, digest

path = ROOT / 'catalog.json'
data = json.loads(path.read_text(encoding='utf-8'))
for skill in data['skills']:
    package = child(ROOT, skill['package'])
    files = {}
    for file in sorted(package.rglob('*')):
        if file.is_symlink():
            raise ValueError(f'Symlink in package: {file}')
        if file.is_file():
            files[file.relative_to(package).as_posix()] = digest(file)
    skill['files'] = files
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('Updated package file hashes. Run scripts/validate.py next.')
