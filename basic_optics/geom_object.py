# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 10:46:05 2022

@author: mens
"""

# print("geom_object modul wird importiert")

import numpy as np
from scipy.spatial.transform import Rotation as Rot
from basic_optics.freecad_models import model_lens, freecad_da


NAME0="unnamed"
POS0 = np.array((0,0,80)) #Strahlhöhe 80 mm
NORM0 = np.array((1,0,0)) #Strahl startet in x-Richtung
TOLERANCE = 1e-8 #Wert ab dem zwei Größen (meist Winkel) als gleich angenommen werden

# def is_round_about(): #sollte mal toleranz einarbeiten, wurde aber noch nicht geschrieben
# 	return False

# def rotation_matrix(v, phi):
#     """berechnet die Rotationsmatrix R_v(phi) um den Vector v im R^3"""
#     v = np.array(v)
#     v /= np.linalg.norm(v)  # falls v nicht normiert ist
#     return Rot.from_rotvec(phi * v).as_matrix()

def rotation_matrix(vec, phi):
	"""berechnet die Rotationsmatrix R_v(phi) um den Vectro v im R^3"""
	vec = np.array(vec)*1.0 #erst mal in ein float array
	v_abs = np.linalg.norm(vec)
	vec *= 1/v_abs
	rot_mat = np.eye(3)
	rot_mat[0,0] = vec[0]*vec[0]*(1-np.cos(phi)) + np.cos(phi)
	rot_mat[0,1] = vec[1]*vec[0]*(1-np.cos(phi)) + vec[2]*np.sin(phi)
	rot_mat[0,2] = vec[2]*vec[0]*(1-np.cos(phi)) - vec[1]*np.sin(phi)
	rot_mat[1,0] = vec[0]*vec[1]*(1-np.cos(phi)) - vec[2]*np.sin(phi)
	rot_mat[1,1] = vec[1]*vec[1]*(1-np.cos(phi)) + np.cos(phi)
	rot_mat[1,2] = vec[2]*vec[1]*(1-np.cos(phi)) + vec[0]*np.sin(phi)
	rot_mat[2,0] = vec[0]*vec[2]*(1-np.cos(phi)) + vec[1]*np.sin(phi)
	rot_mat[2,1] = vec[1]*vec[2]*(1-np.cos(phi)) - vec[0]*np.sin(phi)
	rot_mat[2,2] = vec[2]*vec[2]*(1-np.cos(phi)) + np.cos(phi)
	return rot_mat

def rotation_matrix_from_vectors(vec1, vec2):
  """ Find the rotation matrix that aligns vec1 to vec2
  :param vec1: A 3d "source" vector
  :param vec2: A 3d "destination" vector
  :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
  """
  vec1 = np.array(vec1) *1.0
  vec2 = np.array(vec2) *1.0
  vec1 *= 1/np.linalg.norm(vec1)
  vec2 *= 1/np.linalg.norm(vec2)
  a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
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
  speichert die elementaren Informationen über Position und Ausrichtung
  und Namen, definiert die Defaults für alle folgenden Objekte
  passt bei Änderung der normal automatisch das inner Koordiantwensystem an
  Bsp: geom = Geom_Object(name="ErsterPunkt", pos=(1,2,3), norm=(-1,2,0))
  siehe tests()
  Methoden:
    siehe __dict__


  """
  def __init__(self, name=NAME0, pos=POS0, normal=NORM0):
    self.name = name
    self._pos = pos
    # self._normal = normal # wird schon später noch gebraucht
    self._axes = np.eye(3)
    # self.__normal = normal/ np.linalg.norm(normal) #als property immer auf 1 normiert
    # das eigene Kordinatensystem, die erste Spalte ist immer die Normale
    self._axes = self._updated_axes(normal, NORM0)
    # self.normal = self.__normal #um das axes zu ändern und alle Folgefunktionen aufzurufen falls nötig
    self.draw_dict = {"name": self.name, "geom":self.get_geom()} #für die Cosmetics

  # stellt sicher, das immer Copies von norm und pos übergeben werden
  # und alles float arrays sind, normiert die normal, updatet das eigene Koo-Sys "axes"
  @property
  def pos(self):
    return np.array(self._pos) * 1.0
  @pos.setter
  def pos(self, x):
    old_pos = self._pos
    self._pos = np.array(x) * 1.0
    self._pos_changed(old_pos, x)

  @property
  def normal(self):
    return np.array(self._axes[:,0])
  @normal.setter
  def normal(self, x):
    # old_normal = np.array(self.__normal)
    old_normal = self.normal
    # self.__normal = x / np.linalg.norm(x)
    new_normal = x / np.linalg.norm(x)
    # print(new_normal, old_normal)
    # self.__normal_changed(old__normal, x)
    self.set_axes(self._updated_axes(new_normal, old_normal))
    # self._axes[:,0] = np.array(self.__normal)

  def get_axes(self):
    # gibt _axes zurück
    return np.array(self._axes)
  
  def get_coordinate_system(self):
    # gibt normal, senkrecht1 und senkrecht2 als 3 Vektoren zurück
    m = np.array(self._axes)
    return m[:,0], m[:,1], m[:,2]

  def set_axes(self, new_axes):
    old_axes = self.get_axes()
    self._axes = np.array(new_axes)
    # self.__normal = np.array(new_axes[:,0])
    self._axes_changed(old_axes, new_axes)
    

  def _updated_axes(self, new_normal, old_normal):
    """
    old_normal : 3D-array
    berechnet das neue Koordinatensystem durch Drehmatrix zwischen
    (neu-) normal und old_normal
    """
    # print("norm, oldnorm:", (self.__normal, old_normal))
    v = np.cross(new_normal, old_normal) # Drehvektor
    v_abs = np.linalg.norm(v)
    # if v_abs > 1:
      # print("---",v_abs,"---")
      # v_abs = 1
    # elif v_abs < -1:
      # print("---",v_abs,"---")
      # v_abs = -1
    # phi = np.arcsin(v_abs)
    skalarP = np.sum(new_normal * old_normal)
    if v_abs < TOLERANCE:
      if skalarP >= 0:
        # phi kleiner als 1e-8
        # print("GO: phi kleiner als 1e-8")
        return self._axes
      else:
        # phi rund 180°, d.h. die drehung ist nicht eindeutig, negieren
        # willkürlich ax0 und ax1 und behalten ax2 bei um rechtshändiges KooSys
        # zu erhalten. (ax0 und ax2 würden genau so funktionieren)
        # print("GO:phi rund 180°")
        a,b,c = self.get_coordinate_system()
        a = new_normal #just in case
        return np.vstack((a,-b,c))
    else:
      # rot_mat = rotation_matrix(v, phi)
      rot_mat = rotation_matrix_from_vectors(old_normal, new_normal)
      # print("axes:",  self._axes)
      # print("rotmat", rot_mat)
      # print("result", np.matmul(rot_mat, self._axes))
      return np.matmul(rot_mat, self._axes)


  def angle_to(self, vec):
    """computes the angle from a "z-height-ray to the Vector vec with
    correct sign"""
    vec = vec / np.linalg.norm(vec)
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
    """
    rot_mat = rotation_matrix(vec, -phi)
    new_ax = np.matmul(rot_mat, self._axes)
    # self.__normal = new_ax[:,0]
    self.set_axes(new_ax ) #nur um sicher zu gehen, kP, Drehungen im R3 halt


  def __repr__(self):
#     txt = 'Geom_Object(name="' + self.name
    txt = self.Klassenname()+ '(name="' + self.name
    txt += '", pos='+vec2str(self.pos)
    txt += ", normal="+vec2str(self.normal)+")"
    return txt

  def __str__(self):
    return ">>> " + repr(self)

  def Klassenname(cls):
    return str(type(cls)).split(".")[-1].split("'")[0]

  def get_geom(self):
    return (self.pos, self.normal)

  def set_geom(self, geom):
    self.pos = np.array(geom[0])
    self.normal = np.array(geom[1])
    
  def update_draw_dict(self):
    self.draw_dict["name"]=self.name
    self.draw_dict["geom"]=self.get_geom() 

  def draw(self):
    if freecad_da:
      return self.draw_fc()
    else:
      txt = self.draw_text()
      print(txt)
      return txt

  def draw_fc(self):
    #ToDo: fürs Debugging hier einfach einen Zylinder mit norm uns k zeichnen
    return None

  def draw_text(self):
#     txt = "Das geometrische Objekt <" + self.name + "> wird an die Position "
    txt = "Das Objekt <" + self.Klassenname() + ":" +self.name
    txt += "> wird an die Position "
    txt += vec2str(self.pos) + " mit der Ausrichtung " + vec2str(self.normal)
    txt += " gezeichnet."
    return txt

  # def FreeCAD_model(self):
  #   """
  #   deprecated
  #   """
  #   model_lens()

  def is_equal(self, obj):
    """
    checkt ob <self> und obj äquivalent sind, also ob sie die gleichen Einträge
    haben
    returns True/False
    """
    d1 = self.__dict__
    d2 = obj.__dict__
    res = True
    for key in d1.keys():
      res &= np.all( d1[key] == d2[key] )
    return res

  def _pos_changed(self, old_pos, new_pos):
    """
    wird aufgerufen, wen die Position von <self> verändert wird, kann nützlich
    sein für abgeleitete, zusammengesetzte Objekte wie beam oder composition
    """
    pass

  # def _normal_changed(self, old_normal, new_normal):
  #   """
  #   deprecated, nutze _axes_changed
    
  #   wird aufgerufen, wen die Normale von <self> verändert wird, kann nützlich
  #   sein für abgeleitete, zusammengesetzte Objekte wie beam oder composition

  #   dreht außerdem das eigene Koordiantensystem
  #   """
  #   old_axes = self.get_axes()
  #   new_axes = self._updated_axes(old_normal)
  #   self._axes = new_axes
  #   self._axes_changed(old_axes, new_axes)
    
    
  def _axes_changed(self, old_axes, new_axes):
    pass
    # self.__normal = self._axes[:,0]
    
    
  def _rearange_subobjects_axes(self, old_axes, new_axes, objs):
    """
    wichtig für beam und Composition
    wenn eigene <old_axes> auf <new_axes> geändert wird, soll die _axes
    aller Subobjekte entsprechend geändert werden, d.h. relative Ausrichtung
    und Drehung soll beibehalten werden
    ...LinAlg Kram halt
    """
    RotM = np.matmul(new_axes, np.linalg.inv(old_axes) )
    p0 = self.pos
    for obj in objs:
      qvec = obj.pos - p0 # relativer Orstvector innnerhalb der Einheit
      new_qvec = np.matmul(RotM, qvec)
      obj.pos = new_qvec + p0
      obj.set_axes( np.matmul( RotM, obj.get_axes() ) )
      
  # def _rearange_subobjects_normal(self, old_normal, new_normal, objs):
  #   """
  #   deprecated, wird jetzt über "_changed_axes" erledigt 
    
  #   wichtig für beam und Composition
  #   wenn eigene <old_normal> auf <new_normal> geändert wird, soll die normal
  #   aller Subobjekte entsprechend geändert werden, d.h. relative Ausrichtung
  #   und Drehung soll beibehalten werden
  #   ...LinAlg Kram halt
  #   """
  #   p0 = self.pos
  #   RotM = rotation_matrix_from_vectors(old_normal, new_normal)
  #   for obj in objs:
  #     qvec = obj.pos - p0 # relativer Orstvector innnerhalb der Einheit
  #     new_qvec = np.matmul(RotM, qvec)
  #     obj.pos = new_qvec + p0
  #     obj.normal = np.matmul(RotM, obj.normal)
  #     # das sollte es gewesen sein

  def _rearange_subobjects_pos(self, old_pos, new_pos, objs):
    """
    wichtig für beam und Composition
    wenn eigene <old_pos> auf <new_pos> geändert wird, soll die pos aller
    Subobjekte entsprechend geändert werden, d.h. relative Ausrichtung und
    Drehung soll beibehalten werden
    ...LinAlg Kram halt
    """
    delta_pos = new_pos - old_pos
    for obj in objs:
      obj.pos += delta_pos
      # das sollte es gewesen sein




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
  xvec = np.array((1,0,0))
  print("Winkel von g zur x-Achse default", g.angle_to(xvec))
  print("KooSys von g default x y z:", g.get_axes())
  yvec = np.array((0,1,0))
  g.normal = (yvec)
  print("KooSys von g nach Drehung auf yAchse x y z:", g.get_axes())
  g.normal = -xvec
  print("KooSys von g nach Drehung auf -xAchse x y z:", g.get_axes())
  print("sollte bei (-1,0,0), (0,-1,0) und (0,0,1) liegen")

  print()

  h = Geom_Object()
  zvec = np.array((0,0,1))
  print("KooSys von h default x y z:", h.get_axes())
  h.normal = (zvec)
  print("KooSys von h nach Drehung auf zAchse x y z:", h.get_axes())
  h.normal = -xvec
  print("KooSys von h nach Drehung auf -xAchse x y z:", h.get_axes())
  print("sollte bei (-1,0,0), (0,1,0) und (0,0,-1) liegen")

  return x, g, h


if __name__ == "__main__":
  tests()
