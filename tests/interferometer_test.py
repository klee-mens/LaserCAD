#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 11:25:25 2025

@author: clemens
"""

from LaserCAD import freecad_da, clear_doc
from LaserCAD.moduls.interferometer import Make_Michelson_Interferometer
from LaserCAD.moduls.interferometer import Make_Machzehnder_Interferometer

if freecad_da:
  clear_doc()


mi = Make_Michelson_Interferometer()
mi.draw()


mz_new = Make_Machzehnder_Interferometer()
mz_new.pos = (300, 100, 90)
mz_new.draw()