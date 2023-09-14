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
DEFAULT_COLOR_LENS = (0/84,0/255,255/255)

import csv
if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Mesh
  import ImportGui
  import Part
  import Sketcher
  from math import pi


def model_crystal(name="crystal", width=50, height=10, thickness=25, geom=None, 
                  color=DEFAULT_COLOR_LENS, **kwargs):

  DOC = get_DOC()

  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  sketch.Support = (DOC.getObject('YZ_Plane'),[''])
  sketch.MapMode = 'FlatFace'
  
  geoList = []
  geoList.append(Part.LineSegment(Vector(-width/2,height/2,0),Vector(width/2,height/2,0)))
  geoList.append(Part.LineSegment(Vector(width/2,height/2,0),Vector(width/2,-height/2,0)))
  geoList.append(Part.LineSegment(Vector(width/2,-height/2,0),Vector(-width/2,-height/2,0)))
  geoList.append(Part.LineSegment(Vector(-width/2,-height/2,0),Vector(-width/2,height/2,0)))
  sketch.addGeometry(geoList,False)
  conList = []
  conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
  conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
  conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
  conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
  conList.append(Sketcher.Constraint('Horizontal',0))
  conList.append(Sketcher.Constraint('Horizontal',2))
  conList.append(Sketcher.Constraint('Vertical',1))
  conList.append(Sketcher.Constraint('Vertical',3))
  sketch.addConstraint(conList)
  del geoList, conList
  sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,width))
  sketch.addConstraint(Sketcher.Constraint('DistanceY',1,2,1,1,height)) 
  sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,height/2))
  sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,width/2)) 
  
  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = thickness
  pad.ReferenceAxis = (sketch,['N_Axis'])
  sketch.Visibility = False
  
  obj.ViewObject.ShapeColor = color
  obj.ViewObject.Transparency = 50
  update_geom_info(obj, geom)
  DOC.recompute()

  return obj

# Test
if __name__ == "__main__":
  from utils import start_DOC
  DOC = None
  start_DOC(DOC)
  model_crystal()