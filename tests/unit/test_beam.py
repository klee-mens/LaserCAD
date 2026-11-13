# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.beam (Beam, SquareBeam, CircularRayBeam,
RainbowBeam, Ray_Distribution, Gaussian_Beam)

Ein Beam ist eine Gruppe von Strahlen. Der erste Strahl (_rays[0]) ist der
"innere" Strahl, bei Beam/CircularRayBeam/RainbowBeam liegt er auf der Achse.
Die anderen liegen im Abstand <radius> um die Achse. <angle> ist der Winkel
zur Achse: > 0 divergent, < 0 konvergent (Konvention der Matrizenoptik).
"""
import unittest

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import (Beam, SquareBeam, CircularRayBeam, RainbowBeam,
                      Gaussian_Beam, Ray_Distribution, Ray)
from LaserCAD.basic_optics.geom_object import rotation_matrix
from helpers import axis_crossing


def local_offsets(beam):
  """Strahlpositionen relativ zu beam.pos im Koordinatensystem des Beams."""
  return np.array([(r.pos - beam.pos) @ beam.get_axes() for r in beam._rays])


class TestBeamConstruction(unittest.TestCase):

  def test_defaults(self):
    b = Beam()
    self.assertEqual(len(b._rays), 2)
    assert_allclose(b._rays[0].pos, b.pos)                  # innerer Strahl
    assert_allclose(b._rays[1].pos, b.pos + (0, 0, 1))      # radius=1 nach +z
    for r in b._rays:
      assert_allclose(r.normal, (1, 0, 0), atol=1e-12)

  def test_ray_count_and_equal_spacing_of_outer_rays(self):
    # theta=0 liegt bei +z, wachsendes theta dreht nach -y
    for n in range(2, 9):
      with self.subTest(ray_count=n):
        b = Beam(radius=3, ray_count=n)
        self.assertEqual(len(b._rays), n)
        loc = local_offsets(b)
        assert_allclose(loc[0], (0, 0, 0), atol=1e-12)
        for k in range(n - 1):
          t = 2 * np.pi * k / (n - 1)
          assert_allclose(loc[k + 1], (0, -3 * np.sin(t), 3 * np.cos(t)),
                          atol=1e-12)

  def test_all_rays_get_the_wavelength_of_the_beam(self):
    b = Beam(wavelength=800e-6, ray_count=5)
    self.assertEqual({r.wavelength for r in b._rays}, {800e-6})

  def test_radius_and_angle_are_reproduced_by_radius_angle(self):
    for radius in (0.5, 1, 5):
      for angle in (-0.1, -0.01, 0, 0.02, 0.1):
        with self.subTest(radius=radius, angle=angle):
          r, a = Beam(radius=radius, angle=angle).radius_angle()
          self.assertAlmostEqual(r, radius, places=9)
          self.assertAlmostEqual(a, angle, places=9)

  def test_positive_angle_diverges_negative_angle_converges(self):
    div = Beam(radius=2, angle=0.1)._rays[1]    # Strahl bei +z
    con = Beam(radius=2, angle=-0.1)._rays[1]
    self.assertAlmostEqual(div.normal[2], np.sin(0.1))
    self.assertAlmostEqual(con.normal[2], -np.sin(0.1))

  def test_focal_length_is_where_the_outer_ray_crosses_the_axis(self):
    for radius, angle in ((5, -0.05), (2, -0.2), (5, 0.05), (1, 0.1)):
      with self.subTest(radius=radius, angle=angle):
        b = Beam(radius=radius, angle=angle)
        s, miss = axis_crossing(b._rays[1], b._rays[0].pos, b._rays[0].normal)
        self.assertAlmostEqual(miss, 0, places=9)
        self.assertAlmostEqual(b.focal_length(), s, places=6)
        self.assertAlmostEqual(b.focal_length(), -radius / np.tan(angle),
                               places=6)

  def test_diverging_beam_has_a_negative_focal_length(self):
    self.assertLess(Beam(radius=5, angle=0.05).focal_length(), 0)
    self.assertGreater(Beam(radius=5, angle=-0.05).focal_length(), 0)

  def test_collimated_beam_has_focal_length_zero_by_convention(self):
    # kollimiert = unendliche Brennweite, wird hier als 0 zurückgegeben
    self.assertEqual(Beam(radius=5, angle=0).focal_length(), 0)


class TestBeamAccessors(unittest.TestCase):

  def test_get_all_rays_returns_copies_by_default(self):
    b = Beam(ray_count=4)
    rays = b.get_all_rays()
    self.assertEqual(len(rays), 4)
    rays[0].pos = (999, 999, 999)
    assert_allclose(b._rays[0].pos, b.pos)

  def test_get_all_rays_by_reference_returns_the_beams_own_rays(self):
    b = Beam(ray_count=4)
    rays = b.get_all_rays(by_reference=True)
    for mine, theirs in zip(b._rays, rays):
      self.assertIs(mine, theirs)

  def test_inner_and_outer_rays_are_copies(self):
    b = Beam(ray_count=4)
    self.assertEqual(len(b.outer_rays()), 3)
    inner = b.inner_ray()
    inner.pos = (999, 999, 999)
    assert_allclose(b._rays[0].pos, b.pos)
    self.assertIsNot(b.inner_ray(), b._rays[0])

  def test_length_is_the_length_of_the_inner_ray(self):
    b = Beam()
    self.assertEqual(b.length(), Ray().length)

  def test_set_length_sets_all_rays(self):
    b = Beam(ray_count=5)
    b.set_length(123)
    self.assertEqual({r.length for r in b._rays}, {123})
    self.assertEqual(b.length(), 123)

  def test_wavelength_is_the_wavelength_of_the_inner_ray(self):
    self.assertEqual(Beam(wavelength=800e-6).wavelength(), 800e-6)

  def test_set_wavelength_sets_the_wavelength_of_all_rays(self):
    # Regression: set_wavelength hat früher ray.length statt ray.wavelength
    # gesetzt, die Wellenlänge blieb unverändert, dafür wurde die Länge
    # überschrieben.
    b = Beam(wavelength=1030e-6, ray_count=4)
    old_length = b.length()
    b.set_wavelength(500e-6)
    self.assertEqual({r.wavelength for r in b._rays}, {500e-6})
    self.assertEqual(b.wavelength(), 500e-6)
    self.assertEqual(b.length(), old_length)

  def test_set_wavelength_survives_recomputing_the_distribution(self):
    b = Beam(wavelength=1030e-6, ray_count=4)
    b.set_wavelength(500e-6)
    b.make_cone_distribution(4)
    self.assertEqual({r.wavelength for r in b._rays}, {500e-6})

  def test_set_ray_color(self):
    b = Beam(ray_count=3)
    b.set_ray_color((1, 0, 0))
    for r in b._rays:
      self.assertEqual(r.draw_dict["color"], (1, 0, 0))


class TestBeamMotion(unittest.TestCase):

  def test_moving_the_beam_moves_all_rays(self):
    b = Beam(radius=2, ray_count=5)
    before = np.array([r.pos for r in b._rays])
    b.pos = b.pos + (10, 20, 30)
    after = np.array([r.pos for r in b._rays])
    assert_allclose(after - before, np.tile((10, 20, 30), (5, 1)), atol=1e-12)

  def test_rotating_the_beam_rotates_all_rays_about_its_position(self):
    b = Beam(radius=2, ray_count=5)
    loc_before = local_offsets(b)
    b.rotate((0, 0, 1), np.pi / 2)
    assert_allclose(b._rays[0].normal, (0, 1, 0), atol=1e-12)
    for r in b._rays:
      assert_allclose(r.normal, (0, 1, 0), atol=1e-12)
    # im Koordinatensystem des Beams hat sich nichts geändert
    assert_allclose(local_offsets(b), loc_before, atol=1e-12)
    # der innere Strahl bleibt am Drehpunkt
    assert_allclose(b._rays[0].pos, b.pos, atol=1e-12)

  def test_setting_the_normal_turns_all_rays(self):
    b = Beam(ray_count=3)
    b.normal = (0, 1, 0)
    for r in b._rays:
      assert_allclose(r.normal, (0, 1, 0), atol=1e-12)

  def test_set_geom_moves_and_turns_the_rays(self):
    b = Beam(radius=2, ray_count=4)
    target = Ray()
    target.pos = (5, 6, 7)
    target.normal = (0, 0, 1)
    b.set_geom(target.get_geom())
    assert_allclose(b._rays[0].pos, (5, 6, 7), atol=1e-12)
    for r in b._rays:
      assert_allclose(r.normal, (0, 0, 1), atol=1e-12)
      self.assertLessEqual(np.linalg.norm(r.pos - (5, 6, 7)), 2 + 1e-9)


class TestOverrideRays(unittest.TestCase):

  def test_override_rays_takes_over_rays_and_geometry_of_the_first_ray(self):
    b = Beam(name="B")
    rays = [Ray(), Ray(), Ray()]
    rays[0].pos = (1, 2, 3)
    rays[0].normal = (0, 1, 0)
    b.override_rays(rays)
    self.assertEqual(b._ray_count, 3)
    self.assertEqual(len(b._rays), 3)
    assert_allclose(b.pos, (1, 2, 3))
    assert_allclose(b.normal, (0, 1, 0), atol=1e-12)

  def test_override_rays_renames_the_rays(self):
    b = Beam(name="B")
    b.override_rays([Ray(), Ray(), Ray()])
    self.assertEqual([r.name for r in b._rays],
                     ["B_middle_ray", "B_ray1", "B_ray2"])


class TestSquareBeam(unittest.TestCase):

  def test_rays_form_a_regular_grid(self):
    for n in range(2, 8):
      for radius in (0.3, 1, 2.5):
        with self.subTest(ray_in_line=n, radius=radius):
          sq = SquareBeam(radius=radius, ray_in_line=n)
          self.assertEqual(len(sq._rays), n * n)
          self.assertEqual(sq._ray_count, n * n)
          grid = np.linspace(-radius, radius, n)
          expected = sorted((y, z) for y in grid for z in grid)
          found = sorted((r.pos[1] - sq.pos[1], r.pos[2] - sq.pos[2])
                         for r in sq._rays)
          assert_allclose(found, expected, atol=1e-9)

  def test_all_rays_are_parallel_to_the_beam_axis(self):
    sq = SquareBeam(radius=2, ray_in_line=4)
    for r in sq._rays:
      assert_allclose(r.normal, (1, 0, 0), atol=1e-12)
      self.assertAlmostEqual(r.pos[0], sq.pos[0])

  def test_wavelength_is_passed_on_to_the_rays(self):
    # Regression: SquareBeam hat <wavelength> früher nicht an Beam
    # weitergereicht, alle Strahlen hatten die Default-Wellenlänge.
    sq = SquareBeam(wavelength=800e-6, ray_in_line=3)
    self.assertEqual({r.wavelength for r in sq._rays}, {800e-6})

  def test_default_wavelength(self):
    sq = SquareBeam(ray_in_line=3)
    self.assertEqual({r.wavelength for r in sq._rays}, {Beam().wavelength()})

  def test_ray_names(self):
    sq = SquareBeam(name="S", ray_in_line=3)
    self.assertEqual(sq._rays[0].name, "S_inner_Ray")
    self.assertEqual(sq._rays[5].name, "S_Ray5")


class TestCircularRayBeam(unittest.TestCase):

  def test_ray_count_and_rings(self):
    # ring_number n: 6*k Strahlen im Ring k (Radius k*radius/n), plus Mitte
    for n in range(1, 5):
      with self.subTest(ring_number=n):
        cb = CircularRayBeam(radius=3, ring_number=n)
        self.assertEqual(len(cb._rays), 3 * n * (n + 1) + 1)
        self.assertEqual(cb._ray_count, 3 * n * (n + 1) + 1)
        radii = np.round([np.linalg.norm((r.pos - cb.pos)[1:])
                          for r in cb._rays], 6)
        self.assertEqual(int(np.sum(radii == 0)), 1)
        for k in range(1, n + 1):
          self.assertEqual(int(np.sum(radii == round(3 * k / n, 6))), 6 * k)

  def test_rays_are_parallel_and_have_the_beam_wavelength(self):
    cb = CircularRayBeam(radius=3, ring_number=2, wavelength=800e-6)
    for r in cb._rays:
      assert_allclose(r.normal, (1, 0, 0), atol=1e-12)
      self.assertEqual(r.wavelength, 800e-6)

  def test_first_ray_is_the_central_ray(self):
    cb = CircularRayBeam(name="C", radius=3, ring_number=2)
    assert_allclose(cb._rays[0].pos, cb.pos)
    self.assertEqual(cb._rays[0].name, "C_inner_Ray")


class TestRainbowBeam(unittest.TestCase):

  CENTER = 1000e-6
  BANDWIDTH = 100e-6

  def _wavelengths(self, n):
    rb = RainbowBeam(wavelength=self.CENTER, bandwidth=self.BANDWIDTH,
                     ray_count=n)
    return rb, np.array([r.wavelength for r in rb._rays])

  def test_ray_count(self):
    for n in (3, 4, 5, 6, 11, 20):
      with self.subTest(ray_count=n):
        rb, w = self._wavelengths(n)
        self.assertEqual(len(rb._rays), n)

  def test_inner_ray_has_the_central_wavelength(self):
    for n in (3, 4, 11):
      with self.subTest(ray_count=n):
        _, w = self._wavelengths(n)
        self.assertEqual(w[0], self.CENTER)

  def test_wavelengths_span_exactly_the_bandwidth(self):
    for n in (3, 4, 5, 6, 11, 20):
      with self.subTest(ray_count=n):
        _, w = self._wavelengths(n)
        self.assertAlmostEqual(w.min(), self.CENTER - self.BANDWIDTH / 2,
                               places=12)
        self.assertAlmostEqual(w.max(), self.CENTER + self.BANDWIDTH / 2,
                               places=12)

  def test_wavelengths_are_evenly_spaced_and_symmetric_for_odd_ray_count(self):
    for n in (3, 5, 11):
      with self.subTest(ray_count=n):
        _, w = self._wavelengths(n)
        w = np.sort(w)
        assert_allclose(w, np.linspace(self.CENTER - self.BANDWIDTH / 2,
                                       self.CENTER + self.BANDWIDTH / 2, n),
                        atol=1e-12)

  def test_all_wavelengths_are_different(self):
    for n in (4, 6, 20):
      with self.subTest(ray_count=n):
        _, w = self._wavelengths(n)
        self.assertEqual(len(set(np.round(w, 15))), n)

  def test_all_rays_share_position_and_direction(self):
    rb, _ = self._wavelengths(7)
    for r in rb._rays:
      assert_allclose(r.pos, rb.pos)
      assert_allclose(r.normal, (1, 0, 0), atol=1e-12)

  def test_default_bandwidth_is_10_nm(self):
    rb = RainbowBeam(wavelength=1000e-6, ray_count=11)
    w = [r.wavelength for r in rb._rays]
    self.assertAlmostEqual(max(w) - min(w), 10e-6, places=12)

  def test_ray_thickness_is_passed_to_the_rays(self):
    rb = RainbowBeam(ray_count=5, thickness=4)
    self.assertEqual({r.draw_dict["thickness"] for r in rb._rays}, {4})
    rb = RainbowBeam(ray_count=5)
    self.assertEqual({r.draw_dict["thickness"] for r in rb._rays}, {2})


class TestRayDistribution(unittest.TestCase):

  def test_ray_count(self):
    # steps^2 Richtungen mit je einem SquareBeam aus steps^2 Strahlen, plus
    # ein zusätzlicher Strahl: steps^4 + 1 (die Docstring der Klasse nennt
    # fälschlich steps^3 + 1)
    for steps in (2, 3):
      with self.subTest(steps=steps):
        rd = Ray_Distribution(radius=3, steps=steps)
        self.assertEqual(len(rd._rays), steps**4 + 1)

  def test_ray_directions_stay_within_the_opening_angle(self):
    angle = 0.05
    rd = Ray_Distribution(radius=3, steps=3, angle=angle)
    for r in rd._rays:
      tilt = np.arccos(np.clip(r.normal[0], -1, 1))
      self.assertLessEqual(tilt, np.sqrt(2) * angle + 1e-9)


class TestGaussianBeam(unittest.TestCase):

  def test_waist_follows_the_divergence_angle(self):
    for angle in (0.02, 0.005, -0.01):
      with self.subTest(angle=angle):
        g = Gaussian_Beam(radius=10, angle=angle, wavelength=1030e-6)
        w0 = 1030e-6 / (np.pi * np.tan(abs(angle)))
        self.assertAlmostEqual(g.waist() / w0, 1, places=9)

  def test_beam_radius_follows_from_the_q_parameter(self):
    for radius in (3, 10, 25):
      with self.subTest(radius=radius):
        g = Gaussian_Beam(radius=radius, angle=0.02, wavelength=1030e-6)
        q = g.q_para
        w = np.sqrt(g.wavelength / np.pi * abs(q)**2 / q.imag)
        self.assertAlmostEqual(w / radius, 1, places=9)

  def test_sign_of_the_angle_gives_the_sign_of_the_distance_to_the_waist(self):
    self.assertGreater(Gaussian_Beam(radius=10, angle=0.02).q_para.real, 0)
    self.assertLess(Gaussian_Beam(radius=10, angle=-0.02).q_para.real, 0)

  def test_set_length(self):
    g = Gaussian_Beam()
    g.set_length(42)
    self.assertEqual(g.length, 42)


if __name__ == "__main__":
  unittest.main()
