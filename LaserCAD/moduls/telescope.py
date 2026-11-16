# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:56:05 2023

@author: 12816
"""

from .. basic_optics import Mirror, Lens, Beam, Composition, inch



def Make_Telescope(name="Teleskop", f1=100.0, f2=100.0, d0=100.0, lens1_aperture=25,
             lens2_aperture=inch):
  """Create a telescope of two thin lenses with distance f1+f2.

  Parameters
  ----------
  name : str, optional
    The default is "Teleskop".
  f1 : float, optional
    Focal length of the first lens in mm. The default is 100.
  f2 : float, optional
    Focal length of the second lens in mm. The ratio f2/f1 is the
    amplification <amplification> of the telescope. The default is 100
    (amplification 1.0).
  d0 : float, optional
    Distance in mm between the start position of the telescope and the first
    lens. The default is 100.

  Returns
  -------
  teles : Composition

  Examples
  --------
  >>> teles = Make_Telescope()
  >>> teles.draw()
  """
  ls = Beam(radius=1.5, angle=0)
  l1 = Lens(f=f1)
  l1.aperture = lens1_aperture
  # p2 = Propagation(f1+f2)
  l2 = Lens(f=f2)
  l2.aperture = lens2_aperture
  amp = f2/f1
  d3 = f1*(1+amp)*amp - d0*amp*amp
  # p3 = Propagation(d3)

  teles = Composition(name=name)
  teles.set_light_source(ls)
  teles.propagate(d0)
  teles.add_on_axis(l1)
  teles.propagate(f1+f2)
  teles.add_on_axis(l2)
  teles.propagate(d3)
  teles.amplification = amp


  return teles