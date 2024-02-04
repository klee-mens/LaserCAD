#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 19:55:00 2022

@author: mens
"""
import sys
# sys.path.append(u'/home/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models')
# sys.path.append(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models")

# from .utils import freecad_da, update_geom_info
from .utils import freecad_da, update_geom_info, get_DOC, thisfolder#, inch
from .freecad_model_composition import initialize_composition_old, add_to_composition
import numpy as np
#import math

DEFALUT_MAX_ANGULAR_OFFSET = 10
DEFAULT_COLOR_LENS = (0/255,170/255,124/255)
# LENS_TRANSPARENCY = 50
LENS_TRANSPARENCY = 0

import csv
if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Mesh
  import ImportGui
  import Part
  import Sketcher
  from math import pi


def model_lens(name="lens", dia=25, Radius1=300, Radius2=0, thickness=3, geom=None, **kwargs):
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

  obj.ViewObject.ShapeColor = DEFAULT_COLOR_LENS
  obj.ViewObject.Transparency = LENS_TRANSPARENCY
  update_geom_info(obj, geom)
  #DOC.recompute()

  return obj
"""

def lens_mount(mount_name="mirror_mount", dia=inch,  geom=None,
                mount_type="DEFAULT", mesh=True, **kwargs):
  
  
  if dia <= 0.51*inch:
    kind = "MLH05_M"
    offset = Vector(1,-9.5,-8.2)
    place = Placement(offset, Rotation(Vector(-0.57735,0.57735,0.57735),240), Vector(0,0,0))
  elif dia <= 1.01*inch:
    kind = "LMR1_M"
    offset = Vector(1,-9.5,-8.2)
    place = Placement(offset, Rotation(Vector(-0.57735,0.57735,0.57735),240), Vector(0,0,0))
  elif dia <= 1.51*inch:
    kind = "LMR1.5_M"
    offset = Vector(1,-9.5,-8.2)
    place = Placement(offset, Rotation(Vector(-0.57735,0.57735,0.57735),240), Vector(0,0,0))
  elif dia <= 2.01*inch:
    kind = "LMR2_M"
    offset = Vector(13,-31.2,32.4)
    place = Placement(offset, Rotation(-90,2.22639e-14,90), Vector(0,0,0))
  
  if not mount_type == "DEFAULT":
    kind = mount_type #kind kann auf expliziten Wunsch überschireben werden
    offset = Vector(13,-31.2,112.5)
    place = Placement(offset, Rotation(-90,2.22639e-14,90), Vector(0,0,0))
    
  # if kind == "LMR2_M":
  datei = thisfolder + "mount_meshes/lens/" + kind
  if mesh:
    DOC = get_DOC()
    obj = DOC.addObject("Mesh::Feature", mount_name)
    datei += ".stl"
    # obj.Mesh = Mesh.Mesh("/home/mens/projects/optics-workbench/basic_optics/freecad_models/mount_meshes/POLARIS-K1-Step.stl")
    obj.Mesh = Mesh.Mesh(datei)
  else:
    datei += ".step"
    # obj = ImportGui.insert(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib/thorlabs/POLARIS-K1-Step.step","labor_116")
    obj = ImportGui.insert(datei, "labor_116")

  obj.Placement = place
  update_geom_info(obj, geom, off0=offset)
  obj.Label = mount_name

  #DOC.recompute()
  return obj

"""

# Test
if __name__ == "__main__":
  from utils import start_DOC
  DOC = None
  start_DOC(DOC)
  model_lens()