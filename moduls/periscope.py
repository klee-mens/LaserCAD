# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:56:05 2023

@author: 12816
"""

from .. basic_optics import Mirror, Composition, Component
from .. basic_optics import Unit_Mount, Rooftop_Mirror_Mount
from ..freecad_models import model_rooftop_mirror



def Make_Periscope(name="Periskop", height=150, up=True, backwards=False):
  """
  Creates an up=True going periscope that translates the incoming beam for a
  specific height=150 mm. If backwards=False is true, the beam is also back 
  reflected as in Make_RoofTop_Mirror.
  Since there is now standard solution for the 2 mirrors to be mounted (at 
  least not to my knowledge) the Mounts are set to the unspecific Unit_Mount()
  which will not be drawn.

  Parameters
  ----------
  name : TYPE, optional
    DESCRIPTION. The default is "Periskop".
  height : TYPE, optional
    DESCRIPTION. The default is 150.
  up : TYPE, optional
    DESCRIPTION. The default is True.
  backwards : TYPE, optional
    DESCRIPTION. The default is False.

  Returns
  -------
  peris : TYPE
    DESCRIPTION.

  """

  peris = Composition(name=name)
  if up:
    m1 = Mirror(theta=90)
  else:
    m1 = Mirror(theta=-90)
  
  m1.set_mount(Unit_Mount()) # default Mount is invisible
  peris.add_on_axis(m1)

  peris.propagate(height)

  m2 = Mirror()
  m2.set_mount(Unit_Mount()) # default Mount is invisible
  peris.add_on_axis(m2)
  n1 = m1.normal
  if backwards:
    m2.normal = (n1[0], n1[1], -n1[2])
  else:
    m2.normal = -n1
  
  return peris




class Rooftop_Mirror_Component(Component):
  """
  This is the pure cosmetic component, that give the rooftop mirror its shape,
  but does not actually interact with the beam. It sits in the middle between
  the two invisible mirrors of the real RoofTopMirror Composition.
  """
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.freecad_model = model_rooftop_mirror
    self.set_mount_to_default()
    
  def set_mount_to_default(self):
    smm = Rooftop_Mirror_Mount()
    smm.set_geom(self.get_geom())
    smm.pos += self.normal * self.aperture / 2
    self.Mount = smm

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["dia"] = self.aperture
    self.draw_dict["model_type"] = "Rooftop"    


def Make_RoofTop_Mirror(name="RoofTopMirror", height=20, up=True):
  """
  creates a RoofTopMirror as an composition of 2 mirrors and an purely 
  cosmetic Component for the 3D view.
  In fact it is nothing more than an fancy looking backward periscope.

  Parameters
  ----------
  name : TYPE, optional
    DESCRIPTION. The default is "RoofTopMirror".
  height : TYPE, optional
    DESCRIPTION. The default is 20.
  up : TYPE, optional
    DESCRIPTION. The default is True.

  Returns
  -------
  roof : TYPE
    DESCRIPTION.

  """

  roof = Make_Periscope(name=name, height=height, up=up, backwards=True)
  roof.height = height # just for the records
  m1, m2 = roof._elements
  m1.invisible = True
  m2.invisible = True

  pure_cosmetic = Rooftop_Mirror_Component(name="RoofTop_Mirror")
  pure_cosmetic.pos += (0,0,height/2)
  pure_cosmetic.draw_dict["model_type"] = "Rooftop"
  pure_cosmetic.set_mount_to_default()
  
  roof.add_fixed_elm(pure_cosmetic)
  
  return roof




def Rooftop_mirror_draw_test():
  rm = Rooftop_Mirror_Component()
  rm.pos = (120,50,130)
  rm.normal = (1,-1,0)
  rm.aperture = 10
  rm.set_mount_to_default()
  rm.draw()
  rm.draw_mount()




