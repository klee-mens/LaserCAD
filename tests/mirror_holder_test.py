# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:16:37 2023

@author: mens
"""
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror
from LaserCAD.basic_optics.mount import Unit_Mount,Post, Composed_Mount,Post_Marker


if freecad_da:
  clear_doc()
  

from LaserCAD.basic_optics.mount import Adaptive_Angular_Mount

mir = Mirror(theta= 120) 
M = Composed_Mount(unit_model_list=["Adaptive_Angular_Mount","KS1","1inch_post"])
mir.normal = (1,0,0.5)
mir.set_mount(M)
mir.draw()
mir.draw_mount()

# mir.Mount = M
# M.set_geom(mir.get_geom())

mir2 = Mirror()
mir2.normal = (1,0,-2)
mir2. pos += (0,55, 0)
M2 = Composed_Mount()
M2.add(Adaptive_Angular_Mount(aperture=50.8/2,angle= 60))
M2.add(Unit_Mount("KS1"))
M2.add(Post())
M2.add(Post_Marker())
mir2.set_mount(M2)
mir2.draw()
mir2.draw_mount()

if freecad_da:
  setview()