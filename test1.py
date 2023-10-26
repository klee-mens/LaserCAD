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


# from LaserCAD.non_interactings import Iris
# from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror
from LaserCAD.basic_optics import Beam,Grating, Composition, inch, Curved_Mirror, Ray, Geom_Object, LinearResonator, Lens, Component
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.basic_optics.mount import Mount,Composed_Mount,Special_mount

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
mir=Mirror(phi=90)
mir.mount_dict['model']= 'KS1'
mir.draw()
mir.draw_mount()

mir1=Mirror(phi=-90)
mir1.pos = (100,0,80)
mir1.mount_dict["post_type"] = "0.5inch_post"
mir1.draw()
mir1.draw_mount()

mir2=Mirror(phi=90)
mir2.pos = (200,0,80)
mir2.aperture = 25.4*2
mir2.draw()
mir2.draw_mount()

mir3 = Mirror()
mir3.pos = (400,0,80)
mir3.mount_dict["post_type"] = "large_post"
mir3.draw()
mir3.draw_mount()

M=Composed_Mount()
M1=Special_mount(model="MH25",drawing_post=False)
M1.docking_obj.pos = M1.pos+(6.3,0,0)
M1.docking_obj.normal = M1.normal
M2=Mount(model="KMSS")
M.add(M1)
M.add(M2)
mir4 = Mirror(phi=90)
mir4.pos = (600,0,80)
mir4.mount = M
mir4.draw()
mir4.draw_mount()

# from LaserCAD.non_interactings.table import Table
# t = Table()
# t.pos = (-1000,-500,0)
# t.draw()

# # compo = Component()
# # compo.draw()
# # compo.draw_mount()

# M = Mirror(phi=90)
# M.draw()

# ls = Beam(radius=2, angle=-0.01)
# ls.draw()

# from LaserCAD.basic_optics.post import Post_and_holder

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