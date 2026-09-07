"""Shared, dependency-free catalog and integrity helpers."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def child(root, relative):
    base = root.resolve()
    candidate = root / relative
    resolved = candidate.resolve()
    if resolved == base or not resolved.is_relative_to(base):
        raise ValueError(f'Path outside allowed directory: {relative}')
    if candidate.is_symlink():
        raise ValueError(f'Symlink not allowed: {relative}')
    return candidate


def load_catalog():
    data = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    skills = data['skills']
    names = set()
    for skill in skills:
        sid = skill['id']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', sid) or sid in names:
            raise ValueError(f'Invalid or duplicate skill ID: {sid}')
        names.add(sid)
        child(ROOT, skill['package'])
    return skills


def verify_package(skill):
    package = child(ROOT, skill['package'])
    expected = skill['files']
    actual = set()
    for path in package.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Symlink in package: {path}')
        if path.is_file():
            actual.add(path.relative_to(package).as_posix())
    if actual != set(expected):
        raise ValueError(f'File inventory mismatch: {skill["id"]}')
    for relative, value in expected.items():
        path = child(package, relative)
        if digest(path) != value:
            raise ValueError(f'Hash mismatch: {skill["id"]}/{relative}')
    return package
