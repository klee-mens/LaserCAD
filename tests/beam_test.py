# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 16:14:45 2024

@author: 12816
"""

from LaserCAD.basic_optics import Mirror,Beam,Cylindrical_Mirror,Grating,Ray
from LaserCAD.basic_optics import Intersection_plane,Cylindrical_Mirror1
from LaserCAD.basic_optics import Curved_Mirror, Composition,Rainbow,Lens

from LaserCAD.basic_optics import Unit_Mount,Composed_Mount,Gaussian_Beam
from LaserCAD.non_interactings import Pockels_Cell
from LaserCAD.non_interactings import Lambda_Plate

from LaserCAD.freecad_models import clear_doc, setview, add_to_composition
from LaserCAD.freecad_models import freecad_da
from LaserCAD.moduls import Make_RoofTop_Mirror, Make_Periscope
from LaserCAD.moduls.periscope import Rooftop_Mirror_Component

if freecad_da:
  clear_doc()

r = Ray()
r.draw()
b = Beam()
b.pos += (0,50,0)
b.draw()
gb = Gaussian_Beam(radius=5,angle=-0.05,wavelength=1E-1)
gb.pos += (0,100,0)
gb.draw()

b1 = Beam(ray_count = 6)
b1.pos -= (0,50,0)
b1.draw_dict["model"] = "ray_group"
b1.draw()