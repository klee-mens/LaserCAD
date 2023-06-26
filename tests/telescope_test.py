# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:53:52 2023

@author: 12816
"""

from moduls import Make_Telescope


def telescope_test():  
  teles = Make_Telescope()
  teles.pos = (0, 500,100)
  teles.draw()
  return teles