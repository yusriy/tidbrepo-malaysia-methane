"""Owner-informed triage; source text is data and no route verifies a measurement."""
import re

POLICY_VERSION = 'owner-2026-11-01-v1'


def classify(work, title, abstract, policy):
    """Apply auditable title/type rules before ranking; ambiguous cases stay visible."""
    title_lower = title.lower()
    text = f'{title} {abstract}'.lower()
    for rule in policy.get('rules', []):
        doi = str(work.get('doi') or '').lower().removeprefix('https://doi.org/')
        if ((rule.get('title_pattern') and re.search(rule['title_pattern'], title_lower))
                or work.get('type') in rule.get('work_types', [])
                or any(doi.startswith(prefix) for prefix in rule.get('doi_prefixes', []))):
            if rule['id'] == 'dna_only' and re.search(r'\bflux(?:es)?\b|emission factor', text):
                continue
            # B0 is an inventory input even when measured in laboratory BMP assays.
            if rule['id'] == 'reactor_optimization' and re.search(r'\bb[₀0]\b|maximum methane (?:capacity|potential)', text):
                continue
            return {'policy_version': POLICY_VERSION, 'route': rule['route'],
                    'reason': rule['id'], 'scientifically_verified': False}
    if re.search(r'\bb[₀0]\b|maximum methane (?:capacity|potential)', text):
        route, reason = 'factor_assessment', 'inventory_parameter_b0'
    elif re.search(r'emission factor|\bflux(?:es)?\b|eddy covariance|\bchamber\b', text):
        route, reason = 'factor_assessment', 'potential_inventory_factor_or_flux'
    else:
        route, reason = 'manual_scope_review', 'insufficient_inventory_evidence'
    return {'policy_version': POLICY_VERSION, 'route': route, 'reason': reason,
            'scientifically_verified': False}
