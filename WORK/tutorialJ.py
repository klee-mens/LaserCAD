#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 16:13:57 2025

@author: mens
"""
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
from LaserCAD.basic_optics import Beam, Lens, SquareBeam, Ray, Composition, Ray_Distribution
import numpy as np

if freecad_da:
  clear_doc()

alphas = np.linspace(-0.05, 0.05, 3)
betas = np.linspace(-0.05, 0.05, 3)

allrays = [Ray()]

for al in alphas:
  for bet in betas:
    sq = SquareBeam(radius=5, ray_in_line=3)
    sq.rotate(vec=(0,0,1), phi=al)
    sq.rotate(vec=(0,1,0), phi=bet)
    allrays.extend(sq.get_all_rays())

bigbundel = SquareBeam()
bigbundel.override_rays(allrays)

focal = 100

raydist = Ray_Distribution(radius=5, angle=0.05, steps=3)

comp = Composition("BigRayTeles")
comp.set_light_source(raydist)
comp.propagate(100)
comp.add_on_axis(Lens(f=100))
comp.propagate(100*2)
comp.add_on_axis(Lens(f=100))
comp.propagate(100)

comp.draw()

if freecad_da:
  setview()