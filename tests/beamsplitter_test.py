# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 10:08:41 2025

@author: mens
"""

from LaserCAD import ThinBeamsplitter, ThickBeamsplitter, TFP56, Rectangular_Beamsplitter, Rectangular_Thin_Beamsplitter
from LaserCAD import Beam, Composition, inch, Composed_Mount
from LaserCAD import freecad_da, clear_doc
from LaserCAD.moduls import Transmission_Disk
import numpy as np

if freecad_da:
  clear_doc()

# =============================================================================
# ThinBeamsplitter() test
# =============================================================================
"""
creates a 2 inch thin beam splitter, e.g. 2 dimenional (so no internal
refraction or lateral shift)
inserts in a Composition
creates the reflected beam in yellow by chaging the .transmission property
"""


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
# ThickBeamsplitter() test
# =============================================================================
"""
creates a 2 inch thick beam splitter, e.g. not 2 dimenional (so with internal
refraction and lateral shift)
inserts in a Composition
creates the reflected beam in yellow by chaging the .transmission property
"""

thbs = ThickBeamsplitter(angle_of_incidence=45, transmission=True, name="ThinBS")
thbs.aperture = 2*inch
thbs.thickness = 6 # 6mm thick
# thbs.set_mount(Composed_Mount(["KS2", "1inch_post"])) # proper Mount, or not

# Transmission ThickBeamsplitter
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
# Rectangular Beamsplitter
# =============================================================================
rect = Rectangular_Beamsplitter(name="NewRectBS", height=25, width=40, angle_of_incidence=45,
             thickness=5, refractive_index=1.45)

# Transmission ThickBeamsplitter
ls = Beam(radius=1.5) #LightSource = starting beam
comprect = Composition(name="ThinBSComp")
comprect.pos = (30, 270, 100)
comprect.set_light_source(ls)
comprect.propagate(80)
comprect.add_on_axis(rect)
comprect.propagate(80)
comprect.draw()

# Reflected Beam
rect.transmission = False
refl = rect.next_beam(ls)
rect.transmission = True
refl.draw_dict["color"] = (1.0, 0.8, 0.0) # cosmetic
refl.draw()


# =============================================================================
# Rectangular Thin Beamsplitter
# =============================================================================
thnect = Rectangular_Thin_Beamsplitter(name="NewRectBS", height=25, width=35, angle_of_incidence=45)

# Transmission ThickBeamsplitter
ls = Beam(radius=1.5) #LightSource = starting beam
compthnect = Composition(name="ThinBSComp")
compthnect.pos = (30, 400, 100)
compthnect.set_light_source(ls)
compthnect.propagate(80)
compthnect.add_on_axis(thnect)
compthnect.propagate(80)
compthnect.draw()

# Reflected Beam
thnect.transmission = False
refl = thnect.next_beam(ls)
thnect.transmission = True
refl.draw_dict["color"] = (1.0, 0.8, 0.0) # cosmetic
refl.draw()

# =============================================================================
# TFP56 tests (mostly mount alignement)
# =============================================================================
"""
OK, the only thing special about the TFP56 is its mount (Thorlabs) and the ways
to arange it.
By all other meanings it is a Thick BS.
There are 3 different True Falls properties, resulting in 8 different ways to
place TFP and Mount.
The default is
tb56.angle_positiv = True
tb56.flip_mount = False
tb56.revers_mount = False

all 8 variants are drawn and labeled
"""
def arguemntlist_to_srting(angpos=True, flipmount=True, revermount=True):
  st = "AOI"
  if angpos:
    st += "+"
  else:
    st += "-"
  if flipmount:
    st += "_Flip"
  else:
    st += "_NoFlip"
  if revermount:
    st += "_Revers"
  else:
    st += "_NoReverse"
  return st


tfplist = []

truefalse = [True, False]
pos = np.array((210,-200,0))
for angpos in truefalse:
  for flipmount in truefalse:
    for revermount in truefalse:
      tb56 = TFP56()
      tb56.angle_positiv = angpos
      tb56.flip_mount = flipmount
      tb56.revers_mount = revermount
      tb56.update_phi()
      tb56.update_mount()

      comp56 = Composition(name="tb56"+arguemntlist_to_srting(angpos, flipmount, revermount))
      pos += (0, 150, 0)
      comp56.pos += pos
      comp56.propagate(70)
      comp56.add_on_axis(tb56)
      comp56.propagate(70)

      b0 = comp56._lightsource
      tb56.transmission = False
      br = tb56.next_beam(b0)
      tb56.transmission = True
      br.draw_dict["color"] = (1.0, 1.0, 0.1)
      br.set_length(60)

      comp56.draw()
      br.draw()

      tfplist.append(tb56)



# =============================================================================
# Transmission Disk
# =============================================================================
"""
If you really want to see the inner ray of a thick TFP (because you are into it
or maybe because you want to calculate the exact length of an optical axis
including the inner beam (in fact you would have to divide by n, yeah, anyway))
so if that is true, you can use the subcomposition Transmission Disk.
"""

trdisk = Transmission_Disk(name="TMD", refractive_index=1.45,
                           AOI=-56, thickness=6, aperture=2*inch)

trdiskbeam = Beam(radius=2)

trdiskcomp = Composition(name="ThickCompositionTFP")
trdiskcomp.set_light_source(trdiskbeam)
trdiskcomp.pos = (300, 200, 100)
trdiskcomp.propagate(85)
trdiskcomp.add_supcomposition_on_axis(trdisk)
trdiskcomp.propagate(85)
trdiskcomp.draw()

reflec = trdisk.reflected_beam(trdiskbeam)
reflec.draw_dict["color"] = (0.6, 0.8, 0.2)
reflec.draw()