from LaserCAD.basic_optics.beam import Beam
from LaserCAD.moduls.polarization_rotator import Polarization_Rotator
from LaserCAD import Composition
from LaserCAD import freecad_da, clear_doc

if freecad_da:
  clear_doc()

Pol_Rotator1 = Polarization_Rotator()
Pol_Rotator2 = Polarization_Rotator(flip=True)

Setup = Composition()
Setup.set_light_source(Beam())
Setup.propagate(100)
Setup.add_supcomposition_on_axis(Pol_Rotator1)
Setup.propagate(100)
Setup.add_supcomposition_on_axis(Pol_Rotator2)
Setup.propagate(100)
Setup.draw()