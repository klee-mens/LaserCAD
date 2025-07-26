#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 11:55:56 2025

@author: clemens
"""

from LaserCAD.basic_optics import Mirror, Curved_Mirror, Lens, Beam
from LaserCAD.basic_optics import Composition, Composed_Mount
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
import numpy as np

if freecad_da:
  clear_doc()

firsttry = Composition(name="BeamLine1")
firsttry.set_light_source(Beam(radius=2, angle=0.02))
firsttry.propagate(500)
firsttry.add_on_axis(Lens(f=150))
firsttry.propagate(400)
firsttry.add_on_axis(Lens(f=120))
firsttry.propagate(110)
firsttry.add_on_axis(Mirror(phi=110))
firsttry.propagate(90)
firsttry.add_on_axis(Mirror(phi=70))
firsttry.propagate(150)
firsttry.add_on_axis(Lens(f=200))
firsttry.propagate(400)
firsttry.add_on_axis(Mirror(phi=-90))
firsttry.propagate(60)

# firsttry.pos += (0,0,10)
firsttry.draw_elements()
firsttry.draw_mounts()

start_beam = Beam()
start_beam.set_geom(firsttry.get_geom())
start_beam.rotate(vec=(0,0,1), phi=3*np.pi/180)
beams = firsttry.compute_beams(external_source=start_beam)
for b in beams:
  b.draw()

for oa in firsttry._optical_axis:
  oa.draw()

# mirteles = Composition(name="MirrorTelescope")
# mirteles.pos += (0,200,0)

# lightsource = Beam(radius=2)
# lightsource.draw_dict["color"] = (1.0, 1.0, 0.0)

# mirteles.set_light_source(lightsource)
# mirteles.propagate(350)
# mirteles.add_on_axis(Curved_Mirror(radius=250, phi=180-15))
# mirteles.propagate(250)

# next_mirror = Curved_Mirror(radius=250, phi=0, theta=180-15)
# next_mirror.set_mount(Composed_Mount(unit_model_list=["KS1", "0.5inch_post"]))
# mirteles.add_on_axis(next_mirror)

# mirteles.propagate(350)

# mirteles.draw()



if freecad_da:
  setview()