# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 14:41:08 2023

@author: mens
"""
import sys
sys.path.append('C:\\ProgramData\\Anaconda3')
# from LaserCAD.basic_optics import Component
# from .component import Component
from LaserCAD.freecad_models.utils import thisfolder,load_STL,freecad_da,clear_doc
from LaserCAD.freecad_models.freecad_model_composition import initialize_composition_old,add_to_composition
from LaserCAD.freecad_models.freecad_model_mounts import draw_post,draw_post_holder,draw_post_base
from LaserCAD.basic_optics.geom_object import Geom_Object
# from LaserCAD.non_interactings.mount import Mount,Special_mount
from copy import deepcopy
import csv
import os
import numpy as np


DEFALUT_POST_COLOR = (0.8,0.8,0.8)
DEFALUT_HOLDER_COLOR = (0.2,0.2,0.2)

class Post_and_holder(Geom_Object):
  def __init__(self, name="post",elm_type="default",xshift=0,height=12, **kwargs):
    super().__init__(name, **kwargs)
    self.xshift=xshift
    self.height=height
    self.post_color = DEFALUT_POST_COLOR
    self.holder_color = DEFALUT_HOLDER_COLOR
    self.elm_type = elm_type
  
  def set_axes(self, new_axes):
    self._axes = np.eye(3)
  
  def draw_fc(self):
    self.draw_dict["xshift"]=0
    self.draw_dict["height"]=0
    self.draw_dict["geom"]=self.get_geom()
    self.draw_dict["post_color"] = self.post_color
    self.draw_dict["holder_color"] = self.holder_color
    if self.elm_type == "dont_draw":
      return None
    return draw_post_part(**self.draw_dict)
    

def draw_post_part(name="post_part", base_exists=False, height=12,xshift=0,
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
  # AXES = geom[1]
  # if np.shape(AXES)==(3,):
  #   NORMAL=AXES
  # else:
  #   NORMAL=AXES[:,0]
  if (POS[2]-height<34) or (POS[2]-height>190):
    print("Warning, there is no suitable post holder and slotted base at this height")
    return None
  post_length=50
  if base_exists:
      if POS[2]-height>110:
        post_length=100
      elif POS[2]-height>90:
        post_length=75
      elif POS[2]-height>65:
        post_length=50
      elif POS[2]-height>55:
        post_length=40
      elif POS[2]-height>40:
        post_length=30
      else:
        post_length=20
        post2 = draw_post_holder(name="PH20E_M", height=0,xshift=xshift,
                                 color=holder_color, geom=geom)
      post = draw_post(name="TR"+str(post_length)+"_M", height=height,
                       xshift=xshift,color=post_color,geom=geom)
      if post_length>20:
        post2 = draw_post_holder(name="PH"+str(post_length)+"_M", height=0,
                                 xshift=xshift,color=holder_color, geom=geom)
  else:
      if POS[2]-height>105:
        post_length=100
      elif POS[2]-height>85:
        post_length=75
      elif POS[2]-height>60:
        post_length=50
      elif POS[2]-height>50:
        post_length=40
      elif POS[2]-height>35:
        post_length=30
      else:
        post_length=20
        post2 = draw_post_holder(name="PH"+str(post_length)+"E_M", height=0,
                                 xshift=xshift,color=holder_color, geom=geom)
      post = draw_post(name="TR"+str(post_length)+"_M", height=height,
                       xshift=xshift,color=post_color,geom=geom)
      post2 = draw_post_holder(name="PH"+str(post_length)+"E_M", height=0,
                               xshift=xshift,color=holder_color, geom=geom)
  if base_exists:
    if post_length>90 or post_length<31:
        post1 = draw_post_base(name="BA2_M", height=0,xshift=xshift, geom=geom)
    else:
        post1 = draw_post_base(name="BA1L", height=0,xshift=xshift, geom=geom)
  else:
    post1 = None
  
  part = initialize_composition_old(name=name)
  container = post,post1,post2
  add_to_composition(part, container)
  return part

# if freecad_da:
#   clear_doc()
# M1 = Special_mount(name = "H45CN",docking_pos=(22,22,0),docking_normal=(1,1,0),normal=(1,1,0),pos=(0,0,100))
# M1.normal=(1,0,0)
# M1.draw()
# M2= Mount(name="POLARIS-K2",pos=M1.docking_pos,normal=M1.docking_normal)
# M2.draw()
# M=Post_and_holder(xshift=M2.xshift,height=-M2.zshift,pos=M2.pos,normal=M2.normal)
# # M=Post_and_holder(**M2.draw_dict)
# M.pos += (10,20,5)
# M.draw()