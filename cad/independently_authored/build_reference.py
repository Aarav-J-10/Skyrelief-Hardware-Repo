"""Independent R01 keyhole gate bench reference. No historical CAD is read.
SPDX-License-Identifier: LicenseRef-Pending-Approval
Requires cadquery-ocp==8.0.1.1.0; geometry in millimetres.
"""
import json, math, sys
from pathlib import Path
from OCP.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse, BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.gp import gp_Trsf
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.STEPControl import STEPControl_Writer, STEPControl_Reader, STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopoDS import TopoDS_Compound
from OCP.BRep import BRep_Builder
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
HERE=Path(__file__).resolve().parent
def box(x,y,z,dx,dy,dz): return BRepPrimAPI_MakeBox(gp_Pnt(x,y,z),dx,dy,dz).Shape()
def cyl(x,y,z,r,h): return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x,y,z),gp_Dir(0,0,1)),r,h).Shape()
def cut(a,b): return BRepAlgoAPI_Cut(a,b).Shape()
def fuse(a,b): return BRepAlgoAPI_Fuse(a,b).Shape()
def move(s,x=0):
 t=gp_Trsf();t.SetTranslation(gp_Vec(x,0,0));return BRepBuilderAPI_Transform(s,t,True).Shape()
def vol(s):
 p=GProp_GProps();BRepGProp.VolumeProperties_s(s,p);return p.Mass()
def solids(s):
 e=TopExp_Explorer(s,TopAbs_SOLID);n=0
 while e.More(): n+=1;e.Next()
 return n
def compound(parts):
 c=TopoDS_Compound();b=BRep_Builder();b.MakeCompound(c)
 for p in parts:b.Add(c,p)
 return c
def main():
 p=json.loads((HERE/'parameters.json').read_text());out=HERE/'exports';out.mkdir(exist_ok=True)
 L=p['base_length'];W=p['base_width'];B=p['base_thickness'];T=p['release_travel']
 GL=p['gate_length'];GW=p['gate_width'];GT=p['gate_thickness'];G=p['rail_clearance'];GZ=p['gate_bottom_z']
 XC=L/2;YC=W/2;NECK=p['gate_neck_width'];AP=p['gate_release_hole_diameter'];FLANGE=p['coupon_flange_diameter'];STEM=p['coupon_stem_diameter']
 assert L>=10+GL+T and W>GW+12 and G>0 and GZ==B+G and int(T)==T
 assert STEM<NECK<FLANGE<AP<p['drop_window_diameter'] and abs(XC-T-18)>AP/2+1.6
 low=YC-GW/2-G-4;high=YC+GW/2+G;lipz=GZ+GT+G;top=lipz+2
 base=box(0,0,0,L,W,B)
 for x in (6,L-6):
  for y in (6,W-6):base=cut(base,cyl(x,y,-1,p['mount_hole_diameter']/2,B+2))
 base=cut(base,cyl(XC,YC,-1,p['drop_window_diameter']/2,B+2))
 # Wall/lip overlaps form connected rails on the base. Gate clearance 0.5 mm.
 for y in (low,high):
  base=fuse(base,box(5,y,B,L-10,4,top-B))
 for y in (low+4,high-3):base=fuse(base,box(5,y,lipz,L-10,3,2))
 gate=box(10,YC-GW/2,GZ,GL,GW,GT)
 gate=cut(gate,cyl(XC-T,YC,GZ-1,AP/2,GT+2))
 gate=cut(gate,box(XC-T,YC-NECK/2,GZ-1,T+6,NECK,GT+2))
 gate=cut(gate,cyl(18,YC,GZ-1,1.6,GT+2))
 coupon=fuse(cyl(XC,YC,-3,STEM/2,GZ+GT+3),cyl(XC,YC,GZ+GT,FLANGE/2,2))
 parts={'R01_chassis':base,'R01_gate':gate,'R01_coupon':coupon,
 'R01_locked_assembly':compound([base,gate,coupon]),
 'R01_released_assembly':compound([base,move(gate,T),coupon])}
 rows=[]
 for name,shape in parts.items():
  assert BRepCheck_Analyzer(shape).IsValid() and vol(shape)>0
  f=out/(name+'.step');w=STEPControl_Writer();w.Transfer(shape,STEPControl_AsIs);assert w.Write(str(f))==IFSelect_RetDone
  # Omit local export identity while retaining STEP structure.
  import re
  text=f.read_text();text=re.sub(r"FILE_NAME\s*\(.*?;", "FILE_NAME('"+f.name+"','2026-10-20T00:00:00',('SkyRelief reference documentation'),('Independent bench reference'),'Open CASCADE','R01 new design','');",text,count=1,flags=re.S);f.write_text(text)
  r=STEPControl_Reader();assert r.ReadFile(str(f))==IFSelect_RetDone;assert r.TransferRoots()>0
  reopened=r.OneShape();assert BRepCheck_Analyzer(reopened).IsValid()
  assert solids(reopened)==(3 if 'assembly' in name else 1)
  rows.append({'file':f.name,'valid':True,'solids':solids(reopened),'volume_mm3':vol(reopened)})
 checks=[]
 for dx in range(int(T)+1):
  overlap=abs(vol(BRepAlgoAPI_Common(base,move(gate,dx)).Shape()))
  assert overlap<1e-6
  checks.append({'gate_translation_mm':dx,'chassis_overlap_mm3':overlap})
 report={'design':'REFERENCE DESIGN (NEW), unbuilt bench mechanism','kernel':'cadquery-ocp 8.0.1.1.0','units':'mm','part_exports':rows,'translation_checks':checks,'release_geometry':{'flange_diameter_mm':FLANGE,'neck_width_mm':NECK,'release_aperture_mm':AP,'travel_mm':T},'limits':'Geometric clearance only. No material, load, wear, servo, linkage or flight validation.'}
 (HERE/'geometry_verification.json').write_text(json.dumps(report,indent=2))
 print(json.dumps({'step_files':len(rows),'translation_positions_checked':len(checks),'status':'PASS digital geometry only'}))
if __name__=='__main__':main()

