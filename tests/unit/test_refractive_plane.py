# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.refractive_plane (brechende Ebene)

<relative_refractive_index> ist n2/n1, also das Verhältnis aus dem Index der
Seite, in die der Strahl läuft, und dem der Einfallsseite. Erwartungswerte
stammen aus dem Snelliusschen Brechungsgesetz sin(a1) = n2/n1 * sin(a2).
"""
import unittest
import warnings

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Ray
from LaserCAD.basic_optics import Refractive_plane

PLANE_POS = np.array((100.0, 0.0, 80.0))


def make_plane(n):
  plane = Refractive_plane(relative_refractive_index=n)
  plane.pos = PLANE_POS
  return plane


def ray_with_angle(deg, offset=(0, 0, 0)):
  """Strahl, der die Ebene (Normale +x) unter <deg> zur Normalen trifft."""
  a = np.radians(deg)
  r = Ray()
  r.normal = (np.cos(a), np.sin(a), 0)
  r.pos = PLANE_POS - 100 * r.normal + offset
  return r


class TestSnell(unittest.TestCase):

  def test_snell_law_into_denser_medium(self):
    plane = make_plane(1.5)
    for deg in (0, 10, 30, 60, 80):
      out = plane.next_ray(ray_with_angle(deg))
      sin_out = np.linalg.norm(out.normal[1:])
      assert_allclose(sin_out, np.sin(np.radians(deg)) / 1.5, atol=1e-12)

  def test_snell_law_into_thinner_medium(self):
    plane = make_plane(1 / 1.5)
    out = plane.next_ray(ray_with_angle(30))
    assert_allclose(out.normal[1], 0.75, atol=1e-12)     # sin = 1.5 * 0.5

  def test_normal_incidence_goes_straight(self):
    out = make_plane(1.5).next_ray(ray_with_angle(0))
    assert_allclose(out.normal, (1, 0, 0), atol=1e-14)

  def test_refracted_ray_is_normalized_and_keeps_its_plane(self):
    out = make_plane(1.5).next_ray(ray_with_angle(40))
    self.assertAlmostEqual(np.linalg.norm(out.normal), 1.0, places=12)
    self.assertAlmostEqual(out.normal[2], 0.0, places=14)
    self.assertGreater(out.normal[1], 0)           # bleibt auf derselben Seite

  def test_ray_continues_into_the_plane_direction(self):
    out = make_plane(1.5).next_ray(ray_with_angle(40))
    self.assertGreater(out.normal[0], 0)

  def test_new_ray_starts_on_the_plane(self):
    out = make_plane(1.5).next_ray(ray_with_angle(30, offset=(0, 4, 5)))
    self.assertAlmostEqual(out.pos[0], PLANE_POS[0], places=10)
    self.assertAlmostEqual(out.pos[1], 4.0, places=9)
    self.assertAlmostEqual(out.pos[2], 85.0, places=10)

  def test_input_ray_is_not_changed(self):
    r = ray_with_angle(30)
    normal, pos = r.normal.copy(), r.pos.copy()
    make_plane(1.5).next_ray(r)
    assert_allclose(r.normal, normal)
    assert_allclose(r.pos, pos)

  def test_two_planes_in_series_restore_the_direction(self):
    # Glas hinein (n) und wieder hinaus (1/n) -> Richtung wie zu Beginn
    front, back = make_plane(1.5), make_plane(1 / 1.5)
    back.pos = PLANE_POS + (5, 0, 0)
    r = ray_with_angle(35)
    out = back.next_ray(front.next_ray(r))
    assert_allclose(out.normal, r.normal, atol=1e-12)

  def test_tilted_plane_uses_its_own_normal(self):
    plane = make_plane(1.5)
    plane.normal = (np.cos(np.radians(20)), np.sin(np.radians(20)), 0)
    r = ray_with_angle(20)                         # fällt senkrecht ein
    out = plane.next_ray(r)
    assert_allclose(out.normal, r.normal, atol=1e-12)

  def test_wavelength_is_preserved(self):
    r = ray_with_angle(30)
    r.wavelength = 800e-6
    self.assertEqual(make_plane(1.5).next_ray(r).wavelength, 800e-6)

  def test_total_internal_reflection_reflects_the_ray(self):
    # sin(a) * n1/n2 > 1: früher unphysikalische, negierte Richtung
    plane = make_plane(1 / 1.5)
    r = ray_with_angle(60)
    with warnings.catch_warnings():
      warnings.simplefilter("error")          # auch keine NumPy-Warnung
      out = plane.next_ray(r)
    assert_allclose(out.normal, (-r.normal[0], r.normal[1], r.normal[2]),
                    atol=1e-12)
    self.assertAlmostEqual(out.pos[0], PLANE_POS[0], places=10)

  def test_critical_angle_separates_refraction_and_reflection(self):
    plane = make_plane(1 / 1.5)
    crit = np.degrees(np.arcsin(1 / 1.5))       # 41.81 Grad
    below = plane.next_ray(ray_with_angle(crit - 0.5)).normal
    above = plane.next_ray(ray_with_angle(crit + 0.5)).normal
    self.assertGreater(below[0], 0)             # gebrochen: weiter in +x
    self.assertLess(above[0], 0)                # total reflektiert: zurück

  def test_reflected_ray_is_normalized(self):
    out = make_plane(1 / 1.5).next_ray(ray_with_angle(70))
    self.assertAlmostEqual(np.linalg.norm(out.normal), 1.0, places=12)


if __name__ == "__main__":
  unittest.main()
