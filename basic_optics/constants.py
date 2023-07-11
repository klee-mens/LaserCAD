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