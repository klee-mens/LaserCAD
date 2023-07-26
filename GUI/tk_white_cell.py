# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:15:19 2023

@author: 12816
"""

#!/usr/bin/python

import sys
import os
    
sys.path.append('C:\\ProgramData\\Anaconda3')
# pfad = __file__
# pfad = pfad.replace("\\", "/") #just in case
# ind = pfad.rfind("/")
# pfad = pfad[0:ind]
# ind = pfad.rfind("/")
# pfad = pfad[0:ind+1]
# path_added = False
# for path in sys.path:
#   if path ==pfad:
#     path_added = True
# if not path_added:
#   sys.path.append(pfad)

from LaserCAD import basic_optics

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating, Lam_Plane,inch

from LaserCAD.freecad_models import clear_doc, setview, freecad_da,add_to_composition
from LaserCAD.moduls import Make_White_Cell

# from basic_optics.mirror import curved_mirror_test
import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk


def white_cell_GUI():
  font_size = 14
  font_name = "Times New Roman"
  
  def build_white_cell():
    if freecad_da:
      clear_doc()
    Radius = float(Radius_input.get())
    roundtrips4 = int(roundtrips4_input.get())
    mirror_sep = float(mirror_sep_input.get())
    tele = Make_White_Cell(Radius=Radius, roundtrips4=roundtrips4, aperture_small=1*inch,aperture_big=2*inch, mirror_sep=mirror_sep)
    tele.pos=(0,0,100)
    tele.draw()
    
  window =tk.Tk()
  window.title("FreeCAD GUI make white cell")
  window.resizable(width=True, height=True)
  Radius_entry = tk.Frame(master=window)
  Radius_Label = tk.Label(master=Radius_entry, text="Radius(mm)=",font=(font_name,font_size))
  Radius_input = tk.Entry(master=Radius_entry, width=10,font=(font_name,font_size))
  Radius_input.insert(0, "300")
  Radius_Label.grid(row=0, column=0)
  Radius_input.grid(row=0, column=1)
  
  roundtrips4_entry = tk.Frame(master=window)
  roundtrips4_Label = tk.Label(master=roundtrips4_entry, text="roundtrips=",font=(font_name,font_size))
  roundtrips4_input = tk.Entry(master=roundtrips4_entry, width=10,font=(font_name,font_size))
  roundtrips4_input.insert(0, "2")
  roundtrips4_Label.grid(row=0, column=0)
  roundtrips4_input.grid(row=0, column=1)
  
  mirror_sep_entry = tk.Frame(master=window)
  mirror_sep_Label = tk.Label(master=mirror_sep_entry, text="mirror sepration(mm)=",font=(font_name,font_size))
  mirror_sep_input = tk.Entry(master=mirror_sep_entry, width=10,font=(font_name,font_size))
  mirror_sep_input.insert(0, "10")
  mirror_sep_Label.grid(row=0, column=0)
  mirror_sep_input.grid(row=0, column=1)
  
  aperture_small_entry = tk.Frame(master=window)
  aperture_small_Label = tk.Label(master=aperture_small_entry, text="small mirror aperture(mm)=",font=(font_name,font_size))
  aperture_small_input = tk.Entry(master=aperture_small_entry, width=10,font=(font_name,font_size))
  aperture_small_input.insert(0, "25.4")
  aperture_small_Label.grid(row=0, column=0)
  aperture_small_input.grid(row=0, column=1)
  
  aperture_big_entry = tk.Frame(master=window)
  aperture_big_Label = tk.Label(master=aperture_big_entry, text="big mirror aperture(mm)=",font=(font_name,font_size))
  aperture_big_input = tk.Entry(master=aperture_big_entry, width=10,font=(font_name,font_size))
  aperture_big_input.insert(0, "50.8")
  aperture_big_Label.grid(row=0, column=0)
  aperture_big_input.grid(row=0, column=1)
  
  btn_convert = tk.Button(
      master=window,
      text="build white cell",
      command=build_white_cell,font=(font_name,font_size)
  )
  
  Radius_entry.grid(row=0, column=0, padx=10)
  roundtrips4_entry.grid(row=1, column=0, padx=10)
  mirror_sep_entry.grid(row=2, column=0, padx=10)
  aperture_small_entry.grid(row=3,column=0, padx=10)
  aperture_big_entry.grid(row=4,column=0, padx=10)
  btn_convert.grid(row=5, column=0, padx=10)
  window.rowconfigure([0,1,2,3,4,5],weight=1, minsize=30)
  window.columnconfigure([0,1],weight=1, minsize=50)
  window.mainloop()
  
# white_cell_GUI()