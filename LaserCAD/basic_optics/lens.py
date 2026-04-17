#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 20:28:02 2022

@author: mens
"""

from ..freecad_models import model_lens, lens_mount
from .optical_element import Opt_Element
from .constants import inch
import numpy as np
from copy import deepcopy
from scipy.optimize import brentq


class Lens(Opt_Element):
  def __init__(self, f=100, name="NewLens", **kwargs):
    super().__init__(name=name, **kwargs)
    self.focal_length = f
    self.thickness = 4
    self.freecad_model = model_lens

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
    return self.ABCD_refraction(ray)

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["Radius1"] = 400
    self.draw_dict["Radius2"] = 0

  def __repr__(self):
    n = len(self.class_name())
    txt = 'Lens(f=' + repr(self.focal_length)
    txt += ', ' + super().__repr__()[n+1::]
    return txt


class Thicklens(Opt_Element):
  """
  Build a thick lens with given focal length, refractive index, aperture and edge thickness.

  Parameters
  ----------
    f : float
      Focal length of the lens in mm
    n : float
      Refractive index of the lens material
    aperture : float
      Aperture of the lens in mm
    biconvex : bool
      If True, the lens is biconvex. If False, it is plano-convex.
    thickness : float, optional
      Thickness of the lens in mm. If None, it is calculated from the edge thickness. The default is None.
    edge_thickness : float, optional
      Edge thickness of the lens in mm. The default is 3 mm. for a lens with f < 0 this is equal to the thickness, since an edge thickness parameter is non-practical here.
  
  Functions
  ---------
    radius1()
      Calculates the radius of curvature of the first lens surface using the lens maker equation and assuming that the second surface is either flat or has the same radius of curvature as the first surface (biconvex).
    radius2()
      Calculates the radius of curvature of the second lens surface. Returns 0 for plano-convex lenses.
    intersection(ray, radius, thickness=0)
      Calculates the intersection point of a ray with a spherical surface of given radius and thickness offset. Note that f>0 corresponds to a convex lens surface and vice versa. For radius=0, a plane intersection is calculated. The reference point should be the plane of the center of the lens. For the back surface, the thickness of the lens needs to be added as an offset. see Springer Handbook of Lasers and Optics page 66f.
    refraction(ray, R, from_material = False)
      Calculates the refracted ray at a spherical surface with radius R. If from_material is True, the ray is refracted from the lens material to air, otherwise from air to lens material. Same notation as in Springer Handbook of Lasers and Optics page 68.
    next_ray(ray)
      Calculates the refracted ray through the thick lens by calculating the refraction at both surfaces using the refraction function.
  """
  def __init__(self, f=100, n=1.5, name="NewThickLens", aperture=1*inch, biconvex=False, thickness=None, edge_thickness=3, **kwargs):
    super().__init__(name=name, **kwargs)
    self.focal_length = f
    self.edge_thickness = edge_thickness
    self.refractive_index = n
    self.biconvex = biconvex
    self.aperture = aperture
    self.thickness = self.calc_thickness() if thickness is None else thickness

    self.calc_principal_planes()
    self.freecad_model = model_lens
    self.set_Mount()

  def set_Mount(self):
    self.set_mount_to_default()
    if self.biconvex: 
      self.Mount.pos += self.normal * (self.thickness/2 - 4.5)
    else:
      self.Mount.pos += self.normal * (self.thickness-9)


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

  def calc_thickness(self):
    if self.focal_length < 0:
      return self.edge_thickness
    # Calculate R1 from the edge thickness, focal length, refractive index and aperture
    if self.biconvex: 
      R_low = self.aperture/2 * 1.01
      R_high = self.aperture*20
      R1 = brentq(self.radius_function, R_low, R_high)
      thickness = self.edge_thickness + 2*R1 - 2*np.sqrt(R1**2 - (self.aperture/2)**2)
    else: 
      R1 = (self.refractive_index-1)*self.focal_length
      thickness = self.edge_thickness + R1 - np.sqrt(R1**2 - (self.aperture/2)**2)
    return thickness

  
  def radius_function(self, R):
    f = self.focal_length
    delta = self.edge_thickness
    n = self.refractive_index

    if R <= self.aperture/2:
      return 1e6 # very large radius ~ flat
    else:
      d = delta + 2*R - 2*np.sqrt(R**2 - (self.aperture/2)**2)
      lhs = 1/f
      rhs = (n-1)*(2/R - (n-1)*d/(n*R**2))
      return lhs - rhs
  
  def radius1(self):
    f = self.focal_length
    d = self.thickness
    n = self.refractive_index
    if not self.biconvex:
      return (n-1)*f
    else:
      return (n-1)*(f+np.sign(f)*np.sqrt(f**2-f*d/n))
    
  def radius2(self):
    if not self.biconvex:
      return 0
    else:
      return -self.radius1()
  
  def calc_principal_planes(self):
    """
    Calculates the positions of the principal planes h1 and h2 relative to the lens center.
    Positive signs indicate the principle plane is located outside the lens, negative signs inside. 

    For an imaging with an object and image distance g and b, the distances to propagate are g+h1 and b+h2. 
    """
    R1 = self.radius1()
    R2 = self.radius2()
    n = self.refractive_index
    d = self.thickness
    f = self.focal_length

    self.h1 =  f*(n-1)*d/(R2*n) if R2 != 0 else 0
    self.h2 = -f*(n-1)*d/(R1*n) if R1 != 0 else 0

  
  def intersection(self, ray, radius):
    """
    ermittelt den Schnittpunkt vom Strahl mit einer Spähre, die durch
    <center> € R^3 und <radius> € R definiert ist
    und setzt seine Länge auf den Abstand self.pos--element.pos (bedenken!)
    siehe Springer Handbook of Lasers and Optics Seite 66 f

    if radius = 0: plane intersection is calculated

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
    if radius == 0:
      return self.intersection_plane(ray)
    
    radius = -radius
    diffvec = self.pos - radius*self.normal - ray.pos
    k = np.sum( diffvec * ray.normal )
    w = np.sqrt(k**2 - np.sum(diffvec**2) + radius**2)
    s1 = k + w
    s2 = k - w
    #Fallunterscheidung
    if radius < 0 and s2 > 0:
      dist = s2
    else:
      dist = s1
    ray.length = dist
    return ray.endpoint()
  
  def intersection_plane(self, ray):
    """
    Calculates the intersection point of the ray with a plane given by a 
    Geom_Object (e.g a thin lens).

    Parameters
    ----------
    element : Geom_Object
      Element in the intersection plane.
    set_length : optional
      Sets the length of the ray so that it end on the object plane if true. 
      The default is True.

    Returns
    -------
    endpoint
    """
    C = self.pos
    n_z = self.normal 
    a = ray.normal
    p = ray.pos

    s0 = np.sum((C-p)*n_z) / np.sum(a*n_z)
    ray.length = s0
    
    return ray.endpoint()
  
  
  def next_ray(self, ray):
    mid_ray = self.refraction(ray, R=self.radius1(), from_material=False)
    self.pos += self.normal * self.thickness
    out_ray = self.refraction(mid_ray, R=self.radius2(), from_material=True)
    self.pos -= self.normal * self.thickness
    # mid_ray.draw()

    return out_ray
  
  def refraction(self, ray, R, from_material = False):
    # See Springer Handbook of Lasers and Optics page 68
    ray2 = deepcopy(ray)
    ray2.pos = self.intersection(ray, R)
    center = self.pos + self.normal * R
    N = self.normal if R == 0 else (ray2.pos - center)
    N = N / np.linalg.norm(N)
    a1 = ray.normal
    n1n2 = self.refractive_index if from_material else 1/self.refractive_index

    a2 = n1n2* a1 - n1n2*np.sum(a1*N)* N + np.sqrt(1 - n1n2**2*(1 - np.sum(a1*N)**2))* N
    if np.sign(np.sum(a1*N)) != np.sign(np.sum(a2*N)):
      a2 = n1n2* a1 - n1n2*np.sum(a1*N)* N - np.sqrt(1 - n1n2**2*(1 - np.sum(a1*N)**2))* N
    ray2.normal = a2
    # if np.isnan(ray2.normal).any():
    #   ray2.normal = ray.normal
    #   print("no intersection with lens surface")

    return ray2

  def update_draw_dict(self):
    super().update_draw_dict()
    radius = self.radius1()
    self.draw_dict["Radius1"] = radius
    self.draw_dict["Radius2"] = radius if self.biconvex else 0

  def __repr__(self):
    n = len(self.class_name())
    txt = 'Lens(f=' + repr(self.focal_length)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

def tests():
  from basic_optics import Ray

  l1 = Lens(name="susanne")
  l2 = eval(repr(l1))
  print(l2)

  print()

  r = Ray(pos = (0,0,90))
  print(r)
  r2 = l1.next_ray(r)
  print(r2)
  s = l1.focal_length / r2.normal[0]
  h = r2.normal[2]*s
  print(h)
  print("sollte bei -10 liegen")


if __name__ == "__main__":
  tests()