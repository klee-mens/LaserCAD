# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:16:37 2023

@author: mens
"""

import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
ind = pfad.rfind("/")
pfad = pfad[0:ind-1]
ind = pfad.rfind("/")
pfad = pfad[0:ind]
if not pfad in sys.path:
  sys.path.append(pfad)


# from LaserCAD.non_interactings import Iris
# from LaserCAD.non_interactings import Lambda_Plate

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

# sm = Curved_Mirror()
# sm.aperture =25.4*6
# # sm = Stripe_mirror()
# sm.pos = (130, 89, 120)
# sm.normal = (1,1,0)
# sm.thickness = 40
# sm.set_mount_to_default()
# sm.draw()
# sm.draw_mount()

# smm = Stripe_Mirror_Mount()
# smm.draw()


from LaserCAD.non_interactings import Lambda_Plate

# mon = Composed_Mount()
# mon1 = Unit_Mount("56_degree_mounts")
# mon.add(mon1)
# mon2 = Unit_Mount("65_degree_mounts")
# mon.add(mon2)
# mon3 = Unit_Mount("H45")
# mon.add(mon3)
# mon4 = Unit_Mount("KS1")
# mon.add(mon4)
# mon.add(Post())
# mon.add(Post_Marker())
# mon.draw()

# mir=Mirror()
# # mir.pos = (0,0,0)
# mir.Mount.mount_list[0].flip()
# mir.draw()
# mir.draw_mount()

# mir2=Mirror()
# mir2.pos += (0,50,0)
# # mir.Mount.mount_list[0].flip()
# mir2.draw()
# mir2.draw_mount()


from LaserCAD.freecad_models.freecad_model_geom_object import model_geom_object

# if freecad_da:
  # model_geom_object()

g = Geom_Object()
# g.freecad_model = model_geom_object
g.pos = (1,2,3)
# g.normal = (1,1,0)
g.draw()

# comp = Composition()
# comp.propagate(300)
# comp.add_on_axis(Mirror(phi=0, theta=90))

# comp.propagate(400)

# comp.pos += (12,50,0)
# comp.draw()

# M= Mirror()
# # M.Mount.add(Post_Marker(name=M.name,size=3))
# M.pos = (19.5-16,12.5+18,80)
# # M.normal = (1,1,0)
# M.draw()
# M.draw_mount()
# from LaserCAD.freecad_models.freecad_model_mounts import model_Post_Marker
# if freecad_da:
#   obj=model_Post_Marker(geom=M.Mount.mount_list[1].get_geom())

# lam = Lambda_Plate()
# lam.pos +=(10,20,30)
# lam.normal = (1,1,0)
# lam.draw()
# lam.draw_mount()

# rm = Rooftop_mirror()
# rm.pos = (120,50,130)
# rm.normal = (1,-1,0)
# rm.aperture = 10
# rm.set_mount_to_default()
# rm.draw()
# rm.draw_mount()

# grat = Grating()
# grat.pos = (120,13,150)
# grat.normal = (1,-1,0)
# grat.height = 40
# grat.thickness = 8
# grat.set_mount_to_default()
# grat.draw()
# grat.draw_mount()

# mon = Composed_Mount()
# mon1 = Unit_Mount("56_degree_mounts")
# mon.add(mon1)
# mon2 = Unit_Mount("65_degree_mounts")
# mon.add(mon2)
# mon3 = Unit_Mount("H45")
# mon.add(mon3)
# mon4 = Unit_Mount("KS1")
# mon.add(mon4)
# mon.add(Post())
# mon.draw()

# mir2 = Mirror()
# a = Unit_Mount(model='POLARIS-K1')
# mir2.Mount = a
# a.reverse()
# mir2.draw()
# mir2.draw_mount()

# mir2 = Mirror()
# mir2.pos += (50,0,0)
# mir2.Mount.reverse()
# mir2.draw()
# mir2.draw_mount()

# mir.Mount.mount_list[-1].set_lower_limit(22)
# mir.aperture = 2*inch
# mir.set_mount_to_default()
# mir.pos = (39,123,90)
# mir.normal = (1,2,0.5)
# mir.set_mount_to_default()
# a= Special_Mount()
# a.draw()
# mir.draw()
# mir.Mount.draw()

# for i in range(len(MIRROR_LIST)):
#   M = Composed_Mount(unit_model_list=[MIRROR_LIST[i],"1inch_post"])
#   aperture = M.mount_list[0].aperture
#   mir= Mirror()
#   mir.aperture = aperture
#   mir.Mount = M
#   mir.pos = (i*50,0,50+i*10)
#   mir.draw()
#   mir.Mount.draw()
  
# for i in range(len(LENS_LIST)):
#   M = Composed_Mount(unit_model_list=[LENS_LIST[i],"0.5inch_post"])
#   aperture = M.mount_list[0].aperture
#   mir= Lens()
#   mir.aperture = aperture
#   mir.Mount = M
#   mir.pos = (i*50,-100,100+i*10)
#   mir.draw()
#   mir.Mount.draw()

# M = Unit_Mount(model="KS2")
# M.is_horizontal = False
# M.normal = (1,1,1)
# M.draw()

# p = Post(model="0.5inch_post")
# p.draw()
# print(MIRROR_LIST)
# models = ["KS1", "1inch_post"]
# comp = Composed_Mount(unit_model_list=models)
# comp.draw()

# mir2 = Lens()
# mir2.set_geom(M.docking_obj.get_geom())
# mir2.draw()

if freecad_da:
  setview()