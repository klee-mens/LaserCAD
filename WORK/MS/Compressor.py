# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:53:29 2024

@author: 12816
"""

import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
from copy import deepcopy

from LaserCAD.freecad_models import clear_doc, setview, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch
from LaserCAD.basic_optics import Curved_Mirror, Ray, Component
from LaserCAD.basic_optics import LinearResonator, Lens
from LaserCAD.basic_optics import Grating, Crystal
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate
from LaserCAD.basic_optics.mirror import Stripe_mirror
from LaserCAD.moduls import Make_RoofTop_Mirror
from LaserCAD.basic_optics.mount import Unit_Mount, Composed_Mount
from LaserCAD.non_interactings.table import Table
if freecad_da:
  clear_doc()
  
grating_const = 1/1480 # in 1/mm
seperation = 5750 # difference grating position und radius_concave
lambda_mid = 1030e-9 * 1e3 # central wave length in mm
delta_lamda = 60e-9*1e3 # full bandwith in mm
number_of_rays = 15
# safety_to_stripe_mirror = 5 #distance first incomming ray to stripe_mirror in mm
periscope_height = 12
c0 = 299792458*1000 #mm/s

lightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lambda_mid-delta_lamda/2, lambda_mid+delta_lamda/2, number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
  rn = Ray()
  # rn.normal = vec
  # rn.pos = pos0
  rn.wavelength = wavel
  x = 1-(wavel - lambda_mid + delta_lamda/2) / delta_lamda
  rn.draw_dict["color"] = cmap( x )
  rays.append(rn)
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"
helper_light_source = Beam(angle=0, wavelength=lambda_mid)

Compressor= Composition()
Compressor.set_light_source(lightsource)
Compressor.redefine_optical_axis(helper_light_source.inner_ray())

angle = gamma = 8.3254033412311523321136 /180*np.pi
SinS = np.sin(angle)
CosS = np.cos(angle)

v = lambda_mid/grating_const
a = v/2
B = np.sqrt(a**2 - (v**2 - SinS**2)/(2*(1+CosS)))
sinB_new = a - B
Grating_normal = (np.sqrt(1-sinB_new**2), sinB_new, 0)

Grat1 = Grating(grat_const=grating_const, order=-1)
Grat1.pos -=(500-10,0,0)
Grat1.normal = Grating_normal
Grat1.normal = -Grat1.normal
Plane_height = 23+25.4
Grat2 = Grating(grat_const=grating_const, order=-1)
# propagation_length = 99.9995
# propagation_length = seperation*2-0.0078
propagation_length = seperation

# propagation_length = 99.9949
Grat2.pos -= (500-10-propagation_length*CosS,SinS*propagation_length,0)
Grat2.normal = Grating_normal

shift_direction = np.cross((0,0,1),Grat1.normal)
Grat1.pos += shift_direction * -15
Grat2.pos += shift_direction * 1

Grat1.pos += (1000,0,0)
Grat2.pos += (1000,0,0)

# =============================================================================
# Four Gratings Compressor
# =============================================================================
Grat3 =Grating(grat_const=grating_const,order=1)
Grat3.pos = (Grat1.pos[0]-Grat2.pos[0]+Grat1.pos[0]-45-2*35*abs(Grat1.normal[0]),Grat2.pos[1],Grat2.pos[2])
Grat3.normal = (Grat1.normal[0],-Grat1.normal[1],Grat1.normal[2])
Grat4 =Grating(grat_const=grating_const,order=1)
Grat4.pos = (Grat2.pos[0]-Grat2.pos[0]+Grat1.pos[0]-45-2*35*abs(Grat1.normal[0]),Grat1.pos[1],Grat2.pos[2])
Grat4.normal = (Grat2.normal[0],-Grat2.normal[1],Grat2.normal[2])
# Grat3.pos += (1,0,0)
# Grat4.pos -= (1,0,0)

# Grat3.rotate((0,0,1), 0.01)
# Grat4.rotate((0,0,1), 0.01)

# Grat1.height=Grat2.height=Grat3.height=Grat4.height=25
Grat1.thickness=Grat2.thickness=Grat3.thickness=Grat4.thickness=9.5
Grat1.set_mount_to_default()
Grat2.set_mount_to_default()
Grat3.set_mount_to_default()
Grat4.set_mount_to_default()
Grat1.Mount.mount_list[1].flip(-90)
Grat2.Mount.mount_list[1].flip(-90)
Grat1.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat2.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat3.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat4.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat1.Mount.mount_list[1].docking_obj.pos = Grat1.Mount.mount_list[1].pos + Grat1.Mount.mount_list[1].normal*17.1-np.array((0,0,1))*25.4
Grat1.Mount.mount_list[2].set_geom(Grat1.Mount.mount_list[1].docking_obj.get_geom())
Grat2.Mount.mount_list[1].docking_obj.pos = Grat2.Mount.mount_list[1].pos + Grat2.Mount.mount_list[1].normal*17.1-np.array((0,0,1))*25.4
Grat2.Mount.mount_list[2].set_geom(Grat2.Mount.mount_list[1].docking_obj.get_geom())
Grat3.Mount.mount_list[1].docking_obj.pos = Grat3.Mount.mount_list[1].pos + Grat3.Mount.mount_list[1].normal*17.1-np.array((0,0,1))*25.4
Grat3.Mount.mount_list[2].set_geom(Grat3.Mount.mount_list[1].docking_obj.get_geom())
Grat4.Mount.mount_list[1].docking_obj.pos = Grat4.Mount.mount_list[1].pos + Grat4.Mount.mount_list[1].normal*17.1-np.array((0,0,1))*25.4
Grat4.Mount.mount_list[2].set_geom(Grat4.Mount.mount_list[1].docking_obj.get_geom())
# PM1=Post_Marker()
# PM2=Post_Marker()
# Grat2.Mount.add(PM1)
# Grat3.Mount.add(PM2)
# print("setting pos=",(Grat1.pos+Grat2.pos+Grat3.pos+Grat4.pos)/4)
# ip = Intersection_plane()
# ip.pos -= (100,0,0)
Roof = Make_RoofTop_Mirror(height=periscope_height, up=False)
Compressor.add_fixed_elm(Grat4)
Compressor.add_fixed_elm(Grat3)
Compressor.recompute_optical_axis()
Compressor.propagate(750)
Compressor.add_supcomposition_on_axis(Roof)
Compressor.set_sequence([0,1,2,3,1,0])
Compressor.recompute_optical_axis()
# Compressor.add_fixed_elm(Grat2)
# Compressor.add_fixed_elm(Grat1)
Compressor.propagate(300)
Compressor.draw()

pathlength = {}
for ii in range(Compressor._beams[0]._ray_count):
  wavelength = Compressor._beams[0].get_all_rays()[ii].wavelength
  pathlength[wavelength] = 0
for jj in range(len(Compressor._beams)-1):
  for ii in Compressor._beams[jj].get_all_rays():
    a=pathlength[ii.wavelength]
    pathlength[ii.wavelength] = a +ii.length
ray_lam = [ray.wavelength for ray in Compressor._beams[0].get_all_rays()]
path = [pathlength[ii] for ii in ray_lam]
path_diff = [ii-path[int(len(path)/2)] for ii in path]
fai = [path_diff[ii]/ray_lam[ii]*2*np.pi for ii in range(len(path))]
delay = [path_diff[ii]/c0 for ii in range(len(path))]
omega = [c0/ii*2*np.pi for ii in ray_lam]
omega = [(ii - c0/lambda_mid*2*np.pi) for ii in omega]
fai_new = deepcopy(fai)
delay_new = deepcopy(delay)
para_order = 9
para = np.polyfit(omega, fai, 6)
fai = [para[0]*(ii**6) + para[1]*(ii**5) + para[2]*(ii**4) + para[3]*(ii**3) + para[4]*(ii**2) + para[5]*(ii) + para[6] for ii in omega]
fai1 = [6  *para[0]*(ii**5) + 5 *para[1]*(ii**4) + 4 *para[2]*(ii**3) + 3*para[3]*(ii**2) + 2*para[4]*(ii) + para[5] for ii in omega]
fai2 = [30 *para[0]*(ii**4) + 20*para[1]*(ii**3) + 12*para[2]*(ii**2) + 6*para[3]*ii + 2*para[4] for ii in omega] # Taylor Expantion
fai3 = [120*para[0]*(ii**3) + 60*para[1]*(ii**2) + 24*para[2]*ii      + 6*para[3] for ii in omega]
para = np.polyfit(omega, delay, para_order)
fai2 = []
fai3 = []
i_count = 0
for ii in omega:
  fai_add = 0
  fai_add2 = 0
  fai_add3 = 0
  for jj in range(para_order,-1,-1):
    fai_add += para[para_order-jj]* ((ii)**jj)
    if jj-1>=0:
      fai_add2 += para[para_order-jj] * jj * (ii**(jj-1))
    if jj-2>=0:
      fai_add3 += para[para_order-jj] * jj * (jj-1) * (ii**(jj-2))
  fai2.append(fai_add2)
  fai3.append(fai_add3)
plt.figure()

ax1=plt.subplot(1,3,1)
plt.scatter(omega,delay,label="delay")
plt.plot(omega,delay_new,label="delay")
plt.title("Relationship of delay with angular frequency",fontsize = 20)
plt.xlabel("angular frequency ω (rad/s)",fontsize = 20)
plt.ylabel("delay (s)",fontsize = 20)
plt.axhline(delay[int(len(delay)/2)], color = 'black', linewidth = 1)
ax2=plt.subplot(1,3,2)
plt.plot(omega,fai2)
plt.title("Group delay dispersion",fontsize = 20)
plt.xlabel("angular frequency ω (rad/s)",fontsize = 20)
plt.ylabel("The second order derivative of φ(ω)",fontsize = 20)
plt.axhline(fai2[int(len(fai2)/2)], color = 'black', linewidth = 1)
print("Group delay dispersion at the center wavelength:",fai2[int(len(fai2)/2)])
ax3=plt.subplot(1,3,3)
plt.plot(omega,fai3)
# plt.plot(omega_d,fai3_new)
plt.title("Third order dispersion",fontsize = 20)
plt.xlabel("angular frequency ω (rad/s)",fontsize = 20)
plt.ylabel("The third order derivative of φ(ω)",fontsize = 20)
plt.axhline(fai3[int(len(fai3)/2)], color = 'black', linewidth = 1)
print("3rd order dispersion at the center wavelength:",fai3[int(len(fai2)/2)])
