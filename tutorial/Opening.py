#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:19:05 2024

@author: mens
"""

import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)


from LaserCAD.basic_optics import Mirror, Curved_Mirror, Lens, Beam, Ray, Gaussian_Beam, LinearResonator, Composition
from LaserCAD.freecad_models import freecad_da, clear_doc, setview


if freecad_da:
  clear_doc()
  
linres = LinearResonator(name="MasterOscillatores")

linres.add_on_axis(Mirror())
linres.propagate(330)
linres.add_on_axis(Curved_Mirror(radius=600, phi = 180+13))
linres.propagate(250)
linres.add_on_axis(Mirror(phi=90))
linres.propagate(80)
linres.add_on_axis(Mirror(phi=90))
linres.propagate(250)
linres.add_on_axis(Mirror())


beam_out = linres.output_beam()
beam_out = beam_out.transform_to_cone_beam()
# beam_out.set_length(400)
beam_out.draw()

comp = Composition("FancyBeamLine")
comp.set_geom(beam_out.get_geom())
comp.set_light_source(beam_out)
comp.propagate(400)
comp.add_on_axis(Mirror(phi=120))
comp.propagate(150)
comp.add_on_axis(Lens(f=40))
comp.propagate(40 + 400)
comp.add_on_axis(Lens(f=400))
comp.propagate(60)

comp.draw()



# linres.compute_eigenmode()
linres.draw()  
if freecad_da:
  setview()