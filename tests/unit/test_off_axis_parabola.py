# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.off_axis_parabola (Off_Axis_Parabola)

Ein außeraxialer Parabolspiegel fokussiert einen achsparallelen Strahl exakt
(ohne sphärische Aberration) in einen Punkt im Abstand <reflected_focal_length>
vom Auftreffpunkt der Mittelachse. <angle> ist der Winkel zwischen dem
(umgedrehten) einfallenden und dem reflektierten Strahl. Mit colim=True läuft
der Strahlengang rückwärts (Punktquelle -> kollimierter Strahl).
"""
import unittest

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import Ray, inch
from LaserCAD.basic_optics import Off_Axis_Parabola

POS = np.array((100.0, 0.0, 80.0))
RFL = 2 * inch


def make_oap(angle=90, colim=False, **kwargs):
  oap = Off_Axis_Parabola(reflected_focal_length=RFL, angle=angle,
                          colim=colim, **kwargs)
  if colim:
    oap.set_geom((POS, np.eye(3)))     # colim dreht den Spiegel erst in set_geom
  else:
    oap.pos = POS
  return oap


def parallel_ray(offset=(0, 0, 0)):
  r = Ray()
  r.pos = POS - (100, 0, 0) + offset
  return r


def miss_distance(ray_out, point):
  s = np.dot(point - ray_out.pos, ray_out.normal)
  return np.linalg.norm(ray_out.pos + s * ray_out.normal - point)


class TestParentParabola(unittest.TestCase):

  def test_90_degree_parent_focal_length_is_half_the_reflected(self):
    oap = make_oap(angle=90)
    self.assertAlmostEqual(oap.parent_focal_length(), RFL / 2)

  def test_curvature_and_focal_length_are_consistent(self):
    for angle in (30, 60, 90, 120):
      oap = make_oap(angle=angle)
      self.assertAlmostEqual(oap.parent_focal_length() * 4
                             * oap.parent_parabola_curvature(), 1.0)

  def test_reflected_focal_length_equals_distance_from_parent_focus(self):
    # Brennpunkt der Elternparabel: Scheitel + 1/(4c) entlang der Achse
    for angle in (60, 90, 120):
      oap = make_oap(angle=angle)
      center = oap.next_ray(parallel_ray())
      focus = center.pos + RFL * center.normal
      apex = oap.parent_parabola_apex()
      x, y, z = oap.get_coordinate_system()
      parent_focus = apex - x * oap.parent_focal_length()
      # der reflektierte Fokus ist der Brennpunkt der Elternparabel
      assert_allclose(focus, parent_focus, atol=1e-9)


class TestFocusing(unittest.TestCase):

  def test_center_ray_is_deflected_by_the_angle(self):
    for angle in (45, 60, 90, 120):
      out = make_oap(angle=angle).next_ray(parallel_ray())
      # Winkel zwischen umgedrehtem Einfall (-x) und Ausfall = angle
      cos = np.dot((-1, 0, 0), out.normal)
      self.assertAlmostEqual(np.degrees(np.arccos(cos)), angle, places=6)

  def test_center_ray_hits_the_mirror_position(self):
    out = make_oap().next_ray(parallel_ray())
    assert_allclose(out.pos, POS, atol=1e-9)

  def test_90_degree_center_ray_goes_to_plus_y(self):
    out = make_oap(angle=90).next_ray(parallel_ray())
    assert_allclose(out.normal, (0, 1, 0), atol=1e-12)

  def test_parallel_rays_meet_in_one_focus_point(self):
    for angle in (60, 90, 120):
      oap = make_oap(angle=angle)
      center = oap.next_ray(parallel_ray())
      focus = center.pos + RFL * center.normal
      for off in ((0, 3, 0), (0, -3, 0), (0, 0, 3), (0, 0, -3), (0, 2, 2),
                  (0, -4, 1)):
        out = oap.next_ray(parallel_ray(off))
        self.assertLess(miss_distance(out, focus), 1e-9,
                        msg=f"angle={angle}, offset={off}")

  def test_outgoing_rays_are_normalized(self):
    out = make_oap().next_ray(parallel_ray((0, 3, 2)))
    self.assertAlmostEqual(np.linalg.norm(out.normal), 1.0, places=12)

  def test_input_ray_direction_is_unchanged(self):
    r = parallel_ray((0, 3, 0))
    make_oap().next_ray(r)
    assert_allclose(r.normal, (1, 0, 0))

  def test_displaced_mirror_moves_the_focus_with_it(self):
    oap = make_oap()
    c1 = oap.next_ray(parallel_ray())
    oap.pos = POS + (0, 0, 10)
    r = parallel_ray((0, 0, 10))
    c2 = oap.next_ray(r)
    assert_allclose(c2.pos - c1.pos, (0, 0, 10), atol=1e-9)
    assert_allclose(c2.normal, c1.normal, atol=1e-12)


class TestCollimation(unittest.TestCase):

  def test_point_source_in_focus_gives_a_parallel_beam(self):
    for angle, direction in ((90, (-1, 0, 0)), (60, (-np.sqrt(3) / 2, 0.5, 0))):
      oap = make_oap(angle=angle, colim=True)
      focus = POS + RFL * np.array(direction)
      outs = []
      for tilt in ((0, 0), (0.02, 0), (-0.02, 0), (0, 0.02), (0, -0.02)):
        d = POS - focus
        d = d / np.linalg.norm(d)
        side = np.array((-d[1], d[0], 0))
        r = Ray()
        r.pos = focus
        dd = d + tilt[0] * side + tilt[1] * np.array((0, 0, 1))
        r.normal = dd / np.linalg.norm(dd)
        outs.append(oap.next_ray(r).normal)
      for o in outs[1:]:
        assert_allclose(o, outs[0], atol=1e-9, err_msg=f"angle={angle}")


class TestAperture(unittest.TestCase):

  def test_default_aperture_is_one_inch(self):
    self.assertEqual(make_oap().aperture, inch)

  def test_thickness_follows_aperture_class(self):
    oap = make_oap()
    expected = {0.4 * inch: 20, 1 * inch: 1.25 * inch,
                2 * inch: 2.47 * inch, 3 * inch: 3.47 * inch}
    for ap, th in expected.items():
      oap.aperture = ap
      self.assertAlmostEqual(oap.thickness, th)


if __name__ == "__main__":
  unittest.main()
