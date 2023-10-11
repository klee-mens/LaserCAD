# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:16:37 2023

@author: mens
"""

import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
ind = pfad.rfind("/")
pfad = pfad[0:ind-1]
ind = pfad.rfind("/")
pfad = pfad[0:ind]
if not pfad in sys.path:
  sys.path.append(pfad)


from LaserCAD.non_interactings import Iris, Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam,Grating, Composition, inch, Curved_Mirror, Ray, Geom_Object, LinearResonator, Lens, Component
from LaserCAD.freecad_models.utils import thisfolder, load_STL

if freecad_da:
  clear_doc()

# iris = Iris()
# iris.draw()
# iris.draw_mount()

# mir = Grating()
# mir.pos= (0,0,120)
# mir.normal=(1,1,0)
# mon = mir.mount
# print(mir.mount.docking_obj.get_geom())
# mon.draw_dict["offset"] = np.array((-5, 0, 0))
# mon.draw_dict["rotation"] = np.array((1, 0, 0)), np.pi*90/180
mir=Mirror()
mir.aperture = 25.4
mir.pos = (100,0,65)
mir.draw()
mir.draw_mount()
# mir.draw_mount()

# compo = Component()
# compo.draw()
# compo.draw_mount()

from LaserCAD.basic_optics.post import Post_and_holder

# post = Post_and_holder()
# post.draw()

# res = LinearResonator(name="Compact")
# m1 = Mirror()
# m2 = Mirror()
# focus = 1500
# foc = Lens(f=focus)
# g1 = 0.5
# g2 = 0.1
# print(g1*g2)
# a = focus*(1-g1)
# b = focus*(1-g2)

# res.set_wavelength(2400e-6)
# res.add_on_axis(m1)
# res.propagate(a)
# res.add_on_axis(foc)
# res.propagate(b)
# res.add_on_axis(m2)

# res.draw()

# lam = Lambda_Plate()
# lam.pos += (0,40,0)
# lam.draw()

# lam.draw_mount()


if freecad_da:
  setview()