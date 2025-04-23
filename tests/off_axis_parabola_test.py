# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 14:57:21 2025

@author: mens
"""

from LaserCAD.basic_optics.off_axis_parabola import Off_Axis_Parabola_Focus
from LaserCAD.basic_optics.beam import SquareBeam
from LaserCAD.basic_optics import Composition
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
import numpy as np

if freecad_da:
  clear_doc()


# oapf = Off_Axis_Parabola_Focus(angle=45)
oapf = Off_Axis_Parabola_Focus(angle=90)

sb = SquareBeam(radius=5, ray_in_line=20)


comp = Composition()
comp.set_light_source(sb)
comp.propagate(50)
comp.add_on_axis(oapf)
oapf.rotate(vec=oapf.normal, phi=np.pi)
comp.recompute_optical_axis()
comp.propagate(150)


comp.draw()

# nb = oapf.next_beam(sb)

# oapf.normal = (1,1,0)

# oapf.draw()

# sb.draw()
# nb.draw()
# oapf.draw()
# oapf.draw_mount()

if freecad_da:
  setview()