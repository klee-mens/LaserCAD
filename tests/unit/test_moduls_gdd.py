# -*- coding: utf-8 -*-
"""
Regressionstests für die Module Compressor und Stretcher.

1. GDD und TOD: Beide Module berechnen aus dem Beugungswinkel
   (Geom_Object.angle_to ohne <axis>) die Dispersion. Die Referenzwerte hier
   wurden mit dem Code-Stand VOR der Änderung an angle_to gemessen. Der Test
   sichert damit nur, dass sich die Ergebnisse nicht unbemerkt ändern. Er ist
   KEINE unabhängige physikalische Validierung der Formeln.

2. Bandbreite: Die Lichtquelle beider Module ist ein RainbowBeam, dessen
   Bandbreite aus dem Parameter des Moduls stammen muss. Hintergrund: Die
   Klassen nehmen beliebige Keyword-Argumente an und verwerfen unbekannte
   still (Geom_Object.__init__(**kwargs)). Nach der Umbenennung von
   "bandwith" in "bandwidth" hat der Compressor deshalb unbemerkt mit der
   Default-Bandbreite von 10 nm statt der eingestellten gerechnet.
"""
import contextlib
import io
import unittest

from LaserCAD import RainbowBeam
from LaserCAD.moduls.compressor import Make_Compressor
from LaserCAD.moduls.stretcher import Make_Stretcher

# gemessen mit den Default-Parametern der Make_*-Funktionen
COMPRESSOR_GDD = -5.272268994413651e-25   # s^2
COMPRESSOR_TOD = -1.1082160594660152e-39  # s^3
STRETCHER_GDD = 2.355682993441341e-25     # s^2
STRETCHER_TOD = 4.498126657733657e-40     # s^3


def quiet(func, *args, **kwargs):
  with contextlib.redirect_stdout(io.StringIO()):
    return func(*args, **kwargs)


class TestDispersionOfModules(unittest.TestCase):

  def test_compressor_default_gdd_and_tod(self):
    c = quiet(Make_Compressor)
    self.assertAlmostEqual(c.GDD / COMPRESSOR_GDD, 1, places=9)
    self.assertAlmostEqual(c.TOD / COMPRESSOR_TOD, 1, places=9)

  def test_stretcher_default_gdd_and_tod(self):
    s = quiet(Make_Stretcher)
    self.assertAlmostEqual(s.GDD / STRETCHER_GDD, 1, places=9)
    self.assertAlmostEqual(s.TOD / STRETCHER_TOD, 1, places=9)

  def test_compressor_and_stretcher_have_opposite_gdd_sign(self):
    # Ein Stretcher dehnt den Puls, ein Compressor staucht ihn: entgegengesetzt
    c = quiet(Make_Compressor)
    s = quiet(Make_Stretcher)
    self.assertLess(c.GDD * s.GDD, 0)


def wavelength_span(rainbow):
  """Abstand der kürzesten und längsten Wellenlänge im RainbowBeam (in mm)."""
  wavelengths = [ray.wavelength for ray in rainbow._rays]
  return max(wavelengths) - min(wavelengths)


class TestBandwidthOfModules(unittest.TestCase):

  def test_compressor_lightsource_is_a_rainbow_beam(self):
    c = quiet(Make_Compressor)
    self.assertIsInstance(c._lightsource, RainbowBeam)

  def test_compressor_passes_its_bandwidth_to_the_lightsource(self):
    for band_width in (100e-9 * 1e3, 40e-9 * 1e3):   # in mm
      with self.subTest(band_width=band_width):
        c = quiet(Make_Compressor, band_width=band_width)
        self.assertAlmostEqual(wavelength_span(c._lightsource) / band_width,
                               1, places=9)

  def test_stretcher_lightsource_is_a_rainbow_beam(self):
    s = quiet(Make_Stretcher)
    self.assertIsInstance(s._lightsource, RainbowBeam)

  def test_stretcher_passes_its_bandwidth_to_the_lightsource(self):
    for bandwidth in (100e-9 * 1e3, 20e-9 * 1e3):    # in mm
      with self.subTest(bandwidth=bandwidth):
        s = quiet(Make_Stretcher, bandwidth=bandwidth)
        self.assertAlmostEqual(wavelength_span(s._lightsource) / bandwidth,
                               1, places=9)

  def test_stretcher_rejects_the_old_misspelled_keywords(self):
    # Make_Stretcher hat eine feste Signatur, alte Namen müssen laut scheitern
    for old in ({"seperation": 50}, {"seperation_angle": 0.1},
                {"band_width": 1e-4}):
      with self.subTest(keyword=list(old)[0]):
        with self.assertRaises(TypeError):
          quiet(Make_Stretcher, **old)

  def test_stretcher_accepts_the_corrected_keywords(self):
    s = quiet(Make_Stretcher, separation=60, separation_angle=0.2,
              bandwidth=5e-5)
    self.assertIsInstance(s._lightsource, RainbowBeam)


if __name__ == "__main__":
  unittest.main()
