# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:28:07 2022

@author: mens
"""

from .geom_object import TOLERANCE, NORM0
from .ray import Ray
from .optical_element import Opt_Element
from .mount import Stripe_Mirror_Mount, Rooftop_Mirror_Mount, Unit_Mount
from ..freecad_models import model_mirror, model_stripe_mirror, model_rooftop_mirror
import numpy as np
from copy import deepcopy


class Mirror(Opt_Element):
  """
  Spiegelklasse, erbit von <Opt_Element>, nimmt einen ray und transformiert
  ihn entsprechend des Reflexionsgesetzes
  Anwendung wie folgt:

  m = Mirror(phi=90)
  r = Ray()
  m.set_geom(r.get_geom())
  nr = m.next_ray(r)

  dreht <r> in der xy-Ebene um den Winkel <phi> €[-180,180] und dreht um
  <theta> € [-90,90] aus der xy-Ebene heraus, wenn man die normale voher mit
  set_geom() einstellt
  """
  def __init__(self, phi=180, theta=0, name="NewMirror", **kwargs):
    super().__init__(name=name, **kwargs)
    self.__incident_normal = np.array(NORM0) # default von Strahl von x
    self.__theta = theta
    self.__phi = phi
    self.update_normal()
    self.freecad_model = model_mirror

  def update_normal(self):
    """
    aktualisiert die Normale des Mirrors entsprechend der __incident_normal,
    phi und theta
    """
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
    """
    setzt <pos> und __incident_normal auf <geom> und akturalisiert dann die
    eigene <normal> entsprechend <phi> und <theta>

    Parameters
    ----------
    geom : 2-dim Tupel aus 3-D float arrays
      (pos, normal)
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
    self.__theta = x
    self.update_normal()
    
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
    ray2.pos = self.intersection(ray) #dadruch wird ray.length verändert(!)
    k = ray2.normal
    km = -self.normal
    scpr = np.sum(km*k)
    newk = k-2*scpr*km
    ray2.normal = newk
    # print("REFL", k, km, scpr, newk, ray2.normal)
    return ray2

  def next_ray(self, ray):
    return self.reflection(ray)
  
  def through_out_beam(self, beam):
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
    """
    setzt neue <__incident_normal> und berechnet daraus mit <phi> und <theta>
    die neue <normal>
    """
    vec = vec / np.linalg.norm(vec)
    self.__incident_normal = np.array((1.0,1.0,1.0)) * vec
    self.update_normal()

  def recompute_angles(self):
    """
    berechnet die Winkel neu aus <__incident_normal> und <normal>
    """
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
    super().update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    self.draw_dict["Radius"] = 0

  def kostenbauder(self, inray=Ray()):
    kmatrix = np.eye(4)
    # kmatrix[0:2, 0:2] = self.matrix(inray=inray)
    kmatrix[0:2, 0:2] = -self.matrix(inray=inray)
    return np.array(kmatrix)



class Curved_Mirror(Mirror):
  def __init__(self, radius=200, **kwargs):
    super().__init__(**kwargs)
    self.radius = radius

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

  def __repr__(self):
    n = len(self.class_name())
    txt = self.class_name() + '(radius=' + repr(self.radius)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["Radius"] = self.radius
    self.draw_dict["dia"]=self.aperture
    # self.draw_dict["Radius1"] = self.radius

  def intersection(self, ray):
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
    diffvec = self.pos - self.radius*self.normal - ray.pos
    k = np.sum( diffvec * ray.normal )
    w = np.sqrt(k**2 - np.sum(diffvec**2) + self.radius**2)
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
    # p0 = ray.intersect_with_sphere(center, self.radius) #Auftreffpunkt p0
    p0 = self.intersection(ray) #Auftreffpunkt p0
    surface_norm = p0 - center #Normale auf Spiegeloberfläche in p0
    surface_norm *= 1/np.linalg.norm(surface_norm) #normieren
    ray2.normal = ray.normal - 2*np.sum(ray.normal*surface_norm)*surface_norm
    ray2.pos = p0
    return ray2



class Stripe_mirror(Curved_Mirror):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.aperture *= 3 #default 3inch
    self.thickness = 25
    self.height = 10
    self.freecad_model = model_stripe_mirror
    self.set_mount_to_default()

  def set_mount_to_default(self):
    smm = Stripe_Mirror_Mount(mirror_thickness=self.thickness)
    smm.set_geom(self.get_geom())
    # smm.pos += self.normal * self.thickness
    self.Mount = smm

  def update_draw_dict(self):
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

# from .component import Component
# class Rooftop_mirror(Component):
#   def __init__(self, **kwargs):
#     super().__init__(**kwargs)
#     self.freecad_model = model_rooftop_mirror
#     self.set_mount_to_default()

#   def set_mount_to_default(self):
#     smm = Rooftop_Mirror_Mount()
#     smm.set_geom(self.get_geom())
#     smm.pos += self.normal * self.aperture / 2
#     self.Mount = smm

#   def update_draw_dict(self):
#     super().update_draw_dict()
#     self.draw_dict["dia"] = self.aperture
#     self.draw_dict["model_type"] = "Rooftop"


# def Rooftop_mirror_draw_test():
#   rm = Rooftop_mirror()
#   rm.pos = (120,50,130)
#   rm.normal = (1,-1,0)
#   rm.aperture = 10
#   rm.set_mount_to_default()
#   rm.draw()
#   rm.draw_mount()

  # def set_mount_to_default(self):
  #   self.mount = Composed_Mount()

    # self.mount.set_geom(self.get_geom())

  # def _update_mount_dict(self):
  #   super()._update_mount_dict()
  #   self.mount_dict["model"] = "Stripe mirror mount"
  #   self.mount_dict["name"] = self.name + "_mount"
  #   # self.mount_dict["aperture"] = self.aperture
  #   self.mount_dict["thickness"] = self.thickness

  # def draw_fc(self):
  #   self.update_draw_dict()
  #   self.draw_dict["dia"]=self.aperture
  #   # self.draw_dict["mount_type"] = "POLARIS-K1-Step"
  #   self.draw_dict["Radius1"] = self.radius
  #   self.draw_dict["thickness"] = self.thickness
  #   self.draw_dict["model_type"] = "Stripe"
  #   obj = model_mirror(**self.draw_dict)
  #   return obj

  # def __repr__(self):
  #   n = len(self.class_name())
  #   txt = 'Stripe_mirror(' + super().__repr__()[n+1::]
  #   return txt

  # def draw_mount(self):
  #   # self.update_mount()
  #   self._update_mount_dict()
  #   self.mount = Composed_Mount()
  #   self.mount.set_geom(self.get_geom())
  #   mon1 = Special_mount(**self.mount_dict)
  #   # print(mon1.normal,mon1.docking_obj.normal,mon1.docking_normal)
  #   # mon1.docking_obj.normal = -self.normal
  #   mon2 = Mount(aperture=25.4*2)
  #   self.mount.add(mon1)
  #   self.mount.add(mon2)
  #   # print(self.aperture)
  #   return (self.mount.draw())



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

  # def focal_length(self):
  #   return self.radius/2

  # def next_ray(self, ray):
  #   # r1 = self.refraction(ray)
  #   # r2 = self.reflection(r1)
  #   r2 = self.next_ray_tracing(ray)
  #   return r2

  # def __repr__(self):
  #   txt = 'Cylindrical_Mirror(radius=' + repr(self.radius)
  #   txt += ', ' + super().__repr__()[7::]
  #   return txt

  # def next_geom(self, geom):
  #   r0 = Ray()
  #   r0.set_geom(geom)
  #   r1 = self.next_ray(r0)
  #   return r1.get_geom()

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    self.draw_dict["Radius"] = self.radius
    self.draw_dict["height"]=self.height
    self.draw_dict["thickness"]=self.thickness

  # def draw_fc(self):
  #   self.update_draw_dict()
  #   self.draw_dict["dia"]=self.aperture
  #   # self.draw_dict["mount_type"] = "POLARIS-K1-Step"
  #   self.draw_dict["Radius1"] = self.radius
  #   obj = model_mirror(**self.draw_dict)
  #   # default = Vector(0,0,1)
  #   # xx,yy,zz = self.get_coordinate_system()
  #   # zz = Vector(zz)
  #   # angle = default.getAngle(zz)*180/np.pi
  #   # vec = default.cross(zz)
  #   # rotate(obj, vec, angle, off0=0)
  #   return obj

  def next_ray(self, ray):
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
        print(ray2)
        ray2.draw()
        print("ray_origin=",ray_origin)
        print("ray_direction=",ray_direction)
        print("cylinder_center=",cylinder_center)
        print("cylinder_axis=",cylinder_axis)
        return None

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


class Cylindrical_Mirror1(Cylindrical_Mirror):
  @property
  def radius(self):
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
      self._matrix[1,0] = 0


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