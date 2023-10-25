# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:15:19 2023

@author: He
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
from LaserCAD.basic_optics import Geom_Object,Lens
from LaserCAD.freecad_models import clear_doc, freecad_da

import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
import tkinter as tk

def GUI(path=""):
  global comp, element_list,ls

  comp = Composition()
  ls=Beam()
  element_list =[]
  element_prop = []
  font_size = 14
  font_name = "Times New Roman"
  
  def set_germ(obj=Geom_Object(),tl=None):
    geomWindow = tk.Toplevel(tl)
    geomWindow.title = ("Geomery setting")
    title = tk.Label(geomWindow,text=str(obj),font=(font_name,font_size))
    pos_entry = tk.Frame(master=geomWindow)
    pos_Label = tk.Label(master=pos_entry,text="position(mm):",font=(font_name,font_size))
    pos_input = tk.Entry(master=pos_entry,width=10,font=(font_name,font_size))
    pos_input.insert(0, "(0,0,80)")
    pos_Label.grid(row=0, column=0)
    pos_input.grid(row=0, column=1)
    
    normal_entry = tk.Frame(master=geomWindow)
    normal_Label = tk.Label(master=normal_entry,text="direction:",font=(font_name,font_size))
    normal_input = tk.Entry(master=normal_entry,width=10,font=(font_name,font_size))
    normal_input.insert(0, "(1,0,0)")
    normal_Label.grid(row=0, column=0)
    normal_input.grid(row=0, column=1)
    
    def complete_geom_setting():
      p1=pos_input.get().find(",")
      p2=pos_input.get().rfind(",")
      px=float(pos_input.get()[1:p1])
      py=float(pos_input.get()[p1+1:p2])
      pz=float(pos_input.get()[p2+1:-1])
      obj.pos=np.array((px,py,pz))
      p1=normal_input.get().find(",")
      p2=normal_input.get().rfind(",")
      nx=float(normal_input.get()[1:p1])
      ny=float(normal_input.get()[p1+1:p2])
      nz=float(normal_input.get()[p2+1:-1])
      obj.normal=np.array((nx,ny,nz))
      geomWindow.destroy()
    btn = tk.Button(
        master=geomWindow,
        text="complete setting",
        command=complete_geom_setting,
        font=(font_name,font_size)
    )
    title.pack()
    pos_entry.pack()
    normal_entry.pack()
    btn.pack()
    
  def set_geom_on_axis(obj=Geom_Object(),tl=None,phi=0,theta=0):
    axisWindow = tk.Toplevel(tl)
    axisWindow.title = ("add on axis")
    title = tk.Label(axisWindow,text=str(obj),font=(font_name,font_size))
    prop_entry = tk.Frame(axisWindow)
    prop_Label = tk.Label(master=prop_entry,text="propagation length before last elements(mm):",font=(font_name,font_size))
    prop_input = tk.Entry(master=prop_entry,width=10,font=(font_name,font_size))
    prop_input.insert(0, "100")
    prop_Label.grid(row=0, column=0)
    prop_input.grid(row=0, column=1)
    def complete_setting():
      global comp,ls
      new_ele =deepcopy(obj)
      element_list.append(new_ele)
      if type(element_list[-1])==Mirror:
        element_list[-1]=Mirror(phi=phi,theta=theta)
      element_prop.append(float(prop_input.get()))
      if freecad_da:
        clear_doc()
      L1.config(text = "A new element has been added at the end of composition.")
      comp=Composition()
      comp.set_light_source(ls)
      for ele in range(len(element_list)):
        comp.propagate(element_prop[ele])
        comp.add_on_axis(element_list[ele])
      comp.propagate(50)
      comp.draw()
      axisWindow.destroy()
      tl.destroy()
    btn = tk.Button(
        master=axisWindow,
        text="complete setting and add the element",
        command=complete_setting,
        font=(font_name,font_size)
    )
    title.pack()
    prop_entry.pack()
    btn.pack()
    
  def open_ls_window():
    if freecad_da:
      clear_doc()
    lsWindow = tk.Toplevel(window)
    lsWindow.title = ("light source setting")
    # lsWindow.geometry("400*400")
    title=tk.Label(lsWindow,text ="This is the light source setting window. Please enter some basic parameters about light source.",font=(font_name,font_size))
    radius_entry = tk.Frame(master=lsWindow)
    radius_Label = tk.Label(master=radius_entry, text="beam radius(mm)=",font=(font_name,font_size))
    radius_input = tk.Entry(master=radius_entry,width=10,font=(font_name,font_size))
    radius_input.insert(0,"1")
    radius_Label.grid(row=0, column=0)
    radius_input.grid(row=0, column=1)
    
    angle_entry = tk.Frame(master=lsWindow)
    angle_Label = tk.Label(master=angle_entry, text="beam divergence angle(mm)=",font=(font_name,font_size))
    angle_input = tk.Entry(master=angle_entry,width=10,font=(font_name,font_size))
    angle_input.insert(0, "0")
    angle_Label.grid(row=0, column=0)
    angle_input.grid(row=0, column=1)
    
    lamda_entry = tk.Frame(master=lsWindow)
    lamda_Label = tk.Label(master=lamda_entry, text="beam wavelength(mm)=",font=(font_name,font_size))
    lamda_input = tk.Entry(master=lamda_entry,width=10,font=(font_name,font_size))
    lamda_input.insert(0, "1030E-6")
    lamda_Label.grid(row=0, column=0)
    lamda_input.grid(row=0, column=1)
    
    distribution_entry = tk.Frame(master=lsWindow)
    distribution_Label = tk.Label(master=distribution_entry, text="The distribution of beam:",font=(font_name,font_size))
    distribution = "cone"
    distribution_Label.grid(row=0, column=0)
    def distribution_select():
      site_list = {1:"cone",2:"square",3:"circular",4:"Gaussian"}
      global distribution
      distribution = site_list.get(v.get())
    site = [("cone",1),("square",2),("circular",3),("Gaussian",4)]
    v =tk.IntVar()
    for name, num in site:
      radio_button = tk.Radiobutton(distribution_entry,text=name,variable=v,value=num,command=distribution_select,font=(font_name,font_size))
      radio_button.grid(row=num+1,column=0)
    def setting_geom():
      set_germ(obj=comp,tl=lsWindow)
    btn_geom = tk.Button(
        master=lsWindow,
        text="Setting the Geometric Parameters",
        command=setting_geom,
        font=(font_name,font_size)
    )
  
    def complete_ls_setting():
      radi = float(radius_input.get())
      ang = float(angle_input.get())
      lamda = float(lamda_input.get())
      # distribution = str(distribution_input.get())
      global distribution,ls
      ls = Beam( radius=radi, angle=ang, name="NewBeam",wavelength=lamda, distribution=distribution)
      comp.set_light_source(ls)
      # if freecad_da:
      #   clear_doc()
      # comp.draw()
      L1.config(text = "The light source is set.")
      lsWindow.destroy()
    btn_convert = tk.Button(
        master=lsWindow,
        text="complete setting",
        command=complete_ls_setting
        ,font=(font_name,font_size)
    )
    title.grid(row=1, column=0, padx=10)
    radius_entry.grid(row=2, column=0, padx=10)
    angle_entry.grid(row=3, column=0, padx=10)
    lamda_entry.grid(row=4, column=0, padx=10)
    distribution_entry.grid(row=5, column=0, padx=10)
    btn_geom.grid(row=6, column=0, padx=10)
    btn_convert.grid(row=7, column=0, padx=10)
    lsWindow.rowconfigure([0,1,2,3,4,5,6,7],weight=1, minsize=30)
    lsWindow.columnconfigure([0,1],weight=1, minsize=30)
  
  def open_lens_window():
    lensWindow = tk.Toplevel(window)
    lensWindow.title = ("add a lens")
    title=tk.Label(lensWindow,text ="This is the lens setting window. Please enter some basic parameters about lens.",font=(font_name,font_size))
    f_entry = tk.Frame(master=lensWindow)
    f_Label = tk.Label(master=f_entry, text="focal length(mm)=",font=(font_name,font_size))
    f_input = tk.Entry(master=f_entry,width=10,font=(font_name,font_size))
    f_input.insert(0,"100")
    f_Label.grid(row=0, column=0)
    f_input.grid(row=0, column=1)
    
    aper_entry = tk.Frame(master=lensWindow)
    aper_Label = tk.Label(master=aper_entry, text="lens aperture(mm)=",font=(font_name,font_size))
    aper_input = tk.Entry(master=aper_entry,width=10,font=(font_name,font_size))
    aper_input.insert(0, "25.4")
    aper_Label.grid(row=0, column=0)
    aper_input.grid(row=0, column=1)
    
    l_new= Lens()
  
    def complete_lens_setting():
      global comp,ls
      l_new.focal_length = float(f_input.get())
      l_new.aperture = float(aper_input.get())
      new_ele =deepcopy(l_new)
      element_list.append(new_ele)
      comp.add_fixed_elm(element_list[-1])
      comp.propagate(50)
      if freecad_da:
        clear_doc()
      L1.config(text = "A new Lens has been added.")
      comp=Composition()
      comp.set_light_source(ls)
      for ele in element_list:
        comp.add_fixed_elm(ele)
      comp.propagate(50)
      comp.draw()
      lensWindow.destroy()
    btn_convert = tk.Button(
        master=lensWindow,
        text="complete setting",
        command=complete_lens_setting,font=(font_name,font_size)
    )
  
    def setting_geom():
      set_germ(obj=l_new,tl=lensWindow)
    btn_geom = tk.Button(
        master=lensWindow,
        text="Setting the Geometric Parameters",
        command=setting_geom,font=(font_name,font_size)
    )
    
    def setting_geom_on_axis():
      set_geom_on_axis(obj=l_new,tl=lensWindow)
    btn_geom_on_axis = tk.Button(
        master=lensWindow,
        text="Setting the Geometric Parameters by adding is on axis",
        command=setting_geom_on_axis,font=(font_name,font_size)
    )
    
    title.pack()
    f_entry.pack()
    aper_entry.pack()
    btn_geom.pack()
    btn_convert.pack()
    btn_geom_on_axis.pack()
  
  def open_mirror_window():
    mirrorWindow = tk.Toplevel(window)
    mirrorWindow.title = ("add a new mirror")
    title=tk.Label(mirrorWindow,text ="This is the mirror setting window. Please enter some basic parameters about mirror.",font=(font_name,font_size))
    
    aper_entry = tk.Frame(master=mirrorWindow)
    aper_Label = tk.Label(master=aper_entry, text="lens aperture(mm)=",font=(font_name,font_size))
    aper_input = tk.Entry(master=aper_entry,width=10,font=(font_name,font_size))
    aper_input.insert(0, "25.4")
    aper_Label.grid(row=0, column=0)
    aper_input.grid(row=0, column=1)
    
    theta_entry = tk.Frame(mirrorWindow)
    theta_Label = tk.Label(master=theta_entry,text="theta=",font=(font_name,font_size))
    theta_input = tk.Entry(master=theta_entry,width=10,font=(font_name,font_size))
    theta_input.insert(0, "0")
    theta_Label.grid(row=0, column=0)
    theta_input.grid(row=0, column=1)
    
    phi_entry = tk.Frame(mirrorWindow)
    phi_Label = tk.Label(master=phi_entry,text="phi=",font=(font_name,font_size))
    phi_input = tk.Entry(master=phi_entry,width=10,font=(font_name,font_size))
    phi_input.insert(0, "180")
    phi_Label.grid(row=0, column=0)
    phi_input.grid(row=0, column=1)
    
    m_new= Mirror(phi=float(phi_input.get()),theta=float(theta_input.get()))
    
    type_entry = tk.Frame(master=mirrorWindow)
    type_Label = tk.Label(master=type_entry, text="Mirror type:",font=(font_name,font_size))
    # Mtype = "Plane"
    type_Label.grid(row=0, column=0)
    def type_select():
      site_list = {1:"Plane Mirror",2:"Curved Mirror",3:"Cylindrical Mirror"}
      global m_new
      Mtype = site_list.get(v.get())
      if Mtype=="Plane Mirror":
        m_new = Mirror(phi=float(phi_input.get()),theta=float(theta_input.get()))
      elif Mtype=="Curved Mirror":
        m_new = Curved_Mirror()
      else:
        m_new = Cylindrical_Mirror()
    site = [("Plane Mirror",1),("Curved Mirror",2),("Cylindrical Mirror",3)]
    v =tk.IntVar()
    for name, num in site:
      radio_button = tk.Radiobutton(type_entry,text=name,variable=v,value=num,command=type_select,font=(font_name,font_size))
      radio_button.grid(row=num+1,column=0)
    def setting_geom():
      set_germ(obj=m_new,tl=mirrorWindow)
    btn_geom = tk.Button(
        master=mirrorWindow,
        text="Setting the Geometric Parameters",
        command=setting_geom,font=(font_name,font_size)
    )
    def setting_geom_on_axis():
      set_geom_on_axis(obj=m_new,tl=mirrorWindow,phi=float(phi_input.get()),theta=float(theta_input.get()))
    btn_geom_on_axis = tk.Button(
        master=mirrorWindow,
        text="Setting the Geometric Parameters by adding is on axis",
        command=setting_geom_on_axis,font=(font_name,font_size)
    )
    def complete_mirror_setting():
      global comp,ls
      m_new.aperture=float(aper_input.get())
      element_list.append(deepcopy(m_new))
      comp.add_fixed_elm(element_list[-1])
      comp.propagate(50)
      if freecad_da:
        clear_doc()
      L1.config(text = "A new Mirror has been added.")
      comp=Composition()
      comp.set_light_source(ls)
      for ele in element_list:
        comp.add_fixed_elm(ele)
      comp.propagate(50)
      comp.draw()
      mirrorWindow.destroy()
    btn_convert = tk.Button(
        master=mirrorWindow,
        text="complete setting",
        command=complete_mirror_setting,font=(font_name,font_size)
    )
  
    title.grid(row=0, column=0, padx=10)
    aper_entry.grid(row=1, column=0, padx=10)
    phi_entry.grid(row=2, column=0, padx=10)
    theta_entry.grid(row=3, column=0, padx=10)
    type_entry.grid(row=4, column=0, padx=10)
    btn_geom.grid(row=5, column=0, padx=10)
    btn_convert.grid(row=6, column=0, padx=10)
    btn_geom_on_axis.grid(row=7, column=0, padx=10)
    mirrorWindow.rowconfigure([0,1,2,3,4,5,6,7],weight=1, minsize=30)
    mirrorWindow.columnconfigure([0,1],weight=1, minsize=30)
  
  def open_ip_window():
    ipWindow = tk.Toplevel(window)
    ipWindow.title = ("add a grating")
    title=tk.Label(ipWindow,text ="This is the grating setting window. Please set the geomery parameters, then choose the beam you want to project.",font=(font_name,font_size))
    global comp,ls,element_list
    name_list=[i.name for i in comp._beams]
    elelist = tk.Listbox(ipWindow, selectmode = "single",width=50, font=(font_name,font_size))
    for each_item in range(len(name_list)):
      elelist.insert(each_item, name_list[each_item])
    
    ip_new = Intersection_plane()
  
    def complete_ip_setting():
      global comp,ls
      if freecad_da:
        clear_doc()
      comp=Composition()
      comp.set_light_source(ls)
      for ele in element_list:
        comp.add_fixed_elm(ele)
      comp.propagate(50)
      comp.draw()
      ipWindow.destroy()
    btn_convert = tk.Button(
        master=ipWindow,
        text="close",
        command=complete_ip_setting,font=(font_name,font_size)
    )
    def setting_geom():
      set_germ(obj=ip_new,tl=ipWindow)
    btn_geom = tk.Button(
        master=ipWindow,
        text="Setting the Geometric Parameters",
        command=setting_geom,font=(font_name,font_size)
    )
    def draw_spot_diagram():
      x = list(elelist.curselection())
      new_ele =deepcopy(ip_new)
      global comp
      if freecad_da:
        clear_doc()
      comp=Composition()
      comp.set_light_source(ls)
      for ele in element_list:
        comp.add_fixed_elm(ele)
      comp.propagate(50)
      comp.draw()
      new_ele.draw()
      
      for i in x:  
        new_ele.spot_diagram(comp._beams[i])
    btn_draw = tk.Button(
        master=ipWindow,
        text="draw the spot diagram",
        command=draw_spot_diagram,font=(font_name,font_size)
    )
    def close_spot_diagram():
      plt.close("all")
    btn_close = tk.Button(
        master=ipWindow,
        text="close the spot diagram",
        command=close_spot_diagram,font=(font_name,font_size)
    )
    title.pack()
    btn_geom.pack()
    elelist.pack()
    btn_draw.pack()
    btn_close.pack()
    btn_convert.pack()
  
  def open_grating_window():
    gratingWindow = tk.Toplevel(window)
    gratingWindow.title = ("add a grating")
    title=tk.Label(gratingWindow,text ="This is the grating setting window. Please enter some basic parameters about grating.",font=(font_name,font_size))
    grat_const_entry = tk.Frame(master=gratingWindow)
    grat_const_Label = tk.Label(master=grat_const_entry, text="Grating constent(mm)=",font=(font_name,font_size))
    grat_const_input = tk.Entry(master=grat_const_entry,width=10,font=(font_name,font_size))
    grat_const_input.insert(0,"0.005")
    grat_const_Label.grid(row=0, column=0)
    grat_const_input.grid(row=0, column=1)
    
    g_new= Grating()
  
    def complete_grat_setting():
      global comp,ls
      g_new.grating_constant = float(grat_const_input.get())
      new_ele =deepcopy(g_new)
      element_list.append(new_ele)
      comp.add_fixed_elm(element_list[-1])
      comp.propagate(50)
      if freecad_da:
        clear_doc()
      L1.config(text = "A new Grating has been added.")
      comp=Composition()
      comp.set_light_source(ls)
      for ele in element_list:
        comp.add_fixed_elm(ele)
      comp.propagate(50)
      comp.draw()
      gratingWindow.destroy()
    btn_convert = tk.Button(
        master=gratingWindow,
        text="complete setting",
        command=complete_grat_setting,font=(font_name,font_size)
    )
  
    def setting_geom():
      set_germ(obj=g_new,tl=gratingWindow)
    btn_geom = tk.Button(
        master=gratingWindow,
        text="Setting the Geometric Parameters",
        command=setting_geom,font=(font_name,font_size)
    )
    def setting_geom_on_axis():
      set_geom_on_axis(obj=g_new,tl=gratingWindow)
    btn_geom_on_axis = tk.Button(
        master=gratingWindow,
        text="Setting the Geometric Parameters by adding is on axis",
        command=setting_geom_on_axis,font=(font_name,font_size)
    )
    title.pack()
    grat_const_entry.pack()
    btn_geom.pack()
    btn_convert.pack()
    btn_geom_on_axis.pack()
  
  window =tk.Tk()
  window.title("FreeCAD GUI")
  window.resizable(width=True, height=True)
  
  btn_ls = tk.Button(
      master=window,
      text="set light source",
      command=open_ls_window,font=(font_name,font_size)
  )
  
  btn_lens = tk.Button(
      master=window,
      text="add a lens",
      command=open_lens_window,font=(font_name,font_size)
  )
  
  btn_mirror = tk.Button(
      master=window,
      text="add a mirror",
      command=open_mirror_window,font=(font_name,font_size)
  )
  
  btn_grating = tk.Button(
      master=window,
      text="add a grating",
      command=open_grating_window,font=(font_name,font_size)
  )
  
  btn_ip = tk.Button(
      master=window,
      text="set a Intersection plane",
      command=open_ip_window,font=(font_name,font_size)
  )
  
  def delete_elements():
    deleteWindow = tk.Toplevel(window)
    deleteWindow.title = ("Delete setting")
    title = tk.Label(deleteWindow,text="please select the elements you want to delete:",font=(font_name,font_size))
    global comp,ls,element_list
    name_list=[i.name for i in element_list]
    elelist = tk.Listbox(deleteWindow, selectmode = "multiple",width=50, font=(font_name,font_size))
    for each_item in range(len(name_list)):
      elelist.insert(each_item, name_list[each_item])
    def complete_delete_setting():
      global comp,ls,element_list
      x = list(elelist.curselection())
      # print(x)
      element_list1=[]
      for i in range(len(element_list)):
        if not i in x:
          element_list1.append(element_list[i])
      element_list = element_list1
      # for i in x:
      #   element_list.pop(i)
      if freecad_da:
        clear_doc()
      
      comp=Composition()
      comp.set_light_source(ls)
      for ele in element_list:
        comp.add_fixed_elm(ele)
      comp.propagate(50)
      comp.draw()
      deleteWindow.destroy()
    btn_fin = tk.Button(
        master=deleteWindow,
        text="complete setting",
        command=complete_delete_setting,font=(font_name,font_size)
    )
    
    title.grid(row=0, column=0, padx=10)
    elelist.grid(row=1, column=0, padx=10)
    btn_fin.grid(row=2, column=0, padx=10)
    deleteWindow.rowconfigure([0,1,2],weight=1, minsize=50)
    deleteWindow.columnconfigure([0],weight=1, minsize=300)
  btn_delete = tk.Button(
      master=window,
      text="detele elements",
      command=delete_elements,font=(font_name,font_size)
  )
  
  def clear_settings():
    if freecad_da:
      clear_doc()
    global comp,ls,element_list
    comp=Composition()
    ls=Beam()
    element_list=[]
  btn_clear = tk.Button(
      master=window,
      text="clear all settings",
      command=clear_settings,font=(font_name,font_size)
  )
  
  L1 = tk.Label(window,text="This is the FreeCAD user interface. Please set up the light source first, and then add the optical elements you want",font=(font_name,font_size))
  def coading():
    fp = open(path+'/samples.py', 'w+')
    fp.truncate(0)
    myself = open(__file__,"r")
    line = myself.readlines()
    for i in range(23):
      fp.write(line[i])
    myself.close()
    global comp,ls,element_list
    ele_count=0
    for ele in element_list:
      fp.write("a"+str(ele_count)+"="+str(ele)[3:]+"\n")
      if type(ele)==Mirror:
        fp.write("a"+str(ele_count)+".normal=("+str(ele.normal[0])+","+str(ele.normal[1])+","+str(ele.normal[2])+")\n")
      ele_count+=1
    fp.write("ls="+str(ls)[3:]+"\n")
    fp.write("comp="+str(comp)[3:]+"\n")
    fp.write("comp.set_light_source(ls)\n")
    for ele in range(len(element_list)):
      fp.write("comp.add_fixed_elm(a"+str(ele)+")\n")
    fp.write("comp.draw()")
    L1.config(text = "code generated. Saved as 'sample.py'.")
    fp.close()
  btn_coading = tk.Button(
      master=window,
      text="Generate Code",
      command=coading,font=(font_name,font_size)
  )
  btn_ls.grid(row=1, column=0, padx=10)
  btn_lens.grid(row=2, column=0, padx=10)
  btn_mirror.grid(row=3, column=0, padx=10)
  btn_grating.grid(row=4, column=0, padx=10)
  btn_ip.grid(row=5, column=0, padx=10)
  btn_delete.grid(row=6, column=0, padx=10)
  btn_clear.grid(row=7, column=0, padx=10)
  btn_coading.grid(row=8, column=0, padx=10)
  L1.grid(row=9,column=0,padx=10)
  window.rowconfigure([0,1,2,3,4,5,6,7,8,9],weight=1, minsize=50)
  window.columnconfigure([0],weight=1, minsize=300)
  window.mainloop()

if __name__ == "__main__":
  GUI()