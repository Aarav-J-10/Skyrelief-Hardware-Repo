"""Fail-closed public-release gate, shared by both SkyRelief repositories.
SPDX-License-Identifier: LicenseRef-Pending-Approval

Rejects the release candidate if the working tree OR any blob in Git history
matches a withheld historical STEP hash, or if prohibited material is present
(STEP/mesh files outside the R01 export folder, the MDPI template, nested
archives, OS temp files, credentials). Also builds LICENSE_MATRIX.csv and checks
that no file claims an approved licence while PUBLICATION_RELEASE_LOCK.json says
licensing is pending. Standard library only; git is optional (history check is
skipped, and reported as skipped, without it).

  python scripts/release_gate.py               # check
  python scripts/release_gate.py --write-matrix  # (re)generate LICENSE_MATRIX.csv, then check
"""
import argparse, csv, fnmatch, hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', '__pycache__', '.venv'}
ALLOWED_STEP_DIR = 'cad/independently_authored/exports/'
FORBIDDEN_GLOBS = ['*.dot', '*.dotx', '*hardware-template*', '*.zip', '*.7z', '*.rar', '.DS_Store', 'Thumbs.db',
                   '*.tmp', '*.bak', '*.kicad_prl', '*.lck', '*.env', '*.pem', '*.key']
SECRET_RE = re.compile(rb'github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----')

# Classification rules for LICENSE_MATRIX.csv: first match wins.
RULES = [
    ('evidence/original/*.py', 'Abhinav Patro (credited in file name and project records)', 'Historical original script', 'MIT (proposed)'),
    ('evidence/original/*', 'Aarav Jalan; Abhinav Patro (project records)', 'Historical original document/data', 'CC-BY-4.0 (proposed)'),
    ('images/*', 'Aarav Jalan; Abhinav Patro (project photographs)', 'Historical original photograph', 'CC-BY-4.0 (proposed)'),
    ('assets/original_wiring_reference/*', 'Abhinav Patro (signed sketch)', 'Historical original sketch', 'CC-BY-4.0 (proposed)'),
    ('cad/independently_authored/*', 'SkyRelief authors with AI assistance (2026)', 'New unbuilt reference design (R01)', 'CERN-OHL-W-2.0 or CERN-OHL-S-2.0 (proposed)'),
    ('drawings/R01_*', 'SkyRelief authors with AI assistance (2026)', 'New reference drawing', 'CERN-OHL-W-2.0 or CERN-OHL-S-2.0 (proposed)'),
    ('kicad/*', 'SkyRelief authors with AI assistance (2026)', 'New native KiCad source/export', 'CERN-OHL-W-2.0 or CERN-OHL-S-2.0 (proposed)'),
    ('scripts/*', 'SkyRelief authors with AI assistance (2026)', 'New script', 'MIT (proposed)'),
    ('.github/*', 'SkyRelief authors with AI assistance (2026)', 'New CI configuration', 'MIT (proposed)'),
    ('*', 'SkyRelief authors with AI assistance (2026)', 'New documentation/data', 'CC-BY-4.0 (proposed)'),
]
GENERATED_LAST = {'verification/file_manifest.csv', 'verification/repository_checks.json'}
FIELDS = ['relative_path', 'hash', 'original_creator', 'authorship_evidence', 'created_when', 'third_party_dependencies',
          'publication_permission', 'redistribution_permission', 'modification_permission', 'chosen_license',
          'approving_owner', 'date_signed', 'release_status', 'justification']


def files():
    out = []
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            out.append(p)
    return out


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def classify(rel):
    for pat, creator, kind, proposal in RULES:
        if fnmatch.fnmatch(rel, pat):
            return creator, kind, proposal


def matrix_rows(fs):
    rows = []
    for p in fs:
        rel = p.relative_to(ROOT).as_posix()
        if rel == 'LICENSE_MATRIX.csv':
            continue
        creator, kind, proposal = classify(rel)
        hist = kind.startswith('Historical')
        rows.append({
            'relative_path': rel, 'hash': 'generated after this matrix; see verification/file_manifest.csv' if rel in GENERATED_LAST else 'sha256:' + sha(p), 'original_creator': creator,
            'authorship_evidence': 'Upstream project archive and author clarification (2026-10-19)' if hist else 'Created in this repository; see CHANGELOG.md',
            'created_when': '2024-2025 (project period; file dates are not acquisition dates)' if hist else '2026',
            'third_party_dependencies': 'Depicts commercial components; no third-party artwork' if hist else ('Open CASCADE / KiCad tooling (not redistributed)' if 'design' in kind or 'KiCad' in kind else 'None bundled'),
            'publication_permission': 'Granted by both authors for own material' if hist else 'Pending author review',
            'redistribution_permission': 'PENDING', 'modification_permission': 'PENDING',
            'chosen_license': 'NONE ELECTED; candidate ' + proposal, 'approving_owner': 'Aarav Jalan; Abhinav Patro (both required)',
            'date_signed': '', 'release_status': 'PUBLIC_LICENSE_APPROVAL_PENDING',
            'justification': kind + '; publication consent does not grant reuse rights'})
    return rows


def main():
    a = argparse.ArgumentParser(); a.add_argument('--write-matrix', action='store_true'); args = a.parse_args()
    fails, notes = [], []
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
    # Git history
    try:
        objs = subprocess.run(['git', 'rev-list', '--objects', '--all'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split('\n')
        blobs = [o.split(' ', 1) for o in objs if ' ' in o]
        hits, checked = [], 0
        for oid, path in blobs:
            kind = subprocess.run(['git', 'cat-file', '-t', oid], cwd=ROOT, capture_output=True, text=True).stdout.strip()
            if kind != 'blob':
                continue
            data = subprocess.run(['git', 'cat-file', 'blob', oid], cwd=ROOT, capture_output=True).stdout
            checked += 1
            if hashlib.sha256(data).hexdigest() in withheld or hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest() in withheld:
                hits.append(path)
        notes.append(f'git history: {checked} blobs screened')
        fails += [f'withheld CAD in git history: {x}' for x in hits]
    except (FileNotFoundError, subprocess.CalledProcessError):
        notes.append('git history: NOT CHECKED (no git metadata available)')
    # Licence consistency
    lock = ROOT / 'PUBLICATION_RELEASE_LOCK.json'
    pending = True
    if lock.exists():
        pending = json.loads(lock.read_text())['rights_status']['overall'] != 'APPROVED'
    else:
        fails.append('PUBLICATION_RELEASE_LOCK.json missing')
    if pending:
        for p in fs:
            if p.name.upper().startswith('LICENSE') and p.name.upper() not in ('LICENSES.MD', 'LICENSE_MATRIX.CSV'):
                fails.append(f'standalone licence file {p.name} present while licensing is pending')
    rows = matrix_rows(fs)
    mpath = ROOT / 'LICENSE_MATRIX.csv'
    if args.write_matrix:
        with mpath.open('w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator='\n'); w.writeheader(); w.writerows(rows)
    if mpath.exists():
        with mpath.open(encoding='utf-8', newline='') as f:
            have = list(csv.DictReader(f))
        if {r['relative_path'] for r in have} != {r['relative_path'] for r in rows}:
            fails.append('LICENSE_MATRIX.csv does not cover exactly the files in the tree (run --write-matrix)')
        if pending and any(r['release_status'] != 'PUBLIC_LICENSE_APPROVAL_PENDING' or r['date_signed'] for r in have):
            fails.append('LICENSE_MATRIX.csv records an approval while the lock says licensing is pending')
    else:
        fails.append('LICENSE_MATRIX.csv missing (run --write-matrix)')
    out = {'status': 'PASS' if not fails else 'FAIL', 'files_screened': len(fs), 'notes': notes, 'failures': fails,
           'scope': 'Rights/exclusion screening of files; not a legal opinion'}
    print(json.dumps(out, indent=2))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
