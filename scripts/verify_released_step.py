"""Read-only reimport of every delivered new STEP.
SPDX-FileCopyrightText: 2026 Aarav Jalan and Abhinav Patro
SPDX-License-Identifier: MIT
"""
from pathlib import Path
import json
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
root=Path(__file__).resolve().parents[1]
expected=json.loads((root/'cad/independently_authored/geometry_verification.json').read_text())
results=[]
for x in expected['part_exports']:
 p=root/'cad/independently_authored/exports'/x['file'];r=STEPControl_Reader();assert r.ReadFile(str(p))==IFSelect_RetDone;assert r.TransferRoots()>0
 shape=r.OneShape();assert BRepCheck_Analyzer(shape).IsValid();e=TopExp_Explorer(shape,TopAbs_SOLID);n=0
 while e.More():
  solid=e.Current();prop=GProp_GProps();BRepGProp.VolumeProperties_s(solid,prop);assert prop.Mass()>0;n+=1;e.Next()
 prop=GProp_GProps();BRepGProp.VolumeProperties_s(shape,prop)
 assert n==x['solids'] and abs(prop.Mass()-x['volume_mm3'])<1e-5
 results.append({'file':p.name,'solids':n,'valid':True,'positive_volumes':True})
print(json.dumps({'status':'PASS','step_files':results,'scope':'Digital geometry only, no physical qualification'},indent=2))

