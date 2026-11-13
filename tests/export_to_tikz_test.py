import os
import tempfile

from LaserCAD.moduls import Make_Telescope
from LaserCAD.basic_optics import export_to_TikZ

teles = Make_Telescope()

# Ausgabe nur auf der Konsole
export_to_TikZ(teles)

# Ausgabe zusaetzlich in eine Datei. export_to_TikZ haengt an eine bestehende
# Datei an, deshalb schreibt die Demo in ein temporaeres Verzeichnis, das
# danach geloescht wird (im Projektordner bleibt nichts liegen).
# Wer die .tex-Datei behalten will: filename="telescope.tex" angeben.
with tempfile.TemporaryDirectory() as folder:
  path = os.path.join(folder, "telescope.tex")
  export_to_TikZ(teles, filename=path)
  with open(path) as f:
    print("--- Inhalt von telescope.tex ---")
    print(f.read())
