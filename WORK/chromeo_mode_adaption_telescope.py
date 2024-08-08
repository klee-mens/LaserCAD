#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 00:27:52 2024

@author: mens
"""

from LaserCAD.basic_optics import Mirror, Composition, Lens, Beam, Composed_Mount
from LaserCAD.non_interactings import Lambda_Plate
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()

PulsePicker = Composition()

PulsePicker.propagate(45)
PulsePicker.add_on_axis(Mirror(phi=90))
PulsePicker.propagate(100)
L1 = Lens(f=1029)
PulsePicker.add_on_axis(L1)
# L1.set_geom( PulsePicker.last_geom())
L1.pos += L1.get_coordinate_system()[1]*7.5
# PulsePicker.add_fixed_elm(L1)
PulsePicker.recompute_optical_axis()
PulsePicker.propagate((19.3920212936470+1029*2-4)/2)
M_tele = Mirror()
PulsePicker.add_on_axis(M_tele)
# M_tele.set_geom(PulsePicker.last_geom())
M_tele.normal = L1.normal
# PulsePicker.add_fixed_elm(M_tele)
PulsePicker.recompute_optical_axis()
# PulsePicker.propagate((19.3920212936470+1029*2)/2)
PulsePicker.set_sequence([0,1,2,1])
PulsePicker.recompute_optical_axis()
PulsePicker.propagate(50)
M_tele2 = Mirror(phi = 90)
M_tele2.set_mount(Composed_Mount(unit_model_list=["MH25_KMSS", "1inch_post"]))
# # M_tele2.Mount.mount_list[0].flip()
# # M_tele2.Mount.set_geom(M_tele2.get_geom())
PulsePicker.add_on_axis(M_tele2)
PulsePicker.propagate(30)
PulsePicker.add_on_axis(Lambda_Plate())
PulsePicker.propagate(80)

PulsePicker.draw()


if freecad_da:
  setview()