# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:53:06 2024

@author: mens
"""
from LaserCAD.basic_optics import Beam, Refractive_plane
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()
  

ref = Refractive_plane()

b0 = Beam(radius=1.5)

ref.pos += (60, 0 , 0)
ref.normal = (1,1,0)

b1 =  ref.next_beam(b0)

ref2 = Refractive_plane(relative_refractive_index=1/1.5)

ref2.pos += (2*60, 0 , 0)
ref2.normal = ref.normal

b2 = ref2.next_beam(b1)

# =============================================================================
# drawing
# =============================================================================
b0.draw()
ref.draw()
b1.draw()
ref2.draw()
b2.draw()


if freecad_da:
  setview()