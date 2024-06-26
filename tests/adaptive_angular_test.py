# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:16:37 2023

@author: mens
"""
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror
from LaserCAD.basic_optics.mount import Composed_Mount

if freecad_da:
  clear_doc()

mir = Mirror(theta= 120) 
M = Composed_Mount(unit_model_list=["Adaptive_Angular_Mount","KS1","1inch_post"])
mir.normal = (1,1,-2)
mir.Mount = M
M.set_geom(mir.get_geom())
mir.draw()
mir.draw_mount()



if freecad_da:
  setview()