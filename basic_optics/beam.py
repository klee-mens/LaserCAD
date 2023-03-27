# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:34:44 2022

@author: mens
"""

from basic_optics import Ray, Geom_Object, TOLERANCE
from basic_optics.freecad_models import model_beam

from copy import deepcopy
import numpy as np

class Beam(Geom_Object):
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
  """
  def __init__(self, radius=1, angle=-0.05, ray_count=2, name="NewBeam", **kwargs):
    super().__init__(name=name, **kwargs)
    self.__ray_count = ray_count
    self._rays = [Ray() for n in range(self.__ray_count)]
    self.wavelength = 1030e-6 #Wellenlänge in mm
    self.power = 1 # Power in W
    self.__radius = radius
    self.__angle = angle
    self.update_rays()

  def update_rays(self):
    mr = self._rays[0]
    mr.set_geom(self.get_geom())
    mr.name = self.name + "_inner_Ray"
#     our = self._rays[1]
    thetas = np.linspace(0, 2*np.pi, self.__ray_count)
    for n in range(self.__ray_count-1):
      our = self._rays[n+1]
      our.from_h_alpha_theta(self.__radius, self.__angle, thetas[n], self)
      our.name = self.name + "_outer_Ray" + str(n)

  def inner_ray(self):
    return deepcopy(self._rays[0])

  def outer_rays(self):
    return deepcopy(self._rays[1::])

#   def __repr__(self):

  def override_rays(self, rays):
    """
    setzt die rays neu, muss man eventuell aufpassen, mal sehen

    Parameters
    ----------
    rays : list of rays
    """
    rc = len(rays)
    self.__ray_count = rc
    self._rays = rays
    if self.is_valid():
      # self.set_geom(rays[0].get_geom())
      # self._normal = rays[0].normal
      self._axes = rays[0].get_axes()
      self._pos = rays[0].pos
      # print(self._pos)

  def __repr__(self):
    radius, angle = self.radius_angle()
    txt = 'Beam(radius=' + repr(radius)
    txt += ', anlge=' + repr(angle)
    txt += ', ' + super().__repr__()[7::]
    return txt

  # def radius_angle_old(self):
  #   our = self._rays[1]
  #   return our.h_alpha_to(self._rays[0])

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

  def get_all_rays(self):
    return self._rays

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

  def focal_length(self):
    r, alph = self.radius_angle()
    if alph == 0:
      return 0
    else:
      return - r/alph

  def length(self):
    return self.inner_ray().length

  def draw_fc(self):
    radius, _ = self.radius_angle()
    return model_beam(name=self.name, dia=2*radius, prop=self.length(),
         f=self.focal_length(), geom_info=self.get_geom())

  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird
    ändert die Position aller __rays mit
    """
    # print("Beam oldpos, newpos:", old_pos, new_pos)
    super()._pos_changed(old_pos, new_pos)
    self._rearange_subobjects_pos(old_pos, new_pos, self._rays)

  # def _normal_changed(self, old_normal, newnormal):
  #   """
  #   wird aufgerufen, wen die Normale von <self> verändert wird
  #   dreht die Normale aller __rays mit

  #   dreht außerdem das eigene Koordiantensystem
  #   """
  #   super()._normal_changed(old_normal, newnormal)
  #   self._rearange_subobjects_normal(old_normal, newnormal, self._rays)

  def _axes_changed(self, old_axes, new_axes):
    """
    wird aufgerufen, wen das KooSys <_axes> von <self> verändert wird
    dreht die KooSys aller __rays mit

    dreht außerdem das eigene Koordiantensystem
    """
    super()._axes_changed(old_axes, new_axes)
    self._rearange_subobjects_axes(old_axes, new_axes, self._rays)

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
