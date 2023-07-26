# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:15:19 2023

@author: 12816
"""

#!/usr/bin/python

import sys
import os
    
sys.path.append('C:\\ProgramData\\Anaconda3')

from LaserCAD import basic_optics

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating, Lam_Plane

from LaserCAD.freecad_models import clear_doc, setview, freecad_da,add_to_composition
from LaserCAD.moduls import Make_Periscope

# from basic_optics.mirror import curved_mirror_test
import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk


def periscope_GUI():
  font_size = 14
  font_name = "Times New Roman"
  
  def build_periscope():
    if freecad_da:
      clear_doc()
    length = float(length_input.get())
    theta = float(theta_input.get())
    dist1 = float(dist1_input.get())
    dist2 = float(dist2_input.get())
    tele = Make_Periscope(length=length,theta=theta,dist1=dist1,dist2=dist2)
    tele.pos=(0,0,100)
    tele.draw()
    
  window =tk.Tk()
  window.title("FreeCAD GUI make periscope")
  window.resizable(width=True, height=True)
  length_entry = tk.Frame(master=window)
  length_Label = tk.Label(master=length_entry, text="length(mm)=",font=(font_name,font_size))
  length_input = tk.Entry(master=length_entry, width=10,font=(font_name,font_size))
  length_input.insert(0, "160")
  length_Label.grid(row=0, column=0)
  length_input.grid(row=0, column=1)
  
  theta_entry = tk.Frame(master=window)
  theta_Label = tk.Label(master=theta_entry, text="theta=",font=(font_name,font_size))
  theta_input = tk.Entry(master=theta_entry, width=10,font=(font_name,font_size))
  theta_input.insert(0, "90")
  theta_Label.grid(row=0, column=0)
  theta_input.grid(row=0, column=1)
  
  dist1_entry = tk.Frame(master=window)
  dist1_Label = tk.Label(master=dist1_entry, text="dist1(mm)=",font=(font_name,font_size))
  dist1_input = tk.Entry(master=dist1_entry, width=10,font=(font_name,font_size))
  dist1_input.insert(0, "75")
  dist1_Label.grid(row=0, column=0)
  dist1_input.grid(row=0, column=1)
  
  dist2_entry = tk.Frame(master=window)
  dist2_Label = tk.Label(master=dist2_entry, text="dist2(mm)=",font=(font_name,font_size))
  dist2_input = tk.Entry(master=dist2_entry, width=10,font=(font_name,font_size))
  dist2_input.insert(0, "75")
  dist2_Label.grid(row=0, column=0)
  dist2_input.grid(row=0, column=1)
  
  btn_convert = tk.Button(
      master=window,
      text="build telescope",
      command=build_periscope,font=(font_name,font_size)
  )
  
  length_entry.grid(row=0, column=0, padx=10)
  theta_entry.grid(row=1, column=0, padx=10)
  dist1_entry.grid(row=2, column=0, padx=10)
  dist2_entry.grid(row=3, column=0, padx=10)
  btn_convert.grid(row=4, column=0, padx=10)
  window.rowconfigure([0,1,2,3,4],weight=1, minsize=30)
  window.columnconfigure([0,1],weight=1, minsize=50)
  window.mainloop()
  
# periscope_GUI()