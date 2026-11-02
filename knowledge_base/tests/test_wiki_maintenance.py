import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'pipeline'))
import wiki_maintenance as maintenance


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.repo = Path(self.tmp.name)
        self.wiki = self.repo / 'knowledge_base/wiki'
        for folder in ('papers', 'topics', 'methods', 'locations'):
            (self.wiki / folder).mkdir(parents=True)
        self.paper = self.wiki / 'papers/paper.md'
        self.paper.write_text('---\ntitle: "Methane study"\ndoi: "10.1234/Example"\nyear: 2024\nverification_status: "machine_extracted"\n---\n# Methane study\n\nHuman scientific interpretation.\n')
        self.topic = self.wiki / 'topics/methane.md'; self.topic.write_text('# Methane\n\nHuman topic synthesis.\n')
        (self.wiki / 'index.md').write_text('# Wiki\n\n[Paper](papers/paper.md)\n[Topics](topics/index.md)\n[Methods](methods/index.md)\n[Locations](locations/index.md)\n[Report](lint-report.md)\n')
        self.registry = self.repo / maintenance.NAVIGATION; self.registry.parent.mkdir(parents=True)
        self.row = {'paper':'paper.md', 'topics':['methane'], 'methods':[], 'locations':[], 'basis':'Source note, methods section'}
        self.registry.write_text(json.dumps({'papers':[self.row]}))
    def tearDown(self):
        self.tmp.cleanup()
    def build(self):
        return maintenance.run(self.repo, checked_date='2026-11-02')
    def test_repeatable_blocks_preserve_human_text_and_scientific_flags(self):
        self.build(); before = {p:p.read_bytes() for p in self.wiki.rglob('*.md')}
        self.build()
        self.assertEqual(before, {p:p.read_bytes() for p in self.wiki.rglob('*.md')})
        self.assertIn('Human scientific interpretation.', self.paper.read_text())
        self.assertIn('verification_status: "machine_extracted"', self.paper.read_text())
        self.assertIn('Human topic synthesis.', self.topic.read_text())
        self.assertEqual(self.paper.read_text().count(maintenance.START), 1)
        self.assertEqual(maintenance.run(self.repo, check=True)['navigation_coverage']['topics'], 1)
    def test_counts_deduplicate_existing_and_curated_links(self):
        self.topic.write_text(self.topic.read_text() + '\n- [[papers/paper|Existing source]]\n')
        self.build()
        self.assertNotIn('](../papers/paper.md)', self.topic.read_text())
        self.assertIn('1 linked paper pages', (self.wiki/'topics/index.md').read_text())
    def test_broken_markdown_and_obsidian_links_are_both_reported(self):
        self.build(); self.paper.write_text(self.paper.read_text() + '\n[Missing](missing.md)\n[[missing-wikilink]]\n')
        result = maintenance.audit(self.repo)
        self.assertEqual(len(result['broken_links']), 2)
        with self.assertRaisesRegex(ValueError, 'Stale wiki lint report'): maintenance.run(self.repo, check=True)
    def test_duplicate_doi_identity_and_orphan_are_detected(self):
        self.build()
        p = self.wiki/'papers/duplicate.md'
        p.write_text('---\ntitle: "Different title"\ndoi: "https://doi.org/10.1234/example"\n---\n# Other\n')
        result = maintenance.audit(self.repo)
        self.assertEqual(len(result['duplicate_identities']), 1)
        self.assertIn('papers/duplicate.md', result['orphan_pages'])
    def test_missing_metadata_remains_a_gap_not_an_invented_identifier(self):
        self.paper.write_text(self.paper.read_text().replace('doi: "10.1234/Example"','doi: ""'))
        result = self.build()
        self.assertEqual(result['missing_metadata'], [{'paper':'paper.md', 'field':'doi'}])
        self.assertIn('doi: ""', self.paper.read_text())
    def test_unknown_navigation_target_is_rejected_without_edits(self):
        before = self.paper.read_bytes()
        self.registry.write_text(json.dumps({'papers':[{**self.row,'methods':['imagined-method']}]}))
        with self.assertRaisesRegex(ValueError, 'Missing navigation destination'): self.build()
        self.assertEqual(self.paper.read_bytes(), before)
    def test_stale_navigation_check_does_not_rewrite_notes(self):
        self.build(); text = self.topic.read_text().replace('Editorial navigation', 'Changed editorial navigation')
        self.topic.write_text(text)
        with self.assertRaisesRegex(ValueError, 'Stale navigation'): maintenance.run(self.repo, check=True)
        self.assertEqual(self.topic.read_text(), text)


if __name__ == '__main__': unittest.main()
