"""Portable file-level verification. No hardware access.
SPDX-License-Identifier: LicenseRef-Pending-Approval
"""
from pathlib import Path
import argparse,csv,hashlib,json,re,sys,xml.etree.ElementTree as ET,urllib.parse
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
def csvrows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'MISSING'
checks=[];fail=[]
def check(name,condition,detail=''):
 checks.append({'check':name,'pass':bool(condition),'detail':detail})
 if not condition:fail.append(name+': '+detail)
def exact_exists(target):
 try:
  rel=target.relative_to(ROOT);cur=ROOT
  for part in rel.parts:
   if part not in [x.name for x in cur.iterdir()]:return False
   cur=cur/part
  return cur.is_file() or cur.is_dir()
 except (ValueError,FileNotFoundError,NotADirectoryError):return False
def main():
 files=[p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts]
 paths={p.relative_to(ROOT).as_posix() for p in files}
 check('README at repository root','README.md' in paths)
 check('No nested ZIP, git, caches or temporary files',not any(p.suffix.lower() in ['.zip','.tmp','.bak','.pyc','.kicad_prl'] or '.git' in p.parts or '__pycache__' in p.parts for p in files))
 check('Portable unique case-sensitive filenames',len(paths)==len({x.casefold() for x in paths}) and all(not any(c in x for c in '<>:"|?*') for x in paths))
 check('No unintended huge files',all(p.stat().st_size<25_000_000 for p in files))
 originals=csvrows(ROOT/'data/included_original_assets.csv')
 source=csvrows(ROOT/'data/source_manifest.csv');source_map={x['path']:x for x in source}
 check('Fresh 49-source manifest',len(source)==49 and all(x['frozen_commit']=='42f9a44600351ec6d0a57fb20756c547acf38cad' for x in source))
 for x in originals:
  p=ROOT/x['release_path']
  check('Original asset release hash: '+x['release_path'],p.is_file() and sha(p)==x['release_sha256'])
  check('Original source hash: '+x['source_path'],source_map.get(x['source_path'],{}).get('sha256')==x['source_sha256'])
 restricted={x['sha256'] for x in csvrows(ROOT/'data/withheld_asset_manifest.csv')}
 check('No rights-withheld original binaries',not any(sha(p) in restricted for p in files))
 for p in files:
  rel=p.relative_to(ROOT).as_posix()
  if p.suffix.lower() in ['.md','.csv','.json','.py','.svg','.net','.kicad_sch','.kicad_pro','.kicad_sym','.step','.cff','.txt']:
   t=p.read_text(encoding='utf8')
   # Actual local paths, common tokens/private keys; email for citation is intentionally public.
   pattern=r'\b[A-Za-z]:[\\/]|/Us'+r'ers/|/ho'+r'me/|github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----'
   check('No local path/secret text: '+rel,not bool(re.search(pattern,t)))
  if p.suffix.lower()=='.md':
   for label,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',p.read_text(encoding='utf8')):
    if re.match(r'^(https?://|mailto:|#)',target):continue
    target=urllib.parse.unquote(target.split('#')[0]).strip('<>')
    check('Exact-case Markdown link: '+rel+' -> '+target,exact_exists((p.parent/target).resolve()))
  if p.suffix.lower() in ['.svg','.net']:
   try:ET.parse(p);valid=True
   except Exception:valid=False
   check('XML parse: '+rel,valid)
  if p.suffix.lower()=='.csv':
   try:
    with p.open(encoding='utf8',newline='') as f:
     rr=list(csv.reader(f));valid=bool(rr) and len(set(rr[0]))==len(rr[0]) and all(len(x)==len(rr[0]) for x in rr[1:])
   except Exception:valid=False
   check('UTF-8 rectangular CSV: '+rel,valid)
 parts=csvrows(ROOT/'bom/complete_platform_parts_crosswalk.csv')
 required='platform subsystem source_component_name reported_quantity confirmed_or_assumed model_family verified_revision source_reference replacement_item manufacturer_or_vendor_url price currency price_date stock_status tax_shipping_status licensing_or_reuse_status electrical_compatibility_status cost_scope uncertainty_notes'.split()
 check('34 stable BOM IDs and required schema',len(parts)==34 and [x['component_id'] for x in parts]==[f'B{i:02}' for i in range(1,35)] and all(k in parts[0] for k in required))
 quotes=csvrows(ROOT/'bom/supplier_cost_provenance.csv');qm={x['cost_id']:x for x in quotes}
 check('20 distinct supplier observations',len(quotes)==20 and len(qm)==20)
 for q in quotes:
  check('Quote arithmetic '+q['cost_id'],Decimal(q['unit_replacement_price'])*Decimal(q['quantity'])==Decimal(q['extended_price']))
  check('Source URL/date '+q['cost_id'],q['url'].startswith('https://') and q['accessed_date']=='2026-10-20')
 check('INR named partial 18428',sum(Decimal(qm[f'P{i:02}']['extended_price']) for i in range(1,6))==Decimal(18428))
 check('Proposed category partial 5920',sum(Decimal(qm[f'P{i:02}']['extended_price']) for i in range(6,12))==Decimal(5920))
 check('USD named AIO/motors 115.95',sum(Decimal(qm[f'P{i:02}']['extended_price']) for i in [12,13])==Decimal('115.95'))
 check('Two CW quote never priced as four',qm['P06']['quantity']=='2' and next(x for x in parts if x['component_id']=='B03')['reported_quantity']=='4')
 cats=json.loads((ROOT/'data/evidence_categories.json').read_text())
 check('Ledger uses exact evidence classes',all(x['category'] in cats for x in csvrows(ROOT/'data/evidence_ledger.csv')))
 check('18 historical + 2 new functional interfaces',len(csvrows(ROOT/'data/documented_connections.csv'))==20)
 freeze=json.loads((ROOT/'data/source_freeze.json').read_text());check('49 Git blobs verified',freeze['all_git_blobs_verified'] and freeze['blobs']==49)
 severity={'BLOCKING FOR PUBLIC RELEASE','BLOCKING FOR REPRODUCIBLE HARDWARE','MAJOR','MINOR'}
 check('Completed issue severity vocabulary',all(x['severity'] in severity for x in csvrows(ROOT/'data/issue_matrix.csv')))
 if (ROOT/'kicad').is_dir():
  report=json.loads((ROOT/'verification/native_kicad_checks.json').read_text())
  check('Native KiCad 9.x actually executed',report['tool_version'].startswith('9.0.') and len(report['projects'])==3)
  for project in report['projects']:
   check('Native export success '+project['project'],all(project[k]['exit_code']==0 for k in ['svg','pdf','netlist']))
   if project['project']=='scout_reference':check('Scout unresolved ERC retained',project['erc']['exit_code']==5 and project['violations_by_type']=={'pin_not_connected':9})
   else:check('Scoped role ERC zero '+project['project'],project['erc']['exit_code']==0 and project['violations_by_type']=={})
 else:
  g=json.loads((ROOT/'cad/independently_authored/geometry_verification.json').read_text())
  check('Five new STEP imports recorded',len(g['part_exports'])==5 and all(x['valid'] and x['volume_mm3']>0 for x in g['part_exports']))
  check('19 sampled gate positions',len(g['translation_checks'])==19 and all(abs(x['chassis_overlap_mm3'])<1e-6 for x in g['translation_checks']))
 if (ROOT/'verification/file_manifest.csv').exists():
  mf=csvrows(ROOT/'verification/file_manifest.csv')
  check('File manifest covers exact repository',set(x['path'] for x in mf)==paths-{'verification/file_manifest.csv'})
  for x in mf:check('SHA-256 '+x['path'],sha(ROOT/x['path'])==x['sha256'])
 result={'status':'PASS' if not fail else 'FAIL','checks_run':len(checks),'failures':fail,'python':sys.version.split()[0],'scope':'File/native report validation only; no physical testing','checks':checks}
 return result
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--write-report',action='store_true');args=a.parse_args()
 result=main()
 if args.write_report:
  (ROOT/'verification/repository_checks.json').write_text(json.dumps(result,indent=2),encoding='utf8')
 print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
 sys.exit(0 if result['status']=='PASS' else 1)

