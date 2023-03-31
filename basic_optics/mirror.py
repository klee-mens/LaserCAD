# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:28:07 2022

@author: mens
"""

# from basic_optics import Opt_Element, TOLERANCE, Ray
# from basic_optics.freecad_models import model_mirror, freecad_da
from .geom_object import TOLERANCE, NORM0
from .ray import Ray
from .freecad_models import model_mirror, mirror_mount, model_stripe_mirror
from .optical_element import Opt_Element
import numpy as np
from copy import deepcopy



class Mirror(Opt_Element):
  """
  Spiegelklasse, nimmt einen ray und transformiert ihn
  dreht ihn in der xy Ebene um den Winkel phi und theta aus der Ebene heraus, wenn man
  die normale voher mit set_geom() einstellt
  Bsp: m = Mirror(), ...siehe unten

  """
  def __init__(self, phi=180, theta=0, **kwargs):
    super().__init__(**kwargs)
    self.__incident_normal = np.array(NORM0) # default von Strahl von x
    self.__theta = theta
    self.__phi = phi
    # print("n0", self.normal)
    self.update_normal()
    #Cosmetics
    # self.draw_dict["mount_type"] = "POLARIS-K1-Step"
    self.draw_dict["Radius"] = 0
    

  def update_normal(self):
    """
    setzt die Normale des Mirrors entsprechend der incident, phi und theta
    """
    phi = self.__phi/180*np.pi
    theta = self.__theta/180*np.pi
    if phi == 0 and theta == 0:
      print("Warnung, Spiegel unbestimmt und sinnlos, beide Winkel 0")
      self.normal = (0,1,0)
      return -1

    rho = self.__incident_normal[0:2]
    rho_abs = np.linalg.norm(rho)
#     print(rho_abs)
    z = self.__incident_normal[2]

    rho2_abs = rho_abs * np.cos(theta) - z * np.sin(theta)
    z2 = rho_abs * np.sin(theta) + z * np.cos(theta)

    if rho_abs == 0:
      x = rho2_abs
      y = 0
    else:
      x = rho[0] * rho2_abs/rho_abs
      y = rho[1] * rho2_abs/rho_abs

    x2 = x * np.cos(phi) - y * np.sin(phi)
    y2 = x * np.sin(phi) + y * np.cos(phi)
    # print("x,y,z",  (x2, y2, z2))
    # print("n1:", self.normal)
    self.normal = (x2, y2, z2) # eigentlich nur zur sicherheit normieren,
    # print("n2:", self.normal)
    #aber quasi unnötig, könnte auch zwischengespeichert werden, evt später
    self.normal = self.__incident_normal - self.normal
    # print("n3:", self.normal)

  def set_geom(self, geom):
    self.pos = geom[0]
    self.__incident_normal = geom[1]
    self.update_normal()

  @property
  def phi(self):
    return self.__phi
  @phi.setter
  def phi(self, x):
    self.__phi = x
    self.update_normal()

  @property
  def theta(self):
    return self.__theta
  @theta.setter
  def theta(self, x):
    self.__theta = x
    self.update_normal()

  def next_ray(self, ray):
    return self.reflection(ray)

  def next_geom(self, geom):
    pos, k = geom[0], geom[1]
    km = -self.normal
    scpr = np.sum(km*k)
    newk = k-2*scpr*km
    return (pos, newk)

  def set_incident_normal(self, vec):
    # setzt neuen incident Vector und berechnet daraus mit phi, theta die neue Normale
    vec = vec / np.linalg.norm(vec)
    self.__incident_normal = np.array((1.0,1.0,1.0)) * vec
    self.update_normal()

  def recompute_angles(self):
    """
    berechnet die Winkel neu aus incident und normal
    """
    vec1 = self.__incident_normal
    dummy = Opt_Element(normal=vec1)
    #nur um die bekannten Funktionen zu nutzen
    geom = self.next_geom(dummy.get_geom())
    vec2 = geom[1]
    xy1 = vec1[0:2]
    xy2 = vec2[0:2]
    teiler = np.linalg.norm(xy1) * np.linalg.norm(xy2)
    if teiler < TOLERANCE:
      #wenn die Komponenten verschwinden, kann kein Winkel bestimmt werden
      phi = 0
    else:
      phi = np.arcsin( (xy1[0]*xy2[1]-xy1[1]*xy2[0]) /teiler) * 180/np.pi
    v3 = np.array((np.linalg.norm(xy1), vec1[2]))
    v4 = np.array((np.linalg.norm(xy2), vec2[2]))
    teiler = np.linalg.norm(v3) * np.linalg.norm(v4)
    if teiler < TOLERANCE:
      #wenn die Komponenten verschwinden, kann kein Winkel bestimmt werden
      theta = 0
    else:
      theta = np.arcsin( (v3[0]*v4[1]-v3[1]*v4[0]) /teiler) * 180/np.pi
    return phi, theta

  def set_normal_with_2_points(self, p0, p1):
    """
    setzt die Normale neu, sodass der mirror einen Strahl reflektiert, der von
    p0 kommt, den Spiegel in self.pos trifft und dann zu p1 reflektiert wird
    berechnet anschließend die Winkel neu
    """
    inc = self.pos - p0
    refl = p1 - self.pos
    inc *= 1/np.linalg.norm(inc)
    refl *= 1/np.linalg.norm(refl)
    # print("nextnormal", (inc - refl)/np.linalg.norm(inc - refl))
    self.normal = inc - refl
    self.__phi, self.__theta =  self.recompute_angles()

  # def set_normal_with_2_obj(self, obj0, obj1):
  #   """
  #   wrapper func um <set_normal_with_2_points> auch einfacher mit 2 objekten
  #   aufzurufen
  #   """
  #   # vielleicht sinnlos, besser löschen

  def __repr__(self):
    n = len(self.Klassenname())
    txt = 'Mirror(phi=' + repr(self.phi)
    txt += ", theta=" + repr(self.theta)
    txt += ', ' + super().__repr__()[n+1::]

    # txt = 'Mirror(phi=' + repr(self.phi)
    # txt += ", theta=" + repr(self.theta)
    # txt += ', name="' + self.name
    # txt += '", pos='+repr(self.pos)[6:-1]
    # txt += ", norm="+repr(self.normal)[6:-1]+")"
    return txt

  def draw_fc(self):
    self.update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    
    obj = model_mirror(**self.draw_dict)
    return obj

  def draw_mount_fc(self):
    self.update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    # self.draw_dict["mount_type"] = "POLARIS-K1-Step"
    # self.draw_dict["Radius"] = 0
    obj = mirror_mount(**self.draw_dict)
    return obj



class Curved_Mirror(Mirror):
  def __init__(self, radius=200, **kwargs):
    super().__init__(**kwargs)
    self.radius = radius
    self.draw_dict["Radius"] = self.radius

  @property
  def radius(self):
    return self.__radius
  @radius.setter
  def radius(self, x):
    self.__radius = x
    if x == 0:
      self._matrix[1,0] = 0
    else:
      self._matrix[1,0] = -2/x

  def focal_length(self):
    return self.radius/2

  def next_ray(self, ray):
    # r1 = self.refraction(ray)
    # r2 = self.reflection(r1)
    r2 = self.next_ray_trace(ray)
    return r2

  def __repr__(self):
    txt = 'Curved_Mirror(radius=' + repr(self.radius)
    txt += ', ' + super().__repr__()[7::]
    return txt

  def next_geom(self, geom):
    r0 = Ray()
    r0.set_geom(geom)
    r1 = self.next_ray(r0)
    return r1.get_geom()

  def draw_fc(self):
    self.update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    # self.draw_dict["mount_type"] = "POLARIS-K1-Step"
    self.draw_dict["Radius1"] = self.radius
    obj = model_mirror(**self.draw_dict)
    return obj
  
  def next_ray_trace(self, ray):
    """
    erzeugt den nächsten Ray auf Basis der analytischen Berechung von Schnitt-
    punkt von Sphere mit ray und dem vektoriellen Reflexionsgesetz
    siehe S Hb o LaO S 66 f

    Parameters
    ----------
    ray : TYPE Ray
      input ray

    Returns
    -------
    ray2 : TYPE Ray
      output ray

    """
    ray2 = deepcopy(ray)
    ray2.name = "next_" + ray.name
    center = self.pos - self.radius * self.normal
    p0 = ray.intersect_with_sphere(center, self.radius) #Auftreffpunkt p0
    surface_norm = p0 - center #Normale auf Spiegeloberfläche in p0 
    surface_norm *= 1/np.linalg.norm(surface_norm) #normieren
    #Reflektionsgesetz
    ray2.normal = ray.normal - 2*np.sum(ray.normal*surface_norm)*surface_norm
    ray2.pos = p0
    return ray2


# class Stripe_Mirror(Curved_Mirror):
#   """
#   das gleiche wie ein Curved_Mirror, nur als Streifen
#   wird in Offner-Streckern eingesetzt
#   ...eigentlich reine Kosmetik, alles Raytracing ist das gleiche
#   """
#   def __init__(self, **kwargs):
#     super().__init__(**kwargs)
#     self.height = 10
#     self.thickness = 25
#     self.dia = 75
  
#   def draw_fc(self):
#     obj = model_stripe_mirror(name=self.name, dia=self.dia, R1=-self.radius, 
#                               thickness=self.thickness, height=self.height, 
#                               geom_info=self.get_geom())
#     return obj
  

def tests():
  m = Mirror(phi=90, theta=0) # einfacher Flip Mirror
  r0 = Ray()
  r1 = m.next_ray(r0)
  print(m)
  print(r0)
  print(r1)
  print()
  m.phi = 23
  m.theta = 34
  r2 = m.next_ray(r0)
  print(r2)
  m.draw()
  print(m.recompute_angles())
  return m, r0, r1, r2

def curved_mirror_test():
  cm = Curved_Mirror()
  r = Ray(pos = (-100, 0, 85))
  r2 = cm.next_ray(r)
  return cm, r,r2

if __name__ == "__main__":
  tests()