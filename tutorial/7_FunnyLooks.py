
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 17:38:55 2023

@author: mens
"""

# =============================================================================
# some usefull imports that should be copied to ANY project
# =============================================================================
import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Mirror, Component, Composition
from LaserCAD.basic_optics import Composed_Mount, Unit_Mount, Post
from LaserCAD.freecad_models import freecad_da, clear_doc, setview, pfad


if freecad_da:
  clear_doc()
  
"""
Cosmetics tutorial

For comparision a standard <mir1> is drawn
Note that all essential draw parameters are gathered in the draw_dict.
For the passable arguments study the functions in the "freecad_models" folder

mir2: changed color and thickness

mir3: changed the mount model to something extravagant

seed_laser: example of a component that gets a fancy stl file for rendering

All objects could be easily added to a composition
"""

# =============================================================================
# Playground
# =============================================================================

mir1 = Mirror()
mir1.draw()
print()
# print(mir1.draw_dict)


mir2 = Mirror()
mir2.name = "FancyMirror"
mir2.pos += (0,42*2,0)

mir2.aperture = 50
mir2.draw_dict["thickness"] = 8
mir2.draw_dict["color"] = (1.0, 0.0, 1.0)  #RGB

mir2.draw()




# mir3.normal = (1,2,0)
# mir3.pos += (180, -170, 10)

class Spartan_Mount(Composed_Mount):
  def __init__(self):
    super().__init__()
    um = Unit_Mount()
    um.model = "Spartan"
    um.path = pfad + "misc_meshes/"
    um.docking_obj.pos += (24, 2, -35) # from manual adjustments in FreeCAD
    self.add(um)
    self.add(Post())

mir3 = Mirror(phi=75)
mir3.set_mount(Spartan_Mount())
mir4 = Mirror(phi=-60)
mir4.set_mount(Spartan_Mount())
mir5 = Mirror(phi=90)
mir5.set_mount(Spartan_Mount())
    
comp = Composition(name="MirrorAssembly")
comp.pos += (-200, -300, 0)
comp.propagate(200)
comp.add_on_axis(mir3)
comp.propagate(200)
comp.add_on_axis(mir4)
comp.propagate(200)
comp.add_on_axis(mir5)
comp.propagate(200)

comp.draw()
# mir3.Mount = Spartan_Mount()
# mir3.Mount.set_geom()
# mir3.draw()
# mir3.draw_mount()



from LaserCAD.freecad_models.utils import load_STL, thisfolder
seed_laser = Component()
stl_file=thisfolder+"\misc_meshes\Laser_Head-Body.stl"
seed_laser.draw_dict["stl_file"]=stl_file
color = (170/255, 170/255, 127/255) #RGB
seed_laser.draw_dict["color"]=color
seed_laser.freecad_model = load_STL
seed_laser.pos = (-100,-100, 90)
seed_laser.draw()

# =============================================================================
# Playground End
# =============================================================================
if freecad_da:
  setview()