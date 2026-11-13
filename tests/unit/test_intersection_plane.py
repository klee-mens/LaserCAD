# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.intersection_plane (Intersection_plane)

Die Schnittebene ändert die Strahlrichtung nicht, sie setzt den Strahl nur auf
die Ebene. spot_diagram liefert die Auftreffpunkte in Ebenenkoordinaten
(horizontale Achse in der Ebene, z-Achse).
"""
import unittest

import matplotlib
matplotlib.use("Agg")          # keine Fenster beim Testlauf
import matplotlib.pyplot as plt

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Ray
from LaserCAD.basic_optics import Intersection_plane

POS = np.array((100.0, 0.0, 80.0))


def make_plane(dia=50):
  plane = Intersection_plane(dia=dia)
  plane.pos = POS
  return plane


def ray_to(offset, direction=(1, 0, 0)):
  r = Ray()
  r.normal = direction
  r.pos = POS - 100 * r.normal + offset
  return r


class TestNextRay(unittest.TestCase):

  def test_ray_is_moved_onto_the_plane(self):
    out = make_plane().next_ray(ray_to((0, 3, 4)))
    assert_allclose(out.pos, (100, 3, 84), atol=1e-12)

  def test_direction_is_unchanged(self):
    d = np.array((np.cos(0.3), np.sin(0.3), 0))
    out = make_plane().next_ray(ray_to((0, 0, 0), d))
    assert_allclose(out.normal, d, atol=1e-14)

  def test_oblique_ray_hits_the_plane(self):
    d = np.array((np.cos(0.3), np.sin(0.3), 0))
    r = ray_to((0, 3, 4), d)
    out = make_plane().next_ray(r)
    self.assertAlmostEqual(out.pos[0], POS[0], places=10)
    assert_allclose(out.pos - r.pos, np.dot(out.pos - r.pos, d) * d, atol=1e-10)

  def test_tilted_plane(self):
    plane = make_plane()
    plane.normal = (np.cos(0.5), np.sin(0.5), 0)
    out = plane.next_ray(ray_to((0, 0, 0)))
    self.assertAlmostEqual(np.dot(out.pos - POS, plane.normal), 0.0, places=10)

  def test_matrix_is_identity(self):
    assert_allclose(make_plane().matrix(), np.eye(2))

  def test_aperture_follows_dia(self):
    self.assertEqual(make_plane(dia=80).aperture, 80)


class TestSpotDiagram(unittest.TestCase):

  def test_points_in_plane_coordinates(self):
    plane = make_plane()
    xs, ys = plane.spot_diagram([ray_to((0, 1, 2)), ray_to((0, -1, 3)),
                                 ray_to((0, 0, 0))])
    assert_allclose(xs, [1, -1, 0], atol=1e-12)
    assert_allclose(ys, [2, 3, 0], atol=1e-12)

  def test_dia_grows_to_contain_all_points(self):
    plane = make_plane(dia=10)
    plane.spot_diagram([ray_to((0, 30, 40)), ray_to((0, 0, 0))])
    self.assertGreaterEqual(plane.aperture, 50.0 - 1e-9)

  def test_accepts_a_beam(self):
    from LaserCAD import Beam
    plane = make_plane()
    beam = Beam(radius=2.0, angle=0)
    xs, ys = plane.spot_diagram(beam)
    self.assertEqual(len(xs), len(ys))
    self.assertGreater(len(xs), 1)
    self.assertLessEqual(max(abs(np.array(xs))), 2.0 + 1e-6)

  def test_repr_contains_class_name_and_dia(self):
    self.assertTrue(repr(make_plane(dia=50)).startswith("Intersection_plane(dia=50"))
    
  def tearDown(self):
    plt.close("all")


if __name__ == "__main__":
  unittest.main()
