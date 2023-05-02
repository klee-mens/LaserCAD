#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 18:30:44 2022

@author: mens
"""


from .utils import freecad_da, update_geom_info, get_DOC, GEOM0
# from .utils import freecad_da, update_geom_info, DOC_NAME
if freecad_da:
  import FreeCAD
  from FreeCAD import Vector
  import Part


RAY_RADIUS = 0.05 #in mm, also 50 um
# RAY_COLOR = (0.67, 0.0, 0.5) #rot-violettt
# RAY_COLOR = (170/255, 0.0, 0.0) #dunkelrot
RAY_COLOR = (200/255, 200/255, 0.0) #gelb

def model_ray_cylinder(name="ray", length=200, geom=GEOM0):
  """
  kreiert aus geom und length einen zylinderförmigen Strahl

  Parameters
  ----------
  name : TYPE, optional
    DESCRIPTION. The default is "ray".
  length : TYPE, optional
    DESCRIPTION. The default is 200.
  geom : TYPE, optional
    DESCRIPTION. The default is GEOM0.

  Returns
  -------
  obj : TYPE
    DESCRIPTION.

  """
  DOC = get_DOC()
  obj = DOC.addObject("Part::Cylinder",name)
  obj.Label = name
  obj.Radius = RAY_RADIUS
  obj.Height = length
  obj.ViewObject.ShapeColor = (0.67,0.00,0.50)
  
  obj.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(Vector(0,1,0),90), Vector(0,0,0))
  update_geom_info(obj, geom)
  #DOC.recompute()
  return obj


def model_ray_1D(name="ray1D", length=200, geom=GEOM0, color=RAY_COLOR):
  """
  kreiert aus geom und length einen 1D-Edge Strahl

  Parameters
  ----------
  name : TYPE, optional
    DESCRIPTION. The default is "ray1D".
  length : TYPE, optional
    DESCRIPTION. The default is 200.
  geom : TYPE, optional
    DESCRIPTION. The default is GEOM0.

  Returns
  -------
  None.

  """
  if length == 0:
    length=3 #3mm Ray, nur für den Fehler zu vermeiden falls length=0
  pos, axes = geom
  normal = axes[:,0]
  DOC = get_DOC()
  p1 = Vector(pos)
  p2 = Vector(pos + length*normal)
  l1 = Part.LineSegment(p1, p2)
  s1 = l1.toShape()
  obj = DOC.addObject("Part::Feature", name)
  obj.Shape = s1
  obj.ViewObject.LineColor = color
  
  #DOC.recompute()
  return obj
  


# Test
if __name__ == "__main__":
  from utils import start_DOC
  DOC = None
  start_DOC(DOC)
  model_ray_1D()
  model_ray_cylinder()