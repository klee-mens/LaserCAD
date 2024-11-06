# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:14:09 2024

@author: mens
"""

from LaserCAD.non_interactings import Crystal
from LaserCAD.freecad_models import freecad_da, clear_doc

if freecad_da:
  clear_doc()
  
crys = Crystal(width=7, height=5, thickness=10)
crys.draw()