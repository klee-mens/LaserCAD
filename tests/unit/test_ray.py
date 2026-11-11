# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.ray
"""
import unittest

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Ray, Geom_Object


def plane_at(pos, normal=(1, 0, 0)):
  """Hilfsobjekt: Ebene durch <pos> mit Normale <normal>."""
  g = Geom_Object()
  g.pos = pos
  g.normal = normal
  return g


class TestRayBasics(unittest.TestCase):

  def test_defaults(self):
    r = Ray()
    assert_allclose(r.pos, (0, 0, 80))
    assert_allclose(r.normal, (1, 0, 0))
    self.assertGreater(r.length, 0)
    self.assertAlmostEqual(r.wavelength, 660e-6)  # 660 nm, Angabe in mm

  def test_endpoint_is_pos_plus_length_times_normal(self):
    r = Ray()
    r.pos = (1, 2, 3)
    r.normal = (0, 1, 0)
    r.length = 50
    assert_allclose(r.endpoint(), (1, 52, 3), atol=1e-12)

  def test_endpoint_follows_a_changed_normal(self):
    r = Ray()
    r.length = 10
    r.normal = (0, 0, 1)
    assert_allclose(r.endpoint(), (0, 0, 90), atol=1e-12)


class TestRayIntersection(unittest.TestCase):

  def test_perpendicular_plane(self):
    r = Ray()
    p = r.intersection(plane_at((100, 0, 80)))
    assert_allclose(p, (100, 0, 80), atol=1e-12)

  def test_intersection_sets_length_by_default(self):
    r = Ray()
    r.intersection(plane_at((100, 0, 80)))
    self.assertAlmostEqual(r.length, 100)

  def test_intersection_can_leave_length_unchanged(self):
    r = Ray()
    old = r.length
    p = r.intersection(plane_at((100, 0, 80)), set_length=False)
    self.assertEqual(r.length, old)
    assert_allclose(p, (100, 0, 80), atol=1e-12)

  def test_oblique_ray_hits_plane_at_expected_point(self):
    r = Ray()
    r.normal = (1, 1, 0)
    p = r.intersection(plane_at((100, 0, 80)))
    assert_allclose(p, (100, 100, 80), atol=1e-12)
    self.assertAlmostEqual(r.length, 100 * np.sqrt(2))

  def test_tilted_plane(self):
    # Ebene mit Normale (1,1,0) durch (100,0,80): x + y = 100
    r = Ray()
    p = r.intersection(plane_at((100, 0, 80), normal=(1, 1, 0)))
    assert_allclose(p, (100, 0, 80), atol=1e-12)
    # Strahl in y-Richtung ab (0,0,80) trifft x+y=100 bei (0,100,80)
    r2 = Ray()
    r2.normal = (0, 1, 0)
    p2 = r2.intersection(plane_at((100, 0, 80), normal=(1, 1, 0)))
    assert_allclose(p2, (0, 100, 80), atol=1e-12)

  def test_plane_behind_the_ray_gives_negative_length(self):
    r = Ray()
    r.intersection(plane_at((-30, 0, 80)))
    self.assertAlmostEqual(r.length, -30)

  def test_result_does_not_depend_on_plane_normal_sign(self):
    r1, r2 = Ray(), Ray()
    p1 = r1.intersection(plane_at((100, 0, 80), normal=(1, 0, 0)))
    p2 = r2.intersection(plane_at((100, 0, 80), normal=(-1, 0, 0)))
    assert_allclose(p1, p2, atol=1e-12)

  def test_ray_position_and_direction_are_not_changed(self):
    r = Ray()
    r.pos = (1, 2, 3)
    r.normal = (1, 1, 0)
    r.intersection(plane_at((100, 0, 80)))
    assert_allclose(r.pos, (1, 2, 3))
    assert_allclose(r.normal, np.array((1, 1, 0)) / np.sqrt(2), atol=1e-12)


class TestRayHAlphaTheta(unittest.TestCase):

  def test_from_h_alpha_theta_axis_ray(self):
    # h=0, alpha=0: Strahl liegt exakt auf der Achse des Elements
    el = plane_at((100, 0, 80))
    r = Ray()
    r.from_h_alpha_theta(0, 0, 0, el)
    assert_allclose(r.pos, el.pos, atol=1e-12)
    assert_allclose(r.normal, el.normal, atol=1e-12)

  def test_from_h_alpha_theta_height_in_z_direction(self):
    # theta=0 bedeutet: der Strahl liegt bei +z des Elements
    el = plane_at((100, 0, 80))
    r = Ray()
    r.from_h_alpha_theta(5, 0, 0, el)
    assert_allclose(r.pos, (100, 0, 85), atol=1e-12)
    assert_allclose(r.normal, (1, 0, 0), atol=1e-12)

  def test_from_h_alpha_theta_positive_alpha_diverges_from_axis(self):
    # Konvention der Matrizenoptik: h>0 und alpha>0 -> Strahl läuft von der
    # Achse weg
    el = plane_at((100, 0, 80))
    r = Ray()
    r.from_h_alpha_theta(5, 0.1, 0, el)
    self.assertGreater(r.normal[2], 0)
    self.assertAlmostEqual(r.normal[2], np.sin(0.1), places=9)

  def test_from_h_alpha_theta_uses_geometry_of_the_element(self):
    # Element um 90° um z gedreht: Achse zeigt in +y, "oben" bleibt +z
    el = plane_at((0, 100, 80), normal=(0, 1, 0))
    r = Ray()
    r.from_h_alpha_theta(5, 0, 0, el)
    assert_allclose(r.pos, (0, 100, 85), atol=1e-12)
    assert_allclose(r.normal, (0, 1, 0), atol=1e-12)

  @unittest.expectedFailure
  def test_h_alpha_to_returns_height_and_angle(self):
    # BUG: Ray.h_alpha_to ruft self.angle_to(element.normal) auf, angle_to
    # erwartet aber ein Objekt mit .normal und bricht mit
    # "AttributeError: 'numpy.ndarray' object has no attribute 'normal'" ab.
    # Vermutlich soll es self.angle_to(element) heißen. Die Funktion wird im
    # Projekt bisher nirgends aufgerufen.
    r = Ray()
    r.pos = (0, 0, 85)
    h, alpha = r.h_alpha_to(plane_at((100, 0, 80)))
    self.assertAlmostEqual(h, 5)
    self.assertAlmostEqual(alpha, 0)

  @unittest.expectedFailure
  def test_h_alpha_theta_to_returns_height_and_angles(self):
    # gleiche Ursache wie oben (h_alpha_theta_to ruft h_alpha_to auf)
    r = Ray()
    r.pos = (0, 0, 85)
    h, alpha, theta = r.h_alpha_theta_to(plane_at((100, 0, 80)))
    self.assertAlmostEqual(h, 5)


if __name__ == "__main__":
  unittest.main()
