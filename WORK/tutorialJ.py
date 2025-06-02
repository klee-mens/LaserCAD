#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 16:13:57 2025

@author: mens
"""
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()

import LaserCAD.basic_optics as LC

sb = LC.SquareBeam(radius=5, ray_in_line=5)
lens1 = LC.Lens(f=100)
lens2 = LC.Lens(f=200)
lens2.aperture = 50.8
kt = LC.Composition()
kt.set_light_source(sb)
kt.propagate(100)
kt.add_on_axis(lens1)
kt.propagate(100+200)
kt.add_on_axis(lens2)
kt.propagate(200)
kt.draw()


# =============================================================================
# draw section
# =============================================================================


if freecad_da:
  setview()