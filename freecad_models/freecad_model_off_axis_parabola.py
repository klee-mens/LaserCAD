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
# DEFAULT_COLOR_OAP = (100/255,50/255,150/255)
DEFAULT_COLOR_OAP = (92/255,79/255,79/255)
# LENS_TRANSPARENCY = 50
# LENS_TRANSPARENCY = 0

if freecad_da:
  from FreeCAD import Vector
  # import MeshPart
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

  revol_body = DOC.addObject('PartDesign::Body','Body')
  revol_body.Label = 'revobody'

  sketch = revol_body.newObject('Sketcher::SketchObject','Sketch')
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
  revol = revol_body.newObject('PartDesign::Revolution','Revolution')
  revol.Profile = (sketch, ['',])

  revol.Angle = 360.000000
  revol.ReferenceAxis = (sketch, ['Edge3'])
  revol.Midplane = 0
  revol.Reversed = 0
  revol.Type = 0
  revol.UpToFace = None

  sketch.Visibility = False
  DOC.recompute()


  ### Begin command PartDesign_Body
  offaxisparab = DOC.addObject('PartDesign::Body','Body001')
  offaxisparab.Label = 'OAPBody'
  # Gui.Selection.addSelection('labor_116','Body001','Origin001.YZ_Plane001.')
  oap_sketch = offaxisparab.newObject('Sketcher::SketchObject','Sketch001')
  oap_sketch.AttachmentSupport = (DOC.getObject('YZ_Plane001'),[''])
  oap_sketch.MapMode = 'FlatFace'

  geoList = []
  geoList.append(Part.Circle(Vector(0.000000, 0.000000, 0.000000), Vector(0.000000, 0.000000, 1.000000), 30.658336))
  oap_sketch.addGeometry(geoList,False)
  del geoList

  # constraintList = []
  oap_sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))


  oap_sketch.addConstraint(Sketcher.Constraint('Diameter',0,61.316672))
  # oap_sketch.setDatum(1,App.Units.Quantity('25.000000 mm'))
  oap_sketch.setDatum(1, dia)

  ### Begin command PartDesign_Pad
  oappad = offaxisparab.newObject('PartDesign::Pad','Pad')
  oappad.Profile = (oap_sketch, ['',])

  oappad.Length = (thickness - cylinder_shift) * 2
  oappad.TaperAngle = 0.000000
  oappad.UseCustomVector = 0
  oappad.Direction = (1, 0, 0)
  oappad.ReferenceAxis = (oap_sketch, ['N_Axis'])
  oappad.AlongSketchNormal = 1
  oappad.Type = 0
  oappad.UpToFace = None
  oappad.Reversed = 0
  oappad.Midplane = 1
  oappad.Offset = 0
  oap_sketch.Visibility = False
  ### Begin command PartDesign_Boolean
  # DOC.recompute()

  diff = offaxisparab.newObject('PartDesign::Boolean','Boolean')
  diff.setObjects( [revol_body,])
  diff.Type = 1
  # DOC.recompute()

  # oap_mesh = DOC.addObject("Mesh::Feature", "Mesh")
  # oap_mesh.Mesh = MeshPart.meshFromShape(Shape=offaxisparab.Shape, LinearDeflection=0.05, AngularDeflection=0.0872665, Relative=False)
  # oap_mesh.Label = "OAPMesh"

  # DOC.recompute()
  update_geom_info(offaxisparab, geom)
  # update_geom_info(oap_mesh, geom)

  if "color" in kwargs.keys():
    offaxisparab.ViewObject.ShapeColor = kwargs["color"]
  else:
    offaxisparab.ViewObject.ShapeColor = DEFAULT_COLOR_OAP
  # if "color" in kwargs.keys():
  #   oap_mesh.ViewObject.ShapeColor = kwargs["color"]
  # else:
  #   # offaxisparab.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
  #   oap_mesh.ViewObject.ShapeColor = DEFAULT_COLOR_OAP
  # DOC.recompute()

  return offaxisparab

