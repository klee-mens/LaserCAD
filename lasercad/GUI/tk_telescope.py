# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:15:19 2023

@author: 12816
"""

#!/usr/bin/python

import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD import basic_optics

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating

from LaserCAD.freecad_models import clear_doc, setview, freecad_da,add_to_composition
from LaserCAD.moduls import Make_Telescope

# from basic_optics.mirror import curved_mirror_test
import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk


def telescope_GUI():
  font_size = 14
  font_name = "Times New Roman"
  
  def build_telescope():
    if freecad_da:
      clear_doc()
    f1 = float(f1_input.get())
    f2 = float(f2_input.get())
    d0 = float(d0_input.get())
    tele = Make_Telescope(f1=f1,f2=f2,d0=d0)
    tele.pos=(0,0,100)
    tele.draw()
    
  window =tk.Tk()
  window.title("FreeCAD GUI make telescope")
  window.resizable(width=True, height=True)
  f1_entry = tk.Frame(master=window)
  f1_Label = tk.Label(master=f1_entry, text="f1(mm)=",font=(font_name,font_size))
  f1_input = tk.Entry(master=f1_entry, width=10,font=(font_name,font_size))
  f1_Label.grid(row=0, column=0)
  f1_input.grid(row=0, column=1)
  
  f2_entry = tk.Frame(master=window)
  f2_Label = tk.Label(master=f2_entry, text="f2(mm)=",font=(font_name,font_size))
  f2_input = tk.Entry(master=f2_entry, width=10,font=(font_name,font_size))
  f2_Label.grid(row=0, column=0)
  f2_input.grid(row=0, column=1)
  
  d0_entry = tk.Frame(master=window)
  d0_Label = tk.Label(master=d0_entry, text="light sourse position(mm)=",font=(font_name,font_size))
  d0_input = tk.Entry(master=d0_entry, width=10,font=(font_name,font_size))
  d0_Label.grid(row=0, column=0)
  d0_input.grid(row=0, column=1)
  
  btn_convert = tk.Button(
      master=window,
      text="build telescope",
      command=build_telescope,font=(font_name,font_size)
  )
  
  f1_entry.grid(row=0, column=0, padx=10)
  f2_entry.grid(row=1, column=0, padx=10)
  d0_entry.grid(row=2, column=0, padx=10)
  btn_convert.grid(row=3, column=0, padx=10)
  window.rowconfigure([0,1,2,3],weight=1, minsize=30)
  window.columnconfigure([0,1],weight=1, minsize=50)
  window.mainloop()
  
# telescope_GUI()