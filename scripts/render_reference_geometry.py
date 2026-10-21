"""Render only the independent R01 STEP exports; no historical source geometry.
SPDX-FileCopyrightText: 2026 Aarav Jalan and Abhinav Patro
SPDX-License-Identifier: MIT
Requires cadquery-ocp==8.0.1.1.0 and matplotlib.
"""
from pathlib import Path
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE,TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.TopLoc import TopLoc_Location
from OCP.BRep import BRep_Tool
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];CAD=ROOT/'cad/independently_authored/exports'
def triangles(shape):
 BRepMesh_IncrementalMesh(shape,0.25,False,0.3,True).Perform()
 exp=TopExp_Explorer(shape,TopAbs_FACE);out=[]
 while exp.More():
  face=TopoDS.Face(exp.Current());loc=TopLoc_Location();mesh=BRep_Tool.Triangulation_s(face,loc)
  if mesh:
   pts={}
   for i in range(1,mesh.NbNodes()+1):
    p=mesh.Node(i).Transformed(loc.Transformation());pts[i]=(p.X(),p.Y(),p.Z())
   for i in range(1,mesh.NbTriangles()+1):out.append([pts[k] for k in mesh.Triangle(i).Get()])
  exp.Next()
 return out
fig=plt.figure(figsize=(12,5.8),facecolor='white')
for n,(filename,title) in enumerate([('R01_locked_assembly.step','Locked / gate X = 10 mm'),('R01_released_assembly.step','Released / gate X = 28 mm')],1):
 r=STEPControl_Reader();assert r.ReadFile(str(CAD/filename))==IFSelect_RetDone;assert r.TransferRoots()>0
 shape=r.OneShape();ax=fig.add_subplot(1,2,n,projection='3d');ex=TopExp_Explorer(shape,TopAbs_SOLID);i=0
 forcolor=['#c2cbd2','#466e88','#ce9d45'];all_tri=[];all_colors=[]
 while ex.More():
  tri=triangles(ex.Current());all_tri.extend(tri);all_colors.extend([forcolor[i]]*len(tri));i+=1;ex.Next()
 poly=Poly3DCollection(all_tri,facecolors=all_colors,edgecolors='#56616a',linewidths=.05,alpha=1)
 ax.add_collection3d(poly)
 ax.set(xlim=(-4,114),ylim=(-4,68),zlim=(-6,15),xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm')
 ax.set_box_aspect((110,64,30));ax.view_init(elev=32,azim=-65);ax.set_title(title,fontsize=13,pad=15);ax.grid(False)
fig.suptitle('R01: independent keyhole gate bench reference',fontsize=17)
fig.text(.5,.05,'New CAD rendering, not a photograph. Unbuilt; material, loads and actuator linkage unassigned.',ha='center',fontsize=11)
fig.subplots_adjust(top=.83,bottom=.17,left=.02,right=.96,wspace=.13)
out=ROOT/'drawings/R01_geometry_preview.png';fig.savefig(out,dpi=180);plt.close(fig);print('Rendered independent R01 geometry')

