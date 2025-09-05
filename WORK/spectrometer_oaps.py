#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  8 09:15:24 2025

@author: mens
"""

from LaserCAD.basic_optics import Beam, Lens, Off_Axis_Parabola, Mirror, Composition, inch, Geom_Object
from LaserCAD.non_interactings import Crystal
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
from LaserCAD.freecad_models.utils import thisfolder, load_STL
import numpy as np




cooling_rod_file = thisfolder+"misc_meshes/Cooling_Rod.stl"
chamber_file = thisfolder+"misc_meshes/Vacuum_Chamber.stl"

cool_rod = Geom_Object()
cool_rod.freecad_model = load_STL
cool_rod.draw_dict["stl_file"]=cooling_rod_file
cool_rod.draw_dict["color"] = (0.6, 0.2, 0.1)
cool_rod.pos = (0,0,0)


chamber = thisfolder+"misc_meshes/Cooling_Rod.stl"

chamber = Geom_Object()
chamber.freecad_model = load_STL
chamber.draw_dict["stl_file"] = chamber_file
chamber.draw_dict["transparency"] = 90
chamber.pos = (0,0,0)


if freecad_da:
  clear_doc()
  

fiber1 = Beam(radius=0.025, angle=0.18)

white_light_focus = 100
teles_lens1 = Lens(f=white_light_focus, name="WhiteTeles1")
teles_lens1.aperture = 2*inch
# teles_lens1.set_mount_to_default()

teles_lens2 = Lens(f=white_light_focus, name="WhiteTeles2")
teles_lens2.aperture = 2*inch
# teles_lens2.set_mount_to_default()

teles_mirror = Mirror(phi=90)
teles_mirror.aperture = 2*inch
# teles_mirror.set_mount_to_default()
  
oap_focus = 2*inch
oap_colim = Off_Axis_Parabola(colim=True, reflected_focal_length=oap_focus, name="ColimOAP")
oap_fibre = Off_Axis_Parabola(colim=False, reflected_focal_length=oap_focus, name="FocusOAP", theta=180)

crystal = Crystal(width=6, height=6, thickness=2, name="Sample")

spectro = Composition(name="Spectro")
spectro.set_light_source(fiber1)
spectro.propagate(white_light_focus*1)
spectro.add_on_axis(teles_lens1)
spectro.propagate(white_light_focus*1)
spectro.add_on_axis(teles_mirror)
spectro.propagate(white_light_focus*1)
spectro.add_on_axis(teles_lens2)
spectro.propagate(white_light_focus*1)
spectro.add_on_axis(crystal)
spectro.propagate(oap_focus)
spectro.add_on_axis(oap_colim)
spectro.propagate(180)
spectro.add_on_axis(oap_fibre)
spectro.propagate(oap_focus)

spectro.rotate(vec=(0,0,1), phi=np.pi/2)
spectro.pos = (200, 57-210, 110)
# spectro.pos = crystal.pos

# =============================================================================
# pump_fibre setup
# =============================================================================
pump_fibre = Beam(radius=0.025, angle=0.15)
pump_fibre.draw_dict["color"] = (0.05, 0.0, 0.9)

pump_focal = 100
pump_teles_lens1 = Lens(f=pump_focal, name="PumpLensColim")
pump_teles_lens1.aperture = 2*inch

pump_teles_lens2 = Lens(f=pump_focal, name="PumpLensCoFocus")
pump_teles_lens2.aperture = 2*inch

pump_teles_mirror = Mirror(phi=-95)
pump_teles_mirror.aperture = 2*inch

pump_comp = Composition(name="PumpLine")
pump_comp.set_light_source(pump_fibre)
pump_comp.set_geom(crystal.get_geom())
pump_comp.rotate(vec=(0,0,1), phi=30*np.pi/180)
pump_comp.propagate(pump_focal)
pump_comp.add_on_axis(pump_teles_lens2)
pump_comp.propagate(pump_focal)
pump_comp.add_on_axis(pump_teles_mirror)
pump_comp.propagate(pump_focal)
pump_comp.add_on_axis(pump_teles_lens1)
pump_comp.propagate(pump_focal)



# =============================================================================
# draw selesction
# =============================================================================

cool_rod.draw()
chamber.draw()

spectro.draw()
pump_comp.draw()

if freecad_da:
  setview()