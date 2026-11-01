"""OpenAlex credentials stay in local configuration and HTTPS headers only."""
import os
from pathlib import Path
import re
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener

ENV_FILE = Path.home() / '.config/tidbrepo-monthly.env'


class OpenAlexError(RuntimeError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def read_key(path=None):
    if 'OPENALEX_API_KEY' in os.environ:
        return os.environ['OPENALEX_API_KEY'].strip()
    path = ENV_FILE if path is None else Path(path)
    if not path.is_file():
        return ''
    matches = []
    for line in path.read_text().splitlines():
        match = re.match(r'^\s*OPENALEX_API_KEY\s*=\s*(.*?)\s*$', line)
        if match:
            matches.append(match[1].strip('"\''))
    if len(matches) > 1:
        raise OpenAlexError('Duplicate OPENALEX_API_KEY entries; repair the local environment file.')
    return matches[0] if matches else ''


def save_key(key, path=None):
    if not key or not re.fullmatch(r'[A-Za-z0-9._-]+', key):
        raise OpenAlexError('Key contains unsupported characters; paste only the OpenAlex API key.')
    path = ENV_FILE if path is None else Path(path)
    if path.is_symlink():
        raise OpenAlexError('Refusing to replace a symlinked environment file.')
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text() if path.exists() else ''
    lines = [line for line in existing.splitlines() if not re.match(r'^\s*OPENALEX_API_KEY\s*=', line)]
    lines.append('OPENALEX_API_KEY=' + key)
    fd, temporary = tempfile.mkstemp(prefix='.tidbrepo-env-', dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, 'w') as stream:
            stream.write('\n'.join(lines) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def request_json(url, mailto=None, key=None):
    import json
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.netloc != 'api.openalex.org' or 'api_key' in parsed.query.lower():
        raise OpenAlexError('OpenAlex requests must use the fixed HTTPS host and header-only authentication.')
    token = read_key() if key is None else key
    headers = {'Accept': 'application/json', 'User-Agent': 'TIDBRepo-Malaysia-Methane-Literature-Update/1.1'}
    if mailto:
        headers['User-Agent'] += f' (mailto:{mailto})'
    if token:
        headers['Authorization'] = 'Bearer ' + token
    try:
        request = Request(url, headers=headers)
        with build_opener(NoRedirect()).open(request, timeout=90) as response:
            return json.load(response)
    except HTTPError as error:
        # No server response bodies, request URLs or credential values in logs.
        hint = ' Check that the saved key is correct and activated.' if error.code in (401,403) else ''
        raise OpenAlexError(f'OpenAlex returned HTTP {error.code}.{hint}') from None
    except (URLError, TimeoutError, ValueError):
        raise OpenAlexError('OpenAlex request failed or returned unreadable JSON; no credentials were logged.') from None
