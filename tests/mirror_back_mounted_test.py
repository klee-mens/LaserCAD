# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 03:47:53 2026

@author: mens
"""

from LaserCAD import Mirror, Composition
from LaserCAD import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()
  

setup = Composition(name="Thickmirrortest")
setup.propagate(100)

mir1 = Mirror(phi=90)
mir1.thickness = 15

setup.add_on_axis(mir1)
setup.propagate(70)
mir1.set_mount_face_mounted()

setup.draw()


setup2 = Composition(name="Thickmirrortest")
setup2.pos += (150, 0, 0)

setup2.propagate(100)

mir2 = Mirror(phi=90)
mir2.thickness = 15
mir2.set_mount_back_mounted()

setup2.add_on_axis(mir2)
setup2.propagate(70)

setup2.draw()

if freecad_da:
  setview()