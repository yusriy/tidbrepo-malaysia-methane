#!/usr/bin/env python3
"""Read-only methane factor audit. Flags are review prompts, never corrections."""
import argparse
import base64
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import html
import json
import math
from pathlib import Path
import statistics
import unicodedata
from urllib.request import Request, urlopen

from doi_identifiers import normalize_doi, doi_url

ROOT = Path(__file__).resolve().parents[2]
API = 'https://tidbrepo.usm.my/api/v1/database/8cb5b734-7d57-4ca5-81a6-4d1de7acee88/table/ff844ee0-03d8-4531-ae43-14f4bbdf4cd4/data'
FIELDS = ('mean', 'median', 'min', 'max', 'stdev')
VERSION = '1.1'


def normalized(text):
    return ' '.join(unicodedata.normalize('NFKC', str(text or '')).replace('−', '-').split())


def number(value):
    if value is None or str(value).strip() == '':
        return None
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('non-finite number')
    return result


def fetch_rows():
    rows, seen = [], set()
    for page in range(100):
        request = Request(f'{API}?page={page}&size=1000', headers={'Accept': 'application/json', 'User-Agent': 'TIDBRepo-ReadOnly-Audit/1.0'})
        with urlopen(request, timeout=60) as response:
            batch = json.load(response)
        if not isinstance(batch, list):
            raise ValueError('Expected a list from public API')
        if not batch:
            if not rows:
                raise ValueError('Empty database; audit aborted')
            return rows
        for row in batch:
            if row.get('id') is None or row['id'] in seen:
                raise ValueError('Missing or repeated record ID; pagination unsafe')
            seen.add(row['id'])
            rows.append(row)
    raise ValueError('Pagination did not terminate')


def prepare(row):
    unit = normalized(row.get('unit'))
    factor = 1.0
    formula = 'identity; activity basis preserved'
    if unit == 'kg CH4 ha-1 yr-1':
        unit = 'kg CH4 ha-1 day-1'
        factor = 1 / 365
        formula = 'annual value / 365; assumed 365-day year'
    values, issues = {}, []
    for field in FIELDS:
        try:
            values[field] = number(row.get(field))
            if values[field] is not None:
                values[field] *= factor
        except (ValueError, TypeError):
            values[field] = None
            issues.append(f'{field}: malformed or non-finite value')
    if not unit or not row.get('category'):
        issues.append('missing category or unit')
    lo, hi = values['min'], values['max']
    if lo is not None and hi is not None and lo > hi:
        issues.append('minimum exceeds maximum')
    if values['stdev'] is not None and values['stdev'] < 0:
        issues.append('negative standard deviation')
    for field in ('mean', 'median'):
        value = values[field]
        if value is not None and ((lo is not None and value < lo) or (hi is not None and value > hi)):
            issues.append(f'{field} outside recorded bounds; check aggregation/definitions')
    sources = sorted({normalize_doi(row[k]) for k in row if k.startswith('doi_') and row[k]})
    comparison_values = dict(values)
    statistic_semantics = 'reported statistic; no substitution'
    if row.get('countries') == 'IPCC' and values['min'] is not None and all(values[k] is None for k in ('mean', 'median', 'max')):
        comparison_values['default_factor'] = comparison_values.pop('min')
        statistic_semantics = 'owner-accepted IPCC/BUR default stored in min; default point factor, not a measured minimum'
    comparison_values.setdefault('default_factor', None)
    source = '|'.join(sources) or str(row.get('url') or row.get('countries') or 'unknown')
    return {'id': row['id'], 'category': row.get('category', ''), 'condition': row.get('condition', ''),
            'country': row.get('countries', ''), 'unit': unit, 'reported_unit': row.get('unit'),
            'comparison_values': comparison_values, 'statistic_semantics': statistic_semantics,
            'reported_dois': {k: row[k] for k in row if k.startswith('doi_') and row[k]},
            'conversion_factor': factor, 'conversion_formula': formula, 'values': values,
            'reported_values': {k: row.get(k) for k in FIELDS}, 'source': source, 'dois': sources,
            'url': row.get('url'), 'scaling_factor_not_applied': row.get('scaling_factor'),
            'issues': issues}


def audit(rows):
    if len({r.get('id') for r in rows}) != len(rows):
        raise ValueError('Duplicate record IDs')
    prepared = [prepare(r) for r in rows]
    groups = defaultdict(list)
    for row in prepared:
        groups[(row['category'], row['unit'])].append(row)
    signals, unassessed, contrasts = [], [], []
    # Exact condition and country restrict formal peer comparisons. Multiple records
    # from a source contribute one median, and the candidate source is left out.
    for candidate in prepared:
        for field in ('mean', 'median', 'min', 'max', 'default_factor'):
            value = candidate['comparison_values'].get(field)
            if value is None:
                continue
            peers = defaultdict(list)
            peer_ids = []
            for other in groups[(candidate['category'], candidate['unit'])]:
                v = other['comparison_values'].get(field)
                overlap = set(candidate['dois']) & set(other['dois'])
                if (other['source'] != candidate['source'] and not overlap and candidate['condition']
                    and normalized(other['condition']).casefold() == normalized(candidate['condition']).casefold()
                    and other['country'] == candidate['country'] and v is not None and v > 0 and value > 0):
                    peers[other['source']].append(math.log10(v))
                    peer_ids.append(other['id'])
            if len(peers) < 3 or len(peer_ids) < 6:
                unassessed.append({'id': candidate['id'], 'statistic': field, 'reason': 'insufficient independent peers with matching condition, country and statistic'})
                continue
            reference = [statistics.median(v) for v in peers.values()]
            center = statistics.median(reference)
            mad = statistics.median(abs(v - center) for v in reference)
            if mad == 0:
                unassessed.append({'id': candidate['id'], 'statistic': field, 'reason': 'zero reference MAD'})
                continue
            score = .6745 * (math.log10(value) - center) / mad
            if abs(score) > 3.5:
                signals.append({'id': candidate['id'], 'statistic': field, 'modified_z_log10': score, 'peer_ids': peer_ids,
                                'independent_sources': len(peers), 'status': 'investigate; not a verified error'})
    for (category, unit), members in groups.items():
        for field in ('mean', 'median', 'min', 'max', 'default_factor'):
            candidates = [r for r in members if r['comparison_values'].get(field) is not None and r['comparison_values'].get(field) > 0]
            if len(candidates) < 2:
                continue
            low = min(candidates, key=lambda r: r['comparison_values'].get(field))
            high = max(candidates, key=lambda r: r['comparison_values'].get(field))
            ratio = high['comparison_values'].get(field) / low['comparison_values'].get(field)
            if ratio >= 100:
                contrasts.append({'category': category, 'unit': unit, 'statistic': field, 'low_id': low['id'],
                                  'high_id': high['id'], 'ratio': ratio,
                                  'status': 'context only: conditions/countries/boundaries may differ; not a peer outlier'})
    return {'analysis_version': VERSION, 'rows': prepared, 'peer_signals': signals, 'unassessed': unassessed,
            'contextual_contrasts': contrasts, 'group_count': len(groups),
            'consistency_issues': [{'id': r['id'], 'issues': r['issues']} for r in prepared if r['issues']]}


def plots(result, directory):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    groups = defaultdict(list)
    for row in result['rows']:
        groups[(row['category'], row['unit'])].append(row)
    output = []
    items = sorted(groups.items())
    # Each category is a panel; height expands to keep all 180 labels legible.
    for page, offset in enumerate(range(0, len(items), 5), 1):
        batch = items[offset:offset + 5]
        heights = [max(2.1, len(members) * .27 + .9) for _, members in batch]
        fig, axes = plt.subplots(len(batch), 1, figsize=(13, sum(heights) + .8), gridspec_kw={'height_ratios': heights}, squeeze=False)
        for ax, ((category, unit), members) in zip(axes[:, 0], batch):
            all_values = [v for r in members for k, v in r['values'].items() if v is not None and k != 'stdev']
            if all_values and min(all_values) > 0 and max(all_values) / min(all_values) > 50:
                ax.set_xscale('log')
                scale = 'log'
            elif all_values and min(all_values) <= 0 and max(abs(x) for x in all_values) > 0:
                nonzero = [abs(v) for v in all_values if v]
                ax.set_xscale('symlog', linthresh=min(nonzero) if nonzero else 1)
                scale = 'symlog (signed; linear near zero)'
                ax.axvline(0, color='grey', lw=.7)
            else:
                scale = 'linear'
            for y, row in enumerate(members):
                v = row['values']
                default = row['comparison_values']['default_factor']
                if default is not None:
                    ax.plot(default, y, marker='*', color='#8055a2', ms=7, linestyle='none')
                if v['min'] is not None and v['max'] is not None:
                    ax.plot([v['min'], v['max']], [y, y], color='#8999ab', lw=2)
                for key, marker, color in [('mean', 'o', '#147d92'), ('median', 'D', '#d47919'), ('min', '|', '#536273'), ('max', '|', '#536273')]:
                    if v[key] is not None and not (key == 'min' and default is not None):
                        ax.plot(v[key], y, marker=marker, color=color, ms=5, linestyle='none')
            ax.set_yticks(range(len(members)), [f"{r['id']} · {str(r['condition'])[:64]} [{r['country']}]" for r in members], fontsize=7)
            ax.invert_yaxis()
            ax.set_title(category, fontsize=10, loc='left')
            ax.set_xlabel(f'{unit} · {scale} scale', fontsize=8)
            ax.grid(axis='x', alpha=.2)
            ax.margins(y=.15)
        fig.legend(handles=[Line2D([], [], marker='*', color='#8055a2', ls='', label='IPCC default stored in min'), Line2D([], [], marker='o', color='#147d92', ls='', label='Reported mean'), Line2D([], [], marker='D', color='#d47919', ls='', label='Reported median'), Line2D([], [], color='#8999ab', label='Reported min–max (not confidence interval)')], loc='upper center', bbox_to_anchor=(.5, .98), ncol=2, fontsize=8)
        fig.suptitle(f'Methane factor audit · contextual comparisons · page {page}', y=.998, fontsize=12)
        fig.tight_layout(rect=(0, 0, 1, .91))
        name = f'factors-{page:02}.png'
        fig.savefig(directory / name, dpi=130, bbox_inches='tight')
        plt.close(fig)
        output.append(name)
    return output


def write_report(result, directory):
    escape = lambda value: html.escape(str(value), quote=True)
    intro = (f"Read-only audit of {len(result['rows'])} database records across {result['group_count']} category/unit groups. "
             f"{len(result['consistency_issues'])} records have numerical consistency prompts; "
             f"{len(result['peer_signals'])} statistical peer signals; {len(result['contextual_contrasts'])} broad magnitude contrasts. "
             f"{len(result['unassessed'])} stored statistics lack sufficient usable peer references. None of these results verifies or changes a factor.")
    limitations = ('Groups in the plots share category and unit only: species, process, country, methods and system boundaries can differ. '
                   'A 100-fold category contrast is a navigation aid, not an implausibility threshold. '
                   'Peer screening requires matching condition, country and statistic, at least six other rows and three independent source groups; '
                   'source medians are weighted equally and overlapping DOI sources are excluded. Unknown source identities can remain dependent. '
                   'Positive peer values use a log10 modified z score threshold of 3.5. Nonpositive values remain visible but are not scored. '
                   'No universal physical limits are assumed. Missing signals do not demonstrate plausibility. '
                   'Means, medians and endpoints are never substituted for each other. Owner-accepted IPCC/BUR defaults stored only in min are separately labeled default factors, with raw values preserved; they are not treated as measured minima. Ranges are reported bounds, not uncertainty intervals. '
                   'Annual area fluxes are divided by 365; no other numeric conversions are applied. Scaling-factor modifiers are retained, not multiplied automatically. '
                   'Oil/gas sales-volume, energy, BOD, product, dry matter and dry fuel bases remain separate. '
                   'Previously closed sago conversion Q01 and paddy Q02 decisions remain closed; contextual plots do not reopen them.')
    parts = [f'<h1>Methane emission-factor review · {escape(result["run_id"])}</h1>', f'<p>{escape(intro)}</p>',
             '<h2>How to review</h2><p>Start with consistency prompts, then inspect the contextual comparisons. Follow record DOI/source links to check original tables, units, conditions and boundaries before deciding whether any value needs correction. No database records were changed.</p>',
             f'<p>{escape(limitations)}</p>', '<h2>Numerical consistency prompts</h2>']
    parts.append('<ul>' + ''.join(f'<li>Record {r["id"]}: {escape("; ".join(r["issues"]))}</li>' for r in result['consistency_issues']) + '</ul>' if result['consistency_issues'] else '<p>None detected.</p>')
    parts.append('<h2>Contextual magnitude contrasts — review conditions first</h2><ul>')
    for r in result['contextual_contrasts']:
        parts.append(f'<li>{escape(r["category"])} · {escape(r["statistic"])}: records {r["low_id"]} and {r["high_id"]}, {r["ratio"]:,.0f}× span ({escape(r["unit"])}). {escape(r["status"])}</li>')
    parts.append('</ul><p>Review near-zero denominators before interpreting very large ratios. Check the original source and conversion for the lowest aquatic fluxes; country, season and measurement boundary differences may explain other contrasts. Previously closed Q01/Q02 decisions remain closed.</p><h2>Peer signals</h2><pre>' + escape(json.dumps(result['peer_signals'], indent=2)) + '</pre>')
    parts.append('<h2>Plots</h2>')
    for filename in result['plots']:
        data = base64.b64encode((directory / filename).read_bytes()).decode()
        parts.append(f'<img alt="Category factor comparison {escape(filename)}" style="max-width:100%" src="data:image/png;base64,{data}">')
    parts.append('<h2>Record inventory and provenance</h2><table border="1" cellspacing="0" cellpadding="4"><tr><th>ID</th><th>Category / condition / country</th><th>Normalized statistics</th><th>Unit and conversion</th><th>Sources</th></tr>')
    for r in result['rows']:
        links = ' '.join(f'<a href="{escape(doi_url(doi))}">{escape(doi)}</a>' for doi in r['dois'])
        # Only safe web URLs become clickable; all metadata is escaped.
        if r.get('url') and str(r['url']).startswith(('https://', 'http://')):
            links += f' <a href="{escape(r["url"])}">source</a>'
        values = ', '.join(f'{k}={v:.8g}' for k, v in r['values'].items() if v is not None)
        parts.append(f'<tr><td>{r["id"]}</td><td>{escape(r["category"])}<br>{escape(r["condition"])}<br>{escape(r["country"])}</td><td>{escape(values)}<br>{escape(r.get("statistic_semantics", "historical audit"))}</td><td>{escape(r["unit"])}<br>{escape(r["conversion_formula"])}</td><td>{links or escape(r["source"])}</td></tr>')
    parts.append(f'</table><p>Snapshot SHA-256: {result["snapshot_sha256"]}; analysis version {VERSION}. Original values and conversion factors are preserved in audit.json. Raw API response stays local.</p><p>Method reference: <a href="https://itl.nist.gov/div898/handbook/eda/section3/eda35h.htm">NIST: detection of outliers</a>. Statistical signals are exploratory and do not establish errors.</p>')
    document = '<!doctype html><html><head><meta charset="utf-8"><title>Methane factor audit</title></head><body style="font:14px sans-serif;max-width:1400px;margin:24px auto">' + '\n'.join(parts) + '</body></html>'
    (directory / 'report.html').write_text(document)
    summary = f'# Methane factor audit · {result["run_id"]}\n\n{intro}\n\n{limitations}\n\n[Full report with plots and source inventory](report.html) · [Machine-readable findings](audit.json)\n\n'
    for r in result['contextual_contrasts']:
        summary += f'- {r["category"]}: {r["statistic"]}, records {r["low_id"]}/{r["high_id"]}, {r["ratio"]:,.0f}× contextual span.\n'
    for name in result['plots']:
        summary += f'\n![Category comparisons]({name})\n'
    summary += '\nMethod: [NIST outlier guidance](https://itl.nist.gov/div898/handbook/eda/section3/eda35h.htm). No automatic corrections or verification changes.\n'
    (directory / 'report.md').write_text(summary)
    return intro


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, help='Explicit local snapshot instead of live GET (identified in provenance)')
    parser.add_argument('--run-id', default=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    args = parser.parse_args()
    if not args.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.run_id):
        parser.error('run-id must be alphanumeric, dash or underscore')
    local = ROOT / 'knowledge_base/plausibility_audits/runs' / args.run_id
    curated = ROOT / 'knowledge_base/reports/plausibility' / args.run_id
    if local.exists() or curated.exists():
        parser.error('run ID already exists; immutable reports must not be overwritten')
    rows = json.loads(args.snapshot.read_text()) if args.snapshot else fetch_rows()
    raw = json.dumps(rows, ensure_ascii=False, indent=2).encode()
    result = audit(rows)
    result.update(run_id=args.run_id, snapshot_sha256=hashlib.sha256(raw).hexdigest(), source_api=API,
                  acquisition='explicit local snapshot' if args.snapshot else 'live public GET; pagination checked to empty terminal page',
                  generated_at=datetime.now(timezone.utc).isoformat())
    local.mkdir(parents=True)
    curated.mkdir(parents=True)
    (local / 'snapshot.json').write_bytes(raw)
    result['plots'] = plots(result, curated)
    (curated / 'audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    summary = write_report(result, curated)
    print(json.dumps({'run_id': args.run_id, 'report': str(curated / 'report.html'), 'summary': summary, 'plots': result['plots']}))


if __name__ == '__main__':
    main()
