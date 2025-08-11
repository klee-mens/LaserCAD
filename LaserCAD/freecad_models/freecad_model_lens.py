#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 19:55:00 2022

@author: mens
"""

from .utils import freecad_da, update_geom_info, get_DOC
#import math

DEFALUT_MAX_ANGULAR_OFFSET = 10
DEFAULT_COLOR_LENS = (0/255,170/255,124/255)
LENS_TRANSPARENCY = 50
# LENS_TRANSPARENCY = 0

if freecad_da:
  from FreeCAD import Vector
  import Part
  import Sketcher
  from math import pi


def model_lens(name="lens", dia=25, Radius1=300, Radius2=0, thickness=3, 
               color=DEFAULT_COLOR_LENS, transparency=LENS_TRANSPARENCY,
               geom=None, **kwargs):
  """
    Build a lens.

    Parameters
    ----------
    name : String, optional
        The name of the lens. The default is "lens".
    dia : float/int, optional
        The diameter of the lens. The default is 25.
    Radius1 : float/int, optional
        The curvature of the first serface. The default is 300.
    Radius2 : float/int, optional
        The curvature of the second serface. The default is 0.
    Radius = 0 means the flat serface.
    thickness : float/int, optional
        The thickness of the lens. The default is 3.
    geom : TYPE, optional
        geom info. The default is None.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    obj : TYPE
        DESCRIPTION.
    example:
        lens64 = model_lens("Lens64", dia=25.4, Radius1=250, Radius2=500, thickness=3, geom=None)

    """
  DOC = get_DOC()
  """Beispiel
  #lens_1 = model_lens("lens01", 25, 50, 0, 10)
  #lens_1.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(Vector(0,0,1),0), Vector(0,0,0))
  #lens_2 = model_lens("lens02", 25, 0, 150, 5)
  #lens_2.Placement = FreeCAD.Placement(Vector(0,50,0), FreeCAD.Rotation(Vector(0,0,1),0), Vector(0,0,0))
  #lens_3 = model_lens("lens03", 25, 100, -50, 10)
  #lens_3.Placement = FreeCAD.Placement(Vector(0,0,50), FreeCAD.Rotation(Vector(0,0,1),0), Vector(0,0,0))
  #lens_4 = model_lens("lens04", 25, -100, -50, 10)
  #lens_4.Placement = FreeCAD.Placement(Vector(0,50,50), FreeCAD.Rotation(Vector(0,0,1),0), Vector(0,0,0))
  """
  a = 1 if Radius1>0 else 0
  b = 1 if Radius2>=0 else 0

  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  #sketch.Support = (DOC.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'

  sketch.addGeometry(Part.LineSegment(Vector(0,0,0),Vector(thickness,0,0)),
                      False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1))
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-1))
  sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,thickness))

  if Radius1 == 0:
    sketch.addGeometry(Part.LineSegment(Vector(0.0,0.0,0),Vector(0,10,0)),
                        False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-2))
  else:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(Radius1,0,0),
                                        Vector(0,0,1),abs(Radius1)),0.9*a*pi,
                                        0.9*a*pi+0.1*pi),False)
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,3,-1))
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,1+a,0,1))
    sketch.addConstraint(Sketcher.Constraint('Radius',1,abs(Radius1)))

  if Radius2 == 0:
    sketch.addGeometry(Part.LineSegment(Vector(5.0,0.0,0),Vector(5,10,0)),
                        False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,0,2))
    sketch.addConstraint(Sketcher.Constraint('Vertical',2))
  else:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(
                                        Vector(thickness-Radius2,0,0),
                                        Vector(0,0,1),abs(Radius2)),
                                        0.9*pi-0.9*b*pi,pi-0.9*b*pi),False)
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',2,3,-1))
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,2-b,0,2))
    sketch.addConstraint(Sketcher.Constraint('Radius',2,abs(Radius2)))

  sketch.addGeometry(Part.LineSegment(Vector(0,10,0),Vector(10,10,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,1,2-a))
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,2,1+b))
  sketch.addConstraint(Sketcher.Constraint('Horizontal',3))
  sketch.addConstraint(Sketcher.Constraint('DistanceY',0,1,1,2-a,dia/2))

  rev = obj.newObject('PartDesign::Revolution',name+'_Revolution')
  rev.Profile = sketch
  rev.ReferenceAxis = (sketch,['H_Axis'])
  rev.Angle = 360.0
  rev.Reversed = 1
  sketch.Visibility = False

  obj.ViewObject.ShapeColor = color
  obj.ViewObject.Transparency = transparency
  update_geom_info(obj, geom)
  #DOC.recompute()

  return obj


# Test
if __name__ == "__main__":
  from utils import start_DOC
  DOC = None
  start_DOC(DOC)
  model_lens()