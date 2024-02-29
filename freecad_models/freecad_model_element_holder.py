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
    obj = DOC.addObject("Part::Box",name)
    obj.Label = name
    obj.Length = 5
    obj.Width = 5
    obj.Height = height
    obj.ViewObject.ShapeColor=color
    obj.Placement = Placement(Vector(-5,-2.5,-height), Rotation(0,0,0), Vector(0,0,0))
    update_geom_info(obj, geom)
    update_geom_info(obj_ele, geom)
    part=DOC.addObject("Part::MultiFuse","Fusion")
    part.Shapes = [obj,obj_ele]
    obj.Visibility = False
    obj_ele.Visibility = False
    
    DOC.recompute()
    return part