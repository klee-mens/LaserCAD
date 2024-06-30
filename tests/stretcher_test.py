# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:53:52 2023

@author: 12816
"""


from LaserCAD.moduls import Make_Stretcher_chromeo
from LaserCAD.freecad_models import freecad_da, clear_doc, setview


def stretcher_test():
  stretch1 = Make_Stretcher_chromeo()
  stretch1.pos = (0, 0, 100)
  # stretch1.draw()
  return stretch1


if __name__ == "__main__":
  if freecad_da:
    clear_doc()
  stretcher = stretcher_test()
  # stretcher.draw_elements()
  # bs = stretcher.compute_beams()
  # for i in range(3):
    # bs[i].draw()
  stretcher.draw()
  if freecad_da:
    setview()