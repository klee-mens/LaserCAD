# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 10:08:41 2025

@author: mens
"""

from LaserCAD.basic_optics.beam_splitter import ThinBeamsplitter, ThickBeamplitter, TFP56
from LaserCAD.basic_optics import Beam, Composition, inch, Composed_Mount
from LaserCAD.freecad_models import freecad_da, clear_doc
import numpy as np

if freecad_da:
  clear_doc()

# =============================================================================
# ThinBeamsplitter() test
# =============================================================================

tnbs = ThinBeamsplitter(angle_of_incidence=45, transmission=True, name="ThinBS")
tnbs.aperture = 2*inch
tnbs.set_mount(Composed_Mount(["KS2", "1inch_post"])) # proper Mount

# Transmission ThinBeamsplitter
ls = Beam(radius=1.5) #LightSource = starting beam
comptnbs = Composition(name="ThinBSComp")
comptnbs.pos = (0, 0, 100)
comptnbs.set_light_source(ls)
comptnbs.propagate(80)
comptnbs.add_on_axis(tnbs)
comptnbs.propagate(80)
comptnbs.draw()

# Reflected Beam
tnbs.transmission = False
refl = tnbs.next_beam(ls)
tnbs.transmission = True
refl.draw_dict["color"] = (1.0, 0.8, 0.0) # cosmetic
refl.draw()


# =============================================================================
# ThickBeamplitter() test
# =============================================================================

thbs = ThickBeamplitter(angle_of_incidence=45, transmission=True, name="ThinBS")
thbs.aperture = 2*inch
thbs.thickness = 6 # 6mm thick
# thbs.set_mount(Composed_Mount(["KS2", "1inch_post"])) # proper Mount, or not

# Transmission ThinBeamsplitter
ls = Beam(radius=1.5) #LightSource = starting beam
compthbs = Composition(name="ThinBSComp")
compthbs.pos = (30, 95, 100)
compthbs.set_light_source(ls)
compthbs.propagate(80)
compthbs.add_on_axis(thbs)
compthbs.propagate(80)
compthbs.draw()

# Reflected Beam
thbs.transmission = False
refl = thbs.next_beam(ls)
thbs.transmission = True
refl.draw_dict["color"] = (1.0, 0.8, 0.0) # cosmetic
refl.draw()



# =============================================================================
# TFP56 tests (mostly mount alignement)
# =============================================================================
tfplist = []

trfal = [True, False]
pos = np.array((190,-120,0))
for angpos in trfal:
  for flipmount in trfal:
    for revermount in trfal:
      tb56 = TFP56()
      tb56.angle_positiv = angpos
      tb56.flip_mount = flipmount
      tb56.revers_mount = revermount
      tb56.update_phi()
      tb56.update_mount()

      comp56 = Composition(name="tb65_in_action")
      pos += (0, 80, 0)
      comp56.pos += pos
      comp56.propagate(70)
      comp56.add_on_axis(tb56)
      comp56.propagate(70)

      r0 = comp56._beams[0].inner_ray()
      rr = tb56.reflection(r0)
      rr.length = 60

      comp56.draw()
      rr.draw()

      tfplist.append(tb56)

