# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 14:40:56 2023

@author: mens
"""

from ..freecad_models.utils import thisfolder,load_STL,rotate,translate
from ..freecad_models.freecad_model_composition import initialize_composition_old,add_to_composition
from ..freecad_models.freecad_model_mounts import mirror_mount,DEFAULT_MOUNT_COLOR,DEFAULT_MAX_ANGULAR_OFFSET,model_Post_Marker
from ..freecad_models.freecad_model_grating import grating_mount
from .geom_object import Geom_Object, rotation_matrix
from .post import Post_and_holder
from ..freecad_models.freecad_model_mounts import draw_post,draw_post_holder,draw_post_base,draw_1inch_post,draw_large_post,model_mirror_holder
# from .mirror import Mirror

DEFALUT_POST_COLOR = (0.8,0.8,0.8)
DEFALUT_HOLDER_COLOR = (0.2,0.2,0.2)
POST_LIST = ["1inch_post","0.5inch_post","big_post"]

# from copy import deepcopy
import csv
import os
import numpy as np
import math


DEFALUT_CAV_PATH = thisfolder
DEFALUT_MIRROR_PATH = thisfolder + "mount_meshes/mirror"
DEFALUT_LENS_PATH = thisfolder + "mount_meshes/lens"
DEFALUT_SPEIAL_MOUNT_PATH = thisfolder + "mount_meshes/special_mount"

MIRROR_LIST1 = os.listdir(DEFALUT_MIRROR_PATH)
MIRROR_LIST = []
for i in MIRROR_LIST1:
  a,b,c = str.partition(i, ".")
  if "stl" in c:
    MIRROR_LIST.append(a)

LENS_LIST1 = os.listdir(DEFALUT_LENS_PATH)
LENS_LIST = []
for i in LENS_LIST1:
  a,b,c = str.partition(i, ".")
  if "stl" in c:
    LENS_LIST.append(a)
  
SPECIAL_LIST1 = os.listdir(DEFALUT_SPEIAL_MOUNT_PATH)
SPECIAL_LIST = []
for i in SPECIAL_LIST1:
  a,b,c = str.partition(i, ".")
  if "stl" in c:
    SPECIAL_LIST.append(a)
del a,b,c,i,SPECIAL_LIST1,LENS_LIST1,MIRROR_LIST1


def get_mount_by_aperture_and_element(aperture, elm_type, elm_thickness):
  if elm_type == "Lens":
    if aperture<= 25.4/2:
      model = "MLH05_M"
    elif aperture <= 25.4:
      model = "LMR1_M"
    elif aperture <= 25.4*1.5:
      model = "LMR1.5_M"
    elif aperture <=25.4*2:
      model = "LMR2_M"
    post = "0.5inch_post"
  elif elm_type == "Mirror" or elm_type == "Curved_Mirror":
    post = "1inch_post"
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
      model = "6inch_mirror_mount"
      post = "big_post"
  else:
    return Unit_Mount()
  
  Output_mount = Composed_Mount(unit_model_list=[model,post])
  Output_mount.mount_list[0].element_thickness = elm_thickness
  Output_mount.mount_list[0].aperture = aperture
  
  if aperture>25.4*4:
    first = Output_mount.mount_list[0]
    x,y,z = first.get_coordinate_system()
    first.pos += x * first.element_thickness
    Output_mount.set_geom(Output_mount.get_geom())
  # else:
  #   Output_mount.add(Post_Marker())
  return Output_mount


class Unit_Mount(Geom_Object):
  """
  Mount class, erbit from <Geom_Object>
  Application as follows:
    Mon = Mount(elm_type="mirror")
  Usually exists as part of the component
  """
  # def __init__(self, name="mount",model="default", **kwargs):
  def __init__(self, model="dont_draw", name="mount",element_thickness=5, **kwargs):
    super().__init__(name, **kwargs)
    self.model = model
    self.path = ""
    self.docking_obj = Geom_Object()
    self.element_thickness = element_thickness #standard thickness of for example a mirror
    self.aperture = 25.4
    self.is_horizontal = True
    self.flip_angle = 0
    self.freecad_model = load_STL
    if self.model != "dont_draw":
      self.set_by_table()
      self.draw_dict["stl_file"] = self.path + self.model + ".stl"
      # self.draw_dict["color"] = DEFAULT_MOUNT_COLOR

  def set_axes(self, new_axes):
    if self.is_horizontal:
      old_axes = self.get_axes()
      newx, newy, newz = new_axes[:,0], new_axes[:,1], new_axes[:,2]
      newx = np.array((newx[0],newx[1],0))
      newx *= 1/np.linalg.norm(newx)
      newz = np.array((0,0,1))
      newy = np.cross(newz, newx)
      self._axes[:,0] = newx
      self._axes[:,1] = newy
      self._axes[:,2] = newz
      self._axes_changed(old_axes, self.get_axes())
    else:
      super().set_axes(new_axes)
    
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
        model_type = "special_mount"
        # return False
    folder = thisfolder+"mount_meshes/"+model_type+"/"
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
        self.draw_dict["color"] = eval(mount_loop["color"])
        # eval
    if not mount_in_database:
      print("The mount '", self.model, "' is not in the database.")
      self.path = folder
      return False
    self.aperture = aperture
    docking_normal = np.array((DockNormalX,DockNormalY,DockNormalZ))
    # self.docking_obj = Geom_Object()
    self.docking_obj.pos = self.pos+DockingX*self._axes[:,0]+DockingY*self._axes[:,1]+DockingZ*self._axes[:,2]
    self.docking_obj.normal = docking_normal
    self.path = folder
    return True
  
  def reverse(self):
    x,y,z = self.get_coordinate_system()
    self.rotate(z, np.pi)
    self.pos += x * self.element_thickness
    
  def flip(self, angle=90):
    self.flip_angle = angle
  

  def update_draw_dict(self):
    super().update_draw_dict()
    modified_axes = self.get_axes()
    modified_axes = np.matmul(rotation_matrix(self.normal, self.flip_angle/180*np.pi), modified_axes)
    self.draw_dict["geom"] = (self.pos, modified_axes)
    self.draw_dict["stl_file"] = self.path + self.model + ".stl"
    
  def draw_text(self):
    txt = super().draw_text()
    txt += " and the model " + self.model
  
  def __repr__(self):
    txt = super().__repr__()
    ind = txt.index(",")
    txt2 = txt[0:ind] + ', model="' + self.model + '"' + txt[ind::]
    return txt2

  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj])
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj])


class Post(Geom_Object):
  def __init__(self, name="post",model="1inch_post", **kwargs):
    super().__init__(name, **kwargs)
    self.axis_fixed = True
    self._lower_limit = 0
    self.draw_dict["post_color"] = DEFALUT_POST_COLOR
    self.draw_dict["holder_color"] = DEFALUT_HOLDER_COLOR
    self.model=model
    self.docking_obj = Geom_Object()
  
  def set_axes(self, new_axes):
    if self.axis_fixed:
      self._axes = np.eye(3)
    else:
      super().set_axes(new_axes)
  
  def find_1inch_post(self):
    height = self.pos[2] - self._lower_limit
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
    return draw_1inch_post(name=model,h_diff = height_difference,ll=self._lower_limit,
                            color=self.draw_dict["post_color"],geom = self.get_geom())
  
  def draw_post_part(self,name="post_part", base_exists=False, 
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
    POS[2]-=self._lower_limit
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
          post2 = draw_post_holder(name="PH20E_M", ll=self._lower_limit,
                                   color=holder_color, geom=geom)
        POS[2]+=self._lower_limit
        post = draw_post(name="TR"+str(post_length)+"_M", color=post_color,geom=geom)
        if post_length>20:
          post2 = draw_post_holder(name="PH"+str(post_length)+"_M", ll=self._lower_limit,
                                   color=holder_color, geom=geom)
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
          post2 = draw_post_holder(name="PH"+str(post_length)+"E_M", ll=self._lower_limit,
                                   color=holder_color, geom=geom)
        POS[2]+=self._lower_limit
        post = draw_post(name="TR"+str(post_length)+"_M", color=post_color,geom=geom)
        post2 = draw_post_holder(name="PH"+str(post_length)+"E_M", ll=self._lower_limit,
                                 color=holder_color, geom=geom)
    if base_exists:
      if post_length>90 or post_length<31:
          post1 = draw_post_base(name="BA2_M", geom=geom)
      else:
          post1 = draw_post_base(name="BA1L",  geom=geom)
    else:
      post1 = None
    # print(name,"'s height=",POS[2]+post_length)
    # print(name,"'s height=",POS[2])
    part = initialize_composition_old(name=name)
    container = post,post1,post2
    add_to_composition(part, container)
    return part
  
  def set_lower_limit(self,lower_limit):
    self._lower_limit = lower_limit
    self.docking_obj.pos = np.array((self.pos[0],self.pos[1],self._lower_limit))
  
  def _pos_changed(self, old_pos, new_pos):
    self.docking_obj.pos = np.array((self.pos[0],self.pos[1],self._lower_limit))
  
  def draw_freecad(self, **kwargs):
    self.draw_dict["geom"]=self.get_geom()
    self.draw_dict["name"] = self.name 
    if self.model == "dont_draw":
      return None
    # print(self.name,"'s position = ",self.pos)
    if self.model == "1inch_post":
      return self.find_1inch_post()
    elif self.model == "0.5inch_post":
      return self.draw_post_part(**self.draw_dict)
    else:
      return draw_large_post(height=self.pos[2],geom=self.get_geom())



class Composed_Mount(Geom_Object):
  """
  This one is for compositions of mulitple mounts stacked togehter
  The add function drags every new mount to the docking position of the old one
  and as usual all are moved correctly when the Composed_Mount is moved.
  
  Example: cm = Composed_Mount(unit_model_list=["KS1", "1inch_post"])
  """
  def __init__(self, unit_model_list=[], **kwargs):
    self.unit_model_list = unit_model_list
    self.mount_list = []
    super().__init__(**kwargs)
    self.docking_obj = Geom_Object()
    self.docking_obj.set_geom(self.get_geom())
    for model in self.unit_model_list:
      if "Marker" in model:
        newmount = Post_Marker()
      elif "post" in model:
        newmount = Post(model=model)
      elif "Angular" in model:
        newmount = Adaptive_Angular_Mount()
      else:  
        newmount = Unit_Mount(model=model)
      self.add(newmount)
    
  def add(self, mount):
    mount.set_geom(self.docking_obj.get_geom())
    self.mount_list.append(mount)
    self.docking_obj.set_geom(mount.docking_obj.get_geom())
    
  def draw_freecad(self):
    part = initialize_composition_old(name="mount, post and base")
    container = []
    for mount in self.mount_list:
      # container.append(mount.draw_fc())
      container.append(mount.draw())
    add_to_composition(part, container)
    return part
  
  def reverse(self):
    first = self.mount_list[0]
    first.reverse()
    self.set_geom(self.get_geom()) # to adjust the other elements
    
  def __repr__(self):
   txt = super().__repr__()
   ind = txt.index(",")
   modellist = str([um.model for um in self.mount_list])
   txt2 = txt[0:ind] + ', unit_model_list=' + modellist + txt[ind::]
   return txt2
    
  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos(old_pos, new_pos,[self.mount_list[0]])
    for mount_number in range(len(self.mount_list)-1):
      first = self.mount_list[mount_number]
      second = self.mount_list[mount_number+1]
      second.pos = first.docking_obj.pos
  
  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.mount_list[0]])
    for mount_number in range(len(self.mount_list)-1):
      first = self.mount_list[mount_number]
      second = self.mount_list[mount_number+1]
      second.set_geom(first.docking_obj.get_geom())



class Stripe_Mirror_Mount(Composed_Mount):
  def __init__(self, mirror_thickness=10,**kwargs):
    super().__init__(**kwargs)
    self.docking_obj.pos += self.normal * mirror_thickness
    stripe = Unit_Mount("Stripe_mirror_mount")
    self.add(stripe)
    self.add(Unit_Mount("POLARIS-K2"))
    self.add(Post())
    
class Rooftop_Mirror_Mount(Composed_Mount):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    roof = Unit_Mount("Rooftop_mirror_mount")
    self.add(roof)
    self.add(Unit_Mount("POLARIS-K2"))
    self.add(Post())

class Grating_Mount(Composed_Mount):
  def __init__(self,height=50,thickness=8, **kwargs):
    super().__init__(**kwargs)
    self.height = height
    self.thickness = thickness
    gratingmount = Unit_Mount()
    gratingmount.draw_dict["height"] = self.height
    gratingmount.draw_dict["thickness"] = self.thickness
    gratingmount.freecad_model = grating_mount#(height=self.height,thickness=self.thickness)
    gratingmount.docking_obj.pos += (9+self.thickness,0,0)
    gratingmount.docking_obj.normal = (1,0,0)
    if self.height<26 and self.height>24:
      gratingmount.path = thisfolder+"mount_meshes/Grating/"
      gratingmount.model = "Grat_designed_mount"
      # gratingmount.draw_dict["stl_file"] = thisfolder+"mount_meshes/Grating/Grat_designed_mount.stl"
      gratingmount.freecad_model = load_STL
      gratingmount.docking_obj.pos -= (3.9,0,0)
    self.add(gratingmount)
    self.add(Unit_Mount("POLARIS-K1"))
    self.add(Post())
    

class Post_Marker(Unit_Mount):
  def __init__(self, name="Post_Marker",size=3,**kwargs):
    super().__init__(name,**kwargs)
    self.name = name + "'s holder"
    self.size = size
    self.quot_x = math.floor(self.pos[0]/(25*size))
    self.quot_y = math.floor(self.pos[1]/(25*size))
    self.h1 = (self.quot_x*(25*size),self.quot_y*(25*size))
    if self.pos[0]-self.h1[0]<16:
      self.h1=(self.h1[0]-25,self.h1[1])
    if self.pos[1]-self.h1[1]<16:
      self.h1=(self.h1[0],self.h1[1]-25)
    if self.h1[0]+(25*size)-self.pos[0]<16:
      self.h1=(self.h1[0]+25,self.h1[1])
    if self.h1[1]+(25*size)-self.pos[1]<16:
      self.h1=(self.h1[0],self.h1[1]+25)
    self.freecad_model = model_Post_Marker
    
  def _pos_changed(self, old_pos, new_pos):
    self.quot_x = math.floor(new_pos[0]/(25*self.size))
    self.quot_y = math.floor(new_pos[1]/(25*self.size))
    self.h1 = (self.quot_x*(25*self.size),self.quot_y*(25*self.size))
    if new_pos[0]-self.h1[0]<16:
      self.h1=(self.h1[0]-25,self.h1[1])
    if new_pos[1]-self.h1[1]<16:
      self.h1=(self.h1[0],self.h1[1]-25)
    if self.h1[0]+(25*self.size)-new_pos[0]<16:
      self.h1=(self.h1[0]+25,self.h1[1])
    if self.h1[1]+(25*self.size)-new_pos[1]<16:
      self.h1=(self.h1[0],self.h1[1]+25)
  
  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["h1"] = self.h1
    self.draw_dict["h2"] = (self.h1[0]+(25*self.size),self.h1[1])
    self.draw_dict["h3"] = (self.h1[0]+(25*self.size),self.h1[1]+(25*self.size))
    self.draw_dict["h4"] = (self.h1[0],self.h1[1]+75)
    # print(self.name," holes' pos=",self.h1,(self.h1[0]+(25*self.size),self.h1[1]),
    #       (self.h1[0]+(25*self.size),self.h1[1]+(25*self.size)),
    #       (self.h1[0],self.h1[1]+(25*self.size)))

class Adaptive_Angular_Mount(Unit_Mount):
  def __init__(self, aperture=25.4,angle = 30,**kwargs):
    super().__init__(**kwargs)
    self.aperture = aperture
    self.angle = angle
    self.docking_obj = Geom_Object()
    self.rot_angle = abs(90-angle)
    dia_l = int(aperture/10+1)*10
    self.docking_obj.pos = self.pos+self.normal * (dia_l/(2*np.tan(self.rot_angle/180*np.pi))+1.5)
    self.docking_obj.normal = self.normal
    self.freecad_model = model_mirror_holder
    
  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["dia"] = self.aperture
    self.draw_dict["angle"] = self.rot_angle
  
  def set_axes(self, new_axes):
    if abs(new_axes[2][0])>0:
      z=-new_axes[2][0]
      self.angle = np.arcsin(z)*180/np.pi
      dia_l = int(self.aperture/10+1)*10
      self.docking_obj.normal = self.normal
      if self.angle>0:
        self.rot_angle = (90-self.angle) 
        self.docking_obj.pos = self.pos+self.normal * (dia_l/(2*np.tan(self.rot_angle/180*np.pi))+1.5)
      else:
        self.rot_angle = (-90-self.angle) 
        self.docking_obj.pos = self.pos+self.normal * (dia_l/(2*np.tan(-self.rot_angle/180*np.pi))+1.5)
    elif new_axes[2][0]>0:
      z=new_axes[2][0]
      self.angle = np.arcsin(z)*180/np.pi
      self.rot_angle = abs(90-self.angle)
      dia_l = int(self.aperture/10+1)*10
      self.docking_obj.pos = self.pos+self.normal * (dia_l/(2*np.tan(self.rot_angle/180*np.pi))+1.5)
      self.docking_obj.normal = self.normal
    super().set_axes(new_axes)
    
  # def reverse(self):
  #   x,y,z = self.get_coordinate_system()
  #   self.rotate(z, np.pi)
  #   self.pos += x * self.element_thickness
    

# class Special_mount(Unit_Mount):
#   """
#   in fact only for rooftop mirrors and stripe mirrors
#   maybe deleted in the next version or more generalized
#   """
#   def __init__(self, name="special_mounmt",model="special_mount",aperture=25.4,thickness=10,
#                docking_pos = (1,2,3),docking_normal=(0,0,1),drawing_post=False, **kwargs):
#     super().__init__(name, **kwargs)
#     self.draw_dict["aperture"] = aperture
#     self.aperture = aperture
#     self.draw_dict["thickness"] = thickness
#     self.thickness = thickness
#     self.draw_dict["geom"]=self.get_geom()
#     self.model = model
#     self.drawing_post = drawing_post
#     if model=="rooftop mirror mount":
#       self.post = None
#       xshift = 38
#       zshift = -5
#       docking_pos = (xshift,0,zshift)
#       docking_normal = self.normal
#     if model == "Stripe mirror mount":
#       xshift = 24
#       yshift = 104.3
#       self.post = None
#       docking_pos = (xshift,yshift,0)
#       docking_normal = -self.normal
#     self.docking_obj = Geom_Object()
#     self.docking_obj.pos = self.pos+docking_pos[0]*self._axes[:,0]+docking_pos[1]*self._axes[:,1]+docking_pos[2]*self._axes[:,2]
#     self.docking_obj.normal=docking_normal
#     if drawing_post:
#       post = Post_and_holder(name=self.name + "post",elm_type=self.elm_type)
#       post.set_geom(self.docking_obj.get_geom())
#       self.post = post
  
#   def set_geom(self, geom):
#     """
#     since the position of rooftop mirror and stripe mirror are related to the 
#     aperture and thickness of the mirror itself, the are some changes that must 
#     be made in the geom setting.

#     """
#     if np.shape(geom[1])==(3,3):
#       normal = geom[1][:,0]
#     else:
#       normal = geom[1]
#     if self.model != "Stripe mirror mount" and self.model != "rooftop mirror mount":
#       self.pos = np.array(geom[0])
#       self.set_axes(geom[1])
#       return 1
#     if self.model =="Stripe mirror mount":
#       new_pos = np.array((self.thickness-25,0,0))
#     elif self.model == "rooftop mirror mount":
#       new_pos = np.array((self.aperture/2,0,0))
#     a = (1,0,0)
#     if np.sum(np.cross(a,normal))!=0:
#       rot_axis = np.cross(a,normal)/np.linalg.norm(np.cross(a,normal))
#       rot_angle = np.arccos(np.sum(a*normal)/(np.linalg.norm(a)*np.linalg.norm(normal)))
#       new_pos = rotate_vector(new_pos,rot_axis,rot_angle)
#     if np.sum(np.cross(a,normal))==0 and normal[0]<-0.999:
#       geom0 = np.array(geom[0] - new_pos)
#     else:
#       geom0 = np.array(geom[0] + new_pos)
#     self.pos = np.array(geom0)
#     self.set_axes(geom[1])
    
#   @property
#   def docking_pos(self):
#     return np.array(self.docking_obj.pos) * 1.0
#   @docking_pos.setter
#   def docking_pos(self, x):
#     self.docking_pos = np.array(x) * 1.0
#     self.docking_obj.pos = self.docking_pos
  
#   @property
#   def docking_normal(self):
#     return np.array(self.docking_obj.normal) * 1.0
#   @docking_normal.setter
#   def docking_normal(self, x):
#     self.docking_normal = np.array(x) * 1.0
#     self.docking_obj.normal = self.docking_normal
  
#   def _pos_changed(self, old_pos, new_pos):
#     if self.post != None:
#       self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj,self.post])
#     else:
#       self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj])
  
#   def _axes_changed(self, old_axes, new_axes):
#     if self.post != None:
#       self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj,self.post])
#     else:
#       self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj])
  
#   def draw_fc(self):
#     if self.model=="rooftop mirror mount" or self.model=="Stripe mirror mount":
#       self.draw_dict["geom"]=self.get_geom()
#       self.draw_dict["stl_file"]=thisfolder+"/mount_meshes/special mount/" + self.model + ".stl"
#       return load_STL(**self.draw_dict)
#       # return mirror_mount(**self.draw_dict)
#     else:
#       if self._axes[2,2] <-0.9:
#         self.rotate(self.normal,np.pi)
#         self.draw_dict["geom"] = self.get_geom()
#       self.draw_dict["geom"]=self.get_geom()
#       self.draw_dict["stl_file"]=thisfolder+"/mount_meshes/special mount/" + self.model + ".stl"
#       obj = load_STL(**self.draw_dict)
#       if self.drawing_post:
#         obj1 = self.post.draw()
#         part = initialize_composition_old(name="mount, post and base")
#         container = obj,obj1
#         add_to_composition(part, container)
#         return part
#       else:
#         return obj
    
