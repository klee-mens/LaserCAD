# -*- coding: utf-8 -*-
"""
Gemeinsame Hilfsfunktionen für die Unit-Tests.
"""
import numpy as np


def axis_crossing(ray, axis_point, axis_dir):
  """
  Berechnet, wo ein Strahl die optische Achse (Gerade durch <axis_point> in
  Richtung <axis_dir>) kreuzt bzw. ihr am nächsten kommt.

  Returns
  -------
  s : float
    Position auf der Achse, gemessen von <axis_point> in Richtung <axis_dir>
  miss : float
    Abstand der beiden Geraden an dieser Stelle (0 = sie schneiden sich echt)
  """
  p = np.array(ray.pos, dtype=float)
  d = np.array(ray.normal, dtype=float)
  a = np.array(axis_point, dtype=float)
  e = np.array(axis_dir, dtype=float)
  e = e / np.linalg.norm(e)
  A = np.column_stack((e, -d))
  sol = np.linalg.lstsq(A, p - a, rcond=None)[0]
  s, t = sol
  miss = np.linalg.norm((a + s * e) - (p + t * d))
  return s, miss


def is_orthonormal_right_handed(axes, atol=1e-12):
  """True, wenn <axes> eine Drehmatrix ist (orthonormal, Determinante +1)."""
  axes = np.asarray(axes, dtype=float)
  ortho = np.allclose(axes.T @ axes, np.eye(3), atol=atol)
  det_ok = abs(np.linalg.det(axes) - 1) < atol
  return bool(ortho and det_ok)
