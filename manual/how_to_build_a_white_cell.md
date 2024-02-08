"""
Created on Mon Feb  5 00:46:35 2024

@author: mens
"""

# How to build a Multi Pass White Cell

Wwe will build a White Cell (see Wikipedia) as an beginners example of how to
use helper compositions to simplify the positioning of the elements in the first step.
To finish we will set the sequence of the composition to let the beam pass the
elements several times, thus seeing the effect of multipass arrangements.
Here you can see the code:

```python
from .. basic_optics import Composition, inch, Curved_Mirror, Unit_Mount
import numpy as np


def Make_White_Cell(name="WhiteCell", Radius=300, roundtrips4=2, seperation=15):

  mirror_sep_angle = 12 #degree, could be smaller
  deflection = 2 * np.arcsin(seperation/2 / Radius) * 180/np.pi

  helper = Composition(name=name)
  helper.propagate(Radius)
  scm1 = Curved_Mirror(radius=Radius, phi=180-deflection)
  helper.add_on_axis(scm1)
  helper.propagate(Radius)

  bigcm = Curved_Mirror(radius=Radius, phi=180+mirror_sep_angle)
  bigcm.aperture = 12 + (roundtrips4-1)*2*seperation
  bigcm.Mount = Unit_Mount()
  helper.add_on_axis(bigcm)
  helper.propagate(Radius)

  scm2 = Curved_Mirror(radius=Radius, phi=180-deflection)
  helper.add_on_axis(scm2)
  helper.propagate(Radius)

  white_cell = Composition()
  white_cell.pos = helper.pos - (0, seperation*(roundtrips4-1), 0)
  white_cell.normal = scm1.pos - white_cell.pos
  white_cell.add_supcomposition_fixed(helper)

  seq = [0, 1, 2]
  roundtrip_sequence = [1, 0, 1, 2]
  for n in range(roundtrips4-1):
    seq.extend(roundtrip_sequence)
  white_cell.set_sequence(seq)

  white_cell.propagate(Radius*1.2)
  return white_cell
```


The code generates a White Cell mirror triplett for a compact multipass system
with optical unity matrix (or something similar, in fact you need to go back in it again).
See Multipass cells on wikipedia or so.
Parameters
----------
name : str, optional
  DESCRIPTION. The default is "WhiteCell".
Radius : float, optional
  Radius of all convex spheres and distances. The default is 300.
roundtrips4 : integer, optional
  gives the number of roundtrips the beam apsses the cell.
  For each the beam will propagate 4x the Radius.
  The default is 2.
seperation : TYPE, optional
  The seperation of the beam hits on the big sphere. Might be smaller.
  The default is 15.

Returns
-------
white_cell : Composition
  DESCRIPTION.



