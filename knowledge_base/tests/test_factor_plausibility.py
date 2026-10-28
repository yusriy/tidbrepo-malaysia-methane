import importlib.util
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "pipeline"))
import unittest

spec = importlib.util.spec_from_file_location('factor_plausibility', Path(__file__).parents[1] / 'pipeline/factor_plausibility.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class FactorAuditTests(unittest.TestCase):
    def row(self, **values):
        return dict(id=1, category='Peat lands', condition='Forest', countries='Malaysia', unit='kg CH₄ ha⁻¹ day⁻¹', **values)

    def test_annual_conversion_preserves_original(self):
        row = self.row(mean='365', stdev='36.5')
        row['unit'] = 'kg CH₄ ha⁻¹ yr⁻¹'
        r = m.prepare(row)
        self.assertEqual(r['values']['mean'], 1)
        self.assertEqual(r['reported_values']['mean'], '365')
        self.assertAlmostEqual(r['values']['stdev'], .1)

    def test_signed_flux_and_endpoint_semantics(self):
        r = m.prepare(self.row(min='-2', max='3'))
        self.assertEqual(r['values']['min'], -2)
        self.assertIsNone(r['values']['mean'])
        self.assertEqual(r['issues'], [])

    def test_consistency_flags(self):
        r = m.prepare(self.row(min='4', max='2', mean='9', stdev='-1'))
        self.assertEqual(len(r['issues']), 3)
        self.assertTrue(m.prepare(self.row(mean='NaN'))['issues'])

    def test_incompatible_bases_remain_separate(self):
        a = self.row(mean='1')
        b = dict(a, id=2, unit='kg CH₄ m⁻³ natural gas sales volume')
        result = m.audit([a, b])
        self.assertEqual(result['group_count'], 2)
        self.assertFalse(result['peer_signals'])

    def test_source_dependence_does_not_create_peers(self):
        rows = [dict(self.row(mean=str(10**i)), id=i, doi_1='10.1234/shared') for i in range(8)]
        result = m.audit(rows)
        self.assertFalse(result['peer_signals'])
        self.assertEqual(len(result['unassessed']), 8)

    def test_positive_peer_signal_and_wrong_condition_exclusion(self):
        rows = [dict(self.row(mean=str(10 + i*.1)), id=i, doi_1=f'10.1234/{i}') for i in range(7)]
        rows.append(dict(self.row(mean='10000'), id=99, doi_1='10.1234/extreme'))
        result = m.audit(rows)
        self.assertTrue(any(s['id'] == 99 for s in result['peer_signals']))
        rows[-1]['condition'] = 'Different boundary'
        self.assertFalse(any(s['id'] == 99 for s in m.audit(rows)['peer_signals']))

    def test_duplicate_records_rejected(self):
        with self.assertRaises(ValueError):
            m.audit([self.row(), self.row()])

if __name__ == '__main__':
    unittest.main()

class PaginationTests(unittest.TestCase):
    def test_reads_until_empty_terminal_page(self):
        import io
        import json
        from unittest.mock import patch
        with patch.object(m, 'urlopen', side_effect=[io.StringIO(json.dumps([{'id': 1}])), io.StringIO('[]')]) as request:
            self.assertEqual(m.fetch_rows(), [{'id': 1}])
            self.assertIn('page=1&size=1000', request.call_args.args[0].full_url)

    def test_repeated_page_aborts(self):
        import io
        from unittest.mock import patch
        with patch.object(m, 'urlopen', side_effect=[io.StringIO('[{"id":1}]'), io.StringIO('[{"id":1}]')]):
            with self.assertRaises(ValueError):
                m.fetch_rows()
