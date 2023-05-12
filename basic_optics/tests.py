# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 19:46:37 2023

@author: mens
"""

from .lens import Lens
from .mirror import Mirror, Curved_Mirror,Cylindrical_Mirror
from .beam import Beam
from .moduls import Make_Telescope
# from .propagation import Propagation
from .ray import Ray
from .composition import Composition
from .grating import Grating
import numpy as np
import matplotlib.pyplot as plt

from .iris import Iris
from .intersection_plane import Intersection_plane

from .resonator import Resonator

# from iris import Iris
# from intersection_plane import Intersection_plane



# def Telescope_4beam():
#   teles = Make_Telescope(name="teles", lens1_aperture=50, lens2_aperture=50)
#   teles.draw()
#   dist = 8
#   b0 = Beam(name="b1", angle=0)
#   b0.pos += (0, dist, dist)
#   bs = [b0]
#   for elm in teles._elements:
#     if not type(elm) == type(Propagation()):
#       beam = bs[-1]
#       bs.append(elm.next_beam(beam))
#       beam.draw()

#   be = bs[-1]
#   be.draw()
#   return (bs, teles)


def Lens_4beam_Fokus():
  """
  erstellt 4 Kollimierte Strahlen die durch eine Linse der Brennweite focus in
  einem Punkt gebündelt werden
  um die Brennebene zu veranschaulichen wird ein Spiegel an die Position gezeichnet

  Returns
  -------
  bs : list of beams
    input beams
  nbs : list of beams
    focused beams
  foc_lens : Lens()
    focussing lens
  plane_mirror : Mirror()
    marks the focus plane

  """
  dist = 8
  focus = 200
  lens_pos = 100
  bs = []
  for i in range(4):
    bs.append(Beam(angle=0))
    bs[i].name = "Kollimated_beam_" + str(i+1)

  bs[0].pos = (0, dist, -dist)
  bs[1].pos = (0, dist, dist)
  bs[2].pos = (0, -dist, -dist)
  bs[3].pos = (0, -dist, dist)
  foc_lens = Lens(name="focusing lens", f=focus, pos=(lens_pos, 0,0))
  foc_lens.draw()

  nbs = []
  for i in range(4):
    nbs.append(foc_lens.next_beam(bs[i]))
    # nbs[i].length=1.2*focus
    bs[i].draw()
    nbs[i].draw()

  plane_mirror = Mirror(name="plane", pos = (lens_pos+focus, 0, 0))
  plane_mirror.aperture = 50
  plane_mirror.draw()
  for i in range(4):
    plane_mirror.next_beam(nbs[i])
  return (bs, nbs, foc_lens, plane_mirror)


def Lens_4beam_Fokus_with_tild():
  """
  so ziemlich das gleiche wie Lens_4beam_Fokus {
  erstellt 4 Kollimierte Strahlen die durch eine Linse der Brennweite focus in
  einem Punkt gebündelt werden
  um die Brennebene zu veranschaulichen wird ein Spiegel an die Position gezeichnet
  }
  aber mit kleinem Winkel der Strahlen zur Linseachse

  Returns
  -------
  bs : list of beams
    input beams
  nbs : list of beams
    focused beams
  foc_lens : Lens()
    focussing lens
  plane_mirror : Mirror()
    marks the focus plane

  """
  dist = 8
  focus = 200
  lens_pos = 100
  bs = []
  for i in range(4):
    bs.append(Beam(angle=0, normal=(1,0, 0.1)))
    bs[i].name = "Kollimated_beam_" + str(i+1)

  bs[0].pos = (0, dist, -dist)
  bs[1].pos = (0, dist, dist)
  bs[2].pos = (0, -dist, -dist)
  bs[3].pos = (0, -dist, dist)
  foc_lens = Lens(name="focusing lens", f=focus, pos=(lens_pos, 0,0))
  foc_lens.aperture = 80
  foc_lens.draw()

  nbs = []
  for i in range(4):
    nbs.append(foc_lens.next_beam(bs[i]))
    # nbs[i].length=1.2*focus
    bs[i].draw()
    nbs[i].draw()

  plane_mirror = Mirror(name="plane", pos = (lens_pos+focus, 0, 0))
  plane_mirror.aperture = 50
  plane_mirror.draw()
  for i in range(4):
    plane_mirror.next_beam(nbs[i])
  return (bs, nbs, foc_lens, plane_mirror)


  """
  so ziemlich das gleiche wie Lens_4beam_Fokus {
  erstellt 4 Kollimierte Strahlen die durch eine Linse der Brennweite focus in
  einem Punkt gebündelt werden
  um die Brennebene zu veranschaulichen wird ein Spiegel an die Position gezeichnet
  }
  aber mit 5° Winkel im letzten Speigel und kompletter Back prop, sollte wieder
  4 kollimierte Strahlen in andere Richtung ergeben

  Returns
  -------
  bs : list of beams
    input beams
  nbs : list of beams
    focused beams
  foc_lens : Lens()
    focussing lens
  plane_mirror : Mirror()
    marks the focus plane

  """
  dist = 8
  focus = 200
  lens_pos = 100
  bs = []
  for i in range(4):
    bs.append(Beam(angle=0))
    bs[i].name = "Kollimated_beam_" + str(i+1) #4 kollimierte Anfangsstrahlen

  bs[0].pos = (0, dist, -dist)
  bs[1].pos = (0, dist, dist)
  bs[2].pos = (0, -dist, -dist)
  bs[3].pos = (0, -dist, dist)
  foc_lens = Lens(name="focusing lens", f=focus, pos=(lens_pos, 0,0))
  foc_lens.draw()
  print()

  nbs = []
  for i in range(4):
    nbs.append(foc_lens.next_beam(bs[i]))
    # nbs[i].length=1.2*focus
    bs[i].draw()
    nbs[i].draw() #4 fokussierte Strahlen nach der Linse
    print("Beamfokus:", nbs[i].focal_length())

  print()
  plane_mirror = Mirror(name="plane", pos = (lens_pos+focus, 0, 0), theta=5)
  plane_mirror.aperture = 50
  plane_mirror.draw()
  nnbs = []
  nnnbs = []
  # end_mirror = Mirror(name="end_mirror", pos=(0,0,0))
  for i in range(4):
    #4 zurück nach oben refl Strahlen unter leichtem Winkel
    nnbs.append(plane_mirror.next_beam(nbs[i]))
    #4 zurück wieder kollimerte Strahlen unter leichtem Winkel
    nnnbs.append(foc_lens.next_beam(nnbs[i]))
    nnbs[i].draw()
    nnnbs[i].draw()
    # end_mirror.next_beam(nnnbs[i]) #nur um den letzten Strahl wieder auf die richtige
  return (bs, nbs, nnbs, nnnbs, foc_lens, plane_mirror)



def Parallel_ray_bundle_tilted_lens():
  """
  schießt eine Matrix aus line_count x line_count parallelen rays auf eine Linse
  unter einem bestimmten Winkel
  ...Sollten alle in einem Punkt fokussiert werden

  Returns
  -------
  die komplette Komposition

  """
  dist = 3
  line_count = 5
  rays = []
  pos0 = np.array( ( 0, -dist*(line_count//2), -dist*(line_count//2) ) )
  for m in range(line_count):
    for n in range(line_count):
      r = Ray()
      r.pos = pos0 + np.array( (0, m*dist, n*dist) )
      rays.append(r)

  bundel = Beam()
  Ray0 = Ray()
  rm = rays[line_count**2//2]
  Ray0.set_geom(rm.get_geom())
  rays.insert(0, Ray0)
  bundel.override_rays(rays)

  comp = Composition(name="Parallel_ray_bundle_tilted_lens_test")
  comp.set_light_source(bundel)
  comp.pos = 2*bundel.pos #geht bsetimmt auch schöner
  # p1 = Propagation(d=100)
  le = Lens(f=200)
  # p2 = Propagation(d=200)
  # comp.add(p1)
  comp.propagate(100)
  comp.add_on_axis(le)
  comp.propagate(200)
  # comp.add(p2)
  le.normal = (1,0.1,0.1)
  le.normal *= -1 #sollte keine Rolle spielen -> Test für den Raytracer

  comp.draw_elements()
  comp.draw_rays()

  return comp

# def Parallel_ray_bundle_tilted_mirror_ray_trace(focal_length = 200):
#   """
#   schießt eine Matrix aus line_count x line_count parallelen rays auf einen
#   sphärischen Spiegel unter einem bestimmten Winkel und berechnet die neuen
#   Strahlen mittels analytischem Raytracing
#   ...Sollten alle in einem Punkt fokussiert werden, +- Astigmatismus

#   Returns
#   -------
#   die komplette Komposition

#   """
#   dist = 3
#   line_count = 5
#   rays = []
#   pos0 = np.array( ( 0, -dist*(line_count//2), -dist*(line_count//2) ) )
#   for m in range(line_count):
#     for n in range(line_count):
#       r = Ray()
#       r.pos = pos0 + np.array( (0, m*dist, n*dist) )
#       rays.append(r)

#   bundel = Beam()
#   bundel.override_rays(rays)

#   comp = Composition(name="Parallel_ray_bundle_tilted_lens_test")
#   comp.set_light_source(bundel)
#   comp.pos = 2*bundel.pos #geht bsetimmt auch schöner
#   p1 = Propagation(d=100)
#   # le = Lens(f=focal_length)
#   le = Curved_Mirror(radius=2*focal_length)
#   p2 = Propagation(d=200)
#   comp.add(p1)
#   comp.add(le)
#   comp.add(p2)
#   le.normal = (1,0.1,0.1)

#   comp.draw()
#   comp.draw_rays()

#   return comp

def grating_ray_bundle_test(draw=False):
  """
  erzeugt ein 1D ray-Bündel und schickt es auf ein Grating, von dem dann ein
  entsprechendes aufgefächertes Bündel ausgehen sollte

  Returns
  -------
  TYPE
    DESCRIPTION.

  """
  grat = Grating()
  grat.pos += (100, 0, 0)
  grat.normal = (1, -0.2, 0)

  wavelength_range = np.linspace(800e-6, 1000e-6, 20) #alle Wellenlängen in mm
  rays0 = []
  for wavelen in wavelength_range:
    r = Ray()
    r.wavelength = wavelen
    rays0.append(r)


  rays1 = [grat.next_ray(x) for x in rays0]

  plane = Mirror()
  plane.normal *= -1
  for ray in rays1:
    ray.intersect_with(plane)

  if draw:
    for ray in rays0:
      ray.draw()
    for ray in rays1:
      ray.draw()
    grat.draw()
  return rays0, rays1


def all_moduls_test():
  from .moduls import Make_Periscope, Make_Telescope, Make_Amplifier_Typ_II_simple, Make_Stretcher, Make_White_Cell

  peris = Make_Periscope()
  peris.pos = (0,0,100)
  peris.draw()

  teles = Make_Telescope()
  teles.pos = (0, 500,100)
  teles.draw()

  amp = Make_Amplifier_Typ_II_simple(roundtrips2=3)
  amp.pos = (0, 1000, 100)
  amp.draw()

  stretch = Make_Stretcher()
  stretch.pos = (0, 1500, 100)
  stretch.draw()

  wcell = Make_White_Cell(roundtrips4=2)
  wcell.pos = (0, 2000, 100)
  wcell.draw()

  return peris, teles, amp, stretch, wcell

def iris_test():
  # rg=RayGroup(waist=2.5,pos=(0,0,100))
  rg=Beam(radius=2.5,angle=0)
  # rg.make_square_distribution(10)
  dia1 = Composition(name="RayGroup test")
  dia1.set_light_source(rg)
  opt_element_count = 0
  dia1.normal=(-1,0,0)
  dia1.propagate(100)
  m1=Mirror(phi=-90)
  dia1.add_on_axis(m1)
  opt_element_count += 1
  dia1.propagate(150)
  m2=Mirror(phi=-90)
  dia1.add_on_axis(m2)
  opt_element_count += 1
  dia1.propagate(150)
  l1=Lens(f=150)
  dia1.add_on_axis(l1)
  opt_element_count += 1
  dia1.propagate(150)

  ip1=Intersection_plane()
  dia1.add_on_axis(ip1)
  opt_element_count += 1
  ip1_seq = opt_element_count
  # ip1.spot_diagram(dia1.compute_beams().pop())
  dia1.propagate(150)

  l2=Lens(f=150)
  dia1.add_on_axis(l2)
  opt_element_count += 1
  dia1.propagate(150)

  iris = Iris(dia=4)
  dia1.add_on_axis(iris)
  opt_element_count += 1
  dia1.propagate(150)

  l3=Lens(f=150)
  dia1.add_on_axis(l3)
  opt_element_count += 1
  dia1.propagate(150)

  ip2=Intersection_plane()
  dia1.add_on_axis(ip2)
  opt_element_count += 1
  ip2_seq = opt_element_count
  dia1.propagate(150)
  # ip2.spot_diagram(dia1.compute_beams().pop())

  dia1.draw_elements()
  dia1.draw_rays()
  dia1.draw_mounts()
  dia1.draw_beams()

  # ip1.spot_diagram(dia1._ray_groups[ip1_seq])
  # ip2.spot_diagram(dia1._ray_groups[-1])
  ip2.spot_diagram(dia1._beams[-2])
  return dia1


def Intersection_plane_spot_diagram_test():
  # from .iris import Iris
  from .beam import RayGroup
  from .intersection_plane import Intersection_plane
  rg=RayGroup(waist=2.5,pos=(0,0,100))
  rg.make_square_distribution(10)
  dia1 = Composition(name="RayGroup test")
  dia1.set_light_source(rg)
  dia1.normal=(-1,0,0)
  dia1.propagate(100)
  m1=Mirror(phi=-90)
  dia1.add_on_axis(m1)
  dia1.propagate(150)
  m2=Mirror(phi=-90)
  dia1.add_on_axis(m2)
  dia1.propagate(150)
  l1=Lens(f=150)
  dia1.add_on_axis(l1)
  dia1.propagate(150)
  ip1=Intersection_plane()
  dia1.add_on_axis(ip1)
  ip1.spot_diagram(dia1.compute_beams().pop())
  dia1.propagate(150)
  l2=Lens(f=150)
  dia1.add_on_axis(l2)
  dia1.propagate(300)
  l3=Lens(f=150)
  dia1.add_on_axis(l3)
  dia1.propagate(150)
  ip2=Intersection_plane()
  dia1.add_on_axis(ip2)
  dia1.propagate(150)
  ip2.spot_diagram(dia1.compute_beams().pop())
  return dia1

def cavity_test(cm_radius = 200, cavity_length = 425, angle_shift = 2.796834341,
                cav_height = 100, ls_shift = 35, mr_shift =15,
                aperture_big = 25.4*2, aperture_small = 25.4/2):
  """


    Parameters
    ----------
    cm_radius : TYPE, optional
        The curvature of Curved_Mirror. The default is 200.
    cavity_length : TYPE, optional
        length of the cavity. The default is 425.
    angle_shift : TYPE, optional
        Angle of light incident on the cavity. The default is 2.796834341.
    cav_height : TYPE, optional
        Height of cavity. The default is 100.
    ls_shift : TYPE, optional
        The shift of the light sourse. The default is 35.
    mr_shift : TYPE, optional
        The shift of output miror. The default is 15.
    aperture_big : TYPE, optional
        The aperture of curved mirror. The default is 25.4*2.
    aperture_small : TYPE, optional
        the aperture of mirror. The default is 25.4/2.

    Returns
    -------
    None.

    """
  l_from_m1_to_cm1 = 1/(2/cm_radius - 2/cavity_length) - ls_shift
  cm1_x = l_from_m1_to_cm1*np.cos(angle_shift*2/180*np.pi)
  m1_y = l_from_m1_to_cm1*np.sin(angle_shift*2/180*np.pi)


  ls = Beam(radius=0.1,angle=0.05,wavelength=1030E-6, distribution="Gaussian",
            pos=(0,0,cav_height))
  cavset=Composition(name="Cavity Setting")
  cavset.set_light_source(ls)
  cavset.normal=(0,-1,0)
  cavset.pos=(0,ls_shift-m1_y,cav_height)

  m1 = Mirror()
  m1.pos = (0,-m1_y,cav_height)
  point0 = (0,ls_shift,cav_height)
  point1 = (-cm1_x,0,cav_height)
  m1.set_normal_with_2_points(point0, point1)
  m1.aperture = aperture_small

  cm1 = Curved_Mirror(radius= cm_radius)
  cm1.pos = (-cm1_x,0,cav_height)
  cm1.normal = (-1,0,0)
  point1 = (0,-m1_y,cav_height)
  point0 = cm1.pos+(cavity_length,0,0)
  cm1.set_normal_with_2_points(point0, point1)
  cm1.aperture = aperture_big

  cm2 = Curved_Mirror(radius= cm_radius,theta=-angle_shift*2)
  cm2.pos = cm1.pos+(cavity_length,0,0)
  cm2.aperture = aperture_big

  l_from_m2_to_cm2 = 1/(2/cm_radius-2/cavity_length) - mr_shift
  cm2_x =l_from_m2_to_cm2*np.cos(angle_shift*2/180*np.pi)
  cm2_z = l_from_m2_to_cm2*np.sin(angle_shift*2/180*np.pi)
  m2 = Mirror()
  m2.pos = cm2.pos -( cm2_x,0, cm2_z)
  point0 = cm2.pos
  point1 = m2.pos - (0,15,0)
  m2.set_normal_with_2_points(point0, point1)
  m2.aperture = aperture_small


  ip = Intersection_plane()
  ip.pos = m2.pos - (0,13.17,0)
  ip.normal = (0,-1,0)

  cavset.add_fixed_elm(m1)
  cavset.add_fixed_elm(cm1)
  cavset.add_fixed_elm(cm2)
  cavset.add_fixed_elm(m2)
  cavset.add_fixed_elm(ip)
  cavset.propagate(25)
  # ip.spot_diagram(cavset._ray_groups[-1])
  cavset.draw()

def Reflective_plane_test(Beam_radius = 2.5, Beam_angle = 0.1):
  """


    Parameters
    ----------
    Beam_radius : TYPE, optional
        The radius of the Beam. The default is 2.5.
    Beam_angle : TYPE, optional
        Scattering angle of beam. The default is 0.1.

    Returns
    -------
    None.

    """
  from .refractive_plane import Refractive_plane
  rg=Beam(radius=Beam_radius,angle=Beam_angle)
  rg.make_square_distribution(10)
  re_test = Composition(name = "refractive test")

  re_test.set_light_source(rg)
  re_test.pos=(0,0,100)
  re_test.normal = (1,0,0)
   # re_test.propagate(20)

  lens1 = Lens(f=20,pos=(10,0,100))
  re_test.add_fixed_elm(lens1)
  re_plane = Refractive_plane(r_ref_index=10,pos=(200,0,100))
  re_test.add_fixed_elm(re_plane)
  re_plane2 = Refractive_plane(r_ref_index=0.1,pos=(240,0,100))
  re_test.add_fixed_elm(re_plane2)
  re_test.propagate(50)
  re_test.draw_elements()
  re_test.draw_beams()

def Cylindrical_Mirror_test():
  """
  a simple Cylindrical_Mirror_test

  Returns
  -------
  None.

  """
  rg=Beam(radius=2.5,angle=0.1,pos=(-100,0,100))
  rg.normal = (1,0,0)
  rg.make_square_distribution(10)
  m = Cylindrical_Mirror(name="Standard_Mirror",radius=200, pos=(100,0,100))
  # m.normal = (1,1,0)
  # m.draw_dict["model_type"]="Rooftop"
  #m.normal = (1,0,0)
  # m.draw_dict["mount_type"] = "rooftop_mirror"
  m.aperture = 25.4*4
  m.draw()
  m.draw_mount()
  rg1 = m.next_beam(rg)
  # rg1.length = 2000
  rg.draw()
  rg1.draw()

def Stretcher_Cavity_test():
    Radius = 1000 #Radius des großen Konkavspiegels
    Aperture_concav = 6 * 25.4
    h_StripeM = 10 #Höhe des Streifenspiegels
    gamma = 21 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
    grat_const = 1/450 # Gitterkonstante in 1/mm
    seperation = 100 # Differenz zwischen Gratingposition und Radius
    lam_mid = 2400e-9 * 1e3 # Zentralwellenlänge in mm
    delta_lamda = 250e-9*1e3 # Bandbreite in mm
    number_of_rays = 20
    safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
    periscope_distance = 12

    # abgeleitete Parameter
    v = lam_mid/grat_const
    s = np.sin(gamma)
    c = np.cos(gamma)
    a = v/2
    b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
    sinB = a - b

    Concav = Curved_Mirror(radius=Radius, name="Concav_Mirror")
    Concav.pos = (0,0,0)
    Concav.aperture = Aperture_concav
    Concav.normal = (-1,0,0)
    # Concav._axes = np.array([[-1,0,0],[0,0,1],[0,1,0]])
    # Concav.draw_dict["height"]=40
    # Concav.draw_dict["thickness"]=25
    # Concav.draw_dict["model_type"]="Stripe"

    StripeM = Cylindrical_Mirror(radius= -Radius/2, name="Stripe_Mirror")
    StripeM.pos = (Radius/2, 0, 0)
    #Cosmetics
    StripeM.aperture=75
    StripeM.draw_dict["height"]=10
    StripeM.draw_dict["thickness"]=25
    StripeM.draw_dict["model_type"]="Stripe"

    Grat = Grating(grat_const=grat_const, name="Gitter")
    Grat.pos = (Radius-seperation, 0, 0)
    Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)

    ray0 = Ray()
    p_grat = np.array((Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM))
    vec = np.array((c, s, 0))
    pos0 = p_grat - 250 * vec
    ray0.normal = vec
    ray0.pos = pos0
    ray0.wavelength = lam_mid

    lightsource = Beam(radius=0, angle=0)
    wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
    rays = []
    cmap = plt.cm.gist_rainbow
    for wavel in wavels:
      rn = Ray()
      # rn.normal = vec
      # rn.pos = pos0
      rn.wavelength = wavel
      x = (wavel - lam_mid + delta_lamda/2) / delta_lamda
      rn.draw_dict["color"] = cmap( x )
      rays.append(rn)
    lightsource.override_rays(rays)

    nfm1 = - ray0.normal
    pfm1 = Grat.pos + 400 * nfm1 + (0,0,h_StripeM/2 + safety_to_StripeM + periscope_distance)
    # subperis = Periscope(length=8, theta=-90, dist1=0, dist2=0)
    # subperis.pos = pfm1
    # subperis.normal = nfm1
    flip_mirror1 = Mirror()
    flip_mirror1.pos = pfm1
    flip_mirror1.normal = nfm1 - np.array((0,0,-1))
    def useless():
      return None
    flip_mirror1.draw = useless
    flip_mirror1.draw_dict["mount_type"] = "dont_draw"

    flip_mirror2 = Mirror()
    flip_mirror2.pos = pfm1 - np.array((0,0,periscope_distance))
    flip_mirror2.normal = nfm1 - np.array((0,0,1))
    flip_mirror2.draw = useless
    flip_mirror2.draw_dict["mount_type"] = "dont_draw"

    pure_cosmetic = Mirror(name="RoofTop_Mirror")
    pure_cosmetic.draw_dict["model_type"]="Rooftop"
    pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror"
    pure_cosmetic.pos = (flip_mirror1.pos + flip_mirror2.pos ) / 2
    pure_cosmetic.normal = (flip_mirror1.normal + flip_mirror2.normal ) / 2
    pure_cosmetic.aperture = periscope_distance

    M1 = Mirror()
    M1.aperture = 25.4/2
    M1.pos = pos0 - (0,0,periscope_distance)
    point0 = p_grat - (0,0,periscope_distance)
    point1 = M1.pos + (100,0,0)
    M1.set_normal_with_2_points([point0], point1)

    M2 = Mirror()
    M2.aperture = 25.4/2
    M2.pos = M1.pos + (750,0,0)
    point0 = M1.pos
    point1 = p_grat - (-100,0,periscope_distance)
    M2.set_normal_with_2_points([point0], point1)

    Concav1 = Curved_Mirror(radius=500, name="Concav_Mirror")
    Concav1.pos = point1
    Concav1.aperture = 25.4*2
    # Concav1.normal = (-1,0,0)
    point0 = M2.pos
    point1 = Concav1.pos + (100,0,0)
    Concav1.set_normal_with_2_points(point0, point1)

    Concav2 = Curved_Mirror(radius=500, name="Concav_Mirror")
    Concav2.pos = Concav1.pos + (500,0,0)
    Concav2.aperture = 25.4*2
    Concav2.normal = (1,0,0)


    # pure_cosmetic.draw = useless

    Stretcher = Composition(name="Strecker", pos=pos0, normal=vec)

    Stretcher.set_light_source(lightsource)
    Stretcher.add_fixed_elm(Grat)
    Stretcher.add_fixed_elm(Concav)
    Stretcher.add_fixed_elm(StripeM)
    Stretcher.add_fixed_elm(flip_mirror2)
    Stretcher.add_fixed_elm(flip_mirror1)
    Stretcher.add_fixed_elm(M1)
    Stretcher.add_fixed_elm(M2)
    Stretcher.add_fixed_elm(Concav1)
    Stretcher.add_fixed_elm(Concav2)

    Stretcher.add_fixed_elm(pure_cosmetic)

    # for item in subperis._elements:
    #   Stretcher.add_fixed_elm(item)


    # seq = [0,1,2,1,0]
    # seq = [0,1,2,1,0, 3]
    # seq = [0,1,2,1,0, 3,4]
    seq = [0,1,2,1,0, 3,4, 0, 1, 2, 1, 0, 5, 6, 7, 8, 7]
    Stretcher.set_sequence(seq)
    Stretcher.propagate(1000)
    Stretcher.pos = (0,0,100)
    Stretcher.draw_elements()
    Stretcher.draw_mounts()
    Stretcher.draw_rays()

def Wrong_stretcher_with_two_Cylindrical_Mirror():
  Radius = 1000 #Radius des großen Konkavspiegels
  Aperture_concav = 6 * 25.4
  h_StripeM = 10 #Höhe des Streifenspiegels
  gamma = 21 /180 *np.pi # Seperationswinkel zwischen einfallenden und Mittelpunktsstrahl; Alpha = Gamma + Beta
  grat_const = 1/450 # Gitterkonstante in 1/mm
  seperation = 100 # Differenz zwischen Gratingposition und Radius
  lam_mid = 2400e-9 * 1e3 # Zentralwellenlänge in mm
  delta_lamda = 250e-9*1e3 # Bandbreite in mm
  number_of_rays = 20
  safety_to_StripeM = 5 #Abstand der eingehenden Strahlen zum Concav Spiegel in mm
  periscope_distance = 12

  # abgeleitete Parameter
  v = lam_mid/grat_const
  s = np.sin(gamma)
  c = np.cos(gamma)
  a = v/2
  b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
  sinB = a - b

  Concav = Cylindrical_Mirror(radius=Radius, name="Concav_Mirror")
  Concav.pos = (0,0,0)
  Concav.aperture = Aperture_concav
  Concav.normal = (-1,0,0)
  Concav._axes = np.array([[-1,0,0],[0,0,1],[0,1,0]])
  Concav.draw_dict["height"]=40
  Concav.draw_dict["thickness"]=25
  Concav.draw_dict["model_type"]="Stripe"

  StripeM = Cylindrical_Mirror(radius= -Radius/2, name="Stripe_Mirror")
  StripeM.pos = (Radius/2, 0, 0)
  #Cosmetics
  StripeM.aperture=75
  StripeM.draw_dict["height"]=10
  StripeM.draw_dict["thickness"]=25
  StripeM.draw_dict["model_type"]="Stripe"

  Grat = Grating(grat_const=grat_const, name="Gitter")
  Grat.pos = (Radius-seperation, 0, 0)
  Grat.normal = (np.sqrt(1-sinB**2), -sinB, 0)

  ray0 = Ray()
  p_grat = np.array((Radius-seperation, 0, -h_StripeM/2 - safety_to_StripeM))
  vec = np.array((c, s, 0))
  pos0 = p_grat - 250 * vec
  ray0.normal = vec
  ray0.pos = pos0
  ray0.wavelength = lam_mid

  lightsource = Beam(radius=0, angle=0)
  wavels = np.linspace(lam_mid-delta_lamda/2, lam_mid+delta_lamda/2, number_of_rays)
  rays = []
  cmap = plt.cm.gist_rainbow
  for wavel in wavels:
    rn = Ray()
    # rn.normal = vec
    # rn.pos = pos0
    rn.wavelength = wavel
    x = (wavel - lam_mid + delta_lamda/2) / delta_lamda
    rn.draw_dict["color"] = cmap( x )
    rays.append(rn)
  lightsource.override_rays(rays)

  nfm1 = - ray0.normal
  pfm1 = Grat.pos + 400 * nfm1 + (0,0,h_StripeM/2 + safety_to_StripeM + periscope_distance)
  # subperis = Periscope(length=8, theta=-90, dist1=0, dist2=0)
  # subperis.pos = pfm1
  # subperis.normal = nfm1
  flip_mirror1 = Mirror()
  flip_mirror1.pos = pfm1
  flip_mirror1.normal = nfm1 - np.array((0,0,-1))
  def useless():
    return None
  flip_mirror1.draw = useless
  flip_mirror1.draw_dict["mount_type"] = "dont_draw"

  flip_mirror2 = Mirror()
  flip_mirror2.pos = pfm1 - np.array((0,0,periscope_distance))
  flip_mirror2.normal = nfm1 - np.array((0,0,1))
  flip_mirror2.draw = useless
  flip_mirror2.draw_dict["mount_type"] = "dont_draw"

  pure_cosmetic = Mirror(name="RoofTop_Mirror")
  pure_cosmetic.draw_dict["model_type"]="Rooftop"
  pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror"
  pure_cosmetic.pos = (flip_mirror1.pos + flip_mirror2.pos ) / 2
  pure_cosmetic.normal = (flip_mirror1.normal + flip_mirror2.normal ) / 2
  pure_cosmetic.aperture = periscope_distance

  M1 = Mirror()
  M1.aperture = 25.4/2
  M1.pos = pos0 - (0,0,periscope_distance)
  point0 = p_grat - (0,0,periscope_distance)
  point1 = M1.pos + (100,0,0)
  M1.set_normal_with_2_points(point0, point1)

  M3 = Mirror()
  M3.aperture = 25.4/2
  M3.pos = p_grat - 300 * vec
  point0 = p_grat - (0,0,periscope_distance)
  M3.normal = -vec

  M2 = Mirror()
  M2.aperture = 25.4/2
  M2.pos = M1.pos + (750,0,0)
  point0 = M1.pos
  point1 = p_grat - (-100,0,periscope_distance)
  M2.set_normal_with_2_points([point0], point1)

  Concav1 = Curved_Mirror(radius=500, name="Concav_Mirror")
  Concav1.pos = point1
  Concav1.aperture = 25.4*2
  # Concav1.normal = (-1,0,0)
  point0 = M2.pos
  point1 = Concav1.pos + (100,0,0)
  Concav1.set_normal_with_2_points(point0, point1)

  Concav2 = Curved_Mirror(radius=500, name="Concav_Mirror")
  Concav2.pos = Concav1.pos + (500,0,0)
  Concav2.aperture = 25.4*2
  Concav2.normal = (1,0,0)


  # pure_cosmetic.draw = useless

  Stretcher = Composition(name="Strecker", pos=pos0, normal=vec)

  Stretcher.set_light_source(lightsource)
  Stretcher.add_fixed_elm(Grat)
  Stretcher.add_fixed_elm(Concav)
  Stretcher.add_fixed_elm(StripeM)
  # Stretcher.add_fixed_elm(flip_mirror2)
  # Stretcher.add_fixed_elm(flip_mirror1)
  # Stretcher.add_fixed_elm(M1)
  # Stretcher.add_fixed_elm(M2)
  # Stretcher.add_fixed_elm(Concav1)
  # Stretcher.add_fixed_elm(Concav2)
  # Stretcher.add_fixed_elm(M3)

  # Stretcher.add_fixed_elm(pure_cosmetic)

  # for item in subperis._elements:
  #   Stretcher.add_fixed_elm(item)


  # seq = [0,1,2,1,0]
  # seq = [0,1,2,1,0, 3]
  # seq = [0,1,2,1,0, 3,4]
  # seq = [0,1,2,1,0, 3,4, 0, 1, 2, 1, 0]
  # roundtrip_sequence = seq
  # roundtrip=1
  # for n in range(roundtrip-1):
    # seq.extend(roundtrip_sequence)
  # Stretcher.set_sequence(seq)
  Stretcher.propagate(1000)
  Stretcher.pos = (0,0,100)
  Stretcher.draw_elements()
  Stretcher.draw_mounts()
  Stretcher.draw_rays()

def simple_resonator_test():
  res = Resonator()
  m0 = Mirror()
  le = Lens(f=250)
  m1 = Mirror()
  res = Resonator()
  res.add_on_axis(m0)
  res.propagate(500)
  res.add_on_axis(le)
  res.propagate(270)
  res.add_on_axis(m1)
  res.draw()
  return res


def three_resonators_test():
  from basic_optics.resonator import Resonator

  res = Resonator(name="SimpleRes")
  g = 0.2
  L = 250
  R = L / (1-g)
  wavelength = 0.1
  res.wavelength = wavelength
  cm1 = Curved_Mirror(radius=R)
  cm2 = Curved_Mirror(radius=R)
  res.add_on_axis(cm1)
  res.propagate(L)
  res.add_on_axis(cm2)
  res.draw()


  alpha = -8
  beta = -0.1
  print("g1*g2 = ", alpha*beta)
  focal = 250
  dist1 = (1-alpha)*focal
  dist2 = (1-beta)*focal
  wavelength = 0.1
  res2 = Resonator(name="3ElmRes")
  res2.pos += (0,100, 0)
  mir1 = Mirror()
  mir2 = Mirror()
  le1 = Lens(f=focal)

  res2.add_on_axis(mir1)
  res2.propagate(dist1)
  res2.add_on_axis(le1)
  res2.propagate(dist2)
  res2.add_on_axis(mir2)

  q = res2.compute_eigenmode()

  print()
  print(res2.matrix())
  print()

  redu = (1-alpha*beta)*focal
  mat2 = np.array([[beta*alpha - redu/focal, 2*alpha*redu], [-2*beta/focal, beta*alpha - redu/focal]])
  print()
  print()
  print(mat2)
  print()

  res2.draw()



  res3 = Resonator(name="foldedRes")
  res3.pos += (0,-200, 0)

  alpha = -8
  beta = -0.1
  print("g1*g2 = ", alpha*beta)
  focal = 250
  dist1 = (1-alpha)*focal
  dist2 = (1-beta)*focal
  wavelength = 0.1
  frac1 = 0.4
  frac2 = 0.1
  frac3 = 1 - frac1 - frac2

  mir1 = Mirror(phi=180)
  mir2 = Mirror(phi=75)
  mir3 = Mirror(phi=-75)
  mir4 = Mirror(phi=180)
  cm = Curved_Mirror(radius=focal*2, phi = 170)

  res3.add_on_axis(mir1)
  res3.propagate(dist1*frac1)
  res3.add_on_axis(mir2)
  res3.propagate(dist1*frac2)
  res3.add_on_axis(mir3)
  res3.propagate(dist1*frac3)
  res3.add_on_axis(cm)
  res3.propagate(dist2)
  res3.add_on_axis(mir4)

  res3.compute_eigenmode()

  res3.draw()
  return res, res2, res3