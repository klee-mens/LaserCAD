# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:15:19 2023

@author: 12816
"""

#!/usr/bin/python

import sys
import os
    
sys.path.append('C:/ProgramData/Anaconda3')
# pfad = __file__
# pfad = pfad.replace("/", "/") #just in case
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

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Intersection_plane,Cylindrical_Mirror1,Curved_Mirror,Ray, Composition, Grating

from LaserCAD.freecad_models import clear_doc, setview, freecad_da,add_to_composition
from LaserCAD.moduls import Make_Amplifier_Typ_I_simple,Make_Amplifier_Typ_I_Mirror,Make_Amplifier_Typ_II_simple
from LaserCAD.moduls import Make_Amplifier_Typ_II_Mirror,Make_Amplifier_Typ_II_UpDown,Make_Amplifier_Typ_II_plane
from LaserCAD.moduls import Make_Amplifier_Typ_II_with_theta,Make_Amplifier_Typ_II_Juergen

# from basic_optics.mirror import curved_mirror_test
import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk


def amplifier_GUI():
  font_size = 14
  font_name = "Times New Roman"
  
  def get_numbers():
    if freecad_da:
      clear_doc()
    focal_length = float(f_input.get())
    magnification = float(magnification_input.get())
    dist3 = float(d3_input.get())
    roundtrips2 = int(roundtrips2_input.get())
    beam_sep = float(beam_sep_input.get())
    return focal_length,dist3,roundtrips2,beam_sep,magnification
  
  def Amplifier_Typ_I_simple():
    focal_length,dist3,roundtrips2,beam_sep,magnification = get_numbers()
    tele = Make_Amplifier_Typ_I_simple(focal_length=focal_length,dist3=dist3,roundtrips2=roundtrips2,beam_sep=beam_sep)
    tele.pos=(0,0,100)
    tele.draw()
    
  def Amplifier_Typ_I_mirror():
    focal_length,dist3,roundtrips2,beam_sep,magnification = get_numbers()
    tele = Make_Amplifier_Typ_I_Mirror(focal_length=focal_length,magnification=magnification,roundtrips2=roundtrips2,beam_sep=beam_sep)
    tele.pos=(0,0,100)
    tele.draw()
  
  def Amplifier_Typ_II_simple():
    focal_length,dist3,roundtrips2,beam_sep,magnification = get_numbers()
    tele = Make_Amplifier_Typ_II_simple(focal_length=focal_length,magnification=magnification,roundtrips2=roundtrips2,beam_sep=beam_sep)
    tele.pos=(0,0,100)
    tele.draw()
  
  def Amplifier_Typ_II_mirror():
    focal_length,dist3,roundtrips2,beam_sep,magnification = get_numbers()
    tele = Make_Amplifier_Typ_II_Mirror(focal_length=focal_length,magnification=magnification,roundtrips2=roundtrips2,beam_sep=beam_sep)
    tele.pos=(0,0,100)
    tele.draw()

  def Amplifier_Typ_II_UpDown():
    focal_length,dist3,roundtrips2,beam_sep,magnification = get_numbers()
    tele = Make_Amplifier_Typ_II_UpDown(focal_length=focal_length,magnification=magnification,roundtrips2=roundtrips2,beam_sep=beam_sep)
    tele.pos=(0,0,100)
    tele.draw()
    
  def Amplifier_Typ_II_plane():
    focal_length,dist3,roundtrips2,beam_sep,magnification = get_numbers()
    tele = Make_Amplifier_Typ_II_plane(focal_length=focal_length,magnification=magnification,roundtrips2=roundtrips2,beam_sep=beam_sep)
    tele.pos=(0,0,100)
    tele.draw()
    
  def Amplifier_Typ_II_with_theta():
    focal_length,dist3,roundtrips2,beam_sep,magnification = get_numbers()
    tele = Make_Amplifier_Typ_II_with_theta(focal_length=focal_length,magnification=magnification,roundtrips2=roundtrips2,beam_sep=beam_sep)
    tele.pos=(0,0,100)
    tele.draw()
    
  def Amplifier_Typ_II_Juergen():
    focal_length,dist3,roundtrips2,beam_sep,magnification = get_numbers()
    tele = Make_Amplifier_Typ_II_Juergen(focal_length=focal_length,magnification=magnification,roundtrips2=roundtrips2,beam_sep=beam_sep)
    tele.pos=(0,0,100)
    tele.draw()

  window =tk.Tk()
  window.title("FreeCAD GUI make telescope")
  window.resizable(width=True, height=True)
  f_entry = tk.Frame(master=window)
  f_Label = tk.Label(master=f_entry, text="focal_length(mm)=",font=(font_name,font_size))
  f_input = tk.Entry(master=f_entry, width=10,font=(font_name,font_size))
  f_input.insert(0, "600")
  f_Label.grid(row=0, column=0)
  f_input.grid(row=0, column=1)
  
  magnification_entry = tk.Frame(master=window)
  magnification_Label = tk.Label(master=magnification_entry, text="magnification=",font=(font_name,font_size))
  magnification_input = tk.Entry(master=magnification_entry, width=10,font=(font_name,font_size))
  magnification_input.insert(0, "1")
  magnification_Label.grid(row=0, column=0)
  magnification_input.grid(row=0, column=1)
  
  d3_entry = tk.Frame(master=window)
  d3_Label = tk.Label(master=d3_entry, text="dist3(mm) (only works for simple type I amplifier)=",font=(font_name,font_size))
  d3_input = tk.Entry(master=d3_entry, width=10,font=(font_name,font_size))
  d3_input.insert(0, "600")
  d3_Label.grid(row=0, column=0)
  d3_input.grid(row=0, column=1)
  
  roundtrips2_entry = tk.Frame(master=window)
  roundtrips2_Label = tk.Label(master=roundtrips2_entry, text="roundtrips=",font=(font_name,font_size))
  roundtrips2_input = tk.Entry(master=roundtrips2_entry, width=10,font=(font_name,font_size))
  roundtrips2_input.insert(0, "2")
  roundtrips2_Label.grid(row=0, column=0)
  roundtrips2_input.grid(row=0, column=1)
  
  beam_sep_entry = tk.Frame(master=window)
  beam_sep_Label = tk.Label(master=beam_sep_entry, text="beam seperation=",font=(font_name,font_size))
  beam_sep_input = tk.Entry(master=beam_sep_entry, width=10,font=(font_name,font_size))
  beam_sep_input.insert(0, "15")
  beam_sep_Label.grid(row=0, column=0)
  beam_sep_input.grid(row=0, column=1)
  
  btn_T1_Amp_Simple = tk.Button(
      master=window,
      text="build lens Type I Amplifier",
      command=Amplifier_Typ_I_simple,font=(font_name,font_size)
  )
  
  btn_T1_Amp_Mirror = tk.Button(
      master=window,
      text="build mirror Type I Amplifier",
      command=Amplifier_Typ_I_mirror,font=(font_name,font_size)
  )
  
  btn_T2_Amp_Simple = tk.Button(
      master=window,
      text="build lens Type II Amplifier",
      command=Amplifier_Typ_II_simple,font=(font_name,font_size)
  )
  
  btn_T2_Amp_Mirror = tk.Button(
      master=window,
      text="build mirror Type II Amplifier",
      command=Amplifier_Typ_II_mirror,font=(font_name,font_size)
  )
  
  btn_T2_Amp_UpDown = tk.Button(
      master=window,
      text="build up down Type II Amplifier",
      command=Amplifier_Typ_II_UpDown,font=(font_name,font_size)
  )
  
  btn_T2_Amp_plane = tk.Button(
      master=window,
      text="build plane Type II Amplifier",
      command=Amplifier_Typ_II_plane,font=(font_name,font_size)
  )
  
  btn_T2_Amp_with_theta = tk.Button(
      master=window,
      text="build Type II Amplifier with theta",
      command=Amplifier_Typ_II_with_theta,font=(font_name,font_size)
  )
  
  btn_T2_Amp_Juergen = tk.Button(
      master=window,
      text="build Type II Amplifier Juergen",
      command=Amplifier_Typ_II_Juergen,font=(font_name,font_size)
  )
  
  f_entry.grid(row=0, column=0, padx=10)
  magnification_entry.grid(row=1, column=0, padx=10)
  d3_entry.grid(row=2, column=0, padx=10)
  roundtrips2_entry.grid(row=3, column=0, padx=10)
  beam_sep_entry.grid(row=4, column=0, padx=10)
  btn_T1_Amp_Simple.grid(row=5, column=0, padx=10)
  btn_T1_Amp_Mirror.grid(row=6, column=0, padx=10)
  btn_T2_Amp_Simple.grid(row=7, column=0, padx=10)
  btn_T2_Amp_Mirror.grid(row=8, column=0, padx=10)
  btn_T2_Amp_UpDown.grid(row=9, column=0, padx=10)
  btn_T2_Amp_plane.grid(row=10, column=0, padx=10)
  btn_T2_Amp_with_theta.grid(row=11, column=0, padx=10)
  btn_T2_Amp_Juergen.grid(row=12, column=0, padx=10)
  window.rowconfigure([0,1,2,3,4,5,6,7,8,9,10,11,12],weight=1, minsize=30)
  window.columnconfigure([0,1],weight=1, minsize=50)
  window.mainloop()
  
# amplifier_GUI()