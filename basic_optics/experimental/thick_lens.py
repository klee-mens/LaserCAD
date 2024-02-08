# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 09:05:00 2023

@author: HE
"""

# from basic_optics import Opt_Element
# from .basic_optics.freecad_models import model_lens
from LaserCAD.freecad_models import model_lens, lens_mount
from LaserCAD.basic_optics.optical_element import Opt_Element
from LaserCAD.basic_optics.geom_object import TOLERANCE
from copy import deepcopy
import numpy as np

class Thick_Lens(Opt_Element):
  def __init__(self, radius1 = 300, radius2= 250,thickness = 10, n = 1.5, name="NewLens", **kwargs):
    super().__init__(name=name, **kwargs)
    # self.focal_length = f
    self.draw_dict["thickness"] = thickness #sieht schöner aus
    self.thickness = thickness
    self.draw_dict["Radius1"] = radius1
    self.R1 = radius1
    self.draw_dict["Radius2"] = radius2
    self.R2 = radius2
    self.draw_dict["Refractive_index"] = n
    self.Refractive_index = n
    if abs(radius1) < TOLERANCE:
      if abs(radius2) < TOLERANCE:
        self.focal_length = 0
        print("infinite focal length")
      else:
        self.focal_length = float(1 / ((n-1)*(1/radius2)))
    else:
      if abs(radius2) < TOLERANCE:
        self.focal_length = float(1 / ((n-1)*(1/radius1)))
      else:
        self.focal_length = float(1 / ((n-1)*(1/radius1+1/radius2)-(n-1)*(n-1)*thickness/(n*radius1*radius2)))
  @property
  def focal_length(self):
    return self.__f
  @focal_length.setter
  def focal_length(self, x):
    self.__f = x
    if x == 0:
      self._matrix[1,0] = 0
    else:
      self._matrix[1,0] = -1/x
  def next_ray(self, ray):
    if np.sum(self.normal*ray.normal)>0:
      ray2 = self.next_ray_surface_in(ray,center_pos=self.pos,R=self.R1,Norm=self.normal)
      # print(ray2)
      ray3 = self.next_ray_surface_out(ray2,center_pos=self.pos+self.normal*self.thickness,R=self.R2,Norm=self.normal)
      return ray3
    else:
      ray2 = self.next_ray_surface_in(ray,center_pos=self.pos+self.normal*self.thickness,R=self.R2,Norm=-self.normal)
      # print(ray2)
      ray3 = self.next_ray_surface_out(ray2,center_pos=self.pos,R=self.R1,Norm=-self.normal)
      # print(ray3)
      return ray3
    # return self.refraction(ray)
  
  def next_ray_surface_in(self,ray,center_pos,R,Norm):
    ray2 = deepcopy(ray)
    R_center = center_pos+R*Norm
    vec_a = R_center-ray.pos
    a = np.sqrt(vec_a[0]**2+vec_a[1]**2+vec_a[2]**2)
    if np.linalg.norm(vec_a)==0 and R!=0:
      prop_length=abs(R)
    else:
      normal1=vec_a/np.linalg.norm(vec_a)
      normal2=ray.normal/np.linalg.norm(ray.normal)
      # if np.sum(normal1*normal2)<0:
      #   normal1 = -normal1
      cos_theta = np.sum(normal1*normal2)
      sin_theta = np.sqrt(1-cos_theta**2)
      if R>0:
        prop_length = a*cos_theta-np.sqrt(R**2-a**2*sin_theta**2)
      elif R<0:
        prop_length = a*cos_theta+np.sqrt(R**2-a**2*sin_theta**2)
      else:
        delta_p = center_pos - ray.pos
        prop_length = np.sum(delta_p*Norm) / np.sum(ray.normal * Norm)
    # print(prop_length)
    end_point = ray.pos+ray.normal*prop_length
    ray.length = prop_length
    ray2.pos = end_point
    norm = ray2.normal
    if R ==0:
      ea = Norm
      if np.sum(ea*norm)<0:
        ea =-ea
    elif R>0:
      ea = (R_center-end_point)
      ea = ea/np.linalg.norm(ea)
    else:
      ea = -(R_center-end_point)
      ea = ea/np.linalg.norm(ea)
    ref = 1/self.Refractive_index
    muti = np.sum(norm*ea)#norm[0]*ea[0]+norm[1]*ea[1]+norm[2]*ea[2]#np.sum(norm*ea)
    norm2 = ref * norm - ref*(muti)*ea + pow(1-ref**2*(1-muti**2),0.5)*ea
    muti2 = np.sum(norm2*ea)#norm2[0]*ea[0]+norm2[1]*ea[1]+norm2[2]*ea[2]
    if muti2 < 0 :
        norm2 = ref * norm - ref*(muti)*ea - pow(1-ref**2*(1-muti**2),0.5)*ea
    ray2.normal = norm2
    return ray2
  
  def next_ray_surface_out(self,ray,center_pos,R,Norm):
    ray2 = deepcopy(ray)
    R_center = center_pos-R*Norm
    vec_a = R_center-ray.pos
    a = np.sqrt(vec_a[0]**2+vec_a[1]**2+vec_a[2]**2)
    if np.linalg.norm(vec_a)==0 and R!=0:
      prop_length=abs(R)
    else:
      normal1=vec_a/np.linalg.norm(vec_a)
      normal2=ray.normal/np.linalg.norm(ray.normal)
      # if np.sum(normal1*normal2)<0:
      #   normal1 = -normal1
      cos_theta = np.sum(normal1*normal2)
      sin_theta = np.sqrt(1-cos_theta**2)
      if R<0:
        prop_length = a*cos_theta-np.sqrt(R**2-a**2*sin_theta**2)
      elif R>0:
        prop_length = a*cos_theta+np.sqrt(R**2-a**2*sin_theta**2)
      else:
        delta_p = center_pos - ray.pos
        prop_length = np.sum(delta_p*Norm) / np.sum(ray.normal * Norm)
    # print(prop_length)
    end_point = ray.pos+ray.normal*prop_length
    ray.length = prop_length
    ray2.pos = end_point
    norm = ray2.normal
    if R ==0:
      ea = Norm
      if np.sum(ea*norm)<0:
        ea =-ea
    elif R>0:
      ea = -(R_center-end_point)
      ea = ea/np.linalg.norm(ea)
    else:
      ea = (R_center-end_point)
      ea = ea/np.linalg.norm(ea)
    ref = self.Refractive_index
    muti = norm[0]*ea[0]+norm[1]*ea[1]+norm[2]*ea[2]#np.sum(norm*ea)
    norm2 = ref * norm - ref*(muti)*ea + pow(1-ref**2*(1-muti**2),0.5)*ea
    muti2 = norm2[0]*ea[0]+norm2[1]*ea[1]+norm2[2]*ea[2]
    # print(norm2)
    if muti2 <= 0 :
        norm2 = ref * norm - ref*(muti)*ea - pow(1-ref**2*(1-muti**2),0.5)*ea
    ray2.normal = norm2
    return ray2
  
  def draw_fc(self):
    self.update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    # model_lens(self.name, dia=self.aperture, geom_info=self.get_geom())
    return model_lens(**self.draw_dict)

  def draw_mount_fc(self):
    return lens_mount(**self.draw_dict)

  def __repr__(self):
    n = len(self.class_name())
    txt = 'Thick Lens(f=' + repr(self.focal_length)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def from_dict(dc):
    oe = Opt_Element()
    oe.name = dc["name"]
    oe.pos = dc["pos"]
    oe.normal = dc["normal"]
    oe._axes = dc["axes"]
    oe._matrix = dc["matrix"]
    oe.aperture = dc["aperture"]
    oe.group = dc["group"]
    return oe