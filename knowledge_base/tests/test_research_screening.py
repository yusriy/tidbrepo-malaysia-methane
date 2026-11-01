import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

KB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KB / 'pipeline'))
import research_screening as triage
import tidbrepo_literature_update as workflow
CONFIG = json.loads((KB / 'config/tidbrepo_literature_update.json').read_text())

class OwnerScopeTests(unittest.TestCase):
    def route(self, title, abstract='', kind='article'):
        return triage.classify({'type': kind}, title, abstract, CONFIG['screening_policy'])['route']

    def test_field_factors_survive_and_models_go_to_context(self):
        self.assertEqual(self.route('Methane emission factors from coal combustion in Malaysia'), 'factor_assessment')
        self.assertEqual(self.route('Rice emission factors compared with EDGAR'), 'wiki_context')
        self.assertEqual(self.route('Methane cost analysis in Malaysia'), 'wiki_context')

    def test_b0_inventory_input_survives_lab_assay_language(self):
        self.assertEqual(self.route('Biochemical methane potential in Malaysian broiler manure',
                                   'Laboratory assays measured B0 for comparison with IPCC defaults.'), 'factor_assessment')

    def test_comments_reviews_dna_and_reactor_optimization_filtered(self):
        for title in ['Comment on essd-2024-90', 'A mini review of methane composting',
                      'Long Read Sequencing Identifies Putative Methanogens',
                      'Anaerobic Co-Digestion of Bread Waste for Methane Production',
                      'Carbon Nanotube Growth in Methane Combustion']:
            with self.subTest(title=title):
                self.assertEqual(self.route(title), 'filtered_out')
        self.assertEqual(self.route('Methane in Malaysia', kind='review'), 'filtered_out')

    def test_dna_with_actual_flux_evidence_is_not_discarded(self):
        self.assertEqual(self.route('Sequencing and methane flux in Malaysian wetlands'), 'factor_assessment')

    def test_ambiguous_material_remains_visible(self):
        self.assertEqual(self.route('Methane in Malaysia'), 'manual_scope_review')

    def test_egu_abstract_identity_filtered_without_banning_proceedings(self):
        result = triage.classify({'doi': 'https://doi.org/10.5194/egusphere-egu25-19060'},
                                'GHG emissions from peatland ditches', '', CONFIG['screening_policy'])
        self.assertEqual(result['route'], 'filtered_out')
        self.assertEqual(self.route('Methane flux in Malaysia', kind='proceedings-article'), 'factor_assessment')

    def test_discovery_archives_filtered_work_and_retains_field_work(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); config = dict(CONFIG, seed_candidates=[], openalex_max_pages_per_query=1, queries=['Malaysia methane'])
            path = root/'config.json'; path.write_text(json.dumps(config))
            args = SimpleNamespace(config=path, run_id='scope-test', runs_dir=root/'runs', db=root/'missing.sqlite',
                                   snapshot=root/'missing.json', mailto=None, include_known=False)
            works = [{'id': 'https://openalex.org/W1', 'title': 'A review of methane flux in Malaysia', 'publication_year': 2026, 'type': 'review'},
                     {'id': 'https://openalex.org/W2', 'title': 'Methane flux in Malaysian rice fields', 'publication_year': 2026, 'type': 'article'}]
            with patch.object(workflow, 'request_json', return_value={'results': works, 'meta': {}}):
                workflow.command_discover(args)
            run = args.runs_dir/args.run_id
            self.assertEqual(len(workflow.read_jsonl(run/'candidates.jsonl')), 1)
            self.assertEqual(len(workflow.read_jsonl(run/'screened_out.jsonl')), 1)
            self.assertEqual(workflow.load_json(run/'manifest.json')['works_deduplicated'], 2)

    def test_scope_gate_blocks_automatic_download_but_owner_can_override(self):
        with tempfile.TemporaryDirectory() as d:
            run = Path(d)
            workflow.write_jsonl(run/'candidates.jsonl', [{'candidate_id': 'c1', 'title':'Context model',
                'screening_score':14, 'screening_flags':['malaysia_context'], 'open_access_pdf_url':'https://example.invalid/a.pdf',
                'screening_triage':{'route':'wiki_context'}}])
            args = SimpleNamespace(run_dir=run, screening_decisions=None, minimum_score=8, include_known=False)
            with patch.object(workflow, 'download_pdf') as download:
                workflow.command_extract(args)
                download.assert_not_called()
            self.assertEqual(workflow.candidate_retrieval_status(0, 'owner_scope_requires_paper_screening'),
                             'not_attempted_pending_screening')
            gate=run/'gate.json'; workflow.write_json(gate, {'decisions':[{'candidate_id':'c1','decision':'retrieve_extract'}]})
            args.screening_decisions=gate
            with patch.object(workflow, 'download_pdf', side_effect=ValueError('test source unavailable')) as download:
                workflow.command_extract(args)
                download.assert_called_once()

    def test_affiliation_alone_does_not_trigger_automatic_extraction(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)
            workflow.write_jsonl(run/'candidates.jsonl', [{'candidate_id':'c1','screening_score':14,
                'screening_flags':['malaysian_author_affiliation'], 'screening_triage':{'route':'factor_assessment'},
                'open_access_pdf_url':'https://example.invalid/a.pdf'}])
            with patch.object(workflow,'download_pdf') as download:
                workflow.command_extract(SimpleNamespace(run_dir=run,screening_decisions=None,minimum_score=8,include_known=False))
                download.assert_not_called()
