# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:28:07 2022

@author: mens
"""

# from basic_optics import Opt_Element, TOLERANCE, Ray
# from basic_optics.freecad_models import model_mirror, freecad_da
from .geom_object import TOLERANCE, NORM0
from .ray import Ray
from ..freecad_models import model_mirror,lens_mount, mirror_mount, model_stripe_mirror, model_lamda_plane
from .optical_element import Opt_Element
import numpy as np
from copy import deepcopy

try:
  import FreeCAD
  DOC = FreeCAD.activeDocument()
  print(DOC)
  from FreeCAD import Vector, Placement, Rotation
except:
  freecad_da = False
  DOC = None

from ..freecad_models.utils import freecad_da, update_geom_info, get_DOC, rotate, thisfolder

class Mount(Opt_Element):
  """

  """
  def __init__(self, xshift=0,mount_type="default",obj_type="lens", **kwargs):
    super().__init__(**kwargs)
    
    # self.update_normal()
    #Cosmetics
    self.draw_dict["dia"] = 25.4
    self.draw_dict["drawing_post"] = False
    self.draw_dict["mount_type"] = mount_type
    if obj_type == "lens":
      self.simple_mount = True
    else:
      self.simple_mount = False

  def set_geom(self, geom):
    """
    setzt <pos> und __incident_normal auf <geom> und akturalisiert dann die 
    eigene <normal> entsprechend <phi> und <theta>

    Parameters
    ----------
    geom : 2-dim Tupel aus 3-D float arrays
      (pos, normal)
    """
    self.pos = geom[0]
    # self.__incident_normal = geom[1]
    axes = geom[1]
    self.__incident_normal = axes[:,0]
    self.update_normal()

  def __repr__(self):
    n = len(self.class_name())
    txt = 'Mirror(phi=' + repr(self.phi)
    txt += ", theta=" + repr(self.theta)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def draw_fc(self):
    self.update_draw_dict()
    # self.draw_dict["dia"]=self.aperture
    if self.simple_mount:
      obj = lens_mount(**self.draw_dict)
    else:
      obj = mirror_mount(**self.draw_dict)
    return obj

  def draw_text(self):
    if self.draw_dict["mount_type"] == "dont_draw":
      txt = "<" + self.name + ">'s mount will not be drawn."
    elif self.draw_dict["mount_type"] == "default":
      txt = "<" + self.name + ">'s mount is the default mount."
    else:
      txt = "<" + self.name + ">'s mount is the " + self.draw_dict["mount_type"] + "."
    return txt

class Post(Opt_Element):
  def __init__(self, xshift=0,base_exists=False, **kwargs):
    super().__init__(**kwargs)
    self.draw_dict["base_exists"]=base_exists
    
  def set_geom(self, geom):
    """
    setzt <pos> und __incident_normal auf <geom> und akturalisiert dann die 
    eigene <normal> entsprechend <phi> und <theta>

    Parameters
    ----------
    geom : 2-dim Tupel aus 3-D float arrays
      (pos, normal)
    """
    self.pos = geom[0]
    # self.__incident_normal = geom[1]
    axes = geom[1]
    self.__incident_normal = axes[:,0]
    self.update_normal()
  
  def __repr__(self):
    n = len(self.class_name())
    txt = 'Mirror(phi=' + repr(self.phi)
    txt += ", theta=" + repr(self.theta)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def draw_fc(self):
    self.update_draw_dict()
    # self.draw_dict["dia"]=self.aperture
    if self.simple_mount:
      obj = lens_mount(**self.draw_dict)
    else:
      obj = mirror_mount(**self.draw_dict)
    return obj