#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 15:14:50 2023

@author: mens
"""

import numpy as np

c = 3e8
h = 6e-34

inch = 25.4 # Grundeinheit für Optikdurchmesser

NAME0="unnamed"
POS0 = np.array((0,0,80)) #Strahlhöhe 80 mm
NORM0 = np.array((1,0,0)) #Strahl startet in x-Richtung
TOLERANCE = 1e-9 #Wert ab dem zwei Größen (meist Winkel) als gleich angenommen werden

def table_coordinates_to_xy(p, q):
  """
  transforms the integer table coordinates (just the screw hole number counted
  along and transverse the table) to x,y coordinates in mm
  the specific table used here reaches from hole 1 to 114 in x direction and
  from 1 to 58 in (unfortunately negative, my fault) y direction, of course
  this can be altered by the user and changes from table to table, so yeah, it
  is therefore in the constant section

  Parameters
  ----------
  p : TYPE
    DESCRIPTION.
  q : TYPE
    DESCRIPTION.

  Returns
  -------
  None.

  """
  return p*25, (59-q)*25

def xy_to_table_plus_offset(x,y):
  """
  the opposite funtion, tells you from the real coordinates (x,y) in mm at which
  screw hole pair on the table plus offset in mm the element should be placed

  Parameters
  ----------
  x : TYPE
    DESCRIPTION.
  y : TYPE
    DESCRIPTION.

  Returns
  -------
  None.

  """
  p = int(x // 25)
  offset_x = x - 25*p
  q = int(59 - y//25)
  offset_y = y - (59-q)*25
  return  [p, offset_x, q, offset_y]


def test_xy_table():
  x,y = [1259.95368134,  762.68269095]
  print("x,y original : ", x, "|", y)
  print()
  p, xo, q, yo = xy_to_table_plus_offset(x, y)
  print("p , offest_x | q, offest_y : ", p, ",", xo, "|", q, ",", yo)
  print()
  xb, yb = table_coordinates_to_xy(p, q)
  print("back again to x | y : ", xb+xo, "|", yb+yo)


if __name__ == "__main__":
  test_xy_table()
