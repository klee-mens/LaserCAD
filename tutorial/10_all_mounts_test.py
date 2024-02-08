# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:16:37 2023

@author: mens
"""

import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)


# from LaserCAD.non_interactings import Iris
# from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror,Crystal
from LaserCAD.basic_optics import Beam,Grating, Composition, inch, Curved_Mirror, Ray, Geom_Object, LinearResonator, Lens, Component
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.basic_optics.mount import Unit_Mount,Post, Composed_Mount
from LaserCAD.basic_optics.mount import MIRROR_LIST,LENS_LIST

if freecad_da:
  clear_doc()
  
for i in range(len(MIRROR_LIST)):
  M = Composed_Mount(unit_model_list=[MIRROR_LIST[i],"1inch_post"])
  aperture = M.mount_list[0].aperture
  mir= Mirror()
  mir.aperture = aperture
  mir.Mount = M
  mir.pos = (i*75,0,50+i*10)
  if mir.aperture > 25.4*4:
    mir.pos -= (50,0,0)
    mir.Mount.pos += mir.normal*mir.thickness
  mir.draw()
  mir.Mount.draw()
  
for i in range(len(LENS_LIST)):
  M = Composed_Mount(unit_model_list=[LENS_LIST[i],"0.5inch_post"])
  aperture = M.mount_list[0].aperture
  mir= Lens()
  mir.aperture = aperture
  mir.Mount = M
  mir.pos = (i*75,-100,100+i*10)
  mir.draw()
  mir.Mount.draw()

#   The above code is just a demonstration of how the mount is drawn. The next 
# step is to demonstrate the practical use of the mount.


# case1: aperture
mir = Mirror()
mir.pos += (0,-200,0)
mir.aperture = 1.75* inch
mir.set_mount_to_default() 
mir.draw()
mir.Mount.draw()

# case2: Specified mount
mir = Mirror()
mir.aperture = 2* inch
mir.pos += (100,-200,0)
M = Composed_Mount(unit_model_list=["KS2","1inch_post"])
mir.Mount = M
M.set_geom(mir.get_geom())
mir.draw()
mir.Mount.draw()


# case3: Adaptive_Angular_Mount
mir = Mirror() 
M = Composed_Mount(unit_model_list=["Adaptive_Angular_Mount","KS1","1inch_post"])
mir.pos = (0,100,80)
mir.normal = (1,1,-2)
mir.Mount = M
M.set_geom(mir.get_geom())
mir.draw()
mir.draw_mount()

# case3.5: Post holder
mir = Mirror()
M = Composed_Mount(unit_model_list=["KS1","1inch_post","Post_Marker"])
mir.pos = (100,100,80)
mir.Mount = M
M.set_geom(mir.get_geom())
mir.draw()
mir.draw_mount()

# case4: Filpped mount and reversed mount
Comp0 = Composition()
B0 = Beam()
Comp0.set_light_source(B0)
Comp0.pos += (0,300,0)
Comp0.propagate(100)
mir0 = Mirror(phi=150)
Comp0.add_on_axis(mir0)
Comp0.propagate(100)
Comp0.draw()

Comp1 = Composition()
B1 = Beam()
Comp1.set_light_source(B1)
Comp1.pos += (0,400,0)
Comp1.propagate(100)
mir1 = Mirror(phi=150)
mir1.pos+=(0,250,0)
mir1.Mount.mount_list[0].flip(90)
Comp1.add_on_axis(mir1)
Comp1.propagate(100)
Comp1.draw()

Comp2 = Composition()
B2 = Beam()
Comp2.set_light_source(B2)
Comp2.pos += (0,200,0)
Comp2.propagate(100)
mir2 = Mirror(phi=150)
mir2.Mount.reverse()
Comp2.add_on_axis(mir2)
Comp2.propagate(100)
Comp2.draw()

# case5: Mirror with lens mount or half inch post
mir = Mirror()
mir.pos += (0,500,0)
M = Composed_Mount(unit_model_list=["LMR1_M","1inch_post"])
mir.Mount = M
M.set_geom(mir.get_geom())
mir.draw()
mir.draw_mount()

mir1 = Mirror()
mir1.pos += (0,550,0)
M = Composed_Mount(unit_model_list=["KS1","0.5inch_post"])
mir1.Mount = M
M.set_geom(mir1.get_geom())
mir1.draw()
mir1.draw_mount()


if freecad_da:
  setview()