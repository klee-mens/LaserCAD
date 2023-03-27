#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 01:31:42 2022

@author: mens
"""

import sys
sys.path.append(u'/home/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models')
sys.path.append(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models")

# from .utils import freecad_da, update_geom_info
from .utils import freecad_da, update_geom_info, get_DOC
if freecad_da:
  import FreeCAD
  from FreeCAD import Vector
  import Part


def model_beam(name="beam", dia=10, prop=200,  f=130, clr="crimson", geom_info=None):
  """creates a red beam with length <prop>, diameter <dia>,
  fokus <f> and name ~
  example :  beam1 = model_beam("laser1", 10, 200, 100)
  beam1 = model_beam(name="laser1", dia=10, prop=200, f=-45)
  """
  DOC = get_DOC()
  if f==0 or abs(f) > 1e4:
    # wenn die Brennweite unendlich oder zu groß (10m) ist
     obj = DOC.addObject("Part::Cylinder", name)
     obj.Height = prop
     obj.Radius = dia/2
  elif prop < f or f < 0:
    # only one cone
    dia2 = dia * (f-prop)/f
    obj = DOC.addObject("Part::Cone", name)
    obj.Height = prop
    obj.Radius1 = dia/2
    obj.Radius2 = dia2/2
  else:
    dia2 = 0 #1 altern
    obj1 = DOC.addObject("Part::Cone", name+"_1")
    obj1.Height = f
    obj1.Radius1 = dia/2
    obj1.Radius2 = dia2/2

    dia3 = dia * (prop-f)/f
    obj2 = DOC.addObject("Part::Cone", name+"_2")
    obj2.Height = prop-f
    obj2.Radius1 = dia2/2
    obj2.Radius2 = dia3/2
    obj2.Placement = FreeCAD.Placement(Vector(0,0,f), FreeCAD.Rotation(Vector(0,1,0),0), Vector(0,0,0))
    obj = DOC.addObject("Part::Fuse", name)
    obj.Base = obj1
    obj.Tool = obj2
    obj.Refine = True
    DOC.recompute()

  obj.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(Vector(0,1,0),90), Vector(0,0,0))
  obj.ViewObject.ShapeColor = (0.86,0.08,0.24)
  obj.ViewObject.Transparency = 50
  obj.Label = name
  update_geom_info(obj, geom_info)

  DOC.recompute()
  return obj


# Test
if __name__ == "__main__":
  from utils import start_DOC
  DOC = None
  start_DOC(DOC)
  model_beam()