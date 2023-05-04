# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023
hi
i@author: mens
"""


import sys
import os
import numpy as np

pfad = __file__
pfad = pfad[0:-7] #nur wenn das Skript auch wirklich main.py heißt
sys.path.append(pfad)
inch = 25.4


from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens
from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Lens, Ray, Composition, Grating, Propagation
from basic_optics.tests import all_moduls_test
from basic_optics.moduls import Make_Stretcher


if freecad_da:
  clear_doc()


stretcher = Make_Stretcher()
stretcher.pos=(0,0,120)
stretcher.draw_elements()
stretcher.draw_mounts()
stretcher.draw_rays()


# teles = Composition(name="KepplerTelescope")
# liso = Beam(radius=1, angle=0)
# teles.set_light_source(liso)
# f1 = 100
# f2 = 300
# le1 = Lens(f=f1)
# le2 = Lens(f=f2)

# teles.propagate(f1)
# teles.add_on_axis(le1)
# teles.propagate(f1+f2)
# teles.add_on_axis(le2)
# teles.propagate(f2)

# flip1 = Mirror(phi=65)
# flip1.draw_dict["mount_type"] = "KS1"

# teles.add_on_axis(flip1)
# teles.propagate(80)

# teles.draw()


if freecad_da:
  setview()