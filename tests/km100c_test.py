# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 23:15:51 2026

@author: mens
"""

from LaserCAD.basic_optics import SquareBeam
from LaserCAD.basic_optics.lens import Cylindrical_Lens
from LaserCAD.basic_optics import Intersection_plane, Composition
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
# import numpy as np

if freecad_da:
  clear_doc()



ls = SquareBeam(radius =5,ray_in_line = 10)
comp = Composition(name="horizontal")
comp.set_light_source(ls)

comp.propagate(100)

cyl = Cylindrical_Lens(f=100, height=50, thickness=5, aperture=40, horizontal=True)
comp.add_on_axis(cyl)

comp.propagate(105)

IP = Intersection_plane()
comp.add_on_axis(IP)

comp.draw()

# IP.spot_diagram(comp._beams[2])



ls2 = SquareBeam(radius =5,ray_in_line = 10)
ls2.set_ray_color((0.5, 0.0, 0.8))
comp2 = Composition(name="vertical")
comp2.set_light_source(ls2)

comp2.propagate(100)
cyl2 = Cylindrical_Lens(f=180)

comp2.add_on_axis(cyl2)
comp2.propagate(200)

comp2.pos += (0,80,0)
comp2.draw()



ls_rev = SquareBeam(radius =5,ray_in_line = 10)
ls_rev.set_ray_color((0.5, 0.0, 0.8))
comp_rev = Composition(name="vertical_reversed")
comp_rev.set_light_source(ls_rev)

comp_rev.propagate(100)
cyl_rev = Cylindrical_Lens(f=180)

comp_rev.add_on_axis(cyl_rev)
cyl_rev.Mount.reverse(thickness=7)
comp_rev.propagate(200)

comp_rev.pos += (0,-110,0)
comp_rev.draw()


from LaserCAD import KM100C_flipped


ls3 = SquareBeam(radius =5,ray_in_line = 10)
ls3.set_ray_color((0.5, 0.0, 0.8))
comp3 = Composition(name="flipped")
comp3.set_light_source(ls3)

comp3.propagate(100)
cyl3 = Cylindrical_Lens(f=180, height=40, aperture=70)
cyl3.set_mount(KM100C_flipped(height=cyl3.height, width=cyl3.aperture))

comp3.add_on_axis(cyl3)
comp3.propagate(200)

comp3.pos += (0,160,0)
comp3.draw()

ls3_rev = SquareBeam(radius =5,ray_in_line = 10)
ls3_rev.set_ray_color((0.5, 0.0, 0.8))
comp3_rev = Composition(name="flipped_reversed")
comp3_rev.set_light_source(ls3_rev)

comp3_rev.propagate(100)
cyl3_rev = Cylindrical_Lens(f=180, height=40, aperture=70)
cyl3_rev.set_mount(KM100C_flipped(height=cyl3_rev.height, width=cyl3_rev.aperture))

comp3_rev.add_on_axis(cyl3_rev)
cyl3_rev.Mount.reverse(thickness=7)
comp3_rev.propagate(200)

comp3_rev.pos += (0,160+110,0)
comp3_rev.draw()


# =============================================================================
# left handed
# =============================================================================

from LaserCAD.basic_optics.mount import KM100CL, KM100CL_flipped



cyl5 = Cylindrical_Lens()
cyl5.set_mount(KM100CL(height=cyl5.height, width=cyl5.aperture))

ls5 = SquareBeam(radius =5,ray_in_line = 10)
ls5.set_ray_color((0.5, 0.0, 0.8))
comp5 = Composition("left")
comp5.set_light_source(ls5)

comp5.propagate(100)
comp5.add_on_axis(cyl5)
comp5.propagate(200)

comp5.pos += (0,-300,0)
comp5.draw()



cyl6 = Cylindrical_Lens(aperture=80)
cyl6.set_mount(KM100CL(height=cyl6.height, width=cyl6.aperture))
cyl6.Mount.reverse()

ls6 = SquareBeam(radius =5,ray_in_line = 10)
# ls6.set_ray_color((0.5, 0.0, 0.8))
comp6 = Composition("left")
comp6.set_light_source(ls6)

comp6.propagate(100)
comp6.add_on_axis(cyl6)
comp6.propagate(200)

comp6.pos += (0,-400,0)
comp6.draw()


cyl7 = Cylindrical_Lens(aperture=80)
cyl7.set_mount(KM100CL_flipped(height=cyl7.height, width=cyl7.aperture))
# cyl7.Mount.reverse()

ls7 = SquareBeam(radius =5,ray_in_line = 10)
# ls7.set_ray_color((0.5, 0.0, 0.8))
comp7 = Composition("left")
comp7.set_light_source(ls7)

comp7.propagate(100)
comp7.add_on_axis(cyl7)
comp7.propagate(200)

comp7.pos += (100,-400,0)
comp7.draw()


cyl8 = Cylindrical_Lens(aperture=80)
cyl8.set_mount(KM100CL_flipped(height=cyl8.height, width=cyl8.aperture))
cyl8.Mount.reverse()

ls8 = SquareBeam(radius =5,ray_in_line = 10)
# ls8.set_ray_color((0.5, 0.0, 0.8))
comp8 = Composition("left")
comp8.set_light_source(ls8)

comp8.propagate(100)
comp8.add_on_axis(cyl8)
comp8.propagate(200)

comp8.pos += (200,-400,0)
comp8.draw()
