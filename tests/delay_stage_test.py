# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 18:36:02 2025

@author: mens
"""

from LaserCAD.moduls.delay_stage import Delay_Stage
from LaserCAD import Composition
from LaserCAD import clear_doc, setview, freecad_da

if freecad_da:
  clear_doc()

comp = Composition(name="2DelyStage")

comp.propagate(180)

delsta = Delay_Stage(name="1stStage", path_length=320, left_turn=False,
                 xstage_distance = 38)

comp.add_supcomposition_on_axis(delsta)
comp.recompute_optical_axis()


comp.propagate(120)

delay2 = Delay_Stage(name="2ndStage", path_length=250, left_turn=True,
                     xstage_distance=45)

comp.add_supcomposition_on_axis(delay2)
comp.recompute_optical_axis()

comp.propagate(270)

comp.draw()

if freecad_da:
  setview()