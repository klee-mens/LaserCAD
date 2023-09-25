# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 14:40:56 2023

@author: mens
"""

# from ..basic_optics import Component
# from ..freecad_models.utils import thisfolder, load_STL
# from ..freecad_models.freecad_model_mounts import load_mount_from_csv

import sys
sys.path.append('C:\\ProgramData\\Anaconda3')
from LaserCAD.basic_optics import Component
from LaserCAD.freecad_models.utils import thisfolder,load_STL,freecad_da
from LaserCAD.freecad_models.freecad_model_mounts import load_mount_from_csv,lens_mount,mirror_mount

import csv
import os
# DEFALUT_CAV_PATH = "C:\\ProgramData\\Anaconda3\\LaserCAD\\freecad_models"
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

if freecad_da:
  from FreeCAD import Vector, Placement, Rotation
  import Mesh
  import ImportGui
  import Sketcher
  import Part

DEFALUT_MOUNT_COLOR = (0.75,0.75,0.75)


class Mount(Component):
  def __init__(self, name="KS1", **kwargs):
    super().__init__(name, **kwargs)
    if name in MIRROR_LIST:
      stl_file=thisfolder+"\\mount_meshes\\mirror\\" + name + ".stl"
    elif name in LENS_LIST:
      stl_file=thisfolder+"\\mount_meshes\\lens\\" + name + ".stl"
    else:
      stl_file=thisfolder+"\\mount_meshes\\special mount\\" + name + ".stl"
    self.name = name
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=DEFALUT_MOUNT_COLOR
    self.draw_dict["geom"]=[self.pos,self.normal]
    # self.freecad_model = load_STL
    # mount_in_database = self.set_by_table()
    
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
    # place = Placement(offset, rotation, Vector(0,0,0))
    
    # if self.name in MIRROR_LIST:
    #   mount_in_database,aperture,height,price,xshift,place,offset = load_mount_from_csv(mount_type = self.name,model_type="mirror")
    # else:
    #   mount_in_database,aperture,height,price,xshift,place,offset = load_mount_from_csv(mount_type = self.name,model_type="lens")
    if not mount_in_database:
      # print("This mount was not in the table")
      return False
    self.aperture = aperture
    self.height = height
    self.price = price
    self.xshift = xshift
    self.offset_vector = offset
    self.post_docking_pos = (xshift,0,height)
    self.post_docking_direction = (0,0,1)
    self.rotation = rotation
    return True
  
  def draw_fc(self):
    self.update_draw_dict()
    if self.set_by_table():
      self.draw_dict["mount_type"] = self.name
      if self.name in MIRROR_LIST:
        return mirror_mount(mount_type=self.name,geom=self.draw_dict["geom"],drawing_post=False)
      else:
        return lens_mount(mount_type=self.name,geom=self.draw_dict["geom"],drawing_post=False)
    elif self.name in SPECIAL_LIST or self.name in MIRROR_LIST or self.name in LENS_LIST:
      return load_STL(**self.draw_dict)
    else:
      return("This mount is not in the correct folder")

M = Mount(name = "LMR1.5_M")
M.draw()
M1 = Mount(name = "H45CN")
M1.draw()