# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:01:12 2024

@author: 12816
"""
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
from LaserCAD import Composition, Beam, ThinBeamsplitter, Mirror, Composed_Mount, ThickBeamsplitter


if freecad_da:
  clear_doc()

from LaserCAD.WORK.tutorialJ import comp

from LaserCAD.basic_optics.mount import KM100C

mir = Mirror()
mir.set_mount(KM100C(aperture=mir.aperture))
# km = KM100C()
# km.draw()

mir.draw()
mir.draw_mount()

if freecad_da:
  setview()