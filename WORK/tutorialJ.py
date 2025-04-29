#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 16:13:57 2025

@author: mens
"""

from LaserCAD.basic_optics import Beam, Lens, Composition, Mirror
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()

b1 = Beam(2, 0.1, ray_count=10)
l1 = Lens(100, name='L1')
l1.pos += (50, 0, 0) 
b2 = l1.next_beam(b1)
l2 = Lens(50, name= 'L2')
l2.pos = l1.pos+(100,0,5)
b3 = l2.next_beam(b2)


comp1 = Composition('Teleskop')
comp1.set_light_source(b1)
comp1.propagate(50)
comp1.add_on_axis(l1)
comp1.propagate(100)
comp1.add_on_axis(l2)
l2.pos += (0,0,5)
comp1.recompute_optical_axis()
comp1.propagate(100)
comp1.add_on_axis(Mirror(90))
comp1.propagate(100)


# =============================================================================
# draw section
# =============================================================================
# b1.draw()
# l1.draw()
# l1.draw_mount()
# b2.draw()
# l2.draw()
# l2.draw_mount()
# b3.draw()
comp1.draw() 

if freecad_da:
  setview()