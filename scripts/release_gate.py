"""Fail-closed public-release gate, shared by both SkyRelief repositories.
SPDX-FileCopyrightText: 2026 Aarav Jalan and Abhinav Patro
SPDX-License-Identifier: MIT

Rejects the release if the working tree OR any blob in Git history matches a
withheld historical STEP hash, or if prohibited material is present (STEP/mesh
outside the R01 export folder, the MDPI template, nested archives, OS temp
files, credentials). Assigns each file its approved licence by the explicit
rules below, writes LICENSE_MATRIX.csv and REUSE.toml (--write-matrix), and
checks that: every file is covered; canonical licence texts are present and
unmodified; script SPDX headers agree with the matrix; no licence is applied
while PUBLICATION_RELEASE_LOCK.json says approval is missing.
Standard library only; git optional (history check reported as skipped).

  python scripts/release_gate.py                 # check
  python scripts/release_gate.py --write-matrix  # regenerate LICENSE_MATRIX.csv and REUSE.toml, then check
"""
import argparse, csv, fnmatch, hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', '__pycache__', '.venv'}
ALLOWED_STEP_DIR = 'cad/independently_authored/exports/'
FORBIDDEN_GLOBS = ['*.dot', '*.dotx', '*hardware-template*', '*.zip', '*.7z', '*.rar', '.DS_Store', 'Thumbs.db',
                   '*.tmp', '*.bak', '*.kicad_prl', '*.lck', '*.env', '*.pem', '*.key']
SECRET_RE = re.compile(rb'github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----')

# Canonical texts from SPDX license-list-data 3.29.0 (text/<id>.txt), stored unmodified in LICENSES/.
LICENSE_TEXT_SHA256 = {
    'CERN-OHL-W-2.0': 'c1432111d0aeefc9d1ced8105d2d4ed07d5dcb1fd43abb5d4616c4f9ef96e08f',
    'MIT': 'b05785f9f18e6716bab63424b11454513b9943a222595b70411009202fc592b5',
    'CC-BY-4.0': 'd557539df68e771cc1eedcc91d13f70fca930e508d11eedcafa4b15db49e3744',
}
APPROVAL = {'date': '2026-10-21', 'owners': 'Aarav Jalan; Abhinav Patro (both)',
            'record': 'AUTHOR_LICENSING_DECISIONS.md'}
NEW = '2026 Aarav Jalan and Abhinav Patro'
HIST = '2024-2025 Aarav Jalan and Abhinav Patro'
# (glob, licence, copyright, class) -- first match wins. Ordered from specific to general.
RULES = [
    ('LICENSES/*', None, None, 'Licence text (not relicensed)'),
    ('evidence/original/*.py', 'MIT', '2024-2025 Abhinav Patro', 'Historical original script (author-owned)'),
    ('evidence/original/*', 'CC-BY-4.0', HIST, 'Historical original document/data (author-owned)'),
    ('images/*', 'CC-BY-4.0', HIST, 'Historical original photograph (author-owned)'),
    ('assets/original_wiring_reference/*', 'CC-BY-4.0', '2024-2025 Abhinav Patro', 'Historical original sketch (author-owned)'),
    ('cad/independently_authored/*.py', 'MIT', NEW, 'New CAD generation code (R01)'),
    ('cad/*', 'CERN-OHL-W-2.0', NEW, 'New hardware design source/documentation (R01)'),
    ('drawings/R01_*', 'CERN-OHL-W-2.0', NEW, 'New hardware design drawing (R01)'),
    ('docs/R01_*', 'CERN-OHL-W-2.0', NEW, 'New hardware design documentation (R01)'),
    ('bom/reference_R01_bom.csv', 'CERN-OHL-W-2.0', NEW, 'New hardware design BOM (R01)'),
    ('kicad/*', 'CERN-OHL-W-2.0', NEW, 'New electronic design source/export (KiCad)'),
    ('scripts/*', 'MIT', NEW, 'New script'),
    ('.github/*', 'MIT', NEW, 'New CI configuration'),
    ('requirements*.txt', 'MIT', NEW, 'Build configuration'),
    ('.gitignore', 'MIT', NEW, 'Build configuration'),
    ('.gitattributes', 'MIT', NEW, 'Build configuration'),
    ('REUSE.toml', 'CC-BY-4.0', NEW, 'Licence metadata'),
    ('*', 'CC-BY-4.0', NEW, 'New documentation/data/illustration'),
]
FIELDS = ['relative_path', 'hash', 'original_creator', 'authorship_evidence', 'created_when', 'third_party_dependencies',
          'publication_permission', 'redistribution_permission', 'modification_permission', 'chosen_license',
          'approving_owner', 'date_signed', 'release_status', 'justification']
STALE = 'LicenseRef-' + 'Pending-Approval'  # split so this file does not match itself
GENERATED_LAST = {'verification/file_manifest.csv', 'verification/repository_checks.json'}


def files():
    return [p for p in sorted(ROOT.rglob('*')) if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS)]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def classify(rel):
    for pat, lic, cr, kind in RULES:
        if fnmatch.fnmatch(rel, pat):
            return lic, cr, kind


def approved():
    lock = ROOT / 'PUBLICATION_RELEASE_LOCK.json'
    return lock.exists() and json.loads(lock.read_text())['rights_status']['overall'] == 'APPROVED'


def matrix_rows(fs, ok):
    rows = []
    for p in fs:
        rel = p.relative_to(ROOT).as_posix()
        lic, cr, kind = classify(rel)
        if rel == 'LICENSE_MATRIX.csv' or lic is None:
            continue
        hist = kind.startswith('Historical')
        rows.append({
            'relative_path': rel,
            'hash': 'generated after this matrix; see verification/file_manifest.csv' if rel in GENERATED_LAST else 'sha256:' + sha(p),
            'original_creator': cr,
            'authorship_evidence': 'Upstream project archive (49-file source manifest) and author clarification 2026-10-19' if hist
            else 'Created in this repository with AI assistance; authorship accepted by both authors (see CHANGELOG.md)',
            'created_when': '2024-2025 (project period; file dates are not acquisition dates)' if hist else '2026',
            'third_party_dependencies': 'Depicts commercial components; no third-party artwork' if hist else
            ('KiCad / Open CASCADE tooling (not redistributed)' if lic == 'CERN-OHL-W-2.0' else 'None bundled'),
            'publication_permission': 'Granted by both authors' if ok else ('Granted by both authors for own material' if hist else 'Pending author review'),
            'redistribution_permission': 'Granted under ' + lic if ok else 'PENDING',
            'modification_permission': 'Granted under ' + lic if ok else 'PENDING',
            'chosen_license': lic if ok else 'NONE ELECTED; candidate ' + lic,
            'approving_owner': APPROVAL['owners'],
            'date_signed': APPROVAL['date'] if ok else '',
            'release_status': 'LICENSED' if ok else 'PUBLIC_LICENSE_APPROVAL_PENDING',
            'justification': kind + ('; approved by both authors, recorded in ' + APPROVAL['record'] if ok
                                     else '; publication consent does not grant reuse rights')})
    return rows


def reuse_toml(rows):
    out = ['version = 1', '']
    rows = rows + [{'relative_path': 'LICENSE_MATRIX.csv', 'original_creator': NEW, 'chosen_license': 'CC-BY-4.0'}]
    for r in rows:
        out += ['[[annotations]]', f'path = "{r["relative_path"]}"', 'precedence = "override"',
                f'SPDX-FileCopyrightText = "{r["original_creator"]}"', f'SPDX-License-Identifier = "{r["chosen_license"]}"', '']
    return '\n'.join(out)


def main():
    a = argparse.ArgumentParser(); a.add_argument('--write-matrix', action='store_true'); args = a.parse_args()
    fails, notes = [], []
    ok = approved()
    fs = files()
    withheld = {}
    wm = ROOT / 'data/withheld_asset_manifest.csv'
    if wm.exists():
        with wm.open(encoding='utf-8-sig', newline='') as f:
            withheld = {r['sha256']: r['source_id'] for r in csv.DictReader(f)}
    else:
        fails.append('data/withheld_asset_manifest.csv missing; cannot screen withheld CAD')
    for p in fs:
        rel = p.relative_to(ROOT).as_posix()
        h = sha(p)
        if h in withheld:
            fails.append(f'withheld {withheld[h]} present as {rel}')
        if p.suffix.lower() in ('.stp', '.step', '.stl', '.obj', '.iges', '.igs', '.ipt', '.iam', '.f3d') and not rel.startswith(ALLOWED_STEP_DIR):
            fails.append(f'CAD/mesh outside R01 export folder: {rel}')
        if rel.startswith(ALLOWED_STEP_DIR) and not p.name.startswith('R01_'):
            fails.append(f'non-R01 file in R01 export folder: {rel}')
        if any(fnmatch.fnmatch(p.name, g) for g in FORBIDDEN_GLOBS):
            fails.append(f'prohibited file type: {rel}')
        if p.stat().st_size < 5_000_000 and SECRET_RE.search(p.read_bytes()):
            fails.append(f'credential-like text: {rel}')
    try:
        objs = subprocess.run(['git', 'rev-list', '--objects', '--all'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split('\n')
        hits, checked = [], 0
        for oid, path in [o.split(' ', 1) for o in objs if ' ' in o]:
            if subprocess.run(['git', 'cat-file', '-t', oid], cwd=ROOT, capture_output=True, text=True).stdout.strip() != 'blob':
                continue
            data = subprocess.run(['git', 'cat-file', 'blob', oid], cwd=ROOT, capture_output=True).stdout
            checked += 1
            if hashlib.sha256(data).hexdigest() in withheld or hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest() in withheld:
                hits.append(path)
        notes.append(f'git history: {checked} blobs screened')
        fails += [f'withheld CAD in git history: {x}' for x in hits]
    except (FileNotFoundError, subprocess.CalledProcessError):
        notes.append('git history: NOT CHECKED (no git metadata available)')

    rows = matrix_rows(fs, ok)
    if args.write_matrix:
        for _ in range(2):  # second pass covers REUSE.toml itself once it exists
            with (ROOT / 'LICENSE_MATRIX.csv').open('w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator='\n'); w.writeheader(); w.writerows(rows)
            if ok:
                (ROOT / 'REUSE.toml').write_text(reuse_toml(rows) + '\n')
            fs = files(); rows = matrix_rows(fs, ok)
    mpath = ROOT / 'LICENSE_MATRIX.csv'
    if not mpath.exists():
        fails.append('LICENSE_MATRIX.csv missing (run --write-matrix)')
        have = []
    else:
        with mpath.open(encoding='utf-8', newline='') as f:
            have = list(csv.DictReader(f))
        if {r['relative_path'] for r in have} != {r['relative_path'] for r in rows}:
            fails.append('LICENSE_MATRIX.csv does not cover exactly the files in the tree (run --write-matrix)')
        want = {r['relative_path']: r['chosen_license'] for r in rows}
        for r in have:
            if r['relative_path'] in want and r['chosen_license'] != want[r['relative_path']]:
                fails.append(f'licence mismatch for {r["relative_path"]}')
    used = {r['chosen_license'] for r in rows}
    if ok:
        for lid in sorted(used):
            if lid not in LICENSE_TEXT_SHA256:
                fails.append(f'unapproved licence id {lid}')
                continue
            t = ROOT / 'LICENSES' / f'{lid}.txt'
            if not t.is_file() or sha(t) != LICENSE_TEXT_SHA256[lid]:
                fails.append(f'LICENSES/{lid}.txt missing or not the canonical SPDX text')
        if any(r['release_status'] != 'LICENSED' or r['date_signed'] != APPROVAL['date'] for r in have):
            fails.append('matrix row not marked LICENSED with the recorded approval date')
        for p in fs:
            rel = p.relative_to(ROOT).as_posix()
            if p.suffix == '.py' and not rel.startswith('evidence/'):
                m = re.search(r'SPDX-License-Identifier:\s*([^\s"]+)', p.read_text(encoding='utf-8'))
                if not m or m.group(1) != classify(rel)[0]:
                    fails.append(f'SPDX header missing or wrong in {rel}')
            if p.suffix in ('.py', '.kicad_sch', '.kicad_sym', '.yml', '.toml') and STALE in p.read_text(encoding='utf-8', errors='ignore'):
                fails.append(f'stale pending-licence marker in {rel}')
        reuse = ROOT / 'REUSE.toml'
        if not reuse.is_file() or reuse.read_text() != reuse_toml(rows) + '\n':
            fails.append('REUSE.toml missing or out of date (run --write-matrix)')
    else:
        if any(r['release_status'] != 'PUBLIC_LICENSE_APPROVAL_PENDING' or r['date_signed'] for r in have):
            fails.append('LICENSE_MATRIX.csv records an approval while the lock says licensing is pending')
        if (ROOT / 'LICENSES').is_dir():
            fails.append('LICENSES/ present while licensing is pending')
    out = {'status': 'PASS' if not fails else 'FAIL', 'licensing': 'APPROVED' if ok else 'PENDING', 'files_screened': len(fs),
           'licences_used': sorted(used), 'notes': notes, 'failures': fails,
           'scope': 'Rights/exclusion screening of files; not a legal opinion'}
    print(json.dumps(out, indent=2))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
