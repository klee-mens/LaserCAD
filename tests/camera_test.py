from LaserCAD.non_interactings import Camera
from LaserCAD.basic_optics import Beam, Composition
from LaserCAD.freecad_models import freecad_da, setview, clear_doc

if freecad_da:
  clear_doc()

Setup = Composition()
beam = Beam(radius=2)

camera = Camera()
Setup.set_light_source(beam)
Setup.propagate(150)
Setup.add_on_axis(camera)

if freecad_da:
  Setup.draw()
  setview()