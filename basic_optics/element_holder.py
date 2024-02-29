# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 14:21:51 2024

@author: 庄赫
"""

from .mirror import Mirror
from .mount import Post_Marker

class Element_Marker(Post_Marker):
  def __init__(self, element=Mirror(),size=2,**kwargs):
    self.size = size
    self.element = element
    super().__init__(**kwargs)
    self.freecad_model 

  def update_draw_dict(self):
    super().update_draw_dict()
    # self.draw_dict["h1"] = self.h1
    # self.draw_dict["h2"] = (self.h1[0]+(25*self.size),self.h1[1])
    # self.draw_dict["h3"] = (self.h1[0]+(25*self.size),self.h1[1]+(25*self.size))
    # self.draw_dict["h4"] = (self.h1[0],self.h1[1]+75)
    # print(self.name," holes' pos=",self.h1,(self.h1[0]+(25*self.size),self.h1[1]),
    #       (self.h1[0]+(25*self.size),self.h1[1]+(25*self.size)),
    #       (self.h1[0],self.h1[1]+(25*self.size)))
    self.draw_dict["element"] = self.element.freecad_model
    