# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:34:44 2022

@author: mens
"""

from basic_optics import Ray, Geom_Object, TOLERANCE
from basic_optics.freecad_models import model_beam,model_ray_1D,model_Gaussian_beam
from basic_optics.freecad_models.freecad_model_composition import initialize_composition_old, add_to_composition
# from .optical_element import Opt_Element

from copy import deepcopy
import numpy as np



class Beam(Geom_Object):
  """
  Base class for a group of rays (you don't say!)
  special funcitoins: make_square_distribution(radius=1, ray_count=5)
  make_circular_distribution(radius=1, ray_count=5)
  average_divegence = ?

  """
  def __init__(self, radius=1, angle=0, name="NewBeam",wavelength=1030E-6, distribution="cone", **kwargs):
    super().__init__(name=name, **kwargs)
    self._ray_count = 2
    self._rays = [Ray() for n in range(self._ray_count)]
    self._angle = angle
    self._radius = radius
    self._distribution = distribution
    self._wavelength = wavelength
    if distribution == "cone":
      self.make_cone_distribution()
      self.draw_dict["model"] = "cone"      
    elif distribution == "square":
      self.make_square_distribution()
      self.draw_dict["model"] = "ray_group"      
    elif distribution == "circular":
      self.make_circular_distribution()
      self.draw_dict["model"] = "ray_group" 
    elif distribution == "Gaussian":
      z0 = wavelength/(np.pi*np.tan(angle)*np.tan(angle))
      w0 = wavelength/(np.pi*np.tan(angle))
      if w0>radius:
        print("Woring: Wrong Radius!")
      z = z0*pow((radius*radius)/(w0*w0)-1,0.5)
      if angle<0:
        z = -z
      q_para = complex(z,z0)
      self.wavelength = wavelength
      self.q_para = q_para
      self.make_Gaussian_distribution()
      self.draw_dict["model"] = "Gaussian"
    else:
      # Abortion
      print("Distribution tpye not know. Beam not valid.")
      print("Allowed distribution types are: 'cone', 'square', 'circular'")
      self = -1
      return None
    
  def make_cone_distribution(self, ray_count=2):
    self._ray_count = ray_count
    self._distribution = "cone"
    self.draw_dict["model"] = "cone"
    mr = self._rays[0]
    mr.set_geom(self.get_geom())
    mr.name = self.name + "_inner_Ray"
    thetas = np.linspace(0, 2*np.pi, self._ray_count)
    for n in range(self._ray_count-1):
      our = self._rays[n+1]
      our.from_h_alpha_theta(self._radius, self._angle, thetas[n], self)
      our.name = self.name + "_outer_Ray" + str(n)
  
  def make_Gaussian_distribution(self, ray_count=2):
    self._ray_count = 1
    radius = self._radius
    wavelength = self._wavelength
    angle = self._angle
    self._distribution = "Gaussian"
    self.draw_dict["model"] = "Gaussian"
    
    z0 = wavelength/(np.pi*np.tan(angle)*np.tan(angle))
    w0 = wavelength/(np.pi*np.tan(angle))
    if w0>radius:
      print("Woring: Wrong Radius!")
    z = z0*pow((radius*radius)/(w0*w0)-1,0.5)
    if angle<0:
      z = -z
    q_para = complex(z,z0)
    self.q_para = q_para
    mr = self._rays[0]
    mr.set_geom(self.get_geom())
    mr.name = self.name + "_inner_Ray"

  
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
        ray_counting+=1
    # print(ray_counting) # ray_counting is the number of the rays.
    self._ray_count = ray_counting
    self._distribution = "square"
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
      if r!=0:                                                                #if the ray is not in the center
        thetas = np.linspace(0, 2*np.pi, int(r*ring_number/radius)*6+1)        #thetas repersents the rotation angle of the ray
        for n in range(int(r*ring_number/radius)*6):
          our=self._rays[ray_counting]
          our.from_h_alpha_theta(r, self._angle, thetas[n], self)            # rotate the ray which is not in the center
          our.name=self.name + "_outer_Ray" +str(ray_counting)
          ray_counting+=1
      else:
        mr=self._rays[ray_counting]
        mr.set_geom(self.get_geom())
        mr.name = self.name + "_inner_Ray"
        ray_counting+=1
    # print(ray_counting) # ray_counting is the number of the rays.
    self._ray_count = ray_counting
    self._distribution = "circular"
    self.draw_dict["model"] = "ray_group"

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


  def draw_fc(self):
    if self.draw_dict["model"] == "Gaussian":
      return model_Gaussian_beam(name=self.name, q_para=self.q_para,
                                 wavelength=self.wavelength,
                                 prop=self.get_all_rays()[0].length,
                                 geom_info=self.get_geom())
    elif self.draw_dict["model"] == "cone":
      radius, _ = self.radius_angle()
      return model_beam(name=self.name, dia=2*radius, prop=self.length(),
           f=self.focal_length(), geom_info=self.get_geom())
      # return model_Gaussian_beam(name=self.name, dia=2*radius, prop=self.length(),
      #      f=self.focal_length(), geom_info=self.get_geom())
    else:
      part = initialize_composition_old(name="ray group")
      container = []
      for nn in range(self._ray_count):
        our=self._rays[nn]
        obj = our.draw_fc()
        container.append(obj)
      add_to_composition(part, container)
      return part    





class Gaussian_Beam(Ray):
# class Gaussian_beam(Geom_Object):
  def __init__(self, radius=10, angle=0.05, wavelength=1030E-6, name="NewGassian",  **kwargs):
    super().__init__(name=name, **kwargs)
    z0 = wavelength/(np.pi*np.tan(angle)*np.tan(angle))
    w0 = wavelength/(np.pi*np.tan(angle))
    if w0>radius:
      print("Woring: Wrong Radius!")
    z = z0*pow((radius*radius)/(w0*w0)-1,0.5)
    if angle<0:
      z = -z
    q_para = complex(z,z0)
    self.wavelength = wavelength
    self.q_para = q_para
    
  def __repr__(self):
    # radius, angle = self.radius_angle()
    n = len(self.class_name())
    txt = 'Gaussian_Beam(q_para=' + repr(self.q_para)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def draw_fc(self):
    return model_Gaussian_beam(name=self.name, q_para=self.q_para,
                               wavelength=self.wavelength,prop=self.length,
                               geom_info=self.get_geom())




if __name__ == "__main__":
  b = Beam(name = "Strahlo", radius=2)
  print(b)
  print(b.inner_ray())
  print(b.outer_rays())

  print()

  b = Beam(pos=(1,2,3))
  print(b.outer_rays())
  print("Radius, Winkel von b:", b.radius_angle())

  # print("Beam valide:", b.is_valid())
  # c = deepcopy(b)
  # murx = ["banane", 12, 3.1]
  # c.override_rays(murx)
  # print("Beam immer noch valide:", c.is_valid())
