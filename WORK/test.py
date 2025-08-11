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
from LaserCAD.basic_optics.mirror import Rectangular_Mirror

# mir = Mirror()
# mir = Rectangular_Mirror(height=30, width=60)
# mir = Rectangular_Mirror(height=50, width=60)
mir = Rectangular_Mirror(height=80, width=60)
mir.pos += (42, 41 , 50)
mir.normal = (1,2,0)

mir.set_mount(KM100C(height=mir.height, width=mir.width) )
# km = KM100C()
# km.draw()

mir.draw()
mir.draw_mount()

ml = mir.Mount.mount_list
for m in ml:
  print(m)

if freecad_da:
  setview()