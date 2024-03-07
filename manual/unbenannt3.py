# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 16:18:51 2024

@author: mens
"""
import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Geom_Object, Beam, Component
from LaserCAD.basic_optics import Composed_Mount, Unit_Mount, Post
from LaserCAD.freecad_models.utils import freecad_da, clear_doc, setview, load_STL, thisfolder

if freecad_da:
  clear_doc()

class Detector(Component):
  def __init__(self, name="Det_PDA10A2", **kwargs):
    super().__init__(name, **kwargs)
    stl_file = thisfolder+"misc_meshes/Diode.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(0.1, 0.1, 0.1)
    self.freecad_model = load_STL
    self.set_mount_to_default()

  def set_mount_to_default(self):
    invis_adapter = Unit_Mount()
    invis_adapter.docking_obj.pos += (10.5, 0, -25)
    comp = Composed_Mount(name=self.name + "_mount")
    comp.add(invis_adapter)
    comp.add(Post(model="0.5inch_post"))
    # comp.add(Post())
    comp.set_geom(self.get_geom())
    self.Mount = comp

detector = Detector()
detector.draw()
detector.draw_mount()
# detector.pos += (100,0,0)


# b = Beam()
# b.set_length(100)
# b.draw()

# detector2 = Detector()
# detector2.pos += (0,50,0)
# detector2.normal = (-3,1,0)
# detector2.draw()

if freecad_da:
  setview()