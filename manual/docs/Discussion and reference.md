# Discussion and Explanation

## Why LaserCAD?

As already described in He's reports and the presentation, it can be pretty advantageous to visualise an optical setup completely in 3D on the computer in advance. This makes planning, discussions with colleagues and setbacks and compromises in the lab due to space problems and clipping easier, as they almost always inevitably occur when you go from a pencil sketch to the actual setup. Particularly when setting up laser systems, in which nested beam paths with many folds are common and every aperture is used sparingly, problems are repeatedly encountered during experiments that could have been avoided with a 3D sketch at the planning stage.
Most software packages for this, such as Zeemax and others, have the problem of offering super-precise ray tracing calculations, which are usually not needed in the case of paraxial laser beams. Still, in return, they also demand vast amounts of unnecessary information, usually with a very inflexible and non-modular interface. And then there are the high costs and license hurdles. In addition, most software packages cannot easily integrate mechanical peripherals such as mirror holders, Pockels cell housings, posts, and the like, which are usually the very objects that cause problems during the realisation of the setup.
In short, the goal is to develop an easy-to-use, script-based, modular software that can output a structure as realistically as possible in 3D with just a few lines of code, with the option of manual post-processing and exporting. The principles are:
1. make the typical case simple.
2. the user should be able to set everything in the script, but the default values should also be set so well that you don't have to.
3. the code should be designed comprehensibly so that you know where to reprogram something if necessary.

Installation and Import
The project can be imported directly from Github to any location, but for development in an IDE such as Spyder, a location in the standard directory (e.g. '/usr/lib/python3.11/site-packages/') is recommended. The clone command can be downloaded in the terminal with

git clone https://github.com/klee-mens/LaserCAD

The intended workflow includes an IDE for scripting the optical setup, testing for bugs, and then executing the resulting Python script in FreeCAD; see figure below.

<img src="images/overview_windows.png" alt="StretcherStuff" title="" />



Unfortunately, FreeCAD has its own package sources and default directories, so there is no trivial solution for using and importing LaserCAD on both sides. The standard solution is to start all projects in the LaserCAD package or subfolders and add the following lines from the tutorial 1_ImportTest.py:

```python
import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)

from LaserCAD.basic_optics import Mirror
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()

if freecad_da:
  setview()
```

# Construction and object structure

LaserCAD is based on a combination of an extensive Python program for defining and calculating all the necessary objects and an interface for using FreeCAD as an output program for visualization in 3D.
The objects are presented and explained below:


## Constants

The constants module contains all the constants that are important for LaserCAD.
```python
import numpy as np

c = 3e8
h = 6e-34
inch = 25.4 # Grundeinheit für Optikdurchmesser
NAME0="unnamed"
POS0 = np.array((0,0,80)) #Strahlhöhe 80 mm
NORM0 = np.array((1,0,0)) #Strahl startet in x-Richtung
TOLERANCE = 1e-9 #Wert ab dem zwei GröÃŸen (meist Winkel) als gleich angenommen werden
```

TOLERANCE describes the value from which a quantity is assumed to be equal to zero. For example, two vectors are assumed to be parallel if the magnitude of their cross-product is less than TOLERANCE.

## Geom_Object

All basic objects are located in the "basic_optics" folder, even though strictly speaking it contains much more than optics. The basic object from which all others inherit is called Geom_Object and, in turn, inherits from the object (standard Python object).
The core task of this data structure is to store and edit the position "pos" and orientation "axes" and "normal" in 3D space.

```python
class Geom_Object(object):
  """
  speichert die elementaren Informationen über Position <pos>, Ausrichtung
  <normal> und Namen <name>,
  Definiert die Defaults für alle folgenden Objekte, passt bei Ã„nderung der
  <normal> automatisch das innere Koordiantwensystem <_axes> an und ruft dann
  die Hilfsfunktionen <_pos_changed> und <_axes_changed> auf

  führt zur Darstellung das <draw_dict> mit allen wichtigen keyword arguments
  ein, kann beliebig erweitert werden, wird an die draw_fc Routinen weiter
  gegeben

  stores the elementary information about position <pos>, alignment
  <normal> and name <name>,
  defines the defaults for all subsequent objects, automatically adjusts the
  <normal> automatically adjusts the inner coordinate system <_axes>, and then
  calls the auxiliary functions <_pos_changed> and <_axes_changed>.

  introduces the <draw_dict> with all important keyword arguments for the
  display can be extended arbitrarily, is passed to the draw_fc routines given

  siehe tests()
  """
  def __init__(self, name=NAME0, **kwargs):
    self.name = name
    self._pos = POS0
    self._axes = np.eye(3)
    # das eigene Kordinatensystem, die erste Spalte ist immer die Normale
    self.draw_dict = {"name": self.name, "geom":self.get_geom()}

  @property
  def pos(self):
    """
    beschreibt die Position des GeomObject als 3D-numpy-float-array
    stellt über Setter und Getter sicher, dass nur Kopien übergeben werden und
    das _pos_changed aufgrufen wird

    describes the position of the GeomObject as 3D-numpy-float-array
    uses setters and getters to make sure that only copies are passed and that
    the _pos_changed is called

    """
    return np.array(self._pos) * 1.0

  @pos.setter
  def pos(self, x):
    old_pos = self._pos
    self._pos = np.array(x) * 1.0
    self._pos_changed(old_pos, x)

  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird, kann nützlich
    sein für abgeleitete, zusammengesetzte Objekte wie beam oder composition

    is called when the position of <self> is changed, can be useful for derived
    for derived composite objects like beams or composition
    """
    pass

  def _rearange_subobjects_pos(self, old_pos, new_pos, objs):
    """
    wichtig für beam und Composition
    wenn eigene <old_pos> auf <new_pos> geändert wird, soll die pos aller
    Subobjekte entsprechend geändert werden, d.h. relative Ausrichtung und
    Drehung soll beibehalten werden
    ...LinAlg Kram halt

    important for beam and composition
    if custom <old_pos> is changed to <new_pos>, the pos of all
    subobjects should be changed accordingly, i.e. relative orientation and
    rotation should be kept
    ...LinAlg stuff halt
    """
    delta_pos = new_pos - old_pos
    for obj in objs:
      obj.pos += delta_pos
```


Setting and reading the position works with :
obj.pos = (1,2,3)
print(obj.pos)
The _rearange_subobjects_pos function is required for container objects such as Composition, Beam and Composed_Mount.

```python

  @property
  def normal(self):
    """
    Beschreibt die Ausrichtung (= interne x-Achse) des GeomObject als 3D-numpy-
    float-array mit Betrag 1
    stellt über Setter und Getter sicher, dass nur Kopien übergeben werden, der
    Vektor stehts normiert wird und das die _axes aktualisiert wird

    Describes the orientation (= internal x-axis) of the GeomObject as a 3D-
    numpy-float-array with amount 1
    ensures via setter and getter that only copies are passed, that the vector
    is vector is always normalized and the _axes is updated.

    """
    return np.array(self._axes[:,0])

  @normal.setter
  def normal(self, x):
    old_normal = self.normal
    new_normal = x / np.linalg.norm(x)
    self.set_axes(self._updated_axes(new_normal, old_normal))

  def _updated_axes(self, new_normal, old_normal):
    """
    old_normal : 3D-array
    berechnet das neue Koordinatensystem durch Drehmatrix zwischen
    (neu-) normal und old_normal (setzt es aber nicht)

    old_normal : 3D-array
    calculates the new coordinate system by rotation matrix between
    (new-) normal and old_normal (but does not set it)
    """
    rotvec = np.cross(new_normal, old_normal) # Drehvektor
    v_abs = np.linalg.norm(rotvec)
    skalarP = np.sum(new_normal * old_normal)
    if v_abs < TOLERANCE:
      if skalarP >= 0:
        # phi kleiner als 1e-8
        return self._axes
      else:
        a,b,c = self.get_coordinate_system()
        a = new_normal #just in case
        b*=-1
        x=np.array([a[0],b[0],c[0]])
        y=np.array([a[1],b[1],c[1]])
        z=np.array([a[2],b[2],c[2]])
        # return np.vstack((x,y,z))
        return np.vstack((x,y,z))
    else:
      rot_mat = rotation_matrix_from_vectors(old_normal, new_normal)
      return np.matmul(rot_mat, self._axes)

  def _axes_changed(self, old_axes, new_axes):
    """
    wird aufgerufen, wen das Koordinatensystem >_axes> von <self> verändert
    wird,kann nützlich sein für abgeleitete, zusammengesetzte Objekte wie beam
    oder composition

    is called when the coordinate system >_axes> of <self> is changed.
    can be useful for derived composite objects like beam
    or composition
    """
    pass

  def _rearange_subobjects_axes(self, old_axes, new_axes, objs):
    """
    wichtig für beam und Composition
    wenn eigene <old_axes> auf <new_axes> geändert wird, soll die _axes
    aller Subobjekte entsprechend geändert werden, d.h. relative Ausrichtung
    und Drehung soll beibehalten werden
    ...LinAlg Kram halt

    important for beam and composition
    if custom <old_axes> is changed to <new_axes>, the _axes
    of all subobjects should be changed accordingly, i.e. relative orientation
    and rotation should be kept
    ...LinAlg stuff halt
    """
    RotM = np.matmul(new_axes, np.linalg.inv(old_axes) )
    p0 = self.pos
    for obj in objs:
      qvec = obj.pos - p0 # relativer Orstvector innnerhalb der Einheit
      new_qvec = np.matmul(RotM, qvec)
      obj.pos = new_qvec + p0
      obj.set_axes( np.matmul( RotM, obj.get_axes() ) )

  def get_axes(self):
    """
    gibt das eigene Kooridnatensystem _axes als 3x3 Matrix zurück
    indem die x,y,z-Vektoren als Spaltenvektoren stehen

    returns the own coordinate system _axes as 3x3 matrix
    where the x,y,z-vectors are column vectors
    """
    return np.array(self._axes)

  def get_coordinate_system(self):
    """
    gibt normal (x), senkrecht1 (y) und senkrecht2 (z) als 3 Vektoren zurück
    (transponiert zu self.get_axes)

    returns normal (x), perpendicular1 (y) and perpendicular2 (z) as 3 vectors
    (transposed to self.get_axes)
    """
    mat = np.array(self._axes)
    return mat[:,0], mat[:,1], mat[:,2]

  def set_axes(self, new_axes):
    """
    setzt das eigene Koordinatensystem auf <new_axes> und ruft
    _axes_changed auf

    new_axes : reelle, orthogonale 3x3 numpy float Matrix mit Determinante +1

    sets the own coordinate system to <new_axes> and calls
    _axes_changed

    new_axes: real, orthogonal 3x3 numpy float matrix with determinant +1
    """
    old_axes = self.get_axes()
    self._axes = np.array(new_axes)
    self._axes_changed(old_axes, new_axes)

  def get_geom(self):
    """
    gibt das so genannte geom = (pos, axes) zurück, einfach nur ein Tupel aus
    <pos> und <axes>, wichtig zur geometrischen Definition der meisten Objekte

    returns the so-called geom, simply a tuple of <pos> and
    <axes>, important for the geometric definition of most objects
    """
    return (self.pos, self.get_axes())

Every object derived from Geom_Object (and therefore pretty much every object in LaserCAD) has a right-handed, orthonormal coordinate system, which can be output via get_axes() and set via set_axes. Most frequently, however, only the normal of an object is explicitly set by the user; it always corresponds to the x-axis and can be set via obj.normal = (1,1,0), for example. The setter automatically normalizes the vector, then the inner coordinate system is adjusted and the corresponding _rearange_subobjects_axes function is called for container objects.

  def set_geom(self, geom):
    """
    setzt (pos, axes) auf geom indem es die entsprechenden setter Funktionen
    aufruft

    Parameters
    ----------
    geom : 2-dim Tupel aus 3-D float arrays
      (pos, axes)
    """
    self.pos = np.array(geom[0])
    self.set_axes(geom[1])

In most cases, however, objects are adapted via get_ and set_geom, usually from higher-level structures such as Composition.add_on_axis(obj).
Here and in the following, the tuple (pos, axes), i.e. a 3D vector and a 3x3 matrix, is referred to as "geom".

  def angle_to(self, obj):
    """
    computes the angle to the normal of an other GeomObj <obj> with
    correct sign

    """
    vec = obj.normal
    c = np.cross(self.normal, vec)
    abs_c = np.linalg.norm(c)
    if abs_c > 1: #because you know rounding errors and stuff
      abs_c = 1
    elif abs_c < -1:
      abs_c = -1
    sign = 1 if np.sum(c * self._axes[:,1]) >= 0 else -1
    return np.arcsin(abs_c)*sign

  def rotate(self, vec, phi):
    """
    rotiert das Objekt in Bezug auf vec um den Winkel phi
    Parameters
    ----------
    vec : 3D-Vector
      Raumrichtung um die gedreht wird, muss nicht normiert sein
    phi : Winkel im BogenmaÃŸ

    Bsp: element.rotate((0,1,0), 0.7854)
    entspricht Drehung um y-Achse um 45Â°

    rotates the object with respect to vec by the angle phi
    Parameters
    ----------
    vec : 3D vector
      Space direction around which is rotated, must not be normalized
    phi : angle in radians

    Ex: element.rotate((0,1,0), 0.7854)
    corresponds to rotation around y-axis by 45Â°.

    """
    rot_mat = rotation_matrix(vec, phi)
    new_ax = np.matmul(rot_mat, self._axes)
    self.set_axes(new_ax)
```

Auxiliary functions for positioning and rotating could also be extended as required, e.g. with Euler angles, etc. .
```python

  def __repr__(self):
    txt = self.class_name()+ '(name="' + self.name
    txt += '", pos='+vec2str(self.pos)
    txt += ", normal="+vec2str(self.normal)+")"
    return txt

  def __str__(self):
    return ">>> " + repr(self)

  def class_name(cls):
    return str(type(cls)).split(".")[-1].split("'")[0]

Functions for the output in the terminal. As a rule, the expression x = eval(repr(y)) should create an object x similar to y. Due to immense malicious bugs and loops in the more complex objects, the explicit setting of pos and normal in the constructor (of the __init__ function) was prohibited by decision, which is why this property must then be changed subsequently. Every object in LaserCAD is created at the default position POS0 = (0,0,80) with the normal = NORM0 = (1,0,0) in the x-direction and can only be moved after complete initialisation.

  def update_draw_dict(self):
    """
    wird meist for den draw_routinen aufgerufen und kann die wichtigesten
    key word arguments des <draw_dict> aktualisieren, falls sie genändert
    wurden (z.B. self.radius von Curved_Mirror)

    is usually called for the draw_routines and can update the most important
    key word arguments of <draw_dict> if they have been changed (e.g.
    self.radius of have been changed (e.g. self.radius of Curved_Mirror).
    """
    self.draw_dict["name"]=self.name
    self.draw_dict["geom"]=self.get_geom()

  def draw(self):
    """
    Funktion zur Darstellung des Objekts
    prüft nach, ob freecad als Backend verfügbar ist und ruft dann die
    entsprechende draw-Funktion auf

    function to display the object
    checks whether freecad is available as backend and then calls the
    corresponding draw function
    """
    if freecad_da:
      return self.draw_freecad()
    else:
      txt = self.draw_text()
      print(txt)
      return txt

  def draw_freecad(self):
    """
    ruft falls FreeCAD vorhanden ist die entsprechende Zeichenfunktion aus
    freecad_models auf, gibt im Normalfall eine Referenz auf das entsprechende
    FreeCAD-Objekt zurück

    if FreeCAD is present, calls the corresponding drawing function from
    freecad_models, normally returns a reference to the corresponding
    FreeCAD object
    """
    self.update_draw_dict()
    return self.freecad_model(**self.draw_dict)

  def freecad_model(self, **kwargs):
    # ToDo: fürs Debugging hier einfachch einen Zylinder mit norm uns k zeichnen
    return None

  def draw_text(self):
    """
    falls FreeCAD nicht zur Verfügung steht, wird das Objekt in die Konsole
    "gezeichnet", d.h. alle relevanten Parameter aus dem <draw_dict> werden
    per Text ausgegeben, gibt den Text als str zurück

    if FreeCAD is not available, the object will be "drawn" into the console.
    "drawn", i.e. all relevant parameters from the <draw_dict> will be
    by text, returns the text as str
    """
    self.update_draw_dict()
    txt = "The geometric object <" + self.class_name() + ":" + self.name
    txt += "> is drawn to the position"
    txt += vec2str(self.pos) + " with the direction " + vec2str(self.normal)
    return txt
```


Each object has a draw function. First, This checks whether the Python script is executed in a standard terminal or FreeCAD using the boolean variable freecad_da. Depending on the result, it calls draw_txt as text output or draw_freecad. The latter then draws the object and returns a link to it to save it later in a higher-level structure such as Composition. In principle, all draw_freecad functions are based on the exact procedure: first, the draw_dict of the object is updated with update_draw_dict, and then the corresponding freecad_model is called with all the arguments from the draw_dict. As expected, the draw_dict consists of a dictionary as a data type, which contains all the relevant parameters for the drawing, e.g. for a lens, the two radii of curvature, the thickness, the aperture and, of course, the position and orientation as a geom. Following the credo from the beginning of the chapter, pretty much any function and thus also, for example, the model_lens function from the freecad_models folder can be called without any arguments, as all values in the function are already set as default and additional keyword arguments are intercepted via the classic **kwargs variable. Conversely, it is also possible to save additional keyword arguments in the draw_dict. For example, almost every model function also accepts the keyword colour = (R/255, G/255, B/255), where RGB 8-bit integer values between 0 and 255 can describe the colour of the object in a known way. See also the tutorial 2_PositionAndAxes.


## Ray

The Ray is the class for one-dimensional rays, the code is listed here:

```python

class Ray(Geom_Object):
  """
  Klasse für Strahlen
  erbt von Geom_Object
  besitzt neben pos und normal auch length zum zeichnen
  neue Methoden:
    endpoint()
    intersection_with(element)
    h_alpha_to(element)
    h_alpha_theta_to(element)
    from_h_alpha_theta
  """
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.length = DEFAULT_LENGTH #willkürlich, muss immer neu berechnet werden
    self.wavelength = 660e-6 #Wellenlänge in mm; Default: 660nm
    self.update_draw_dict()
    self.freecad_model = model_ray_1D
    # self.draw_dict.update({"length":self.length})

  def endpoint(self):
    return self.pos + self.length * self.normal

  def intersection(self, element):
    """
    ermittelt den Schnittpunkt vom Strahl mit der ebene eines opt Elements

    Parameters
    ----------
    element : Geom_Object
      Element mit dessen Ebene der Schnittpunkt berechnet wird

    Returns
    -------
    endpoint

    """
    delta_p = element.pos - self.pos
    s = np.sum(delta_p*element.normal) / np.sum(self.normal * element.normal)
    return self.pos + s * self.normal

  def intersect_with(self, element):
    """
    ermittelt den Schnittpunkt vom Strahl mit der ebene eines opt Elements
    und setzt seine Länge auf den Abstand self.pos--element.pos (bedenken!)

    Parameters
    ----------
    element : Geom_Object
      Element mit dessen Ebene der Schnittpunkt berechnet wird

    Returns
    -------
    endpoint

    """
    delta_p = element.pos - self.pos
    s = np.sum(delta_p*element.normal) / np.sum(self.normal * element.normal)
    self.length = s
    return self.endpoint()

  def intersect_with_sphere(self, center, radius):
    """
    ermittelt den Schnittpunkt vom Strahl mit einer Spähre, die durch
    <center> â‚¬ R^3 und <radius> â‚¬ R definiert ist
    und setzt seine Länge auf den Abstand self.pos--element.pos (bedenken!)
    siehe Springer Handbook of Lasers and Optics Seite 66 f

    Parameters
    ----------
    center : TYPE 3D-array
      Mittelpunkt der Sphäre

    radius : TYPE float
      Radius der Sphäre; >0 für konkave Spiegel (Fokus), <0 für konvexe

    Returns
    -------
    endpoint : TYPE 3D-array
    """
    diffvec = center - self.pos
    k = np.sum( diffvec * self.normal )
    w = np.sqrt(k**2 - np.sum(diffvec**2) + radius**2)
    s1 = k + w
    s2 = k - w
    #Fallunterscheidung
    if radius < 0 and s2 > 0:
      dist = s2
    else:
      dist = s1
    self.length = dist
    endpoint = self.endpoint()
    return endpoint

  def sphere_intersection(self, center, radius):
    """
    ermittelt den Schnittpunkt vom Strahl mit einer Spähre, die durch
    <center> â‚¬ R^3 und <radius> â‚¬ R definiert ist
    und setzt seine Länge auf den Abstand self.pos--element.pos (bedenken!)
    siehe Springer Handbook of Lasers and Optics Seite 66 f

    Parameters
    ----------
    center : TYPE 3D-array
      Mittelpunkt der Sphäre

    radius : TYPE float
      Radius der Sphäre; >0 für konkave Spiegel (Fokus), <0 für konvexe

    Returns
    -------
    endpoint : TYPE 3D-array
    """
    diffvec = center - self.pos
    k = np.sum( diffvec * self.normal )
    w = np.sqrt(k**2 - np.sum(diffvec**2) + radius**2)
    s1 = k + w
    s2 = k - w
    #Fallunterscheidung
    if radius < 0 and s2 > 0:
      dist = s2
    else:
      dist = s1
    # self.length = dist
    endpoint = self.pos + dist * self.normal
    return endpoint

  def h_alpha_to(self, element):
    """
    ermittelt die Parameter (h, alpha) der geometrischen Optik, wenn Ray()
    auf ein Element trifft (verwendet intersection)
    """
    p = self.intersection(element)
    h = np.linalg.norm(p - element.pos)
    v = element.normal
    return np.array((h, self.angle_to(v)))

  def h_alpha_theta_to(self, element):
    """
    ermittelt die Parameter (h, alpha) der geometrischen Optik, wenn Ray()
    auf ein Element trifft, sowie den Winkel <theta> unter dem die ray.normal zur
    z-Achse des elements steht (verwendet intersection)
    """
    h, alpha = self.h_alpha_to(element)
    ep = self.endpoint()
    v = ep - element.pos
    vabs = np.linalg.norm(v)
    if vabs < TOLERANCE:
       theta = 0 # kein Winkel bestimmbar, default=0
    else:
       v = v / vabs
       xa, ya, za = element.get_axes()
       c = np.cross(za, v) #Winkel mit z-Achse
       sign = 1 if np.sum(c * xa) >= 0 else -1
       theta = np.arcsin(np.linalg.norm(c))*sign
    return (h, alpha, theta)

  def from_h_alpha_theta(self, h, alpha, theta, element):
    """
    setzt das ray geom so, dass er in Bezug auf <element> die geometrischen
    Parameter <h, alpha, theta> hat

    Parameters
    ----------
    h : float
    alpha : float - Winkel im BogenmaÃŸ
    theta : float - Winkel im BogenmaÃŸ
    element : geom_object
    """
    self.set_geom(element.get_geom())
    # pos, norm = element.get_geom()
    # pos = element.pos
    # norm = element.normal
    xa, ya, za = element.get_coordinate_system()
    vec_in_eb = za*np.cos(theta) - ya*np.sin(theta)
    self.pos += vec_in_eb*h
    rotation_vec = np.cross(vec_in_eb, xa)
    self.rotate(rotation_vec, -alpha)

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["length"] = self.length
```

It has the additional properties of wavelength (which is only used for grids and sometimes for display) and length. The endpoint can be calculated from the latter. The functions intersection and intersect_with calculate the intersection with an infinitely extended plane represented by an element using its pos and normal. The only difference between the functions is that the latter also sets the ray's length to the calculated endpoint. Both functions return the intersection point. The sphere_intersection functions are defined in the same way. The function h_alpha_to returns the two important quantities r and alpha from the ABCD matrix formalism, which the ray would have with respect to an element (i.e. its pos and normal). The FreeCAD model for the ray is the model_ray_1D function.

## Beam

Beam represents the class for extended, 3-dimensional rays and consists of a list of rays and some auxiliary functions. The standard is a cone beam ("model="cone"), which is defined in the constructor via radius and angle, i.e. r and alpha from the matrix optics. It contains precisely two rays as a standard value: the inner_ray, which determines the position, direction and length of the beam, and a ray that lies on the lateral surface and thus defines radius_angle, as known from matrix optics. Various distribution functions such as make_square_distribution can be used for deviating beam shapes. The get_all_rays method returns all the rays that make up the beam; the override_rays function overwrites them.
Several models are available in draw_dict, such as the semi-transparent cone or the simple collection of rays (ray_group, or as a fallback method if the model is not recognised).
```python

class Beam(Geom_Object):
  """
  Base class for a group of rays (you don't say!)
  special funcitoins: make_square_distribution(radius=1, ray_count=5)
  make_circular_distribution(radius=1, ray_count=5)
  average_divegence = ?

  """
  def __init__(self, radius=1, angle=0, name="NewBeam",wavelength=1030E-6, distribution="cone", **kwargs):
    super().__init__(name=name, **kwargs)
    self._ray_count = 2
    self._rays = [Ray() for n in range(self._ray_count)]
    self._angle = angle
    self._radius = radius
    self._distribution = distribution
    self._Bwavelength = wavelength
    if distribution == "cone":
      self.make_cone_distribution()
      self.draw_dict["model"] = "cone"
    elif distribution == "square":
      self.make_square_distribution()
      self.draw_dict["model"] = "ray_group"
    elif distribution == "circular":
      self.make_circular_distribution()
      self.draw_dict["model"] = "ray_group"
    elif distribution == "Gaussian":
      z0 = wavelength/(np.pi*np.tan(angle)*np.tan(angle))
      w0 = wavelength/(np.pi*np.tan(angle))
      if w0>radius:
        print("Woring: Wrong Radius!")
      z = z0*pow((radius*radius)/(w0*w0)-1,0.5)
      if angle<0:
        z = -z
      q_para = complex(z,z0)
      self.wavelength = wavelength
      self.q_para = q_para
      self.make_Gaussian_distribution()
      self.draw_dict["model"] = "Gaussian"
    else:
      # Abortion
      print("Distribution tpye not know. Beam not valid.")
      print("Allowed distribution types are: 'cone', 'square', 'circular', 'Gaussian'")
      self = -1
      return None

  def make_cone_distribution(self, ray_count=2):
    self._ray_count = ray_count
    self._rays = [Ray() for n in range(self._ray_count)]
    self._distribution = "cone"
    self.draw_dict["model"] = "cone"
    mr = self._rays[0]
    mr.set_geom(self.get_geom())
    mr.name = self.name + "_inner_Ray"
    mr.wavelength = self._Bwavelength
    thetas = np.linspace(0, 2*np.pi, self._ray_count)
    for n in range(self._ray_count-1):
      our = self._rays[n+1]
      our.from_h_alpha_theta(self._radius, self._angle, thetas[n], self)
      our.name = self.name + "_outer_Ray" + str(n)
      our.wavelength = self._Bwavelength

  def make_Gaussian_distribution(self, ray_count=2):
    self._ray_count = 1
    self._distribution = "Gaussian"
    self.draw_dict["model"] = "Gaussian"
    mr = self._rays[0]
    mr.set_geom(self.get_geom())
    mr.name = self.name + "_inner_Ray"


  def make_square_distribution(self, ray_in_line=3):
    """
    Let the group of rays follow the square distribution
    The width of square equals 2*radius of ray group
    Parameters
    ----------
    ray_in_line : int(>0)
      rays in a line.That is going to determine the density of ray.

    Returns
    -------
    None.

    """
    self._rays = [Ray() for n in range((ray_in_line)**2)]                     #calculate the number of rays,set the rays group
    ray_counting=0
    radius=self._radius
    for n in np.arange(-radius,radius+radius/(ray_in_line-1),
                       2*radius/(ray_in_line-1)):                              #n repersents y coordinates of the ray
      for m in np.arange(-radius,radius+radius/(ray_in_line-1),
                         2*radius/(ray_in_line-1)):                            #m repersents z coordinates of the ray
        self._rays[ray_counting].set_geom(self.get_geom())
        self._rays[ray_counting].pos=self._rays[ray_counting].pos+(0,n,m)     #change the position of the ray
        self._rays[ray_counting].name=self.name+str(ray_counting)
        self._rays[ray_counting].wavelength = self._Bwavelength
        ray_counting+=1
    # print(ray_counting) # ray_counting is the number of the rays.
    self._ray_count = ray_counting
    self._distribution = "square"
    self.draw_dict["model"] = "ray_group"

  def make_circular_distribution(self, ring_number=2):
    """
    Let the group of rays follow the circular distribution
    The radius of circle equals the radius of ray group
    Parameters
    ----------
    ring_number : int(>0).
      The number of the rings around the center. That is going to
     determine the density of ray.

    Returns
    -------
    None.

    """

    self._rays = [Ray() for n in range(3*ring_number*(ring_number+1)+1)]      #calculate the number of rays,set the rays group
    ray_counting=0
    radius=self._radius
    for r in np.arange(0,radius+radius/ring_number/2,radius/ring_number):        #r repersents the height of the ray

      if r!=0:                                                                 #if the ray is not in the center
        thetas = np.linspace(0, 2*np.pi, int(r*ring_number/radius)*6+1)        #thetas repersents the rotation angle of the ray
        for n in range(int(r*ring_number/radius)*6):
          our=self._rays[ray_counting]
          # self._rays[ray_counting].wavelength = self._Bwavelength
          our.from_h_alpha_theta(r, self._angle, thetas[n], self)            # rotate the ray which is not in the center
          our.name=self.name + "_circular_distribution_Ray" +str(ray_counting)
          ray_counting+=1
      else:
        # self._rays[ray_counting].wavelength = self._Bwavelength
        mr=self._rays[ray_counting]
        mr.set_geom(self.get_geom())
        mr.name = self.name + "_inner_Ray"
        ray_counting+=1
    # print(ray_counting) # ray_counting is the number of the rays.
    self._ray_count = ray_counting
    # print(ray_counting)
    for r in range(0,self._ray_count):
      self._rays[r].wavelength = self._Bwavelength
    self._distribution = "circular"
    self.draw_dict["model"] = "ray_group"

  def override_rays(self, rays):
    """
    setzt die rays neu, muss man eventuell aufpassen, mal sehen

    resets the rays, you may have to watch out, let's see

    Parameters
    ----------
    rays : list of rays
    """
    rc = len(rays)
    self._ray_count = rc
    self._rays = rays
    self._axes = rays[0].get_axes()
    self._pos = rays[0].pos
    for n in range(len(rays)):
      rays[n].name = self.name + "_ray" + str(n)
    rays[0].name = self.name + "_middle_ray"

  def __repr__(self):
    radius, angle = self.radius_angle()
    txt = 'Beam(radius=' + repr(radius)
    txt += ', anlge=' + repr(angle)
    txt += ', distribution=' + repr(self._distribution)
    if self._distribution == "Gaussian":
       txt = 'Gaussian_Beam(q_para=' + repr(self.q_para)
    txt += ', ' + super().__repr__()[6::]
    return txt

  def radius_angle(self):
    """
    berechnet aus 2 Strahlen inn und outer den zugehörigen beam Kegel mit
    radius r und öffnungswinkel alpha und zwar von hinten durch die Brust
    ins Auge
    """
    inner = self._rays[0]
    outer = self._rays[1]
    v0 = inner.normal
    v1 = outer.normal
    poi = outer.intersection(inner) #Punkt in der Kegelgrundfläche, in dem outer schneidet
    ovec = poi - inner.pos
    novec = np.linalg.norm(ovec)
    if novec < TOLERANCE:
      #beide rays im gleichen Punkt, h = 0, alpha>0
      return novec, np.arccos(np.sum(v0 * v1))
    else:
      ovec /= novec #normieren
      a = np.sum(v1 * ovec)
      b = np.sum(v0 * v1)
    return novec, np.arctan(a/b)

  def get_all_rays(self, by_reference=False):
    if by_reference:
      return self._rays
    else:
      return deepcopy(self._rays)

  def inner_ray(self):
    return deepcopy(self._rays[0])

  def outer_rays(self):
    return deepcopy(self._rays[1::])

  def focal_length(self):
    r, alph = self.radius_angle()
    if alph == 0:
      return 0
    else:
       return - r/np.tan(alph)

  def length(self):
    return self.inner_ray().length

  def set_length(self, x):
    for ray in self._rays:
      ray.length = x


  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird
    ändert die Position aller __rays mit

    is called when the position of <self> is changed
    changes the position of all __rays with
    """
    super()._pos_changed(old_pos, new_pos)
    self._rearange_subobjects_pos(old_pos, new_pos, self._rays)


  def _axes_changed(self, old_axes, new_axes):
    """
    wird aufgerufen, wen das KooSys <_axes> von <self> verändert wird
    dreht die KooSys aller __rays mit

    dreht auÃŸerdem das eigene Koordiantensystem

    is called when the KooSys <_axes> is changed from <self>.
    rotates the KooSys of all __rays as well

    also rotates the own coordiante system
    """
    super()._axes_changed(old_axes, new_axes)
    self._rearange_subobjects_axes(old_axes, new_axes, self._rays)


  def draw_freecad(self):
    if self.draw_dict["model"] == "Gaussian":
      return model_Gaussian_beam(name=self.name, q_para=self.q_para,
                                 wavelength=self.wavelength,
                                 prop=self.get_all_rays()[0].length,
                                 geom_info=self.get_geom())
    elif self.draw_dict["model"] == "cone":
      radius, angle = self.radius_angle()
      # return model_beam(name=self.name, dia=2*radius, prop=self.length(),
           # f=self.focal_length(), geom_info=self.get_geom(), **self.draw_dict)
      # return model_beam(dia=2*radius, prop=self.length(), f=self.focal_length(),
      #                   geom_info=self.get_geom(), **self.draw_dict)
      return model_beam_new(radius=radius, length=self.length(),  angle=angle,
                            geom_info=self.get_geom(),**self.draw_dict)
      # return model_Gaussian_beam(name=self.name, dia=2*radius, prop=self.length(),
      #      f=self.focal_length(), geom_info=self.get_geom())
    else:
      part = initialize_composition_old(name="ray group")
      container = []
      for nn in range(self._ray_count):
        our=self._rays[nn]
        obj = our.draw_freecad()
        container.append(obj)
      add_to_composition(part, container)
      return part
```


In addition, the class Gaussian_Beam describes Gaussian beams and inherits from Ray. The constructor takes the same arguments: radius, angle, and wavelength. The q parameter is calculated from this, and all other characteristic values are derived.
The draw_freecad function returns a collection of merged conic sections that reproduce the shape of the caustic but take longer to compute in FreeCAD than the standard rays. This is the code:

```python
class Gaussian_Beam(Ray):
  def __init__(self, radius=10, angle=0.02, wavelength=1030E-6, name="NewGassian",  **kwargs):
    super().__init__(name=name, **kwargs)
    z0 = wavelength/(np.pi*np.tan(angle)*np.tan(angle))
    w0 = wavelength/(np.pi*np.tan(angle))
    if w0>radius:
      print("Woring: Wrong Radius!")
    z = z0*pow((radius*radius)/(w0*w0)-1,0.5)
    if angle<0:
      z = -z
    q_para = complex(z,z0)
    self.wavelength = wavelength
    self.q_para = q_para
    self._distribution = "Gaussian"
    self.draw_dict["model"] = "Gaussian"

  def set_length(self, length):
    # needed for consitency in next_beam function
    self.length = length

  def waist(self):
    return np.sqrt( self.wavelength / np.pi * np.imag(self.q_para) )

  def __repr__(self):
    # radius, angle = self.radius_angle()
    n = len(self.class_name())
    txt = 'Gaussian_Beam(q_para=' + repr(self.q_para)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def draw_freecad(self):
    if self.draw_dict["model"] == "Gaussian":
      return model_Gaussian_beam(name=self.name, q_para=self.q_para,
                                 wavelength=self.wavelength,prop=self.length,
                                 geom_info=self.get_geom())
    if self.draw_dict["model"] == "cone":
      # quicker method with nearly the same look in most cases
      radius = self.radius()
      focal_length = - radius / self.divergence()
      col = (244/255, 22/255, 112/255)
      return model_beam(dia=2*radius, prop=self.length, f=focal_length,
                        geom_info=self.get_geom(), color=col, **self.draw_dict)
    else:
      return -1

  def radius(self):
    z = np.real(self.q_para)
    zr = np.imag(self.q_para)
    return self.waist() * np.sqrt(1 + (z/zr)**2)

  def divergence(self):
    z = np.real(self.q_para)
    zr = np.imag(self.q_para)
    return np.sign(z) * self.waist() / zr

  def transform_to_cone_beam(self):
    cone = Beam(name=self.name, radius=self.radius(), angle=self.divergence())
    cone.set_geom(self.get_geom())
    cone.set_length(self.length)
    return cone

  def get_all_rays(self):
    ray = Ray()
    ray.set_geom(self.get_geom())
    ray.wavelength = self.wavelength
    ray.length = self.length
    return [ray]
```
All types of rays are shown in the tutorial 3_RaysAndBeams.

<img src="images/rays_and_beams.png" alt="some-nice-beams" title="" />

## Component

Before the actual class of optical elements (Opt_Element), which can access and change the beam parameters, is discussed, the superordinate class Component must be introduced. It inherits from Geom_Object and, in addition to the sizes aperture and thickness, which are important for drawing and calculation, introduces the mount, described further in the chapter below. Via _pos_changed and _axes_changed it is ensured that all shifts are also applied to the mount.
```python
from .geom_object import Geom_Object
from .constants import inch
from .mount import Unit_Mount, get_mount_by_aperture_and_element
from .. freecad_models import freecad_da

class Component(Geom_Object):
  """
  class for shaped components with mounts, posts and bases
  developes into Optical_Element and many non interactings
  """
  def __init__(self, name="Component", **kwargs):
    super().__init__(name, **kwargs)
    self.aperture = 1*inch # Aperture in mm for drawing, Mount and clipping (not yet implemented)
    self.thickness = 5 # Thickness in mm, importent for mount placing and drawing
    self.set_mount_to_default()

  def set_mount_to_default(self):
    self.Mount = get_mount_by_aperture_and_element(self.aperture,
                                                   self.class_name(),
                                                   self.thickness)
    self.Mount.set_geom(self.get_geom())


  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    self.draw_dict["thickness"] = self.thickness

  def draw_mount(self):
    # self.update_mount()
    return (self.Mount.draw())

  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.Mount])

  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.Mount])
```


## Opt_Element

The base class for all concrete optical elements, such as Lens and Mirror, inherits from Component. The method matrix() returns the ABCD matrix of the element; for more complex objects, this must be calculated; the default is the unit matrix. Furthermore, the next_ray(ray) method is defined, which calculates the ray that falls out. 3 different methods are offered as standard:
just_pass_throug: Creates a new ray behind the element with the same orientation as the incident ray.
- Reflection: Generates the ray reflected at the surface according to the vectorial reflection law (see Springer p.300???). It should be noted that the normal of most reflecting elements usually points in the direction of the incident ray rather than against it. For example, the default ray is in the x-direction, as is the default mirror (and all other elements, see Geom_Obj), whereby the ray is reflected by 180°. You could define the behaviour as a reflection on the back, but this is irrelevant for an infinitely thin object (length=0).
- Refraction: Refraction of the beam using the ABCD law extended to 3 dimensions. The incident beam vector is first divided into 3 components: One along the optical axis, equivalent to the component parallel to the normal of the element, and one along the line connecting the intersection point and the element centre (=element.pos), which describes the meridional component, and a last one perpendicular to the other two, which characterizes the sagittal component. The latter remains constant, while the radius and angle are calculated from the first two components and then transformed according to the matrix multiplication. The results are converted back into a 3-dimensional vector similarly and applied to the new ray.
```python
from .geom_object import Geom_Object, TOLERANCE
from .component import Component
from .ray import Ray
from .beam import Beam, Gaussian_Beam
from .constants import inch
import numpy as np
from copy import deepcopy
from .. freecad_models import freecad_da


class Opt_Element(Component):
  """
  Basisklasse aller "dünnen" optischen Elemente wie z.B. Linse
  "dünn" heiÃŸt, nur der Winkel (normal) vom Strahl wird geändert, nicht seine
  Höhe (pos)
  die Oberfläche wird als ebene im R3 angenommen
  erbt von Geom_Obj
  führt neben pos, normal auch Matrix für geometrische Optik ein
  neue Methoden:
    next_ray(ray)
    reflection(ray)
    refraction(ray)
    diffraction(ray) ?

  """
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._matrix = np.eye(2)
    self.length = 0 #Länge in mm, die meisten opt Elemente sind 2D, also 0

  def matrix(self):
    return np.array(self._matrix)

  def next_ray(self, ray):
    """
    erzeugt den durch das opt Elem veränderten Strahl und gibt ihn zurück
    Parameters
    ----------
    ray : Ray
      Eingangsstrahl
    Returns
    -------
    ray2 : Ray
      Ausgangsstrahl
    """
    return self.just_pass_through(ray)

  def just_pass_through(self, ray):
    ray2 = deepcopy(ray)
    ray2.pos = ray.intersect_with(self) #dadruch wird ray.length verändert(!)
    return ray2

  def reflection(self, ray):
    """
    erzeugt den nächsten Strahl aus <Ray> mit Hilfe des Reflexionsgesetzes
    (man beachte die umgedrehte <normal> im Gegensatz zur Konvention in z.B.
    Springer Handbook of Optics and Lasers S. 68)

    Parameters
    ----------
    ray : Ray()
      incident ray

    Returns
    -------
    reflected ray
    """
    ray2 = deepcopy(ray)
    ray2.pos = ray.intersect_with(self) #dadruch wird ray.length verändert(!)
    k = ray2.normal
    km = -self.normal
    scpr = np.sum(km*k)
    newk = k-2*scpr*km
    ray2.normal = newk
    # print("REFL", k, km, scpr, newk, ray2.normal)
    return ray2

  def refraction(self, ray):
    ray2 = deepcopy(ray)
    ray2.pos = ray.intersect_with(self) #dadruch wird ray.length verändert(!)
    norm = ray2.normal
    radial_vec = ray2.pos - self.pos
    radius = np.linalg.norm(radial_vec) #Radius im sinne der parax Optik
    ea = self.normal #Einheitsvec in Richtung der optischen Achse oA
    if np.sum(ea * norm) < 0:
      ea *= -1 #gibt sonst hässliche Ergebnisse, wenn die Linse falsch rum steht
    if radius > TOLERANCE:
      # kein Mittelpunktsstrahl
      er = radial_vec / radius #radialer Einheitsvektor (meridional)
      es = np.cross(er, ea) #Einheitsvektor in sagitaler Richtung
      es = es / np.linalg.norm(es) #eigentlich automatisch, aber man weiÃŸ ja nie
      cr = np.sum(er * norm)
      ca = np.sum(ea * norm)
      cs = np.sum(es * norm)
      alpha = np.arctan(cr/ca)
      vm = np.sqrt(cr**2 + ca**2) #length of the raz.normal projected in the meridional plane
      parax1 = np.array((radius, alpha)) #classic matrix optics
      rad2, alpha2 = np.matmul(self._matrix, parax1) #classic matrix optics
      pos2 = self.pos + er * rad2 #neue position
      norm2 = vm*np.cos(alpha2)*ea + vm*np.sin(alpha2)*er + cs*es # neue normale
      ray2.pos = pos2
      ray2.normal = norm2
      return ray2

    #else: Mittelpunktsstrahl
    ca = np.sum(ea * norm)
    em = norm - ca * ea #meridionaler Einheitsvektor
    m = np.linalg.norm(em)
    if m < TOLERANCE:
      # s = (0,0) -> (0,0) Mittelpunkstrahl ohne Winkel
      return ray2
    em *= 1/m
    alpha = np.arctan(m/ca)
    rad2 = self._matrix[0,1] * alpha #r2 = B*alpha
    alpha2 = self._matrix[1,1] * alpha #alpha2 = D*alpha
    pos2 = self.pos + rad2 * em
    norm2 = np.cos(alpha2)*ea + np.sin(alpha2)*em
    ray2.pos = pos2
    ray2.normal = norm2

    return ray2
```

The method next_beam calculates the next beam simply by iterating over the inner rays and applying the next_ray function. Next_gauss calculates the outgoing Gaussian beam from an incoming Gaussian beam using Kogelnik's ABCD matrix law (see any suitable source).

Theorie:
ABCD Gesetz von Gaußtrahlen:
Siehe Report He 1

<img src="images/ABDC_q.png" alt="StretcherStuff" title="" />


Where q1 is the 1-parameter of the incident beam and q2 is the parameter of the outgoing beam. See
J. P. Tach'e. Derivation of ABCD law for Laguerre-Gaussian beams.
Optical Society of America, 1987.
Reflektionsgesetz:

<img src="images/reflection_formular.png" alt="StretcherStuff" title="" />

Where a2 is the vector of the outgoing ray, a1 is the vector of the incoming ray and N is the normal of the mirror. See Prof. Dr. Frank Träger. Springer Handbook of Lasers and Optics.
Springer Dordrecht Heidelberg London New York, 2012. p.64 ff


```python
  def next_beam(self, beam):
    """
    erzeugt den durch das opt Elem veränderten Beam und gibt ihn zurück
    und zwar ultra lazy
    Parameters
    ----------
    beam : Beam()

    Returns
    -------
    next Beam()
    """
    if type(beam) == type(Gaussian_Beam()):
      return self.next_gauss(beam)
    newb = deepcopy(beam)
    newb.name = "next_" + beam.name
    rays = beam.get_all_rays(by_reference=True)
    newrays = []
    for ray in rays:
      nr = self.next_ray(ray)
      if not nr:
        return False #Für Elemente die nicht mit Strahlen interagieren wird -1 als beam zurück gegeben
      newrays.append(nr)
    newb.override_rays(newrays)
    return newb

  def next_gauss(self,gaussian):
      next_gaussian = deepcopy(gaussian)
      next_middle = self.next_ray(gaussian) #change the length of Gaussian
      next_gaussian.set_geom(next_middle.get_geom())
      [[A,B],[C,D]] = self._matrix
      q_parameter = deepcopy(gaussian.q_para)
      q_parameter += gaussian.length
      next_gaussian.q_para = (A*q_parameter+B)/(C*q_parameter+D)
      # print(next_gaussian.q_para)
      return next_gaussian
```


## Lens

With the definitions from Opt_Element, the class Lens can now be implemented fairly straightforwardly, which inherits from Opt_Element. The additional property f or focal_length in mm is introduced in the constructor. Using a getter and setter, the matrix is always adjusted when its value is changed. The calculation of the ray that falls out is carried out using the matrix itself and the refraction method from Opt_Element. The freecad_model model_lens is used for drawing. Like all freecad_models, it is located in the freecad_models package; at least, that seemed logical. The code follows:
```python
from ..freecad_models import model_lens, lens_mount
from .optical_element import Opt_Element


class Lens(Opt_Element):
  def __init__(self, f=100, name="NewLens", **kwargs):
    super().__init__(name=name, **kwargs)
    self.focal_length = f
    self.thickness = 3
    self.freecad_model = model_lens

  @property
  def focal_length(self):
    return self.__f
  @focal_length.setter
  def focal_length(self, x):
    self.__f = x
    if x == 0:
      self._matrix[1,0] = 0
    else:
      self._matrix[1,0] = -1/x

  def next_ray(self, ray):
    return self.refraction(ray)

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["Radius1"] = 300
    self.draw_dict["Radius2"] = 0

  def __repr__(self):
    n = len(self.class_name())
    txt = 'Lens(f=' + repr(self.focal_length)
    txt += ', ' + super().__repr__()[n+1::]
    return txt
```


## Mirror

The Mirror class as the mirror.py module naturally also inherits from the Opt_Element. While ray tracing uses the reflection function, most of the code is spent on the correct mirror alignment using its defining angles, phi and theta. The two angles can be specified in the constructor. Phi describes the rotation of the outgoing beam relative to the incoming beam in the xy plane. Example: Phi=180 describes a mirror with an angle of incidence = 0, phi = 90, a 45° mirror that rotates a beam from the x-direction into a beam in the y-direction, phi=-90 correspondingly in the -90° direction. Analogously, theta denotes the proportion of the change in direction in the z-direction, i.e. out of the xy-plane. For example, a beam in the x-direction is rotated in the z-direction by a phi=0, theta=90° mirror.
When the mirror is created, it is always aligned to rotate the standard beam from the x-direction by precisely the specified amount. An override of the set_geom routine allows the mirror to be aligned so that a beam with any geom would be transformed according to the angle. This means that a mirror after set_geom(Geom2) will, in most cases, not (!) have the orientation of Geom2.
It is also possible to realign the mirror using its normal; the angles phi and theta no longer have any meaning.
Another possible way to define the direction of the mirror is via the set_normal_with_2_points function. Here is the code:
```python
from .geom_object import TOLERANCE, NORM0
from .ray import Ray
from .optical_element import Opt_Element
from .mount import Stripe_Mirror_Mount, Rooftop_Mirror_Mount
from ..freecad_models import model_mirror, model_stripe_mirror, model_rooftop_mirror
import numpy as np
from copy import deepcopy

class Mirror(Opt_Element):
  """
  Spiegelklasse, erbit von <Opt_Element>, nimmt einen ray und transformiert
  ihn entsprechend des Reflexionsgesetzes
  Anwendung wie folgt:

  m = Mirror(phi=90)
  r = Ray()
  m.set_geom(r.get_geom())
  nr = m.next_ray(r)

  dreht <r> in der xy-Ebene um den Winkel <phi> â‚¬[-180,180] und dreht um
  <theta> â‚¬ [-90,90] aus der xy-Ebene heraus, wenn man die normale voher mit
  set_geom() einstellt
  """
  def __init__(self, phi=180, theta=0, **kwargs):
    super().__init__(**kwargs)
    self.__incident_normal = np.array(NORM0) # default von Strahl von x
    self.__theta = theta
    self.__phi = phi
    self.update_normal()
    self.freecad_model = model_mirror

  def update_normal(self):
    """
    aktualisiert die Normale des Mirrors entsprechend der __incident_normal,
    phi und theta
    """
    phi = self.__phi/180*np.pi
    theta = self.__theta/180*np.pi
    if phi == 0 and theta == 0:
      print("Warnung, Spiegel unbestimmt und sinnlos, beide Winkel 0")
      self.normal = (0,1,0)
      return -1

    rho = self.__incident_normal[0:2]
    rho_abs = np.linalg.norm(rho)
    z = self.__incident_normal[2]
    rho2_abs = rho_abs * np.cos(theta) - z * np.sin(theta)
    z2 = rho_abs * np.sin(theta) + z * np.cos(theta)
    if rho_abs == 0:
      x = rho2_abs
      y = 0
    else:
      x = rho[0] * rho2_abs/rho_abs
      y = rho[1] * rho2_abs/rho_abs
    x2 = x * np.cos(phi) - y * np.sin(phi)
    y2 = x * np.sin(phi) + y * np.cos(phi)
    self.normal = self.__incident_normal - (x2, y2, z2)

  def set_geom(self, geom):
    """
    setzt <pos> und __incident_normal auf <geom> und akturalisiert dann die
    eigene <normal> entsprechend <phi> und <theta>

    Parameters
    ----------
    geom : 2-dim Tupel aus 3-D float arrays
      (pos, normal)
    """
    # print("GEOM-MIRROR:", geom)
    self.pos = geom[0]
    axes = geom[1]
    self.__incident_normal = axes[:,0]
    self.update_normal()

  @property
  def phi(self):
    """
    beschreibt den Winkel <phi> um den der Mirror einen Strahl in
    <__incident_normal> Richtung in der xy-Ebene durch Reflexion weiter dreht
    (mathematisch positive Drehrichtung)
    stellt über Setter sicher, dass die normale entsprechend aktualisiert wird
    """
    return self.__phi
  @phi.setter
  def phi(self, x):

    self.__phi = x
    self.update_normal()

  @property
  def theta(self):
    """
    beschreibt den Winkel <theta> um den der Mirror einen Strahl in
    <__incident_normal> Richtung aus der xy-Ebene durch Reflexion weiter dreht
    (mathematisch positive Drehrichtung)
    stellt über Setter sicher, dass die normale entsprechend aktualisiert wird
    """
    return self.__theta
  @theta.setter
  def theta(self, x):
    self.__theta = x
    self.update_normal()

  def next_ray(self, ray):
    return self.reflection(ray)

  def set_incident_normal(self, vec):
    """
    setzt neue <__incident_normal> und berechnet daraus mit <phi> und <theta>
    die neue <normal>
    """
    vec = vec / np.linalg.norm(vec)
    self.__incident_normal = np.array((1.0,1.0,1.0)) * vec
    self.update_normal()

  def recompute_angles(self):
    """
    berechnet die Winkel neu aus <__incident_normal> und <normal>
    """
    vec1 = self.__incident_normal
    dummy = Ray()
    dummy.normal=vec1
    #nur um next_ray und reflectino zu nutzen
    reflected_dummy = self.next_ray(dummy)
    vec2 = reflected_dummy.normal
    xy1 = vec1[0:2]
    xy2 = vec2[0:2]
    teiler = np.linalg.norm(xy1) * np.linalg.norm(xy2)
    if teiler < TOLERANCE:
      #wenn die Komponenten verschwinden, kann kein Winkel bestimmt werden
      phi = 0
    else:
      phi0 = np.arcsin( (xy1[0]*xy2[1]-xy1[1]*xy2[0]) /teiler) * 180/np.pi
      scalar = np.sum(xy1*xy2)
      if scalar >= 0:
        phi = phi0
      else:
        phi = -180 - phi0 if (phi0 < 0) else 180 - phi0
    v3 = np.array((np.linalg.norm(xy1), vec1[2]))
    v4 = np.array((np.linalg.norm(xy2), vec2[2]))
    teiler = np.linalg.norm(v3) * np.linalg.norm(v4)
    if teiler < TOLERANCE:
      #wenn die Komponenten verschwinden, kann kein Winkel bestimmt werden
      theta = 0
    else:
      theta = np.arcsin( (v3[0]*v4[1]-v3[1]*v4[0]) /teiler) * 180/np.pi
    return phi, theta

  def set_normal_with_2_points(self, p0, p1):
    """
    setzt die Normale neu, sodass der mirror einen Strahl reflektiert, der von
    p0 kommt, den Spiegel in self.pos trifft und dann zu p1 reflektiert wird
    berechnet anschlieÃŸend die Winkel neu
    """
    inc = self.pos - p0
    refl = p1 - self.pos
    inc *= 1/np.linalg.norm(inc)
    refl *= 1/np.linalg.norm(refl)
    # print("nextnormal", (inc - refl)/np.linalg.norm(inc - refl))
    self.normal = inc - refl
    self.__phi, self.__theta =  self.recompute_angles()

  def __repr__(self):
    n = len(self.class_name())
    txt = self.class_name() + '(phi=' + repr(self.phi)
    txt += ", theta=" + repr(self.theta)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["dia"]=self.aperture
    self.draw_dict["Radius"] = 0
```


## Curved_Mirror
The class for spherically curved mirrors inherits from Mirror. A radius can be specified in the constructor, which always changes the matrix, similar to the focal_length of the lens. The ray tracing method could run via the successive execution of refraction and reflection, but it has been shown that the vectorial calculation by means of intersection calculation with the sphere and subsequent formation of the normal and reflection is simpler and more exact, which is why no ABCD matrix needs to be used. See
See Prof. Dr. Frank Träger. Springer Handbook of Lasers and Optics.
Springer Dordrecht Heidelberg London New York, 2012. p.66

```python
class Curved_Mirror(Mirror):
  def __init__(self, radius=200, **kwargs):
    super().__init__(**kwargs)
    self.radius = radius

  @property
  def radius(self):
    return self.__radius
  @radius.setter
  def radius(self, x):
    self.__radius = x
    if x == 0:
      self._matrix[1,0] = 0
    else:
      self._matrix[1,0] = -2/x

  def focal_length(self):
    return self.radius/2

  def next_ray(self, ray):
    # r1 = self.refraction(ray)
    # r2 = self.reflection(r1)
    r2 = self.next_ray_trace(ray)
    return r2

  def __repr__(self):
    n = len(self.class_name())
    txt = self.class_name() + '(radius=' + repr(self.radius)
    txt += ', ' + super().__repr__()[n+1::]
    return txt

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["Radius"] = self.radius
    self.draw_dict["dia"]=self.aperture
    # self.draw_dict["Radius1"] = self.radius

  def next_ray_trace(self, ray):
    """
    erzeugt den nächsten Ray auf Basis der analytischen Berechung von Schnitt-
    punkt von Sphere mit ray und dem vektoriellen Reflexionsgesetz
    siehe S Hb o LaO S 66 f

    Parameters
    ----------
    ray : TYPE Ray
      input ray

    Returns
    -------
    ray2 : TYPE Ray
      output ray

    """
    ray2 = deepcopy(ray)
    ray2.name = "next_" + ray.name

    center = self.pos - self.radius * self.normal
    p0 = ray.intersect_with_sphere(center, self.radius) #Auftreffpunkt p0
    surface_norm = p0 - center #Normale auf Spiegeloberfläche in p0
    surface_norm *= 1/np.linalg.norm(surface_norm) #normieren
    ray2.normal = ray.normal - 2*np.sum(ray.normal*surface_norm)*surface_norm
    ray2.pos = p0
    return ray2
```

The functionality is also shown in the tutorial 4_LensesAndMirrors.

<img src="images/opt_elements.png" alt="lenses-and-mirrors" title="" />


## Grating

The Grating class is another child object of Opt_Element and simulates optical reflection gratings. The grating constant grat_const and the diffraction order are provided as additional values in the constructor. The default values are 0.005 mm and first order. The next_ray method calculates the beam diffracted at the grating in the corresponding order (e.g. 1 or -1). As an optional argument, any order can be given as an integer, temporarily overwriting the grid order. The theory and equation can be found on Thorlabs, Springer ? SOURCE.
In the constructor, the geometric dimensions important for drawing and mount positioning are also defined as width, height and thickness. As mount the dedicated created and customised Grating_Mount is imported, that freecad_model is model_grating. Here is the code:
```python
import numpy as np
from copy import deepcopy
from .optical_element import Opt_Element
from .ray import Ray
from ..freecad_models import model_grating
from .mount import Grating_Mount


class Grating(Opt_Element):
  """
  Klasse für Gitter
  """
  def __init__(self, grat_const=0.005, order=1, **kwargs):
    self.height = 60
    self.thickness = 8
    super().__init__(**kwargs)
    self.grating_constant = grat_const
    self.width = 50
    self.diffraction_order = order
    self.update_draw_dict()
    self.freecad_model = model_grating
    self.set_mount_to_default()

  def next_ray(self, ray, order=None):
    """
    Beugung entsprechend des Gittergesetzes g(sinA + sinB) = m*lam
    m = order
    """
    if order == None:
      order = self.diffraction_order
    norm, gratAx, sagit = self.get_coordinate_system() # Normale, Gitterachse, Sagitalvector
    norm *= -1 #selbe Konvention wie beim Spiegel, 1,0,0 heiÃŸt Reflektion von 1,0,0
    gratAx *= -1 #selbe Konvention wie beim Spiegel, 1,0,0 heiÃŸt Reflektion von 1,0,0
    r1 = ray.normal #einfallender Strahl
    pos = ray.intersect_with(self)
    sagital_component = np.sum(r1 * sagit)
    sinA = np.sum( sagit * np.cross(r1, norm) )
    sinB = order * ray.wavelength/ self.grating_constant - sinA
    ray2 = deepcopy(ray)
    ray2.name = "next_" + ray.name
    ray2.pos = pos
    ray2.normal = (np.sqrt(1-sinB**2) * norm + sinB * gratAx) * np.sqrt(1-sagital_component**2) + sagital_component * sagit
    k_prop = np.cross(norm,np.cross(ray.normal*2*np.pi/ray.wavelength,norm))
    k_p_out = k_prop+order*2*np.pi/self.grating_constant*gratAx
    k_r = k_p_out + abs(np.sqrt((2*np.pi/ray.wavelength)**2-np.linalg.norm(k_p_out)**2))*norm
    n_r = k_r/np.linalg.norm(k_r)
    ray2.normal = n_r
    return ray2

  def update_draw_dict(self):
    super().update_draw_dict()
    self.draw_dict["dimensions"] = (self.width, self.height, self.thickness)

  def set_mount_to_default(self):
    smm = Grating_Mount(height=self.height,thickness=self.thickness)
    smm.set_geom(self.get_geom())
    self.Mount = smm
```

Theory:
<img src="images/grating_theory.png" alt="GratingTheory" title="" />

In the above equation and figure, Tg is a unit vector perpendicular to the grating lines, ni is the vector of the incident beam, nr is the vector of the reflected beam, and ns is the normal vector of the grating surface. The wave vectors k are marked with analogue indices. The grating vector G results from the inverse grating constant d (the distance between two lines). The unit vector Tp points in the direction of the grating lines. The incident wave vector ki is divided into parallel and normal components (kp, kn). The parallel component is then added to the m-fold grating vector, where m is an integer indicating the diffraction order. The incident wave vector results from the new parallel element, and a factor reduces the normal component to equal the magnitude of the incident and incident wave vectors. Source: https://doc.comsol.com/5.5/doc/com.comsol.help.roptics/roptics_ug_optics.6.58.html



## Composition

This class serves as a container class for all-optical setups. Its purpose is the permanent calculation of the optical axis, the correct insertion, naming and positioning of the optical elements, the calculation of the overall matrix of the optical system and the representation of all components with summarising functions.
When moving and rotating in space, the sub-elements are transformed using functions such as _pos_changed and _rearang_subobjects.
The order in which the beam and change hit the elements is defined with the _sequence index list. Double indices make it possible to calculate multipass systems.
Propagate shifts the next reference point (last_geom) on the optical axis. Add_on_axis is used to set an optical element to this point, and add_fixed_element to insert an element without adjusting its position and orientation. Instead of elements, you can insert smaller compositions using add_subcomposition according to the same principle.
The lightsource defines the initial beam and is usually a beam (i.e. a collection of rays). It can be inserted and changed via set_lightsource. The inner_ray of the beam represents the start of the optical axis, which is why the correct wavelength should be taken into account for the lightsource in setups with grids.
The draw() function combines all drawing functions and thus draws all elements, their mounts and the beams. The code can be seen below:
```python
from .ray import Ray
from .beam import Beam
from .geom_object import Geom_Object
from ..freecad_models import warning, freecad_da, initialize_composition, add_to_composition
import numpy as np
from copy import deepcopy


class Composition(Geom_Object):
  """
  Komposition von Elementen, besitzt optical Axis die mit jedem Element und
  jedem .propagate erweitert wird und sequence, die die Reihenfolge der
  Elemente angibt (meist trivial auÃŸer bei multipass)
  """
  def __init__(self, name="NewComposition", **kwargs):
    super().__init__(name=name,**kwargs)
    oA = Ray(name=self.name+"__oA_0")
    oA.pos = self.pos
    oA.normal = self.normal
    oA.length = 0
    self._optical_axis = [oA]
    self._elements = []
    self._sequence = []
    self._last_prop = 0 #für den Fall, dass eine letzte Propagation nach einem Element noch erwünscht ist

    self._lightsource = Beam(radius=1, angle=0)
    self._lightsource.set_geom(self.get_geom())
    self._lightsource.name = self.name + "_Lighsource"
    self._beams = [self._lightsource]
    self._catalogue = {}
    self._drawing_part = -1
    self.non_opticals = []


  def propagate(self, x):
    """
    propagiert das System um x mm vorwärts, updated damit opt_axis,
    self._matrix, ersetzt früheres add(Propagation)

    Parameters
    ----------
    x : float
      Länge um die propagiert wird
    """
    end_of_axis = self._optical_axis[-1]
    end_of_axis.length += x
    self._last_prop = end_of_axis.length #endet mit Propagation

  def last_geom(self):
    end_of_axis = self._optical_axis[-1]
    return (end_of_axis.endpoint(), end_of_axis.get_axes())

  def __add_raw(self, item):
    # #checken ob Elm schon mal eingefügt
    self.__no_double_integration_check(item)
    # # Namen ändern, geom setzen, hinzufügen
    item.name = self.new_catalogue_entry(item)
    self._elements.append(item)
    self._sequence.append(len(self._elements)-1) #neues <item> am Ende der seq
    self._last_prop = 0 #endet mit Element

  def add_on_axis(self, item):
    """
    fügt <item> an der Stelle _last_geom (und damit) auf der optAx ein,
    checkt ob nicht ausversehen doppelt eingefügt, ändert namen, geom

    updatet _matrix, opt_axis
    """
    item.set_geom(self.last_geom())
    if hasattr(item, "next_ray"):
      self.__add_raw(item)
      newoA = item.next_ray(self._optical_axis[-1])
      newoA.length = 0
      self._optical_axis.append(newoA)
    # ignore non-optical Elm, e.g. Geom_Obj, cosmetics
    else:
      self.non_opticals.append(item)

  def add_fixed_elm(self, item):
    """
    fügt <item> genau an der Stelle <item.get_geom()> ein

    updated entsprechend add_on_axis
    """
    if hasattr(item, "next_ray"):
      self.__add_raw(item)
    else:
      self.non_opticals.append(item)

  def add_supcomposition_on_axis(self, subcomp):
    subcomp.set_geom(self.last_geom())
    self.add_supcomposition_fixed(subcomp)

  def add_supcomposition_fixed(self, subcomp):
    for element in subcomp._elements:
      self.add_fixed_elm(element)
    for nonopt in subcomp.non_opticals:
      self.add_fixed_elm(nonopt)

  def redefine_optical_axis(self, ray):
    # zB wenn die wavelength angepasst werden muss
    # print("sollte nur gemacht werden, wenn absolut noch kein Element eingefügt wurde")
    # print("should only be done if absolutely no element has been inserted yet")
    self.set_geom(ray.get_geom())
    oA = deepcopy(ray)
    oA.name = self.name +"__oA_0"
    self._optical_axis = [oA]
    self.recompute_optical_axis()

  def recompute_optical_axis(self):
    self._optical_axis = [self._optical_axis[0]]
    counter = 0

    for ind in self._sequence:
      elm = self._elements[ind]
      # print("-----", elm)
      newoA = elm.next_ray(self._optical_axis[-1])
      counter += 1
      newoA.name = self.name + "__oA_" + str(counter)
      self._optical_axis.append(newoA)
    self._optical_axis[-1].length = self._last_prop


  def matrix(self):
    """
    computes the optical matrix of the system
    each iteration consists of a propagation given by the length of the nth
    ray of the optical_axis followed by the matrix multiplication with the
    seq[n] element

    Returns the ABCD-matrix
    """
    self._matrix = np.eye(2)
    self.recompute_optical_axis()
    counter = -1
    for ind in self._sequence:
      counter += 1
      B = self._optical_axis[counter].length
      M = self._elements[ind]._matrix
      self._matrix = np.matmul(np.array([[1,B], [0,1]]), self._matrix )
      self._matrix = np.matmul(M, self._matrix )
    self._matrix = np.matmul(np.array([[1,self._last_prop], [0,1]]), self._matrix ) #last propagation

    return np.array(self._matrix)

  def get_sequence(self):
    return list(self._sequence)

  def set_sequence(self, seq):
    self._sequence = list(seq)

  def compute_beams(self, external_source=None):
    beamcount = 0
    if external_source:
      beamlist = [external_source]
    else:
      beamlist = [self._lightsource]
    for n in self._sequence:
      elm = self._elements[n]
      beam = elm.next_beam(beamlist[-1])
      if beam:
        # manche Elemente wie Prop geben keine validen beams zurück
        beamcount += 1
        beam.name = self.name + "_beam_" + str(beamcount)
        beamlist.append(beam)
    beamlist[-1].set_length(self._last_prop)
    if not external_source:
      self._beams = beamlist
    return beamlist


  def draw_elements(self):
    self.__init_parts()
    container = []
    for elm in self._elements:
      obj = elm.draw()
      container.append(obj)
    for elm in self.non_opticals:
      obj = elm.draw()
      container.append(obj)
    return self.__container_to_part(self._elements_part, container)

  def draw_beams(self):
    self.__init_parts()
    self.compute_beams()
    container = []
    for beam in self._beams:
      obj = beam.draw()
      container.append(obj)
    return self.__container_to_part(self._beams_part, container)

  def draw_mounts(self):
    self.__init_parts()
    container = []
    for elm in self._elements:
      obj = elm.draw_mount()
      container.append(obj)
    for elm in self.non_opticals:
      obj = elm.draw_mount()
      container.append(obj)
    return self.__container_to_part(self._mounts_part, container)

  def draw(self):
    self.draw_elements()
    self.draw_beams()
    self.draw_mounts()

  def __container_to_part(self, part, container):
    if freecad_da:
      part = add_to_composition(part, container)
    else:
      for x in container:
        part.append(x)
    return part

  def __init_parts(self):
    if self._drawing_part == -1:
      if freecad_da:
        d,e,m,b = initialize_composition(self.name)
        self._drawing_part = d
        self._elements_part = e
        self._mounts_part = m
        self._beams_part = b
      else:
        self._elements_part = []
        self._mounts_part = []
        self._beams_part = []
        self._drawing_part = [self._elements_part, self._mounts_part, self._beams_part]


  def set_light_source(self, ls):
    """
    setzt neue Lightsource (meistens ein Beam) für die Composition und passt
    deren Geom und Namen an
    danach werden _beams[] und raygroups[] neu initialisiert
    """
    self._lightsource = ls
    ls.set_geom(self.get_geom())
    ls.name = self.name + "_Lightsource"
    self._beams = [self._lightsource]
    group_ls = self._lightsource.get_all_rays()
    counter = 0
    for ray in group_ls:
      ray.name = self._lightsource.name + "_" + str(counter)
      counter += 1

  def new_catalogue_entry(self, item):
    #gibt jedem neuen Element einen Namen entsprechend seiner Klasse
    key = item.class_name()
    if key in self._catalogue:
         anz, names = self._catalogue[key]
         anz += 1
         itname = next_name(names[-1])
         names.append(itname)
    else:
         itname = self.name + "_" + item.class_name() + "_01"
         anz = 1
    self._catalogue[key] = [anz, [itname]]
    return itname

  def __no_double_integration_check(self, item):
    #checken ob Elm schon mal eingefügt
    if item in self._elements:
      warning("Das Element -" + str(item) + "- wurde bereits in <" +
            self.name + "> eingefügt.")


  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird
    ändert die Position aller __rays mit
    """
    super()._pos_changed(old_pos, new_pos)
    self._rearange_subobjects_pos(old_pos, new_pos, self._elements)
    self._rearange_subobjects_pos(old_pos, new_pos, [self._lightsource]) #sonst wird ls doppelt geshifted
    self._rearange_subobjects_pos(old_pos, new_pos, self._beams[1::])
    self._rearange_subobjects_pos(old_pos, new_pos, self._optical_axis)
    self._rearange_subobjects_pos(old_pos, new_pos, self.non_opticals)

  def _axes_changed(self, old_axes, new_axes):
    """
    wird aufgerufen, wen die axese von <self> verändert wird
    dreht die axese aller __rays mit

    dreht auÃŸerdem das eigene Koordiantensystem
    """
    super()._axes_changed(old_axes, new_axes)
    self._rearange_subobjects_axes(old_axes, new_axes, [self._lightsource]) #sonst wird ls doppelt geshifted
    self._rearange_subobjects_axes(old_axes, new_axes, self._elements)
    self._rearange_subobjects_axes(old_axes, new_axes, self._beams[1::])
    self._rearange_subobjects_axes(old_axes, new_axes, self._optical_axis)
    self._rearange_subobjects_axes(old_axes, new_axes, self.non_opticals)
```


Two good examples of dealing with compositions can be found in He's work as a telescope and in modules under WhiteCell or Typ2Amplifier. LINKS to come ???
Another excellent example is the tutorial 5_Composition.

<img src="images/composition.png" alt="Alt-Text" title="" />

The intended workflow of LaserCAD is to create a composition for each model of the planned structure and then insert the desired components into this with add_on_axis.


## LinearResonator

The LinearResonator class inherits from Composition and represents the class for laser resonators and regenerative amplifiers. Elements and propagations are inserted in the same way as in Composition. Once all components have been inserted, compute_eigenmode can be used to calculate the eigenmode as a Gaussian beam from the system's optical matrix. The wavelength of the resonator is used for this, among other things.
The two functions, add_output_coupler and set_output_coupler_index, can define the output coupler, i.e. the element at which the laser beam can leave the resonator. For regenerative amplifiers, an input coupler can be defined analogously via set_input_coupler_index, to which the genome of the group is then attached. Here again is some code:
```python
from .composition import Composition
from .mirror import Mirror
from .beam import Gaussian_Beam
import numpy as np

class LinearResonator(Composition):
  """
  class for laser resonators
  inherits from composition
  geometry_type: linear / ring(?)
  this alters the sequence for eigenmode() and compute_beams()
  add_outputcoupler / set_outputcoupler: sets  the OC (type=Mirror)
  """
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._output_coupler_index = 0
    self._input_coupler_index = 0
    self.wavelength = 1030e-6 #Yb in mm
    self.draw_dict["beam_model"] = "Gaussian"

  def add_output_coupler(self, item):
    if type(item) == type(Mirror()):
      self.add_on_axis(item)
      self._out_putcoupler_index = len(self._elements)-1
    else:
      print("Outputcoupler must be a mirror")
      return -1

  def set_output_coupler_index(self, index):
    if type(self._elements[index]) == type(Mirror()):
      self._output_coupler_index = index
    else:
      print("Outputcoupler must be a mirror")
      return -1

  def set_input_coupler_index(self, index, forward=True):
    """
    sets the index for the input coupler if the resonator is used as an regen-
    erative amplifier.
    (Should best be used after all elements have been inserted)
    The optical Element[index] becomes the input coupler meaning that the next
    beams geom will be GEOM0 if forward is true. If not, than the beam before
    will be the input beam with inverted geom.
    All other elements will be turned accordingly and afterwards the geom of
    the whole resonator is reseted to GEOM0


    Parameters
    ----------
    index : integer in the range [0, len(self._elments)-1]
      DESCRIPTION.
    forward : bool, optional
      DESCRIPTION. The default is True.

    Returns
    -------
    None.

    """
    self._input_coupler_index = index
    self.compute_beams()
    if forward:
      direction = self._beams[index].get_axes()
    else:
      helper = Gaussian_Beam()
      helper.normal = - self._beams[index-1].normal
      direction = helper.get_axes()
    rot_mat = np.linalg.inv(direction)
    self.set_axes(rot_mat)
    old_pos = self._elements[index].pos
    self.pos += -old_pos
    # reset to GEOM0
    self._pos = np.zeros(3)
    self._axes = np.eye(3)

  def output_beam(self):
    self.compute_beams()
    return self._beams[self._output_coupler_index-1]


  def set_wavelength(self, wavelength):
    """
    sets the own wavelength and thus the one of the lightsource and eigenmode
    PARAMETER: wavelength in mm
    """
    self.wavelength = wavelength
    self._lightsource.wavelength = wavelength

  def compute_eigenmode(self, start_index=0):
    """
    computes the gaussian TEM00 eigenmode from the matrix law

    Returns
    -------
    q : TYPE complex number
      the q parameter

    """
    #claculate the matrix with the correct sequence
    noe = len(self._elements)
    seq = [x for x in range(noe)]
    seq.extend([x for x in range(noe-2, 0, -1)])
    prop = np.linalg.norm(self._elements[0].pos-self._elements[1].pos)
    self._last_prop = prop
    self.set_sequence(seq)
    matrix = self.matrix()
    A = matrix[0,0]
    B = matrix[0,1]
    C = matrix[1,0]
    D = matrix[1,1]
    z = (A-D)/(2*C)
    E = -B/C - z**2
    if E < 0:
      print("Resonator is unstable")
      return -1
    ### set Lightsource accordingly
    z0 = np.sqrt(E)
    q_para = (z +1j*z0)
    gb00 = Gaussian_Beam(wavelength=self.wavelength) #der -1 strahl
    # gb00 = Beam(wavelength=self.wavelength, distribution="Gaussian") #der -1 strahl
    gb00.q_para = q_para
    gb00.set_geom(self._elements[0].get_geom())
    lsgb = self._elements[0].next_beam(gb00)
    self._lightsource = lsgb
    # set sequence for compute beams
    # self.set_sequence([x for x in range(1, noe)])
    prop = np.linalg.norm(self._elements[-1].pos-self._elements[-2].pos)
    self._last_prop = prop
    return q_para

  def compute_beams(self, external_source=None):
    self.compute_eigenmode()
    self.set_sequence([x for x in range(1, len(self._elements)-1)])
    super().compute_beams(external_source)
    for beam in self._beams:
      beam.draw_dict["model"] = self.draw_dict["beam_model"]


  def transform_gauss_to_cone_beams(self):
    self.compute_beams()
    cones = []
    for gb in self._beams:
      cones.append( gb.transform_to_cone_beam() )
    return cones
```

For an application example, please refer to the tutorial 6_LinearResonator.

<img src="images/resonator.png" alt="Alt-Text" title="" />



## MOUNTS

One of the great strengths of LaserCAD is the automatic insertion, adjustment and positioning of optomechanics in the structure. The algorithms for this can be found in the mount.py module. The idea is as follows:

### Unit_Mount

The smallest unit is the Unit_Mount. This inherits from Geom_Object and has two essential properties: the model (e.g. "POLRAIS-K1", which is equivalent to the file path of an STL file (standard 3D data format, also called stereolithography) and gives the shape in FreeCAD, and a so-called docking_obj, which is also a Geom_Object and specifies the position in space relative to the Unit_Mount's own Geom at which the docking point of the optomechanics is located (e.g. the M4 screw hole in a standard 1-inch mirror mount). Accordingly, a Unit_Mount is abstracted as an object that relates two points in space. The docking_obj is adapted similarly to all other subobjects using the _rearrange_subobjects routines.
In the constructor, all unit_mounts can be predefined using the keyword argument model from a list of standard mounts. The default is "dont_draw", which creates a unit_mount without an STL file, which is therefore not drawn (or automatically skipped in the draw routines) and whose docking_obj is identical to its geom.  In most cases, however, the function get_mount_by_aperture_and_element assigns a different mount to each element derived from the Component during initialisation. Specifically, a Composed_Mount is created at this point, described below, but essentially consists of a list of Unit_Mounts. If a corresponding model string located in one of the three lists MIRROR_LIST, LENS_LIST, SPECIAL_LIST is passed as an argument to the constructor of Unit_Mount, this automatically searches for the properties of the mount from a CSV file via the set_by_table function, which is located in the freecad_models/mount_meshes/mirror folder, for example. This folder also contains the aligned STL files. Aligned means that the model (also known as mesh) has been aligned and saved in a program (e.g. FreeCAD) in such a way that it can hold a corresponding element, which is located at the position (0,0,0) with normal (1,0,0). The values name, aperture, docking position, docking normal and colour of the unit_mount are then read from the CSV. The first line from mirrormounts.csv is shown here as an example:


If the argument model passed in the constructor matches one of the names from any of the CSV files, the listed parameters are transferred to the Unit_Mount.
In addition to initialisation, the Unit_Mount also has a few other functions to simplify the application:
The property is_horizontal = True can (and is also set by default) to enable the mount to be aligned vertically, i.e. the z-axis of its own _axes is always (0,0,1), and the normal can only move in the xy-plane. Since the vast majority of mirrors in optical setups are almost always aligned more or less in the same way and usually do not deviate more than 10° from the xy plane, the corresponding mounts are approximated as vertical for simplicity. Ultimately, in most cases, the task of an optomechanical system is to draw a normal of a mirror or similar, aligned a priori anywhere in space, piece by piece parallel to the coordinate axes, be it a mirror mount, 45° adapter, RM1G 1" construction cube or a construction of half-inch posts with SWC/M Rotating Clamp. They all try to be perpendicular or parallel to the table plane step by step. If is_horizontal is set to True, the set_axes function of the Unit_Mount is overwritten. Otherwise, it uses the default of Geom_Obj. The reverse and flip functions can be helpful to reposition mirror mounts (THERE SHOULD BE ANOTHER TUTORIAL...)

Here is some code again:
```python
from ..freecad_models.utils import thisfolder,load_STL,rotate,translate
from ..freecad_models.freecad_model_composition import initialize_composition_old,add_to_composition
from ..freecad_models.freecad_model_mounts import mirror_mount,DEFAULT_MOUNT_COLOR,DEFAULT_MAX_ANGULAR_OFFSET,model_Post_Marker
from ..freecad_models.freecad_model_grating import grating_mount
from .geom_object import Geom_Object, rotation_matrix
from .post import Post_and_holder
from ..freecad_models.freecad_model_mounts import draw_post,draw_post_holder,draw_post_base,draw_1inch_post,draw_large_post,model_mirror_holder

DEFALUT_POST_COLOR = (0.8,0.8,0.8)
DEFALUT_HOLDER_COLOR = (0.2,0.2,0.2)
POST_LIST = ["1inch_post","0.5inch_post","big_post"]

# from copy import deepcopy
import csv
import os
import numpy as np
import math


DEFALUT_CAV_PATH = thisfolder
DEFALUT_MIRROR_PATH = thisfolder + "mount_meshes/mirror"
DEFALUT_LENS_PATH = thisfolder + "mount_meshes/lens"
DEFALUT_SPEIAL_MOUNT_PATH = thisfolder + "mount_meshes/special_mount"

MIRROR_LIST1 = os.listdir(DEFALUT_MIRROR_PATH)
MIRROR_LIST = []
for i in MIRROR_LIST1:
  a,b,c = str.partition(i, ".")
  if "stl" in c:
    MIRROR_LIST.append(a)

LENS_LIST1 = os.listdir(DEFALUT_LENS_PATH)
LENS_LIST = []
for i in LENS_LIST1:
  a,b,c = str.partition(i, ".")
  if "stl" in c:
    LENS_LIST.append(a)

SPECIAL_LIST1 = os.listdir(DEFALUT_SPEIAL_MOUNT_PATH)
SPECIAL_LIST = []
for i in SPECIAL_LIST1:
  a,b,c = str.partition(i, ".")
  if "stl" in c:
    SPECIAL_LIST.append(a)
del a,b,c,i,SPECIAL_LIST1,LENS_LIST1,MIRROR_LIST1


def get_mount_by_aperture_and_element(aperture, elm_type, elm_thickness):
  if elm_type == "Lens":
    if aperture<= 25.4/2:
      model = "MLH05_M"
    elif aperture <= 25.4:
      model = "LMR1_M"
    elif aperture <= 25.4*1.5:
      model = "LMR1.5_M"
    elif aperture <=25.4*2:
      model = "LMR2_M"
    post = "0.5inch_post"
  elif elm_type == "Mirror" or elm_type == "Curved_Mirror":
    post = "1inch_post"
    if aperture<= 25.4/2:
      model = "POLARIS-K05"
    elif aperture <= 25.4:
      model = "POLARIS-K1"
    elif aperture <= 25.4*1.5:
      model = "POLARIS-K15S4"
    elif aperture <=25.4*2:
      model = "POLARIS-K2"
    elif aperture <=25.4*3:
      model = "POLARIS-K3S5"
    elif aperture <=25.4*4:
      model = "KS4"
    else:
      model = "6inch_mirror_mount"
      post = "big_post"
  else:
    return Unit_Mount()

  Output_mount = Composed_Mount(unit_model_list=[model,post])
  Output_mount.mount_list[0].element_thickness = elm_thickness
  Output_mount.mount_list[0].aperture = aperture

  if aperture>25.4*4:
    first = Output_mount.mount_list[0]
    x,y,z = first.get_coordinate_system()
    first.pos += x * first.element_thickness
    Output_mount.set_geom(Output_mount.get_geom())
  # else:
  #   Output_mount.add(Post_Marker())
  return Output_mount


class Unit_Mount(Geom_Object):
  """
  Mount class, erbit from <Geom_Object>
  Application as follows:
    Mon = Mount(elm_type="mirror")
  Usually exists as part of the component
  """
  # def __init__(self, name="mount",model="default", **kwargs):
  def __init__(self, model="dont_draw", name="mount",element_thickness=5, **kwargs):
    super().__init__(name, **kwargs)
    self.model = model
    self.path = ""
    self.docking_obj = Geom_Object()
    self.element_thickness = element_thickness #standard thickness of for example a mirror
    self.aperture = 25.4
    self.is_horizontal = True
    self.flip_angle = 0
    if self.model != "dont_draw":
      self.set_by_table()
      self.draw_dict["stl_file"] = self.path + self.model + ".stl"
      self.freecad_model = load_STL
      # self.draw_dict["color"] = DEFAULT_MOUNT_COLOR

  def set_axes(self, new_axes):
    if self.is_horizontal:
      old_axes = self.get_axes()
      newx, newy, newz = new_axes[:,0], new_axes[:,1], new_axes[:,2]
      newx = np.array((newx[0],newx[1],0))
      newx *= 1/np.linalg.norm(newx)
      newz = np.array((0,0,1))
      newy = np.cross(newz, newx)
      self._axes[:,0] = newx
      self._axes[:,1] = newy
      self._axes[:,2] = newz
      self._axes_changed(old_axes, self.get_axes())
    else:
      super().set_axes(new_axes)

  def set_by_table(self):
    """
    sets the docking object and the model by reading the "the file.csv"
    Used to determine if there is a default suitable mount in the database.
    Returns
    -------
    bool
      True: this mount was in the csv file, which can be read directy
      False: this mont was not in the csv file
    """
    buf = []
    mount_in_database = False
    if self.model in MIRROR_LIST:
        model_type ="mirror"
    elif self.model in LENS_LIST:
        model_type="lens"
    else:
        model_type = "special_mount"
        # return False
    folder = thisfolder+"mount_meshes/"+model_type+"/"
    with open(folder+model_type+"mounts.csv") as csvfile:
      reader = csv.DictReader(csvfile)

      for row in reader:
        buf.append(row)
    for mount_loop in buf:
      if mount_loop["name"] == self.model:
        mount_in_database = True
        aperture = float(mount_loop["aperture"])
        DockingX = float(mount_loop["DockingX"])
        DockingY = float(mount_loop["DockingY"])
        DockingZ = float(mount_loop["DockingZ"])
        DockNormalX = float(mount_loop["DockNormalX"])
        DockNormalY = float(mount_loop["DockNormalY"])
        DockNormalZ = float(mount_loop["DockNormalZ"])
        self.draw_dict["color"] = eval(mount_loop["color"])
        # eval
    if not mount_in_database:
      print("This mount is not in the database.")
      self.path = folder
      return False
    self.aperture = aperture
    docking_normal = np.array((DockNormalX,DockNormalY,DockNormalZ))
    # self.docking_obj = Geom_Object()
    self.docking_obj.pos = self.pos+DockingX*self._axes[:,0]+DockingY*self._axes[:,1]+DockingZ*self._axes[:,2]
    self.docking_obj.normal = docking_normal
    self.path = folder
    return True

  def reverse(self):
    x,y,z = self.get_coordinate_system()
    self.rotate(z, np.pi)
    self.pos += x * self.element_thickness

  def flip(self, angle=90):
    self.flip_angle = angle


  def update_draw_dict(self):
    super().update_draw_dict()
    modified_axes = self.get_axes()
    modified_axes = np.matmul(rotation_matrix(self.normal, self.flip_angle/180*np.pi), modified_axes)
    self.draw_dict["geom"] = (self.pos, modified_axes)
    self.draw_dict["stl_file"] = self.path + self.model + ".stl"

  def draw_text(self):
    txt = super().draw_text()
    txt += " and the model " + self.model

  def __repr__(self):
    txt = super().__repr__()
    ind = txt.index(",")
    txt2 = txt[0:ind] + ', model="' + self.model + '"' + txt[ind::]
    return txt2

  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos( old_pos, new_pos, [self.docking_obj])

  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.docking_obj])
```

### Post

The post works similarly to the Unit_Mount and inherits from Geom_Obj. The two default options for the model argument are "1inch_post" and "0.5inch_post". Since the alignment of posts is usually even stricter than that of mounts, the post has the property axis_fixed = True, analogous to the property is_horizontal, which means that the inner coordinate system axes never change and are always aligned along the coordinate axes (unit matrix). The second important property distinguishing Post from Unit_Mount is _lower_limit = 0. This sets the lower limit of the Post; the standard is 0, i.e. the Post continuously extends to the table surface, and its model is always automatically adjusted via the find_1inch_post and draw_post functions to correspond to this length. LaserCAD can automatically construct suitable spacers for 1" posts and insert them into the drawing. For the experimenter, these can be selected in FreeCAD and exported as STL files for 3D printing. Nice thing. For instance, if the elements of a particular assembly are on a plate that is 20mm high, the _lower_limit of all assembly posts could be set to 20. (FOR THIS A TUTORIAL WOULD ALSO BE NICE...)
Here is the code:
```python
class Post(Geom_Object):
  def __init__(self, name="post",model="1inch_post", **kwargs):
    super().__init__(name, **kwargs)
    self.axis_fixed = True
    self._lower_limit = 0
    self.draw_dict["post_color"] = DEFALUT_POST_COLOR
    self.draw_dict["holder_color"] = DEFALUT_HOLDER_COLOR
    self.model=model
    self.docking_obj = Geom_Object()

  def set_axes(self, new_axes):
    if self.axis_fixed:
      self._axes = np.eye(3)
    else:
      super().set_axes(new_axes)

  def find_1inch_post(self):
    height = self.pos[2] - self._lower_limit
    if height<12.5:
      print("Warning, there is no suitable post holder at this height")
      return None
    model="RS05P4M"
    height_difference=0
    default_post_height = [12.5,19,25,38,50,65,75,90,100,155,65535]
    model_name = ["RS05P4M","RS075P4M","RS1P4M","RS1.5P4M","RS2P4M","RS2.5P4M",
                  "RS3P4M","RS3.5P4M","RS4P4M","RS6P4M",""]
    for i in range(10):
      if height < default_post_height[i+1] and height > default_post_height[i]:
        model = model_name[i]
        height_difference = height - default_post_height[i]
    return draw_1inch_post(name=model,h_diff = height_difference,ll=self._lower_limit,
                            color=self.draw_dict["post_color"],geom = self.get_geom())

  def draw_post_part(self,name="post_part", base_exists=False,
                     post_color=DEFALUT_POST_COLOR,holder_color=DEFALUT_HOLDER_COLOR, geom=None):
    """
    Draw the post part, including post, post holder and base
    Assuming that all optics are placed in the plane of z = 0.

    Parameters
    ----------
    name : String, optional
      The name of the part. The default is "post_part".
    height : float/int, optional
      distance from the center of the mirror to the bottom of the mount.
      The default is 12.
    xshift : float/int, optional
      distance from the center of the mirror to the cavity at the bottom of the
      mount. The default is 0.
    geom : TYPE, optional
      mount geom. The default is None.

    Returns
    -------
    part : TYPE
      A part which includes the post, the post holder and the slotted bases.

    """
    POS = geom[0]
    POS[2]-=self._lower_limit
    if (POS[2]<34) or (POS[2]>190):
      print("Warning, there is no suitable post holder and slotted base at this height")
      return None
    post_length=50
    if base_exists:
        if POS[2]>110:
          post_length=100
        elif POS[2]>90:
          post_length=75
        elif POS[2]>65:
          post_length=50
        elif POS[2]>55:
          post_length=40
        elif POS[2]>40:
          post_length=30
        else:
          post_length=20
          post2 = draw_post_holder(name="PH20E_M", ll=self._lower_limit,
                                   color=holder_color, geom=geom)
        POS[2]+=self._lower_limit
        post = draw_post(name="TR"+str(post_length)+"_M", color=post_color,geom=geom)
        if post_length>20:
          post2 = draw_post_holder(name="PH"+str(post_length)+"_M", ll=self._lower_limit,
                                   color=holder_color, geom=geom)
    else:
        if POS[2]>105:
          post_length=100
        elif POS[2]>85:
          post_length=75
        elif POS[2]>60:
          post_length=50
        elif POS[2]>50:
          post_length=40
        elif POS[2]>35:
          post_length=30
        else:
          post_length=20
          post2 = draw_post_holder(name="PH"+str(post_length)+"E_M", ll=self._lower_limit,
                                   color=holder_color, geom=geom)
        POS[2]+=self._lower_limit
        post = draw_post(name="TR"+str(post_length)+"_M", color=post_color,geom=geom)
        post2 = draw_post_holder(name="PH"+str(post_length)+"E_M", ll=self._lower_limit,
                                 color=holder_color, geom=geom)
    if base_exists:
      if post_length>90 or post_length<31:
          post1 = draw_post_base(name="BA2_M", geom=geom)
      else:
          post1 = draw_post_base(name="BA1L",  geom=geom)
    else:
      post1 = None
    # print(name,"'s height=",POS[2]+post_length)
    print(name,"'s height=",POS[2])
    part = initialize_composition_old(name=name)
    container = post,post1,post2
    add_to_composition(part, container)
    return part

  def set_lower_limit(self,lower_limit):
    self._lower_limit = lower_limit
    self.docking_obj.pos = np.array((self.pos[0],self.pos[1],self._lower_limit))

  def _pos_changed(self, old_pos, new_pos):
    self.docking_obj.pos = np.array((self.pos[0],self.pos[1],self._lower_limit))

  def draw_freecad(self, **kwargs):
    self.draw_dict["geom"]=self.get_geom()
    self.draw_dict["name"] = self.name
    if self.model == "dont_draw":
      return None
    print(self.name,"'s position = ",self.pos)
    if self.model == "1inch_post":
      return self.find_1inch_post()
    elif self.model == "0.5inch_post":
      return self.draw_post_part(**self.draw_dict)
    else:
      return draw_large_post(height=self.pos[2],geom=self.get_geom())
```


### Composed_Mount

The standard mount of all elements is the Composed_Mount inherited from Geom_Obj, which is usually simply a composition of the two objects Unit_Mount and Post described above and works similarly to Composition. Objects that have a docking_obj can be inserted using the add function. The current docking_obj is always moved to the next corresponding position, and the new element is inserted correctly. In the case of transformations, the _pos and _axes_changed routines again take care of the correct transformation of the sub-objects. The Composed_Mount can be initialised via a list of strings, the unit_model_list. Example: cm = Composed_Mount(unti_model_list = [K1", "1inch_post"]). See also some TUTORIAL for this.

And here is some source code:
```python
class Composed_Mount(Geom_Object):
  """
  This one is for compositions of mulitple mounts stacked togehter
  The add function drags every new mount to the docking position of the old one
  and as usual all are moved correctly when the Composed_Mount is moved
  """
  def __init__(self, unit_model_list=[], **kwargs):
    self.unit_model_list = unit_model_list
    self.mount_list = []
    super().__init__(**kwargs)
    self.docking_obj = Geom_Object()
    self.docking_obj.set_geom(self.get_geom())
    for model in self.unit_model_list:
      if "Marker" in model:
        newmount = Post_Marker()
      elif "post" in model:
        newmount = Post(model=model)
      elif "Angular" in model:
        newmount = Adaptive_Angular_Mount()
      else:
        newmount = Unit_Mount(model=model)
      self.add(newmount)

  def add(self, mount):
    mount.set_geom(self.docking_obj.get_geom())
    self.mount_list.append(mount)
    self.docking_obj.set_geom(mount.docking_obj.get_geom())

  def draw_freecad(self):
    part = initialize_composition_old(name="mount, post and base")
    container = []
    for mount in self.mount_list:
      # container.append(mount.draw_fc())
      container.append(mount.draw())
    add_to_composition(part, container)
    return part

  def reverse(self):
    first = self.mount_list[0]
    first.reverse()
    self.set_geom(self.get_geom()) # to adjust the other elements

  def __repr__(self):
   txt = super().__repr__()
   ind = txt.index(",")
   modellist = str([um.model for um in self.mount_list])
   txt2 = txt[0:ind] + ', unit_model_list=' + modellist + txt[ind::]
   return txt2

  def _pos_changed(self, old_pos, new_pos):
    self._rearange_subobjects_pos(old_pos, new_pos,[self.mount_list[0]])
    for mount_number in range(len(self.mount_list)-1):
      first = self.mount_list[mount_number]
      second = self.mount_list[mount_number+1]
      second.pos = first.docking_obj.pos

  def _axes_changed(self, old_axes, new_axes):
    self._rearange_subobjects_axes( old_axes, new_axes, [self.mount_list[0]])
    for mount_number in range(len(self.mount_list)-1):
      first = self.mount_list[mount_number]
      second = self.mount_list[mount_number+1]
      second.set_geom(first.docking_obj.get_geom())
```



## Non_Interactings

In addition to the optical elements (Opt_Element), some objects derived from Component do not have a next_ray and, therefore, no next_beam function and are thus sorted into the non_interactings group. Examples of this group are Lambda_Plate, Pockels_Cell and Faraday. Strictly speaking, all these elements contain crystals with refractive indices different from 1. Still, their influence on the beam path is usually minimal, especially with parallel beams, which is why LaserCAD neglects it. In addition, for most elements of this type, neither the refractive index nor the length of the material is known when planning the optical experiment. However, for those users who want to include the effect, please refer to the crystal.py module in basic_optics. Assuming a negligible thickness, these elements can now be inserted into the structure of a composition completely analogous to the optical elements with add_on_axis and add_fixed_element. The source code of Lambda_Plate is shown here as an example for all elements in this group:
```python
from ..freecad_models import model_mirror
from ..basic_optics import Component
from ..basic_optics.mount import Unit_Mount,Composed_Mount,Post

DEFAULT_LAMBDA_PLATE_COLOR = (255,255,0)

class Lambda_Plate(Component):

  def __init__(self, name="LambdaPlate", **kwargs):
    super().__init__(name=name, **kwargs)
    self.aperture = 25.4/2
    self.thickness = 2
    self.freecad_model = model_mirror
    self.set_mount_to_default()
    self.draw_dict["Radius"] = 0
    self.draw_dict["color"] = DEFAULT_LAMBDA_PLATE_COLOR

  def set_mount_to_default(self):
    self.Mount = Composed_Mount()
    self.Mount.add(Unit_Mount("lambda_mirror_mount"))
    self.Mount.add(Post())
    self.Mount.set_geom(self.get_geom())
```