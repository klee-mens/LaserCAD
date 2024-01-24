#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 19:06:21 2023

@author: mens
"""

import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
  
  
from LaserCAD.basic_optics import Geom_Object, Beam, Ray
from LaserCAD.basic_optics import Crystal, Grating, Intersection_plane, Lens
from LaserCAD.basic_optics import Mirror

from LaserCAD.freecad_models.utils import load_STL, freecad_da, setview, clear_doc, thisfolder



g = Geom_Object()
g.pos = (-30, -100, 50)
g.normal = (1,1,1)
stl_file=thisfolder+"/misc_meshes/Laser_Head-Body.stl"
g.draw_dict["stl_file"] = stl_file
g.freecad_model = load_STL
g.draw()


b = Beam()
b.draw()

c = Crystal()
c.draw()


gr = Grating()
gr.pos += (0,80,0)
gr.normal = (1,2,0)
gr.draw()


sec = Intersection_plane()
sec.pos += (50,-80,0)
sec.normal = (-1,-2,0)
sec.draw()

le = Lens()
le.pos += (-30, -90, 0)
le.normal = (1,4,0)
le.draw()

mir = Mirror()
mir.pos += (20, 200, 0)
mir.normal = (1,0.3,0)
mir.draw()

r = Ray()
r.pos += (10,20,30)
r.normal = (1,2,3)
r.draw()


from LaserCAD.basic_optics.mount import Unit_Mount

um = Unit_Mount()
um.draw()

