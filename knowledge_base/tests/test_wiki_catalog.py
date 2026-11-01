import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pipeline'))
import wiki_catalog as catalog

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.repo=Path(self.tmp.name)
        self.wiki=self.repo/'knowledge_base/wiki';(self.wiki/'papers').mkdir(parents=True)
        (self.wiki/'index.md').write_text('# Wiki\n')
        (self.repo/'knowledge_base/literature_updates/reviews').mkdir(parents=True)
    def tearDown(self):self.tmp.cleanup()
    def review(self,name,decision='context_only',title='Retained methane paper'):
        path=self.repo/'knowledge_base/literature_updates/reviews'/name
        path.write_text(json.dumps({'candidate_id':'candidate_a','title':title,'doi':'10.1234/example','decision':decision,'wiki_review_page':'findings/review','source_url':'https://doi.org/10.1234/example'}))
    def build(self):
        created=catalog.materialize_missing(self.repo)
        (self.wiki/'papers/index.md').write_text(catalog.render(self.repo))
        catalog.update_home(self.repo)
        return created
    def test_retained_context_is_listed_without_measurement_promotion(self):
        self.review('2026-11-01.json');created=self.build()
        self.assertEqual(len(created),1)
        note=(self.repo/created[0]).read_text()
        self.assertIn('retained_context_only',note);self.assertNotIn('measurements_verified: true',note)
        self.assertEqual(catalog.validate(self.repo)['paper_pages'],1)
        self.assertIn('Retained methane paper',(self.wiki/'index.md').read_text())
    def test_latest_exclusion_prevents_materializing_earlier_retain(self):
        self.review('2026-11-01.json');self.review('2026-11-02.json','exclude')
        self.assertEqual(self.build(),[])
    def test_existing_human_notes_are_never_overwritten_and_reruns_stable(self):
        self.review('2026-11-01.json');created=self.build();p=self.repo/created[0]
        p.write_text(p.read_text()+'\nHuman interpretation preserved.\n');before=p.read_bytes()
        self.assertEqual(self.build(),[]);self.assertEqual(p.read_bytes(),before)
        a=(self.wiki/'index.md').read_text();self.build();self.assertEqual((self.wiki/'index.md').read_text(),a)
    def test_all_existing_pages_listed_even_without_new_review_record(self):
        p=self.wiki/'papers/original.md';p.write_text('---\ntitle: "Original"\nmanuscript_role: "supporting_corpus"\n---\n# Original\n')
        self.build();t=(self.wiki/'papers/index.md').read_text();self.assertIn('Original supporting corpus (1)',t);self.assertIn('[Original](original.md)',t)
    def test_registry_pointer_matches_existing_doi_without_duplicate_note(self):
        self.review('2026-11-01.json')
        p=self.repo/catalog.REGISTRY;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps({'sources':[{'title':'Alternate spelling','doi':'10.1234/example','tidbrepo_row_ids':[1],'metadata_source':'frozen bibliographic record'}]}))
        self.assertEqual(len(self.build()),1);self.assertEqual(catalog.validate(self.repo)['database_doi_sources'],1)
    def test_missing_retained_page_and_stale_catalog_are_rejected(self):
        self.review('2026-11-01.json');created=self.build();(self.repo/created[0]).unlink()
        with self.assertRaisesRegex(ValueError,'Missing or duplicate'):catalog.validate(self.repo)
        self.build();(self.wiki/'papers/unlisted.md').write_text('# Unlisted\n')
        with self.assertRaisesRegex(ValueError,'Unlisted paper'):catalog.validate(self.repo)
    def test_conflicting_nonempty_dois_do_not_collapse_by_title(self):
        a={'title':'Same title','doi':'10.1234/a'};b={'title':'Same title','doi':'10.1234/b'}
        self.assertFalse(catalog.identity_match(a,b))
    def test_source_metadata_cannot_inject_wikilinks_into_catalog(self):
        self.review('2026-11-01.json',title='Methane ]][[injected|go]] <script>')
        self.build();text=(self.wiki/'papers/index.md').read_text()
        self.assertNotIn('[[injected',text);self.assertNotIn('<script>',text)
