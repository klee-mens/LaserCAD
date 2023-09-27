# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 14:40:56 2023

@author: mens
"""

# from ..basic_optics import Component
# from ..freecad_models.utils import thisfolder, load_STL,freecad_da
# from ..freecad_models.freecad_model_mounts import load_mount_from_csv,lens_mount,mirror_mount

import sys
sys.path.append('C:\\ProgramData\\Anaconda3')
from LaserCAD.basic_optics import Component
from LaserCAD.freecad_models.utils import thisfolder,load_STL,freecad_da,clear_doc
from LaserCAD.freecad_models.freecad_model_composition import initialize_composition_old,add_to_composition
from LaserCAD.freecad_models.freecad_model_mounts import lens_mount,mirror_mount,DEFAULT_MOUNT_COLOR,DEFAULT_MAX_ANGULAR_OFFSET,draw_rooftop_mount,rotate_vector
from LaserCAD.freecad_models.freecad_model_grating import grating_mount
from LaserCAD.basic_optics import Mirror, Geom_Object
from copy import deepcopy
import csv
import os
import numpy as np
DEFALUT_CAV_PATH = thisfolder
DEFALUT_MIRROR_PATH = thisfolder + "mount_meshes\\mirror"
DEFALUT_LENS_PATH = thisfolder + "mount_meshes\\lens"
DEFALUT_SPEIAL_MOUNT_PATH = thisfolder + "mount_meshes\\special mount"
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


def rotate_vector(shiftvec=np.array((1.0,0,0)),vec=np.array((1.0,0,0)),angle=0):
  """
  rotates the shiftvec around vec with angle 

  Parameters
  ----------
  shiftvec : np.array(), optional
    The vector needs to be rotated. The default is np.array((1,0,0)).
  vec : np.array(), optional
    The rotating axis. The default is np.array((1,0,0)).
  angle : float/int, optional
    The angle. The default is 0.

  Returns
  -------
  vector:
    retated vector

  """
  k=np.dot(shiftvec,np.cos(angle))+np.cross(vec,shiftvec)*np.sin(angle)+np.dot(vec,(np.sum(vec*shiftvec))*(1-np.cos(angle)))
  return k

class Mount(Component):
  def __init__(self, name="KS1",elm_type="mirror", **kwargs):
    super().__init__(name, **kwargs)
    if name in MIRROR_LIST:
      stl_file=thisfolder+"\\mount_meshes\\adjusted mirror mount\\" + name + ".stl"
    elif name in LENS_LIST:
      stl_file=thisfolder+"\\mount_meshes\\adjusted lens mount\\" + name + ".stl"
    else:
      stl_file=thisfolder+"\\mount_meshes\\special mount\\" + name + ".stl"
    self.name = name
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=DEFAULT_MOUNT_COLOR
    self.draw_dict["geom"]=[self.pos,self._axes]
    self.elm_type = elm_type
    self.draw_dict["drawing_post"] = False
    self.draw_dict["Filp90"] = False
    # self.freecad_model = load_STL
    self.docking_obj = Geom_Object(pos = self.pos+(1,0,3),normal=(0,0,1))
    self.mount_in_database = self.set_by_table()
    
  def set_by_table(self):
    buf = []
    mount_in_database = False
    aperture =height = price = xshift = offset=0
    if self.name in MIRROR_LIST:model_type ="mirror" 
    else:model_type="lens"
    with open(thisfolder+model_type+"mounts.csv") as csvfile: 
      reader = csv.DictReader(csvfile)
      for row in reader:
        buf.append(row)
    for mount_loop in buf:
      if mount_loop["name"] == self.name:
        mount_in_database = True
        aperture = float(mount_loop["aperture"])
        height = float(mount_loop["height"])
        price = float(mount_loop["price"])
        xshift = float(mount_loop["xshift"])
        offset = (float(mount_loop["offsetX"]),
                        float(mount_loop["offsetY"]),
                        float(mount_loop["offsetZ"]))
        rotation = (float(mount_loop["rot_angleZ"]),
                            float(mount_loop["rot_angleY"]),
                            float(mount_loop["rot_angleX"]))
    if not mount_in_database:
      # print("This mount was not in the table")
      return False
    self.aperture = aperture
    self.zshift = -height
    self.price = price
    self.xshift = xshift
    self.draw_dict["xshift"]=xshift
    self.draw_dict["height"]=height
    self.yshift = 0
    self.offset_vector = offset
    # self.post_docking_pos = self.pos+np.array([xshift,0,height])
    docking_pos = np.array([xshift,0,-height])
    docking_normal = (0,0,1)
    a=(1,0,0)
    if np.sum(np.cross(a,self.normal))!=0:
      rot_axis = np.cross(a,self.normal)/np.linalg.norm(np.cross(a,self.normal))
      rot_angle = np.arccos(np.sum(a*self.normal)/(np.linalg.norm(a)*np.linalg.norm(self.normal)))
      docking_pos = rotate_vector(docking_pos,rot_axis,rot_angle)
      docking_normal = rotate_vector(docking_normal,rot_axis,rot_angle)
    
    self.docking_obj = Geom_Object(pos = self.pos+docking_pos,normal=docking_normal)
    
    # self.docking_obj.pos = self.pos + np.array([xshift,0,-height])
    if self.normal[2]<DEFAULT_MAX_ANGULAR_OFFSET:
      self.normal[2]=0
      self.normal = self.normal/np.linalg.norm(self.normal)
      self.post_docking_direction = (0,0,1)
    else:
      print("this post should not be placed in the ground plate")
    self.rotation = rotation
    return True
  
  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj])
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj])
  
  def draw_fc(self):
    self.update_draw_dict()
    if self.mount_in_database:
      self.draw_dict["mount_type"] = self.name
      if self.name in MIRROR_LIST:
        # return mirror_mount(**self.draw_dict)
        return load_STL(**self.draw_dict)
      else:
        return load_STL(**self.draw_dict)
    elif self.name in SPECIAL_LIST or self.name in MIRROR_LIST or self.name in LENS_LIST:
      
      return load_STL(**self.draw_dict)
    else:
      return("This mount is not in the correct folder")

class Grating_mount(Mount):
  def __init__(self, name="grating_mounmt",height=50,thickness=8, **kwargs):
    super().__init__(name, **kwargs)
    self.draw_dict["height"]=height
    self.draw_dict["thickness"]= thickness
    self.draw_dict["drawing_post"] = False
    self.draw_dict["geom"]=[self.pos,self._axes]
    self.xshift = 17
  def draw_fc(self):
    return grating_mount(**self.draw_dict)

class Special_mount(Mount):
  def __init__(self, name="special_mounmt",aperture=25.4,thickness=10,docking_pos = (1,2,3),docking_normal=(0,0,1), **kwargs):
    super().__init__(name, **kwargs)
    self.draw_dict["aperture"] = aperture
    self.draw_dict["thickness"] = thickness
    self.draw_dict["geom"]=[self.pos,self._axes]
    if name=="rooftop mirror mount":
      self.list_rooptop_mirror_mount(aperture)
    if name == "Stripe mirror mount":
      self.list_rooptop_mirror_mount(aperture)
    
    a=(1,0,0)
    if np.sum(np.cross(a,self.normal))!=0:
      rot_axis = np.cross(a,self.normal)/np.linalg.norm(np.cross(a,self.normal))
      rot_angle = np.arccos(np.sum(a*self.normal)/(np.linalg.norm(a)*np.linalg.norm(self.normal)))
      docking_pos = rotate_vector(docking_pos,rot_axis,rot_angle)
      docking_normal = rotate_vector(docking_normal,rot_axis,rot_angle)
    
    self.docking_obj = Geom_Object(pos = self.pos+docking_pos,normal=docking_normal)
    
    
    
  def list_rooptop_mirror_mount(self,aperture=25.4, **keywords):
    self.xshift=38#+aperture/2
    self.zshift=-5
    self.draw_dict["stl_file"]=thisfolder+"\\mount_meshes\\special mount\\rooftop mirror mount.stl"
    self.draw_dict["mount_type"] = "rooftop_mirror_mount"
    """
    # if freecad_da:
    #   additional_mount = draw_rooftop_mount(xxshift=aperture/2,geom=self.draw_dict["geom"])
    # xshift=57+aperture/2-17.2
    # zshift=-5
    # shiftvec=(xshift,0,zshift)
    # default=(1,0,0)
    # default_axis=(0,1,0)
    # normal=self.normal
    # angle = default.getAngle(normal)
    # if angle!=0:
    #   vec = default.cross(normal)
    #   if np.linalg.norm(vec)==0:
    #     vec = (0,0,1) 
    #   vec = vec/np.linalg.norm(vec)
    #   shiftvec = rotate_vector(shiftvec=shiftvec,vec=vec,angle=angle)
    #   default_axis = rotate_vector(shiftvec=default_axis,vec=vec,angle=angle)
    #   default_axis = default_axis/np.linalg.norm(default_axis)
    # if angle==np.pi/180:
    #   shiftvec = -shiftvec
    # new_pos = (self.pos)+shiftvec
    # geom = (new_pos,self.normal)
    # mount_type = "POLARIS-K2"
    # self.draw_dict["geom"]=geom
    """
    
  def list_stripe_mirror_mount(self,thickness=25.4, **keywords):
    self.draw_dict["model_type"] = "Stripe"
    self.xshift = thickness-7
    self.yshift = 104.3
  
  @property
  def docking_pos(self):
    return np.array(self.docking_obj.pos) * 1.0
  @docking_pos.setter
  def docking_pos(self, x):
    self.docking_pos = np.array(x) * 1.0
    self.docking_obj.pos = self.docking_pos
  
  @property
  def docking_normal(self):
    return np.array(self.docking_obj.normal) * 1.0
  @docking_normal.setter
  def docking_normal(self, x):
    self.docking_normal = np.array(x) * 1.0
    self.docking_obj.normal = self.docking_normal
    
  def draw_fc(self):
    # self.draw_dict["geom"][0]=self.draw_dict["geom"][0] + self.normal*self.draw_dict["aperture"]/2
    # a=load_STL(**self.draw_dict)
    # geom_next = deepcopy(self.draw_dict["geom"])
    # geom_next[0] = self.draw_dict["geom"][0]+np.array([self.xshift,0,self.zshift])
    # b=load_STL(stl_file = thisfolder+"\\mount_meshes\\adjusted mirror mount\\POLARIS-K2.stl",  
    #            geom=geom_next, off0=np.array([self.xshift,0,self.zshift]))
    # part = initialize_composition_old(name="rooftop mirror mount")
    # container = a,b
    # add_to_composition(part, container)
    if self.name=="rooftop mirror mount" or self.name=="Stripe mirror mount":
      return mirror_mount(**self.draw_dict)
    else:
      self.draw_dict["geom"]=[self.pos,self._axes]
      return load_STL(**self.draw_dict)
    # return part
    
  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj])
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj])
    
if freecad_da:
  clear_doc()

M1 = Special_mount(name = "H45CN",docking_pos=(22,22,0),docking_normal=(1,1,0),normal=(1,1,0))
M1.normal=(1,0,0)
M1.draw()
M2= Mount(name="KM200CP_M",pos=M1.docking_pos,normal=M1.docking_normal)
M2.draw()