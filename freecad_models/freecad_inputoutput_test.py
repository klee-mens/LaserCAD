# -*- coding: utf-8 -*-
"""
Created on Thu May 11 12:30:15 2023

@author: 12816
"""

import sys
# sys.path.append(u'/home/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models')
# sys.path.append(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models")

# from .utils import freecad_da, update_geom_info
from .utils import freecad_da, update_geom_info, get_DOC
import numpy as np
from .freecad_model_composition import initialize_composition_old, add_to_composition
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
  # doc2 = FreeCAD.open('C:/Users/12816/Desktop/fs.FCStd')
  DOC = get_DOC()
  ImportGui.insert(u"C:/Users/12816/Desktop/telescope/Teleskop_beams.step","labor_116")
  obj1 = DOC.getObject("Feature")
  obj1.ViewObject.ShapeColor = Beam_Color
  obj1.ViewObject.Transparency = 50
  ImportGui.insert(u"C:/Users/12816/Desktop/telescope/Teleskop_elements.step","labor_116")
  obj2 = DOC.getObject("Feature001")
  obj2.ViewObject.ShapeColor = (0.0, 0.32 , 0.0)
  obj2.ViewObject.Transparency = 50
  obj3 = DOC.addObject("Mesh::Feature", "Teleskop_mounts")
  obj3.Mesh = Mesh.Mesh(u"C:/Users/12816/Desktop/telescope/TeleskopTeleskop_mounts.stl")
  part = initialize_composition_old(name="Teleskop")
  container = obj1,obj2,obj3
  add_to_composition(part, container)
  # doc1 = FreeCAD.open('C:/Users/12816/Desktop/foldres.FCStd')
  # objects = doc1.Objects
  # # print(objects)
  # # DOC.addObject(str(objects))
  # for obj in objects:
  #   if isinstance(obj, FreeCAD.Part) and obj.Label:
  #       doc2.addObject(str(obj))
  # DOC.recompute()
  return 1
