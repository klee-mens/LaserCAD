# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:16:37 2023

@author: mens
"""
from LaserCAD import clear_doc, setview, freecad_da
from LaserCAD import Mirror, Composed_Mount, Unit_Mount
from LaserCAD.basic_optics.mount import Adaptive_Angular_Mount

if freecad_da:
  clear_doc()

mir1 = Mirror(phi=0, theta=90) 
M1 = Composed_Mount(unit_model_list=["Adaptive_Angular_Mount","KS1","1inch_post"])
mir1.set_mount(M1)
mir1.draw()
mir1.draw_mount()

mir2 = Mirror(phi=0, theta=120) 
M2 = Composed_Mount(unit_model_list=["Adaptive_Angular_Mount","KS1","1inch_post"])
mir2.set_mount(M2)
mir2.pos += (0, 60, 0)
mir2.draw()
mir2.draw_mount()

mir3 = Mirror() 
M3 = Composed_Mount(unit_model_list=["Adaptive_Angular_Mount","KS1","1inch_post"])
mir3.normal = (1, 1, -2)
mir3.set_mount(M3)
mir3.pos += (0, 100, 0)
mir3.draw()
mir3.draw_mount()




if freecad_da:
  setview()