# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 10:46:05 2022

@author: mens
"""

import numpy as np
# from basic_optics.freecad_models import freecad_da
from .constants import TOLERANCE, NAME0, NORM0, POS0
from .. freecad_models import freecad_da






def rotation_matrix(vec, phi):
	"""
  berechnet die Rotationsmatrix R_v(phi) um den Vektor <vec> im R^3
  
  calculates the rotation matrix R_v(phi) around the vector <vec> in R^3
  """
	vec = np.array(vec)*1.0 #erst mal in ein float array
	v_abs = np.linalg.norm(vec)
	vec *= 1/v_abs
	rot_mat = np.eye(3)
	rot_mat[0,0] = vec[0]*vec[0]*(1-np.cos(phi)) + np.cos(phi)
	rot_mat[1,0] = vec[1]*vec[0]*(1-np.cos(phi)) + vec[2]*np.sin(phi)
	rot_mat[2,0] = vec[2]*vec[0]*(1-np.cos(phi)) - vec[1]*np.sin(phi)
	rot_mat[0,1] = vec[0]*vec[1]*(1-np.cos(phi)) - vec[2]*np.sin(phi)
	rot_mat[1,1] = vec[1]*vec[1]*(1-np.cos(phi)) + np.cos(phi)
	rot_mat[2,1] = vec[2]*vec[1]*(1-np.cos(phi)) + vec[0]*np.sin(phi)
	rot_mat[0,2] = vec[0]*vec[2]*(1-np.cos(phi)) + vec[1]*np.sin(phi)
	rot_mat[1,2] = vec[1]*vec[2]*(1-np.cos(phi)) - vec[0]*np.sin(phi)
	rot_mat[2,2] = vec[2]*vec[2]*(1-np.cos(phi)) + np.cos(phi)
	return rot_mat

def rotation_matrix_from_vectors(vec1, vec2):
  """ 
  Findet die Rotationsmatrix, die vec1 zu vec2 ausrichtet
  :param vec1: Ein 3D-"Quellen"-Vektor
  :param vec2: Ein 3D-"Ziel"-Vektor
  :return mat: Eine Transformationsmatrix (3x3), die, wenn sie auf vec1 angewendet wird, sie mit vec2 ausrichtet.
   
  Finds the rotation matrix that aligns vec1 to vec2
  :param vec1: A 3d "source" vector
  :param vec2: A 3d "destination" vector
  :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
  """
  vec1 = np.array(vec1) *1.0
  vec2 = np.array(vec2) *1.0
  vec1 *= 1/np.linalg.norm(vec1)
  vec2 *= 1/np.linalg.norm(vec2)
  a = (vec1 / np.linalg.norm(vec1)).reshape(3)
  b =  (vec2 / np.linalg.norm(vec2)).reshape(3)
  v = np.cross(a, b)
  if any(v): #if not all zeros then
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
  else:
      return np.eye(3) #cross of all zeros only occurs on identical directions


def vec2str(vec):
	return repr(np.round(vec, decimals=5))[6:-1]




class Geom_Object(object):
  """
  speichert die elementaren Informationen über Position <pos>, Ausrichtung 
  <normal> und Namen <name>, 
  Definiert die Defaults für alle folgenden Objekte, passt bei Änderung der 
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
  def __init__(self, name=NAME0, pos=POS0, normal=NORM0):
    self.name = name
    self._pos = pos
    self._axes = np.eye(3)
    # das eigene Kordinatensystem, die erste Spalte ist immer die Normale
    self._axes = self._updated_axes(normal, NORM0)
    self.draw_dict = {"name": self.name, "geom":self.get_geom()} #für die Cosmetics


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


  def angle_to(self, obj):
    """
    computes the angle to the normal of an other GeomObj <obj> with
    correct sign
    
    """
    vec = obj.normal
    c = np.cross(self.normal, vec)
    sign = 1 if np.sum(c * self._axes[:,1]) >= 0 else -1
    return np.arcsin(np.linalg.norm(c))*sign

  def rotate(self, vec, phi):
    """
    rotiert das Objekt in Bezug auf vec um den Winkel phi
    Parameters
    ----------
    vec : 3D-Vector
      Raumrichtung um die gedreht wird, muss nicht normiert sein
    phi : Winkel im Bogenmaß

    Bsp: element.rotate((0,1,0), 0.7854)
    entspricht Drehung um y-Achse um 45°
    
    rotates the object with respect to vec by the angle phi
    Parameters
    ----------
    vec : 3D vector
      Space direction around which is rotated, must not be normalized
    phi : angle in radians

    Ex: element.rotate((0,1,0), 0.7854)
    corresponds to rotation around y-axis by 45°.
    
    """
    rot_mat = rotation_matrix(vec, phi)
    # print(rot_mat)
    new_ax = np.matmul(rot_mat, self._axes)
    self.set_axes(new_ax) 


  def __repr__(self):
    txt = self.class_name()+ '(name="' + self.name
    txt += '", pos='+vec2str(self.pos)
    txt += ", normal="+vec2str(self.normal)+")"
    return txt

  def __str__(self):
    return ">>> " + repr(self)

  def class_name(cls):
    return str(type(cls)).split(".")[-1].split("'")[0]

  def get_geom(self):
    """
    gibt das so genannte geom = (pos, axes) zurück, einfach nur ein Tupel aus 
    <pos> und <axes>, wichtig zur geometrischen Definition der meisten Objekte
    
    returns the so-called geom, simply a tuple of <pos> and 
    <axes>, important for the geometric definition of most objects
    """
    return (self.pos, self.get_axes())

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
      return self.draw_fc()
    else:
      txt = self.draw_text()
      print(txt)
      return txt

  def draw_fc(self):
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
    #ToDo: fürs Debugging hier einfach einen Zylinder mit norm uns k zeichnen
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
#     txt = "Das geometrische Objekt <" + self.name + "> wird an die Position "
    # txt = "Das Objekt <" + self.class_name() + ":" +self.name
    txt = "The geometric object <" + self.class_name() + ":" + self.name
    # txt += "> wird an die Position "
    txt += "> is drawn to the position"
    # txt += vec2str(self.pos) + " mit der Ausrichtung " + vec2str(self.normal)
    txt += vec2str(self.pos) + " with the direction " + vec2str(self.normal)
    # txt += " gezeichnet."
    return txt

  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird, kann nützlich
    sein für abgeleitete, zusammengesetzte Objekte wie beam oder composition
    
    is called when the position of <self> is changed, can be useful for derived
    for derived, composite objects like beam or composition
    """
    pass
    
    
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

  # def is_equal(self, obj):
  #   """
  #   checkt ob <self> und obj äquivalent sind, also ob sie die gleichen Einträge
  #   haben
  #   returns True/False
  #   """
  #   d1 = self.__dict__
  #   d2 = obj.__dict__
  #   res = True
  #   for key in d1.keys():
  #     res &= np.all( d1[key] == d2[key] )
  #   return res


def tests():
  normal0 = np.array((23,6,1))
  print(normal0)
  x = Geom_Object("Klaus", normal=normal0)
  print(x)
  print(x.get_geom())
  p = x.get_geom()
  n = p[1]
  bet = np.sqrt(n[0]**2+n[1]**2+n[2]**2)
  print("Normale von x:", n, "   mit Betrag:", bet)
  x.draw()

  print()

  g = Geom_Object()
  g2 = Geom_Object()
  xvec = np.array((1,0,0))
  print("Winkel von g zur x-Achse default", g.angle_to(g2))
  print("KooSys von g default x y z:", g.get_coordinate_system())
  yvec = np.array((0,1,0))
  g.normal = (yvec)
  print("KooSys von g nach Drehung auf yAchse x y z:", g.get_coordinate_system())
  g.normal = -xvec
  print("KooSys von g nach Drehung auf -xAchse x y z:", g.get_coordinate_system())
  print("sollte bei (-1,0,0), (0,-1,0) und (0,0,1) liegen")

  print()

  h = Geom_Object()
  zvec = np.array((0,0,1))
  print("KooSys von h default x y z:", h.get_coordinate_system())
  h.normal = (zvec)
  print("KooSys von h nach Drehung auf zAchse x y z:", h.get_coordinate_system())
  h.normal = -xvec
  print("KooSys von h nach Drehung auf -xAchse x y z:", h.get_coordinate_system())
  print("sollte bei (-1,0,0), (0,1,0) und (0,0,-1) liegen")

  return x, g, h


if __name__ == "__main__":
  tests()
