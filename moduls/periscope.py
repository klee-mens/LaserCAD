# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:56:05 2023

@author: 12816
"""

from .. basic_optics import Mirror, Beam, Composition, Component
from .. basic_optics import Special_mount, Mount, Composed_Mount, Post_and_holder
from ..freecad_models import model_crystal



def Make_Periscope(name="Periskop", length=150, theta = 90, dist1=75, dist2=75):

  m1 = Mirror(theta=theta)
  # p = Propagation(d=length)
  m2 = Mirror(theta=-theta)
  peris = Composition(name=name)
  peris.propagate(dist1)
  peris.add_on_axis(m1)
  peris.propagate(length)
  peris.add_on_axis(m2)
  peris.propagate(dist2)

  return peris


def Periscope2(name="Periskop", length=160,theta = 90, phi = 0, dist1=75, dist2=75):
# def Periscope(name="Periskop", length=120, theta=0, dist1=75, dist2=75):
  """
  constructs a Periscope with <name> and Distance <dist1> to the first mirror,
  <length> between the two mirrors and <dist2> after the last mirror
  
  irgendwann einmal:
  the vector between the two mirrors has an angle of <theta> to the z-Axis  

  Parameters
  ----------
  name : TYPE, optional
    DESCRIPTION. The default is "Periskop".
  length : TYPE, optional
    DESCRIPTION. The default is 120.
  theta : TYPE, optional
    Angle to the z-Axis in Degress (0->360°). The default is 0.
  dist1 : TYPE, optional
    DESCRIPTION. The default is 75.
  dist2 : TYPE, optional
    DESCRIPTION. The default is 75.

  Returns
  -------
  the Compostion

  """
  lightsource = Beam(radius=1, angle=0)
  peris = Composition(name=name)
  peris.set_light_source(lightsource)
  peris.propagate(dist1)
  m1 = Mirror()
  peris.add_on_axis(m1)
  m1.normal = (1,0,1)
  peris.recompute_optical_axis()
  
  # theta *= 180/np.pi
  # m1.normal = (1, -np.sin(theta), -np.cos(theta)) #siehe Skizze irgendwo...
  peris.propagate(length)
  m2 = Mirror()
  peris.add_on_axis(m2)
  m2.normal= (1,0,-1)
  peris.recompute_optical_axis()
  # m2.normal = -m1.normal
  peris.propagate(dist2)
  
  return peris



def RoofTop_Mirror(name="RoofTopMirror", height=20, direction=1):
  """
  direction=1 RofftopMirror goes down

  Parameters
  ----------
  name : TYPE, optional
    DESCRIPTION. The default is "RoofTopMirror".
  height : TYPE, optional
    DESCRIPTION. The default is 20.
  direction : TYPE, optional
    DESCRIPTION. The default is 1.

  Returns
  -------
  None.

  """
  roof = Composition(name=name)
  roof.height = height
  m1 = Mirror(phi=0, theta=-90*direction)
  m2 = Mirror(phi=0, theta=-90*direction)
  roof.add_on_axis(m1)
  roof.propagate(height)
  roof.add_on_axis(m2)
  #cosmetics
  def dont_draw():
    return None
  m1.draw = dont_draw
  m1.draw_dict["mount_type"] = "dont_draw"
  m2.draw = dont_draw
  m2.draw_dict["mount_type"] = "dont_draw"
  rooftop_model = Component()
  rooftop_model.freecad_model = model_crystal
  rooftop_model.pos += (height/2, 0, -height/2)
  roof.add_fixed_elm(rooftop_model)
  
  rooftop_M1 = Special_mount(model="rooftop mirror mount")
  M2 = Mount(model="POLARIS-K2")
  rooftop_model = Composed_Mount()
  rooftop_model.add(rooftop_M1)
  rooftop_model.add(M2)
  rooftop_model.pos += (height/2, 0, -height/2)
  post_part = Post_and_holder(xshift=M2.xshift,height=-M2.zshift)
  post_part.set_geom(M2.get_geom())
  roof.add_fixed_elm(rooftop_model)
  roof.add_fixed_elm(post_part)
  return roof