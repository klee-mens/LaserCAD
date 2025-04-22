#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 10:45:09 2025

@author: mens
"""
from LaserCAD.freecad_models.utils import freecad_da, update_geom_info, get_DOC
# from .utils import freecad_da, update_geom_info, get_DOC
#import math

# DEFALUT_MAX_ANGULAR_OFFSET = 10
DEFAULT_COLOR_OAP = (100/255,50/255,150/255)
# LENS_TRANSPARENCY = 50
# LENS_TRANSPARENCY = 0

if freecad_da:
  from FreeCAD import Vector, Rotation, Placement
  from BOPTools import BOPFeatures
  import Part
  import Sketcher
  # from math import pi
  
  
def model_off_axis_parabola(name="off_axis_parab", parent_pos=(25, 50), 
                            parent_focal=25, dia=25, thickness=30, 
                            geom=None, **kwargs):
  
  # parent_pos = (50, 100)
  # parent_focal = 50
  # thickness = 31.7
  # dia = 25.4

  parent_curvature = 1/4 / parent_focal
  cylinder_shift = parent_curvature * (dia*abs(parent_pos[1]) + dia**2/4)
  # cylinder_shift = parent_curvature * (abs(parent_pos[1]))

  DOC = get_DOC()  

  rotparab = DOC.addObject('PartDesign::Body','Body')
  rotparab.Label = 'Body'
  
  sketch = rotparab.newObject('Sketcher::SketchObject','Sketch')
  sketch.AttachmentSupport = (DOC.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'
  sketch.addGeometry(Part.ArcOfParabola(Part.Parabola(Vector(-22.913216,14.395430,0),Vector(25.979458,23.765106,0),Vector(0,0,1)),10.950560,53.375814),False)
  sketch.exposeInternalGeometry(0)
  sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,25.979458))
  # sketch.setDatum(2,App.Units.Quantity('22.000000 mm'))
  sketch.setDatum(2, parent_pos[0])
  sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,23.831428))
  sketch.setDatum(3, parent_pos[1])
  sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,1,18.190452))
  sketch.setDatum(4, parent_pos[1])
  sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,1,21.193090))
  sketch.setDatum(5, parent_pos[0])
  sketch.addConstraint(Sketcher.Constraint('DistanceX',1,1,0,1,44.905686))
  sketch.setDatum(6, parent_focal)
  sketch.addConstraint(Sketcher.Constraint('DistanceX',0,2,0,1,17.816621))
  sketch.setDatum(7, thickness + parent_pos[1] + 20)
  sketch.addGeometry(Part.LineSegment(Vector(-67.803955,-79.955521,0),Vector(-98.153954,13.950961,0)),False)
  sketch.addGeometry(Part.LineSegment(Vector(-98.153954,13.950961,0),Vector(-11.745703,18.949785,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
  sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,0,1))
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,0,2))
  sketch.addConstraint(Sketcher.Constraint('Horizontal',4))
  sketch.addConstraint(Sketcher.Constraint('Vertical',3))

  ### Begin command PartDesign_Revolution
  revol = rotparab.newObject('PartDesign::Revolution','Revolution')
  revol.Profile = (sketch, ['',])

  revol.Angle = 360.000000
  revol.ReferenceAxis = (sketch, ['Edge3'])
  revol.Midplane = 0
  revol.Reversed = 0
  revol.Type = 0
  revol.UpToFace = None

  sketch.Visibility = False

  cyl = DOC.addObject("Part::Cylinder","Cylinder")
  cyl.Label = "Cylinder"
  cyl.Placement=Placement(Vector(-cylinder_shift,0,0), Rotation(0,90,0), Vector(0,0,0))
  cyl.Radius = dia / 2
  # cyl.Height = thickness + 10
  cyl.Height = thickness

  bp = BOPFeatures.BOPFeatures(DOC)
  offaxisparab = bp.make_cut(["Cylinder", "Body", ])
  offaxisparab.ViewObject.ShapeColor = DEFAULT_COLOR_OAP
  update_geom_info(offaxisparab, geom)
  # DOC.recompute()
  
  return offaxisparab



# oap = model_off_axis_parabola()