# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 14:57:21 2025

@author: mens
"""

# from LaserCAD.basic_optics.off_axis_parabola import Off_Axis_Parabola
# from LaserCAD.basic_optics.off_axis_parabola import Off_Axis_Parabola_Colim
from LaserCAD.basic_optics.beam import SquareBeam, Beam
from LaserCAD.basic_optics import Composition, Ray, Mirror, Off_Axis_Parabola, inch
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
import numpy as np

if freecad_da:
  clear_doc()

# =============================================================================
# focus 90
# =============================================================================
oapf = Off_Axis_Parabola(angle=90)

sb = SquareBeam(radius=5, ray_in_line=3)


comp1 = Composition(name="Simple 90")
comp1.set_light_source(sb)
comp1.propagate(50)
comp1.add_on_axis(oapf)
oapf.rotate(vec=oapf.normal, phi=np.pi)
comp1.recompute_optical_axis()
comp1.propagate(150)

comp1.draw()

# =============================================================================
# focus 45
# =============================================================================
oapf = Off_Axis_Parabola(angle=45)

sb = SquareBeam(radius=5, ray_in_line=3)


comp3 = Composition(name="Simple 45")
comp3.set_light_source(sb)
comp3.propagate(50)
comp3.add_on_axis(oapf)
oapf.rotate(vec=oapf.normal, phi=np.pi)
comp3.recompute_optical_axis()
comp3.propagate(150)

comp3.pos += (50, -100, 0)
comp3.draw()


# # # =============================================================================
# # # backreflection, oap2 twice
# # # =============================================================================
comp2 = Composition(name="BackRefelction")
comp2.normal = (1,2,0)
comp2.set_light_source(SquareBeam(radius=5, ray_in_line=3))
comp2.propagate(60)
oap = Off_Axis_Parabola()
comp2.add_on_axis(oap)
comp2.propagate(oap.reflected_focal_length)
comp2.add_on_axis(Mirror())
comp2.set_sequence([0,1,0])
comp2.recompute_optical_axis()
comp2.propagate(100)

comp2.pos += (0, 100, 0)
comp2.draw()


# =============================================================================
# telescope
# =============================================================================

focal = 3*inch

oapf = Off_Axis_Parabola(theta=180, reflected_focal_length=focal)
oap2 = Off_Axis_Parabola(colim=True, theta=0, reflected_focal_length=focal)

sb = SquareBeam(radius=5, ray_in_line=5)

comp4 = Composition(name="Telescope")
comp4.set_light_source(sb)
comp4.propagate(2*focal)
comp4.add_on_axis(oapf)
comp4.propagate(2*oapf.reflected_focal_length)
comp4.add_on_axis(oap2)
comp4.propagate(120)

comp4.pos += (200, -50, 0)
comp4.draw()


# =============================================================================
# 2 inch 45, normal beam
# =============================================================================

focal = 3*inch
aperture = 2*inch
oap2 = Off_Axis_Parabola(reflected_focal_length=focal, angle=45)
oap2.aperture = aperture

comp5 = Composition(name="Big 2inch")
comp5.set_light_source(Beam(radius=20, angle=0.0))
comp5.propagate(80)
comp5.add_on_axis(oap2)
comp5.propagate(2*focal)

comp5.pos += (200, 100, 0)
comp5.draw()


# =============================================================================
# 0.5 inch 90, normal beam
# =============================================================================

focal = 2*inch
aperture = 0.5*inch
oap1k2 = Off_Axis_Parabola(reflected_focal_length=focal, angle=90)
oap1k2.aperture = aperture

comp6 = Composition(name="Small 0.5inch")
comp6.set_light_source(Beam(radius=5, angle=0.0))
comp6.propagate(80)
comp6.add_on_axis(oap1k2)
comp6.propagate(2*focal)

comp6.pos += (200, 200, 0)
comp6.draw()


# # =============================================================================
# # 3 inch 30, normal beam
# # =============================================================================

# focal = 5*inch
# aperture = 3*inch
# oap3 = Off_Axis_Parabola(reflected_focal_length=focal, angle=30)
# oap3.aperture = aperture

# comp7 = Composition(name="Big 3inch")
# comp7.set_light_source(Beam(radius=20, angle=0.0))
# comp7.propagate(80)
# comp7.add_on_axis(oap3)
# comp7.propagate(2*focal)

# comp7.pos += (200, 300, 0)
# comp7.draw()

if freecad_da:
  setview()
