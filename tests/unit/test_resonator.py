# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.resonator (LinearResonator, CircularResonator)

Erwartungswerte stammen aus der Resonatortheorie (g-Parameter):
  g_i = 1 - L/R_i, stabil für 0 <= g1*g2 <= 1,
  z0 = L * sqrt(g1 g2 (1 - g1 g2)) / (g1 + g2 - 2 g1 g2),
  Strahltaille symmetrischer Resonatoren: z0 = sqrt(L (2R - L)) / 2.
Der Eigenmode q = z + i*z0 gilt in der Ebene vor dem ersten Element
(z = Abstand zur Taille).
"""
import unittest

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import (LinearResonator, CircularResonator, Mirror, Curved_Mirror,
                      Lens, Gaussian_Beam)

WAVELENGTH = 1030e-6


def two_mirror_resonator(L, R1, R2=None):
  R2 = R1 if R2 is None else R2
  res = LinearResonator()
  res.wavelength = WAVELENGTH
  res.add_on_axis(Curved_Mirror(radius=R1))
  res.propagate(L)
  res.add_on_axis(Curved_Mirror(radius=R2))
  return res


def fixed_point(M):
  A, B, C, D = np.asarray(M).ravel()
  z = (A - D) / (2 * C)
  return z + 1j * np.sqrt(-B / C - z**2 + 0j)


class TestLinearEigenmode(unittest.TestCase):

  def test_symmetric_resonator_waist_is_in_the_middle(self):
    L, R = 250.0, 400.0
    q = two_mirror_resonator(L, R).compute_eigenmode()
    self.assertAlmostEqual(q.real, L / 2, places=8)
    self.assertAlmostEqual(q.imag, 0.5 * np.sqrt(L * (2 * R - L)), places=8)

  def test_asymmetric_resonator_matches_g_parameter_formulas(self):
    L, R1, R2 = 200.0, 300.0, 500.0
    g1, g2 = 1 - L / R1, 1 - L / R2
    z0 = L * np.sqrt(g1 * g2 * (1 - g1 * g2)) / (g1 + g2 - 2 * g1 * g2)
    z = L * g2 * (1 - g1) / (g1 + g2 - 2 * g1 * g2)
    q = two_mirror_resonator(L, R1, R2).compute_eigenmode()
    self.assertAlmostEqual(q.imag, z0, places=8)
    self.assertAlmostEqual(q.real, z, places=8)

  def test_eigenmode_is_reproduced_by_the_round_trip_matrix(self):
    res = two_mirror_resonator(250, 400)
    q = res.compute_eigenmode()
    A, B, C, D = res.matrix().ravel()
    assert_allclose((A * q + B) / (C * q + D), q, rtol=1e-10)

  def test_round_trip_matrix_has_unit_determinant(self):
    res = two_mirror_resonator(250, 400)
    res.compute_eigenmode()
    self.assertAlmostEqual(np.linalg.det(res.matrix()), 1.0, places=10)

  def test_three_element_resonator_with_lens(self):
    res = LinearResonator()
    res.add_on_axis(Mirror())
    res.propagate(500)
    res.add_on_axis(Lens(f=250))
    res.propagate(270)
    res.add_on_axis(Mirror())
    q = res.compute_eigenmode()
    # Rundlauf: M0 -> Linse -> M2 -> Linse -> M0
    P = lambda d: np.array([[1, d], [0, 1.]])
    Lm = np.array([[1, 0], [-1 / 250, 1.]])
    M = P(500) @ Lm @ P(270) @ P(270) @ Lm @ P(500)
    assert_allclose(q, fixed_point(M), rtol=1e-9)

  def test_unstable_resonator_returns_minus_one(self):
    # g1 = g2 = 1 - 250/100 = -1.5 -> g1*g2 > 1
    self.assertEqual(two_mirror_resonator(250, 100).compute_eigenmode(), -1)

  def test_eigenmode_does_not_depend_on_wavelength(self):
    res = two_mirror_resonator(250, 400)
    q1 = res.compute_eigenmode()
    res.set_wavelength(2 * WAVELENGTH)
    q2 = res.compute_eigenmode()
    self.assertAlmostEqual(q1, q2, places=10)


class TestBeams(unittest.TestCase):

  def test_waist_radius_from_eigenmode(self):
    L, R = 250.0, 400.0
    res = two_mirror_resonator(L, R)
    beam = res.output_beam()
    z0 = 0.5 * np.sqrt(L * (2 * R - L))
    expected = np.sqrt(WAVELENGTH * z0 / np.pi * (1 + (L / 2 / z0)**2))
    self.assertIsInstance(beam, Gaussian_Beam)
    self.assertAlmostEqual(beam.radius(), expected, places=10)

  def test_beam_radius_scales_with_sqrt_wavelength(self):
    res = two_mirror_resonator(250, 400)
    w1 = res.output_beam().radius()
    res.set_wavelength(4 * WAVELENGTH)
    w2 = res.output_beam().radius()
    self.assertAlmostEqual(w2 / w1, 2.0, places=8)

  def test_beam_wavelength_follows_resonator(self):
    res = two_mirror_resonator(250, 400)
    self.assertAlmostEqual(res.output_beam().wavelength, WAVELENGTH)

  def test_set_wavelength_works_before_first_computation(self):
    res = LinearResonator()
    res.set_wavelength(5e-4)
    self.assertEqual(res.wavelength, 5e-4)


class TestCouplers(unittest.TestCase):

  def _resonator(self):
    res = LinearResonator()
    res.add_on_axis(Mirror())
    res.propagate(100)
    res.add_on_axis(Lens(f=100))
    res.propagate(100)
    res.add_on_axis(Mirror())
    return res

  def test_output_coupler_must_be_a_mirror(self):
    res = self._resonator()
    self.assertEqual(res.set_output_coupler_index(1), -1)
    self.assertEqual(res._output_coupler_index, 0)
    self.assertEqual(res.add_output_coupler(Lens()), -1)

  def test_output_coupler_index_can_be_set_to_a_mirror(self):
    res = self._resonator()
    res.set_output_coupler_index(2)
    self.assertEqual(res._output_coupler_index, 2)

  def test_add_output_coupler_sets_the_output_coupler_index(self):
    # Regression: früher Tippfehler "_out_putcoupler_index"
    res = LinearResonator()
    res.add_on_axis(Mirror())
    res.propagate(100)
    res.add_output_coupler(Mirror())
    self.assertEqual(res._output_coupler_index, 1)


class TestCircularResonator(unittest.TestCase):

  def _ring(self):
    """Ring aus 3 Spiegeln + Linse (auf der Strecke m0 -> m1)."""
    f = 150.0
    m0, m1, m2, le = Mirror(), Mirror(), Mirror(), Lens(f=f)
    for e, p in ((m0, (0, 0, 80)), (le, (0, 100, 80)), (m1, (0, 200, 80)),
                 (m2, (-100, 0, 80))):
      e.pos = p
    le.normal = (0, 1, 0)
    m0.set_normal_with_2_points(m2.pos, le.pos)
    m1.set_normal_with_2_points(le.pos, m2.pos)
    m2.set_normal_with_2_points(m1.pos, m0.pos)
    ring = CircularResonator()
    ring.wavelength = WAVELENGTH
    for e in (m0, le, m1, m2):
      ring.add_fixed_elm(e)
    P = lambda d: np.array([[1, d], [0, 1.]])
    Lm = np.array([[1, 0], [-1 / f, 1.]])
    M = P(100) @ P(np.hypot(100, 200)) @ P(100) @ Lm @ P(100)
    return ring, M

  def test_ring_geometry_is_closed(self):
    ring, _ = self._ring()
    ring.matrix()
    first, last = ring._elements[0], ring._elements[-1]
    self.assertAlmostEqual(np.linalg.norm(first.pos - last.pos), 100.0)

  def test_ring_eigenmode_matches_hand_calculated_round_trip(self):
    # Regression: früher wurde die Schlusspropagation doppelt gezählt und
    # dieser stabile Ring als "unstable" gemeldet.
    # Erwartet: q = fixed_point(P(l4) P(l3) P(l2) Lens P(l1)).
    ring, M = self._ring()
    q = ring.compute_eigenmode()
    assert_allclose(q, fixed_point(M), rtol=1e-9)

  def test_setting_last_element_requires_a_mirror(self):
    ring = CircularResonator()
    ring.add_on_axis(Mirror())
    ring.propagate(100)
    ring.add_on_axis(Lens(f=100))
    self.assertEqual(ring.Setting_last_element(), -1)


if __name__ == "__main__":
  unittest.main()
