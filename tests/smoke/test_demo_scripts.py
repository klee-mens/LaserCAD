# -*- coding: utf-8 -*-
"""
Smoke-Tests: führt alle Demo-Skripte aus und prüft, dass sie ohne Fehler
durchlaufen (Exit-Code 0).

Das ersetzt das manuelle Durchklicken von tests/run_all_tests.py: Statt
Fehlermeldungen in der Konsole zu suchen, gibt es pro Skript ein klares
OK / FAIL. Jedes Skript läuft in einem eigenen Prozess, damit sich Skripte
nicht gegenseitig beeinflussen (globale Zustände, geänderte Pfade, ...).

Geprüft wird nur, dass nichts abstürzt, nicht, ob das Ergebnis physikalisch
stimmt. Das übernehmen die Tests in tests/unit.

Matplotlib läuft ohne Fenster (Backend "Agg"), damit plt.show() nicht blockiert.

Umgebungsvariable LASERCAD_SMOKE_TIMEOUT: Zeitlimit pro Skript in Sekunden
(Standard 300).
"""
import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEMO_DIR = REPO_ROOT / "tests"
TUTORIAL_DIR = REPO_ROOT / "manual" / "tutorial"
TIMEOUT = int(os.environ.get("LASERCAD_SMOKE_TIMEOUT", "300"))

# Skripte in tests/, die keine Demos sind
NOT_A_DEMO = {"run_all_tests.py"}

# Tutorial-Skripte, die aktuell nachweislich fehlschlagen (Stand der Analyse).
# Sobald eines repariert ist, schlägt der Test mit einer entsprechenden Meldung
# an, und der Eintrag kann hier gelöscht werden.
KNOWN_BROKEN_TUTORIALS = {
  "6_LinearResonator.py":
    "importiert Crystal aus LaserCAD.basic_optics, die Klasse liegt aber in "
    "LaserCAD.non_interactings",
  "8_HeTutorial.py":
    "ruft Beam.make_circular_distribution auf, die Methode existiert nicht "
    "mehr (make_cone_distribution?)",
  "9_GUI.py":
    "importiert LaserCAD.GUI, dieses Paket gibt es im Repository nicht",
}


def run_script(path):
  """Führt <path> in einem eigenen Prozess aus, gibt CompletedProcess zurück."""
  env = dict(os.environ)
  env["MPLBACKEND"] = "Agg"
  env["PYTHONPATH"] = os.pathsep.join(
    [str(REPO_ROOT)] + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else []))
  return subprocess.run(
    [sys.executable, str(path)],
    cwd=str(path.parent), env=env, capture_output=True, text=True,
    stdin=subprocess.DEVNULL, timeout=TIMEOUT)


def last_lines(text, n=12):
  return "\n".join(text.strip().splitlines()[-n:])


def demo_scripts():
  return sorted(p for p in DEMO_DIR.glob("*.py") if p.name not in NOT_A_DEMO)


def tutorial_scripts():
  return sorted(TUTORIAL_DIR.glob("*.py"))


class TestDemoScripts(unittest.TestCase):
  """Alle Skripte direkt in tests/ (Demos und Beispiele)."""

  def test_demo_scripts_were_found(self):
    self.assertGreater(len(demo_scripts()), 20,
                       "Zu wenige Demo-Skripte gefunden, stimmt der Pfad?")

  def test_every_demo_script_runs_without_error(self):
    for script in demo_scripts():
      with self.subTest(script=script.name):
        result = run_script(script)
        self.assertEqual(
          result.returncode, 0,
          f"{script.name} endete mit Exit-Code {result.returncode}:\n"
          + last_lines(result.stderr))


class TestTutorialScripts(unittest.TestCase):
  """Skripte in manual/tutorial/: stellen sicher, dass die Doku funktioniert."""

  def test_tutorial_scripts_were_found(self):
    self.assertGreater(len(tutorial_scripts()), 5)

  def test_every_tutorial_script_runs_without_error(self):
    for script in tutorial_scripts():
      with self.subTest(script=script.name):
        result = run_script(script)
        reason = KNOWN_BROKEN_TUTORIALS.get(script.name)
        if reason is None:
          self.assertEqual(
            result.returncode, 0,
            f"{script.name} endete mit Exit-Code {result.returncode}:\n"
            + last_lines(result.stderr))
        elif result.returncode == 0:
          self.fail(f"{script.name} läuft jetzt durch! Bitte aus "
                    "KNOWN_BROKEN_TUTORIALS entfernen.")
        else:
          self.skipTest(f"bekannt defekt: {reason}")


if __name__ == "__main__":
  unittest.main()
