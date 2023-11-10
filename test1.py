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
from LaserCAD.basic_optics import Mirror,Crystal
from LaserCAD.non_interactings import Pockels_Cell,Lambda_Plate
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
# A_target = 4.908738521234052 #from gain simlutation area in mm^2
# focal = 2500
# lam_mid = 2.4e-3
# A_natural = lam_mid * focal
# geometrie_factor = A_target / A_natural
# total_length = focal * (1 - np.sqrt(1 - geometrie_factor**2))

# # design params
# dist1 = 570
# dist_crystal_end = 20
# last = total_length - dist1
# # optics
# mir1 = Mirror(phi=180)
# cm = Curved_Mirror(radius=focal*2, phi = 180)

# simres = LinearResonator(name="simple_Resonator1")
# simres.set_wavelength(lam_mid)
# simres.add_on_axis(mir1)
# simres.propagate(dist1)
# simres.propagate(last-dist_crystal_end)
# laser_crys = Crystal(width=6, thickness=10, n=2.45)

# simres.add_on_axis(laser_crys)
# simres.propagate(dist_crystal_end)

# simres.add_on_axis(cm)

# simres.compute_eigenmode()
# simres.draw()
# from LaserCAD.non_interactings.table import Table
# t = Table()
# t.pos = (-1000,-500,0)
# t.draw()
a = Mirror()
a.pos = (0,0,0)
a.draw()
a.draw_mount()
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