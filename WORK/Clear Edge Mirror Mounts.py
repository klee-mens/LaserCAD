# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:12:57 2024

@author: 12816
"""
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror,Crystal
from LaserCAD.basic_optics import Beam,Grating, Composition, inch, Curved_Mirror, Ray, Geom_Object, LinearResonator, Lens, Component
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.basic_optics.mount import Unit_Mount,Post, Composed_Mount
from LaserCAD.basic_optics.mount import MIRROR_LIST,LENS_LIST

if freecad_da:
  clear_doc()
  
M = Mirror()
M.Mount = Composed_Mount(["U100-A2K","1inch_post"])
M.draw()
M.draw_mount()

M2 = Mirror()
M2.aperture = 25.4*2
M2.Mount = Composed_Mount(["U200-A2K","1inch_post"])
M2.pos = (100,0,80)
M2.draw()
M2.draw_mount()