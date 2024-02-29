# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:03:42 2024

@author: 庄赫
"""

from .utils import freecad_da, update_geom_info, get_DOC, rotate, thisfolder#,translate
from .freecad_model_lens import model_lens
from .freecad_model_composition import initialize_composition_old, add_to_composition
import numpy as np
import csv
import math
from copy import deepcopy

if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Mesh
  import ImportGui
  import Sketcher
  import Part
  from math import pi

DEFAULT_MAX_ANGULAR_OFFSET = 10
price = 0
DEFAULT_MOUNT_COLOR = (0.75,0.75,0.75)
DEFAULT_POST_COLOR = (0.8,0.8,0.8)
DEFAULT_HOLDER_COLOR = (0.2,0.2,0.2)

def Model_element_holder(name="marker", h1 = (0,0), h2 = (75,0), h3 = (75,75), 
                      h4 = (0,75),color=DEFAULT_MOUNT_COLOR,
                      geom=None,aperture=25.4,thickness=5,**kwargs):
    # obj_ele = deepcopy(element)
    DOC = get_DOC()
    POS = geom[0]
    AXES = geom[1]
    if np.shape(AXES)==(3,):
      NORMAL=AXES
    else:
      NORMAL=AXES[:,0]
    obj_ele = DOC.addObject("Part::Cylinder","Cylinder")
    obj_ele.Label = "element"
    obj_ele.Radius = aperture/2
    obj_ele.Height = thickness
    obj_ele.Placement = Placement(Vector(0,0,0), Rotation(0,90,0), Vector(0,0,0))
    height = POS[2]
    obj1 = DOC.addObject("Part::Box",name)
    obj1.Label = name+" part1"
    obj1.Length = 11
    obj1.Width = 10
    obj1.Height = 5
    obj1.ViewObject.ShapeColor=color
    obj1.Placement = Placement(Vector(-10,-5,-5), Rotation(0,0,0), Vector(0,0,0))
    obj = DOC.addObject("Part::Box",name)
    obj.Label = name
    obj.Length = 5
    obj.Width = 10
    obj.Height = height
    obj.ViewObject.ShapeColor=color
    obj.Placement = Placement(Vector(-15 ,-5,-height), Rotation(0,0,0), Vector(0,0,0))
    update_geom_info(obj, geom)
    update_geom_info(obj1, geom)
    update_geom_info(obj_ele, geom)
    part=DOC.addObject("Part::MultiFuse","Fusion")
    part.Shapes = [obj,obj_ele,obj1]
    obj.Visibility = False
    obj_ele.Visibility = False
    size = 1
    NEW_POS = POS - NORMAL*12.5
    quot_x = math.floor(NEW_POS[0]/(25*size))
    quot_y = math.floor(NEW_POS[1]/(25*size))
    h1 = (quot_x*(25*size),quot_y*(25*size))
    if NEW_POS[0]-h1[0]<8:
      h1=(h1[0]-25,h1[1])
    if NEW_POS[1]-h1[1]<8:
      h1=(h1[0],h1[1]-25)
    if h1[0]+(25*size)-NEW_POS[0]<8:
      h1=(h1[0]+25,h1[1])
    if h1[1]+(25*size)-NEW_POS[1]<8:
      h1=(h1[0],h1[1]+25)
    h2 =(h1[0]+(25*size),h1[1])
    h3 =(h1[0]+(25*size),h1[1]+(25*size))
    
    obj_new = DOC.addObject('PartDesign::Body', name)
    sketch = obj_new.newObject('Sketcher::SketchObject', name+'_sketch')
    sketch.addGeometry(Part.LineSegment(Vector(h1[0]-17.5,h1[1]-7.5,0),Vector(h2[0]+7.5,h1[1]-7.5,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Horizontal',0)) 
    sketch.addGeometry(Part.LineSegment(Vector(h2[0]+7.5,h1[1]-7.5,0),Vector(h2[0]+7.5,h3[1]+17.5,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,2)) 
    sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
    sketch.addGeometry(Part.LineSegment(Vector(h2[0]+7.5,h3[1]+17.5,0),Vector(h1[0]-17.5,h1[1]-7.5,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2)) 
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,0,1)) 
    pad = obj_new.newObject('PartDesign::Pad','Pad')
    pad.Profile = sketch
    pad.Length = 5
    pad.ReferenceAxis = (sketch,['N_Axis'])
    pad.Midplane = 1
    sketch.Visibility = False
    obj_new.Placement = Placement(Vector(0,0,7.5), Rotation(0,0,0), Vector(0,0,0))
    obj_h1 = DOC.addObject("Part::Cone","Cone")
    obj_h1.Radius1 = 0
    obj_h1.Radius2 = 6
    obj_h1.Height = 5
    obj_h1.Placement = Placement(Vector(h1[0],h1[1],0), Rotation(0,0,0), Vector(0,0,0))
    obj_h2 = DOC.addObject("Part::Cone","Cone")
    obj_h2.Radius1 = 0
    obj_h2.Radius2 = 6
    obj_h2.Height = 5
    obj_h2.Placement = Placement(Vector(h2[0],h2[1],0), Rotation(0,0,0), Vector(0,0,0))
    obj_h3 = DOC.addObject("Part::Cone","Cone")
    obj_h3.Radius1 = 0
    obj_h3.Radius2 = 6
    obj_h3.Height = 5
    obj_h3.Placement = Placement(Vector(h3[0],h3[1],0), Rotation(0,0,0), Vector(0,0,0))
    
    holder=DOC.addObject("Part::MultiFuse","Fusion")
    holder.Shapes = [obj_new,obj_h1,obj_h2,obj_h3]
    obj_new.Visibility = False
    obj_h1.Visibility = False
    obj_h2.Visibility = False
    obj_h3.Visibility = False
    
    obj_holder = DOC.addObject("Part::Cut","Cut")
    obj_holder.Base = holder
    obj_holder.Tool = obj
    holder.Visibility = False
    part_all = initialize_composition_old(name="element_holder")
    container = part,obj_holder
    add_to_composition(part_all, container)
    DOC.recompute()
    return part_all