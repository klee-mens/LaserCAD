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
# from .intersection_plane import Intersection_plane
from ..freecad_models import warning, freecad_da, initialize_composition, add_to_composition
from ..freecad_models.freecad_model_element_holder import Model_element_holder
from .constants import xy_to_table_plus_offset
import numpy as np
from copy import deepcopy
from scipy.constants import speed_of_light
# speed_of_light = 3e8


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
    # self._catalogue = {}
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
    # item.name = self.new_catalogue_entry(item)
    item.name = self.name + "_" + item.name
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
    # old_sequence = self._sequence
    # sub_sequence = np.array(subcomp.get_sequence())
    # sub_sequence += max(old_sequence)
    # for element in subcomp._elements:
    #   self.add_fixed_elm(element)
    # for nonopt in subcomp.non_opticals:
    #   self.add_fixed_elm(nonopt)
    # self.set_sequence(old_sequence + list(sub_sequence))

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

  # def kostenbauder_matmul(self):
  #   """
  #   computes the optical matrix of the system
  #   each iteration consists of a propagation given by the length of the nth
  #   ray of the optical_axis followed by the matrix multiplication with the
  #   seq[n] element

  #   Returns the ABCD-matrix
  #   """
  #   self._kostenbauder = np.eye(4)
  #   self.recompute_optical_axis()
  #   counter = -1
  #   for ind in self._sequence:
  #     counter += 1
  #     B = self._optical_axis[counter].length
  #     moment_propa = np.eye(4)
  #     moment_propa[0,1] = B
  #     # moment_propa[0,1] = B *1e-3
  #     M = self._elements[ind].kostenbauder(inray = self._optical_axis[counter])

  #     print("Counter =", counter)
  #     print(moment_propa)
  #     print(M)

  #     self._kostenbauder = np.matmul( moment_propa, self._kostenbauder )
  #     self._kostenbauder = np.matmul( M, self._kostenbauder )

  #   last_propa = np.eye(4)
  #   last_propa[0,1] = self._last_prop
  #   # last_propa[0,1] = self._last_prop * 1e-3
  #   self._kostenbauder = np.matmul( last_propa, self._kostenbauder ) #last propagation
  #   return np.array(self._kostenbauder)

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
    # if self._last_prop >= 0:
      # beamlist[-1].set_length(self._last_prop)
    # else:
      # beamlist.pop(-1)
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

  def post_positions(self, verbose=False):
    post_coordinate_list = []
    for elm in self._elements:
      try:
        post = elm.Mount.mount_list[-1]
        xy = post.pos[0:2]
        if verbose:
          post_coordinate_list.append((elm.name, xy))
        else:
          post_coordinate_list.append(xy)
      except:
        print("No Post found for Element", elm.name)
    for non_optical in self.non_opticals:
      try:
        post = non_optical.Mount.mount_list[-1]
        xy = post.pos[0:2]
        if verbose:
          post_coordinate_list.append((non_optical.name, xy))
        else:
          post_coordinate_list.append(xy)
      except:
        print("No Post found for Element", non_optical.name)
    return post_coordinate_list

  def posts_pq_on_table(self, verbose=True):
    # Gives the postions in hole p, q coordiantes plus offset accodring to xy_to_table_plus_offset
    if verbose:
      return [(name, xy_to_table_plus_offset(*xy) ) for (name, xy) in self.post_positions(verbose=True)]
    else:
      return [xy_to_table_plus_offset(*xy) for xy in self.post_positions(verbose=False)]


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
    # key = item.class_name()
    key = item.name
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


  def Kostenbauder_matrix(self, reference_ray=None, dimension=4,
                           reference_axis="z", text_explanation=False):
    if reference_ray:
      ray0 = reference_ray
    else:
      ray0 = self._optical_axis[0]

    DeltaR = 1e-3 # 1 um displace
    DeltaPhi = 1e-6 # 1um rad
    DeltaLambda = ray0.wavelength * 1e-3

    z = np.array((0, 0, 1)) # Gravitanional axis
    y0 = np.cross(z, ray0.normal)
    if np.linalg.norm(y0) < 1-1e-3:
      print("Warning in Kostenbauder computation:")
      print("\t Starting ray is not in xy Plane.")
      print("\t This may cause strange ABCD entries")
    y0 *= 1/np.linalg.norm(y0) # better save than sorry

    ray_z = deepcopy(ray0)
    ray_z.pos += DeltaR * z

    ray_alpha = deepcopy(ray0)
    ray_alpha.rotate(vec=-y0, phi=DeltaPhi)

    ray_y = deepcopy(ray0)
    ray_y.pos += DeltaR * y0

    ray_beta = deepcopy(ray0)
    ray_beta.rotate(vec=z, phi=DeltaPhi)

    ray_lam = deepcopy(ray0)
    ray_lam.wavelength += DeltaLambda

    beam0 = Beam()
    beam0.override_rays([ray0, ray_z, ray_alpha, ray_y, ray_beta, ray_lam])

    computed_beams = self.compute_beams(external_source=beam0)
    endbeam = computed_beams[-1]
    endray0, endray_z, endray_alpha, endray_y, endray_beta, endray_lam = endbeam.get_all_rays(by_reference=True)

    # end triad
    xe = endray0.normal # reference for all angular computations
    ye = np.cross(z, xe)
    if np.linalg.norm(ye) < 1-1e-3:
      print("Warning in Kostenbauder computation:")
      print("\t End ray is not in xy Plane.")
      print("\t This may cause strange ABCD entries")
    ye *= 1/np.linalg.norm(ye) # norming

    endplane = Geom_Object()
    endplane.pos = endray0.endpoint()
    endplane.normal = xe

    dist_z = endray_z.intersection(endplane) - endplane.pos
    dist_y = endray_y.intersection(endplane) - endplane.pos
    dist_alpha = endray_alpha.intersection(endplane) - endplane.pos
    dist_beta = endray_beta.intersection(endplane) - endplane.pos
    dist_lam = endray_lam.intersection(endplane) - endplane.pos

    # optical path lengths
    opl0, opl_z, opl_alpha, opl_y, opl_beta, opl_lam = 0,0,0,0,0,0
    for com in computed_beams:
      crays = com.get_all_rays()
      opl0 += crays[0].length
      opl_z += crays[1].length
      opl_alpha += crays[2].length
      opl_y += crays[3].length
      opl_beta += crays[4].length
      opl_lam += crays[5].length

    dz2_dz = np.sum(dist_z * z) / DeltaR # si units
    dz2_dalpha = np.sum(dist_alpha * z) * 1e-3 / DeltaPhi # si units
    dz2_dy = np.sum(dist_y * z) / DeltaR # si units
    dz2_dbeta = np.sum(dist_beta * z) * 1e-3 / DeltaPhi # si units
    dz2_dlam = np.sum(dist_lam * z) / DeltaLambda # si units

    dy2_dz = np.sum(dist_z * ye) / DeltaR # si units
    dy2_dalpha = np.sum(dist_alpha * ye) * 1e-3 / DeltaPhi # si units
    dy2_dy = np.sum(dist_y * ye) / DeltaR # si units
    dy2_dbeta = np.sum(dist_beta * ye) * 1e-3 / DeltaPhi # si units
    dy2_dlam = np.sum(dist_lam * ye) / DeltaLambda # si units

    dalpha2_dz = np.arcsin(np.sum(np.cross(endray_z.normal, xe) * ye)) / (DeltaR*1e-3) # si units
    dalpha2_dy = np.arcsin(np.sum(np.cross(endray_y.normal, xe) * ye)) / (DeltaR*1e-3) # si units
    dalpha2_dalpha = np.arcsin(np.sum(np.cross(endray_alpha.normal, xe) * ye)) / DeltaPhi # si units
    dalpha2_dbeta = np.arcsin(np.sum(np.cross(endray_beta.normal, xe) * ye)) / DeltaPhi # si units
    dalpha2_dlam =  np.arcsin(np.sum(np.cross(endray_lam.normal, xe) * ye))/ (DeltaLambda * 1e-3) # si units

    dbeta2_dz = np.arcsin(np.sum(np.cross(xe, endray_z.normal) * z)) / (DeltaR*1e-3) # si units
    dbeta2_dy = np.arcsin(np.sum(np.cross(xe, endray_y.normal) * z)) / (DeltaR*1e-3) # si units
    dbeta2_dalpha = np.arcsin(np.sum(np.cross(xe, endray_alpha.normal) * z)) / DeltaPhi # si units
    dbeta2_dbeta = np.arcsin(np.sum(np.cross(xe, endray_beta.normal) * z)) / DeltaPhi # si units
    dbeta2_dlam =  np.arcsin(np.sum(np.cross(xe, endray_lam.normal) * z)) / (DeltaLambda * 1e-3) # si units

    c = speed_of_light # light speed in m / s
    dt2_dz = (opl_z - opl0)/c / DeltaR # si units
    dt2_dy = (opl_y - opl0)/c / DeltaR # si units
    dt2_dalpha = (opl_alpha - opl0)*1e-3/c / DeltaPhi # si units
    dt2_dbeta = (opl_beta - opl0)*1e-3/c / DeltaPhi # si units
    dt2_dlam = (opl_lam - opl0)/c / DeltaLambda # si units

    lam0 = ray0.wavelength * 1e-3
    dlam_dfreq = - (lam0)**2 / c # Kostenbauder took frequency, not wavelength

    textlines = []
    def txtline(str1, obj, str2):
      return str1 + str(obj) + str2
    textlines.append(txtline("dz2_dz: ", dz2_dz, " | Magnification z-z\n"))
    textlines.append(txtline("dz2_dalpha: ", dz2_dalpha*1e3, " mm | Propagation z-alpha\n"))
    textlines.append(txtline("dz2_dy: ", dz2_dy, "| Twisting z-y\n"))
    textlines.append(txtline("dz2_dbeta: ", dz2_dbeta*1e3, " mm | Twisting propagation z-beta\n"))
    textlines.append(txtline("dz2_dt: ", 0, " mm/s | Time dependence z-t, by definition 0\n"))
    textlines.append(txtline("dz2_dlam: ", dz2_dlam*1e3/(1e9), " mm/nm | Spatial chirp z-lambda\n"))
    textlines.append("\n")
    textlines.append(txtline("dalpha2_dz: ", dalpha2_dz*1e-3, " /mm | Focal power alpha-z\n"))
    textlines.append(txtline("dalpha2_dalpha: ", dalpha2_dalpha, " | Angular magnification alpha-alpha\n"))
    textlines.append(txtline("dalpha2_dy: ", dalpha2_dy*1e-3, " /mm | Twisting focal power alpha-y\n"))
    textlines.append(txtline("dalpha2_dbeta: ", dalpha2_dbeta, " | Twisting angular magnification alpha-beta\n"))
    textlines.append(txtline("dalpha2_dt: ", 0, " mrad/s | Time dependence alpha-t, by definition 0\n"))
    textlines.append(txtline("dalpha2_dlam: ", dalpha2_dlam*1e3/1e9, " mrad/nm | Angular chirp alpha-lambda\n"))
    textlines.append("\n")
    textlines.append(txtline("dy2_dz: ", dy2_dz, " | Twisting magnification y-z\n"))
    textlines.append(txtline("dy2_dalpha: ", dy2_dalpha*1e3, " mm | Twisting propagation y-alpha\n"))
    textlines.append(txtline("dy2_dy: ", dy2_dy, " | Magnification y-y\n"))
    textlines.append(txtline("dy2_dbeta: ", dy2_dbeta*1e3, " mm | Propagation y-beta\n"))
    textlines.append(txtline("dy2_dt: ", 0, " mm/s | Time dependence y-t, by definition 0\n"))
    textlines.append(txtline("dy2_dlam: ", dy2_dlam*1e3/1e9, " mm/nm | Spatial chirp y-lambda\n"))
    textlines.append("\n")
    textlines.append(txtline("dbeta2_dz: ", dbeta2_dz*1e-3, " /mm | Focal power beta-z\n"))
    textlines.append(txtline("dbeta2_dalpha: ", dbeta2_dalpha, " | Twisting angular magnification beta-alpha\n"))
    textlines.append(txtline("dbeta2_dy: ", dbeta2_dy*1e-3, " /mm | Focal power beta-y\n"))
    textlines.append(txtline("dbeta2_dbeta: ", dbeta2_dbeta, " | Angular magnification beta-beta\n"))
    textlines.append(txtline("dbeta2_dt: ", 0, " mrad/s | Time dependence beta-t, by definition 0\n"))
    textlines.append(txtline("dbeta2_dlam: ", dbeta2_dlam*1e3/1e9, " mrad/nm | Angular chirp beta-lambda\n"))
    textlines.append("\n")
    textlines.append(txtline("dt2_dz: ", dt2_dz*1e15/1e3, " fs/mm | Spatial pulse front tilt t-z\n"))
    textlines.append(txtline("dt2_dalpha: ", dt2_dalpha*1e15/1e3, " fs/mrad | Angular pulse front tilt t-alpha\n"))
    textlines.append(txtline("dt2_dy: ", dt2_dy*1e15/1e3, " fs/mm | Spatial pulse front tilt t-y\n"))
    textlines.append(txtline("dt2_dbeta: ", dt2_dbeta*1e15/1e3, " fs/mrad | Angular pulse front tilt t-beta\n"))
    textlines.append(txtline("dt2_dt: ", 1, " | Time dependence t-t, by definition 1\n"))
    textlines.append(txtline("dt2_dlam: ", dt2_dlam*dlam_dfreq/(2*np.pi)*1e30, " fs^2 | Group delay dispersion\n"))
    textlines.append("\n")
    textlines.append(txtline("df2_dz: ", 0, " f-z, by definition 0\n"))
    textlines.append(txtline("df2_dalpha: ", 0, " f-alpha, by definition 0\n"))
    textlines.append(txtline("df2_dy: ", 0, " f-y, by definition 0\n"))
    textlines.append(txtline("df2_dbeta: ", 0, " f-beta, by definition 0\n"))
    textlines.append(txtline("df2_dt: ", 0, " f-t, by definition 0\n"))
    textlines.append(txtline("df2_dlam: ", 1, " f-f, by definition 1\n"))

    if dimension == 4:
      if reference_axis == "z":
        KostenB = np.eye(4)
        KostenB[0,0] = dz2_dz # A
        KostenB[0,1] = dz2_dalpha # B
        KostenB[1,0] = dalpha2_dz # C
        KostenB[1,1] = dalpha2_dalpha # D
        KostenB[0,3] = dz2_dlam * dlam_dfreq # E
        KostenB[1,3] = dalpha2_dlam * dlam_dfreq# F
        KostenB[2,0] = dt2_dz # G
        KostenB[2,1] = dt2_dalpha # H
        KostenB[2,3] = dt2_dlam * dlam_dfreq # I

        if text_explanation:
          indices = [0, 1, 4, 5, 6]
          indices.extend([7, 8, 11, 12, 13])
          indices.extend([28, 29, 32, 33, 34])
          indices.extend([35, 36, 39, 40])
          txt4z = ""
          for ind in indices:
            txt4z += textlines[ind]
          return KostenB, txt4z
        return KostenB

      elif reference_axis == "y":
        KostenB = np.eye(4)
        KostenB[0,0] = dy2_dy # A
        KostenB[0,1] = dy2_dbeta # B
        KostenB[1,0] = dbeta2_dy # C
        KostenB[1,1] = dbeta2_dbeta # D
        KostenB[0,3] = dy2_dlam * dlam_dfreq # E
        KostenB[1,3] = dbeta2_dlam * dlam_dfreq# F
        KostenB[2,0] = dt2_dy # G
        KostenB[2,1] = dt2_dbeta # H
        KostenB[2,3] = dt2_dlam * dlam_dfreq # I

        if text_explanation:
          indices = [16, 17, 18, 19, 20]
          indices.extend([23, 24, 25, 26, 27])
          indices.extend([30, 31, 32, 33, 34])
          indices.extend([37, 38, 39, 40])
          txt4y = ""
          for ind in indices:
            txt4y += textlines[ind]
          return KostenB, txt4y
        return KostenB
      else:
        print("Usage: refrenece_axis = 'z' or 'y' when dimension = 4")
        return -1

    elif dimension == 6:
      KostenB = np.eye(6)
      KostenB[0,0] = dz2_dz # A
      KostenB[0,1] = dz2_dalpha # B
      KostenB[0,2] = dz2_dy
      KostenB[0,3] = dz2_dbeta
      KostenB[0,5] = dz2_dlam * dlam_dfreq

      KostenB[1,0] = dalpha2_dz # C
      KostenB[1,1] = dalpha2_dalpha # D
      KostenB[1,2] = dalpha2_dy
      KostenB[1,3] = dalpha2_dbeta
      KostenB[1,5] = dalpha2_dlam * dlam_dfreq

      KostenB[2,0] = dy2_dz # A
      KostenB[2,1] = dy2_dalpha # B
      KostenB[2,2] = dy2_dy
      KostenB[2,3] = dy2_dbeta
      KostenB[2,5] = dy2_dlam * dlam_dfreq

      KostenB[3,0] = dbeta2_dz # C
      KostenB[3,1] = dbeta2_dalpha # D
      KostenB[3,2] = dbeta2_dy
      KostenB[3,3] = dbeta2_dbeta
      KostenB[3,5] = dbeta2_dlam * dlam_dfreq

      KostenB[4,0] = dt2_dz
      KostenB[4,1] = dt2_dalpha
      KostenB[4,2] = dt2_dy
      KostenB[4,3] = dt2_dbeta
      KostenB[4,5] = dt2_dlam * dlam_dfreq

      if text_explanation:
        txt6 = ""
        for line in textlines:
          txt6 += line
        return KostenB, txt6
      return KostenB

    else:
      print("This dimension in not implemented. I don't know, try dimension = 4 or 6.")
      return -1



def next_name(name, prefix=""):
  # generiert einen neuen namen aus dem alten Element
  ind = name.rfind("_")
  try:
    num = int(name[ind+1::])+1
  except:
    num = 1
  suffix = str(num) if num>9 else "0"+str(num)
  return prefix + name[0:ind] + "_" + suffix



