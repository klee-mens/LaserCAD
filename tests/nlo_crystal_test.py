#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 09:15:45 2025

@author: mens
"""

from LaserCAD.basic_optics.non_linear_crystal import NLO_Crystal
from LaserCAD import Composition
from LaserCAD import freecad_da, clear_doc

if freecad_da:
  clear_doc()

comp = Composition(name="SHG_Beamline")
comp.propagate(80)
comp.add_on_axis(NLO_Crystal())
comp.propagate(80)

comp.draw()