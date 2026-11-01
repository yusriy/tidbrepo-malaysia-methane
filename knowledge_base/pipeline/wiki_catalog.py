#!/usr/bin/env python3
"""Index retained literature and database source pointers without promoting evidence."""
import argparse
import json
import re
from pathlib import Path
from doi_identifiers import normalize_doi

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = Path('knowledge_base/reconciliations/wiki-source-registry.json')


def label(value):
    text=re.sub(r'\s+',' ',str(value))
    for before,after in [('&','&amp;'),('[','&#91;'),(']','&#93;'),('|','&#124;'),('<','&lt;'),('>','&gt;')]:
        text=text.replace(before,after)
    return text


def metadata(path):
    text=path.read_text()
    header=text.split('---',2)[1] if text.startswith('---\n') else ''
    fields={}
    for line in header.splitlines():
        if ':' not in line: continue
        key,value=line.split(':',1);value=value.strip()
        try: fields[key]=json.loads(value)
        except (ValueError,TypeError):fields[key]=value.strip('"\'')
    fields['title']=fields.get('title') or next((x[2:] for x in text.splitlines() if x.startswith('# ')),path.stem)
    return fields


def latest_reviews(repo):
    result={}
    for path in sorted((repo/'knowledge_base/literature_updates/reviews').glob('*.json')):
        row=json.loads(path.read_text());result[row['candidate_id']]={**row,'decision_file':str(path.relative_to(repo))}
    return result


def retained_reviews(repo):
    return [r for r in latest_reviews(repo).values() if r.get('decision') in ('context_only','retrieve_extract')]


def identity_match(fields,row):
    doi=normalize_doi(row.get('doi'))
    if fields.get('candidate_id')==row.get('candidate_id') and row.get('candidate_id'):return True
    existing=normalize_doi(fields.get('doi'))
    if doi and existing:return doi==existing
    return re.sub(r'\W+','',str(fields['title']).lower())==re.sub(r'\W+','',row['title'].lower())


def registry(repo):
    p=repo/REGISTRY
    return json.loads(p.read_text()) if p.exists() else {'sources':[]}


def materialize_missing(repo):
    directory=repo/'knowledge_base/wiki/papers';directory.mkdir(parents=True,exist_ok=True)
    pages=[(p,metadata(p)) for p in directory.glob('*.md')];created=[]
    rows=retained_reviews(repo)+[{**r,'database_pointer':True} for r in registry(repo)['sources']]
    for row in rows:
        if any(identity_match(fields,row) for _,fields in pages):continue
        identity=row.get('candidate_id') or normalize_doi(row['doi'])
        import hashlib
        suffix=hashlib.sha256(identity.encode()).hexdigest()[:8]
        slug=re.sub(r'[^a-z0-9]+','-',row['title'].lower()).strip('-')[:95].rstrip('-')
        path=directory/f'{slug}-{suffix}.md'
        if path.exists():raise ValueError('Paper filename collision; refusing overwrite')
        pointer=row.get('database_pointer',False)
        status='database_source_pointer' if pointer else ('retained_context_only' if row['decision']=='context_only' else 'retained_for_factor_assessment')
        year=row.get('publication_year_check',{}).get('source_checked_year')
        fields={'title':row['title'],'doi':normalize_doi(row.get('doi')),'candidate_id':row.get('candidate_id'),
                'year':year,'verification_status':status,'manuscript_role':'retained_literature' if not pointer else 'database_source_reference',
                'managed_by':'owner-guided literature catalog'}
        lines=['---']+[k+': '+json.dumps(v,ensure_ascii=False) for k,v in fields.items()]+['---','','# '+label(row['title']),'']
        if pointer:
            lines+=['> Bibliographic pointer to a source referenced by TIDBRepo. Catalog inclusion does not verify its measurements or imply full-text ingestion.','',
                    '- Source DOI: https://doi.org/'+row['doi'],
                    '- Referenced database rows: '+', '.join(str(i) for i in row['tidbrepo_row_ids']),
                    '- Bibliographic metadata: '+row['metadata_source'],
                    '- Database reference coverage: `'+str(REGISTRY)+'`',
                    '- Full-text synthesis and measurement verification: not established by this catalog entry.']
        else:
            lines+=['> '+('Retained as wiki context by owner decision; quantitative measurements are not approved by this retention decision.' if row['decision']=='context_only' else 'Retained for factor assessment. See the latest owner review and database completion record for quantitative approval.'),'',
                    '- Candidate ID: `'+row['candidate_id']+'`',
                    '- Source: '+str(row.get('source_url') or ('https://doi.org/'+row.get('doi',''))),
                    '- DOI: '+(normalize_doi(row.get('doi')) or 'Not established; do not invent a DOI.'),
                    '- Publication year: '+(str(year)+' (source checked)' if year else 'Not independently established in this note; consult the source.'),
                    '- Owner decision: `'+row['decision']+'`',
                    '- Decision record: `'+row['decision_file']+'`',
                    '- Reason: '+row.get('reason','Recorded owner decision'),
                    '- Review and limitations: [['+row['wiki_review_page']+'|Owner review]]']
        lines+=['','## Use in research','','Use this page as a source entry point. Follow its review record and original source before citing numerical results; preserve units, statistic meaning, study conditions and source locators. Do not infer atmospheric emission factors from production yields or model outputs.','','[Complete literature catalog](index.md)','']
        path.write_text('\n'.join(lines));created.append(str(path.relative_to(repo)));pages.append((path,fields))
    return created


def render(repo):
    pages=sorted((repo/'knowledge_base/wiki/papers').glob('*.md'))
    rows=[(p,metadata(p)) for p in pages if p.name!='index.md']
    groups=[('Original quantitative manuscript baseline',lambda f:f.get('manuscript_role')=='quantitative_baseline'),
            ('Original supporting corpus',lambda f:f.get('manuscript_role')=='supporting_corpus'),
            ('Monthly paper pages and owner-retained literature',lambda f:f.get('manuscript_role') not in ('quantitative_baseline','supporting_corpus','database_source_reference')),
            ('Database references awaiting full-text wiki synthesis',lambda f:f.get('manuscript_role')=='database_source_reference')]
    lines=['# Complete literature catalog','',f'**{len(rows)} distinct paper/source pages.** This catalog includes the original corpus, reviewed monthly additions, owner-retained wiki context and bibliographic pointers for DOI sources in the recorded TIDBRepo snapshot. It does not claim all papers worldwide or all discovered candidates are retained.','',
           'Status labels matter: wiki-only retention, source-pointer coverage, reviewed factor suitability and database submission are different states. Original machine-extracted pages and proposals keep their existing verification flags.','',
           'For pending/excluded discoveries, use [the discovery and decision archive](../unverified-literature/index.md). For work still requiring a decision, use [the review queue](../review-queue.md). IPCC/BUR official reports may have no DOI and remain documented through report citations and reconciliation records.','']
    for title,predicate in groups:
        selected=sorted([(p,f) for p,f in rows if predicate(f)],key=lambda x:x[1]['title'].casefold())
        lines+=['## '+title+f' ({len(selected)})','']
        for p,f in selected:
            year=f.get('year');status=f.get('verification_status','see paper page')
            lines+=['- ['+label(f['title'])+']('+p.name+')'+(' ('+str(year)+')' if year else '')+' — `'+str(status)+'`']
        lines+=['']
    return '\n'.join(lines)


def validate(repo):
    p=repo/'knowledge_base/wiki/papers/index.md'
    if not p.exists():return {'catalog':'not_configured'}
    pages=[(x,metadata(x)) for x in p.parent.glob('*.md') if x.name!='index.md'];text=p.read_text();errors=[]
    for path,_ in pages:
        if ']('+path.name+')' not in text:errors.append('Unlisted paper: '+path.name)
    for row in retained_reviews(repo)+registry(repo)['sources']:
        matches=[path for path,fields in pages if identity_match(fields,row)]
        if len(matches)!=1:errors.append('Missing or duplicate retained/source page: '+row['title'])
    if text!=render(repo):errors.append('Catalog stale; run wiki_catalog.py')
    if errors:raise ValueError('; '.join(errors))
    return {'paper_pages':len(pages),'retained_decisions':len(retained_reviews(repo)),'database_doi_sources':len(registry(repo)['sources']),'catalog_coverage':'passed'}


def update_home(repo):
    path=repo/'knowledge_base/wiki/index.md'
    if not path.exists():return
    text=path.read_text()
    start='<!-- retained-catalog:start -->';end='<!-- retained-catalog:end -->'
    rows=[(p,metadata(p)) for p in (repo/'knowledge_base/wiki/papers').glob('*.md') if p.name!='index.md']
    extra=[(p,f) for p,f in rows if f.get('manuscript_role') in ('retained_literature','database_source_reference')]
    lines=[start,'','## Additional retained literature and database references','',
           f'[Complete catalog: {len(rows)} paper/source pages](papers/index.md). Newly materialized pages below preserve their review status; source pointers are not full-text syntheses.','']
    for p,f in sorted(extra,key=lambda x:x[1]['title'].casefold()):
        lines.append('- ['+label(f['title'])+'](papers/'+p.name+') — `'+f['verification_status']+'`')
    lines+=['',end]
    block='\n'.join(lines)
    if start in text:
        a=text.index(start);b=text.index(end,a)+len(end);text=text[:a]+block+text[b:]
    else:text+='\n'+block+'\n'
    path.write_text(text)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if not args.check:
        created=materialize_missing(ROOT)
        (ROOT/'knowledge_base/wiki/papers/index.md').write_text(render(ROOT))
        update_home(ROOT)
        print(json.dumps({'created':created}))
    print(json.dumps(validate(ROOT)))

if __name__=='__main__':main()
