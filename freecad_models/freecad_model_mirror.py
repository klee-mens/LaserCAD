# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:28:18 2022

@author: mens
"""


from .utils import freecad_da, update_geom_info, get_DOC, rotate, thisfolder#,translate
from .freecad_model_lens import model_lens
from .freecad_model_composition import initialize_composition_old, add_to_composition
import numpy as np
import csv
import math

if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Mesh
  import ImportGui
  import Sketcher
  import Part
  from math import pi

DEFAULT_COLOR_JOERG = (0.8,0.2,0.8)
DEFAULT_COLOR = (199/255, 144/255, 28/255) #Messing
DEFAULT_TRANSPARENCY = 50
# DEFAULT_TRANSPARENCY = 0
DEFALUT_MAX_ANGULAR_OFFSET = 10


def model_mirror(model_type="DEFAULT", **kwargs):
  """
    bulid a mirror model

    Parameters
    ----------
    model_type : String, optional
        The type of the mirror.
        There are two options, Round mirror(DEFAULT) and Stripe mirror.
        The default is "DEFAULT".
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    obj : TYPE
        object of mirror.
    Example:
    mirror47 = mirror("mirror_47", dia=25, d=5, R=200)
  """
  if model_type == "DEFAULT" or model_type == "Round" or model_type == "polarizer":
    obj = model_round_mirror(**kwargs)
  elif model_type == "Stripe":
    obj = model_stripe_mirror(**kwargs)
  elif model_type == "Rooftop":
    obj = model_rooftop_mirror(**kwargs)
  else:
    obj = model_round_mirror(**kwargs)
  return obj


def model_round_mirror(name="mirror", dia=25, thickness=5, Radius=0, geom=None, **kwargs):
  """
    Build a round mirror model with a certain diameter, thickness and radius

    Parameters
    ----------
    name : String, optional
        The name of the mirror. The default is "mirror".
    dia : float/int, optional
        The diameter of the mirror. The default is 25.
    thickness : float/int, optional
        The thickness of the mirror. The default is 5.
    Radius : float/int, optional
        The curvature of the mirror. 0 means plane mirror. The default is 0.
    geom : TYPE, optional
        The geometrical parameter of the mirror. The default is None.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    obj : TYPE
    object of mirror.

    Example:
    mirror47 = mirror("mirror_47", dia=25, d=5, R=200)
  """
  DOC = get_DOC()
  obj = model_lens(name, dia, Radius1=-Radius, Radius2=0, thickness=thickness)


  if "color" in kwargs.keys():
    obj.ViewObject.ShapeColor = kwargs["color"]
  else:
    obj.ViewObject.ShapeColor = DEFAULT_COLOR
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = DEFAULT_TRANSPARENCY
  update_geom_info(obj, geom)

  DOC = get_DOC()
  #DOC.recompute()
  return obj


def model_stripe_mirror(name="Stripe_Mirror", dia=75, Radius=250, thickness=25,
                        height=10, geom=None, pos=0, axes = "somthing", **kwargs):
  """


    Parameters
    ----------
    name : String, optional
        The name of the mirror. The default is "Stripe_Mirror".
    dia : TYPE, optional
        The width of the mirror. The default is 75.
    Radius : TYPE, optional
        The curvature of the mirror. The default is 250.
    thickness : TYPE, optional
        The thickness of the mirror. The default is 25.
    height : TYPE, optional
        The height of the mirror. The default is 10.
    geom : TYPE, optional
        The geometrical parameter of the mirror. The default is None.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    obj : TYPE
        object of mirror.
   example:
       stripe_mirror=model_stripe_mirror(name="Stripe_Mirror", dia=60,
                                         Radius=300, thickness=30, height=15,
                                         geom=None,)
   """
  DOC = get_DOC()
  """Beispiel
  s.o.
  """

  Radius *= -1
  a = 1 if Radius>0 else -1

  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  #sketch.Support = (DOC.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'
  if a == 1:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(Radius,0,0),Vector(0,0,1),abs(Radius)),0.9*a*pi,0.9*a*pi+0.2*pi),False)
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',-1,1,0))
    sketch.addConstraint(Sketcher.Constraint('Symmetric',0,1,0,2,-1))
    sketch.addConstraint(Sketcher.Constraint('Radius',0,Radius))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',0,2,0,1,dia))
  else:
    sketch.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(Radius,0,0),Vector(0,0,1),abs(Radius)),np.arcsin(dia/(2*-Radius)),-np.arcsin(dia/(2*-Radius))),False)
    sketch.addConstraint(Sketcher.Constraint('DistanceX',0,3,-1,1,-Radius))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,dia/2))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',0,1,-1,1,dia/2))
    sketch.addConstraint(Sketcher.Constraint('Radius',0,-Radius))
  xx = Radius-pow(Radius**2-(dia/2)**2,0.5)
  sketch.addGeometry(Part.LineSegment(Vector(a*xx,dia/2,0.0),Vector(thickness,dia/2,0.0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1))
  sketch.addConstraint(Sketcher.Constraint('Horizontal',1))
  sketch.addGeometry(Part.LineSegment(Vector(thickness,dia/2,0.0),Vector(thickness,-dia/2,0.0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2))
  sketch.addConstraint(Sketcher.Constraint('Vertical',2))
  sketch.addGeometry(Part.LineSegment(Vector(thickness,-dia/2,0),Vector(a*xx,-dia/2,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,2,2))
  sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,2))
  sketch.addConstraint(Sketcher.Constraint('Horizontal',3))
  sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,2,2,thickness))

  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = height
  pad.ReferenceAxis = (sketch,['N_Axis'])
  pad.Midplane = 1
  sketch.Visibility = False
  # print("geom=",geom)
  # obj.Placement = Placement(Vector(0,0,0), Rotation(0,0,90), Vector(0,0,0))

  if "color" in kwargs.keys():
    obj.ViewObject.ShapeColor = kwargs["color"]
  else:
    # obj.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
    obj.ViewObject.ShapeColor = DEFAULT_COLOR
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = DEFAULT_TRANSPARENCY
  update_geom_info(obj, geom)

  DOC = get_DOC()
  #DOC.recompute()

  return obj


def model_rooftop_mirror(name="rooftop_mirror",dia=0, geom=None, **kwargs):
  """
  draw a rooftop mirror

  Parameters
  ----------
  name : TYPE, optional
    mirror name. The default is "rooftop_mirror".
  dia : TYPE, optional
    the periscope distance, which will deside the pos of mirror.
    The default is 0.
  geom : TYPE, optional
    DESCRIPTION. The default is None.
  **kwargs : TYPE
    DESCRIPTION.

  Returns
  -------
  obj : TYPE
    DESCRIPTION.

  example:
      stripe_mirror= model_rooftop_mirror(name="rooftop_mirror",dia=0,
                                          geom=None, **kwargs)
  """

  DOC = get_DOC()
  obj = DOC.addObject('PartDesign::Body', name)
  sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
  # sketch.Support = (DOC.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'

  sketch.addGeometry(Part.LineSegment(Vector(0,0,0),Vector(24.748737,24.748737,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,1))
  sketch.addGeometry(Part.LineSegment(Vector(24.748737,24.748737,0),Vector(24.748737,-24.748737,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1))
  sketch.addConstraint(Sketcher.Constraint('Vertical',1))
  sketch.addGeometry(Part.LineSegment(Vector(24.748737,-24.748737,0),Vector(0,0,0)),False)
  sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1))
  sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,0,1))
  sketch.addConstraint(Sketcher.Constraint('Angle',-1,1,0,1,45/180*np.pi))
  sketch.addConstraint(Sketcher.Constraint('Angle',2,2,-1,1,45/180*np.pi))
  sketch.addConstraint(Sketcher.Constraint('Distance',0,35))


  pad = obj.newObject('PartDesign::Pad','Pad')
  pad.Profile = sketch
  pad.Length = 90
  pad.ReferenceAxis = (sketch,['N_Axis'])
  pad.Midplane = 1
  sketch.Visibility = False

  if "color" in kwargs.keys():
    obj.ViewObject.ShapeColor = kwargs["color"]
  else:
    # obj.ViewObject.ShapeColor = (204/255, 204/255, 204/255)
    obj.ViewObject.ShapeColor = DEFAULT_COLOR
  if "transparency" in kwargs.keys():
    obj.ViewObject.Transparency = kwargs["transparency"]
  else:
    obj.ViewObject.Transparency = DEFAULT_TRANSPARENCY+20
  offset=Vector(dia/2,0,0)
  obj.Placement = Placement(offset, Rotation(0,-180,90), Vector(0,0,0))
  update_geom_info(obj, geom, off0=offset)
  # DOC = get_DOC()
  #DOC.recompute()

  return obj

