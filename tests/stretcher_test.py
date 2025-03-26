# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:53:52 2023

@author: 12816
"""


from LaserCAD.moduls import Make_Stretcher
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
import numpy as np
inch = 25.4


def stretcher_test():

  stretch1 = Make_Stretcher(radius_concave = 1000, #radius of the big concave sphere
      aperture_concave = 6 * inch,
      height_stripe_mirror = 10, #height of the stripe mirror in mm
      seperation_angle = 10 /180 *np.pi, # sep between in and outgoing middle ray
      grating_const = 1/1000, # in 1/mm
      seperation = 50, # difference grating position und radius_concave
      lambda_mid = 800e-9 * 1e3, # central wave length in mm
      band_width = 100e-9*1e3, # full bandwith in mm
      number_of_rays = 20,
      safety_to_stripe_mirror = 5, #distance first incomming ray to stripe_mirror in mm
      periscope_height = 10,
      first_propagation = 120, # legnth of the first ray_bundle to flip mirror1 mm
      distance_roof_top_grating = 600)

  return stretch1


if __name__ == "__main__":
  if freecad_da:
    clear_doc()
  stretcher1 = stretcher_test()
  stretcher1.draw()

  print()
  print("Stretcher GDD:", np.round(stretcher1.GDD * 1e30), "fs^2")
  print("Stretcher TOD:", np.round(stretcher1.TOD * 1e45), "fs^3")
  if freecad_da:
    setview()