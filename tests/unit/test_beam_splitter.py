# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.beam_splitter

ThinBeamsplitter: Transmission geht geradeaus durch, Reflexion wie ein Spiegel.
ThickBeamsplitter: planparallele Platte (Dicke d, Brechzahl n). Ein Strahl
verlässt sie parallel zur ursprünglichen Richtung, seitlich versetzt um
  s = d * sin(a) * (1 - cos(a) / sqrt(n^2 - sin^2(a)))
bei Einfallswinkel a zur Plattennormalen.
TFP56: Dünnschichtpolarisator mit 56° Einfallswinkel.
"""
import unittest

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Ray, Beam
from LaserCAD.basic_optics import (ThinBeamsplitter, ThickBeamsplitter, TFP56,
                                   Rectangular_Beamsplitter,
                                   Rectangular_Thin_Beamsplitter)

POS = np.array((100.0, 0.0, 80.0))


def placed(obj):
  obj.pos = POS
  return obj


def incoming(direction=(1, 0, 0)):
  r = Ray()
  d = np.array(direction, dtype=float)
  r.normal = d
  r.pos = POS - 100 * r.normal
  return r


def plate_shift(d, n, aoi_deg):
  a = np.radians(aoi_deg)
  return d * np.sin(a) * (1 - np.cos(a) / np.sqrt(n**2 - np.sin(a)**2))


class TestThinBeamsplitter(unittest.TestCase):

  def test_transmission_passes_straight(self):
    out = placed(ThinBeamsplitter()).next_ray(incoming())
    assert_allclose(out.normal, (1, 0, 0), atol=1e-14)
    assert_allclose(out.pos, POS, atol=1e-12)

  def test_reflection_at_45_degrees_turns_by_90(self):
    bs = placed(ThinBeamsplitter(transmission=False))
    out = bs.next_ray(incoming())
    assert_allclose(out.normal, (0, 1, 0), atol=1e-12)

  def test_reflection_angle_follows_angle_of_incidence(self):
    for aoi in (30, 45, 56, 70):
      bs = placed(ThinBeamsplitter(angle_of_incidence=aoi, transmission=False))
      out = bs.next_ray(incoming())
      deflection = np.degrees(np.arccos(np.dot((1, 0, 0), out.normal)))
      # Winkel zwischen Ein- und Ausfallsrichtung: 180 - 2 * aoi
      self.assertAlmostEqual(deflection, 180 - 2 * aoi, places=6)

  def test_default_is_transmission(self):
    self.assertTrue(ThinBeamsplitter().transmission)

  def test_next_beam_returns_selected_and_stores_alternative(self):
    bs = placed(ThinBeamsplitter())
    beam = Beam(radius=1.0, angle=0)
    out = bs.next_beam(beam)
    assert_allclose(out.normal, (1, 0, 0), atol=1e-12)
    assert_allclose(bs.get_output_beam().normal, (1, 0, 0), atol=1e-12)
    assert_allclose(bs.get_alternative_beam().normal, (0, 1, 0), atol=1e-12)
    assert_allclose(bs.get_input_beam().normal, beam.normal, atol=1e-12)

  def test_next_beam_keeps_the_transmission_flag(self):
    for flag in (True, False):
      bs = placed(ThinBeamsplitter(transmission=flag))
      bs.next_beam(Beam(radius=1.0, angle=0))
      self.assertEqual(bs.transmission, flag)

  def test_reflection_mode_swaps_output_and_alternative(self):
    bs = placed(ThinBeamsplitter(transmission=False))
    out = bs.next_beam(Beam(radius=1.0, angle=0))
    assert_allclose(out.normal, (0, 1, 0), atol=1e-12)
    assert_allclose(bs.get_alternative_beam().normal, (1, 0, 0), atol=1e-12)

  def test_input_beam_is_a_snapshot(self):
    bs = placed(ThinBeamsplitter())
    beam = Beam(radius=1.0, angle=0)
    bs.next_beam(beam)
    beam.normal = (0, 1, 0)                 # Original danach verändern
    assert_allclose(bs.get_input_beam().normal, (1, 0, 0), atol=1e-12)

  def test_getters_return_copies(self):
    bs = placed(ThinBeamsplitter())
    bs.next_beam(Beam(radius=1.0, angle=0))
    bs.get_output_beam().pos = (9, 9, 9)
    self.assertFalse(np.allclose(bs.get_output_beam().pos, (9, 9, 9)))


class TestThickBeamsplitter(unittest.TestCase):

  def test_transmission_keeps_direction(self):
    bs = placed(ThickBeamsplitter(thickness=5, refractive_index=1.5))
    out = bs.next_ray(incoming())
    assert_allclose(out.normal, (1, 0, 0), atol=1e-12)

  def test_lateral_shift_matches_plate_formula(self):
    for d, n in ((5, 1.5), (10, 1.45), (3, 2.0)):
      bs = placed(ThickBeamsplitter(thickness=d, refractive_index=n))
      out = bs.next_ray(incoming())
      shift = plate_shift(d, n, 45)
      # Versatz senkrecht zur ursprünglichen Strahlrichtung (hier y, Betrag)
      self.assertAlmostEqual(abs(out.pos[1]), shift, places=9)

  def test_exit_point_lies_on_the_back_surface(self):
    bs = placed(ThickBeamsplitter(thickness=5, refractive_index=1.5))
    out = bs.next_ray(incoming())
    self.assertAlmostEqual(np.dot(out.pos - POS, bs.normal), 5.0, places=9)

  def test_reflection_is_a_front_surface_mirror(self):
    bs = placed(ThickBeamsplitter(transmission=False))
    out = bs.next_ray(incoming())
    assert_allclose(out.normal, (0, 1, 0), atol=1e-12)
    assert_allclose(out.pos, POS, atol=1e-12)

  def test_thicker_plate_shifts_more(self):
    a = placed(ThickBeamsplitter(thickness=3)).next_ray(incoming())
    b = placed(ThickBeamsplitter(thickness=9)).next_ray(incoming())
    self.assertGreater(abs(b.pos[1]), abs(a.pos[1]))

  def test_input_ray_unchanged(self):
    r = incoming()
    placed(ThickBeamsplitter()).next_ray(r)
    assert_allclose(r.normal, (1, 0, 0))

  def test_ray_from_the_back_side_keeps_its_direction(self):
    # Regression: früher stand an der Rückseite beim Eintritt 1/n statt n
    bs = placed(ThickBeamsplitter(thickness=5, refractive_index=1.5))
    r = Ray()
    r.normal = (-1, 0, 0)
    r.pos = POS + (100, 0, 0)
    out = bs.next_ray(r)
    assert_allclose(out.normal, (-1, 0, 0), atol=1e-9)

  def test_back_side_shift_has_the_same_size_as_front_side(self):
    bs = placed(ThickBeamsplitter(thickness=5, refractive_index=1.5))
    r = Ray()
    r.normal = (-1, 0, 0)
    r.pos = POS + (100, 0, 0)
    out = bs.next_ray(r)
    self.assertAlmostEqual(abs(out.pos[1]), plate_shift(5, 1.5, 45), places=9)
    # Austritt auf der Vorderseite (Ebene durch POS)
    self.assertAlmostEqual(np.dot(out.pos - POS, bs.normal), 0.0, places=9)

  def test_back_and_front_pass_are_reversible(self):
    # Hin und zurück durch die Platte ergibt den Ausgangsstrahl
    bs = placed(ThickBeamsplitter(thickness=5, refractive_index=1.5))
    fwd = bs.next_ray(incoming())
    back = Ray()
    back.pos = fwd.pos
    back.normal = -fwd.normal
    back_out = bs.next_ray(back)
    assert_allclose(back_out.pos, POS, atol=1e-9)
    assert_allclose(back_out.normal, (-1, 0, 0), atol=1e-9)


class TestTFP56(unittest.TestCase):

  def test_angle_of_incidence_is_56(self):
    self.assertEqual(TFP56().angle_of_incidence, 56)

  def test_reflection_turns_by_68_degrees(self):
    tfp = placed(TFP56())
    tfp.transmission = False
    out = tfp.next_ray(incoming())
    deflection = np.degrees(np.arccos(np.dot((1, 0, 0), out.normal)))
    self.assertAlmostEqual(deflection, 68.0, places=6)

  def test_transmission_keeps_direction_with_a_shift(self):
    tfp = placed(TFP56())
    out = tfp.next_ray(incoming())
    assert_allclose(out.normal, (1, 0, 0), atol=1e-12)
    self.assertAlmostEqual(abs(out.pos[1]),
                           plate_shift(tfp.thickness, tfp.refractive_index, 56),
                           places=9)

  def test_flipping_the_sign_of_phi_mirrors_the_reflection(self):
    a = placed(TFP56())
    a.transmission = False
    b = placed(TFP56())
    b.transmission = False
    b.angle_positiv = False
    b.update_phi()
    ya = a.next_ray(incoming()).normal[1]
    yb = b.next_ray(incoming()).normal[1]
    self.assertAlmostEqual(ya, -yb, places=9)


class TestRectangularBeamsplitters(unittest.TestCase):

  def test_rectangular_thick_has_size_and_works_like_thick(self):
    bs = placed(Rectangular_Beamsplitter(height=20, width=30, thickness=5,
                                         refractive_index=1.5))
    self.assertEqual((bs.height, bs.width), (20, 30))
    out = bs.next_ray(incoming())
    assert_allclose(out.normal, (1, 0, 0), atol=1e-12)
    self.assertAlmostEqual(abs(out.pos[1]), plate_shift(5, 1.5, 45), places=9)

  def test_rectangular_thin_reflects_like_thin(self):
    bs = placed(Rectangular_Thin_Beamsplitter(transmission=False))
    assert_allclose(bs.next_ray(incoming()).normal, (0, 1, 0), atol=1e-12)


if __name__ == "__main__":
  unittest.main()
