# -*- coding: utf-8 -*-
"""
Invarianten der Multipass-Module (White Cell, Verstärker Typ I/II).

Per Strahlverfolgung (Beam.compute / Composition.propagate nicht nötig):
Wir prüfen die Elementanzahl pro Umlauf und dass die Determinante der
Gesamtmatrix 1 ist.
"""
import contextlib
import io
import unittest
import warnings

import numpy as np

import itertools

from LaserCAD.moduls import (Make_White_Cell, Make_Amplifier_Typ_I_simple,
                             Make_Amplifier_Typ_I_Mirror,
                             Make_Amplifier_Typ_II_simple,
                             Make_Amplifier_Typ_II_Mirror,
                             Make_Amplifier_Typ_II_UpDown)
from LaserCAD.moduls.type_II_Amplifier import Make_Amplifier_Typ_II_plane


def make(func, *a, **kw):
  with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
    warnings.simplefilter("ignore")
    return func(*a, **kw)


class TestWhiteCell(unittest.TestCase):
  def test_sequence_length_grows_with_roundtrips(self):
    for rt in (1, 2, 3, 4):
      with self.subTest(rt=rt):
        wc = make(Make_White_Cell, roundtrips4=rt)
        self.assertEqual(len(wc.get_sequence()), 3 + 4 * (rt - 1))

  def test_matrix_determinant_is_one(self):
    for rt in (1, 2, 3):
      with self.subTest(rt=rt):
        wc = make(Make_White_Cell, roundtrips4=rt)
        self.assertAlmostEqual(np.linalg.det(wc.matrix()), 1, places=9)


class TestAmplifierTyp1(unittest.TestCase):
  def test_sequence_length(self):
    for rt, n in [(1, 7), (2, 13), (3, 19), (4, 25)]:
      with self.subTest(rt=rt):
        amp = make(Make_Amplifier_Typ_I_simple, roundtrips2=rt)
        self.assertEqual(len(amp.get_sequence()), n)

  def test_matrix_determinant_is_one(self):
    amp = make(Make_Amplifier_Typ_I_simple, roundtrips2=2)
    self.assertAlmostEqual(np.linalg.det(amp.matrix()), 1, places=9)


def hits(comp):
  """Treffpunkte der optischen Achse, gruppiert nach Element-Index."""
  comp.recompute_optical_axis()
  seq, ax = comp.get_sequence(), comp._optical_axis
  per = {}
  for k, i in enumerate(seq):
    per.setdefault(i, []).append(np.array(ax[k + 1].pos, float))
  return per


def unique_points(pts, tol=1.0):
  u = []
  for p in pts:
    if not any(np.linalg.norm(p - q) < tol for q in u):
      u.append(p)
  return u


class TestMultipassInvariants(unittest.TestCase):
  """
  Konstruktionsprinzip: Jede Optik wird innerhalb ihrer Apertur getroffen,
  kleine Spiegel im Zentrum, und verschiedene Durchgänge auf großen Optiken
  haben einen Abstand von etwa <beam_sep>.
  """
  CASES = [
    ("white", Make_White_Cell, "roundtrips4", (1, 2, 3, 4)),
    ("t1s", Make_Amplifier_Typ_I_simple, "roundtrips2", (1, 2, 3, 4)),
    ("t1m", Make_Amplifier_Typ_I_Mirror, "roundtrips2", (1, 2, 3, 4)),
    ("t2s", Make_Amplifier_Typ_II_simple, "roundtrips2", (1, 2, 3, 4)),
    ("t2m", Make_Amplifier_Typ_II_Mirror, "roundtrips2", (1, 2, 3, 4)),
    ("t2plane", Make_Amplifier_Typ_II_plane, "roundtrips2", (1, 2, 3, 4)),
  ]

  def test_hits_inside_aperture(self):
    # Auffälligkeit: Die Verstärker Typ I/II legen die Spots im Abstand
    # <beam_sep> auf einer Linie um die Linsenmitte. Ab 3 Roundtrips liegen
    # sie bei +-30 bzw. +-45 mm, also AUSSERHALB der Apertur (50.8 mm) der
    # Linse. Deshalb wird dieser Test für die Verstärker nur bis 2 Roundtrips
    # geprüft; die White Cell und die plane-Variante bis 4.
    for nm, f, kw, rts in self.CASES:
      if nm not in ("white", "t2plane"):
        rts = [r for r in rts if r <= 2]
      for rt in rts:
        with self.subTest(nm=nm, rt=rt):
          c = make(f, **{kw: rt})
          for i, pts in hits(c).items():
            el = c._elements[i]
            ap = getattr(el, "aperture", None)
            if not ap:
              continue
            d = max(np.linalg.norm(p - el.pos) for p in pts)
            self.assertLessEqual(d, ap / 2 + 0.5)

  @unittest.expectedFailure
  def test_amplifier_spots_inside_aperture_for_4_roundtrips(self):
    # dokumentiert die oben beschriebene Auffälligkeit
    for f in (Make_Amplifier_Typ_I_simple, Make_Amplifier_Typ_II_simple):
      c = make(f, roundtrips2=4)
      for i, pts in hits(c).items():
        el = c._elements[i]
        ap = getattr(el, "aperture", None)
        if ap:
          d = max(np.linalg.norm(p - el.pos) for p in pts)
          self.assertLessEqual(d, ap / 2 + 0.5)

  def test_small_mirrors_hit_at_centre(self):
    for nm, f, kw, rts in self.CASES:
      for rt in rts:
        with self.subTest(nm=nm, rt=rt):
          c = make(f, **{kw: rt})
          for i, pts in hits(c).items():
            el = c._elements[i]
            ap = getattr(el, "aperture", None)
            if ap and ap <= 25.4 and len(unique_points(pts)) == 1:
              d = max(np.linalg.norm(p - el.pos) for p in pts)
              self.assertLess(d, 1.0)

  def test_spots_on_big_optics_are_separated(self):
    for nm, f, kw, rts in self.CASES:
      for rt in rts:
        with self.subTest(nm=nm, rt=rt):
          c = make(f, **{kw: rt})
          for i, pts in hits(c).items():
            u = unique_points(pts)
            if len(u) < 2:
              continue
            dmin = min(np.linalg.norm(a - b)
                       for a, b in itertools.combinations(u, 2))
            self.assertGreater(dmin, 7.0)   # beam_sep=15, plane: ~9

  def test_updown_variant_builds_and_has_unit_determinant(self):
    for rt in (1, 2, 3):
      with self.subTest(rt=rt):
        c = make(Make_Amplifier_Typ_II_UpDown, roundtrips2=rt)
        self.assertAlmostEqual(np.linalg.det(c.matrix()), 1, places=9)

  def test_sequence_lengths_type2(self):
    for f, ns in [(Make_Amplifier_Typ_II_simple, (5, 9, 13, 17)),
                  (Make_Amplifier_Typ_II_Mirror, (5, 9, 13, 17)),
                  (Make_Amplifier_Typ_II_plane, (5, 13, 21, 29)),
                  (Make_Amplifier_Typ_I_Mirror, (7, 13, 19, 25))]:
      for rt, n in zip((1, 2, 3, 4), ns):
        with self.subTest(f=f.__name__, rt=rt):
          self.assertEqual(len(make(f, roundtrips2=rt).get_sequence()), n)


if __name__ == "__main__":
  unittest.main()
