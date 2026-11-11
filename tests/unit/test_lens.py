# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.lens (dünne Linse)

Die dünne Linse arbeitet in paraxialer Näherung (ABCD-Matrix wird auf die
Winkel selbst angewendet, nicht auf deren Tangens). Für Strahlen nahe der
Achse stimmen die Ergebnisse sehr gut mit der geometrischen Optik überein, die
relative Abweichung wächst etwa mit (h/f)^2/3. Die Tests verwenden deshalb
kleine Strahlhöhen bzw. Winkel und passende Toleranzen.
"""
import unittest

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Lens, Ray
from helpers import axis_crossing

LENS_POS = np.array((100.0, 0.0, 80.0))


def make_lens(f=100, normal=None):
  lens = Lens(f=f)
  lens.pos = LENS_POS
  if normal is not None:
    lens.normal = normal
  return lens


def parallel_ray(offset):
  """Achsenparalleler Strahl in x-Richtung mit Versatz <offset> (Vektor)."""
  r = Ray()
  r.pos = LENS_POS - (100, 0, 0) + offset
  return r


class TestLensMatrix(unittest.TestCase):

  def test_matrix_of_a_thin_lens(self):
    M = make_lens(f=100).matrix()
    assert_allclose(M, [[1, 0], [-1 / 100, 1]], atol=1e-15)

  def test_changing_the_focal_length_updates_the_matrix(self):
    lens = make_lens(f=100)
    lens.focal_length = 50
    self.assertEqual(lens.focal_length, 50)
    self.assertAlmostEqual(lens.matrix()[1, 0], -1 / 50)

  def test_negative_focal_length_gives_positive_C(self):
    self.assertGreater(make_lens(f=-80).matrix()[1, 0], 0)

  def test_matrix_returns_a_copy(self):
    lens = make_lens(f=100)
    M = lens.matrix()
    M[1, 0] = 123
    self.assertAlmostEqual(lens.matrix()[1, 0], -1 / 100)


class TestLensFocusing(unittest.TestCase):

  def test_parallel_rays_cross_the_axis_at_the_focal_length(self):
    h = 0.1
    offsets = {"+z": (0, 0, h), "-z": (0, 0, -h),
               "+y": (0, h, 0), "-y": (0, -h, 0)}
    for f in (100, 50, 250, -80):
      for label, off in offsets.items():
        with self.subTest(f=f, offset=label):
          lens = make_lens(f=f)
          out = lens.next_ray(parallel_ray(np.array(off)))
          s, miss = axis_crossing(out, lens.pos, lens.normal)
          self.assertAlmostEqual(miss, 0, places=6)
          self.assertAlmostEqual(s / f, 1, places=5)

  def test_rays_from_the_same_height_diverge_after_a_negative_lens(self):
    lens = make_lens(f=-80)
    out = lens.next_ray(parallel_ray(np.array((0, 0, 0.1))))
    self.assertGreater(out.normal[2], 0)  # läuft von der Achse weg

  def test_axis_ray_is_not_deflected(self):
    lens = make_lens()
    out = lens.next_ray(parallel_ray(np.zeros(3)))
    assert_allclose(out.normal, (1, 0, 0), atol=1e-12)
    assert_allclose(out.pos, LENS_POS, atol=1e-12)

  def test_tilted_ray_through_the_lens_center_is_not_deflected(self):
    lens = make_lens()
    r = Ray()
    r.pos = (0, -10, 80)
    r.normal = (1, 0.1, 0)   # trifft die Linse bei (100, 0, 80)
    out = lens.next_ray(r)
    assert_allclose(out.pos, LENS_POS, atol=1e-9)
    assert_allclose(out.normal, r.normal, atol=1e-12)

  def test_output_ray_starts_on_the_lens_plane(self):
    lens = make_lens()
    out = lens.next_ray(parallel_ray(np.array((0, 0, 3.0))))
    self.assertAlmostEqual(out.pos[0], LENS_POS[0])

  def test_ray_height_is_unchanged_at_the_lens(self):
    lens = make_lens()
    out = lens.next_ray(parallel_ray(np.array((0, 2.0, 3.0))))
    assert_allclose(out.pos, (100, 2, 83), atol=1e-12)

  def test_output_direction_is_a_unit_vector(self):
    lens = make_lens()
    out = lens.next_ray(parallel_ray(np.array((0, 2.0, 3.0))))
    self.assertAlmostEqual(np.linalg.norm(out.normal), 1.0)

  def test_deflection_is_independent_of_the_azimuth(self):
    # Rotationssymmetrie: gleicher Abstand -> gleicher Ablenkwinkel
    lens = make_lens()
    h = 3.0
    angles = []
    for phi in np.linspace(0, 2 * np.pi, 8, endpoint=False):
      off = np.array((0, h * np.cos(phi), h * np.sin(phi)))
      out = lens.next_ray(parallel_ray(off))
      angles.append(np.arccos(np.clip(out.normal[0], -1, 1)))
    assert_allclose(angles, angles[0], atol=1e-12)

  def test_input_ray_is_not_modified(self):
    lens = make_lens()
    r = parallel_ray(np.array((0, 0, 3.0)))
    lens.next_ray(r)
    assert_allclose(r.pos, (0, 0, 83), atol=1e-12)
    assert_allclose(r.normal, (1, 0, 0), atol=1e-12)

  def test_flipped_lens_focuses_just_the_same(self):
    # Linse "falsch herum" (Normale gegen die Ausbreitungsrichtung)
    lens = make_lens(f=100, normal=(-1, 0, 0))
    out = lens.next_ray(parallel_ray(np.array((0, 0, 0.1))))
    s, miss = axis_crossing(out, lens.pos, (1, 0, 0))
    self.assertAlmostEqual(miss, 0, places=6)
    self.assertAlmostEqual(s / 100, 1, places=5)

  def test_lens_along_the_y_axis(self):
    # Gesamter Aufbau um 90° um z gedreht: Achse in +y
    lens = Lens(f=100)
    lens.pos = (0, 100, 80)
    lens.normal = (0, 1, 0)
    r = Ray()
    r.pos = (0.1, 0, 80)
    r.normal = (0, 1, 0)
    out = lens.next_ray(r)
    s, miss = axis_crossing(out, lens.pos, lens.normal)
    self.assertAlmostEqual(miss, 0, places=6)
    self.assertAlmostEqual(s / 100, 1, places=5)

  def test_paraxial_approximation_error_is_small_but_nonzero(self):
    # Dokumentiert die Näherung: bei h=5 mm, f=100 mm liegt der Fokus bei
    # f * h/tan(h/f), also ca. 0.08 % zu kurz. Fällt dieser Test, wurde die
    # Linse auf exakte (tan-basierte) Rechnung umgestellt, dann bitte die
    # Toleranzen der anderen Tests überprüfen.
    lens = make_lens(f=100)
    out = lens.next_ray(parallel_ray(np.array((0, 0, 5.0))))
    s, _ = axis_crossing(out, lens.pos, lens.normal)
    self.assertAlmostEqual(s, 100 * 0.05 / np.tan(0.05), places=6)
    self.assertLess(s, 100)


class TestLensImaging(unittest.TestCase):

  def test_imaging_equation(self):
    # 1/s + 1/s' = 1/f  mit s=250, f=100  ->  s' = 166.667
    f, s_obj = 100, 250
    lens = Lens(f=f)
    lens.pos = (s_obj, 0, 80)
    expected_image = 1 / (1 / f - 1 / s_obj)
    for angle in (0.001, -0.001, 0.002):
      with self.subTest(angle=angle):
        r = Ray()
        r.pos = (0, 0, 80)
        r.normal = (1, 0, angle)
        out = lens.next_ray(r)
        s, miss = axis_crossing(out, lens.pos, lens.normal)
        self.assertAlmostEqual(miss, 0, places=5)
        self.assertAlmostEqual(s / expected_image, 1, places=4)

  def test_object_in_the_focal_plane_gives_collimated_rays(self):
    lens = Lens(f=100)
    lens.pos = (100, 0, 80)
    r = Ray()
    r.pos = (0, 0, 80)
    r.normal = (1, 0, 0.001)
    out = lens.next_ray(r)
    # Quelle in der Brennebene -> kollimiertes Bündel: der Strahl verlässt die
    # Linse (nahezu) parallel zur optischen Achse, trotz seines Startwinkels.
    self.assertLess(abs(out.normal[2]), 1e-5)


if __name__ == "__main__":
  unittest.main()
