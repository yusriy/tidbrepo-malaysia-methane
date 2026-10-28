"""Canonical DOI identity for matching/storage, separate from resolver URLs."""
import re
from urllib.parse import unquote


def normalize_doi(value):
    doi = str(value or '').strip()
    doi = re.sub(r'^doi\s*:\s*', '', doi, flags=re.I)
    if re.match(r'^https?://(?:dx\.)?doi\.org/', doi, re.I):
        doi = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', doi, flags=re.I)
        doi = unquote(doi)
    return doi.strip().lower()


def validated_doi(value):
    doi = normalize_doi(value)
    if not re.fullmatch(r'10\.\d{4,9}/[^\s?#]+', doi):
        raise ValueError('Invalid DOI identity; expected 10.<registrant>/<suffix>')
    return doi


def doi_url(value):
    return 'https://doi.org/' + validated_doi(value)
