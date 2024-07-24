#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:01:45 2024

@author: mens
"""

from LaserCAD.basic_optics import Mirror, Geom_Object, Grating
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()
  
m = Mirror()
m.pos += (12,13,14)
m.normal = 1,2,0

m.draw()
m.draw_mount()

g = Geom_Object()
g.set_geom(m.get_geom())

g.draw()  
  
gr = Grating()
gr.pos += 0,100,0
gr.normal = 1,1,0
gr.draw()
gr.draw_mount()

go = Geom_Object()
go.set_geom(gr.get_geom())
go.draw()

if freecad_da:
  setview()