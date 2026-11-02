#!/usr/bin/env python3
"""Refresh curated navigation and audit wiki links, identities and metadata.

This command edits Markdown navigation/report files only. It never writes to the
scientific database, changes verification flags, or configures scheduled jobs.
"""
import argparse
from collections import defaultdict
from datetime import datetime
import json
from pathlib import Path
import re
from urllib.parse import unquote
from zoneinfo import ZoneInfo
from doi_identifiers import normalize_doi
from wiki_catalog import ROOT, label, metadata

NAVIGATION = Path('knowledge_base/reconciliations/wiki-navigation-2026-11-02.json')
START = '<!-- wiki-maintenance:start -->'
END = '<!-- wiki-maintenance:end -->'


def replace_block(text, body):
    block = START + '\n\n' + body.rstrip() + '\n\n' + END
    if START in text:
        a = text.index(START); b = text.index(END, a) + len(END)
        return text[:a] + block + text[b:]
    return text.rstrip() + '\n\n' + block + '\n'


def without_block(text):
    return re.sub(re.escape(START) + r'.*?' + re.escape(END), '', text, flags=re.S)


def references(page, wiki, names):
    """Return resolved local links and unresolved destinations (fragments ignored)."""
    resolved = set(); broken = []
    for value in re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', page.read_text()):
        target = value.split('#', 1)[0]
        if not target: continue
        target = target.removesuffix('.md') + '.md'
        choices = [wiki / target, page.parent / target]
        choices += names.get(Path(target).stem, []) if '/' not in target else []
        actual = next((x.resolve() for x in choices if x.is_file()), None)
        if actual is None: broken.append(value)
        else: resolved.add(actual)
    for value in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', page.read_text()):
        target = value.strip('<>').split('#', 1)[0]
        if not target or re.match(r'[a-zA-Z][\w+.-]*:', target): continue
        actual = (page.parent / unquote(target)).resolve()
        if not actual.exists(): broken.append(value)
        else: resolved.add(actual)
    return resolved, broken


def audit(repo):
    wiki = repo / 'knowledge_base/wiki'; pages = sorted(wiki.rglob('*.md'))
    names = defaultdict(list)
    for p in pages: names[p.stem].append(p)
    graph = {}; broken = []
    for p in pages:
        links, missing = references(p, wiki, names); graph[p.resolve()] = links
        broken += [str(p.relative_to(wiki)) + ' -> ' + value for value in missing]
    reachable = set(); pending = [(wiki / 'index.md').resolve()]
    while pending:
        p = pending.pop()
        if p in reachable: continue
        reachable.add(p)
        # A report listing an orphan must not itself hide the orphan next time.
        if p.name != 'lint-report.md': pending.extend(graph.get(p, set()) - reachable)
    papers = [p for p in (wiki / 'papers').glob('*.md') if p.name != 'index.md']
    identities = {'doi': defaultdict(list), 'title': defaultdict(list)}
    missing = []
    for p in papers:
        f = metadata(p)
        for key in identities:
            value = f.get(key)
            if value:
                identity = normalize_doi(value) if key == 'doi' else re.sub(r'\W+', '', str(value).casefold())
                identities[key][identity].append(p.name)
        for key in ('year', 'doi'):
            if not f.get(key): missing.append({'paper': p.name, 'field': key})
    duplicates = [key + ': ' + ' / '.join(v) for key, group in identities.items() for v in group.values() if len(v) > 1]
    coverage = {}; missing_topics = []
    for folder in ('topics', 'methods', 'locations'):
        linked = set().union(*(graph[p.resolve()] for p in (wiki / folder).glob('*.md')))
        coverage[folder] = sum(p.resolve() in linked for p in papers)
        if folder == 'topics':
            missing_topics = sorted(p.name for p in papers if p.resolve() not in linked)
    return {'markdown_pages': len(pages), 'paper_pages': len(papers), 'broken_links': sorted(broken),
            'orphan_pages': sorted(str(p.relative_to(wiki)) for p in pages if p.resolve() not in reachable),
            'duplicate_identities': sorted(duplicates), 'navigation_coverage': coverage,
            'missing_topic_links': missing_topics,
            'missing_metadata': sorted(missing, key=lambda r:(r['paper'],r['field']))}


def navigation_outputs(repo):
    path = repo / NAVIGATION
    if not path.exists(): return {}
    rows = json.loads(path.read_text())['papers']; wiki = repo / 'knowledge_base/wiki'
    outputs = {}; reverse = defaultdict(list); seen = set()
    for row in rows:
        p = wiki / 'papers' / row['paper']
        if row['paper'] in seen or not p.is_file(): raise ValueError('Missing/duplicate navigation paper: ' + row['paper'])
        seen.add(row['paper']); text = p.read_text(); f = metadata(p); base = without_block(text); links = []
        for folder in ('topics', 'methods', 'locations'):
            for slug in row[folder]:
                target = wiki / folder / (slug + '.md')
                if not target.is_file(): raise ValueError('Missing navigation destination: ' + str(target))
                reverse[target].append((p, f, row['basis']))
                if not re.search(r'\[\[' + re.escape(folder+'/'+slug) + r'(?:\||\]\])', base):
                    links.append('- [' + label(metadata(target)['title']) + '](../' + folder + '/' + slug + '.md)')
        body = '## Catalog connections\n\nNavigation basis: ' + row['basis'] + '. These links do not change scientific verification or owner decisions.\n\n'
        body += '\n'.join(links) if links else 'Existing connections above supply these navigation links.'
        outputs[p] = replace_block(text, body)
    for p, entries in reverse.items():
        text = p.read_text(); base = without_block(text); links = []
        for paper, f, basis in sorted(entries, key=lambda r:r[1]['title'].casefold()):
            if paper.stem in base: continue
            links.append('- [' + label(f['title']) + '](../papers/' + paper.name + ') — `' + f.get('verification_status', 'see note') + '`; ' + basis + '.')
        body = '## Additional catalog connections\n\nEditorial navigation based on the linked notes and stated evidence basis; scientific approval is separate.\n\n'
        body += '\n'.join(links) if links else 'All curated connections are already listed above.'
        outputs[p] = replace_block(text, body)
    for folder, title in [('topics', 'Topics and sectors'), ('methods', 'Methods'), ('locations', 'Locations')]:
        lines = ['# ' + title, '', 'Complete navigation across original machine assignments and editorial catalog connections. Counts are distinct linked paper pages, not verified measurements or independent datasets. Location links can denote study coverage or contextual scope; methods are assigned only where documented.', '']
        for p in sorted((wiki / folder).glob('*.md')):
            if p.name == 'index.md': continue
            text = outputs.get(p, p.read_text())
            slugs = set(re.findall(r'\[\[papers/([^\]|]+)', text))
            slugs.update(x.removesuffix('.md') for x in re.findall(r'\]\(\.\./papers/([^)#]+)', text))
            count = sum((wiki / 'papers' / (slug + '.md')).is_file() for slug in slugs)
            lines.append('- [' + label(metadata(p)['title']) + '](' + p.name + ') — ' + str(count) + ' linked paper pages')
        outputs[wiki / folder / 'index.md'] = '\n'.join(lines) + '\n'
    return outputs


def report(repo, checked_date):
    result = audit(repo)
    lines = ['---', 'checked_date: ' + json.dumps(checked_date), 'managed_by: "wiki_maintenance"', '---', '', '# Wiki lint report', '',
             'Checked: ' + checked_date + ' (WITA). Reproduce with `wiki_maintenance.py`; use `--check` to detect drift.', '',
             '- Markdown pages: ' + str(result['markdown_pages']), '- Paper/source pages: ' + str(result['paper_pages']),
             '- Broken local links (Markdown and Obsidian): ' + str(len(result['broken_links'])),
             '- Orphan pages (unreachable from wiki home): ' + str(len(result['orphan_pages'])),
             '- Duplicate normalized DOI/title identities: ' + str(len(result['duplicate_identities'])), '',
             'These checks find navigation/identity problems; they do not prove scientific correctness or independent datasets.', '']
    lines += ['## Navigation coverage', '']
    lines += ['- ' + folder.title() + ': ' + str(count) + '/' + str(result['paper_pages']) + ' paper pages linked.' for folder, count in result['navigation_coverage'].items()]
    lines += ['', 'Missing method/location links can reflect insufficient evidence or inapplicability; do not infer them just to fill a field.', '']
    lines += ['## Topic connections requiring editorial review', '']
    lines += (['- [' + label(metadata(repo/'knowledge_base/wiki/papers'/name)['title']) + '](papers/' + name + ')' for name in result['missing_topic_links']] or ['None.']) + ['']
    for title, key in [('Broken links','broken_links'),('Orphan pages','orphan_pages'),('Duplicate identities','duplicate_identities')]:
        lines += ['## ' + title, ''] + (['- `' + item + '`' for item in result[key]] or ['None.']) + ['']
    lines += ['## Metadata still unestablished', '']
    lines += ['- [' + label(metadata(repo/'knowledge_base/wiki/papers'/r['paper'])['title']) + '](papers/' + r['paper'] + ') — ' + r['field'] + '; see the dated bibliographic check.' for r in result['missing_metadata']] or ['None.']
    return '\n'.join(lines).rstrip() + '\n'


def run(repo, check=False, checked_date=None):
    outputs = navigation_outputs(repo)
    stale = [str(p.relative_to(repo)) for p, text in outputs.items() if not p.exists() or p.read_text() != text]
    if check and stale: raise ValueError('Stale navigation: ' + ', '.join(stale))
    if not check:
        for p, text in outputs.items(): p.write_text(text)
    path = repo / 'knowledge_base/wiki/lint-report.md'
    if not path.exists() and not check: path.write_text('# Wiki lint report\n')
    date = checked_date or (metadata(path).get('checked_date') if check and path.exists() else None)
    date = date or datetime.now(ZoneInfo('Asia/Makassar')).date().isoformat()
    expected = report(repo, date)
    if check and (not path.exists() or path.read_text() != expected): raise ValueError('Stale wiki lint report')
    if not check: path.write_text(expected)
    result = audit(repo)
    if result['broken_links'] or result['duplicate_identities'] or result['orphan_pages']:
        raise ValueError(json.dumps(result))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--check', action='store_true'); p.add_argument('--as-of')
    args = p.parse_args(); print(json.dumps(run(ROOT, args.check, args.as_of)))

if __name__ == '__main__': main()
