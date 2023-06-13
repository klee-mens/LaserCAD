#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 20:47:17 2022

@author: mens
"""

# from basic_optics import Opt_Element, Beam, Ray, Lens, Propagation, Mirror
# from basic_optics.freecad_models import warning, freecad_da, initialize_composition, add_to_composition
from .ray import Ray
from .beam import Beam
from .optical_element import Opt_Element
from .lens import Lens
from .mirror import Mirror, Curved_Mirror
from .freecad_models import warning, freecad_da, initialize_composition, add_to_composition, make_to_ray_part,model_table
import numpy as np
from copy import deepcopy


class Composition(Opt_Element):
  """
  Komposition von Elementen, besitzt optical Axis die mit jedem Element und
  jedem .propagate erweitert wird und sequence, die die Reihenfolge der
  Elemente angibt (meist trivial außer bei multipass)
  """
  def __init__(self, name="NewComposition", **kwargs):
    super().__init__(name=name,**kwargs)
    oA = Ray(name=self.name+"__oA_0", pos=self.pos, normal=self.normal)
    oA.length = 0
    self._optical_axis = [oA]
    self._elements = []
    self._sequence = []
    self._last_prop = 0 #für den Fall, dass eine letzte Propagation nach einem Element noch erwünscht ist
    # self._last_geom = self.get_geom()

    self._lightsource = Beam(radius=1, angle=0)
    self._lightsource.set_geom(self.get_geom())
    self._lightsource.name = self.name + "_Lighsource"
    self._beams = [self._lightsource]
    group_ls = self._lightsource.get_all_rays()
    counter = 0
    for ray in group_ls:
      ray.name = self._lightsource.name + "_" + str(counter)
      counter += 1
    self._ray_groups = [group_ls]
    self._catalogue = {}
    self._drawing_part = -1
    self.non_opticals = []


  def propagate(self, x):
    """
    propagiert das System um x mm vorwärts, updated damit opt_axis,
    self._matrix, ersetzt früheres add(Propagation)

    Parameters
    ----------
    x : float
      Länge um die propagiert wird
    """
    end_of_axis = self._optical_axis[-1]
    end_of_axis.length += x
    # self._last_geom = (end_of_axis.endpoint(), end_of_axis.normal)
    # self._matrix = np.matmul( np.array([[1,x], [0,1]]), self._matrix) #braucht keine Sau
    self._last_prop = x #endet mit Propagation

  def last_geom(self):
    end_of_axis = self._optical_axis[-1]
    return (end_of_axis.endpoint(), end_of_axis.get_axes())

  def __add_raw(self, item):
    # #checken ob Elm schon mal eingefügt
    self.__no_double_integration_check(item)
    # # Namen ändern, geom setzen, hinzufügen
    item.name = self.new_catalogue_entry(item)
    self._elements.append(item)
    self._sequence.append(len(self._elements)-1) #neues <item> am Ende der seq
    self._last_prop = 0 #endet mit Element

  def add_on_axis(self, item):
    """
    fügt <item> an der Stelle _last_geom (und damit) auf der optAx ein,
    checkt ob nicht ausversehen doppelt eingefügt, ändert namen, geom

    updatet _matrix, opt_axis
    """
    item.set_geom(self.last_geom())
    if hasattr(item, "next_ray"): 
      self.__add_raw(item)
      newoA = item.next_ray(self._optical_axis[-1])
      newoA.length = 0
      self._optical_axis.append(newoA)
    # ignore non-optical Elm, e.g. Geom_Obj, cosmetics
    else:
      self.non_opticals.append(item)
 
  def add_fixed_elm(self, item):
    """
    fügt <item> genau an der Stelle <item.get_geom()> ein

    updated entsprechend add_on_axis
    """
    if hasattr(item, "next_ray"): 
      self.__add_raw(item)
    else:
      self.non_opticals.append(item)


  def redefine_optical_axis(self, ray):
    # zB wenn die wavelength angepasst werden muss
    # print("sollte nur gemacht werden, wenn absolut noch kein Element eingefügt wurde")
    print("should only be done if absolutely no element has been inserted yet")
    #print("kann die ganze Geometrie hart abfucken")
    self.set_geom(ray.get_geom())
    oA = deepcopy(ray)
    oA.name = self.name +"__oA_0"
    self._optical_axis = [oA]
    self.recompute_optical_axis()

  def recompute_optical_axis(self):
    self._optical_axis = [self._optical_axis[0]]
    counter = 0

    for ind in self._sequence:
      elm = self._elements[ind]
      # print("-----", elm)
      newoA = elm.next_ray(self._optical_axis[-1])
      counter += 1
      newoA.name = self.name + "__oA_" + str(counter)
      self._optical_axis.append(newoA)
    self._optical_axis[-1].length = self._last_prop


  def matrix(self):
    """
    computes the optical matrix of the system
    each iteration consists of a propagation given by the length of the nth
    ray of the optical_axis followed by the matrix multiplication with the
    seq[n] element

    Returns the ABCD-matrix
    """
    self._matrix = np.eye(2)
    self.recompute_optical_axis()
    counter = -1
    for ind in self._sequence:
      counter += 1
      B = self._optical_axis[counter].length
      M = self._elements[ind]._matrix
      self._matrix = np.matmul(np.array([[1,B], [0,1]]), self._matrix )
      print("--")
      print(self._matrix)
      print("--")
      self._matrix = np.matmul(M, self._matrix )
    # self._matrix = np.matmul(np.array([[1,self._last_prop], [0,1]]), self._matrix )
    self._matrix = np.matmul(np.array([[1,self._last_prop], [0,1]]), self._matrix ) #last propagation
    
    return np.array(self._matrix)

  def get_sequence(self):
    return list(self._sequence)

  def set_sequence(self, seq):
    self._sequence = list(seq)
    # self.recompute_optical_axis()



  def compute_beams(self, external_source=None):
    beamcount = 0
    if external_source:
      beamlist = [external_source]
    else:
      beamlist = [self._lightsource]
    for n in self._sequence:
      elm = self._elements[n]
      beam = elm.next_beam(beamlist[-1])
      if beam:
        # manche Elemente wie Prop geben keine validen beams zurück
        beamcount += 1
        beam.name = self.name + "_beam_" + str(beamcount)
        beamlist.append(beam)
    # beam.set_length(self._last_prop)
    beamlist[-1].set_length(self._last_prop)
    if not external_source:
      self._beams = beamlist
    return beamlist


  def draw_elements(self):
    self.__init_parts()
    container = []
    for elm in self._elements:
      obj = elm.draw()
      container.append(obj)
    for elm in self.non_opticals:
      obj = elm.draw()
      container.append(obj)
    return self.__container_to_part(self._elements_part, container)

  def draw_beams(self):
  # def draw_beams(self, style="cone"):
    # liso = self._lightsource
    # if liso._distribution == "cone":
    #   liso.draw_dict["model"] = style
    self.__init_parts()
    self.compute_beams()
    container = []
    for beam in self._beams:
      obj = beam.draw()
      container.append(obj)
    return self.__container_to_part(self._beams_part, container)

  def draw_mounts(self):
    self.__init_parts()
    container = []
    for elm in self._elements:
      obj = elm.draw_mount()
      container.append(obj)
    return self.__container_to_part(self._mounts_part, container)


  # def draw_rays(self): 
  #   """
  #   DEPRECATED, use self._lightsource.draw_dict["model"] = "ray_group" instead
  #   """
  #   return self.draw_beams(style="ray_group")


  def draw(self):
    self.draw_elements()
    self.draw_beams()
    self.draw_mounts()
    # self.draw_rays()

  def __container_to_part(self, part, container):
    if freecad_da:
      part = add_to_composition(part, container)
    else:
      for x in container:
        part.append(x)
    return part

  def __init_parts(self):
    if self._drawing_part == -1:
      if freecad_da:
        d,e,m,b,r = initialize_composition(self.name)
        self._drawing_part = d
        self._elements_part = e
        self._mounts_part = m
        self._beams_part = b
        self._rays_part = r
      else:
        self._elements_part = []
        self._mounts_part = []
        self._rays_part = []
        self._beams_part = []
        self._drawing_part = [self._elements_part, self._mounts_part,
                                self._rays_part, self._beams_part]


  def set_light_source(self, ls):
    """
    setzt neue Lightsource (meistens ein Beam) für die Composition und passt
    deren Geom und Namen an
    danach werden _beams[] und raygroups[] neu initialisiert
    """

    self._lightsource = ls
    # self.set_geom(ls.get_geom())
    ls.set_geom(self.get_geom())
    ls.name = self.name + "_Lightsource"
    self._beams = [self._lightsource]
    group_ls = self._lightsource.get_all_rays()
    counter = 0
    for ray in group_ls:
      ray.name = self._lightsource.name + "_" + str(counter)
      counter += 1
    self._ray_groups = [group_ls]


  def new_catalogue_entry(self, item):
    #gibt jedem neuen Element einen Namen entsprechend seiner Klasse
    key = item.class_name()
    if key in self._catalogue:
         anz, names = self._catalogue[key]
         anz += 1
         itname = next_name(names[-1])
         names.append(itname)
    else:
         itname = self.name + "_" + item.class_name() + "_01"
         anz = 1
    self._catalogue[key] = [anz, [itname]]
    return itname

  def __no_double_integration_check(self, item):
    #checken ob Elm schon mal eingefügt
    if item in self._elements:
      warning("Das Element -" + str(item) + "- wurde bereits in <" +
            self.name + "> eingefügt.")
    # item.group.append(self)

  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird
    ändert die Position aller __rays mit
    """
    # print("---pos---geändert---")
    super()._pos_changed(old_pos, new_pos)
    self._rearange_subobjects_pos(old_pos, new_pos, self._elements)
    self._rearange_subobjects_pos(old_pos, new_pos, [self._lightsource]) #sonst wird ls doppelt geshifted
    self._rearange_subobjects_pos(old_pos, new_pos, self._beams[1::])
    self._rearange_subobjects_pos(old_pos, new_pos, [r for rg in self._ray_groups[1::] for r in rg])
    self._rearange_subobjects_pos(old_pos, new_pos, self._optical_axis)

  def _axes_changed(self, old_axes, new_axes):
    """
    wird aufgerufen, wen die axese von <self> verändert wird
    dreht die axese aller __rays mit

    dreht außerdem das eigene Koordiantensystem
    """
    super()._axes_changed(old_axes, new_axes)
    self._rearange_subobjects_axes(old_axes, new_axes, [self._lightsource]) #sonst wird ls doppelt geshifted
    self._rearange_subobjects_axes(old_axes, new_axes, self._elements)
    self._rearange_subobjects_axes(old_axes, new_axes, self._beams[1::])
    self._rearange_subobjects_axes(old_axes, new_axes, [r for rg in self._ray_groups[1::] for r in rg])
    self._rearange_subobjects_axes(old_axes, new_axes, self._optical_axis)




def next_name(name, prefix=""):
  # generiert einen neuen namen aus dem alten Element
  ind = name.rfind("_")
  try:
    num = int(name[ind+1::])+1
  except:
    num = 1
  suffix = str(num) if num>9 else "0"+str(num)
  return prefix + name[0:ind] + "_" + suffix


# def Composition_lens_test():
#   fok = 100
#   beam1 = Beam(3, 0.02)
#   p1 = Propagation(d=1.5*fok)
#   l1 = Lens(f=fok)
#   p2 = Propagation(d=3*fok)

#   vergAbb = Composition_old(name="VergrAbb")
#   vergAbb._lightsource = beam1
#   vergAbb.add(p1)
#   vergAbb.add(l1)
#   vergAbb.add(p2)
# #   vergAbb.add(p2) # kann eingeschaltet werden um Warnung zu triggern
# #   beams = vergAbb.compute_beams()
#   return vergAbb

# def Teleskop_test():
#   fok = 120
#   # beam1 = Beam(1, 0.05)
#   beam1 = Beam(2.0, 0.0)
#   p1 = Propagation(d=fok)
#   l1 = Lens(f=fok)
#   p2 = Propagation(d=2*fok)
#   l2 = Lens(f=fok)
#   p3 = Propagation(d=fok)

#   teles = Composition_old(name="Teleskop")
#   teles._lightsource = beam1
#   teles.add(p1)
#   teles.add(l1)
#   teles.add(p2)
#   teles.add(l2)
#   teles.add(p3)
# #   teles.add(p2) # kann eingeschaltet werden um Warnung zu triggern
# #   beams = teles.compute_beams()
#   return teles


# def Composition_mirror_test():
#   a = Composition_old(name="4FlipTrip")
#   r = Beam(radius=4, angle=0)
# #   r = Beam(radius=4, angle=0, pos = (0, 0, 85))
#   a._lightsource = r
#   m = Mirror(phi=90)
#   p = Propagation(d=300)
#   m2 = Mirror(phi=90)
#   p2 = Propagation(d=300)
#   m3 = Mirror(phi=90)
#   p3 = Propagation(d=300)
#   p4 = Propagation(d=300)
#   a.add(p)
#   a.add(m)
#   a.add(p2)
#   a.add(m2)
#   a.add(p3)
#   a.add(m3)
#   a.add(p4)

# #   a.draw()
# #   a.compute_beams()
#   #a.draw_mounts()
#   return a

# def Mirror_Teleskop_test():
#   c = Composition_old(name="MirrorTelescope")
#   ls = Beam(angle=0)
#   p1 = Propagation(d=100)
#   cm1 = Curved_Mirror(radius=100, phi=180-10)
#   p2 = Propagation(d=100)
#   cm2 = Curved_Mirror(radius=100, phi=10-180)
#   p3 = Propagation(d=100)

#   c._lightsource = ls
#   c.add(p1)
#   c.add(cm1)
#   c.add(p2)
#   c.add(cm2)
#   c.add(p3)
#   return c

# def add_only_elem_test():
#   comp = Composition_old()
#   lens1 = Lens(f=200, pos=(100, 0, 80))
#   lens2 = Lens(f=200, pos=(500, 0, 80))
#   comp.add_only_elm(lens1)
#   comp.add_only_elm(lens2)
#   return comp






