# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 22:37:04 2024

@author: mens
"""

from LaserCAD.non_interactings import Iris
from LaserCAD.freecad_models import freecad_da, clear_doc
from LaserCAD.freecad_models.freecad_model_iris_diaphragms import model_diaphragms, model_iris_diaphragms

if freecad_da:
  clear_doc()
  # model_diaphragms()
  # model_iris_diaphragms(.)

ir = Iris()
ir.draw()
ir.draw_mount()