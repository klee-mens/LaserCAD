#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 11:25:25 2025

@author: clemens
"""

from LaserCAD import freecad_da, clear_doc
from LaserCAD.moduls.interferometer import Make_Michelson_Interferomter
from LaserCAD.moduls.interferometer import Make_Machzehnder_Interferomater

if freecad_da:
  clear_doc()
  
  
mich_arm1, mich_arm2 = Make_Michelson_Interferomter()

mich_arm1.draw()
mich_arm2.draw()


mz_arm1, mz_arm2 = Make_Machzehnder_Interferomater()

