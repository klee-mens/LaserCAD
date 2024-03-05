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

def Model_element_holder(name="marker", post_distence= 10,base_height=5,color=DEFAULT_MOUNT_COLOR,
                      geom=None,aperture=25.4,thickness=5,width=50,height=25,ele_type="Mirror",**kwargs):
    # opt_ele = deepcopy(element)
    DOC = get_DOC()
    POS = geom[0]
    AXES = geom[1]
    if np.shape(AXES)==(3,):
      NORMAL=AXES
    else:
      NORMAL=AXES[:,0]
      if AXES[2,2]<-0.9:
        geom[1][:,1] = -geom[1][:,1]
        geom[1][:,2] = -geom[1][:,2]
    if ele_type == "Grating":
      opt_ele = DOC.addObject("Part::Box","Box")
      opt_ele.Label = "element"
      opt_ele.Height = height
      opt_ele.Width = width
      opt_ele.Length = thickness
      offset = Vector(0, -opt_ele.Width/2,-opt_ele.Height/2)
      opt_ele.Placement = Placement(offset, Rotation(0,0,0), Vector(0,0,0))
    else:
      opt_ele = DOC.addObject("Part::Cylinder","Cylinder")
      opt_ele.Label = "element"
      opt_ele.Radius = aperture/2
      opt_ele.Height = thickness
      offset = Vector(0,0,0)
      opt_ele.Placement = Placement(Vector(0,0,0), Rotation(0,90,0), Vector(0,0,0))
    # construction fo the horizontal post part
    height = POS[2]
    horizont_post_part = DOC.addObject("Part::Box",name)
    horizont_post_part.Label = name+" part1"
    horizont_post_part.Length = post_distence+1
    horizont_post_part.Width = 10
    horizont_post_part.Height = 5
    horizont_post_part.ViewObject.ShapeColor=color
    horizont_post_part.Placement = Placement(Vector(-post_distence,-5,-5), Rotation(0,0,0), Vector(0,0,0))
    # construction fo the vertical post part
    vertica_post_part = DOC.addObject("Part::Box",name)
    vertica_post_part.Label = name
    vertica_post_part.Length = 5
    vertica_post_part.Width = 10
    vertica_post_part.Height = height
    vertica_post_part.ViewObject.ShapeColor=color
    vertica_post_part.Placement = Placement(Vector(-post_distence-5 ,-5,-height), Rotation(0,0,0), Vector(0,0,0))
    update_geom_info(vertica_post_part, geom)
    update_geom_info(horizont_post_part, geom)
    update_geom_info(opt_ele, geom, off0=offset)
    part=DOC.addObject("Part::MultiFuse","Fusion")
    part.Shapes = [vertica_post_part,opt_ele,horizont_post_part]
    vertica_post_part.Visibility = False
    opt_ele.Visibility = False
    # find the breadboard points h1 to h4
    size = 1
    NEW_POS = POS - NORMAL*((2.5+post_distence))
    
    quot_x = math.floor(NEW_POS[0]/(25*size))
    quot_y = math.floor(NEW_POS[1]/(25*size))
    h1 = (quot_x*(25*size),quot_y*(25*size))
    # if NEW_POS[0]-h1[0]<8:
    #   h1=(h1[0]-25,h1[1])
    # if NEW_POS[1]-h1[1]<8:
    #   h1=(h1[0],h1[1]-25)
    # if h1[0]+(25*size)-NEW_POS[0]<8:
    #   h1=(h1[0]+25,h1[1])
    # if h1[1]+(25*size)-NEW_POS[1]<8:
    #   h1=(h1[0],h1[1]+25)
    h2 = (h1[0]+(25*size),h1[1])
    h3 = (h1[0]+(25*size),h1[1]+(25*size))
    h4 = (h1[0],h1[1]+(25*size))
    
    # construction of the latching cones
    # if NORMAL[0]<=0 and NORMAL[1]>=0:
    obj_new = DOC.addObject('PartDesign::Body', name)
    sketch = obj_new.newObject('Sketcher::SketchObject', name+'_sketch')
    sketch.addGeometry(Part.LineSegment(Vector(h1[0]-7.5,h1[1]-7.5,0),Vector(h2[0]+7.5,h1[1]-7.5,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Horizontal',0)) 
    sketch.addGeometry(Part.LineSegment(Vector(h2[0]+7.5,h1[1]-7.5,0),Vector(h2[0]+7.5,h3[1]+7.5,0)),False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,2)) 
    sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
    sketch.addGeometry(Part.LineSegment(Vector(h2[0]+7.5,h3[1]+7.5,0),Vector(h4[0]-7.5,h3[1]+7.5,0)),False)
    sketch.addGeometry(Part.LineSegment(Vector(h4[0]-7.5,h3[1]+7.5,0),Vector(h1[0]-7.5,h1[1]-7.5,0)),False)
    # sketch.addGeometry(Part.LineSegment(Vector(h2[0]+7.5,h3[1]+17.5,0),Vector(h1[0]-17.5,h1[1]-7.5,0)),False)
    # sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2)) 
    # sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,0,1)) 
    
    # construction of the base part with the cones
    base = obj_new.newObject('PartDesign::Pad','Base')
    base.Profile = sketch
    base.Length = base_height
    base.ReferenceAxis = (sketch,['N_Axis'])
    base.Midplane = 1
    sketch.Visibility = False
    obj_new.Placement = Placement(Vector(0,0,3+base_height/2), Rotation(0,0,0), Vector(0,0,0))
    obj_h1 = DOC.addObject("Part::Cone","Cone")
    obj_h1.Radius1 = 0
    obj_h1.Radius2 = 6/5*3
    obj_h1.Height = 3
    obj_h1.Placement = Placement(Vector(h1[0],h1[1],0), Rotation(0,0,0), Vector(0,0,0))
    obj_h2 = DOC.addObject("Part::Cone","Cone")
    obj_h2.Radius1 = 0
    obj_h2.Radius2 = 6/5*3
    obj_h2.Height = 3
    obj_h2.Placement = Placement(Vector(h2[0],h2[1],0), Rotation(0,0,0), Vector(0,0,0))
    obj_h3 = DOC.addObject("Part::Cone","Cone")
    obj_h3.Radius1 = 0
    obj_h3.Radius2 = 6/5*3
    obj_h3.Height = 3
    obj_h3.Placement = Placement(Vector(h3[0],h3[1],0), Rotation(0,0,0), Vector(0,0,0))
    obj_h4 = DOC.addObject("Part::Cone","Cone")
    obj_h4.Radius1 = 0
    obj_h4.Radius2 = 6/5*3
    obj_h4.Height = 3
    obj_h4.Placement = Placement(Vector(h4[0],h4[1],0), Rotation(0,0,0), Vector(0,0,0))
    
    # construction of the fusion and cut
    holder=DOC.addObject("Part::MultiFuse","Fusion")
    holder.Shapes = [obj_new,obj_h1,obj_h2,obj_h3, obj_h4]
    obj_new.Visibility = False
    obj_h1.Visibility = False
    obj_h2.Visibility = False
    obj_h3.Visibility = False
    obj_h4.Visibility = False
    
    obj_holder = DOC.addObject("Part::Cut","Cut")
    obj_holder.Base = holder
    obj_holder.Tool = vertica_post_part
    
    opt_cut = DOC.addObject("Part::Cylinder","Cylinder")
    opt_cut.Label = "element"
    opt_cut.Radius = height+50
    opt_cut.Height = 50
    opt_cut.Placement = Placement(Vector(0,0,0), Rotation(0,90,0), Vector(0,0,0))
    update_geom_info(opt_cut, geom)
    obj_holder_new = DOC.addObject("Part::Cut","Cut")
    obj_holder_new.Base = obj_holder
    obj_holder_new.Tool = opt_cut
    obj_holder_new.Placement = Placement(Vector(0,0,-3), Rotation(0,0,0), Vector(0,0,0))
    
    holder.Visibility = False
    part_all = initialize_composition_old(name="element_holder")
    container = part,obj_holder_new
    add_to_composition(part_all, container)
    DOC.recompute()
    return part_all