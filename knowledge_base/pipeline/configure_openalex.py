#!/usr/bin/env python3
"""Save an OpenAlex key through a hidden local prompt, or check saved access."""
import argparse
import getpass
import sys
import warnings
from urllib.parse import urlencode
from openalex_auth import ENV_FILE, OpenAlexError, read_key, request_json, save_key


def verify(key):
    params={'search':'Malaysia methane','per_page':1,'cursor':'*'}
    first=request_json('https://api.openalex.org/works?'+urlencode(params), key=key)
    cursor=first.get('meta',{}).get('next_cursor')
    if not cursor:
        raise OpenAlexError('Verification query returned no continuation cursor; second-page access is not confirmed.')
    params['cursor']=cursor
    second=request_json('https://api.openalex.org/works?'+urlencode(params), key=key)
    if not isinstance(second.get('results'),list):
        raise OpenAlexError('Second-page verification did not return a work list.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Check saved key without prompting or changing configuration')
    args=parser.parse_args()
    try:
        if args.check:
            key=read_key()
            if not key:raise OpenAlexError('No OpenAlex key is configured yet.')
        else:
            if not sys.stdin.isatty():raise OpenAlexError('Use an interactive laptop terminal for hidden key entry.')
            with warnings.catch_warnings():
                warnings.simplefilter('error',getpass.GetPassWarning)
                key=getpass.getpass('OpenAlex API key (hidden; not printed): ').strip()
            if not key:raise OpenAlexError('No key entered; configuration unchanged.')
        verify(key)
        if not args.check:save_key(key)
        del key
        print('OpenAlex authentication and second-page cursor access verified.')
        if not args.check:print('Key saved privately for the existing monthly service. Timer and schedule unchanged.')
        return 0
    except (OpenAlexError,OSError) as error:
        print(str(error),file=sys.stderr)
        return 1
    except (EOFError,KeyboardInterrupt,getpass.GetPassWarning):
        print('Cancelled or terminal cannot hide key entry; configuration unchanged.',file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
