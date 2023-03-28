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

# import basic_optics.freecad_models as fcm
# from importlib import reload
# reload(fcm)

from basic_optics.freecad_models import clear_doc, setview, freecad_da, freecad_model_lens
from basic_optics import Beam, Mirror,RayGroup, Opt_Element, Geom_Object, Curved_Mirror, Lens,Iris,Diaphragms,Intersection_plane, Ray, Composition, inch, Grating, Propagation
#from basic_optics.composition import Teleskop_test, Composition_mirror_test, Mirror_Teleskop_test, add_only_elem_test
from basic_optics.mirror import curved_mirror_test

if freecad_da:
  clear_doc()



# from basic_optics.freecad_models.freecad_model_mirror import model_stripe_mirror,model_round_mirror




# from basic_optics.tests import Telescope_4beam, Lens_4beam_Fokus, Parallel_ray_bundle_tilted_lens, grating_ray_bundle_test

# Telescope_4beam()
# Lens_4beam_Fokus()
# Parallel_ray_bundle_tilted_lens()
# grating_ray_bundle_test()

# from basic_optics.tests import all_moduls_test

# peris, teles, amp, stretch, wcell = all_moduls_test()



from basic_optics.moduls import Make_Telescope,Make_Amplifier_Typ_I_simpler,Make_Stretcher,Make_Amplifier_Typ_II_simpler,Make_Amplifier_Typ_II_simple,Make_Amplifier_Typ_I_simple
from basic_optics.moduls import diaphragms_test
# peris = Make_Telescope()
# peris.draw()
# teles = Make_Periscope()
# teles.draw_elements()
# teles.draw_mounts()
# amplifier0 = Make_Amplifier_Typ_I_simple(beam_sep=15,roundtrips2=2)
# amplifier0.pos = (0, 0, 100)
# amplifier0.draw_elements()
# # amplifier0.draw_rays()
# amplifier0.draw_mount()
# amplifier0.draw_beams()

# amplifier1 = Make_Amplifier_Typ_I_simpler(beam_sep=20,roundtrips2=2)
# amplifier1.pos = (0, 200, 100)
# amplifier1.draw_elements()
# # amplifier1.draw_rays()
# amplifier1.draw_mounts()
# amplifier1.draw_beams()

# amplifier2 = Make_Amplifier_Typ_II_simple(beam_sep=15,roundtrips2=2)
# amplifier2.pos = (0, 400, 100)
# amplifier2.draw_elements()
# # amplifier2.draw_rays()
# amplifier2.draw_mount()
# amplifier2.draw_beams()

# amplifier3 = Make_Amplifier_Typ_II_simpler(beam_sep=20,roundtrips2=2)
# amplifier3.pos = (0, 600, 100)
# amplifier3.draw_elements()
# # amplifier3.draw_rays()

# amplifier3.draw_mounts()
# amplifier3.draw_beams()

# dia = diaphragms_test()
# dia.pos = (0,0,100)
# dia.draw_elements()
# dia.draw_rays()
# #dia.draw_beams()
# dia.draw_mounts()

rg=RayGroup(waist=2.5,pos=(0,0,100))
rg.make_square_distribution(10)
dia1 = Composition(name="RayGroup test")
dia1.set_light_source(rg)
dia1.propagate(100)
l1=Lens(f=150)
dia1.add_on_axis(l1)
dia1.propagate(150)
ip=Intersection_plane()
dia1.add_on_axis(ip)
dia1.propagate(150)
ip.spot_diagram(dia1.compute_beams().pop())



dia1.draw_elements()
dia1.draw_rays()
dia1.draw_mounts()


if freecad_da:
  #model_stripe_mirror(dia=152.4,Radius1=-1000)
  #model_round_mirror(dia=152.4, thickness=30,Radius=500)
  setview()

