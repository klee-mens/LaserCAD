# -*- coding: utf-8 -*-
"""
Created on Thu May 11 12:30:15 2023

@author: 12816
"""

import sys
sys.path.append(u'/home/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models')
sys.path.append(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models")

# from .utils import freecad_da, update_geom_info
from .utils import freecad_da, update_geom_info, get_DOC
import numpy as np
from .freecad_model_beam import DEFAULT_COLOR_CRIMSON
# from .freecad_model_lens import DEFAULT_COLOR_CRIMSON
if freecad_da:
  import FreeCAD
  import Import
  from FreeCAD import Vector
  import Part
  import Sketcher
  # import Gui
  import App
  # import runCommand
  # import Selection
  import Mesh
  import ImportGui
Beam_Color = DEFAULT_COLOR_CRIMSON
def input_output_test():
  DOC=get_DOC()
  ImportGui.insert(u"C:/Users/12816/Desktop/telescope/Teleskop_beams.step","labor_116")
  obj = DOC.getObject("Feature")
  obj.ViewObject.ShapeColor = Beam_Color
  obj.ViewObject.Transparency = 50
  ImportGui.insert(u"C:/Users/12816/Desktop/telescope/Teleskop_elements.step","labor_116")
  obj = DOC.getObject("Feature001")
  obj.ViewObject.ShapeColor = (0.0, 0.32 , 0.0)
  obj.ViewObject.Transparency = 50
  ImportGui.insert(u"C:/Users/12816/Desktop/telescope/Teleskop_mounts.step","labor_116")
  return 1
