#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 14:48:12 2022

@author: mens
"""

# from basic_optics import Geom_Object, Ray, TOLERANCE, Beam
from .geom_object import Geom_Object, TOLERANCE
from .ray import Ray
from .beam import Beam, Gaussian_Beam
from .constants import inch
import numpy as np
from copy import deepcopy
from .. freecad_models import freecad_da



class Opt_Element(Geom_Object):
  """
  Basisklasse aller "dünnen" optischen Elemente wie z.B. Linse
  "dünn" heißt, nur der Winkel (normal) vom Strahl wird geändert, nicht seine
  Höhe (pos)
  die Oberfläche wird als ebene im R3 angenommen
  erbt von Geom_Obj
  führt neben pos, normal auch Matrix für geometrische Optik ein
  neue Methoden:
    next_ray(ray)
    reflection(ray)
    refraction(ray)
    diffraction(ray) ?

  """
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._matrix = np.eye(2)
    self.aperture = 1*inch # Apertur in mm, wichtig für Klippingabfrage
    self.length = 0 #Länge in mm, die meisten opt Elemente sind 2D, also 0
    self.group = [] # falls das Element in eine Baugruppe eingesetzt wird
    #Parameter zum zeichnen
    self.draw_dict.update({"dia":self.aperture, "thickness":5,
                           "model_type":"DEFAULT", "mount_type": "default",
                           "mount_name": self.name+"_mount"})
    # self.interacts_with_rays = True

  def matrix(self):
    return np.array(self._matrix)

  def next_ray(self, ray):
    """
    erzeugt den durch das opt Elem veränderten Strahl und gibt ihn zurück
    Parameters
    ----------
    ray : Ray
      Eingangsstrahl
    Returns
    -------
    ray2 : Ray
      Ausgangsstrahl
    """
    return self.just_pass_through(ray)

  def just_pass_through(self, ray):
    ray2 = deepcopy(ray)
    ray2.pos = ray.intersect_with(self) #dadruch wird ray.length verändert(!)
    return ray2

  def next_beam(self, beam):
    """
    erzeugt den durch das opt Elem veränderten Beam und gibt ihn zurück
    und zwar ultra lazy
    Parameters
    ----------
    beam : Beam()

    Returns
    -------
    next Beam()
    """
    if type(beam) == type(Gaussian_Beam()):
      return self.next_gauss(beam)
    newb = deepcopy(beam)
    newb.name = "next_" + beam.name
    rays = beam.get_all_rays(by_reference=True)
    # if beam._distribution == "Gaussian":

    newrays = []
    for ray in rays:
      nr = self.next_ray(ray)
      if not nr:
        return False #Für Elemente die nicht mit Strahlen interagieren wird -1 als beam zurück gegeben
      newrays.append(nr)
    newb.override_rays(newrays)
    # if beam._distribution == "Gaussian":
    #   [[A,B],[C,D]] = self._matrix
    #   q_parameter = deepcopy(beam.q_para)
    #   q_parameter += beam.get_all_rays()[0].length
    #   newb.q_para = (A*q_parameter+B)/(C*q_parameter+D)
    return newb

  def next_gauss(self,gaussian):
      next_gaussian = deepcopy(gaussian)
      next_middle = self.next_ray(gaussian) #change the length of Gaussian
      next_gaussian.set_geom(next_middle.get_geom())
      [[A,B],[C,D]] = self._matrix
      q_parameter = deepcopy(gaussian.q_para)
      q_parameter += gaussian.length
      next_gaussian.q_para = (A*q_parameter+B)/(C*q_parameter+D)
      # print(next_gaussian.q_para)
      return next_gaussian

  def reflection(self, ray):
    """
    erzeugt den nächsten Strahl aus <Ray> mit Hilfe des Reflexionsgesetzes
    (man beachte die umgedrehte <normal> im Gegensatz zur Konvention in z.B.
    Springer Handbook of Optics and Lasers S. 68)

    Parameters
    ----------
    ray : Ray()
      incident ray

    Returns
    -------
    reflected ray
    """
    ray2 = deepcopy(ray)
    ray2.pos = ray.intersect_with(self) #dadruch wird ray.length verändert(!)
    k = ray2.normal
    km = -self.normal
    scpr = np.sum(km*k)
    newk = k-2*scpr*km
    ray2.normal = newk
    # print("REFL", k, km, scpr, newk, ray2.normal)
    return ray2



  def refraction(self, ray):
    ray2 = deepcopy(ray)
    ray2.pos = ray.intersect_with(self) #dadruch wird ray.length verändert(!)
    norm = ray2.normal
    radial_vec = ray2.pos - self.pos
    radius = np.linalg.norm(radial_vec) #Radius im sinne der parax Optik
    ea = self.normal #Einheitsvec in Richtung der optischen Achse oA
    if np.sum(ea * norm) < 0:
      ea *= -1 #gibt sonst hässliche Ergebnisse, wenn die Linse falsch rum steht
    if radius > TOLERANCE:
      # kein Mittelpunktsstrahl
      er = radial_vec / radius #radialer Einheitsvektor (meridional)
      es = np.cross(er, ea) #Einheitsvektor in sagitaler Richtung
      es = es / np.linalg.norm(es) #eigentlich automatisch, aber man weiß ja nie
      cr = np.sum(er * norm)
      ca = np.sum(ea * norm)
      cs = np.sum(es * norm)
      alpha = np.arctan(cr/ca)
      vm = np.sqrt(cr**2 + ca**2) #length of the raz.normal projected in the meridional plane
      parax1 = np.array((radius, alpha)) #classic matrix optics
      rad2, alpha2 = np.matmul(self._matrix, parax1) #classic matrix optics
      pos2 = self.pos + er * rad2 #neue position
      norm2 = vm*np.cos(alpha2)*ea + vm*np.sin(alpha2)*er + cs*es # neue normale
      ray2.pos = pos2
      ray2.normal = norm2
      return ray2

    #else: Mittelpunktsstrahl
    ca = np.sum(ea * norm)
    em = norm - ca * ea #meridionaler Einheitsvektor
    m = np.linalg.norm(em)
    if m < TOLERANCE:
      # s = (0,0) -> (0,0) Mittelpunkstrahl ohne Winkel
      return ray2
    em *= 1/m
    alpha = np.arctan(m/ca)
    rad2 = self._matrix[0,1] * alpha #r2 = B*alpha
    alpha2 = self._matrix[1,1] * alpha #alpha2 = D*alpha
    pos2 = self.pos + rad2 * em
    norm2 = np.cos(alpha2)*ea + np.sin(alpha2)*em
    ray2.pos = pos2
    ray2.normal = norm2

    return ray2


  def draw_mount(self):
    if freecad_da:
      return self.draw_mount_fc()
    else:
      txt = self.draw_mount_text()
      print(txt)
      return txt

  def draw_mount_fc(self):
    #ToDo: fürs Debugging hier einfach einen Zylinder mit norm uns k zeichnen
    return None

  def draw_mount_text(self):
    txt = "Kein Mount für <" +self.name + "> gefunden."
    return txt


def refraction_tests():
  oe = Opt_Element(pos = (100, 0, 0))
  oe._matrix[1,0] = -1/50 #etwas hacky
  r = Ray(pos=(0,0,10))
  r2 = oe.refraction(r)
  print(r2)

  r0 = Ray(pos=(0,0,5))
  r1 = Ray(pos=(0,0,10))
  r2 = Ray(pos=(0,0,15))
  r0.rotate((0,1,0), np.pi/12)
  r1.rotate((0,1,0), np.pi/12)
  r2.rotate((0,1,0), np.pi/12)
  r10 = oe.refraction(r0)
  r11 = oe.refraction(r1)
  r12 = oe.refraction(r2)
  print(r10)
  print(r11)
  print(r12)
  foc_eb = Opt_Element(pos = (150, 0, 0))
  print(r10.intersection(foc_eb))
  print(r11.intersection(foc_eb))
  print(r12.intersection(foc_eb))


def tests():
  # Test mit Sammellinse f = 50
  oe = Opt_Element()
  oe.pos = (100, 0, 80)
  oe._matrix[1,0] = -1/50 #etwas hacky
  r = Ray()
  r.pos = (0,0,80+50)
  r2 = oe.refraction(r)
  print(r2)
  print("sollte bei 100, 0, 130 liegen und 45° nach unten gehen")

  print() # Test mit Reflektion

  oe.normal = (1,-1,0)
  r4 = oe.reflection(r)
  print(r4)
  print("sollte bei 100, 0, 130 liegen und in y-Richtung gehen")
#   r3 = oe.reflection(r)

  print() # Tests mit new Ray, new, Beam
  b = Beam(radius = 3, angle = -0.07)
  print(b, " --- ", b.radius_angle())
  c = oe.next_beam(b)
  print(c, " --- ", c.radius_angle())

  #refraction_tests():

if __name__ == "__main__":
  tests()

  print()
  print()

  refraction_tests()