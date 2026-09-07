"""Install selected skills without overwriting different existing skills."""
import argparse
import os
from pathlib import Path
import shutil
import sys
import tempfile
from library import load_catalog, verify_package, digest, child


def default_destination():
    return Path(os.environ.get('CODEX_HOME') or (Path.home() / '.codex')) / 'skills'


def install(skills, destination, dry_run=False):
    destination = destination.expanduser().resolve()
    plans = []
    # Preflight all requested skills before writing anything.
    for skill in skills:
        source = verify_package(skill)
        target = child(destination, skill['id'])
        if target.exists():
            if not target.is_dir():
                raise ValueError(f'Target is not a directory: {target}')
            actual = set()
            for path in target.rglob('*'):
                if path.is_symlink():
                    raise ValueError(f'Symlink in installed skill: {target}')
                if path.is_file():
                    actual.add(path.relative_to(target).as_posix())
            if actual != set(skill['files']) or any(
                digest(child(target, rel)) != value for rel, value in skill['files'].items()
            ):
                raise ValueError(f'Existing skill differs; no files overwritten: {target}')
            plans.append((skill, source, target, 'unchanged'))
        else:
            plans.append((skill, source, target, 'install'))
    for skill, source, target, action in plans:
        if action == 'install' and not dry_run:
            destination.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix='.skill-install-', dir=destination) as temp:
                staged = Path(temp) / skill['id']
                shutil.copytree(source, staged)
                for relative, value in skill['files'].items():
                    if digest(child(staged, relative)) != value:
                        raise ValueError(f'Copy verification failed: {relative}')
                if target.exists():
                    raise ValueError(f'Target appeared during installation: {target}')
                staged.rename(target)
        print(f'{"PREVIEW " if dry_run else ""}{action}: {skill["name"]} -> {target}')
    return plans


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='List Chinese names and IDs')
    parser.add_argument('--skill', action='append', default=[], help='Select an ID; repeat to select several')
    parser.add_argument('--dest', type=Path, default=default_destination(), help='Override local skill directory')
    parser.add_argument('--dry-run', action='store_true', help='Validate and preview without writing')
    args = parser.parse_args()
    skills = load_catalog()
    if args.list:
        for skill in skills:
            print(f'{skill["id"]:32} {skill["name"]}')
        return
    unknown = set(args.skill) - {s['id'] for s in skills}
    if unknown:
        parser.error('Unknown IDs: ' + ', '.join(sorted(unknown)))
    selected = [s for s in skills if not args.skill or s['id'] in args.skill]
    install(selected, args.dest, args.dry_run)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)
