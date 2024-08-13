# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:34:44 2022

@author: mens
"""

# from basic_optics import Ray, Geom_Object, TOLERANCE
from . constants import TOLERANCE
from . geom_object import Geom_Object
from . ray import Ray
# from .. freecad_models import model_beam,model_ray_1D,model_Gaussian_beam
# from .. freecad_models import model_Gaussian_beam, model_beam
# from .. freecad_models.freecad_model_beam import model_beam_new
from .. freecad_models import model_beam,model_ray_1D,model_Gaussian_beam,model_Gaussian_beam_cone
from .. freecad_models.freecad_model_composition import initialize_composition_old, add_to_composition

from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt




class Beam(Geom_Object):
  """
  Base class for a group of rays (you don't say!)
  special funcitoins: make_square_distribution(radius=1, ray_count=5)
  make_circular_distribution(radius=1, ray_count=5)
  average_divegence = ?

  """
  def __init__(self, radius=1, angle=0, name="NewBeam", wavelength=1030E-6, 
               ray_count = 2, **kwargs):
    super().__init__(name=name, **kwargs)
    self._ray_count = ray_count
    self._rays = [Ray() for n in range(self._ray_count)]
    self._angle = angle
    self._radius = radius
    self._Bwavelength = wavelength
    self.make_cone_distribution(ray_count)
    self._distribution = "cone"
    self.draw_dict["model"] = "cone"
    self.freecad_model = model_beam

  def make_cone_distribution(self, ray_count=2):
    self._ray_count = ray_count
    self._rays = [Ray() for n in range(self._ray_count)]
    mr = self._rays[0]
    mr.set_geom(self.get_geom())
    mr.name = self.name + "_inner_Ray"
    mr.wavelength = self._Bwavelength
    thetas = np.linspace(0, 2*np.pi, self._ray_count)
    for n in range(self._ray_count-1):
      our = self._rays[n+1]
      our.from_h_alpha_theta(self._radius, self._angle, thetas[n], self)
      our.name = self.name + "_outer_Ray" + str(n)
      our.wavelength = self._Bwavelength

  def override_rays(self, rays):
    """
    setzt die rays neu, muss man eventuell aufpassen, mal sehen

    resets the rays, you may have to watch out, let's see

    Parameters
    ----------
    rays : list of rays
    """
    rc = len(rays)
    self._ray_count = rc
    self._rays = rays
    self._axes = rays[0].get_axes()
    self._pos = rays[0].pos
    for n in range(len(rays)):
      rays[n].name = self.name + "_ray" + str(n)
    rays[0].name = self.name + "_middle_ray"

  def radius_angle(self):
    """
    berechnet aus 2 Strahlen inn und outer den zugehörigen beam Kegel mit
    radius r und öffnungswinkel alpha und zwar von hinten durch die Brust
    ins Auge
    """
    inner = self._rays[0]
    outer = self._rays[1]
    v0 = inner.normal
    v1 = outer.normal
    poi = outer.intersection(inner, False) #Punkt in der Kegelgrundfläche, in dem outer schneidet
    ovec = poi - inner.pos
    novec = np.linalg.norm(ovec)
    if novec < TOLERANCE:
      #beide rays im gleichen Punkt, h = 0, alpha>0
      # print("AAAAAAASSDFJEOGERWOGJ")
      # print("v0*v1:", np.sum(v0 * v1))
      return novec, np.arccos(np.clip(np.sum(v0 * v1), -1.0, 1.0))
    else:
      ovec /= novec #normieren
      a = np.sum(v1 * ovec)
      b = np.sum(v0 * v1)
    return novec, np.arctan(a/b)

  def get_all_rays(self, by_reference=False):
    if by_reference:
      return self._rays
    else:
      return deepcopy(self._rays)

  def inner_ray(self):
    return deepcopy(self._rays[0])

  def outer_rays(self):
    return deepcopy(self._rays[1::])

  def focal_length(self):
    r, alph = self.radius_angle()
    if alph == 0:
      return 0
    else:
       return - r/np.tan(alph)

  def length(self):
    return self.inner_ray().length

  def set_length(self, x):
    for ray in self._rays:
      ray.length = x
      
  def set_wavelength(self, wl):
    for ray in self._rays:
      ray.length = wl


  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird
    ändert die Position aller __rays mit

    is called when the position of <self> is changed
    changes the position of all __rays with
    """
    super()._pos_changed(old_pos, new_pos)
    self._rearange_subobjects_pos(old_pos, new_pos, self._rays)

  def _axes_changed(self, old_axes, new_axes):
    """
    wird aufgerufen, wen das KooSys <_axes> von <self> verändert wird
    dreht die KooSys aller __rays mit

    dreht außerdem das eigene Koordiantensystem

    is called when the KooSys <_axes> is changed from <self>.
    rotates the KooSys of all __rays as well

    also rotates the own coordiante system
    """
    super()._axes_changed(old_axes, new_axes)
    self._rearange_subobjects_axes(old_axes, new_axes, self._rays)

  def __repr__(self):
    radius, angle = self.radius_angle()
    txt = 'Beam(radius=' + repr(radius)
    txt += ', anlge=' + repr(angle)
    txt += ', distribution=' + repr(self._distribution)
    txt += ', ' + super().__repr__()[6::]
    return txt

  def update_draw_dict(self):
    super().update_draw_dict()
    radius, angle = self.radius_angle()
    self.draw_dict["length"] = self.length()
    self.draw_dict["radius"] = radius
    self.draw_dict["angle"] = angle
  
  def draw_freecad(self):
    if self.draw_dict["model"] == "cone":
      # radius, angle = self.radius_angle()
      self.update_draw_dict()
      return self.freecad_model(**self.draw_dict)
      # return model_beam(radius=radius, length=self.length(),  angle=angle,
                            # geom=self.get_geom(), name=self.name)
    else:
      part = initialize_composition_old(name="ray group")
      container = []
      for nn in range(self._ray_count):
        our=self._rays[nn]
        obj = our.draw_freecad()
        container.append(obj)
      add_to_composition(part, container)
      return part



class SquareBeam(Beam):
  def __init__(self, radius=1, name="NewBeam", wavelength=1030E-6, ray_in_line = 3, **kwargs):
    super().__init__(name=name, **kwargs)
    self._radius = radius
    self._ray_in_line = ray_in_line
    self.make_square_distribution(ray_in_line)
    self._distribution = "square"
    self.draw_dict["model"] = "ray_group"

  def make_square_distribution(self, ray_in_line=3):
    """
    Let the group of rays follow the square distribution
    The width of square equals 2*radius of ray group
    Parameters
    ----------
    ray_in_line : int(>0)
      rays in a line.That is going to determine the density of ray.

    Returns
    -------
    None.

    """
    self._rays = [Ray() for n in range((ray_in_line)**2)]                     #calculate the number of rays,set the rays group
    ray_counting=0
    radius=self._radius
    for n in np.arange(-radius,radius+radius/(ray_in_line-1),
                       2*radius/(ray_in_line-1)):                              #n repersents y coordinates of the ray
      for m in np.arange(-radius,radius+radius/(ray_in_line-1),
                         2*radius/(ray_in_line-1)):                            #m repersents z coordinates of the ray
        self._rays[ray_counting].set_geom(self.get_geom())
        self._rays[ray_counting].pos=self._rays[ray_counting].pos+(0,n,m)     #change the position of the ray
        self._rays[ray_counting].name=self.name+str(ray_counting)
        self._rays[ray_counting].wavelength = self._Bwavelength
        ray_counting+=1
    self._ray_count = ray_counting
    
    for n in range(1, len(self._rays)):
      self._rays[n].name = self.name + "_Ray" + str(n)
    self._rays[0].name = self.name + "_inner_Ray"
    


class CircularRayBeam(Beam):
  def __init__(self, radius=1, name="NewBeam", wavelength=1030E-6, ring_number = 2, **kwargs):
    super().__init__(name=name, **kwargs)
    self._radius = radius
    self._Bwavelength = wavelength
    self._ring_number = ring_number
    self.make_circular_distribution(ring_number)
    # self._ray_count = len(self._rays)
    self._distribution = "circular"
    self.draw_dict["model"] = "ray_group"

  def make_circular_distribution(self, ring_number=2):
    """
    Let the group of rays follow the circular distribution
    The radius of circle equals the radius of ray group
    Parameters
    ----------
    ring_number : int(>0).
      The number of the rings around the center. That is going to
     determine the density of ray.

    Returns
    -------
    None.

    """

    self._rays = [Ray() for n in range(3*ring_number*(ring_number+1)+1)]      #calculate the number of rays,set the rays group
    ray_counting=0
    radius=self._radius
    for r in np.arange(0,radius+radius/ring_number/2,radius/ring_number):        #r repersents the height of the ray

      if r!=0:                                                                 #if the ray is not in the center
        thetas = np.linspace(0, 2*np.pi, int(r*ring_number/radius)*6+1)        #thetas repersents the rotation angle of the ray
        for n in range(int(r*ring_number/radius)*6):
          our=self._rays[ray_counting]
          # self._rays[ray_counting].wavelength = self._Bwavelength
          our.from_h_alpha_theta(r, self._angle, thetas[n], self)            # rotate the ray which is not in the center
          our.name=self.name + "_circular_distribution_Ray" +str(ray_counting)
          ray_counting+=1
      else:
        # self._rays[ray_counting].wavelength = self._Bwavelength
        mr=self._rays[ray_counting]
        mr.set_geom(self.get_geom())
        mr.name = self.name + "_inner_Ray"
        ray_counting+=1
    # print(ray_counting) # ray_counting is the number of the rays.
    self._ray_count = ray_counting
    # print(ray_counting)
    for r in range(0,self._ray_count):
      self._rays[r].wavelength = self._Bwavelength




# import matplotlib.pyplot as plt

class RainbowBeam(Beam):
  def __init__(self,  name="NewRainbow", wavelength=1030E-6, bandwith=10E-6, ray_count=11, **kwargs):
    super().__init__(name=name, **kwargs)
    self._Bwavelength = wavelength
    self._ray_count = ray_count
    self._bandwith = bandwith
    self.make_rainbow_distribution(ray_count)
    self._distribution = "rainbow"
    self.draw_dict["model"] = "ray_group"
    
  def make_rainbow_distribution(self, ray_count=11):
    self._ray_count = ray_count
    # wavels = np.linspace(self._Bwavelength - self.bandwith/2, self._Bwavelength + self.bandwith/2, ray_count)
    rc_blue = ray_count//2 +1
    rc_red = ray_count + 1 - rc_blue
    blue = np.linspace(self._Bwavelength - self._bandwith/2, self._Bwavelength, rc_blue)
    reds = np.linspace(self._Bwavelength, self._Bwavelength + self._bandwith/2, rc_red)
  
    wavels = [self._Bwavelength] # middle ray hat wavelength
    wavels += list(blue[0:-1]) # then all blue wavelength except middle 
    wavels += list(reds[1::]) # then all red wavelength except middle
    rays = []
    cmap = plt.cm.gist_rainbow
    for wavel in wavels:
      rn = Ray()
      rn.set_geom(self.get_geom())
      rn.wavelength = wavel
      x = 1-(wavel - self._Bwavelength + self._bandwith/2) / self._bandwith
      rn.draw_dict["color"] = cmap( x )
      rays.append(rn)
    self._rays = rays
    for n in range(1, len(self._rays)):
      self._rays[n].name = self.name + "_Ray" + str(n)
    self._rays[0].name = self.name + "_inner_Ray"
  

# =======
#     self._axes = rays[0].get_axes()
#     self._pos = rays[0].pos
#     for n in range(len(rays)):
#       rays[n].name = self.name + "_ray" + str(n)
#     rays[0].name = self.name + "_middle_ray"

  def __repr__(self):
    radius, angle = self.radius_angle()
    txt = 'Beam(radius=' + repr(radius)
    txt += ', anlge=' + repr(angle)
    txt += ', distribution=' + repr(self._distribution)
    if self._distribution == "Gaussian":
       txt = 'Gaussian_Beam(q_para=' + repr(self.q_para)
    txt += ', ' + super().__repr__()[6::]
    return txt

  def radius_angle(self):
    """
    berechnet aus 2 Strahlen inn und outer den zugehörigen beam Kegel mit
    radius r und öffnungswinkel alpha und zwar von hinten durch die Brust
    ins Auge
    """
    inner = self._rays[0]
    outer = self._rays[1]
    v0 = inner.normal
    v1 = outer.normal
    poi = outer.intersection(inner) #Punkt in der Kegelgrundfläche, in dem outer schneidet
    ovec = poi - inner.pos
    novec = np.linalg.norm(ovec)
    if novec < TOLERANCE:
      #beide rays im gleichen Punkt, h = 0, alpha>0
      return novec, np.arccos(np.sum(v0 * v1))
    else:
      ovec /= novec #normieren
      a = np.sum(v1 * ovec)
      b = np.sum(v0 * v1)
    return novec, np.arctan(a/b)

  def get_all_rays(self, by_reference=False):
    if by_reference:
      return self._rays
    else:
      return deepcopy(self._rays)

  def inner_ray(self):
    return deepcopy(self._rays[0])

  def outer_rays(self):
    return deepcopy(self._rays[1::])

  def focal_length(self):
    r, alph = self.radius_angle()
    if alph == 0:
      return 0
    else:
       return - r/np.tan(alph)

  def length(self):
    return self.inner_ray().length

  def set_length(self, x):
    for ray in self._rays:
      ray.length = x


  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird
    ändert die Position aller __rays mit

    is called when the position of <self> is changed
    changes the position of all __rays with
    """
    super()._pos_changed(old_pos, new_pos)
    self._rearange_subobjects_pos(old_pos, new_pos, self._rays)


  def _axes_changed(self, old_axes, new_axes):
    """
    wird aufgerufen, wen das KooSys <_axes> von <self> verändert wird
    dreht die KooSys aller __rays mit

    dreht außerdem das eigene Koordiantensystem

    is called when the KooSys <_axes> is changed from <self>.
    rotates the KooSys of all __rays as well

    also rotates the own coordiante system
    """
    super()._axes_changed(old_axes, new_axes)
    self._rearange_subobjects_axes(old_axes, new_axes, self._rays)


  # def draw_freecad(self):
  #   if self.draw_dict["model"] == "Gaussian":
  #     return model_Gaussian_beam(name=self.name, q_para=self.q_para,
  #                                wavelength=self.wavelength,
  #                                prop=self.get_all_rays()[0].length,
  #                                geom_info=self.get_geom())
  #   elif self.draw_dict["model"] == "cone":
  #     radius, angle = self.radius_angle()
  #     # return model_beam(name=self.name, dia=2*radius, prop=self.length(),
  #          # f=self.focal_length(), geom_info=self.get_geom(), **self.draw_dict)
  #     return model_beam(dia=2*radius, prop=self.length(), f=self.focal_length(),
  #                       geom_info=self.get_geom(), **self.draw_dict)
  #     # return model_beam_new(radius=radius, length=self.length(),  angle=angle,
  #                           # geom_info=self.get_geom(),**self.draw_dict)
  #     # return model_Gaussian_beam(name=self.name, dia=2*radius, prop=self.length(),
  #     #      f=self.focal_length(), geom_info=self.get_geom())
  #   else:
  #     part = initialize_composition_old(name="ray group")
  #     container = []
  #     for nn in range(self._ray_count):
  #       our=self._rays[nn]
  #       obj = our.draw_freecad()
  #       container.append(obj)
  #     add_to_composition(part, container)
  #     return part

class Rainbow(Beam):
  def __init__(self, separation=0, angle=0,ray_count=15, name="NewBeam",wavelength_range=(1000E-6,1060E-6), **kwargs):
    super().__init__(name = name, **kwargs)
    self.draw_dict['model'] = "ray_group"
    self._ray_count = ray_count
    self._wavelength_group = np.linspace(wavelength_range[0], wavelength_range[1],ray_count)
    shifting_group = np.linspace(-separation/2, separation/2,ray_count)
    self._rays = []
    cmap = plt.cm.gist_rainbow
    for i in range(ray_count):
      ray = Ray()
      ray.wavelength = self._wavelength_group[i]
      x = 1-(self._wavelength_group[i] -min(wavelength_range[0],wavelength_range[1])) / abs(wavelength_range[1]-wavelength_range[0])
      ray.draw_dict["color"] = cmap( x )
      ray.set_geom(self.get_geom())
      ray.pos += (0,shifting_group[i],0)
      self._rays.append(ray)
    
    

class Gaussian_Beam(Ray):
# class Gaussian_beam(Geom_Object):
  def __init__(self, radius=10, angle=0.02, wavelength=1030E-6, name="NewGassian",  **kwargs):
    super().__init__(name=name, **kwargs)
    z0 = wavelength/(np.pi*np.tan(abs(angle))*np.tan(abs(angle)))
    w0 = wavelength/(np.pi*np.tan(abs(angle)))
    if w0>radius:
      print("Woring: Wrong Radius!")
    z = z0*pow((radius*radius)/(w0*w0)-1,0.5)
    if angle<0:
      z = -z
    q_para = complex(z,z0)
    self.wavelength = wavelength
    self.q_para = q_para
    self._distribution = "Gaussian"
    self.draw_dict["model"] = "Gaussian"

  def set_length(self, length):
    # needed for consitency in next_beam function
    self.length = length
		
  def waist(self):
    return np.sqrt( self.wavelength / np.pi * np.imag(self.q_para) )

  def __repr__(self):
    # radius, angle = self.radius_angle()
    n = len(self.class_name())
    txt = 'Gaussian_Beam(q_para=' + repr(self.q_para)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def draw_freecad(self):
    if self.draw_dict["model"] == "Gaussian":
      return model_Gaussian_beam(name=self.name, q_para=self.q_para,
                               wavelength=self.wavelength,prop=self.length,
                               geom=self.get_geom())
      # return model_Gaussian_beam(name=self.name, q_para=self.q_para,
      #                             wavelength=self.wavelength,prop=self.length,
      #                             geom_info=self.get_geom())
      
    if self.draw_dict["model"] == "cone":
      self.update_draw_dict()
      self.draw_dict["q_para"] = self.q_para
      return model_Gaussian_beam_cone(**self.draw_dict)
      # return model_Gaussian_beam_cone(name=self.name, q_para=self.q_para,
      #                            wavelength=self.wavelength,prop=self.length,
      #                            geom_info=self.get_geom())
      # quicker method with nearly the same look in most cases
      # radius = self.radius()
      # focal_length = - radius / self.divergence()
      # col = (244/255, 22/255, 112/255)
      # return model_beam(dia=2*radius, prop=self.length, f=focal_length,
      #                   geom_info=self.get_geom(), color=col, **self.draw_dict)
    else:
      return -1
    
  def update_draw_dict(self):
    self.draw_dict["name"] = self.name
    self.draw_dict["wavelength"] = self.wavelength
    self.draw_dict["prop"] = self.length
    self.draw_dict["geom"] = self.get_geom()
     
  def radius(self):
    z = np.real(self.q_para)
    zr = np.imag(self.q_para)
    return self.waist() * np.sqrt(1 + (z/zr)**2)
  
  def divergence(self):
    z = np.real(self.q_para)
    zr = np.imag(self.q_para)
    return np.sign(z) * self.waist() / zr
    
  def transform_to_cone_beam(self):
    cone = Beam(name=self.name, radius=self.radius(), angle=self.divergence())
    cone.set_geom(self.get_geom())
    cone.set_length(self.length)
    return cone

  # def get_all_rays(self, by_reference=True):
  def get_all_rays(self):
    ray = Ray()
    ray.set_geom(self.get_geom())
    ray.wavelength = self.wavelength
    ray.length = self.length
    return [ray]
  
  def draw_gaussian_profile(self,center_intensity= 2,norm=True):
    sig = self.radius()
    fs = 24
    def Gaussian(x, mu, sig):
      return (1.0 / (np.sqrt(2.0 * np.pi) * sig) * np.exp(-np.power((x - mu) / sig, 2.0) / 2))

    ran= int(sig*3)
    x_values = np.linspace(-ran, ran,120)
    cen_amp = Gaussian(0,0,sig)
    norm_amp = 1/cen_amp
    intensity_amp = center_intensity/cen_amp
    a1=plt.figure()
    if norm :
      plt.plot(x_values, norm_amp*Gaussian(x_values,0,sig))
    plt.plot(x_values, intensity_amp*Gaussian(x_values,0,sig))
    plt.xticks(fontsize=fs)
    plt.yticks(fontsize=fs)
    return a1

  def inner_ray(self):
    return self.get_all_rays()[0]
  
if __name__ == "__main__":
  b = Beam(name = "Strahlo", radius=2)
  print(b)
  print(b.inner_ray())
  print(b.outer_rays())

  print()

  b = Beam(pos=(1,2,3))
  print(b.outer_rays())
  print("Radius, Winkel von b:", b.radius_angle())

