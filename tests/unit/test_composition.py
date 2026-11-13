# -*- coding: utf-8 -*-
"""
Tests für LaserCAD.basic_optics.composition (Composition)

Eine Composition verwaltet optische Elemente entlang der optischen Achse
(_optical_axis, eine Liste von Strahlen) sowie eine Lichtquelle (_lightsource).
propagate() verlängert die Achse, add_on_axis() setzt ein Element an das
Achsenende und lenkt die Achse am Element weiter.
"""
import unittest

import numpy as np
from numpy.testing import assert_allclose

from LaserCAD import (Beam, Composition, Curved_Mirror, Geom_Object, Lens,
                      Mirror, Ray)
from helpers import axis_crossing


class TestCompositionBasics(unittest.TestCase):

  def test_new_composition_is_empty(self):
    c = Composition(name="C")
    self.assertEqual(c._elements, [])
    self.assertEqual(c.get_sequence(), [])
    self.assertEqual(len(c._optical_axis), 1)
    assert_allclose(c._optical_axis[0].pos, c.pos)
    assert_allclose(c._optical_axis[0].normal, c.normal)
    self.assertEqual(c._optical_axis[0].length, 0)

  def test_default_lightsource_is_a_beam_named_after_the_composition(self):
    c = Composition(name="C")
    self.assertIsInstance(c._lightsource, Beam)
    self.assertEqual(c._beams, [c._lightsource])

  def test_propagate_extends_the_optical_axis(self):
    c = Composition()
    c.propagate(100)
    self.assertEqual(c._optical_axis[-1].length, 100)
    assert_allclose(c.last_geom()[0], (100, 0, 80))

  def test_propagate_accumulates(self):
    c = Composition()
    c.propagate(100)
    c.propagate(50)
    self.assertEqual(c._optical_axis[-1].length, 150)
    assert_allclose(c.last_geom()[0], (150, 0, 80))

  def test_last_geom_returns_endpoint_and_axes_of_the_axis(self):
    c = Composition()
    c.propagate(70)
    pos, axes = c.last_geom()
    assert_allclose(pos, (70, 0, 80))
    assert_allclose(axes, np.eye(3))


class TestAddOnAxis(unittest.TestCase):

  def test_element_is_placed_at_the_end_of_the_axis(self):
    c = Composition(name="C")
    c.propagate(100)
    lens = Lens(f=100)
    c.add_on_axis(lens)
    assert_allclose(lens.pos, (100, 0, 80))
    assert_allclose(lens.normal, (1, 0, 0), atol=1e-12)

  def test_element_is_registered_and_renamed(self):
    c = Composition(name="C")
    c.add_on_axis(Lens(f=100, name="L"))
    self.assertEqual(len(c._elements), 1)
    self.assertEqual(c._elements[0].name, "C_L")
    self.assertEqual(c.get_sequence(), [0])

  def test_axis_gets_a_new_segment_per_element(self):
    c = Composition()
    c.propagate(100)
    c.add_on_axis(Lens(f=100))
    self.assertEqual(len(c._optical_axis), 2)
    # die Länge des vorherigen Segments reicht bis zum Element
    self.assertAlmostEqual(c._optical_axis[0].length, 100)
    self.assertEqual(c._optical_axis[1].length, 0)

  def test_mirror_turns_the_optical_axis(self):
    c = Composition()
    c.propagate(100)
    c.add_on_axis(Mirror(phi=90))
    c.propagate(50)
    assert_allclose(c._optical_axis[0].normal, (1, 0, 0), atol=1e-12)
    assert_allclose(c._optical_axis[1].normal, (0, 1, 0), atol=1e-12)
    assert_allclose(c.last_geom()[0], (100, 50, 80), atol=1e-9)

  def test_two_mirrors_make_a_u_turn(self):
    c = Composition()
    c.propagate(100)
    c.add_on_axis(Mirror(phi=90))
    c.propagate(100)
    c.add_on_axis(Mirror(phi=90))
    c.propagate(100)
    assert_allclose(c._optical_axis[-1].normal, (-1, 0, 0), atol=1e-12)
    assert_allclose(c.last_geom()[0], (0, 100, 80), atol=1e-9)

  def test_optical_path_length_is_the_sum_of_all_segments(self):
    c = Composition()
    c.propagate(100)
    c.add_on_axis(Mirror(phi=90))
    c.propagate(50)
    self.assertAlmostEqual(c.optical_path_length(), 150)

  def test_object_without_next_ray_is_not_an_optical_element(self):
    c = Composition()
    c.propagate(100)
    thing = Geom_Object(name="cosmetics")
    c.add_on_axis(thing)
    self.assertEqual(c._elements, [])
    self.assertEqual(c.non_opticals, [thing])
    assert_allclose(thing.pos, (100, 0, 80))       # wird trotzdem platziert
    self.assertEqual(len(c._optical_axis), 1)      # lenkt die Achse nicht ab


class TestAddFixedElement(unittest.TestCase):

  def test_fixed_element_keeps_its_own_position(self):
    c = Composition()
    lens = Lens(f=50, name="F")
    lens.pos = (30, 0, 80)
    c.add_fixed_elm(lens)
    assert_allclose(lens.pos, (30, 0, 80))
    self.assertEqual(c.get_sequence(), [0])

  def test_fixed_element_is_only_part_of_the_axis_after_recomputing(self):
    c = Composition()
    lens = Lens(f=50)
    lens.pos = (30, 0, 80)
    c.add_fixed_elm(lens)
    self.assertEqual(len(c._optical_axis), 1)
    c.recompute_optical_axis()
    self.assertEqual(len(c._optical_axis), 2)


class TestSequence(unittest.TestCase):

  def test_sequence_follows_the_order_of_insertion(self):
    c = Composition()
    for _ in range(3):
      c.propagate(10)
      c.add_on_axis(Lens(f=100))
    self.assertEqual(c.get_sequence(), [0, 1, 2])

  def test_get_sequence_returns_a_copy(self):
    c = Composition()
    c.add_on_axis(Lens(f=100))
    seq = c.get_sequence()
    seq.append(99)
    self.assertEqual(c.get_sequence(), [0])

  def test_set_sequence_changes_the_order_used_for_the_axis(self):
    c = Composition()
    c.propagate(100)
    c.add_on_axis(Mirror(phi=90))
    c.propagate(100)
    c.add_on_axis(Mirror(phi=-90))
    c.set_sequence([0])        # nur der erste Spiegel
    c.recompute_optical_axis()
    self.assertEqual(len(c._optical_axis), 2)


class TestMatrix(unittest.TestCase):
  """ABCD-Matrix des Systems; Vergleichswerte aus der Matrizenoptik."""

  def test_free_propagation(self):
    c = Composition()
    c.propagate(100)
    assert_allclose(c.matrix(), [[1, 100], [0, 1]], atol=1e-12)

  def test_lens_with_equal_distances_is_a_fourier_system(self):
    # d - Linse(f) - d mit d = f:  [[0, f], [-1/f, 0]]
    c = Composition()
    c.propagate(100)
    c.add_on_axis(Lens(f=100))
    c.propagate(100)
    assert_allclose(c.matrix(), [[0, 100], [-1 / 100, 0]], atol=1e-12)

  def test_imaging_condition_gives_B_equal_zero(self):
    # 1/s + 1/s' = 1/f mit s = 300, f = 100  ->  s' = 150
    c = Composition()
    c.propagate(300)
    c.add_on_axis(Lens(f=100))
    c.propagate(150)
    M = c.matrix()
    self.assertAlmostEqual(M[0, 1], 0, places=9)           # B = 0: Abbildung
    self.assertAlmostEqual(M[0, 0], -150 / 300)            # Vergrößerung -s'/s
    self.assertAlmostEqual(np.linalg.det(M), 1)

  def test_telescope(self):
    # Kepler-Teleskop f1=100, f2=200, Abstand f1+f2: [[-f2/f1, 0], [0, -f1/f2]]
    c = Composition()
    c.propagate(100)
    c.add_on_axis(Lens(f=100))
    c.propagate(300)
    c.add_on_axis(Lens(f=200))
    c.propagate(200)
    assert_allclose(c.matrix(), [[-2, 0], [0, -0.5]], atol=1e-12)

  def test_concave_mirror_at_normal_incidence_acts_like_a_lens_with_f_half_R(self):
    c = Composition()
    c.propagate(100)
    c.add_on_axis(Curved_Mirror(radius=200, phi=180))
    c.propagate(100)
    assert_allclose(c.matrix(), [[0, 100], [-1 / 100, 0]], atol=1e-12)

  def test_determinant_is_one_for_any_lossless_system(self):
    c = Composition()
    c.propagate(80)
    c.add_on_axis(Lens(f=150))
    c.propagate(40)
    c.add_on_axis(Lens(f=-60))
    c.propagate(120)
    self.assertAlmostEqual(np.linalg.det(c.matrix()), 1)

  def test_matrix_does_not_depend_on_the_absolute_position(self):
    c = Composition()
    c.propagate(100)
    c.add_on_axis(Lens(f=100))
    c.propagate(100)
    M0 = c.matrix()
    c.pos = c.pos + (10, 20, 5)
    assert_allclose(c.matrix(), M0, atol=1e-12)


class TestLightsourceAndBeams(unittest.TestCase):

  def _focusing_setup(self):
    c = Composition(name="C")
    c.set_light_source(Beam(radius=0.1, angle=0))
    c.propagate(100)
    c.add_on_axis(Lens(f=100))
    c.propagate(100)
    return c

  def test_set_light_source_adopts_geometry_and_name(self):
    c = Composition(name="C")
    c.pos = (5, 6, 7)
    ls = Beam(name="source")
    c.set_light_source(ls)
    self.assertIs(c._lightsource, ls)
    self.assertEqual(ls.name, "C_Lightsource")
    assert_allclose(ls.pos, (5, 6, 7))
    self.assertEqual(c._beams, [ls])

  def test_compute_beams_returns_one_beam_per_element_plus_the_source(self):
    c = self._focusing_setup()
    beams = c.compute_beams()
    self.assertEqual(len(beams), 2)
    self.assertEqual([b.name for b in beams], ["C_Lightsource", "C_beam_1"])

  def test_last_beam_has_the_length_of_the_last_propagation(self):
    c = self._focusing_setup()
    self.assertEqual(c.compute_beams()[-1].length(), 100)

  def test_beam_after_a_lens_is_focused_at_the_focal_length(self):
    c = self._focusing_setup()
    after = c.compute_beams()[-1]
    inner, outer = after._rays[0], after._rays[1]
    s, miss = axis_crossing(outer, inner.pos, inner.normal)
    self.assertAlmostEqual(miss, 0, places=6)
    self.assertAlmostEqual(s / 100, 1, places=5)
    assert_allclose(inner.pos, (100, 0, 80), atol=1e-9)      # an der Linse

  def test_compute_beams_stores_the_beams(self):
    c = self._focusing_setup()
    beams = c.compute_beams()
    self.assertEqual(c._beams, beams)

  def test_compute_beams_with_external_source_leaves_the_composition_alone(self):
    c = self._focusing_setup()
    c.compute_beams()
    stored = list(c._beams)
    beams = c.compute_beams(external_source=Beam(radius=2))
    self.assertEqual(len(beams), 2)
    self.assertEqual(c._beams, stored)

  def test_beam_through_a_mirror_changes_direction(self):
    c = Composition()
    c.propagate(100)
    c.add_on_axis(Mirror(phi=90))
    c.propagate(50)
    after = c.compute_beams()[-1]
    assert_allclose(after._rays[0].normal, (0, 1, 0), atol=1e-12)


class TestMovingAComposition(unittest.TestCase):

  def _setup(self):
    c = Composition(name="C")
    c.propagate(100)
    lens = Lens(f=100)
    c.add_on_axis(lens)
    c.propagate(50)
    return c, lens

  def test_moving_moves_elements_axis_and_lightsource(self):
    c, lens = self._setup()
    c.pos = c.pos + (10, 20, 0)
    assert_allclose(lens.pos, (110, 20, 80))
    assert_allclose(c._optical_axis[-1].endpoint(), (160, 20, 80))
    assert_allclose(c._lightsource.pos, (10, 20, 80))

  def test_rotating_turns_everything_about_the_composition_position(self):
    c, lens = self._setup()
    c.pos = c.pos + (10, 20, 0)
    c.rotate((0, 0, 1), np.pi / 2)
    assert_allclose(c.pos, (10, 20, 80))
    assert_allclose(lens.pos, (10, 120, 80), atol=1e-9)
    assert_allclose(lens.normal, (0, 1, 0), atol=1e-12)
    assert_allclose(c._optical_axis[-1].normal, (0, 1, 0), atol=1e-12)

  def test_optical_path_length_does_not_change_by_moving_or_rotating(self):
    c, _ = self._setup()
    opl = c.optical_path_length()
    c.pos = c.pos + (10, 20, 0)
    c.rotate((0, 0, 1), 0.7)
    self.assertAlmostEqual(c.optical_path_length(), opl)


class TestSubcompositions(unittest.TestCase):

  def test_subcomposition_is_placed_at_the_end_of_the_axis(self):
    sub = Composition(name="Sub")
    sub.propagate(50)
    sub_lens = Lens(f=100, name="SL")
    sub.add_on_axis(sub_lens)

    par = Composition(name="Par")
    par.propagate(100)
    par.add_supcomposition_on_axis(sub)
    assert_allclose(sub_lens.pos, (150, 0, 80))
    self.assertEqual([e.name for e in par._elements], ["Par_Sub_SL"])

  def test_subcomposition_follows_a_turned_axis(self):
    sub = Composition(name="Sub")
    sub.propagate(50)
    sub_lens = Lens(f=100, name="SL")
    sub.add_on_axis(sub_lens)

    par = Composition(name="Par")
    par.propagate(100)
    par.add_on_axis(Mirror(phi=90))
    par.add_supcomposition_on_axis(sub)
    assert_allclose(sub_lens.pos, (100, 50, 80), atol=1e-9)
    assert_allclose(sub_lens.normal, (0, 1, 0), atol=1e-12)


class TestRedefineOpticalAxis(unittest.TestCase):

  def test_composition_takes_over_the_geometry_of_the_ray(self):
    c = Composition()
    r = Ray()
    r.pos = (5, 6, 80)
    r.normal = (0, 1, 0)
    c.redefine_optical_axis(r)
    assert_allclose(c.pos, (5, 6, 80))
    assert_allclose(c.normal, (0, 1, 0), atol=1e-12)
    assert_allclose(c._optical_axis[0].pos, (5, 6, 80))
    assert_allclose(c._optical_axis[0].normal, (0, 1, 0), atol=1e-12)

  def test_redefining_does_not_change_the_given_ray(self):
    c = Composition()
    r = Ray()
    r.pos = (5, 6, 80)
    c.redefine_optical_axis(r)
    r.pos = (0, 0, 0)
    assert_allclose(c._optical_axis[0].pos, (5, 6, 80))


if __name__ == "__main__":
  unittest.main()
