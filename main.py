# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:20 2023
hi
i@author: mens
"""


import sys
import os

pfad = __file__
pfad = pfad[0:-7] #nur wenn das Skript auch wirklich main.py heißt
sys.path.append(pfad)

# import basic_optics.freecad_models as fcm
# from importlib import reload
# reload(fcm)

from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens

from basic_optics import Beam, Mirror,RayGroup, Opt_Element, Geom_Object, Curved_Mirror
from basic_optics import Lens,Iris,Barriers,Intersection_plane, Ray, Composition, inch, Grating, Propagation
#from basic_optics.composition import Teleskop_test, Composition_mirror_test, Mirror_Teleskop_test, add_only_elem_test

# from basic_optics.mirror import curved_mirror_test
# from basic_optics.tests import all_moduls_test

if freecad_da:
  clear_doc()


# peris, teles, amp, stretch, wcell = all_moduls_test()



from basic_optics.moduls import Make_Telescope,Make_Amplifier_Typ_I_simpler,Make_Stretcher,Make_Amplifier_Typ_II_simpler,Make_Amplifier_Typ_II_simple,Make_Amplifier_Typ_I_simple
from basic_optics.moduls import diaphragms_test

from basic_optics.tests import iris_test

# teles = Make_Telescope()
# teles.draw()

# rg=Beam(radius=0.05,angle=-0.05)
# cavset=Composition(name="Cavity Setting")
# cavset.set_light_source(rg)
# cavset.normal=(0,-1,0)
# cavset.pos=(0,20,100)

# m1 = Mirror()
# m1.pos = (0,-15,100)
# point0 = (0,20,100)
# point1 = (-153.1560972,0,100)
# m1.set_normal_with_2_points(point0, point1)


# cm1 = Curved_Mirror(radius= 200,phi=180-2.796834341)
# cm1.pos = (-153.1560972,0,100) 
# cm1.aperture = 25.4*2

# cm2 = Curved_Mirror(radius= 200,theta=-2.796834341)
# cm2.pos = cm1.pos+(425,0,0)
# cm2.aperture = 25.4*2

# m2 = Mirror()
# m2.pos = cm2.pos -(173.06080608,0,4695/277)
# point0 = cm2.pos
# point1 = m2.pos - (0,15,0)
# m2.set_normal_with_2_points(point0, point1)

# ip = Intersection_plane()
# ip.pos = m2.pos - (0,15,0)
# ip.normal = (0,-1,0)

# cavset.add_fixed_elm(m1)
# cavset.add_fixed_elm(cm1)
# cavset.add_fixed_elm(cm2)
# cavset.add_fixed_elm(m2)
# cavset.add_fixed_elm(ip)

# cavset.draw()

iris_test()

if freecad_da:

  setview()