"""Cross-repository release-lock check, identical in both SkyRelief repositories.
SPDX-License-Identifier: LicenseRef-Pending-Approval

1. Validates PUBLICATION_RELEASE_LOCK.json against the facts in this repository
   (counts, ERC results, cost baskets, supplement names, licence state).
2. With --other PATH (the sibling repository checkout), fails unless both lock
   files and all shared ledgers are byte-identical.
3. --self-test runs negative tests: deliberately corrupted locks must fail.
Standard library only.
"""
import argparse, copy, csv, hashlib, json, sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = ['PUBLICATION_RELEASE_LOCK.json', 'PUBLICATION_GATE.md', 'AUTHORS_LICENSING_APPROVAL_REQUIRED.md',
          'scripts/check_release_lock.py', 'scripts/release_gate.py',
          'bom/complete_platform_parts_crosswalk.csv', 'bom/supplier_cost_provenance.csv',
          'data/evidence_ledger.csv', 'data/documented_connections.csv', 'data/source_manifest.csv',
          'data/withheld_asset_manifest.csv', 'data/archived_thrust_sheet_transcription.csv', 'data/issue_matrix.csv']


def rows(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def facts(root):
    """Facts derived from repository files, independent of the lock."""
    f = {'bom_crosswalk_entries': len(rows(root / 'bom/complete_platform_parts_crosswalk.csv')),
         'supplier_quotes': len(rows(root / 'bom/supplier_cost_provenance.csv')),
         'documented_interfaces': len(rows(root / 'data/documented_connections.csv')),
         'historical_step_files_withheld': len(rows(root / 'data/withheld_asset_manifest.csv'))}
    q = {r['cost_id']: Decimal(r['extended_price']) for r in rows(root / 'bom/supplier_cost_provenance.csv')}
    f['named_family_partial_INR'] = sum(q[f'P{i:02}'] for i in range(1, 6))
    f['category_proposed_partial_INR'] = sum(q[f'P{i:02}'] for i in range(6, 12))
    f['scout_named_partial_USD'] = q['P12'] + q['P13']
    exp = root / 'cad/independently_authored/exports'
    if exp.is_dir():
        f['r01_step_exports'] = len(list(exp.glob('R01_*.step')))
    erc = {}
    for name in ('delivery_historical_power', 'delivery_reference', 'scout_reference'):
        p = root / f'verification/{name}_erc.json'
        if p.exists():
            d = json.loads(p.read_text())
            erc[name] = [v for s in d['sheets'] for v in s['violations']]
    if erc:
        f['kicad_projects'] = len(list((root / 'kicad').glob('*.kicad_pro')))
        f['erc'] = erc
    return f


def validate(lock, fx):
    errs = []
    req = ['project', 'manuscript_id', 'manuscript_version', 'source_upstream_commit', 'mechanical_repo', 'electronics_repo',
           'supplements', 'rights_status', 'counts', 'erc', 'physical_new_tests', 'review_status', 'last_verification_date']
    errs += [f'missing key {k}' for k in req if k not in lock]
    if errs:
        return errs
    if lock['project'] != 'SkyRelief':
        errs.append('project name')
    if lock['supplements'] != {'S1': 'SkyRelief_Mechanical_Source_Release.zip', 'S2': 'SkyRelief_Electronics_Source_Release.zip',
                               'S3': 'SkyRelief_Reproducible_Computations.zip'}:
        errs.append('supplement S1/S2/S3 mapping')
    if lock['review_status'] not in ('GO', 'CONDITIONAL_GO', 'NO_GO'):
        errs.append('review_status vocabulary')
    if lock['physical_new_tests'] is not False:
        errs.append('physical_new_tests must be false: no new physical tests were performed')
    pending = lock['rights_status'].get('overall') != 'APPROVED'
    if pending and lock['review_status'] == 'GO':
        errs.append('GO is impossible while licensing is pending')
    if pending and (lock.get('mechanical_tag') or lock.get('electronics_tag')):
        if any(str(t).startswith('v1') for t in (lock.get('mechanical_tag'), lock.get('electronics_tag')) if t):
            errs.append('v1.x tag while licensing is pending')
    if lock.get('computational_zip_sha256') is None and 'NOT VERIFIED' not in lock.get('computational_zip_status', ''):
        errs.append('computational supplement must be marked NOT VERIFIED when no hash is recorded')
    c = lock['counts']
    for k in ('bom_crosswalk_entries', 'supplier_quotes', 'documented_interfaces', 'historical_step_files_withheld', 'r01_step_exports', 'kicad_projects'):
        if k in fx and c.get(k) != fx[k]:
            errs.append(f'count {k}: lock {c.get(k)} vs repository {fx[k]}')
    cb = lock['cost_baskets']
    for k in ('named_family_partial_INR', 'category_proposed_partial_INR', 'scout_named_partial_USD'):
        if Decimal(str(cb[k])) != fx[k]:
            errs.append(f'cost basket {k}: lock {cb[k]} vs quotes {fx[k]}')
    if cb.get('complete_total') is not None or cb.get('currency_conversion') is not None:
        errs.append('no complete total or currency conversion is supported')
    if lock['historical_outcomes'].get('separate_release_reliability') is not None:
        errs.append('no separate release-reliability figure is supported')
    if (lock['historical_outcomes']['composite_runs_passed'], lock['historical_outcomes']['composite_runs_total']) != (19, 20):
        errs.append('composite outcome must be 19/20')
    if 'erc' in fx:
        for name, viol in fx['erc'].items():
            if lock['erc'][name]['violations'] != len(viol):
                errs.append(f'ERC {name}: lock {lock["erc"][name]["violations"]} vs report {len(viol)}')
        scout = fx['erc']['scout_reference']
        if c['scout_unresolved_erc_pins'] != sum(v['type'] == 'pin_not_connected' for v in scout):
            errs.append('scout unresolved pin count')
    return errs


def self_test(lock, fx):
    cases = {
        'S2 pointing at computation': lambda L: L['supplements'].__setitem__('S2', 'SkyRelief_Reproducible_Computations.zip'),
        'scout ERC silenced': lambda L: L['erc']['scout_reference'].__setitem__('violations', 0),
        'GO with pending licences': lambda L: L.__setitem__('review_status', 'GO'),
        'invented complete total': lambda L: L['cost_baskets'].__setitem__('complete_total', 30000),
        'unsupported 97% release figure': lambda L: L['historical_outcomes'].__setitem__('separate_release_reliability', 0.97),
        'claimed new physical tests': lambda L: L.__setitem__('physical_new_tests', True),
        'wrong BOM count': lambda L: L['counts'].__setitem__('bom_crosswalk_entries', 33),
    }
    results = {}
    for name, mutate in cases.items():
        L = copy.deepcopy(lock); mutate(L)
        if name == 'scout ERC silenced' and 'erc' not in fx:
            results[name] = 'skipped (no ERC reports in this repository)'; continue
        results[name] = 'rejected' if validate(L, fx) else 'NOT REJECTED'
    return results


def main():
    a = argparse.ArgumentParser(); a.add_argument('--other'); a.add_argument('--self-test', action='store_true'); args = a.parse_args()
    lock = json.loads((ROOT / 'PUBLICATION_RELEASE_LOCK.json').read_text())
    fx = facts(ROOT)
    errs = validate(lock, fx)
    out = {'repository': ROOT.name, 'lock_errors': errs}
    if args.other:
        other = Path(args.other).resolve(); diff = []
        for rel in SHARED:
            pa, pb = ROOT / rel, other / rel
            if not (pa.is_file() and pb.is_file()):
                diff.append(f'{rel}: missing in one repository')
            elif hashlib.sha256(pa.read_bytes()).digest() != hashlib.sha256(pb.read_bytes()).digest():
                diff.append(f'{rel}: differs')
        out['shared_files_checked'] = len(SHARED); out['shared_file_mismatches'] = diff; errs = errs + diff
    if args.self_test:
        st = self_test(lock, fx); out['negative_tests'] = st
        errs = errs + [f'negative test not rejected: {k}' for k, v in st.items() if v == 'NOT REJECTED']
    out['status'] = 'PASS' if not errs else 'FAIL'
    print(json.dumps(out, indent=2, default=str))
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
