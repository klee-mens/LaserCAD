from LaserCAD.basic_optics import SquareBeam, Composition, Intersection_plane
from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics.lens import Thicklens
import numpy as np

def test_radius(Lens):
  n = Lens.refractive_index
  r1 = Lens.radius1()
  r2 = Lens.radius2()
  d = Lens.thickness
  if Lens.biconvex:
    f = 1/((n-1)*(2/r1-(n-1)*d/(n*r1**2)))
  else:
    f = 1/((n-1)*(1/r1))

  print(f"lens radii: R1 = {r1:.2f}mm, R2 = {r2:.2f}mm")
  print(f"lens focal length: {f:.2f}mm")
  print(f"given focal length: {Lens.focal_length:.2f}mm")
  print(f"lens thickness: {d:.2f}mm")

def test_composition(offset=0, f=85, n=1.515, aperture=75, edge_thickness=3, biconvex=False, draw_spot_diagram=False):
  prop1 = 100
  prop2 = abs(f)
  prop3 = 100

  Comp1 = Composition()
  Comp1.pos += (0, -offset,0)

  Beam1 = SquareBeam(radius=20, ray_in_line=5)

  Comp1.set_light_source(Beam1)
  Comp1.propagate(prop1)
  Lens1 = Thicklens(f=f, n=n, aperture=aperture, edge_thickness=edge_thickness, biconvex=biconvex)
  Comp1.add_on_axis(Lens1)
  Comp1.propagate(prop2-Lens1.thickness)
  IP1 = Intersection_plane()
  Comp1.add_on_axis(IP1)
  IP1.draw()
  Comp1.propagate(prop3)
  Comp1.draw()

  if draw_spot_diagram: IP1.spot_diagram(Comp1._beams[1])
  
  test_radius(Lens1)

  return Comp1, IP1




if freecad_da:
  clear_doc()

focal_length = 85
Comp1, IP1 = test_composition(offset=0)
Comp2, IP2 = test_composition(offset=100, biconvex=True)
Comp3, IP3 = test_composition(offset=200, f=-focal_length)
Comp4, IP4 = test_composition(offset=300, f=-focal_length, biconvex=True)


if freecad_da:
  setview()