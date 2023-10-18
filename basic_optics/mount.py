# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 14:40:56 2023

@author: mens
"""

from ..freecad_models.utils import thisfolder,load_STL,rotate,translate
from ..freecad_models.freecad_model_composition import initialize_composition_old,add_to_composition
from ..freecad_models.freecad_model_mounts import mirror_mount,DEFAULT_MOUNT_COLOR,DEFAULT_MAX_ANGULAR_OFFSET
from ..freecad_models.freecad_model_grating import grating_mount
from .geom_object import Geom_Object
from .post import Post_and_holder

# from copy import deepcopy
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

def get_model_by_aperture_and_element(elm_type, aperture):
  if elm_type == "lens":
    if aperture<= 25.4/2:
      model = "MLH05_M"
    elif aperture <= 25.4:
      model = "LMR1_M"
    elif aperture <= 25.4*1.5:
      model = "LMR1.5_M"
    elif aperture <=25.4*2:
      model = "LMR2_M"
  elif elm_type == "mirror":
    if aperture <= 4:
      model = "KMSS"
    elif aperture<= 25.4/2:
      model = "POLARIS-K05"
    elif aperture <= 25.4:
      model = "POLARIS-K1"
    elif aperture <= 25.4*1.5:
      model = "POLARIS-K15S4"
    elif aperture <=25.4*2:
      model = "POLARIS-K2"
    elif aperture <=25.4*3:
      model = "POLARIS-K3S5"
    elif aperture <=25.4*4:
      model = "KS4"
    else:
      model = "large mirror mount"
  else:
    model = "dont_draw"
  return model

class Mount(Geom_Object):
  """
  Mount class, erbit from <Geom_Object>
  Application as follows:
    Mon = Mount(elm_type="mirror")
  Usually exists as part of the component
  """
  def __init__(self, name="mount",model="default",aperture=25.4,thickness=5,elm_type="mirror",Flip90=False, **kwargs):
    super().__init__(name, **kwargs)
    self.draw_dict["color"]=DEFAULT_MOUNT_COLOR
    self.draw_dict["geom"]=self.get_geom()
    self.elm_type = elm_type
    self.draw_dict["drawing_post"] = False
    self.Flip90 = Flip90
    self.draw_dict["Flip90"] = Flip90
    # self.docking_obj = Geom_Object(pos = self.pos+(1,0,3),normal=(0,0,1))
    self.docking_obj = Geom_Object()
    self.draw_dict["offset"] = np.zeros(3)
    self.draw_dict["rotation"] = (np.array((0,0,1)), 0)
    # if Flip90:
    #   self.draw_dict["rotation"] = (self.normal, np.pi/2)
    self.aperture = aperture
    self.thickness = thickness
    self.xshift = 0
    self.zshift = 0
    self.post = Geom_Object()
    if model =="default":
      self.model = get_model_by_aperture_and_element(self.elm_type, self.aperture)
    else:
      self.model = model
    if self.model in MIRROR_LIST:
      stl_file=thisfolder+"\\mount_meshes\\adjusted mirror mount\\" + self.model + ".stl"
    elif self.model in LENS_LIST:
      stl_file=thisfolder+"\\mount_meshes\\adjusted lens mount\\" + self.model + ".stl"
    else:
      stl_file=thisfolder+"\\mount_meshes\\special mount\\" + self.model + ".stl"
    self.draw_dict["stl_file"]=stl_file
    self.mount_in_database = self.set_by_table()
    post = Post_and_holder(name=self.name + "post",elm_type=self.elm_type)
    post.set_geom(self.docking_obj.get_geom())
    self.post = post
    
  def set_by_table(self):
    """
    sets the docking object and the model by reading the "the file.csv"
    Used to determine if there is a default suitable mount in the database.
    Returns
    -------
    bool
      True: this mount was in the csv file, which can be read directy
      False: this mont was not in the csv file
    """
    buf = []
    mount_in_database = False
    aperture =height = price = xshift = offset=0
    if self.model in MIRROR_LIST:model_type ="mirror" 
    else:model_type="lens"
    with open(thisfolder+model_type+"mounts.csv") as csvfile: 
      reader = csv.DictReader(csvfile)
      for row in reader:
        buf.append(row)
    for mount_loop in buf:
      if mount_loop["name"] == self.model:
        mount_in_database = True
        aperture = float(mount_loop["aperture"])
        height = float(mount_loop["height"])
        price = float(mount_loop["price"])
        xshift = float(mount_loop["xshift"])
        offset = (float(mount_loop["offsetX"]),
                        float(mount_loop["offsetY"]),
                        float(mount_loop["offsetZ"]))
        # rotation = (float(mount_loop["rot_angleZ"]),
        #                     float(mount_loop["rot_angleY"]),
        #                     float(mount_loop["rot_angleX"]))
    if not mount_in_database:
      return False
    self.aperture = aperture
    self.zshift = -height
    self.price = price
    self.xshift = xshift
    self.draw_dict["xshift"]=xshift
    self.draw_dict["height"]=height
    self.yshift = 0
    self.offset_vector = offset
    self.draw_dict["mount_type"] = self.model
    docking_pos = np.array([xshift,0,-height])
    docking_normal = self.normal
    # updates the docking geom for the first time
    if self.normal[2]<DEFAULT_MAX_ANGULAR_OFFSET/180*np.pi:
      tempnormal = self.normal
      tempnormal[2]=0
      self.normal=tempnormal
      self.normal = self.normal/np.linalg.norm(self.normal)
    else: print("this post should not be placed in the ground plate")
    # a=(1,0,0)
    # if np.sum(np.cross(a,self.normal))!=0:
    #   rot_axis = np.cross(a,self.normal)/np.linalg.norm(np.cross(a,self.normal))
    #   rot_angle = np.arccos(np.sum(a*self.normal)/(np.linalg.norm(a)*np.linalg.norm(self.normal)))
    #   docking_pos = rotate_vector(docking_pos,rot_axis,rot_angle)
    #   docking_normal = rotate_vector(docking_normal,rot_axis,rot_angle)
    # self.docking_obj = Geom_Object(pos = self.pos+docking_pos,normal=docking_normal)
    self.docking_obj = Geom_Object()
    self.docking_obj.pos = self.pos+xshift*self._axes[:,0]-height*self._axes[:,2]
    self.docking_obj.normal = docking_normal
    # self.rotation = rotation
    return True
  
  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj,self.post])
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj,self.post])

  def draw_fc(self):
    self.update_draw_dict()
    if self.normal[2]<DEFAULT_MAX_ANGULAR_OFFSET/180*np.pi:
      tempnormal = self.normal
      tempnormal[2]=0
      self.normal=tempnormal
      self.normal = self.normal/np.linalg.norm(self.normal)
    else: print("this post should not be placed in the ground plate")
    if self.elm_type == "dont_draw": return None
    if self.draw_dict["Flip90"]==True:
      self.draw_dict["rotation"] = (self.normal, np.pi/2)
    if self.model == "large mirror mount":
      self.draw_dict["thickness"] = self.thickness
      self.draw_dict["dia"] = self.aperture
      return mirror_mount(**self.draw_dict)
    if self._axes[2,2] <-0.9:
      self.rotate(self.normal,np.pi)
      self.draw_dict["geom"] = self.get_geom()
    obj = load_STL(**self.draw_dict)
    translate(obj, self.draw_dict["offset"])
    rotate(obj, self.draw_dict["rotation"][0], self.draw_dict["rotation"][1]*180/np.pi)
    obj1 = self.post.draw()
    part = initialize_composition_old(name="mount, post and base")
    container = obj,obj1
    add_to_composition(part, container)
    return part

class Grating_mount(Mount):
  def __init__(self, name="grating_mounmt",model="grating_mount",height=50,thickness=8, **kwargs):
    
    super().__init__(name, **kwargs)
    self.draw_dict["height"]=height
    self.draw_dict["thickness"]= thickness
    self.draw_dict["drawing_post"] = False
    self.draw_dict["geom"]=self.get_geom()
    self.xshift = 17 + 15
    docking_pos = np.array([self.xshift,0,-29])
    self.docking_obj.pos = self.docking_obj.pos+docking_pos[0]*self._axes[:,0]+docking_pos[2]*self._axes[:,2] 
    self.post.set_geom(self.docking_obj.get_geom())
    
  def draw_fc(self):
    self.update_draw_dict()
    obj = grating_mount(**self.draw_dict)
    obj1 = self.post.draw()
    part = initialize_composition_old(name="mount, post and base")
    container = obj,obj1
    add_to_composition(part, container)
    return part

class Special_mount(Mount):
  def __init__(self, name="special_mounmt",model="special_mount",aperture=25.4,thickness=10,
               docking_pos = (1,2,3),docking_normal=(0,0,1),drawing_post=False, **kwargs):
    super().__init__(name, **kwargs)
    self.draw_dict["aperture"] = aperture
    self.aperture = aperture
    self.draw_dict["thickness"] = thickness
    self.thickness = thickness
    self.draw_dict["geom"]=self.get_geom()
    self.model = model
    self.drawing_post = drawing_post
    if model=="rooftop mirror mount":
      self.post = None
      xshift = 38
      zshift = -5
      docking_pos = (xshift,0,zshift)
      docking_normal = self.normal
    if model == "Stripe mirror mount":
      xshift = 24
      yshift = 104.3
      self.post = None
      docking_pos = (xshift,yshift,0)
      docking_normal = -self.normal
    self.docking_obj = Geom_Object()
    self.docking_obj.pos = self.pos+docking_pos[0]*self._axes[:,0]+docking_pos[1]*self._axes[:,1]+docking_pos[2]*self._axes[:,2]
    self.docking_obj.normal=docking_normal
    if drawing_post:
      post = Post_and_holder(name=self.name + "post",elm_type=self.elm_type)
      post.set_geom(self.docking_obj.get_geom())
      self.post = post
  
  def set_geom(self, geom):
    """
    since the position of rooftop mirror and stripe mirror are related to the 
    aperture and thickness of the mirror itself, the are some changes that must 
    be made in the geom setting.

    """
    if np.shape(geom[1])==(3,3):
      normal = geom[1][:,0]
    else:
      normal = geom[1]
    if self.model != "Stripe mirror mount" and self.model != "rooftop mirror mount":
      self.pos = np.array(geom[0])
      self.set_axes(geom[1])
      return 1
    if self.model =="Stripe mirror mount":
      new_pos = np.array((self.thickness-25,0,0))
    elif self.model == "rooftop mirror mount":
      new_pos = np.array((self.aperture/2,0,0))
    a = (1,0,0)
    if np.sum(np.cross(a,normal))!=0:
      rot_axis = np.cross(a,normal)/np.linalg.norm(np.cross(a,normal))
      rot_angle = np.arccos(np.sum(a*normal)/(np.linalg.norm(a)*np.linalg.norm(normal)))
      new_pos = rotate_vector(new_pos,rot_axis,rot_angle)
    geom0 = np.array(geom[0] + new_pos)
    self.pos = np.array(geom0)
    self.set_axes(geom[1])
    
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
  
  def _pos_changed(self, old_pos, new_pos):
    if self.post != None:
      self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj,self.post])
    else:
      self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj])
  
  def _axes_changed(self, old_axes, new_axes):
    if self.post != None:
      self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj,self.post])
    else:
      self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj])
  
  def draw_fc(self):
    if self.model=="rooftop mirror mount" or self.model=="Stripe mirror mount":
      self.draw_dict["geom"]=self.get_geom()
      self.draw_dict["stl_file"]=thisfolder+"\\mount_meshes\\special mount\\" + self.model + ".stl"
      return load_STL(**self.draw_dict)
      # return mirror_mount(**self.draw_dict)
    else:
      if self._axes[2,2] <-0.9:
        self.rotate(self.normal,np.pi)
        self.draw_dict["geom"] = self.get_geom()
      self.draw_dict["geom"]=self.get_geom()
      self.draw_dict["stl_file"]=thisfolder+"\\mount_meshes\\special mount\\" + self.model + ".stl"
      obj = load_STL(**self.draw_dict)
      if self.drawing_post:
        obj1 = self.post.draw()
        part = initialize_composition_old(name="mount, post and base")
        container = obj,obj1
        add_to_composition(part, container)
        return part
      else:
        return obj
    
class Composed_Mount(Mount):
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
      container.append(mount.draw_fc())
    add_to_composition(part, container)
    return part
    
  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj,self.post])
    self._rearange_subobjects_pos( old_pos, new_pos, self.mount_list)
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj,self.post])
    self._rearange_subobjects_axes( old_axes, new_axes, self.mount_list)

# if freecad_da:
#   clear_doc()

# M1 = Special_mount(name = "aaa",model= "H45CN",docking_pos=(22,22,0),docking_normal=(1,1,0),normal=(1,1,0))
# M1.normal=(1,0,0)
# M1.draw()
# # M2= Mount(name="bbb",model= "KM200CP_M",pos=M1.docking_pos,normal=M1.docking_normal)
# M2= Mount(name="bbb",model= "KM200CP_M")
# M2.draw()

# Comp = Composed_Mount()
# Comp.add(M1)
# Comp.add(M2)
# Comp.draw()