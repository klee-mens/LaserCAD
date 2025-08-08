from LaserCAD.moduls import Make_Telescope
from LaserCAD.basic_optics import export_to_TikZ

teles = Make_Telescope()

import os
Folder = os.path.dirname(os.path.abspath(__file__))

export_to_TikZ(teles)
# export_to_TikZ(teles, filename=os.path.join(Folder, "telescope.tex"))