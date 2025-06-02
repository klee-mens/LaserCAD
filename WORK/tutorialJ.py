#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 16:13:57 2025

@author: mens
"""
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()

# =============================================================================
# Square Beam Lenses
# =============================================================================
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
kt.pos = (10, 20, 120)
# kt.draw()

# =============================================================================
# Anastigmatic Mirror Telescope
# =============================================================================

mir1 = LC.Curved_Mirror(radius=250, phi=180-8)
mir2 = LC.Curved_Mirror(radius=250, phi=0,
                        theta=180-8)
mir2.set_mount(LC.Composed_Mount(
  unit_model_list=["KS1", "0.5inch_post"]))

mt = LC.Composition()
mt.set_light_source(LC.Beam(radius=2))
mt.propagate(350)
mt.add_on_axis(mir1)
mt.propagate(250)
mt.add_on_axis(mir2)
mt.propagate(350)
mt.draw()


# =============================================================================
# draw section
# =============================================================================
kt.draw()
# mt.draw()


if freecad_da:
  setview()