# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:01:12 2024

@author: 12816
"""
from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating
# from LaserCAD.basic_optics.mirror import 
from LaserCAD.basic_optics import Unit_Mount,Composed_Mount
from LaserCAD.non_interactings import Lambda_Plate
from LaserCAD.basic_optics.mount import Stages_Mount
from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics.mount import Stripe_Mirror_Mount
import numpy as np

# B=Beam(radius =5)
# B.make_square_distribution (10)
# C = Composition()
# C.set_light_source(B)
# C.propagate(100)
# a= Cylindrical_Mirror(radius=100)
# a.rotate(a.normal, np.pi/2)
# a.Mount = Stripe_Mirror_Mount(mirror_thickness=a.thickness)
# a.aperture = 75
# a.pos += (100,0,0)
# a.phi = -90
# C.add_on_axis(a)
# # C.recompute_optical_axis()
# C.propagate(70.6)
# IP = Intersection_plane()
# C.add_on_axis(IP)
# C.draw()
# IP.draw()
# IP.spot_diagram(C._beams[-1])

# ray = Ray()
# ray.draw()
# B = Beam(radius=5)
# B.pos += (0,100,0)
# B.draw()
# M = Mirror()
# M.pos += (0,200,0)
# M.draw()
# M.draw_mount()
# G = Grating()
# G.pos += (0,300,0)
# G.draw()
# G.draw_mount()

# from .. basic_optics import Composition, inch, Curved_Mirror, Unit_Mount
# import numpy as np


name="WhiteCell"
Radius=300
roundtrips4=2 
seperation=15
"""
Generates a White Cell Mirror Triplett for a compact multipass system with
optical unity matrix (or something similar)
See Multipass cells on wikipedia or so
Parameters
----------
name : str, optional
  DESCRIPTION. The default is "WhiteCell".
Radius : float, optional
  Radius of all convex spheres and distances. The default is 300.
roundtrips4 : integer, optional
  gives the number of roundtrips the beam apsses the cell.
  For each the beam will propagate 4x the Radius.
  The default is 2.
seperation : TYPE, optional
  The seperation of the beam hits on the big sphere. Might be smaller.
  The default is 15.

Returns
-------
white_cell : Composition
  DESCRIPTION.

"""
mirror_sep_angle = 12 #degree, could be smaller
deflection = 2 * np.arcsin(seperation/2 / Radius) * 180/np.pi

helper = Composition(name=name)
helper.propagate(Radius)
scm1 = Curved_Mirror(radius=Radius, phi=180-deflection)
helper.add_on_axis(scm1)
helper.propagate(Radius)

bigcm = Curved_Mirror(radius=Radius, phi=180+mirror_sep_angle)
bigcm.aperture = 12 + (roundtrips4-1)*2*seperation
bigcm.Mount = Unit_Mount()
helper.add_on_axis(bigcm)
helper.propagate(Radius)

scm2 = Curved_Mirror(radius=Radius, phi=180-deflection)
helper.add_on_axis(scm2)
helper.propagate(Radius)

white_cell = Composition()
white_cell.pos = helper.pos - (0, seperation*(roundtrips4-1), 0)
white_cell.normal = scm1.pos - white_cell.pos
white_cell.add_supcomposition_fixed(helper)

seq = [0, 1, 2]
roundtrip_sequence = [1, 0, 1, 2]
for n in range(roundtrips4-1):
  seq.extend(roundtrip_sequence)
white_cell.set_sequence(seq)

white_cell.propagate(Radius*1.2)


helper.draw_elements()





if freecad_da:
  clear_doc()
# Grating and Mirror test
# ray = Ray()
# ray.draw()
# B = Beam(radius=5)
# B.pos += (0,100,0)
# B.draw()
# M = Mirror()
# M.pos += (0,200,0)
# M.draw()
# M.draw_mount()
# G = Grating()
# G.pos += (0,300,0)
# G.draw()
# G.draw_mount()

M1 = Mirror()
M1.pos = (0,0,100)
M1.normal = (1,1,0)

# M1.Mount = Stages_Mount(aperture=M1.aperture,elm_type = "Mirror",elm_thickness=M1.thickness)
# M1.Mount.set_geom(M1.get_geom())

Mount1 = M1.Mount
M1.Mount = Stages_Mount(basic_mount=Mount1,x_aligned=True)
M1.Mount.set_geom(M1.get_geom())
M1.Mount.find_screw_hole()
M1.draw()
M1.draw_mount()
print(M1.Mount.mount_list[1]._lower_limit)