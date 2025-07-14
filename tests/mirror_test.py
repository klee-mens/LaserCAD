#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:01:45 2024

@author: mens
"""

from LaserCAD.basic_optics import Mirror, Composition, Beamsplitter, Composed_Mount, inch
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()

m = Mirror(phi=120)
comp = Composition(name="FlipMirror")
comp.propagate(70)
comp.add_on_axis(m)
comp.propagate(50)


BStrans = Beamsplitter(name="50-50BS")
BStrans.aperture = 3*inch
BStrans.set_mount(Composed_Mount(unit_model_list=["KS3", "0.5inch_post"]))

BSreflec = Beamsplitter(transmission=False)
BSreflec.invisible = True
BSreflec.Mount.invisible = True

mysterious_back_mirror = Mirror()
mysterious_back_mirror.invisible = True
mysterious_back_mirror.Mount.invisible = True

inputarm = 150
arm1 = 120
arm2 = 130
outputarm = 170

michel = Composition(name="Interferometer")
michel.pos += (0,200,20)
michel.propagate(inputarm)
michel.add_on_axis(BStrans)
michel.propagate(arm1)
michel.add_on_axis(Mirror())
michel.propagate(arm1)

BSreflec.set_geom(BStrans.get_geom())

michel.add_on_axis(BSreflec)
michel.propagate(outputarm)

michel.add_on_axis(mysterious_back_mirror)
michel.propagate(outputarm + arm2)
michel.add_on_axis(Mirror())
michel.propagate(outputarm + arm2)

# =============================================================================
# draw selection
# =============================================================================
comp.draw()

michel.draw()


if freecad_da:
  setview()