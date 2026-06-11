# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:01:12 2024

@author: 12816
"""
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
from LaserCAD import Composition, Beam, ThinBeamsplitter, Mirror, Composed_Mount, ThickBeamsplitter, Crystal

from LaserCAD.freecad_models.freecad_model_crystal import model_crystal_mount, model_crystal, model_cylinder, model_box

import numpy as np

m = Mirror()
m.pos = (30, 0, 0)

if freecad_da:
  clear_doc()
  # obj = model_crystal()
  # obj2 = model_crystal_mount()

  # cyl = model_cylinder(name="lajskdf")

  # box = model_box(name="booox", geom=m.get_geom())

# crys = Crystal()
# crys.pos= (0,0,0)
# crys.draw()

# from LaserCAD.WORK.tutorialJ import comp

from LaserCAD.basic_optics.mount import KM100CL, Post
from LaserCAD.basic_optics.lens import Cylindrical_Lens
# from LaserCAD.basic_optics.mirror import Rectangular_Mirror

from LaserCAD.freecad_models.utils import thisfolder
from LaserCAD import Unit_Mount, inch

class KM100C_flipped(Composed_Mount):
  def __init__(self, name="KM100C", height=15, width=0, post="1inch_post", **kwargs):
    super().__init__(name=name, **kwargs)
    self.height = height
    self.width = width
    self.side_shift = 0 if self.height < 25 else (25-self.height)/2
    self.post_model = post
    self.docking_obj.rotate(vec=(1,0,0), phi=-np.pi/2)
    self.docking_obj.rotate(vec=(0,0,1), phi=np.pi)
    self.docking_obj.pos += (4, -width/2, self.side_shift)

    upper = Unit_Mount()
    upper.is_horizontal = False
    upper.model = "KM100C_upper"
    upper.path = thisfolder + "misc_meshes/"
    upper.draw_dict["color"] = (0.18,0.18,0.18)
    upper.docking_obj.pos += (0, 0, -self.width-0.7)
    self.add(upper)

    self.number_of_extensions = int((self.width+5) // (1.5*25.4)) + 1
    for n in range(self.number_of_extensions):
      extension = Unit_Mount()
      extension.is_horizontal = False
      extension.model = "KM100C_extension"
      extension.path = thisfolder + "misc_meshes/"
      extension.docking_obj.pos += (0, 0, +1.5*25.4)
      self.add(extension)

    invis = Unit_Mount()
    invis.is_horizontal = False
    invis.invisible = True
    invis.docking_obj.pos += (0, 0, -1.5*25.4*self.number_of_extensions)
    self.add(invis)

    lower = Unit_Mount()
    lower.is_horizontal = False
    # print("lower pos", lower.pos)
    lower.model = "KM100C_lower"
    lower.path = thisfolder + "misc_meshes/"
    lower.draw_dict["color"] = (0.18,0.18,0.18)
    lower.docking_obj.pos += (-9, 13.55+inch, -17.65+inch)
    self.add(lower)
    # print("lower pos", lower.pos)

    self.add(Post(model=post))



class KM100CL_flipped(Composed_Mount):
  def __init__(self, name="KM100CL_flipped", height=15, width=0, post="1inch_post", **kwargs):
    super().__init__(name=name, **kwargs)
    self.height = height
    self.width = width
    self.side_shift = 0 if self.height < 25 else (self.height-25)/2
    self.post_model = post
    self.docking_obj.rotate(vec=(1,0,0), phi=np.pi/2)
    self.docking_obj.rotate(vec=(0,0,1), phi=np.pi)
    self.docking_obj.pos += (4, +width/2, -self.side_shift)

    upper = Unit_Mount()
    upper.is_horizontal = False
    upper.model = "KM100CL_upper"
    upper.path = thisfolder + "misc_meshes/"
    upper.draw_dict["color"] = (0.18,0.18,0.18)
    upper.docking_obj.pos += (-1, -45.4, -width-0.7)
    self.add(upper)

    self.number_of_extensions = int((self.width+5) // (1.5*25.4)) + 1
    for n in range(self.number_of_extensions):
      extension = Unit_Mount()
      extension.is_horizontal = False
      extension.model = "KM100C_extension"
      extension.path = thisfolder + "misc_meshes/"
      extension.docking_obj.pos += (0, 0, +1.5*25.4)
      self.add(extension)

    invis = Unit_Mount()
    invis.is_horizontal = False
    invis.invisible = True
    invis.docking_obj.pos += (1, 45.4, -1.5*25.4*self.number_of_extensions)
    self.add(invis)

    lower = Unit_Mount()
    lower.is_horizontal = False
    lower.model = "KM100CL_lower"
    lower.path = thisfolder + "misc_meshes/"
    lower.draw_dict["color"] = (0.18,0.18,0.18)
    lower.docking_obj.pos += (-9-1, 13.55-29-inch, -17.65+inch)
    self.add(lower)
    # print("lower pos", lower.pos)

    self.add(Post(model=post))

  def reverse(self, thickness=7):
    self.rotate(vec=(0,0,1), phi=np.pi)
    self.pos += -self.normal*thickness


# mir = Mirror()
# mir = Rectangular_Mirror(height=30, width=60)
# mir = Rectangular_Mirror(height=50, width=60)
# mir = Rectangular_Mirror(height=80, width=60)
# mir.pos += (42, 41 , 50)
# mir.normal = (1,2,0)

# cyl = Cylindrical_Lens(f=100, height=40, aperture=60)
# cyl.set_mount(KM100CL(height=cyl.height, width=cyl.aperture))

# cyl.draw()
# cyl.draw_mount()


cyl2 = Cylindrical_Lens(f=100, height=40, aperture=70, thickness=5)
cyl2.pos += (0, 100, 0)
cyl2.set_mount(KM100CL_flipped(height=cyl2.height, width=cyl2.aperture))

# cyl2.pos += (40, 250, 60)
# cyl2.normal = (1,2,0)

cyl2.draw()
cyl2.draw_mount()

lmf = cyl2.Mount

cyl1 = Cylindrical_Lens(f=100, height=40, aperture=70, thickness=5)
cyl1.pos += (0, 100, 0)
cyl1.set_mount(KM100C_flipped(height=cyl2.height, width=cyl2.aperture))

cyl1.pos += (40, 150, 60)
# cyl1.normal = (1,2,0)

cyl1.draw()
cyl1.draw_mount()


# mir.set_mount(KM100C(height=mir.height, width=mir.width) )
# # km = KM100C()
# # km.draw()

# mir.draw()
# mir.draw_mount()

# ml = mir.Mount.mount_list
# for m in ml:
#   print(m)

if freecad_da:
  setview()