"""Cross-repository consistency check; standard library only.
SPDX-License-Identifier: LicenseRef-Pending-Approval
"""
import argparse,hashlib,json
from pathlib import Path
a=argparse.ArgumentParser();a.add_argument('mechanical',type=Path);a.add_argument('electronics',type=Path);args=a.parse_args()
shared=['bom/complete_platform_parts_crosswalk.csv','bom/supplier_cost_provenance.csv','data/source_manifest.csv','data/evidence_ledger.csv','data/documented_connections.csv','data/unresolved_nets.csv','data/source_geometry_audit.csv','data/withheld_asset_manifest.csv','data/archived_thrust_sheet_transcription.csv']
result=[]
for f in shared:
 p=args.mechanical/f;q=args.electronics/f
 same=p.is_file() and q.is_file() and p.read_bytes()==q.read_bytes()
 result.append({'file':f,'identical':same})
print(json.dumps({'status':'PASS' if all(x['identical'] for x in result) else 'FAIL','comparisons':result},indent=2))
raise SystemExit(0 if all(x['identical'] for x in result) else 1)

