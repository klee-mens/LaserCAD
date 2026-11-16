# -*- coding: utf-8 -*-
"""
Generates the Markdown reference of LaserCAD from the signatures and the
docstrings of the code, so it can not drift away from the implementation.

Run from the project root (or anywhere):

    python manual/reference/build_reference.py

The pages are written next to this script. The unit test
tests/unit/test_reference.py fails if the committed pages are out of date,
so rerun this script after changing public classes, signatures or docstrings.
"""
import inspect
import io
import os
import re
import sys
import contextlib
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
if ROOT not in sys.path:
  sys.path.insert(0, ROOT)

with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
  warnings.simplefilter("ignore")
  import LaserCAD
  import LaserCAD.moduls as moduls
  import LaserCAD.moduls.interferometer as interferometer
  from LaserCAD.moduls.type_II_Amplifier import Make_Amplifier_Typ_II_plane
  from LaserCAD.moduls.delay_stage import Delay_Stage
  from LaserCAD.moduls.transmission_disk import Transmission_Disk
  from LaserCAD.moduls.motorized_TSF import Motorized_TSF

# page file name -> (title, introduction, predicate on the module name of a class)
PAGES = [
  ("geometry_rays_beams.md", "Geometry, rays and beams",
   "Basic objects: everything with a position and a direction, single rays and bundles of rays.",
   ("basic_optics.geom_object", "basic_optics.ray", "basic_optics.beam")),
  ("optical_elements.md", "Optical elements",
   "Elements that change the rays: mirrors, lenses, gratings, beam splitters and more.",
   ("basic_optics.optical_element", "basic_optics.mirror", "basic_optics.lens",
    "basic_optics.grating", "basic_optics.beam_splitter",
    "basic_optics.off_axis_parabola", "basic_optics.refractive_plane",
    "basic_optics.intersection_plane", "basic_optics.non_linear_crystal")),
  ("compositions.md", "Compositions and resonators",
   "Containers that place elements on an optical axis and compute the beams.",
   ("basic_optics.composition", "basic_optics.resonator",
    "basic_optics.multi_beam_line_composition")),
  ("mounts_components.md", "Mounts and components",
   "Mounts, posts and the base class for shaped components.",
   ("basic_optics.mount", "basic_optics.component")),
  ("non_interacting.md", "Non-interacting components",
   "Components that are drawn but do not change the rays.",
   ("non_interactings.",)),
]
MODULES_PAGE = ("modules.md", "Ready-made modules",
  "Functions and classes that build complete assemblies (telescopes, "
  "compressors, amplifiers, ...).")


def _fmt_default(value):
  if isinstance(value, (bool, int, float, str, type(None))):
    return repr(value)
  if isinstance(value, (tuple, list)):
    return repr(value)
  if isinstance(value, np.ndarray):
    return repr(value.tolist())
  return type(value).__name__ + "()"


def signature_text(obj, name):
  try:
    sig = inspect.signature(obj)
  except (TypeError, ValueError):
    return name + "(...)"
  parts = []
  star_added = False
  for p in sig.parameters.values():
    if p.kind == p.VAR_POSITIONAL:
      parts.append("*" + p.name)
    elif p.kind == p.VAR_KEYWORD:
      parts.append("**" + p.name)
    else:
      if p.kind == p.KEYWORD_ONLY and not star_added and not any(
          q.kind == q.VAR_POSITIONAL for q in sig.parameters.values()):
        parts.append("*")
        star_added = True
      if p.default is p.empty:
        parts.append(p.name)
      else:
        parts.append(f"{p.name}={_fmt_default(p.default)}")
  return f"{name}({', '.join(parts)})"


def doc_to_markdown(doc):
  """Convert a numpydoc-like docstring to simple Markdown."""
  if not doc:
    return ""
  lines = doc.split("\n")
  out = []
  i = 0
  in_params = False
  while i < len(lines):
    line = lines[i]
    nxt = lines[i + 1] if i + 1 < len(lines) else ""
    if line.strip() and nxt.strip() and set(nxt.strip()) == {"-"} and len(nxt.strip()) >= 3:
      out.append("")
      out.append(f"**{line.strip()}**")
      out.append("")
      in_params = line.strip() in ("Parameters", "Returns", "Attributes", "Important methods", "Methods")
      i += 2
      continue
    if in_params:
      m = re.match(r"^(\S[^:]*?)\s*:\s*(.*)$", line)
      if m and not line.startswith(" "):
        out.append(f"- `{m.group(1).strip()}` ({m.group(2).strip()})" if m.group(2).strip()
                   else f"- `{m.group(1).strip()}`")
      elif line.strip() and line.startswith(" "):
        out.append("  " + line.strip())
      elif line.strip():
        out.append(f"- {line.strip()}")
      else:
        out.append("")
    else:
      out.append(line)
    i += 1
  return "\n".join(out).strip("\n")


def first_line(doc):
  if not doc:
    return ""
  para = re.split(r"\n\s*\n", doc.strip())[0]
  text = " ".join(x.strip() for x in para.split("\n"))
  return text.replace("|", "\\|")


def public_members(cls):
  """Own public methods and properties of <cls>: list of (name, kind, obj)."""
  rows = []
  for name, value in vars(cls).items():
    if name.startswith("_"):
      continue
    if isinstance(value, property):
      rows.append((name, "property", value))
    elif isinstance(value, (staticmethod, classmethod)):
      rows.append((name, "method", value.__func__))
    elif inspect.isfunction(value):
      rows.append((name, "method", value))
  return sorted(rows, key=lambda r: r[0])


def member_doc(cls, name, obj):
  f = obj.fget if isinstance(obj, property) else obj
  doc = inspect.getdoc(f)
  if not doc:  # overriding method without own docstring: use the inherited one
    for base in cls.__mro__[1:]:
      if name in vars(base):
        b = vars(base)[name]
        b = b.fget if isinstance(b, property) else b
        doc = inspect.getdoc(b)
        if doc:
          break
  return doc or ""


def class_section(cls):
  lines = [f"### {cls.__name__}", ""]
  lines += ["```python", signature_text(cls, cls.__name__), "```", ""]
  bases = [b.__name__ for b in cls.__bases__ if b is not object]
  if bases:
    lines += ["*Inherits from:* " + ", ".join(f"`{b}`" for b in bases), ""]
  doc = cls.__dict__.get("__doc__")
  if doc:
    lines += [doc_to_markdown(inspect.cleandoc(doc)), ""]
  members = public_members(cls)
  if members:
    lines += ["| Member | Description |", "|---|---|"]
    for name, kind, obj in members:
      if kind == "property":
        label = f"`{name}` (property)"
      else:
        label = f"`{signature_text(obj, name).replace('self, ', '').replace('(self)', '()')}`"
      lines.append(f"| {label} | {first_line(member_doc(cls, name, obj))} |")
    lines.append("")
  return "\n".join(lines)


def function_section(func, name=None):
  name = name or func.__name__
  lines = [f"### {name}", "", "```python", signature_text(func, name), "```", ""]
  doc = inspect.getdoc(func)
  if doc:
    lines += [doc_to_markdown(doc), ""]
  return "\n".join(lines)


def public_classes():
  seen = {}
  for name in sorted(dir(LaserCAD)):
    obj = getattr(LaserCAD, name)
    if inspect.isclass(obj):
      seen[obj.__name__] = obj
  # classes that are not exported at top level but are useful
  for obj in (Delay_Stage, Transmission_Disk, Motorized_TSF):
    seen[obj.__name__] = obj
  return seen


def module_part(cls):
  return cls.__module__.replace("LaserCAD.", "")


def module_items():
  items = []
  for name in sorted(dir(moduls)):
    obj = getattr(moduls, name)
    if inspect.isfunction(obj) and name.startswith("Make_"):
      items.append((name, obj))
  for name, obj in ((n, getattr(interferometer, n)) for n in sorted(dir(interferometer))):
    if inspect.isfunction(obj) and name.startswith("Make_") and obj.__module__ == interferometer.__name__:
      items.append((name, obj))
  items.append(("Make_Amplifier_Typ_II_plane", Make_Amplifier_Typ_II_plane))
  uniq = {}
  for n, o in items:
    uniq[n] = o
  return sorted(uniq.items())


def build():
  """Return {file name: text} for all reference pages."""
  classes = public_classes()
  used = set()
  files = {}
  for fname, title, intro, mods in PAGES:
    chosen = []
    for cname, cls in classes.items():
      part = module_part(cls)
      if any(part == m or (m.endswith(".") and part.startswith(m)) for m in mods):
        chosen.append(cls)
    chosen.sort(key=lambda c: (mods.index(next(m for m in mods if module_part(c) == m or (m.endswith(".") and module_part(c).startswith(m)))), c.__name__))
    used.update(c.__name__ for c in chosen)
    text = [f"# {title}", "", intro, "",
            "*This page is generated by `manual/reference/build_reference.py` "
            "from the code. Do not edit it by hand.*", ""]
    text += ["Contents: " + ", ".join(f"[{c.__name__}](#{c.__name__.lower()})" for c in chosen), ""]
    for cls in chosen:
      text.append(class_section(cls))
    files[fname] = "\n".join(text).rstrip() + "\n"
  leftovers = [c for n, c in classes.items() if n not in used and c.__module__.startswith("LaserCAD.moduls")]
  fname, title, intro = MODULES_PAGE
  items = module_items()
  text = [f"# {title}", "", intro, "",
          "*This page is generated by `manual/reference/build_reference.py` "
          "from the code. Do not edit it by hand.*", ""]
  text += ["Contents: " + ", ".join(f"[{n}](#{n.lower()})" for n, _ in items + [(c.__name__, c) for c in leftovers]), ""]
  for n, f in items:
    text.append(function_section(f, n))
  for cls in leftovers:
    text.append(class_section(cls))
    used.add(cls.__name__)
  files[fname] = "\n".join(text).rstrip() + "\n"
  missing = [n for n in classes if n not in used]
  if missing:
    raise RuntimeError("Classes not assigned to a reference page: " + ", ".join(sorted(missing)))
  index = ["# Reference", "",
           "Interfaces of the public classes and functions of LaserCAD, generated from the code.", ""]
  for f, t, intro, _ in PAGES:
    index.append(f"- [{t}]({f}): {intro}")
  index.append(f"- [{MODULES_PAGE[1]}]({MODULES_PAGE[0]}): {MODULES_PAGE[2]}")
  index += ["", "For the ideas behind the classes see the discussion in `manual/docs`.", ""]
  files["README.md"] = "\n".join(index)
  return files


def write(files=None):
  files = files or build()
  for name, text in files.items():
    with open(os.path.join(HERE, name), "w", encoding="utf-8", newline="") as f:
      f.write(text.replace("\n", "\r\n"))
  return sorted(files)


if __name__ == "__main__":
  names = write()
  print("written:", ", ".join(names))
