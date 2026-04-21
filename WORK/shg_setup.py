#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 09:33:38 2025

@author: mens
"""

from LaserCAD import Beam, Mirror, Composition, TFP56, Lens, NLO_Crystal, Lambda_Plate, Composed_Mount, ThickBeamsplitter, Detector
from LaserCAD import freecad_da, clear_doc
from LaserCAD import CircularRayBeam
from LaserCAD.basic_optics.lens import Cylindrical_Lens
from LaserCAD.non_interactings import Crystal
import numpy as np

if freecad_da:
  clear_doc()
  
# start_beam = Beam(radius=3.22, angle=0) # startdiameter 4 mm, correct values if needed
start_beam = CircularRayBeam(radius=3.22, angle=0) # startdiameter 4 mm, correct values if needed

#new Mirror class with other mounts, thats all
class U100_A_Mirror(Mirror):
  def __init__(self, phi=180, theta=0, **kwargs):
    super().__init__(phi=phi, theta=theta, **kwargs)
    self.set_mount(Composed_Mount(["U100-A2K", "1inch_post"]))



setup = Composition(name="SHG_Beamline")
setup.set_light_source(start_beam)
setup.pos = (0, 0, 80) # 80 mm beam height (need to be measured)
setup.propagate(300)
setup.add_on_axis(U100_A_Mirror(phi=90))
setup.propagate(70)
setup.add_on_axis(U100_A_Mirror(phi=90))

# mode adaption telescope, correct values if needed
f1 = 300
f2 = -75
setup.propagate(46)

setup.add_on_axis(Lens(f=f1))
setup.propagate(f1+f2)
setup.add_on_axis(Lens(f=f2))
setup.propagate(25)

# TFP56 stage, for more examples see beamsplitter_test.py
tfp = TFP56(name="TFP56", thickness=5, transmission=True, refractive_index=1.45)
tfp.angle_positiv = False
tfp.flip_mount = True
tfp.revers_mount = False
tfp.update_phi()
tfp.update_mount()

setup.add_on_axis(U100_A_Mirror(phi=-90))
setup.propagate(60)
setup.add_on_axis(Lambda_Plate())
setup.propagate(90)
setup.add_on_axis(tfp)
setup.propagate(100)

# shg stage
setup.add_on_axis(NLO_Crystal(name="BBO", wavelength_multiplier=0.5, output_color=(0.1, 0.7, 0.3)))
setup.propagate(65)


beamsplitter = ThickBeamsplitter(angle_of_incidence=-50, thickness=6, refractive_index=1.45, transmission=True)
beamsplitter.set_mount(Composed_Mount(["U100-A2K", "1inch_post"]))  # holder generic + post
beamsplitter.aperture = 50.8
setup.add_on_axis(beamsplitter)
setup.propagate(110)
setup.add_on_axis(Lambda_Plate())
setup.propagate(148)
setup.add_on_axis(U100_A_Mirror(phi=-90))
setup.propagate(45)
setup.add_on_axis(U100_A_Mirror(phi=-90))
setup.propagate(135)

#Telescope fundamental arm
f11 = -25
f12 = 300
setup.add_on_axis(Lens(f=f11))
setup.propagate(f11+f12)
setup.add_on_axis(Lens(f=f12))
setup.propagate(80)
setup.add_on_axis(U100_A_Mirror(phi=154.4))
setup.propagate(100)
cyl_fund = Cylindrical_Lens(f=75, height=50.8)
cyl_fund.aperture = 53
setup.add_on_axis(cyl_fund)
cyl_fund.rotate(cyl_fund.normal, phi=np.pi/2)
setup.propagate(100)


"""#Telescope SHG arm
f21 = -25
f22 = 450
setup1 = Composition(name="SHG_Beamline2")
b1=Beam(radius=0.4355)
setup1.set_light_source(b1)
setup1.pos += (3.34,385.85,81.17)
b1.draw_dict["color"] = (0.1, 0.7, 0.3)
setup1.propagate(80)
setup1.add_on_axis(Lens(f=f21))
setup1.propagate(225)
setup1.add_on_axis(U100_A_Mirror(phi=-90))
setup1.propagate(200)
setup1.add_on_axis(Lens(f=f22))
setup1.propagate(50)
setup1.add_on_axis(U100_A_Mirror(phi=-138.7))
setup1.propagate(300)
#b1.set_length(100)"""

#Telescope SHG arm
f21 = -25
f22 = 450
setup1 = Composition(name="SHG_Beamline2")
# b1=Beam(radius=0.4355)
b1=CircularRayBeam(radius=0.4355)
setup1.set_light_source(b1)
setup1.pos = (3.34,385.85,81.17)
b1.draw_dict["color"] = (0.1, 0.7, 0.3)
setup1.propagate(80)
setup1.add_on_axis(Lens(f=f21))
setup1.propagate(100)
setup1.add_on_axis(U100_A_Mirror(phi=110))
setup1.propagate(50)
setup1.add_on_axis(U100_A_Mirror(phi=-110))
setup1.propagate(100)
setup1.add_on_axis(U100_A_Mirror(phi=-90))
setup1.propagate(175)
setup1.add_on_axis(Lens(f=f22))
setup1.propagate(100)
setup1.add_on_axis(U100_A_Mirror(phi=-138.7))
setup1.propagate(100)
cyl_shg = Cylindrical_Lens(f=100, height=30)
cyl_shg.aperture = 32
setup1.add_on_axis(cyl_shg)
cyl_shg.rotate(cyl_shg.normal, phi=np.pi/2)
setup1.propagate(200)


big_bbo = Crystal(width=25, height=5, thickness=2)
big_bbo.pos = (120, 323, 81)
big_bbo.normal = (0,1,0)
   
# =============================================================================
# draw selection
# =============================================================================
setup.draw()
setup1.draw()
big_bbo.draw()