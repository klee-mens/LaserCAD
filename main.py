# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023

i@author: mens
"""


import sys
import os

pfad = __file__
pfad = pfad[0:-7] #nur wenn das Skript auch wirklich main.py heißt
sys.path.append(pfad)

from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens
from basic_optics import Beam, Mirror, Opt_Element, Geom_Object, Curved_Mirror, Lens, Ray, Composition, inch, Grating
# from basic_optics.composition import Teleskop_test, Composition_mirror_test, Mirror_Teleskop_test, add_only_elem_test
from basic_optics.mirror import curved_mirror_test

if freecad_da:
  clear_doc()






from basic_optics.tests import Telescope_4beam, Lens_4beam_Fokus, Parallel_ray_bundle_tilted_lens, grating_ray_bundle_test

# Telescope_4beam()
Lens_4beam_Fokus()
# Parallel_ray_bundle_tilted_lens()
# grating_ray_bundle_test()

from basic_optics.tests import all_moduls_test

# peris, teles, amp, stretch, wcell = all_moduls_test()

from basic_optics.moduls import Make_Amplifier_Typ_II_simple

# amp = Make_Amplifier_Typ_II_simple()
# amp.pos = (0,0,100)
# m0 = amp._elements[0]
# rgs = amp.compute_ray_groups()
# r0 = rgs[0][0]
# amp.draw()


if freecad_da:
  setview()

