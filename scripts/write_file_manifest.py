"""Write verification/file_manifest.csv (path, bytes, sha256) for every file except itself and .git.
SPDX-License-Identifier: LicenseRef-Pending-Approval
Run last, after all generated outputs and verification/repository_checks.json are final."""
import csv, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'verification/file_manifest.csv'
rows = []
for p in sorted(ROOT.rglob('*'), key=lambda q: q.relative_to(ROOT).as_posix()):
    rel = p.relative_to(ROOT)
    if p.is_file() and '.git' not in rel.parts and '__pycache__' not in rel.parts and p != OUT:
        rows.append((rel.as_posix(), p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest()))
with OUT.open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n'); w.writerow(['path', 'bytes', 'sha256']); w.writerows(rows)
print(f'{len(rows)} files written to {OUT.relative_to(ROOT)}')
