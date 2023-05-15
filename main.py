# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023
hi
i@author: mens
"""


import numpy as np
import sys
import os
import numpy as np

pfad = __file__
pfad = pfad[0:-7] #nur wenn das Skript auch wirklich main.py heißt
sys.path.append(pfad)
inch = 25.4


from basic_optics.freecad_models import clear_doc, setview, freecad_da
from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Lens, Ray, Composition, Grating, Propagation
from basic_optics.freecad_models import input_output_test
# from basic_optics.tests import all_moduls_test
from basic_optics.moduls import Make_Stretcher, Make_Telescope
from basic_optics.resonator import LinearResonator

from basic_optics.tests import all_moduls_test, three_resonators_test


if freecad_da:
  clear_doc()

# a,b,c,d,e = all_moduls_test()

# r1,r2,r3 = three_resonators_test()

from basic_optics.freecad_models.freecad_model_lens import model_lens
from basic_optics.freecad_models.freecad_model_mounts import mirror_mount


from basic_optics.freecad_models.utils import load_STEP
g = Geom_Object(name="COSMETIC")
g.draw_dict["drawing_post"] = False
g.draw_dict["mount_name"] = g.name+"_M"
g.draw_dict["step_file"] = u"/home/mens/projects/LaserCAD/dummy2.step"
# g.freecad_model = mirror_mount
g.freecad_model = load_STEP

import os
# print(os.listdir())

res3 = LinearResonator(name="foldedRes")
res3.pos += (0,-200, 0)

alpha = -8
beta = -0.1
print("g1*g2 = ", alpha*beta)
focal = 250
dist1 = (1-alpha)*focal
dist2 = (1-beta)*focal
wavelength = 0.1
frac0 = 0.05
frac1 = 0.3
frac2 = 0.1
frac3 = 1 - frac0 - frac1 - frac2

mir1 = Mirror(phi=180)
mir2 = Mirror(phi=75)
mir3 = Mirror(phi=-75)
mir4 = Mirror(phi=180)
cm = Curved_Mirror(radius=focal*2, phi = 170)

res3.add_on_axis(mir1)
res3.propagate(dist1*frac0)
res3.add_on_axis(g)
res3.propagate(dist1*frac1)
res3.add_on_axis(mir2)
res3.propagate(dist1*frac2)
res3.add_on_axis(mir3)
res3.propagate(dist1*frac3)
res3.add_on_axis(cm)
res3.propagate(dist2)
res3.add_on_axis(mir4)

res3.compute_eigenmode()

res3.draw()

if freecad_da:
  setview()