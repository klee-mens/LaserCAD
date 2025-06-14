#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 13:16:39 2024

@author: mens
"""

from LaserCAD.basic_optics import Beam, RainbowBeam, SquareBeam, Ray_Distribution
from LaserCAD.basic_optics import CircularRayBeam, Gaussian_Beam
from LaserCAD.basic_optics import Composition, Lens, Grating
from LaserCAD.freecad_models import freecad_da, setview, clear_doc

if freecad_da:
  clear_doc()

c1 = Composition(name="ElCone")
b = Beam(radius=2, angle=0.01, name="ElCone")
c1.set_light_source(b)
c1.propagate(150)
c1.add_on_axis(Lens())
c1.propagate(100)
c1.draw()

sq = SquareBeam(radius=3, ray_in_line=3, name="FairAndSquare")
c2 = Composition(name="FairAndSquare")
c2.pos += (0, 50, 0)
c2.set_light_source(sq)
c2.propagate(110)
c2.add_on_axis(Lens())
c2.propagate(110)
c2.draw()

cb = CircularRayBeam(radius=4, ring_number=2, name="CountCircula")
c3 = Composition(name="CountCircula")
c3.set_light_source(cb)
c3.pos += (0, 100, 0)
c3.propagate(110)
c3.add_on_axis(Lens())
c3.propagate(80)
c3.draw()

rb = RainbowBeam(ray_count=11, name="SomwhereOver")
c4 = Composition(name="SomwhereOver")
c4.set_light_source(rb)
c4.pos += (0, 150, 0)
c4.propagate(250)
gr = Grating(grat_const=0.001)
c4.add_on_axis(gr)
gr.normal = (1,1,0)
c4.propagate(100)
c4.draw()

gb = Gaussian_Beam(name="KFG-Beam")
c5 = Composition(name="KFG-Beam")
c5.set_light_source(gb)
c5.pos += (0,200,0)
c5.propagate(80)
c5.add_on_axis(Lens())
c5.propagate(120)
c5.draw()

b1 = Beam(ray_count = 5)
b1.draw_dict["model"] = "ray_group"
c6 = Composition(name="naked rays")
c6.pos -= (0,50,0)
c6.set_light_source(b1)
c6.propagate(80)
c6.add_on_axis(Lens())
c6.propagate(120)
c6.draw()

gb2 = Gaussian_Beam(radius=1)
gb2.pos += (0, 250, 0)
gb2.draw()
gb2.draw_dict["model"] = "cone"
gb2.draw()

raydist = Ray_Distribution(radius=5, angle=0.03, steps=3)
comp = Composition(name="BigRayTeles")
comp.set_light_source(raydist)
comp.propagate(100)
comp.add_on_axis(Lens(f=100))
comp.propagate(100*2)
comp.add_on_axis(Lens(f=100))
comp.propagate(100)
comp.pos += (0,-100, 0)
comp.draw()

if freecad_da:
  setview()