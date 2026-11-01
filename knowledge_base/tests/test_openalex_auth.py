import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch,MagicMock
from urllib.error import HTTPError
sys.path.insert(0,str(Path(__file__).parents[1]/'pipeline'))
import openalex_auth as auth
import configure_openalex as setup

class OpenAlexAuthTests(unittest.TestCase):
    def test_configuration_preserves_settings_and_is_private(self):
        with tempfile.TemporaryDirectory() as temp,patch.dict(os.environ,{},clear=True):
            p=Path(temp)/'settings.env';p.write_text('TIDBREPO_GIT_SYNC=1\nTIDBREPO_CONTACT_EMAIL=test@example.org\n')
            auth.save_key('test-private-key',p)
            self.assertEqual(auth.read_key(p),'test-private-key')
            self.assertIn('TIDBREPO_GIT_SYNC=1',p.read_text())
            self.assertEqual(p.stat().st_mode&0o777,0o600)
            auth.save_key('replacement',p)
            self.assertEqual(p.read_text().count('OPENALEX_API_KEY='),1)

    def test_header_only_auth_and_fixed_host(self):
        opener=MagicMock();opener.open.return_value.__enter__.return_value=io.StringIO('{"results":[]}')
        with patch.object(auth,'build_opener',return_value=opener):
            auth.request_json('https://api.openalex.org/works?cursor=abc',key='private')
            request=opener.open.call_args.args[0]
            self.assertEqual(request.get_header('Authorization'),'Bearer private')
            self.assertNotIn('private',request.full_url)
        for url in ('http://api.openalex.org/works','https://other.example/works','https://api.openalex.org/works?api_key=secret'):
            with self.assertRaises(auth.OpenAlexError):auth.request_json(url,key='private')

    def test_errors_redact_server_body_and_credentials(self):
        opener=MagicMock();opener.open.side_effect=HTTPError('https://api.openalex.org/works',401,'private-secret',{},None)
        with patch.object(auth,'build_opener',return_value=opener):
            with self.assertRaises(auth.OpenAlexError) as error:auth.request_json('https://api.openalex.org/works',key='private-secret')
            self.assertNotIn('private-secret',str(error.exception));self.assertIn('401',str(error.exception))

    def test_redirect_does_not_forward_token(self):
        self.assertIsNone(auth.NoRedirect().redirect_request(None,None,302,'',{},'https://other.example/'))

    def test_setup_verifies_continuation_page(self):
        with patch.object(setup,'request_json',side_effect=[{'meta':{'next_cursor':'opaque'}},{'results':[]}]) as request:
            setup.verify('private')
            self.assertIn('cursor=opaque',request.call_args.args[0])
            self.assertEqual(request.call_args.kwargs['key'],'private')

    def test_discovery_fails_before_network_without_required_key(self):
        from types import SimpleNamespace
        import tidbrepo_literature_update as workflow
        with patch.object(workflow,'load_json',return_value={'openalex_max_pages_per_query':2}),patch.object(workflow,'read_key',return_value=''),patch.object(workflow,'request_json') as request:
            with self.assertRaises(auth.OpenAlexError):workflow.command_discover(SimpleNamespace(config=Path('/unused')))
            request.assert_not_called()
