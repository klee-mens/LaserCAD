# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 19:46:37 2023

@author: mens
"""

from .lens import Lens
from .mirror import Mirror, Curved_Mirror
from .beam import Beam
from .moduls import Make_Telescope
# from .propagation import Propagation
from .ray import Ray
from .composition import Composition
from .grating import Grating
import numpy as np



def Telescope_4beam():
  teles = Make_Telescope(name="teles", lens1_aperture=50, lens2_aperture=50)
  teles.draw()
  dist = 8
  b0 = Beam(name="b1", angle=0)
  b0.pos += (0, dist, dist)
  bs = [b0]
  for elm in teles._elements:
    if not type(elm) == type(Propagation()):
      beam = bs[-1]
      bs.append(elm.next_beam(beam))
      beam.draw()
    
  be = bs[-1]
  be.draw()
  return (bs, teles)


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

def Parallel_ray_bundle_tilted_mirror_ray_trace(focal_length = 200):
  """
  schießt eine Matrix aus line_count x line_count parallelen rays auf einen
  sphärischen Spiegel unter einem bestimmten Winkel und berechnet die neuen
  Strahlen mittels analytischem Raytracing
  ...Sollten alle in einem Punkt fokussiert werden, +- Astigmatismus 

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
  bundel.override_rays(rays)
  
  comp = Composition(name="Parallel_ray_bundle_tilted_lens_test")
  comp.set_light_source(bundel)
  comp.pos = 2*bundel.pos #geht bsetimmt auch schöner
  p1 = Propagation(d=100)
  # le = Lens(f=focal_length)
  le = Curved_Mirror(radius=2*focal_length)
  p2 = Propagation(d=200)
  comp.add(p1)
  comp.add(le)
  comp.add(p2)
  le.normal = (1,0.1,0.1)
  
  comp.draw()
  comp.draw_rays()

  return comp  

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
  stretch.draw_elements()
  stretch.draw_rays()
  
  wcell = Make_White_Cell(roundtrips4=2)
  wcell.pos = (0, 2000, 100)
  wcell.draw()
  
  return peris, teles, amp, stretch, wcell