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
import numpy as np
if freecad_da:
  import FreeCAD
  from FreeCAD import Vector
  import Part
  import Sketcher

DEFAULT_COLOR_CRIMSON = (0.86,0.08,0.24) #crimson


def model_beam(name="beam", dia=10, prop=200,  f=130, color=DEFAULT_COLOR_CRIMSON, 
               geom_info=None):
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
  obj.ViewObject.ShapeColor = color
  obj.ViewObject.Transparency = 50
  obj.Label = name
  update_geom_info(obj, geom_info)

  DOC.recompute()
  return obj

def moedel_Gaussian_beam (name="Gaussian_beam",q=-100+200j,prop=200,wavelength=650E-9,
                          color=DEFAULT_COLOR_CRIMSON, geom_info=None):
    """
    creates a Gaussian beam.
    Parameters
    ----------
    name : TYPE, optional
        beam name. The default is "Gaussian_beam".
    q : TYPE, optional
        q-parameter. The default is -100+200j.
    prop : TYPE, optional
        propgation length. The default is 200.
    wavelength : TYPE, optional
        wavelength. The default is 650E-9.
    color : TYPE, optional
        beam color. The default is DEFAULT_COLOR_CRIMSON.
    geom_info : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    obj : TYPE
        DESCRIPTION.
    example: beam1 = model_beam("laser1", -100+200j, 200, 650E-6)
    """
    DOC = get_DOC()
    obj = DOC.addObject('PartDesign::Body', name)
    sketch = obj.newObject('Sketcher::SketchObject', name+'_sketch')
    sketch.Support = (DOC.getObject('XY_Plane'),[''])
    sketch.MapMode = 'FlatFace'
    z0 = np.imag(q)
    z_start=np.real(q)
    z_end = z_start+prop
    w0 = pow(wavelength*z0/np.pi,0.5)
    w_start = w0 * pow(1+(z_start/z0)**2,0.5)
    w_end = w0 * pow(1+(z_end/z0)**2,0.5)
    
    print("z_start:",z_start)
    print("w0:",w0)
    print("w_start:",w_start)
    print("w_end:",w_end)
    sketch.addGeometry(Part.ArcOfHyperbola(Part.Hyperbola(Vector(-z_start,w0,0),Vector(-z_start-w0/2,0,0),Vector(-z_start,0,0)),-1,1),False)
    sketch.exposeInternalGeometry(0)
    
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1))
    
    sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,-z_start))
    sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,0))
    sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,1,prop)) 
    sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,w_start))
    sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,1,w_end)) 
    # sketch.addConstraint(Sketcher.Constraint('Distance',2,1,1,1,z0))
    
    sketch.addGeometry(Part.LineSegment(Vector(0,w_start,0),Vector(0,0,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',4,1,0,2))
    # sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,-1,1))
    sketch.addConstraint(Sketcher.Constraint('Vertical',4))
    
    sketch.addGeometry(Part.LineSegment(Vector(prop,w_end,0),Vector(prop,0,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',5,1,0,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',5,2,-1)) 
    sketch.addConstraint(Sketcher.Constraint('Vertical',5))
    sketch.addGeometry(Part.LineSegment(Vector(0,0,0),Vector(prop,0,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',6,1,4,2))
    sketch.addConstraint(Sketcher.Constraint('Coincident',6,2,5,2))
    sketch.addConstraint(Sketcher.Constraint('Horizontal',6))
    
    rev = obj.newObject('PartDesign::Revolution',name+'_Revolution')
    rev.Profile = sketch
    rev.Angle = 360
    rev.ReferenceAxis = (obj.getObject('X_Axis'), [''])
    rev.Midplane = 0
    sketch.Visibility = False
    
    obj.ViewObject.ShapeColor = color
    obj.ViewObject.Transparency = 50
    obj.Label = name
    update_geom_info(obj, geom_info)
    return obj

# Test
if __name__ == "__main__":
  from utils import start_DOC
  DOC = None
  start_DOC(DOC)
  model_beam()