# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 14:57:21 2025

@author: mens
"""

from LaserCAD.basic_optics.off_axis_parabola import Off_Axis_Parabola_Focus
# from LaserCAD.basic_optics.off_axis_parabola import Off_Axis_Parabola_Colim
from LaserCAD.basic_optics.beam import SquareBeam
from LaserCAD.basic_optics import Composition, Ray, Mirror
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
import numpy as np

if freecad_da:
  clear_doc()

# =============================================================================
# focus
# =============================================================================

# oapf = Off_Axis_Parabola_Focus(angle=45)
# oapf = Off_Axis_Parabola_Focus(angle=90)

# sb = SquareBeam(radius=5, ray_in_line=3)


# comp = Composition()
# comp.set_light_source(sb)
# comp.propagate(50)
# comp.add_on_axis(oapf)
# oapf.rotate(vec=oapf.normal, phi=np.pi)
# comp.recompute_optical_axis()
# comp.propagate(150)


# comp.draw()



# =============================================================================
# another geom
# =============================================================================
# comp = Composition()
# comp.normal = (1,2,0)
# comp.set_light_source(SquareBeam(radius=5, ray_in_line=3))
# comp.propagate(60)
# comp.add_on_axis(Off_Axis_Parabola_Focus())
# comp.propagate(100)
# comp.draw()


# # =============================================================================
# # backreflection, oap2 twice
# # =============================================================================
# comp = Composition()
# comp.normal = (1,2,0)
# comp.set_light_source(SquareBeam(radius=5, ray_in_line=3))
# comp.propagate(60)
# oap = Off_Axis_Parabola_Focus()
# comp.add_on_axis(oap)
# comp.propagate(oap.reflected_focal_length)
# comp.add_on_axis(Mirror())
# comp.set_sequence([0,1,0])
# comp.recompute_optical_axis()
# comp.propagate(100)
# comp.draw()

# ### AHA!


# # =============================================================================
# # rect ray 1
# # =============================================================================
# ray0 = Ray()
# ray0.pos += (-50, 0, 0)
# oap1 = Off_Axis_Parabola_Focus()
# ray1 = oap1.next_ray(ray0)

# ray2 = Ray()
# ray2.pos = ray1.endpoint()
# ray2.set_axes(ray1.get_axes())
# ray2.normal *= -1

# ray3 = oap1.next_ray(ray2)

# oap1.draw()
# ray0.draw()
# ray1.draw()
# ray2.draw()
# ray3.draw()

# # =============================================================================
# # rect ray
# # =============================================================================

# ray0 = Ray()
# ray0.pos += (-50, 0, 0)
# oap1 = Off_Axis_Parabola_Focus()
# ray1 = oap1.next_ray(ray0)
# oap2 = Off_Axis_Parabola_Focus()
# oap2.pos += (0, 2*oap1.reflected_focal_length, 0)
# oap2.rotate(vec=oap2.normal, phi=np.pi)
# ray2 = oap2.next_ray(ray1)

# =============================================================================
# telescope
# =============================================================================

oapf = Off_Axis_Parabola_Focus()

oap2 = Off_Axis_Parabola_Focus()


sb = SquareBeam(radius=5, ray_in_line=5)


comp2 = Composition()
comp2.set_light_source(sb)
comp2.propagate(50)
comp2.add_on_axis(oapf)
# comp2.propagate(oapf.reflected_focal_length)
comp2.propagate(2*oapf.reflected_focal_length)
comp2.add_on_axis(oap2)
oap2.set_axes(oapf.get_axes())
oap2.rotate(oap2.normal, np.pi)
comp2.recompute_optical_axis()

comp2.propagate(120)

comp2.draw()
# comp2.draw_beams()




if freecad_da:
  setview()