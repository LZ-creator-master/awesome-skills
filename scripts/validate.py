"""Validate catalog hashes, skill metadata, and maintained local links."""
import json
import re
from urllib.parse import unquote
import yaml
from library import ROOT, load_catalog, verify_package, digest


def validate():
    skills = load_catalog()
    assert len(skills) == 17, 'Expected 17 skills'
    assert len({s['name'] for s in skills}) == 17
    maintained = [ROOT / 'README.md', ROOT / '00-使用指南.md']
    maintained += list((ROOT / 'docs').glob('*.md'))
    for skill in skills:
        package = verify_package(skill)
        assert digest(package / 'references/原始说明.txt') == skill['original_sha256'], f'Original source changed: {skill["id"]}'
        entry = package / 'SKILL.md'
        content = entry.read_text(encoding='utf-8')
        match = re.match(r'^---\n(.*?)\n---\n', content, re.S)
        assert match, f'Missing frontmatter: {entry}'
        front = yaml.safe_load(match.group(1))
        assert front['name'] == skill['id']
        assert isinstance(front['description'], str) and 0 < len(front['description']) <= 1024
        ui = yaml.safe_load((package / 'agents/openai.yaml').read_text(encoding='utf-8'))
        assert ui['interface']['display_name'] == skill['name']
        assert '$' + skill['id'] in ui['interface']['default_prompt']
        assert ui['policy']['allow_implicit_invocation'] is True
        maintained.extend([entry, ROOT / skill['folder'] / '使用说明.md'])
    for path in maintained:
        text = path.read_text(encoding='utf-8')
        assert not re.search(r'[A-Za-z]:[/\\]Users[/\\]', text), f'Personal path: {path}'
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if re.match(r'\w+://', link) or link.startswith('#'):
                continue
            relative = unquote(link.split('#')[0])
            if relative:
                target = (path.parent / relative).resolve()
                assert target.is_relative_to(ROOT.resolve()) and target.exists(), f'Broken link: {path}: {link}'
    print(json.dumps({'skills': len(skills), 'packages': 'hash verified', 'metadata': 'passed', 'maintained_links': 'passed'}, ensure_ascii=False))


if __name__ == '__main__':
    validate()
