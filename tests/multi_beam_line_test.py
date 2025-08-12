#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 17:25:33 2025

@author: mens
"""

from LaserCAD import Multi_Beamline_Composition

from LaserCAD import Mirror, Lambda_Plate, TFP56, Lens, Beam
from LaserCAD import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()

mbc = Multi_Beamline_Composition(name="MBC")
mbc.set_light_source(Beam(radius=2.5))

mbc.propagate(120)

mbc.add_on_axis(Mirror(phi=90))

mbc.propagate(75)

mbc.add_on_axis(Mirror(phi=90))

mbc.propagate(100)

mbc.add_on_axis(Mirror(phi=-90))

mbc.propagate(100)

mbc.add_on_axis(Lambda_Plate())

mbc.propagate(100)

tfp = TFP56()
mbc.add_on_axis(tfp)
mbc.compute_beams()

mbc.propagate(120)

mbc.add_on_axis(Mirror(phi=-90))
mbc.propagate(120)

mbc.add_new_line(tfp.get_alternative_beam())

mbc.propagate(80)

mbc.add_on_axis(Mirror(phi=-180+2*56))
mbc.propagate(55)

mbc.add_on_axis(Lens())

mbc.propagate(123)


mbc.draw()

if freecad_da:
  setview()