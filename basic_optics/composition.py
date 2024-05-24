#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 20:47:17 2022

@author: mens
"""

from .ray import Ray
from .beam import Beam
from .geom_object import Geom_Object
from .grating import Grating
from ..freecad_models import warning, freecad_da, initialize_composition, add_to_composition
from ..freecad_models.freecad_model_element_holder import Model_element_holder
import numpy as np
from copy import deepcopy


class Composition(Geom_Object):
  """
  Komposition von Elementen, besitzt optical Axis die mit jedem Element und
  jedem .propagate erweitert wird und sequence, die die Reihenfolge der
  Elemente angibt (meist trivial außer bei multipass)
  """
  def __init__(self, name="NewComposition", **kwargs):
    super().__init__(name=name,**kwargs)
    oA = Ray(name=self.name+"__oA_0")
    oA.pos = self.pos
    oA.normal = self.normal
    oA.length = 0
    self._optical_axis = [oA]
    self._elements = []
    self._sequence = []
    self._last_prop = 0 #für den Fall, dass eine letzte Propagation nach einem Element noch erwünscht ist

    self._lightsource = Beam(radius=1, angle=0)
    self._lightsource.set_geom(self.get_geom())
    self._lightsource.name = self.name + "_Lighsource"
    self._beams = [self._lightsource]
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
    self._last_prop = end_of_axis.length #endet mit Propagation

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

  def add_supcomposition_on_axis(self, subcomp):
    subcomp.set_geom(self.last_geom())
    self.add_supcomposition_fixed(subcomp)

  def add_supcomposition_fixed(self, subcomp):
    for element in subcomp._elements:
      self.add_fixed_elm(element)
    for nonopt in subcomp.non_opticals:
      self.add_fixed_elm(nonopt)

  def redefine_optical_axis(self, ray):
    # zB wenn die wavelength angepasst werden muss
    # print("sollte nur gemacht werden, wenn absolut noch kein Element eingefügt wurde")
    # print("should only be done if absolutely no element has been inserted yet")
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
      M = self._elements[ind].matrix(inray = self._optical_axis[counter])
      self._matrix = np.matmul(np.array([[1,B], [0,1]]), self._matrix )
      self._matrix = np.matmul(M, self._matrix )
      
    self._matrix = np.matmul(np.array([[1,self._last_prop], [0,1]]), self._matrix ) #last propagation
    return np.array(self._matrix)
  
  def kostenbauder(self):
    """
    computes the optical matrix of the system
    each iteration consists of a propagation given by the length of the nth
    ray of the optical_axis followed by the matrix multiplication with the
    seq[n] element

    Returns the ABCD-matrix
    """
    self._kostenbauder = np.eye(4)
    self.recompute_optical_axis()
    counter = -1
    for ind in self._sequence:
      counter += 1
      B = self._optical_axis[counter].length
      moment_propa = np.eye(4)
      moment_propa[0,1] = B
      M = self._elements[ind].kostenbauder(inray = self._optical_axis[counter])
      
      self._kostenbauder = np.matmul( moment_propa, self._kostenbauder )
      self._kostenbauder = np.matmul( M, self._kostenbauder )
      
    last_propa = np.eye(4)
    last_propa[0,1] = self._last_prop
    self._kostenbauder = np.matmul( last_propa, self._kostenbauder ) #last propagation
    return np.array(self._kostenbauder)

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
    beamlist[-1].set_length(self._last_prop)
    if not external_source:
      self._beams = beamlist
    return beamlist

  def optical_path_length(self):
    return sum([ray.length for ray in self._optical_axis])

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
    for elm in self.non_opticals:
      obj = elm.draw_mount()
      container.append(obj)
    return self.__container_to_part(self._mounts_part, container)
  
  def draw_alignment_posts(self):
    self.__init_parts()
    container = []
    for elm in self._elements:
      if freecad_da:
        if type(elm) == Grating:
          obj = Model_element_holder(post_distence=20,base_height=20,
                                     geom=elm.get_geom(),thickness=elm.thickness,
                                     width=elm.width,height=elm.height,
                                     ele_type="Grating")
        else:
          obj = Model_element_holder(post_distence=20,base_height=20,
                                     geom=elm.get_geom(),aperture=elm.aperture,
                                     thickness=elm.thickness,
                                     ele_type="Mirror")
        container.append(obj)
    return self.__container_to_part(self._alignment_post_part, container)

  def draw(self):
    self.draw_elements()
    self.draw_beams()
    self.draw_mounts()

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
        d,e,m,b,a = initialize_composition(self.name)
        self._drawing_part = d
        self._elements_part = e
        self._mounts_part = m
        self._beams_part = b
        self._alignment_post_part = a
      else:
        self._elements_part = []
        self._mounts_part = []
        self._beams_part = []
        self._alignment_post_part = []
        self._drawing_part = [self._elements_part, self._mounts_part, 
                              self._beams_part, self._alignment_post_part]


  def set_light_source(self, ls):
    """
    setzt neue Lightsource (meistens ein Beam) für die Composition und passt
    deren Geom und Namen an
    danach werden _beams[] und raygroups[] neu initialisiert
    """
    self._lightsource = ls
    ls.set_geom(self.get_geom())
    ls.name = self.name + "_Lightsource"
    self._beams = [self._lightsource]
    # group_ls = self._lightsource.get_all_rays()
    # counter = 0
    # for ray in group_ls:
    #   ray.name = self._lightsource.name + "_" + str(counter)
    #   counter += 1

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


  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird
    ändert die Position aller __rays mit
    """
    super()._pos_changed(old_pos, new_pos)
    self._rearange_subobjects_pos(old_pos, new_pos, self._elements)
    self._rearange_subobjects_pos(old_pos, new_pos, [self._lightsource]) #sonst wird ls doppelt geshifted
    self._rearange_subobjects_pos(old_pos, new_pos, self._beams[1::])
    self._rearange_subobjects_pos(old_pos, new_pos, self._optical_axis)
    self._rearange_subobjects_pos(old_pos, new_pos, self.non_opticals)

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
    self._rearange_subobjects_axes(old_axes, new_axes, self._optical_axis)
    self._rearange_subobjects_axes(old_axes, new_axes, self.non_opticals)

  def Kostenbauder_matrix(self,shifting_distence=100):
    point_start=self.pos
    point_end = self.last_geom()[0]
    # if self.normal == np.array(shifting_normal):
    #   return("wrong direction")
    point_start_dx = point_start + 0.1*self.get_coordinate_system()[1]
    ls_group = []
    ls_dx = deepcopy(self._lightsource)
    ls_dx.pos = point_start_dx
    ls_group.append(ls_dx)
    ls_dax = deepcopy(self._lightsource)
    ls_dax.rotate(self.get_coordinate_system()[2],0.5*np.pi/100)
    ls_group.append(ls_dax)
    ls_dlambda = deepcopy(self._lightsource)
    for ii in range(len(ls_dlambda.get_all_rays())):
      ls_dlambda.get_all_rays()[ii].wavelength+=ls_dlambda.get_all_rays()[ii].wavelength/100
    ls_group.append(ls_dlambda)
    # ls_shift_start = deepcopy(self._lightsource)
    # ls_shift_start.pos = point_start + shifting_normal*shifting_distence
    # ls_group.append(ls_shift_start)
    # ls_shift_dx = deepcopy(ls_shift_start)
    # ls_shift_dx.pos += np.linalg.norm(point_start)/100*self.get_coordinate_system()[1]
    # ls_group.append(ls_shift_dx)
    # ls_shift_dax = deepcopy(ls_shift_start)
    # ls_shift_dax.rotate(self.get_coordinate_system()[2],0.5*np.pi/100)
    # ls_group.append(ls_shift_dax)
    # ls_shift_dlambda = deepcopy(ls_shift_start)
    # for ii in range(len(ls_shift_dlambda.get_all_rays())):
    #   ls_shift_dlambda.get_all_rays()[ii].wavelength+=ls_shift_dlambda.get_all_rays()[ii].wavelength/100
    # ls_group.append(ls_shift_dlambda)
    
    point_group = []
    point_group.append(point_end)
    for ls in ls_group:
      comp = Composition()
      comp.set_geom(ls.get_geom())
      comp.set_light_source(ls)
      for element in self._elements:
        comp.add_fixed_elm(element)
      comp.set_sequence(self._sequence)
      comp.recompute_optical_axis()
      comp.propagate(self._last_prop)
      comp.compute_beams()
      point_group.append(comp.last_geom()[0])
      comp.propagate(shifting_distence)
      comp.compute_beams()
      point_group.append(comp.last_geom()[0])
      comp.draw_beams()
      del comp
    return point_group
      
    

def next_name(name, prefix=""):
  # generiert einen neuen namen aus dem alten Element
  ind = name.rfind("_")
  try:
    num = int(name[ind+1::])+1
  except:
    num = 1
  suffix = str(num) if num>9 else "0"+str(num)
  return prefix + name[0:ind] + "_" + suffix



