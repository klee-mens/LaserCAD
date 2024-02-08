# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 11:53:43 2022

@author: mens
"""
import numpy as np
from . constants import TOLERANCE
from . geom_object import Geom_Object
from .. freecad_models import freecad_da, model_ray_1D


DEFAULT_LENGTH = 200

class Ray(Geom_Object):
  """
  Klasse für Strahlen
  erbt von Geom_Object
  besitzt neben pos und normal auch length zum zeichnen
  neue Methoden:
    endpoint()
    intersection_with(element)
    h_alpha_to(element)
    h_alpha_theta_to(element)
    from_h_alpha_theta
  """
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.length = DEFAULT_LENGTH #willkürlich, muss immer neu berechnet werden
    self.wavelength = 660e-6 #Wellenlänge in mm; Default: 660nm
    self.update_draw_dict()
    self.freecad_model = model_ray_1D
    # self.draw_dict.update({"length":self.length})

  def endpoint(self):
    return self.pos + self.length * self.normal

  def intersection(self, element):
    """
    ermittelt den Schnittpunkt vom Strahl mit der ebene eines opt Elements

    Parameters
    ----------
    element : Geom_Object
      Element mit dessen Ebene der Schnittpunkt berechnet wird

    Returns
    -------
    endpoint

    """
    delta_p = element.pos - self.pos
    s = np.sum(delta_p*element.normal) / np.sum(self.normal * element.normal)
    return self.pos + s * self.normal

  def intersect_with(self, element):
    """
    ermittelt den Schnittpunkt vom Strahl mit der ebene eines opt Elements
    und setzt seine Länge auf den Abstand self.pos--element.pos (bedenken!)

    Parameters
    ----------
    element : Geom_Object
      Element mit dessen Ebene der Schnittpunkt berechnet wird

    Returns
    -------
    endpoint

    """
    delta_p = element.pos - self.pos
    s = np.sum(delta_p*element.normal) / np.sum(self.normal * element.normal)
    self.length = s
    return self.endpoint()

  def intersect_with_sphere(self, center, radius):
    """
    ermittelt den Schnittpunkt vom Strahl mit einer Spähre, die durch 
    <center> € R^3 und <radius> € R definiert ist
    und setzt seine Länge auf den Abstand self.pos--element.pos (bedenken!)
    siehe Springer Handbook of Lasers and Optics Seite 66 f

    Parameters
    ----------
    center : TYPE 3D-array
      Mittelpunkt der Sphäre 

    radius : TYPE float
      Radius der Sphäre; >0 für konkave Spiegel (Fokus), <0 für konvexe

    Returns
    -------
    endpoint : TYPE 3D-array
    """
    diffvec = center - self.pos
    k = np.sum( diffvec * self.normal )
    w = np.sqrt(k**2 - np.sum(diffvec**2) + radius**2)
    s1 = k + w
    s2 = k - w
    #Fallunterscheidung
    if radius < 0 and s2 > 0:
      dist = s2
    else:
      dist = s1
    self.length = dist
    endpoint = self.endpoint()
    return endpoint
  
  def sphere_intersection(self, center, radius):
    """
    ermittelt den Schnittpunkt vom Strahl mit einer Spähre, die durch 
    <center> € R^3 und <radius> € R definiert ist
    und setzt seine Länge auf den Abstand self.pos--element.pos (bedenken!)
    siehe Springer Handbook of Lasers and Optics Seite 66 f

    Parameters
    ----------
    center : TYPE 3D-array
      Mittelpunkt der Sphäre 

    radius : TYPE float
      Radius der Sphäre; >0 für konkave Spiegel (Fokus), <0 für konvexe

    Returns
    -------
    endpoint : TYPE 3D-array
    """
    diffvec = center - self.pos
    k = np.sum( diffvec * self.normal )
    w = np.sqrt(k**2 - np.sum(diffvec**2) + radius**2)
    s1 = k + w
    s2 = k - w
    #Fallunterscheidung
    if radius < 0 and s2 > 0:
      dist = s2
    else:
      dist = s1
    # self.length = dist
    endpoint = self.pos + dist * self.normal
    return endpoint
  
  def h_alpha_to(self, element):
    """
    ermittelt die Parameter (h, alpha) der geometrischen Optik, wenn Ray()
    auf ein Element trifft (verwendet intersection)
    """
    p = self.intersection(element)
    h = np.linalg.norm(p - element.pos)
    v = element.normal
    return np.array((h, self.angle_to(v)))

  def h_alpha_theta_to(self, element):
    """
    ermittelt die Parameter (h, alpha) der geometrischen Optik, wenn Ray()
    auf ein Element trifft, sowie den Winkel <theta> unter dem die ray.normal zur
    z-Achse des elements steht (verwendet intersection)
    """
    h, alpha = self.h_alpha_to(element)
    ep = self.endpoint()
    v = ep - element.pos
    vabs = np.linalg.norm(v)
    if vabs < TOLERANCE:
       theta = 0 # kein Winkel bestimmbar, default=0
    else:
       v = v / vabs
       xa, ya, za = element.get_axes()
       c = np.cross(za, v) #Winkel mit z-Achse
       sign = 1 if np.sum(c * xa) >= 0 else -1
       theta = np.arcsin(np.linalg.norm(c))*sign
    return (h, alpha, theta)

  def from_h_alpha_theta(self, h, alpha, theta, element):
    """
    setzt das ray geom so, dass er in Bezug auf <element> die geometrischen
    Parameter <h, alpha, theta> hat

    Parameters
    ----------
    h : float
    alpha : float - Winkel im Bogenmaß
    theta : float - Winkel im Bogenmaß
    element : geom_object
    """
    self.set_geom(element.get_geom())
    # pos, norm = element.get_geom()
    # pos = element.pos
    # norm = element.normal
    xa, ya, za = element.get_coordinate_system()
    vec_in_eb = za*np.cos(theta) - ya*np.sin(theta)
    self.pos += vec_in_eb*h
    rotation_vec = np.cross(vec_in_eb, xa)
    self.rotate(rotation_vec, -alpha)

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["length"] = self.length

  # def draw_freecad(self, **kwargs):
    # self.update_draw_dict()
    # obj = model_ray_1D(**self.draw_dict)
    # return obj



  # def draw(self):
  #   if freecad_da:
  #     model_ray_1D(name=self.name, length=self.length, geom=self.get_geom())
  #   else:
  #     txt = "Der Strahl <" + self.name + "> wird von "
  #     txt += str(self.pos) + " mit der Ausrichtung " + str(self.normal)
  #     txt += " bis nach " + str(self.endpoint()) + " gezeichnet."
  #     print(txt)
  #     return txt

#   def copy(self):
#     cop = Ray()
#     cop.name = self.name
#     cop.set_geom(self.get_geom())
#     cop.length = self.length
#     return cop

def tests():
  r = Ray()
  r.draw()
  g = Geom_Object()
  g.pos = (120, 0, 85)
  # Schnittpunkt, Länge, h, alpha
  print("Schnittpunkt von r mit g bei", r.intersect_with(g))
  print("Sollte bei", g.pos, " liegen")
  print("Gesamte Länge:", r.length)
  print("h, alpha auf g:", r.h_alpha_to(g))
  r.normal = (1,0,1)
  h, a = r.h_alpha_to(g)
  print("Winkel alpha: ", a*180/np.pi)
  print("Am besten 45°")

  # Tests mit h, alpha, theta
  print()
  r = Ray()
  g = Geom_Object()
  r.pos = g.pos + np.array((0, -10, 10))
  rx, ry, rz = r.get_axes()
  r.rotate(ry, np.pi/6)
  print("Normale von um 30° gedrehtem ray", r.normal)
#   print("", r.h_alpha_theta_to(g))
  print("", r.h_alpha_theta_to(g))
  print()

  r2 = Ray()
  r2.set_geom(g.get_geom())
  r2.from_h_alpha_theta(*r.h_alpha_theta_to(g), g)
  print(r)
  print("vs")
  print(r2)
  print("Merke, ein Strahl aus h, alpha, theta ist nicht eindeutig")
  print(r.h_alpha_theta_to(g))
  print("vs")
  print(r2.h_alpha_theta_to(g))

  print()
  r2.from_h_alpha_theta(10, -0.02, 0.3, g)
  print("r = r.from_h_alpha_theta(10, -0.02, 0.3, g)")
  print(r2.h_alpha_theta_to(g))

  r2.draw()
  return r, r2, g


if __name__ == "__main__":
  tests()


