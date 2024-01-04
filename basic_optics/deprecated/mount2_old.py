#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 18:58:53 2023

@author: mens
"""

from ..freecad_models.utils import thisfolder,load_STL,rotate,translate
from ..freecad_models.freecad_model_composition import initialize_composition_old,add_to_composition
from ..freecad_models.freecad_model_mounts import mirror_mount,DEFAULT_MOUNT_COLOR,DEFAULT_MAX_ANGULAR_OFFSET
from .geom_object import Geom_Object
from .post import Post_and_holder

# from copy import deepcopy
import csv
import os
import numpy as np

DEFALUT_CAV_PATH = thisfolder
DEFALUT_MIRROR_PATH = thisfolder + "mount_meshes/mirror"
DEFALUT_LENS_PATH = thisfolder + "mount_meshes/lens"
DEFALUT_SPEIAL_MOUNT_PATH = thisfolder + "mount_meshes/special mount"
MIRROR_LIST1 = os.listdir(DEFALUT_MIRROR_PATH)
MIRROR_LIST = []
for i in MIRROR_LIST1:
  a,b,c = str.partition(i, ".")
  MIRROR_LIST.append(a)

LENS_LIST1 = os.listdir(DEFALUT_LENS_PATH)
LENS_LIST = []
for i in LENS_LIST1:
  a,b,c = str.partition(i, ".")
  LENS_LIST.append(a)
  
SPECIAL_LIST1 = os.listdir(DEFALUT_SPEIAL_MOUNT_PATH)
SPECIAL_LIST = []
for i in SPECIAL_LIST1:
  a,b,c = str.partition(i, ".")
  SPECIAL_LIST.append(a)
del a,b,c,i,SPECIAL_LIST1,LENS_LIST1,MIRROR_LIST1


def load_unit_mount(model):
  unit = Unit_Mount()
  

class Unit_Mount(Geom_Object):
  """
  Mount class, inherit from <Geom_Object>
  Application as follows:
    Mon = Mount(elm_type="mirror")
  Usually exists as part of the component
  Gets a post as an member object in the __init__
  Most values are set and corrected when the draw() funtion is called
  draw_fc() also draws the post
  """
  def __init__(self, name="mount",model="POLARIS-K1", **kwargs):
    super().__init__(name, **kwargs)
    self.model = model
    self.docking_obj = Geom_Object()
    self.draw_dict["color"]=DEFAULT_MOUNT_COLOR
    self.path = thisfolder + "/mount_meshes/mirror/"
    self.draw_dict["stl_file"] = self.path + self.model + ".stl"
    self.freecad_model = load_STL
    
  def update_draw_dict(self):
    self.path = thisfolder + "/mount_meshes/mirror/"
    self.draw_dict["stl_file"] = self.path + self.model + ".stl"
  
  def rotate_around_normal(self, angle=np.pi/2):
    self.rotate(self.normal, phi=angle)
    

class Composed_Mount(Unit_Mount):
  """
  This one is for compositions of mulitple mounts stacked togehter
  The add function drags every new mount to the docking position of the old one
  and as usual all are moved correctly when the Composed_Mount is moved
  """
  def __init__(self, **kwargs):
    self.mount_list = []
    super().__init__(**kwargs)
    self.docking_obj = Geom_Object()
    self.docking_obj.set_geom(self.get_geom())
    
  def add(self, mount):
    mount.set_geom(self.docking_obj.get_geom())
    self.mount_list.append(mount)
    self.docking_obj.set_geom(mount.docking_obj.get_geom())
    
  def draw_fc(self):
    part = initialize_composition_old(name="mount, post and base")
    container = []
    for mount in self.mount_list:
      container.append(mount.draw())
    add_to_composition(part, container)
    return part
    
  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj,self.post])
    self._rearange_subobjects_pos( old_pos, new_pos, self.mount_list)
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj,self.post])
    self._rearange_subobjects_axes( old_axes, new_axes, self.mount_list)
    
