from LaserCAD.basic_optics.beam import Beam
from LaserCAD.moduls.motorized_TSF import Motorized_TSF
from LaserCAD import Composition
from LaserCAD import freecad_da, clear_doc

if freecad_da:
  clear_doc()

Motorized_TSF1 = Motorized_TSF()
Motorized_TSF2 = Motorized_TSF(flip=True)

Setup = Composition()
Setup.set_light_source(Beam())
Setup.propagate(100)
Setup.add_supcomposition_on_axis(Motorized_TSF1)
Setup.propagate(100)
Setup.add_supcomposition_on_axis(Motorized_TSF2)
Setup.propagate(100)
Setup.draw()