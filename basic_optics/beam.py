# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:34:44 2022

@author: mens
"""

from basic_optics import Ray, Geom_Object, TOLERANCE
from basic_optics.freecad_models import model_beam,model_ray_1D
from basic_optics.freecad_models.freecad_model_composition import initialize_composition_old, add_to_composition
# from .optical_element import Opt_Element

from copy import deepcopy
import numpy as np


class RayGroup(Geom_Object):
  """
  Base class for a group of rays (you don't say!)
  special funcitoins: make_square_distribution(radius=1, ray_count=5)
  make_circular_distribution(radius=1, ray_count=5)
  average_divegence = ?

  """
  def __init__(self, radius=1, angle=0, ray_count=121, name="NewRayGroup", **kwargs):
    super().__init__(name=name, **kwargs)
    self._ray_count = ray_count
    self._rays = [Ray() for n in range(self._ray_count)]
    self._angle = angle
    self._radius = radius
    self.draw_dict["model"] = "ray_group"

  def make_square_distribution(self,ray_in_line):
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
    # mr = self._rays[0]
    # mr.set_geom(self.get_geom())
    # mr.name = self.name + "_inner_Ray"
    # thetas = np.linspace(0+np.pi/4, 2*np.pi+np.pi/4, self._ray_count)
    # for n in range(self._ray_count-1):
    #   our = self._rays[n+1]
    #   height=self._radius/max(abs(np.cos(thetas[n])),abs(np.cos(np.pi/2-thetas[n])))
    #   our.from_h_alpha_theta(height, self._angle, thetas[n], self)
    #   our.name = self.name + "_outer_Ray" + str(n)
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

  def make_circular_distribution(self,ring_number):
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
    if self.is_valid():
      # self.set_geom(rays[0].get_geom())
      # self._normal = rays[0].normal
      self._axes = rays[0].get_axes()
      self._pos = rays[0].pos
      # print(self._pos)

  def draw_text(self):
    radius,angle  = self.radius_angle()
    txt = 'Ray Group(radius=' + repr(radius)
    txt += ', ' + super().__repr__()[5::]
    return txt

  def draw_fc(self):
    part = initialize_composition_old(name="ray group")
    container = []
    for nn in range(self._ray_count):
      our=self._rays[nn]
      obj=model_ray_1D(**our.draw_dict)
      container.append(obj)
    add_to_composition(part, container)
    return part

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

  def is_valid(self):
    """
    prüft ob alle rays valide sind
    """
    valid = True
    for ray in self._rays:
      if not type(ray) == type(Ray()):
        valid = False
    return valid

  def set_length(self, x):
    for ray in self._rays:
      ray.length = x

  # def focal_length(self):
  #   r, alph = self.radius_angle()
  #   if alph == 0:
  #     return 0
  #   else:
  #     return - r/alph

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



# class Beam(Geom_Object):
class Beam(RayGroup):
  """
  Klasse für "ausgedehnte" Strahlen
  besteht aus mindestens 2 rays:
  middle_ray, stellt die optische Achse = Symmetrieachse des Strhals dar
  outer_rays[], beinhaltet im Fall eines zlindersymmetrischen Strahls nur einen
  Ray, der in der Mantelfläche liegt, kann aber bis zu 4 Strahlen beeinhalten
  (Astigmatismus)

  besitzt zusätzlich noch wavelength, power

  ermöglicht zudem die Erzeugung von Standard-Beams (r, alpha)
  Astigmatischen Beams ?
  Gauß-Beams?

  Class for "extended" rays
  consists of at least 2 rays:
  middle_ray, represents the optical axis = symmetry axis of the ray
  outer_rays[], contains in case of a zlindersymmetric ray only one
  ray, which is located in the lateral surface, but can contain up to 4 rays
  (astigmatism)

  has additionally wavelength, power

  also allows the generation of standard beams (r, alpha)
  astigmatic beams ?
  Gaussian beams ?
  """
  def __init__(self, radius=1, angle=-0.05, ray_count=2, name="NewBeam", **kwargs):
    super().__init__(name=name, ray_count=ray_count, **kwargs)
    # super().__init__(name=name, **kwargs)
    # self._ray_count = ray_count
    # self._rays = [Ray() for n in range(self._ray_count)]
    # self.wavelength = 1030e-6 #Wellenlänge in mm
    # self.power = 1 # Power in W
    # self._radius = radius
    # self._angle = angle
    self.update_rays()
    self.draw_dict["model"] = "beam_cone"

  def update_rays(self):
    mr = self._rays[0]
    mr.set_geom(self.get_geom())
    mr.name = self.name + "_inner_Ray"
#     our = self._rays[1]
    thetas = np.linspace(0, 2*np.pi, self._ray_count)
    for n in range(self._ray_count-1):
      our = self._rays[n+1]
      our.from_h_alpha_theta(self._radius, self._angle, thetas[n], self)
      our.name = self.name + "_outer_Ray" + str(n)

  def inner_ray(self):
    return deepcopy(self._rays[0])

  def outer_rays(self):
    return deepcopy(self._rays[1::])

#   def __repr__(self):

  # def override_rays(self, rays):
  #   """
  #   setzt die rays neu, muss man eventuell aufpassen, mal sehen

  #   resets the rays, you may have to watch out, let's see

  #   Parameters
  #   ----------
  #   rays : list of rays
  #   """
  #   rc = len(rays)
  #   self._ray_count = rc
  #   self._rays = rays
  #   if self.is_valid():
  #     # self.set_geom(rays[0].get_geom())
  #     # self._normal = rays[0].normal
  #     self._axes = rays[0].get_axes()
  #     self._pos = rays[0].pos
  #     # print(self._pos)

  def __repr__(self):
    radius, angle = self.radius_angle()
    txt = 'Beam(radius=' + repr(radius)
    txt += ', anlge=' + repr(angle)
    txt += ', ' + super().__repr__()[5::]
    return txt

  # def radius_angle_old(self):
  #   our = self._rays[1]
  #   return our.h_alpha_to(self._rays[0])

  def radius_angle(self):
    """
    berechnet aus 2 Strahlen inn und outer den zugehörigen beam Kegel mit
    radius r und öffnungswinkel alpha und zwar von hinten durch die Brust
    ins Auge

    calculates from 2 rays inn and outer the corresponding beam cone with
    radius r and aperture angle alpha and from behind through the breast into
    the eye
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

  # def get_all_rays(self, by_reference=False):
  #  if by_reference:
  #    return self._rays
  #  else:
  #    return deepcopy(self._rays)

  # def is_valid(self):
  #   """
  #   prüft ob alle rays valide sind

  #   checks if all rays are valid
  #   """
  #   valid = True
  #   for ray in self._rays:
  #     if not type(ray) == type(Ray()):
  #       valid = False
  #   return valid

  # def set_length(self, x):
  #   for ray in self._rays:
  #     ray.length = x

  def focal_length(self):
    r, alph = self.radius_angle()
    if alph == 0:
      return 0
    else:
      return - r/alph

  def length(self):
    return self.inner_ray().length

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

    also rotates its own coordiante system
    """
    super()._axes_changed(old_axes, new_axes)
    self._rearange_subobjects_axes(old_axes, new_axes, self._rays)


  def draw_fc(self):
    if self.draw_dict["model"] == "beam_cone":
      radius, _ = self.radius_angle()
      return model_beam(name=self.name, dia=2*radius, prop=self.length(),
           f=self.focal_length(), geom_info=self.get_geom())
    else:
      super().draw()

if __name__ == "__main__":
  b = Beam(name = "Strahlo", radius=2)
  print(b)
  print(b.inner_ray())
  print(b.outer_rays())

  print()

  b = Beam(ray_count=5, pos=(1,2,3))
  print(b.outer_rays())
  print("Radius, Winkel von b:", b.radius_angle())

  print("Beam valide:", b.is_valid())
  c = deepcopy(b)
  murx = ["banane", 12, 3.1]
  c.override_rays(murx)
  print("Beam immer noch valide:", c.is_valid())
