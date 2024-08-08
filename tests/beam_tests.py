#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 13:16:39 2024

@author: mens
"""

from LaserCAD.basic_optics.beam import Beam, RainbowBeam, SquareBeam, CircularRayBeam, Gaussian_Beam
from LaserCAD.freecad_models import freecad_da, setview, clear_doc

if freecad_da:
  clear_doc()

b = Beam(radius=2, angle=0.01, name="ElCone")
b.set_length(250)
b.draw()

sq = SquareBeam(radius=3, ray_in_line=3, name="FairAndSquare")
sq.pos += (0, 50, 0)
sq.set_length(210)
sq.draw()

cb = CircularRayBeam(radius=4, ring_number=2, name="CountCircula")
cb.pos += (0, 100, 0)
cb.set_length(190)
cb.draw()

rb = RainbowBeam(ray_count=11, name="SomwhereOver")
rb.pos += (0, 150, 0)
rb.set_length(230)
rb.draw()

gb = Gaussian_Beam(name="KFG-Beam")
gb.pos += (0,200,0)
gb.draw()


gb2 = Gaussian_Beam(radius=1)
gb2.pos += (0, 250, 0)
gb2.draw()
gb2.draw_dict["model"] = "cone"
gb2.draw()


if freecad_da:
  setview()