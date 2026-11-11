# Tests für LaserCAD

Es gibt zwei Arten von Dateien in diesem Ordner:

| Ort | Zweck |
|---|---|
| `tests/unit/` | **Automatische Tests** mit Erwartungswerten (`assert`). Prüfen die Rechenlogik, brauchen kein FreeCAD. |
| `tests/smoke/` | Führt alle **Demo-Skripte** aus (`tests/*.py` und `manual/tutorial/*.py`) und meldet pro Skript OK oder FAIL. |
| `tests/*.py` | Die bisherigen Demo-Skripte. Sie zeigen, was LaserCAD kann, und bleiben unverändert. |

## Ausführen

Vorher einmalig das Paket verfügbar machen (aus dem Projektordner):

    python -m pip install -e .

oder alternativ `PYTHONPATH` auf den Projektordner setzen (siehe README im Hauptordner).

Mit der Python-Standardbibliothek (nichts weiter nötig):

    python -m unittest discover -s tests/unit -v      # schnell, < 1 s
    python -m unittest discover -s tests/smoke -v     # alle Demos, ca. 1 Minute

Mit pytest (falls installiert, `pytest.ini` im Hauptordner begrenzt die Suche
auf `tests/unit` und `tests/smoke`):

    pytest
    pytest tests/unit/test_lens.py -k focus

## Hinweise

* **Warum `pytest.ini`?** Die Demo-Skripte heißen `*_test.py`. pytest würde sie
  sonst beim Einsammeln als Tests behandeln und ausführen.
* **`expectedFailure`**: Ein so markierter Test beschreibt Verhalten, das gelten
  *sollte*, aber aktuell nicht gilt (siehe Kommentar im Test). Er färbt die Suite
  nicht rot. Wird der Fehler behoben, meldet der Test "unexpected success", dann
  den Dekorator entfernen.
* **`KNOWN_BROKEN_TUTORIALS`** in `tests/smoke/test_demo_scripts.py` listet
  Tutorial-Skripte, die bekanntermaßen nicht laufen. Wird eines repariert,
  meldet der Test das und der Eintrag kann gelöscht werden.
* **Toleranzen**: Die dünne Linse rechnet paraxial. Die Tests verwenden daher
  kleine Strahlhöhen und Toleranzen (siehe Kopf von `test_lens.py`).
* Die Smoke-Tests starten jedes Skript in einem eigenen Prozess mit
  Matplotlib-Backend `Agg`, es öffnen sich also keine Fenster.
