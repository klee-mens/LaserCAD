# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:16:37 2023

@author: mens
"""
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror,Crystal
from LaserCAD.basic_optics import Beam,Grating, Composition, inch, Curved_Mirror, Ray, Geom_Object, LinearResonator, Lens, Component
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.basic_optics.mount import Unit_Mount,Post, Composed_Mount,Post_Marker
from LaserCAD.basic_optics.mount import MIRROR_LIST,LENS_LIST

if freecad_da:
  clear_doc()
  
from LaserCAD.basic_optics.mount import Stripe_Mirror_Mount
from LaserCAD.basic_optics.mirror import Stripe_mirror,Rooftop_mirror

from LaserCAD.freecad_models.freecad_model_mounts import model_mirror_holder
from LaserCAD.basic_optics.mount import Adaptive_Angular_Mount

mir = Mirror(theta= 120) 
M = Composed_Mount(unit_model_list=["Adaptive_Angular_Mount","KS1","1inch_post"])
mir.normal = (1,0,0.5)
mir.Mount = M
M.set_geom(mir.get_geom())
# mir.normal = (1,0,-2)
# M.add(Adaptive_Angular_Mount(aperture=50.8/2,angle= 60))
# M.add(Unit_Mount("KS1"))
# M.add(Post())
# M.add(Post_Marker())
mir.draw()
mir.draw_mount()



if freecad_da:
  setview()