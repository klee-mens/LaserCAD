# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:14:09 2024

@author: mens
"""

from LaserCAD.non_interactings import Crystal, Crystal_Mount
from LaserCAD.freecad_models import freecad_da, clear_doc
from LaserCAD import Composed_Mount, Composition, Beam

if freecad_da:
  clear_doc()

# Standard rectangular crystal
crys1 = Crystal(width=10, height=10, thickness=10)
crys1.draw()
crys1.draw_mount()

# Standard cylindrical crystal
crys2 = Crystal(shape="cylindrical", aperture=15, thickness=10)
crys2.pos += (0, 50, 0)
crys2.draw()
crys2.draw_mount()

# Custom cylindrical crystal with custom mount
crys3 = Crystal(shape="cylindrical", aperture=15, thickness=10)
crys3.pos += (0, 100, 0)
crys3.set_mount(Crystal_Mount(
    shape="cylindrical",
    width=35,
    height=60,
    thickness=crys3.thickness,
    inner_aperture=crys3.aperture,
))
crys3.draw()
crys3.draw_mount()


# Crystal in a composition
crys4 = Crystal(shape="cylindrical", aperture=15, thickness=10)

Setup = Composition()
Setup.pos += (-200, 150, 0)
Setup.set_light_source(Beam())
Setup.propagate(200)
Setup.add_on_axis(crys4)
Setup.propagate(200)
Setup.draw()

