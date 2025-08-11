#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:01:45 2024

@author: mens
"""

from LaserCAD.basic_optics import Mirror, Composition, Composed_Mount, inch
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
from LaserCAD.basic_optics import ThickBeamsplitter, ThinBeamsplitter, TFP56
from LaserCAD.basic_optics.mount import Adaptive_Angular_Mount, Composed_Mount, Unit_Mount, Post

import numpy as np

if freecad_da:
  clear_doc()

# =============================================================================
# simple mirror
# =============================================================================
m = Mirror(phi=120)
comp = Composition(name="FlipMirror")
comp.propagate(70)
comp.add_on_axis(m)
comp.propagate(50)

from LaserCAD.freecad_models.utils import thisfolder

# =============================================================================
# Beam Splitter jetzt erst recht
# =============================================================================


from LaserCAD.basic_optics.refractive_plane import Refractive_plane

# class ThickBeamplitter(Mirror):
#   def __init__(self, phi=90, thickness=4, transmission=True,
#                refractive_index=1.45, name="ThickSplitter", **kwargs):
#     super().__init__(phi=phi, transmission=transmission, name=name, **kwargs)
#     self.thickness = thickness
#     self.refractive_index = refractive_index
#     self.transmission = transmission

#   def next_ray(self, ray):
#     if self.transmission:
#       surface = Refractive_plane(relative_refractive_index=self.refractive_index)
#       surface.set_geom(self.get_geom())
#       backside = Refractive_plane(relative_refractive_index=1/self.refractive_index)
#       backside.set_axes(self.get_axes())
#       backside.pos = self.pos + self.thickness*self.normal
#       if np.dot(self.normal, ray.normal) > 0:
#         first_ray = surface.next_ray(ray)
#         second_ray = backside.next_ray(first_ray)
#       else:
#         first_ray = backside.next_ray(ray)
#         second_ray = surface.next_ray(first_ray)
#       return second_ray
#     return self.reflection(ray)





tfplist = []

trfal = [True, False]
pos = np.array((0,0,0))
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

      # comp56.draw()
      # rr.draw()

      tfplist.append(tb56)

c = Composition()
c.propagate(70)
c.add_on_axis(TFP56())
c.propagate(70)
c.draw()

# =============================================================================
# thick beam splitter
# =============================================================================
tbs = ThickBeamsplitter()
# tbs.aperture = 1*inch
# tbs.thickness = 5
tbsmount = Composed_Mount()
aam = Adaptive_Angular_Mount(angle=45)
aam.is_horizontal = False
tbsmount.add(aam)
aam.rotate(aam.normal, phi=-np.pi/2)
aam.rotate(vec=(0,0,1), phi=45*np.pi/180)
tbsmount.add(Unit_Mount(model="KS1"))
tbsmount.add(Post(model="0.5inch_post"))
tbs.set_mount(tbsmount)

splittercomp = Composition(name="ThickBeamSplitter")
splittercomp.pos += (0, 100, 0)
splittercomp.propagate(120)
splittercomp.add_on_axis(tbs)
splittercomp.propagate(120)




# =============================================================================
# transmission disk
# =============================================================================
from LaserCAD.moduls.transmission_disk import Transmission_Disk

tmd = Transmission_Disk(name="NewExtended_TFP", refractive_index=1.45, AOI=-45,
             thickness=6, aperture = 2*inch, mount_reversed=False, mount_flipped=False)

disccomp = Composition(name="TransmissionDiskComp")
disccomp.pos += (0, 200, 0)
disccomp.propagate(120)
disccomp.add_supcomposition_on_axis(tmd)
disccomp.propagate(120)


# =============================================================================
# draw selection
# =============================================================================
# comp.draw()

# splittercomp.draw()

# disccomp.draw()

# =============================================================================
# michelson interferometer
# =============================================================================

# BStrans = Beamsplitter(name="50-50BS")
# BStrans.aperture = 3*inch
# BStrans.set_mount(Composed_Mount(unit_model_list=["KS3", "0.5inch_post"]))

# BSreflec = Beamsplitter(transmission=False)
# BSreflec.invisible = True
# BSreflec.Mount.invisible = True

# mysterious_back_mirror = Mirror()
# mysterious_back_mirror.invisible = True
# mysterious_back_mirror.Mount.invisible = True

# inputarm = 150
# arm1 = 120
# arm2 = 130
# outputarm = 170

# michel = Composition(name="Interferometer")
# michel.pos += (0,200,20)
# michel.propagate(inputarm)
# michel.add_on_axis(BStrans)
# michel.propagate(arm1)
# michel.add_on_axis(Mirror())
# michel.propagate(arm1)

# BSreflec.set_geom(BStrans.get_geom())

# michel.add_on_axis(BSreflec)
# michel.propagate(outputarm)

# michel.add_on_axis(mysterious_back_mirror)
# michel.propagate(outputarm + arm2)
# michel.add_on_axis(Mirror())
# michel.propagate(outputarm + arm2)


# michel.draw()


if freecad_da:
  setview()