# -*- coding: utf-8 -*-
"""

Beeinhaltet zu allen Objekten aus <basic_objects> die entsprechenden FreeCAD-
Modelle, sowie ein paar grundlegende Funkitonen wie Rotate, etc in <utils>



Created on Thu Aug 18 12:29:31 2022

@author: mens
"""

# from freecad_models.utils import freecad_da, start_DOC, get_DOC
from .utils import freecad_da, start_DOC, get_DOC, warning, clear_doc, setview
from .freecad_model_lens import model_lens
from .freecad_model_ray import model_ray_1D
from .freecad_model_beam import model_beam, model_Gaussian_beam
from .freecad_model_composition import initialize_composition, add_to_composition
from .freecad_model_mirror import model_mirror, model_stripe_mirror, model_rooftop_mirror, model_round_mirror
from .freecad_model_grating import model_grating,grating_mount
from .freecad_model_iris_diaphragms import model_iris_diaphragms,iris_post,model_diaphragms,model_intersection_plane
from .freecad_model_mounts import mirror_mount,lens_mount,model_table, model_lambda_plate
from .freecad_inputoutput_test import input_output_test
from .freecad_model_crystal import model_crystal,model_crystal_mount
from .freecad_model_geom_object import model_geom_object
pfad = __file__[0:-9]


if freecad_da:
  DOC = get_DOC()
else:
  # print("FreeCAD konnte nicht importiert werden")
  print("FreeCAD could not be imported")