#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:41:34 2026

@author: clemens
"""

from LaserCAD.basic_optics import SquareBeam
from LaserCAD.basic_optics.lens import Cylindrical_Lens
from LaserCAD.basic_optics import Intersection_plane, Composition
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
# import numpy as np

if freecad_da:
  clear_doc()

shift = 100
normal = (1,1,0)
xshift = 200
first = 50
last = 50

from LaserCAD.basic_optics.mount import KM100C, KM100C_flipped, KM100CL, KM100CL_flipped


lsE1 = SquareBeam(radius =5,ray_in_line = 10)
compE1 = Composition(name="KM100C")
compE1.set_light_source(lsE1)

compE1.propagate(first)
cylE1 = Cylindrical_Lens(f=180, height=40, aperture=70)
cylE1.set_mount(KM100C(height=cylE1.height, width=cylE1.aperture))

compE1.add_on_axis(cylE1)
compE1.propagate(last)

compE1.pos += (0, 1*shift, 0)
compE1.normal = normal
compE1.draw()


lsE2 = SquareBeam(radius =5,ray_in_line = 10)
compE2 = Composition(name="KM100C_rev")
compE2.set_light_source(lsE2)

compE2.propagate(first)
cylE2 = Cylindrical_Lens(f=180, height=100, aperture=70)
cylE2.set_mount(KM100C(height=cylE2.height, width=cylE2.aperture))
cylE2.Mount.reverse()

compE2.add_on_axis(cylE2)
compE2.propagate(last)

compE2.pos += (0, 2*shift, 0)
compE2.normal = normal
compE2.draw()


lsE3 = SquareBeam(radius =5,ray_in_line = 10)
compE3 = Composition(name="KM100C_flipp")
compE3.set_light_source(lsE3)

compE3.propagate(first)
cylE3 = Cylindrical_Lens(f=180, height=40, aperture=40)
cylE3.set_mount(KM100C_flipped(height=cylE3.height, width=cylE3.aperture))

compE3.add_on_axis(cylE3)
compE3.propagate(last)

compE3.pos += (0, 3*shift, 0)
compE3.normal = normal
compE3.draw()


lsE4 = SquareBeam(radius =5,ray_in_line = 10)
compE4 = Composition(name="KM100C_flipp_rev")
compE4.set_light_source(lsE4)

compE4.propagate(first)
cylE4 = Cylindrical_Lens(f=180, height=40, aperture=70)
cylE4.set_mount(KM100C_flipped(height=cylE4.height, width=cylE4.aperture))
cylE4.Mount.reverse()

compE4.add_on_axis(cylE4)
compE4.propagate(last)

compE4.pos += (0, 4*shift, 0)
compE4.normal = normal
compE4.draw()




lsE5 = SquareBeam(radius =5,ray_in_line = 10)
compE5 = Composition(name="KM100CL")
compE5.set_light_source(lsE5)

compE5.propagate(first)
cylE5 = Cylindrical_Lens(f=180, height=40, aperture=70)
cylE5.set_mount(KM100CL(height=cylE5.height, width=cylE5.aperture))

compE5.add_on_axis(cylE5)
compE5.propagate(last)

compE5.pos += (xshift, 1*shift, 0)
compE5.normal = normal
compE5.draw()


lsE6 = SquareBeam(radius =5,ray_in_line = 10)
compE6 = Composition(name="KM100CL_rev")
compE6.set_light_source(lsE6)

compE6.propagate(first)
cylE6 = Cylindrical_Lens(f=180, height=40, aperture=70)
cylE6.set_mount(KM100CL(height=cylE6.height, width=cylE6.aperture))
cylE6.Mount.reverse()

compE6.add_on_axis(cylE6)
compE6.propagate(last)

compE6.pos += (xshift, 2*shift, 0)
compE6.normal = normal
compE6.draw()


lsE7 = SquareBeam(radius =5,ray_in_line = 10)
compE7 = Composition(name="KM100CL_flipped")
compE7.set_light_source(lsE7)

compE7.propagate(first)
cylE7 = Cylindrical_Lens(f=180, height=40, aperture=70)
cylE7.set_mount(KM100CL_flipped(height=cylE7.height, width=cylE7.aperture))

compE7.add_on_axis(cylE7)
compE7.propagate(last)

compE7.pos += (xshift, 3*shift, 0)
compE7.normal = normal
compE7.draw()


lsE8 = SquareBeam(radius =5,ray_in_line = 10)
compE8 = Composition(name="KM100CL_flipped_rev")
compE8.set_light_source(lsE8)

compE8.propagate(first)
cylE8 = Cylindrical_Lens(f=180, height=40, aperture=70)
cylE8.set_mount(KM100CL_flipped(height=cylE8.height, width=cylE8.aperture))
cylE8.Mount.reverse()

compE8.add_on_axis(cylE8)
compE8.propagate(last)

compE8.pos += (xshift, 4*shift, 0)
compE8.normal = normal
compE8.draw()










ls = SquareBeam(radius =5,ray_in_line = 10)
comp = Composition(name="horizontal")
comp.set_light_source(ls)

comp.propagate(first)

cyl = Cylindrical_Lens(f=100, height=50, thickness=5, aperture=40, horizontal=True)
comp.add_on_axis(cyl)

comp.propagate(105)

IP = Intersection_plane()
comp.add_on_axis(IP)

comp.pos += (0, 600, 0)
comp.draw()
IP.spot_diagram(comp._beams[2])


ls2 = SquareBeam(radius =5,ray_in_line = 10)
ls2.set_ray_color((0.5, 0.0, 0.8))
comp2 = Composition(name="vertical")
comp2.set_light_source(ls2)

comp2.propagate(first)
cyl2 = Cylindrical_Lens(f=180)

comp2.add_on_axis(cyl2)
comp2.propagate(last)

comp2.pos += (0, 680, 0)
comp2.draw()



# # ls_rev = SquareBeam(radius =5,ray_in_line = 10)
# # ls_rev.set_ray_color((0.5, 0.0, 0.8))
# # comp_rev = Composition(name="vertical_reversed")
# # comp_rev.set_light_source(ls_rev)

# # comp_rev.propagate(100)
# # cyl_rev = Cylindrical_Lens(f=180)

# # comp_rev.add_on_axis(cyl_rev)
# # cyl_rev.Mount.reverse(thickness=7)
# # comp_rev.propagate(last)

# # comp_rev.pos += (0,-110,0)
# # comp_rev.draw()


# # from LaserCAD import KM100C_flipped


# ls3 = SquareBeam(radius =5,ray_in_line = 10)
# comp3 = Composition(name="flipped")
# comp3.set_light_source(ls3)

# comp3.propagate(100)
# cyl3 = Cylindrical_Lens(f=180, height=40, aperture=70)
# cyl3.set_mount(KM100C(height=cyl3.height, width=cyl3.aperture, left_hand=False, flipp=False, reverse=False))

# comp3.add_on_axis(cyl3)
# comp3.propagate(200)

# comp3.pos += (0, 100 ,0)
# comp3.draw()

# # ls3_rev = SquareBeam(radius =5,ray_in_line = 10)
# # ls3_rev.set_ray_color((0.5, 0.0, 0.8))
# # comp3_rev = Composition(name="flipped_reversed")
# # comp3_rev.set_light_source(ls3_rev)

# # comp3_rev.propagate(100)
# # cyl3_rev = Cylindrical_Lens(f=180, height=40, aperture=70)
# # cyl3_rev.set_mount(KM100C_flipped(height=cyl3_rev.height, width=cyl3_rev.aperture))

# # comp3_rev.add_on_axis(cyl3_rev)
# # cyl3_rev.Mount.reverse(thickness=7)
# # comp3_rev.propagate(200)

# # comp3_rev.pos += (0,160+110,0)
# # comp3_rev.draw()


# # =============================================================================
# # left handed
# # =============================================================================
# from LaserCAD.basic_optics.mount import KM100CL



# cyl5 = Cylindrical_Lens()
# cyl5.set_mount(KM100CL(height=cyl5.height, width=cyl5.aperture))

# ls5 = SquareBeam(radius =5,ray_in_line = 10)
# ls5.set_ray_color((0.5, 0.0, 0.8))
# comp5 = Composition("left")
# comp5.set_light_source(ls5)

# comp5.propagate(100)
# comp5.add_on_axis(cyl5)
# comp5.propagate(200)

# comp5.pos += (0,-300,0)
# comp5.draw()

if freecad_da:
  setview()