from LaserCAD.non_interactings import Spectrometer
from LaserCAD.basic_optics import Beam, Composition
from LaserCAD.freecad_models import freecad_da, setview, clear_doc

if freecad_da:
  clear_doc()

Setup = Composition()
beam = Beam(radius=2)

Setup.set_light_source(beam)
Setup.propagate(150)
Setup.add_on_axis(Spectrometer())
Setup.propagate(200)
Setup.add_on_axis(Spectrometer(model = "HR"))

if freecad_da:
  Setup.draw()
  setview()