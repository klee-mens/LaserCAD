# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.grating (Reflexionsgitter)

Erwartungswerte stammen aus der Gittergleichung
  sin(alpha) + sin(beta) = m * lambda / d
mit den vorzeichenbehafteten Winkeln, wie sie Grating.angle_of_incidence
liefert (arctan(ry/rx), also beide zur Gitternormalen gemessen), sowie aus
dem Littrow-Fall (Strahl läuft in sich selbst zurück).

Hinweis: <grat_const> ist die Gitterperiode d in mm (nicht Linien/mm).
Die Ordnung m wird relativ zur Einfallsrichtung gezählt: das Vorzeichen des
Gittervektors folgt dem der Einfallskomponente in der Gitterebene.
"""
import unittest

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Grating, Ray

GRAT_POS = np.array((100.0, 0.0, 80.0))
WAVELENGTH = 1030e-6          # mm
PERIOD = 1e-3                 # mm -> 1000 Linien/mm


def make_grating(order=-1, period=PERIOD):
  g = Grating(grat_const=period, order=order)
  g.pos = GRAT_POS
  return g


def incoming(alpha, wavelength=WAVELENGTH):
  """Strahl in der xy-Ebene (Gittervektor y), Einfallswinkel alpha zur Normalen."""
  r = Ray()
  r.wavelength = wavelength
  r.normal = (np.cos(alpha), np.sin(alpha), 0)
  r.pos = GRAT_POS - 100 * r.normal       # trifft das Gitter in GRAT_POS
  return r


class TestGratingEquation(unittest.TestCase):

  def test_grating_equation_for_several_angles_and_wavelengths(self):
    g = make_grating()
    for wl in (800e-6, 1030e-6):
      for deg in (30, 45, 60):
        r_in = incoming(np.radians(deg), wl)
        r_out = g.next_ray(r_in)
        s_in = np.sin(g.angle_of_incidence(r_in))
        s_out = np.sin(g.angle_of_incidence(r_out))
        # m = -1 relativ zur Einfallsrichtung -> Summe der Sinus = +lambda/d
        assert_allclose(s_in + s_out, wl / PERIOD, atol=1e-12)

  def test_output_ray_is_normalized(self):
    g = make_grating()
    out = g.next_ray(incoming(np.radians(45)))
    self.assertAlmostEqual(np.linalg.norm(out.normal), 1.0, places=12)

  def test_output_starts_at_the_grating(self):
    g = make_grating()
    out = g.next_ray(incoming(np.radians(45)))
    assert_allclose(out.pos, GRAT_POS, atol=1e-9)

  def test_output_is_reflected_to_the_incident_side(self):
    g = make_grating()
    out = g.next_ray(incoming(np.radians(45)))
    self.assertLess(np.dot(out.normal, g.normal), 0)

  def test_stays_in_plane_of_incidence_for_in_plane_ray(self):
    g = make_grating()
    out = g.next_ray(incoming(np.radians(45)))
    self.assertAlmostEqual(out.normal[2], 0.0, places=12)

  def test_wavelength_is_preserved(self):
    g = make_grating()
    out = g.next_ray(incoming(np.radians(45), 900e-6))
    self.assertEqual(out.wavelength, 900e-6)

  def test_longer_wavelength_is_diffracted_further(self):
    g = make_grating()
    a = np.radians(45)
    b_short = abs(g.angle_of_incidence(g.next_ray(incoming(a, 800e-6))))
    b_long = abs(g.angle_of_incidence(g.next_ray(incoming(a, 1030e-6))))
    self.assertNotAlmostEqual(b_short, b_long, places=3)

  def test_order_minus_two_obeys_grating_equation(self):
    g = make_grating(period=2 * PERIOD)       # damit die 2. Ordnung existiert
    r_in = incoming(np.radians(30))
    out = g.next_ray(r_in, alternative_order=-2)
    s = np.sin(g.angle_of_incidence(r_in)) + np.sin(g.angle_of_incidence(out))
    assert_allclose(s, 2 * WAVELENGTH / (2 * PERIOD), atol=1e-12)

  def test_diffraction_order_attribute_is_used(self):
    r_in = incoming(np.radians(30))
    a = make_grating(order=-2, period=2 * PERIOD).next_ray(r_in)
    b = make_grating(order=-1, period=2 * PERIOD).next_ray(r_in,
                                                          alternative_order=-2)
    assert_allclose(a.normal, b.normal, atol=1e-14)


class TestLittrow(unittest.TestCase):

  def test_littrow_ray_returns_on_itself(self):
    g = make_grating()
    alpha = np.arcsin(WAVELENGTH / PERIOD / 2)
    r_in = incoming(alpha)
    out = g.next_ray(r_in)
    assert_allclose(out.normal, -r_in.normal, atol=1e-12)


class TestNoDiffraction(unittest.TestCase):

  def test_evanescent_order_returns_default_ray(self):
    g = make_grating()
    out = g.next_ray(incoming(np.radians(10)), alternative_order=-5)
    # Konvention: ein Standard-Ray() als deutlich sichtbarer Fehler
    assert_allclose(out.pos, Ray().pos)
    assert_allclose(out.normal, Ray().normal)

  def test_order_one_on_the_wrong_side_is_not_diffracted(self):
    g = make_grating()
    out = g.next_ray(incoming(np.radians(45)), alternative_order=1)
    assert_allclose(out.normal, Ray().normal)

  def test_alternative_order_zero_gives_the_specular_reflection(self):
    # Regression: 0 wurde früher wie "nicht gesetzt" behandelt (-> Ordnung -1)
    g = make_grating()
    r_in = incoming(np.radians(45))
    out = g.next_ray(r_in, alternative_order=0)
    expected = np.array((-np.cos(np.radians(45)), np.sin(np.radians(45)), 0))
    assert_allclose(out.normal, expected, atol=1e-12)


class TestAngleOfIncidence(unittest.TestCase):

  def test_normal_incidence_is_zero(self):
    g = make_grating()
    self.assertAlmostEqual(g.angle_of_incidence(incoming(0.0)), 0.0)

  def test_sign_follows_the_grating_vector(self):
    g = make_grating()
    self.assertAlmostEqual(g.angle_of_incidence(incoming(np.radians(20))),
                           np.radians(20))
    self.assertAlmostEqual(g.angle_of_incidence(incoming(np.radians(-20))),
                           np.radians(-20))


class TestGratingMatrix(unittest.TestCase):

  def test_matrix_is_cos_ratio_and_has_unit_determinant(self):
    g = make_grating()
    r_in = incoming(np.radians(50))
    out = g.next_ray(r_in)
    A = np.cos(g.angle_of_incidence(out)) / np.cos(g.angle_of_incidence(r_in))
    M = g.matrix(r_in)
    assert_allclose(M, [[A, 0], [0, 1 / A]], atol=1e-12)
    self.assertAlmostEqual(np.linalg.det(M), 1.0, places=12)

  def test_littrow_matrix_is_identity(self):
    g = make_grating()
    r_in = incoming(np.arcsin(WAVELENGTH / PERIOD / 2))
    assert_allclose(g.matrix(r_in), np.eye(2), atol=1e-12)

  def test_beam_expands_when_exit_angle_is_larger(self):
    g = make_grating()
    r_in = incoming(np.radians(50))      # Austritt flacher -> cos größer
    self.assertGreater(g.matrix(r_in)[0, 0], 1.0)


if __name__ == "__main__":
  unittest.main()
