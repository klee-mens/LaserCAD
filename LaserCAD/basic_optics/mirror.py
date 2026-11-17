# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:28:07 2022

@author: mens
"""

from .geom_object import TOLERANCE, NORM0
from .ray import Ray
from .optical_element import Opt_Element
from .mount import Stripe_Mirror_Mount, Unit_Mount, Composed_Mount
from ..freecad_models import model_mirror, model_stripe_mirror, model_crystal
from ..freecad_models.utils import inch
import numpy as np
import warnings
from copy import deepcopy


class Mirror(Opt_Element):
  """Mirror class, inherits from <Opt_Element>. Reflects a ray according to the law of reflection.

  Parameters
  ----------
  phi : float
    Angle in degrees in [-180, 180] by which the mirror rotates the incident ray
    in the xy-plane (mathematically positive direction). The default 180
    sends the ray back.
  theta : float
    Angle in degrees in [-90, 90] by which the mirror rotates the ray out of
    the xy-plane.

  Examples
  --------
  >>> m = Mirror(phi=90)
  >>> r = Ray()
  >>> m.set_geom(r.get_geom())   # the mirror is placed at the ray
  >>> nr = m.next_ray(r)         # the ray is deflected by 90 degrees
  """
  def __init__(self, phi=180, theta=0, name="NewMirror", **kwargs):
    super().__init__(name=name, **kwargs)
    self.__incident_normal = np.array(NORM0) # default von Strahl von x
    self.__theta = theta
    self.__phi = phi
    self.update_normal()
    self.freecad_model = model_mirror

  def update_normal(self):
    """Update the normal of the mirror from the incident direction, phi and theta."""
    phi = self.__phi/180*np.pi
    theta = self.__theta/180*np.pi
    if phi == 0 and theta == 0:
      print("Warnung, Spiegel unbestimmt und sinnlos, beide Winkel 0")
      self.normal = (0,1,0)
      return -1

    rho = self.__incident_normal[0:2]
    rho_abs = np.linalg.norm(rho)
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
    self.normal = self.__incident_normal - (x2, y2, z2)

  def set_geom(self, geom):
    """Set <pos> and the incident direction from <geom>, then update the normal from <phi> and <theta>.

    Parameters
    ----------
    geom : tuple of (3-D array, 3x3 array)
      (pos, axes)
    """
    # print("GEOM-MIRROR:", geom)
    self.pos = geom[0]
    axes = geom[1]
    self.__incident_normal = axes[:,0]
    self.update_normal()

  @property
  def phi(self):
    """
    beschreibt den Winkel <phi> um den der Mirror einen Strahl in
    <__incident_normal> Richtung in der xy-Ebene durch Reflexion weiter dreht
    (mathematisch positive Drehrichtung)
    stellt über Setter sicher, dass die normale entsprechend aktualisiert wird
    """
    return self.__phi
  @phi.setter
  def phi(self, x):

    """Angle <phi> in degrees by which the mirror deflects a ray coming from the incident
    direction in the xy-plane (mathematically positive direction).
    The setter updates the normal accordingly.
    """
    self.__phi = x
    self.update_normal()

  @property
  def theta(self):
    """
    beschreibt den Winkel <theta> um den der Mirror einen Strahl in
    <__incident_normal> Richtung aus der xy-Ebene durch Reflexion weiter dreht
    (mathematisch positive Drehrichtung)
    stellt über Setter sicher, dass die normale entsprechend aktualisiert wird
    """
    return self.__theta
  @theta.setter
  def theta(self, x):
    """Angle <theta> in degrees by which the mirror deflects a ray coming from the incident
    direction out of the xy-plane (mathematically positive direction).
    The setter updates the normal accordingly.
    """
    self.__theta = x
    self.update_normal()

  def reflection(self, ray):
    """Return the next ray from <ray> using the law of reflection.

    Note that the <normal> of the mirror points the other way than in the
    convention of e.g. the Springer Handbook of Optics and Lasers, p. 68.

    Parameters
    ----------
    ray : Ray
      incident ray

    Returns
    -------
    reflected ray
    """
    ray2 = deepcopy(ray)
    ray2.pos = self.intersection(ray) #dadruch wird ray.length verändert(!)
    k = ray2.normal
    km = -self.normal
    scpr = np.sum(km*k)
    newk = k-2*scpr*km
    ray2.normal = newk
    # print("REFL", k, km, scpr, newk, ray2.normal)
    return ray2

  def next_ray(self, ray):
    """Return the ray after the reflection at the mirror (vectorial law of reflection)."""
    return self.reflection(ray)

  def through_out_beam(self, beam):
    """Return a copy of <beam> that propagates through the mirror without reflection."""
    newb = deepcopy(beam)
    newb.name = "next_" + beam.name
    rays = beam.get_all_rays(by_reference=True)
    newrays = []
    for ray in rays:
      nr = self.just_pass_through(ray)
      if not nr:
        return False
      newrays.append(nr)
    newb.override_rays(newrays)
    return newb

  def set_incident_normal(self, vec):
    """Set a new incident direction and compute the new <normal> from <phi> and <theta>."""
    vec = vec / np.linalg.norm(vec)
    self.__incident_normal = np.array((1.0,1.0,1.0)) * vec
    self.update_normal()

  def recompute_angles(self):
    """Recompute <phi> and <theta> from the incident direction and the <normal>."""
    vec1 = self.__incident_normal
    dummy = Ray()
    dummy.normal=vec1
    #nur um next_ray und reflectino zu nutzen
    reflected_dummy = self.next_ray(dummy)
    vec2 = reflected_dummy.normal
    xy1 = vec1[0:2]
    xy2 = vec2[0:2]
    teiler = np.linalg.norm(xy1) * np.linalg.norm(xy2)
    if teiler < TOLERANCE:
      #wenn die Komponenten verschwinden, kann kein Winkel bestimmt werden
      phi = 0
    else:
      phi0 = np.arcsin( (xy1[0]*xy2[1]-xy1[1]*xy2[0]) /teiler) * 180/np.pi
      scalar = np.sum(xy1*xy2)
      if scalar >= 0:
        phi = phi0
      else:
        phi = -180 - phi0 if (phi0 < 0) else 180 - phi0
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
    """Set the normal so that a ray coming from <p0> that hits the mirror at self.pos is reflected towards <p1>.

    The angles <phi> and <theta> are recomputed afterwards.
    """
    inc = self.pos - p0
    refl = p1 - self.pos
    inc *= 1/np.linalg.norm(inc)
    refl *= 1/np.linalg.norm(refl)
    # print("nextnormal", (inc - refl)/np.linalg.norm(inc - refl))
    self.normal = inc - refl
    # <phi> und <theta> sind relativ zur Einfallsrichtung definiert. Die ist
    # hier bekannt und muss gesetzt werden, sonst werden die Winkel relativ zu
    # einer veralteten Einfallsrichtung berechnet (im Extremfall liegt der
    # Hilfsstrahl in recompute_angles parallel zum Spiegel -> Division durch 0)
    self.__incident_normal = np.array(inc)
    self.__phi, self.__theta =  self.recompute_angles()

  def set_normal_with_output_direction(self, output_vec=(0,1,0)):
    """
    sets the normal of the mirror using its __incident_normal and a direction
    where the reflected beam should go

    Example
    m = Mirror()
    m.set_normal_with_output_direction(output_vec=(0,1,0))

    Parameters
    ----------
    output_vec : TYPE, optional
      DESCRIPTION. The default is (0,1,0).

    Returns
    -------
    None.

    """
    p0 = self.pos - self.__incident_normal
    p1 = self.pos + output_vec
    self.set_normal_with_2_points(p0, p1)

  def __repr__(self):
    n = len(self.class_name())
    txt = self.class_name() + '(phi=' + repr(self.phi)
    txt += ", theta=" + repr(self.theta)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def update_draw_dict(self):
    """Update the drawing parameters (draw_dict) from the current attributes."""
    super().update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    self.draw_dict["Radius"] = 0

  def kostenbauder(self, inray=Ray()):
    """Return the 4x4 Kostenbauder matrix of the mirror for the ray <inray>."""
    kmatrix = np.eye(4)
    # kmatrix[0:2, 0:2] = self.matrix(inray=inray)
    kmatrix[0:2, 0:2] = -self.matrix(inray=inray)
    return np.array(kmatrix)



class Curved_Mirror(Mirror):
  """Spherical mirror.

  Parameters
  ----------
  radius : float
    Radius of curvature in mm. Positive values focus (concave), the focal
    length is radius/2. Inherits phi, theta and name from Mirror.

  Notes
  -----
  For a tilted mirror the ray tracing (next_ray) is exact. The ABCD matrix
  is the paraxial one at normal incidence unless the class attribute
  `angle_dependent_matrix` is set to True; then the tangential and sagittal
  powers are 2/(R*cos(theta)) and 2*cos(theta)/R (exact for horizontal or
  vertical incidence planes).
  """
  def __init__(self, radius=200, **kwargs):
    super().__init__(**kwargs)
    self.radius = radius

  @property
  def radius(self):
    """Radius of curvature in mm; 0 means a plane mirror. Setting it updates the ABCD matrix (C = -2/R)."""
    return self.__radius
  @radius.setter
  def radius(self, x):
    self.__radius = x
    if x == 0:
      self._matrix[1,0] = 0
    else:
      self._matrix[1,0] = -2/x

  def focal_length(self):
    """Focal length in mm (radius/2)."""
    return self.radius/2

  # False (Standard): Matrix wie bisher, C = -2/R unabhängig vom Einfallswinkel.
  # True: C = -P mit der Brechkraft P in der horizontalen Ebene beim
  # tatsächlichen Einfallswinkel (siehe _horizontal_power).
  angle_dependent_matrix = False

  def matrix(self, inray=Ray()):
    """Return the 2x2 ABCD matrix of the mirror, see the class docstring for the angle dependence."""
    M = np.array(self._matrix)
    if self.angle_dependent_matrix and self.radius != 0:
      M[1,0] = -self._horizontal_power(inray)
    return M

  def _curvature_direction(self):
    """Direction of the curvature in the tangential plane of the mirror (unit vector).

    None if the mirror is curved equally in all directions (sphere).
    """
    return None

  def _horizontal_power(self, inray):
    """Optical power P (1/mm) of the mirror for the horizontal beam coordinate (perpendicular to the beam and to the z-axis) for the incident ray <inray>.

    For a mirror with curvature tensor K (sphere: K = 1/R) the following holds in the
    plane of incidence (t) and perpendicular to it (s) for the angle of incidence theta:
      P_tt = 2 K_tt / cos(theta),  P_ss = 2 K_ss * cos(theta),  P_ts = 2 K_ts
    Examples: sphere, horizontal plane of incidence: 2/(R cos theta); vertical
    plane of incidence: 2 cos(theta)/R; cylinder with the z-axis in a
    horizontal beam path: 2/(R cos theta).
    This is exact for a horizontal or vertical plane of incidence. For an
    oblique plane of incidence the horizontal and vertical planes mix
    (astigmatic coupling), and a 2x2 matrix is only an approximation.
    """
    R = self.radius
    n = self.normal
    k = np.array(inray.normal, dtype=float)
    k = k / np.linalg.norm(k)
    cos_t = max(abs(np.dot(k, n)), 1e-6)
    e_h = np.cross((0, 0, 1), k)
    if np.linalg.norm(e_h) < 1e-9:      # Strahl senkrecht: keine horizontale Richtung
      return 2/R
    e_h = e_h / np.linalg.norm(e_h)
    k_tang = k - np.dot(k, n)*n
    if np.linalg.norm(k_tang) < 1e-9:   # senkrechter Einfall: t beliebig
      t = np.cross(n, (0, 0, 1))
      if np.linalg.norm(t) < 1e-9:
        t = np.array((0.0, 1.0, 0.0))
    else:
      t = k_tang
    t = t / np.linalg.norm(t)
    s = np.cross(n, t)
    c = self._curvature_direction()
    if c is None:
      K = np.eye(2) / R
    else:
      ct, cs = np.dot(c, t), np.dot(c, s)
      K = np.array(((ct*ct, ct*cs), (ct*cs, cs*cs))) / R
    P = 2*np.array(((K[0,0]/cos_t, K[0,1]), (K[0,1], K[1,1]*cos_t)))
    t_beam = np.cross(s, k)
    t_beam = t_beam / np.linalg.norm(t_beam)
    e = np.array((np.dot(e_h, t_beam), np.dot(e_h, s)))
    return float(e @ P @ e)

  def __repr__(self):
    n = len(self.class_name())
    txt = self.class_name() + '(radius=' + repr(self.radius)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def update_draw_dict(self):
    """Update the drawing parameters (draw_dict), including the radius of curvature."""
    super().update_draw_dict()
    self.draw_dict["Radius"] = self.radius
    self.draw_dict["dia"]=self.aperture
    # self.draw_dict["Radius1"] = self.radius

  def intersection(self, ray):
    """Return the intersection point of <ray> with the spherical surface of the mirror.

    The sphere has its center at pos - radius*normal. The length of <ray> is set
    to the distance to the intersection point (see Springer Handbook of Lasers and
    Optics, p. 66 ff). If the ray misses the sphere, a warning is issued and a NaN
    point is returned.

    Returns
    -------
    endpoint : 3D-array
    """
    diffvec = self.pos - self.radius*self.normal - ray.pos
    k = np.sum( diffvec * ray.normal )
    radicand = k**2 - np.sum(diffvec**2) + self.radius**2
    if radicand < 0:
      # Strahl verfehlt die Kugel: sichtbar machen, Ergebnis ist NaN
      warnings.warn(f"{type(self).__name__}: ray misses the mirror surface "
                    f"(no intersection with the sphere)", UserWarning,
                    stacklevel=2)
      ray.length = np.nan
      return ray.endpoint()
    w = np.sqrt(radicand)
    s1 = k + w
    s2 = k - w
    #Fallunterscheidung
    if self.radius < 0 and s2 > 0:
      dist = s2
    else:
      dist = s1
    ray.length = dist
    endpoint = ray.endpoint()
    return endpoint

  def next_ray(self, ray):
    """Return the next ray: analytic intersection of the ray with the sphere and
    the vectorial law of reflection (Springer Handbook of Lasers and Optics, p. 66 ff).

    Parameters
    ----------
    ray : Ray
      input ray

    Returns
    -------
    ray2 : Ray
      output ray
    """
    ray2 = deepcopy(ray)
    ray2.name = "next_" + ray.name

    center = self.pos - self.radius * self.normal
    # p0 = ray.intersect_with_sphere(center, self.radius) #Auftreffpunkt p0
    p0 = self.intersection(ray) #Auftreffpunkt p0
    surface_norm = p0 - center #Normale auf Spiegeloberfläche in p0
    surface_norm *= 1/np.linalg.norm(surface_norm) #normieren
    ray2.normal = ray.normal - 2*np.sum(ray.normal*surface_norm)*surface_norm
    ray2.pos = p0
    return ray2



class Stripe_mirror(Curved_Mirror):
  """Curved mirror with a wide, flat stripe shape (default aperture 3 inch).

  Used e.g. as the large folding mirror in stretchers and compressors. All
  parameters are those of Curved_Mirror; the mount is a Stripe_Mirror_Mount.
  """
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.aperture *= 3 #default 3inch
    self.thickness = 25
    self.height = 10
    self.freecad_model = model_stripe_mirror
    self.set_mount_to_default()

  def set_mount_to_default(self):
    """Use a Stripe_Mirror_Mount at the position of the mirror."""
    smm = Stripe_Mirror_Mount(mirror_thickness=self.thickness)
    smm.set_geom(self.get_geom())
    # smm.pos += self.normal * self.thickness
    self.Mount = smm

  def update_draw_dict(self):
    """Add the height and the stripe model type to <draw_dict>."""
    super().update_draw_dict()
    self.draw_dict["height"] = self.height
    self.draw_dict["model_type"] = "Stripe"

def stripe_mirror_draw_test():
  sm = Stripe_mirror()
  sm.pos = (130, 89, 120)
  sm.normal = (1,1,0)
  sm.thickness = 40
  sm.set_mount_to_default()
  sm.draw()
  sm.draw_mount()



class Cylindrical_Mirror(Stripe_mirror):
  """
  The class of Cylindrical mirror.
  Cylindrical mirror have those parameters:
    radius: The curvature of the mirror
    height: The vertical thickness of the mirror
    thickness: The horizontal thickness of the mirror
  The default mirror is placed horizontally, which means the cylinder_center
  points tp the z-axis. Use rotate function if you want to rotate the mirror.
  """
  def __init__(self, radius=200,height=10, thickness=25, **kwargs):
    super().__init__(**kwargs)
    self.radius = radius
    # self.draw_dict["Radius"] = radius
    self.height=height
    self.thickness=thickness
    self.draw_dict["model_type"]="Stripe"
    self.freecad_model = model_mirror
    self.Mount = Unit_Mount("dont_draw")

  @property
  def radius(self):
    """Radius of curvature in mm of the curved direction."""
    return self.__radius
  @radius.setter
  def radius(self, x):
    """
    This part is incorrect. Since I don't know the matrix of Cylindrical_Mirror
    Parameters
    ----------
    x : TYPE
      DESCRIPTION.
    """
    self.__radius = x
    if x == 0:
      self._matrix[1,0] = 0
    else:
      self._matrix[1,0] = -2/x


  def _curvature_direction(self):
    # gekrümmt ist die Richtung senkrecht zur Zylinderachse (z-Achse des
    # Spiegelkoordinatensystems) in der Spiegelebene, also dessen y-Achse
    return self.get_coordinate_system()[1]

  def update_draw_dict(self):
    """Add aperture, radius, height and thickness to <draw_dict>."""
    super().update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    self.draw_dict["Radius"] = self.radius
    self.draw_dict["height"]=self.height
    self.draw_dict["thickness"]=self.thickness

  def next_ray(self, ray):
    """Return the next ray: analytic intersection of the ray with the cylinder and
    the vectorial law of reflection.

    If the ray misses the cylinder, a warning is issued and a ray with NaN
    position and axes is returned.

    Parameters
    ----------
    ray : Ray
      input ray

    Returns
    -------
    ray2 : Ray
      output ray
    """
    ray2 = deepcopy(ray)
    ray2.name = "next_" + ray.name
    self.normal *= 1/np.linalg.norm(self.normal)
    center = self.pos - self.radius * self.normal
    xx,yy,zz = self.get_coordinate_system()
    ray_origin = ray2.pos
    ray_direction = ray2.normal
    cylinder_center = center
    cylinder_axis = zz

    ray_origin = np.array(ray_origin)
    ray_direction = np.array(ray_direction)
    cylinder_center = np.array(cylinder_center)
    cylinder_axis = np.array(cylinder_axis)
    middle_vec = cylinder_center + cylinder_axis * (np.dot(ray_origin,cylinder_axis) - np.dot(cylinder_center,cylinder_axis))-ray_origin
    middle_vec2 = cylinder_axis*(np.dot(ray_direction,cylinder_axis))-ray_direction
    a = np.dot(middle_vec2 , middle_vec2)
    b = 2 * np.dot(middle_vec2 , middle_vec)
    c = np.dot(middle_vec , middle_vec) - self.radius **2


    # Compute discriminant
    discriminant = b**2 - 4 * a * c

    # If discriminant is negative, no intersection
    if discriminant < 0:
        # Strahl verfehlt den Zylinder: sichtbar machen, Ergebnis ist ein
        # Strahl mit NaN-Position und -Richtung (wie bei Curved_Mirror)
        warnings.warn(f"{type(self).__name__}: ray misses the cylinder surface "
                      f"(no intersection)", UserWarning, stacklevel=2)
        ray2._pos = np.full(3, np.nan)
        ray2._axes = np.full((3, 3), np.nan)
        return ray2

    # Compute t parameter (parameter along the ray direction)
    t1 = (-b + np.sqrt(discriminant)) / (2 * a)
    t2 = (-b - np.sqrt(discriminant)) / (2 * a)

    # Check if intersection is within ray segment
    # if t1 < 0 and t2 < 0:
    #     return None

    # Select smallest positive t
    # t = min(t1, t2) if t1 >= 0 and t2 >= 0 else max(t1, t2)
    if self.radius>0:
      t = max(t1, t2)
    else:
      t = min(t1, t2)
    # Compute intersection point

    intersection_point = ray_origin + ray_direction * t
    p0 = intersection_point
    new_center = cylinder_center + cylinder_axis * (np.dot(p0,cylinder_axis)-np.dot(cylinder_center,cylinder_axis))
    surface_norm = p0 - new_center #Normale auf Spiegeloberfläche in p0
    surface_norm *= 1/np.linalg.norm(surface_norm) #normieren
    #Reflektionsgesetz
    # print(cylinder_center,new_center)
    ray2.normal = ray.normal - 2*np.sum(ray.normal*surface_norm)*surface_norm
    ray2.pos = p0
    dist = p0-ray.pos
    ray.length=np.sqrt(dist[0]**2+dist[1]**2+dist[2]**2)
    return ray2


class Rectangular_Mirror(Mirror):
  """Flat mirror with a rectangular shape.

  Parameters
  ----------
  height, width : float
    Size of the mirror in mm.
  phi, theta : float
    Deflection angle and tilt in degrees, see Mirror.
  """
  def __init__(self, name="NewRectMirror", height=25, width=25, phi=180, theta=0, **kwargs):
    super().__init__(phi=phi, theta=theta, name=name, **kwargs)
    self.height = height
    self.width = width
    # self.thickness = thickness
    self.freecad_model = model_crystal
    # self.draw_dict["color"] = (131/255,27/255,44/255)

  def update_draw_dict(self):
    """Add height, width and thickness to <draw_dict>."""
    super().update_draw_dict()
    self.draw_dict["height"] = self.height
    self.draw_dict["width"] = self.width
    self.draw_dict["thickness"] = self.thickness


class Newport_Mirror(Mirror):
  """Creates a mirror with a Newport mount. The size of the mount is determined by the aperture of the mirror. The default mount is back-mounted.
  
  parameters
  ----------
  phi : float, optional
      The angle of the mirror in degrees. The default is 180.
  name : str, optional
      The name of the mirror. The default is "Newport Mirror".
  aperture : float, optional
      The aperture of the mirror. The default is inch.
  thickness : float, optional
      The thickness of the mirror. The default is 6.
  mirror : bool, optional
      If True, the mirror is left-handed. The default is False.
  """
  def __init__(self, name="Newport Mirror", aperture=inch, thickness=6, mirror=False, **kwargs):
    super().__init__(name=name, aperture=aperture, thickness=thickness, **kwargs)
    self.aperture = aperture
    add_name = "_LH" if mirror else ""
    if aperture == inch:
        model = "U100-A2K"
    elif aperture == 2*inch:
        model = "U200-A2K"
    elif aperture == 3*inch:
        model = "U300-A2K"
    elif aperture == 4*inch:
        model = "U400-AC2K"

    self.set_mount(Composed_Mount(unit_model_list=[model+add_name, "1inch_post"]))
    self.set_mount_back_mounted()
            

class Newport_Curved_Mirror(Curved_Mirror):
  """Creates a curved mirror with a Newport mount. The size of the mount is determined by the aperture of the mirror. The default mount is back-mounted.
    
    parameters
    ----------
    phi : float, optional
        The angle of the mirror in degrees. The default is 180.
    radius : float, optional
        The radius of the mirror. The default is 200.
    name : str, optional
        The name of the mirror. The default is "Newport Mirror".
    aperture : float, optional
        The aperture of the mirror. The default is inch.
    thickness : float, optional
        The thickness of the mirror. The default is 6.
    mirror : bool, optional
        If True, the mirror is left-handed. The default is False.
    """
  def __init__(self, name="Newport Mirror", aperture=inch, thickness=6, mirror=False, **kwargs):
    super().__init__(name=name, aperture=aperture, thickness=thickness, **kwargs)
    self.aperture = aperture
    add_name = "_LH" if mirror else ""
    if aperture == inch:
        model = "U100-A2K"
    elif aperture == 2*inch:
        model = "U200-A2K"
    elif aperture == 3*inch:
        model = "U300-A2K"
    self.set_mount(Composed_Mount(unit_model_list=[model+add_name, "1inch_post"]))
    self.set_mount_back_mounted()

# class Cylindrical_Mirror1(Cylindrical_Mirror):
#   @property
#   def radius(self):
#     return self.__radius
#   @radius.setter
#   def radius(self, x):
#     """
#     This part is incorrect. Since I don't know the matrix of Cylindrical_Mirror
#     Parameters
#     ----------
#     x : TYPE
#       DESCRIPTION.
#     """
#     self.__radius = x
#     if x == 0:
#       self._matrix[1,0] = 0
#     else:
#       self._matrix[1,0] = 0


 # def draw_fc(self):
   # self.update_draw_dict()

   # obj = model_mirror(**self.draw_dict)
   # return obj

 # def draw_mount(self):
   # self.update_mount()
   # if self.Mount.elm_type != "dont_draw":
   #   # self._update_mount_dict()
   #   self.Mount.elm_type = "mirror"
   #   self.Mount.pos = self.pos
   #   self.Mount.normal = self.normal
   #   self.Mount.aperture = self.aperture
   #   self.Mount.Flip90 = self.mount_dict["Flip90"]
   #   # self._update_mount_dict()
   #   self.Mount.model = self.mount_dict['model']
   #   self.Mount.post_type = self.mount_dict["post_type"]
   # return (self.Mount.draw())

 # def draw_mount_fc(self):
   # self.update_draw_dict()
   # self.draw_dict["dia"]=self.aperture
   # now we will use the old geom definition with (pos, norm) in a dirty,
   # hacky way, because I don't want to fix the 10.000 usages of geom in
   # the mirror_mount function manually, no, I don't
   # helper_dict = dict(self.draw_dict)
   # # helper_dict["geom"] = (self.pos, self.normal)
   # xshift=0
   # obj = mirror_mount(**helper_dict)
   # M = Mount(aperture=self.aperture)
   # M.set_geom(self.get_geom())
   # P = Post_and_holder(xshift=M.xshift,height=-M.zshift)
   # P.set_geom(M.get_geom())
   # obj1=M.draw()
   # obj2=P.draw()
   # post_pos = xshift*self.normal+self.pos
   # part = initialize_composition_old(name="New class for mount and post")
   # cc= obj1,obj2
   # add_to_composition(part, cc)
   # del obj1,obj2
   # return part





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