# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:33:37 2023

@author: He
"""

import sys
# sys.path.append(u'/home/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models')
# sys.path.append(u"C:/Users/mens/Nextcloud/FreeCAD/opticslib2/basic_objects/freecad_models")

# from .utils import freecad_da, update_geom_info
from .utils import freecad_da, update_geom_info, get_DOC, thisfolder#, inch
from .freecad_model_composition import initialize_composition_old, add_to_composition
from .freecad_model_mounts import draw_post_part
import numpy as np
#import math

DEFALUT_MAX_ANGULAR_OFFSET = 10

import csv
if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Mesh
  import ImportGui
  import Part
  import Sketcher
  from math import pi
  

def model_intersection_plane(name="intersection_plane", Radius=25, geom=None, **kwargs):
  """
    Build a model to mark the intersection plane

    Parameters
    ----------
    name : String, optional
        The name of the model. The default is "intersection_plane".
    Radius : float/int, optional
        Radius of the plane. The default is 25.
    geom : TYPE, optional
        geom info of the intersection plane. The default is None.
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
  sketch.addGeometry(Part.Circle(Vector(0.0,0.0,0),Vector(0,0,1),Radius*2),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
  sketch.addConstraint(Sketcher.Constraint('Diameter',0,Radius*2)) 
    
  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = 0.1
  pad.ReferenceAxis = (sketch,['N_Axis'])
  pad.Midplane = 1
  sketch.Visibility = False
  
  if "color" in kwargs.keys():
    obj.ViewObject.ShapeColor = kwargs["color"]
  else:
    # obj.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
    obj.ViewObject.ShapeColor = (240/255, 240/255, 240/255)
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = 80
  obj.Placement=Placement(Vector(0,0,0), Rotation(90,0,90), Vector(0,0,0))
  update_geom_info(obj, geom)
  
  DOC.recompute()
  return obj
  
def model_diaphragms(name="diaphragms", Radius=25,Hole_Radius=2, thickness=5,height=20, geom=None, **kwargs):
  """
    Draw a diaphragms

    Parameters
    ----------
    name : TYPE, optional
        diaphragms name. The default is "diaphragms".
    Radius : TYPE, optional
        The radius of the diaphragm. The default is 25.
    Hole_Radius : TYPE, optional
        radious of the fixed hole at the button of the diaphragm. 
        The default is 2.
    thickness : TYPE, optional
        The thickness of the diaphragm. The default is 3.
    height : TYPE, optional
        The height from the center to the button of the diaphragm. The default is 20.
    geom : TYPE, optional
        geom info. The default is None.
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
  sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(0,0,0),Vector(0,0,1),Radius),0,np.pi),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-1)) 
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-1)) 
  
  sketch.addGeometry(Part.LineSegment(Vector(-Radius,0,0),Vector(-Radius,-height,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,2))
  sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
  
  sketch.addGeometry(Part.LineSegment(Vector(-Radius,-height,0),Vector(Radius,-height,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Horizontal',2)) 
  
  sketch.addGeometry(Part.LineSegment(Vector(Radius,-height,0),Vector(Radius,0,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,2,2))
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
  sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
  
  sketch.addConstraint(Sketcher.Constraint('DistanceY',3,1,3,2,height)) 
  sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2)) 
  sketch.addConstraint(Sketcher.Constraint('DistanceX',2,1,2,2,Radius*2)) 
  
  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = thickness
  pad.ReferenceAxis = (sketch,['N_Axis'])
  pad.Midplane = 1
  sketch.Visibility = False
  
  DOC.recompute()
  sketch001 = obj.newObject('Sketcher::SketchObject', name+'_sketch001')
  sketch001.Support = (pad,['Face3',])
  sketch001.MapMode = 'FlatFace'
  
  sketch001.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),Hole_Radius),False)
  sketch001.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1))
  sketch001.addConstraint(Sketcher.Constraint('Diameter',0,Hole_Radius*2)) 
  
  Pocket = obj.newObject('PartDesign::Pocket','Pocket')
  Pocket.Profile = sketch001
  Pocket.Length = 10
  Pocket.ReferenceAxis = (sketch001,['N_Axis'])
  sketch001.Visibility = False
  if "color" in kwargs.keys():
    obj.ViewObject.ShapeColor = kwargs["color"]
  else:
    # obj.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
    obj.ViewObject.ShapeColor = (220/255, 220/255, 220/255)
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = 0
  obj.Placement=Placement(Vector(0,0,0), Rotation(90,0,90), Vector(0,0,0))
  update_geom_info(obj, geom)
  
  DOC.recompute()
  return obj

def model_iris_diaphragms(name="iris", Radius1=10, Radius2=25,Hole_Radius=2, thickness=5,height=20, geom=None, **kwargs):
  """
    Draw a iris diaphragms (dosn't work for now')

    Parameters
    ----------
    name : TYPE, optional
        DESCRIPTION. The default is "iris".
    Radius1 : TYPE, optional
        DESCRIPTION. The default is 10.
    Radius2 : TYPE, optional
        DESCRIPTION. The default is 25.
    Hole_Radius : TYPE, optional
        DESCRIPTION. The default is 2.
    thickness : TYPE, optional
        DESCRIPTION. The default is 3.
    height : TYPE, optional
        DESCRIPTION. The default is 20.
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
  #sketch.Support = (DOC.getObject('YZ_Plane001'),[''])
  sketch.MapMode = 'FlatFace'
  if abs(Radius1)>0:
    sketch.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),abs(Radius1)),
                     False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1))
    sketch.addConstraint(Sketcher.Constraint('Diameter',0,Radius1*2)) 
  
  sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(0,0,0),Vector(0,0,1),
                                                  Radius2),0,pi),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',1,3,0,3)) 
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,1,-1)) 
  sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-1))
  sketch.addConstraint(Sketcher.Constraint('Radius',1,Radius2)) 
  sketch.addGeometry(Part.LineSegment(Vector(-Radius2,0,0),
                                      Vector(-Radius2,-height,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2)) 
  sketch.addConstraint(Sketcher.Constraint('Vertical',2)) 
  sketch.addGeometry(Part.LineSegment(Vector(Radius2,0,0),
                                      Vector(Radius2,-height,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,1,1)) 
  sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
  sketch.addGeometry(Part.LineSegment(Vector(-Radius2,-height,0),
                                      Vector(Radius2,-height,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',4,1,2,2)) 
  sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,3,2)) 
  sketch.addConstraint(Sketcher.Constraint('Horizontal',4)) 
  sketch.addConstraint(Sketcher.Constraint('DistanceY',3,2,3,1,height)) 
  
  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = thickness
  pad.ReferenceAxis = (sketch,['N_Axis'])
  pad.Midplane = 1
  sketch.Visibility = False
  
  
  DOC.recompute()
  sketch001 = obj.newObject('Sketcher::SketchObject', name+'_sketch001')
  sketch001.Support = (pad,['Face3',])
  sketch001.MapMode = 'FlatFace'
  
  sketch001.addGeometry(Part.Circle(Vector(0,0,0),Vector(0,0,1),Hole_Radius),False)
  sketch001.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1))
  sketch001.addConstraint(Sketcher.Constraint('Diameter',0,Hole_Radius*2)) 
  
  Pocket = obj.newObject('PartDesign::Pocket','Pocket')
  Pocket.Profile = sketch001
  Pocket.Length = 10
  Pocket.ReferenceAxis = (sketch001,['N_Axis'])
  sketch001.Visibility = False

  obj.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = 0
  obj.Placement=Placement(Vector(0,0,0), Rotation(90,0,90), Vector(0,0,0))
  update_geom_info(obj, geom)
  
  DOC.recompute()
  return obj

def iris_post(height=20,geom = None, **kwargs):
  """
    draw the post

    Parameters
    ----------
    geom : TYPE, optional
        DESCRIPTION. The default is None.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
  xshift = 0
  return draw_post_part(name="post_part", height=height,xshift=xshift, geom=geom)