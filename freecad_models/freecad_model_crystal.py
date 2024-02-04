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
from .freecad_model_lens import model_lens
from .freecad_model_mounts import draw_post_part
import numpy as np
#import math

DEFALUT_MAX_ANGULAR_OFFSET = 10
DEFAULT_COLOR_LENS = (0/84,0/255,255/255)
DEFAULT_COLOR_CRYSTAL = (131/255,27/255,44/255)
DEFALUT_MOUNT_COLOR = (207/255,138/255,0/255)
import csv
if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Mesh
  import ImportGui
  import Part
  import Sketcher



def model_crystal(name="crystal",model="cube", width=50, height=10, thickness=25, color=DEFAULT_COLOR_CRYSTAL,Transparency=50, geom=None, **kwargs):
  """
  Parameters
  ----------
  name : string, optional
    crystal name. The default is "crystal".
  model : string, optional
    The model of crystal. It can be "cube" or "round" for cubic crystal and 
    circular crystal. The default is "cube".
  width : float, optional
    The width or radius of the crystal. The default is 50.
  height : float, optional
    The height of the crystal (cube only). The default is 10.
  thickness : float, optional
    The thickness of the crystal. The default is 25.
  color : TYPE, optional
    The color of the crystal. The default is DEFAULT_COLOR_CRYSTAL.
  Transparency : float, optional
    The Transparency of the crystal. The default is 50.
  geom : TYPE, optional
    DESCRIPTION. The default is None.
  **kwargs : TYPE
    DESCRIPTION.

  Returns
  -------
  obj : TYPE
    DESCRIPTION.

  """
  DOC = get_DOC()
  if model== "round":
    obj = model_lens(name, dia=width, Radius1=0, Radius2=0, thickness=thickness)
    obj.ViewObject.ShapeColor = color
    obj.ViewObject.Transparency = Transparency
    update_geom_info(obj, geom)
    #DOC.recompute()
    return obj
  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
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
  obj.ViewObject.Transparency = Transparency
  obj.Placement=Placement(Vector(0,0,0), Rotation(90,0,90), Vector(0,0,0))
  
  update_geom_info(obj, geom)
  #DOC.recompute()

  return obj

def model_crystal_mount(name="crystal_mount",model="cube", width=50, height=10, thickness=25, geom=None, **kwargs):
  """
  Parameters
  ----------
  name : string, optional
    crystal name. The default is "crystal".
  model : string, optional
    The model of crystal. It can be "cube" or "round" for cubic crystal and 
    circular crystal. The default is "cube".
  width : float, optional
    The width or radius of the crystal. The default is 50.
  height : float, optional
    The height of the crystal (cube only). The default is 10.
  thickness : float, optional
    The thickness of the crystal. The default is 25.
  geom : TYPE, optional
    DESCRIPTION. The default is None.
  **kwargs : TYPE
    DESCRIPTION.

  Returns
  -------
  obj : TYPE
    DESCRIPTION.

  """
  DOC = get_DOC()
  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  sketch.MapMode = 'FlatFace'
  if model== "cube":
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
    geoList = []
    geoList.append(Part.LineSegment(Vector(-20,20,0),Vector(20,20,0)))
    geoList.append(Part.LineSegment(Vector(20,20,0),Vector(20,-20,0)))
    geoList.append(Part.LineSegment(Vector(20,-20,0),Vector(-20,-20,0)))
    geoList.append(Part.LineSegment(Vector(-20,-20,0),Vector(-20,20,0)))
    sketch.addGeometry(geoList,False)
    conList = []
    conList.append(Sketcher.Constraint('Coincident',4,2,5,1))
    conList.append(Sketcher.Constraint('Coincident',5,2,6,1))
    conList.append(Sketcher.Constraint('Coincident',6,2,7,1))
    conList.append(Sketcher.Constraint('Coincident',7,2,4,1))
    conList.append(Sketcher.Constraint('Horizontal',4))
    conList.append(Sketcher.Constraint('Horizontal',6))
    conList.append(Sketcher.Constraint('Vertical',5))
    conList.append(Sketcher.Constraint('Vertical',7))
    sketch.addConstraint(conList)
    del geoList, conList
    sketch.addConstraint(Sketcher.Constraint('DistanceX',4,1,4,2,40))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',5,2,5,1,40)) 
    sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,4,2,20))
    sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,4,2,20)) 
  else:
    sketch.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),width/2),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
    sketch.addConstraint(Sketcher.Constraint('Diameter',0,width)) 
    geoList = []
    geoList.append(Part.LineSegment(Vector(-20,20,0),Vector(20,20,0)))
    geoList.append(Part.LineSegment(Vector(20,20,0),Vector(20,-20,0)))
    geoList.append(Part.LineSegment(Vector(20,-20,0),Vector(-20,-20,0)))
    geoList.append(Part.LineSegment(Vector(-20,-20,0),Vector(-20,20,0)))
    sketch.addGeometry(geoList,False)
    conList = []
    conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
    conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
    conList.append(Sketcher.Constraint('Coincident',3,2,4,1))
    conList.append(Sketcher.Constraint('Coincident',4,2,1,1))
    conList.append(Sketcher.Constraint('Horizontal',1))
    conList.append(Sketcher.Constraint('Horizontal',3))
    conList.append(Sketcher.Constraint('Vertical',2))
    conList.append(Sketcher.Constraint('Vertical',4))
    sketch.addConstraint(conList)
    del geoList, conList
    sketch.addConstraint(Sketcher.Constraint('DistanceX',1,1,1,2,40))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',2,2,2,1,40)) 
    sketch.addConstraint(Sketcher.Constraint('DistanceY',0,3,1,2,20))
    sketch.addConstraint(Sketcher.Constraint('DistanceX',0,3,1,2,20)) 
  
  
  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = thickness + 2
  pad.ReferenceAxis = (sketch,['N_Axis'])
  sketch.Visibility = False
  
  #DOC.recompute()
  sketch001 = obj.newObject('Sketcher::SketchObject', name+'_sketch001')
  sketch001.Support = (pad,['Face3',])
  sketch001.MapMode = 'FlatFace'
  
  sketch001.addGeometry(Part.Circle(Vector(0,(thickness + 2)/2,0),Vector(0,0,1),2),
                        False)
  sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-2)) 
  sketch001.addConstraint(Sketcher.Constraint('Diameter',0,2*2)) 
  sketch001.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,(thickness + 2)/2)) 
  
  Pocket = obj.newObject('PartDesign::Pocket','Pocket')
  Pocket.Profile = sketch001
  Pocket.Length = 10
  Pocket.ReferenceAxis = (sketch001,['N_Axis'])
  sketch001.Visibility = False
  
  obj.ViewObject.ShapeColor = DEFALUT_MOUNT_COLOR
  obj.ViewObject.Transparency = 0
  obj.Placement=Placement(Vector(0,0,0), Rotation(90,0,90), Vector(0,0,0))
  update_geom_info(obj, geom)
  #DOC.recompute()
  post_part=draw_post_part(name="post_part",
                           height=20,xshift=(thickness + 2)/2, geom=geom)
  part = initialize_composition_old(name="mount, post and base")
  container = post_part,obj
  add_to_composition(part, container)
  return part

# Test
if __name__ == "__main__":
  from utils import start_DOC
  DOC = None
  start_DOC(DOC)
  model_crystal()