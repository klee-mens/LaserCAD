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
from LaserCAD.moduls import Make_Stretcher

import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk


def stretcher_GUI():
  font_size = 14
  font_name = "Times New Roman"
  
  def build_stretcher():
    if freecad_da:
      clear_doc()
    Radius = float(R_input.get())
    Aperture_concav = float(concav_aperture_input.get())
    h_StripeM = float(h_StripeM_input.get())
    gamma = float(gamma_input.get())
    grat_const = float(grat_const_input.get())
    seperation = float(seperation_input.get())
    lam_mid = float(lam_mid_input.get())
    delta_lamda = float(delta_lamda_input.get())
    number_of_rays = int(number_of_rays_input.get())
    safety_to_StripeM = float(safety_to_StripeM_input.get())
    periscope_distance = float(periscope_distance_input.get())
    tele = Make_Stretcher(Radius,Aperture_concav,h_StripeM,gamma,grat_const,
                          seperation,lam_mid,delta_lamda,number_of_rays,
                          safety_to_StripeM,periscope_distance)
    tele.pos=(0,0,100)
    tele.draw()
    
  window =tk.Tk()
  window.title("FreeCAD GUI make stretcher")
  window.resizable(width=True, height=True)
  R_entry = tk.Frame(master=window)
  R_Label = tk.Label(master=R_entry, text="Radius(mm)=",font=(font_name,font_size))
  R_input = tk.Entry(master=R_entry, width=10,font=(font_name,font_size))
  R_input.insert(0, "1000")
  R_Label.grid(row=0, column=0)
  R_input.grid(row=0, column=1)
  
  concav_aperture_entry = tk.Frame(master=window)
  concav_aperture_Label = tk.Label(master=concav_aperture_entry, text="Concav mirror's aperture(mm)=",font=(font_name,font_size))
  concav_aperture_input = tk.Entry(master=concav_aperture_entry, width=10,font=(font_name,font_size))
  concav_aperture_input.insert(0, "152.4")
  concav_aperture_Label.grid(row=0, column=0)
  concav_aperture_input.grid(row=0, column=1)
  
  h_StripeM_entry = tk.Frame(master=window)
  h_StripeM_Label = tk.Label(master=h_StripeM_entry, text="Height of the strip mirror(mm)=",font=(font_name,font_size))
  h_StripeM_input = tk.Entry(master=h_StripeM_entry, width=10,font=(font_name,font_size))
  h_StripeM_input.insert(0, "10")
  h_StripeM_Label.grid(row=0, column=0)
  h_StripeM_input.grid(row=0, column=1)
  
  gamma_entry = tk.Frame(master=window)
  gamma_Label = tk.Label(master=gamma_entry, text="Seperation angle between incident and center beam; alpha = gamma + beta(rad)=",font=(font_name,font_size))
  gamma_input = tk.Entry(master=gamma_entry, width=30,font=(font_name,font_size))
  gamma_input.insert(0, str(5 /180 *np.pi))
  gamma_Label.grid(row=0, column=0)
  gamma_input.grid(row=0, column=1)
  
  grat_const_entry = tk.Frame(master=window)
  grat_const_Label = tk.Label(master=grat_const_entry, text="Grating const(1/mm)=",font=(font_name,font_size))
  grat_const_input = tk.Entry(master=grat_const_entry, width=30,font=(font_name,font_size))
  grat_const_input.insert(0, str(1/450))
  grat_const_Label.grid(row=0, column=0)
  grat_const_input.grid(row=0, column=1)
  
  seperation_entry = tk.Frame(master=window)
  seperation_Label = tk.Label(master=seperation_entry, text="seperation(mm)=",font=(font_name,font_size))
  seperation_input = tk.Entry(master=seperation_entry, width=10,font=(font_name,font_size))
  seperation_input.insert(0, "100")
  seperation_Label.grid(row=0, column=0)
  seperation_input.grid(row=0, column=1)

  lam_mid_entry = tk.Frame(master=window)
  lam_mid_Label = tk.Label(master=lam_mid_entry, text="wavelength of the middle ray(mm)=",font=(font_name,font_size))
  lam_mid_input = tk.Entry(master=lam_mid_entry, width=10,font=(font_name,font_size))
  lam_mid_input.insert(0, "2400E-6")
  lam_mid_Label.grid(row=0, column=0)
  lam_mid_input.grid(row=0, column=1)
  
  delta_lamda_entry = tk.Frame(master=window)
  delta_lamda_Label = tk.Label(master=delta_lamda_entry, text="Beam wavelength range(mm)=",font=(font_name,font_size))
  delta_lamda_input = tk.Entry(master=delta_lamda_entry, width=10,font=(font_name,font_size))
  delta_lamda_input.insert(0, "250E-6")
  delta_lamda_Label.grid(row=0, column=0)
  delta_lamda_input.grid(row=0, column=1)
  
  number_of_rays_entry = tk.Frame(master=window)
  number_of_rays_Label = tk.Label(master=number_of_rays_entry, text="Number of rays=",font=(font_name,font_size))
  number_of_rays_input = tk.Entry(master=number_of_rays_entry, width=10,font=(font_name,font_size))
  number_of_rays_input.insert(0, "20")
  number_of_rays_Label.grid(row=0, column=0)
  number_of_rays_input.grid(row=0, column=1)
  
  safety_to_StripeM_entry = tk.Frame(master=window)
  safety_to_StripeM_Label = tk.Label(master=safety_to_StripeM_entry, text="Distance of incoming beams to Convex mirror(mm)=",font=(font_name,font_size))
  safety_to_StripeM_input = tk.Entry(master=safety_to_StripeM_entry, width=10,font=(font_name,font_size))
  safety_to_StripeM_input.insert(0, "5")
  safety_to_StripeM_Label.grid(row=0, column=0)
  safety_to_StripeM_input.grid(row=0, column=1)
  
  periscope_distance_entry = tk.Frame(master=window)
  periscope_distance_Label = tk.Label(master=periscope_distance_entry, text="periscope distance(mm)=",font=(font_name,font_size))
  periscope_distance_input = tk.Entry(master=periscope_distance_entry, width=10,font=(font_name,font_size))
  periscope_distance_input.insert(0, "8")
  periscope_distance_Label.grid(row=0, column=0)
  periscope_distance_input.grid(row=0, column=1)

  btn_convert = tk.Button(
      master=window,
      text="build stretcher",
      command=build_stretcher,font=(font_name,font_size)
  )
  
  R_entry.pack()
  concav_aperture_entry.pack()
  h_StripeM_entry.pack()
  gamma_entry.pack()
  grat_const_entry.pack()
  seperation_entry.pack()
  lam_mid_entry.pack()
  delta_lamda_entry.pack()
  number_of_rays_entry.pack()
  safety_to_StripeM_entry.pack()
  periscope_distance_entry.pack()
  
  btn_convert.pack()
  
  window.mainloop()
  
# telescope_GUI()