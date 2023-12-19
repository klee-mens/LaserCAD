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
from ..freecad_models.freecad_model_mounts import draw_post,draw_post_holder,draw_post_base,draw_1inch_post,draw_large_post

DEFALUT_POST_COLOR = (0.8,0.8,0.8)
DEFALUT_HOLDER_COLOR = (0.2,0.2,0.2)
POST_LIST = ["1inch_post","0.5inch_post","big_post"]

# from copy import deepcopy
import csv
import os
import numpy as np

DEFALUT_CAV_PATH = thisfolder
DEFALUT_MIRROR_PATH = thisfolder + "mount_meshes\\mirror"
DEFALUT_LENS_PATH = thisfolder + "mount_meshes\\lens"
DEFALUT_SPEIAL_MOUNT_PATH = thisfolder + "mount_meshes\\special_mount"

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

def default_mirror_mount(aperture):
  print(aperture)
  if aperture<= 25.4/2:
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
  return Unit_Mount(model=model)

def get_mount_by_aperture_and_element(aperture,elm_type):
  if elm_type == "Lens":
    if aperture<= 25.4/2:
      model = "MLH05_M"
    elif aperture <= 25.4:
      model = "LMR1_M"
    elif aperture <= 25.4*1.5:
      model = "LMR1.5_M"
    elif aperture <=25.4*2:
      model = "LMR2_M"
  elif elm_type == "Mirror":
    if aperture<= 25.4/2:
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
  return Unit_Mount(model=model)

# def Load_unit_mount(model = "KS1"):
#     if model in MIRROR_LIST:
#         return Mount(model)

class Unit_Mount(Geom_Object):
  """
  Mount class, erbit from <Geom_Object>
  Application as follows:
    Mon = Mount(elm_type="mirror")
  Usually exists as part of the component
  """
  def __init__(self, name="mount",model="default", **kwargs):
    super().__init__(name, **kwargs)
    self.model = model
    self.docking_obj = Geom_Object()
    self.set_by_table()
    self.draw_dict["stl_file"] = self.path + self.model + ".stl"
    self.freecad_model = load_STL
    
  
    
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
    if self.model in MIRROR_LIST:
        model_type ="mirror" 
    elif self.model in LENS_LIST:
        model_type="lens"
    else:
        model_type = ""
        print("whathzmutrzjtezj")
    folder = thisfolder+"mount_meshes\\"+model_type+"\\"
    with open(folder+model_type+"mounts.csv") as csvfile: 
      reader = csv.DictReader(csvfile)
      for row in reader:
        buf.append(row)
    for mount_loop in buf:
      if mount_loop["name"] == self.model:
        mount_in_database = True
        aperture = float(mount_loop["aperture"])
        DockingX = float(mount_loop["DockingX"])
        DockingY = float(mount_loop["DockingY"])
        DockingZ = float(mount_loop["DockingZ"])
        DockNormalX = float(mount_loop["DockNormalX"])
        DockNormalY = float(mount_loop["DockNormalY"])
        DockNormalZ = float(mount_loop["DockNormalZ"])
        
    if not mount_in_database:
      print("This mount is not in the database.")
      return False
    self.aperture = aperture
    
    docking_normal = np.array((DockNormalX,DockNormalY,DockNormalZ))
    self.docking_obj = Geom_Object()
    self.docking_obj.pos = self.pos+DockingX*self._axes[:,0]+DockingY*self._axes[:,1]+DockingZ*self._axes[:,2]
    self.docking_obj.normal = docking_normal
    self.path = folder
    return True

  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj])
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj])
    
class Post(Unit_Mount):
  def __init__(self, name="post",model="1_inch_post", **kwargs):
    super().__init__(name, **kwargs)
  
  def find_1inch_post(self):
    height = self.pos[2]
    if height<12.5:
      print("Warning, there is no suitable post holder at this height")
      return None
    model="RS05P4M"
    height_difference=0
    default_post_height = [12.5,19,25,38,50,65,75,90,100,155,65535]
    model_name = ["RS05P4M","RS075P4M","RS1P4M","RS1.5P4M","RS2P4M","RS2.5P4M",
                  "RS3P4M","RS3.5P4M","RS4P4M","RS6P4M",""]
    for i in range(10):
      if height < default_post_height[i+1] and height > default_post_height[i]:
        model = model_name[i]
        height_difference = height - default_post_height[i]
    return draw_1inch_post(name=model,h_diff = height_difference,
                            color=self.draw_dict["post_color"],geom = self.get_geom())
  
  def draw_freecad(self, **kwargs):
    self.draw_dict["geom"]=self.get_geom()
    self.draw_dict["name"] = self.name 
    self.draw_dict["post_color"] = self.post_color
    self.draw_dict["holder_color"] = self.holder_color
    if self.elm_type == "dont_draw":
      return None
    print(self.name,"'s position = ",self.pos)
    # return draw_post_part(**self.draw_dict)
    if self.post_type == "1inch_post":
      return self.find_1inch_post()
    elif self.post_type == "0.5inch_post":
      return draw_post_part(**self.draw_dict)
    else:
      return draw_large_post(height=self.pos[2],geom=self.get_geom())
    
def draw_post_part(name="post_part", base_exists=False, 
                   post_color=DEFALUT_POST_COLOR,holder_color=DEFALUT_HOLDER_COLOR, geom=None):
  """
  Draw the post part, including post, post holder and base
  Assuming that all optics are placed in the plane of z = 0.

  Parameters
  ----------
  name : String, optional
    The name of the part. The default is "post_part".
  height : float/int, optional
    distance from the center of the mirror to the bottom of the mount.
    The default is 12.
  xshift : float/int, optional
    distance from the center of the mirror to the cavity at the bottom of the 
    mount. The default is 0.
  geom : TYPE, optional
    mount geom. The default is None.

  Returns
  -------
  part : TYPE
    A part which includes the post, the post holder and the slotted bases.

  """
  POS = geom[0]
  AXES = geom[1]
  if np.shape(AXES)==(3,):
    NORMAL=AXES
  else:
    NORMAL=AXES[:,0]
  if (POS[2]<34) or (POS[2]>190):
    print("Warning, there is no suitable post holder and slotted base at this height")
    return None
  post_length=50
  if base_exists:
      if POS[2]>110:
        post_length=100
      elif POS[2]>90:
        post_length=75
      elif POS[2]>65:
        post_length=50
      elif POS[2]>55:
        post_length=40
      elif POS[2]>40:
        post_length=30
      else:
        post_length=20
        post2 = draw_post_holder(name="PH20E_M", 
                                 color=holder_color, geom=geom)
      post = draw_post(name="TR"+str(post_length)+"_M", color=post_color,geom=geom)
      if post_length>20:
        post2 = draw_post_holder(name="PH"+str(post_length)+"_M", color=holder_color, geom=geom)
  else:
      if POS[2]>105:
        post_length=100
      elif POS[2]>85:
        post_length=75
      elif POS[2]>60:
        post_length=50
      elif POS[2]>50:
        post_length=40
      elif POS[2]>35:
        post_length=30
      else:
        post_length=20
        post2 = draw_post_holder(name="PH"+str(post_length)+"E_M", color=holder_color, geom=geom)
      post = draw_post(name="TR"+str(post_length)+"_M", color=post_color,geom=geom)
      post2 = draw_post_holder(name="PH"+str(post_length)+"E_M", color=holder_color, geom=geom)
  if base_exists:
    if post_length>90 or post_length<31:
        post1 = draw_post_base(name="BA2_M", geom=geom)
    else:
        post1 = draw_post_base(name="BA1L",  geom=geom)
  else:
    post1 = None
  print(name,"'s height=",NORMAL[2]+post_length)
  part = initialize_composition_old(name=name)
  container = post,post1,post2
  add_to_composition(part, container)
  return part