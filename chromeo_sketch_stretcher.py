# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:41:34 2023

@author: 12816
"""

import numpy as np
import sys

pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
ind = pfad.rfind("/")
pfad = pfad[0:ind-1]
ind = pfad.rfind("/")
pfad = pfad[0:ind]
if not pfad in sys.path:
  sys.path.append(pfad)

from scipy.interpolate import interp1d
from scipy.misc import derivative

from LaserCAD.freecad_models import clear_doc, freecad_da
from LaserCAD.basic_optics import Mirror, Beam, Composition, inch
from LaserCAD.basic_optics import Curved_Mirror, Ray, Lens
from LaserCAD.basic_optics.mirror import Rooftop_mirror,Stripe_mirror
# from LaserCAD.basic_optics import LinearResonator, Lens
from LaserCAD.basic_optics import Grating, Intersection_plane
import matplotlib.pyplot as plt
from LaserCAD.freecad_models.utils import thisfolder, load_STL
from LaserCAD.non_interactings import Faraday_Isolator, Pockels_Cell, Lambda_Plate,Table
from LaserCAD.basic_optics.mount import Unit_Mount

if freecad_da:
  clear_doc()

c0 = 299792458*1000 #mm/s

def dont():
  return None


# def Make_Stretcher_chromeo():
"""
constructs an Offner Stretcher with an on axis helper composition
Note: When drawing a rooftop mirror, we will draw apure_cosmetic mirror to
confirm the position of the mount. The mirror's geom is the average of two
flip mirror. And its aperture is the periscope_height.
Returns
-------
TYPE Composition
  den gesamten, geraytracten Strecker...
"""
# defining parameters
radius_concave = 1000 #radius of the big concave sphere
aperture_concave = 6 * inch
height_stripe_mirror = 10 #height of the stripe mirror in mm
width_stripe_mirror = 75 # in mm
seperation_angle = 10 /180 *np.pi # sep between in and outgoing middle ray
# incident_angle = seperation_angle + reflection_angle
grating_const = 1/450 # in 1/mm
seperation = 135 # difference grating position und radius_concave
lambda_mid = 2400e-9 * 1e3 # central wave length in mm
delta_lamda = 200e-9*1e3 # full bandwith in mm
number_of_rays = 10
safety_to_stripe_mirror = 5 #distance first incomming ray to stripe_mirror in mm
periscope_height = 15
first_propagation = 20 # legnth of the first ray_bundle to flip mirror1 mm
distance_flip_mirror1_grating = 300
distance_roof_top_grating = 600

input_radius = 1.25
C1 = np.pi/2 # assume input_radius*input_angle = lambda/pi*C1, C1 is a const. C1=1 if the input beam is a Gaussian beam
C1 = 1 # assume input_radius*input_angle = lambda/pi*C1, C1 is a const. C1=1 if the input beam is a Gaussian beam
input_angle = (lambda_mid+delta_lamda/2)/np.pi*C1/input_radius
# input_angle = 0

# calculated parameters according to the grating equation
v = lambda_mid/grating_const
s = np.sin(seperation_angle)
c = np.cos(seperation_angle)
a = v/2
b = np.sqrt(a**2 - (v**2 - s**2)/(2*(1+c)))
sinB = a - b
grating_normal = (np.sqrt(1-sinB**2), sinB, 0)
# print(np.arcsin(sinB)*180/np.pi)

Concav = Curved_Mirror(radius=radius_concave, name="Concav_Mirror")
Concav.aperture = aperture_concave
Concav.set_mount_to_default()
# Concav.mount.model = "default"

StripeM = Stripe_mirror(radius= -radius_concave/2, name="Stripe_Mirror")
#Cosmetics
StripeM.aperture = width_stripe_mirror
StripeM.draw_dict["height"] = height_stripe_mirror
# StripeM.draw_dict["thickness"] = 25 # arbitrary
StripeM.thickness = 25
StripeM.draw_dict["model_type"] = "Stripe"

Grat = Grating(grat_const=grating_const, name="Gitter", order=-1)

Grat.normal = grating_normal

helper = Composition()
helper_light_source = Beam(angle=0, wavelength=lambda_mid)
helper.set_light_source(helper_light_source)
#to adjust the wavelength of the oA
helper.redefine_optical_axis(helper_light_source.inner_ray())
helper.add_fixed_elm(Grat)
helper.recompute_optical_axis()
helper.propagate(radius_concave - seperation)
helper.add_on_axis(Concav)
helper.propagate(radius_concave/2)
helper.add_on_axis(StripeM)


# -----------------------------------------------------------------------------
# setting the lightsource as a beam of different coulered rays
lightsource = Beam(radius=0, angle=0)
wavels = np.linspace(lambda_mid-delta_lamda/2, lambda_mid+delta_lamda/2, number_of_rays)
rays = []
cmap = plt.cm.gist_rainbow
for wavel in wavels:
    B_test = Beam(radius=input_radius,angle=input_angle)
    B_test.make_cone_distribution(ray_count=9)
    ray_group =B_test.get_all_rays()
    for rn in ray_group:
      # rn = Ray()
      # rn.normal = vec
      # rn.pos = pos0
      rn.wavelength = wavel
      x = 1-(wavel - lambda_mid + delta_lamda/2) / delta_lamda
      rn.draw_dict["color"] = cmap( x )
      rays.append(rn)
lightsource.override_rays(rays)
lightsource.draw_dict['model'] = "ray_group"
# -----------------------------------------------------------------------------
"""

# setting the lightsource as an bundle of different coulered rays
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
"""
# starting the real stretcher
Stretcher = Composition(name="DerStrecker")
Stretcher.set_light_source(lightsource)
Stretcher.redefine_optical_axis(helper_light_source.inner_ray())

Stretcher.propagate(first_propagation)
FlipMirror_In_Out = Mirror(phi=-90, name="FlipMirrorInOut")
Stretcher.add_on_axis(FlipMirror_In_Out)
FlipMirror_In_Out.pos += (0,0,-periscope_height/2)
Stretcher.propagate(distance_flip_mirror1_grating)

#adding the helper
helper.set_geom(Stretcher.last_geom())
helper.pos += (0,0, height_stripe_mirror/2 + safety_to_stripe_mirror)
for element in helper._elements:
  Stretcher.add_fixed_elm(element)

Stretcher.set_sequence([0,1,2,3,2,1])
Stretcher.recompute_optical_axis()

# adding the rooftop mirror and it's cosmetics
Stretcher.propagate(distance_roof_top_grating)
RoofTop1 = Mirror(phi=0, theta=90)
Stretcher.add_on_axis(RoofTop1)
Stretcher.propagate(periscope_height)
RoofTop2 = Mirror(phi=0, theta=90)
Stretcher.add_on_axis(RoofTop2)

RoofTop1.draw = dont
# RoofTop1.draw_dict["mount_type"] = "dont_draw"
RoofTop1.Mount = Unit_Mount("dont_draw")
RoofTop2.draw = dont
RoofTop2.Mount = Unit_Mount("dont_draw")

pure_cosmetic = Rooftop_mirror(name="RoofTop_Mirror")
pure_cosmetic.draw_dict["mount_type"] = "rooftop_mirror_mount"
pure_cosmetic.pos = (RoofTop1.pos + RoofTop2.pos ) / 2
pure_cosmetic.normal = (RoofTop1.normal + RoofTop2.normal ) / 2
# pure_cosmetic.draw = dont
pure_cosmetic.aperture = periscope_height
pure_cosmetic.draw_dict["model_type"] = "Rooftop"
pure_cosmetic.set_mount_to_default()

# le1 = Lens(f=-75)
# le1.pos -= (0,0,periscope_height)
# le2 = Lens(f=100)
# le2.pos -= (25,0,periscope_height)
# Stretcher.add_fixed_elm(le1)
# Stretcher.add_fixed_elm(le2)

ip_s = Intersection_plane(name="the end of the Stretcher")
# ip_s.pos -=(0,0,periscope_height) #two gratings
# ip_s.pos -=(1000,0,periscope_height) #four gratings
ip_s.pos -=(1000,0,periscope_height-24) #four gratings

# angle = 10.00134
# angle = 10.001
angle = 10
SinS = np.sin(angle/180*np.pi)
CosS = np.cos(angle/180*np.pi)

v = lambda_mid/grating_const
a = v/2
B = np.sqrt(a**2 - (v**2 - SinS**2)/(2*(1+CosS)))
sinB_new = a - B
Grating_normal = (np.sqrt(1-sinB_new**2), sinB_new, 0)

Grat1 = Grating(grat_const=grating_const, order=-1)
Grat1.pos -=(500,0,periscope_height)
Grat1.normal = Grating_normal
Grat1.normal = -Grat1.normal
Plane_height = 23+25.4
Grat2 = Grating(grat_const=grating_const, order=-1)
# propagation_length = 99.9995
# propagation_length = seperation*2-0.0078
propagation_length = seperation*2-0.008

# propagation_length = 99.9949
Grat2.pos -= (500-propagation_length*CosS,SinS*propagation_length,periscope_height)
Grat2.normal = Grating_normal

shift_direction = np.cross((0,0,1),Grat1.normal)
Grat1.pos += shift_direction * -15
Grat2.pos += shift_direction * 1

"""
# =============================================================================
# Two Gratings Compressor
# =============================================================================
C_RoofTop1 = Mirror()
C_RoofTop1.pos -= (700,SinS*propagation_length,periscope_height)
C_RoofTop1.normal = (-1,0,-1)
C_RoofTop2 = Mirror()
C_RoofTop2.pos -= (700,SinS*propagation_length,0)
C_RoofTop2.normal = (-1,0,1)

C_RoofTop1.draw = dont
C_RoofTop1.mount.elm_type = "dont_draw"
C_RoofTop2.draw = dont
C_RoofTop2.mount.elm_type = "dont_draw"
pure_cosmetic1 = Rooftop_mirror(name="RoofTop_Mirror")
pure_cosmetic1.draw_dict["mount_type"] = "rooftop_mirror_mount"
pure_cosmetic1.pos = (C_RoofTop1.pos + C_RoofTop2.pos ) / 2
pure_cosmetic1.normal = (C_RoofTop1.normal + C_RoofTop2.normal ) / 2
pure_cosmetic1.draw_dict["model_type"] = "Rooftop"
pure_cosmetic1.aperture = periscope_height
"""
# =============================================================================
# Four Gratings Compressor
# =============================================================================
Grat3 =Grating(grat_const=grating_const,order=1)
Grat3.pos = (Grat1.pos[0]-Grat2.pos[0]+Grat1.pos[0]-50-2*35*abs(Grat1.normal[0]),Grat2.pos[1],Grat2.pos[2])
Grat3.normal = (Grat1.normal[0],-Grat1.normal[1],Grat1.normal[2])
Grat4 =Grating(grat_const=grating_const,order=1)
Grat4.pos = (Grat2.pos[0]-Grat2.pos[0]+Grat1.pos[0]-50-2*35*abs(Grat1.normal[0]),Grat1.pos[1],Grat2.pos[2])
Grat4.normal = (Grat2.normal[0],-Grat2.normal[1],Grat2.normal[2])

Grat1.height=Grat2.height=Grat3.height=Grat4.height=25
Grat1.thickness=Grat2.thickness=Grat3.thickness=Grat4.thickness=9.5
Grat1.set_mount_to_default()
Grat2.set_mount_to_default()
Grat3.set_mount_to_default()
Grat4.set_mount_to_default()
Grat1.Mount.mount_list[1].flip(-90)
Grat2.Mount.mount_list[1].flip(-90)
Grat4.Mount.mount_list[-1]._lower_limit = Plane_height
Grat1.Mount.mount_list[-1]._lower_limit = Plane_height
Grat3.Mount.mount_list[-1]._lower_limit = Plane_height-23
Grat2.Mount.mount_list[-1]._lower_limit = Plane_height-23
Grat1.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat2.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat3.Mount.mount_list[1].model = "POLARIS-K1E3"
Grat4.Mount.mount_list[1].model = "POLARIS-K1E3"

print("setting pos=",(Grat1.pos+Grat2.pos+Grat3.pos+Grat4.pos)/4)
ip = Intersection_plane()
ip.pos -= (100,0,0)
Stretcher.add_fixed_elm(Grat1)
Stretcher.add_fixed_elm(Grat2)
Stretcher.add_fixed_elm(Grat3)
Stretcher.add_fixed_elm(Grat4)
"""
Stretcher.add_fixed_elm(C_RoofTop1)
Stretcher.add_fixed_elm(C_RoofTop2)
"""
# Stretcher.add_fixed_elm(ip_s)
Stretcher.add_fixed_elm(pure_cosmetic)
# Stretcher.add_fixed_elm(pure_cosmetic1)

# setting the final sequence and the last propagation for visualization
# note that pure cosmetic (pos6) is not in the sequence
# Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0,6,7,8,9,7,6,10]) #two Gratings Compressor
Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0,6,7,8,9])#8,9,10,11]) #four Gratings Compressor
# Stretcher.set_sequence([0, 1,2,3,2,1, 4,5, 1,2,3,2,1, 0]) #no compressor
Stretcher.recompute_optical_axis()
Stretcher.pos += (0,0,24)
Stretcher.propagate(500)
# ip=Intersection_plane()
# ip.set_geom(Stretcher.last_geom())
# ip.spot_diagram(Stretcher._beams[-1],aberration_analysis=True)
# ip.draw()
from LaserCAD.basic_optics import Gaussian_Beam
gb = Gaussian_Beam(radius=input_radius,angle=input_angle)
gb.wavelength = 2.3e-3
Stretcher.set_light_source(gb)
Stretcher.draw()
a = Pockels_Cell()
a.pos = (Grat1.pos+Grat4.pos)/2
a.pos-= (0,16,a.pos[2]-Plane_height+23)
a.normal = (0,1,0)
a.draw_dict["stl_file"]=thisfolder+"misc_meshes/XR25C.stl"
a.draw()
b = Table()
b.pos = (Grat1.pos+Grat4.pos)/2
b.pos-= (0,0,b.pos[2])
b.length = 780
b.width = 150
b.height = Plane_height-23
b.pos -= (b.length/2,b.width/2,0)
b.draw_dict["color"]= (0.2,0.2,0.2)
b.draw()

# c = Table()
# c.pos = (Grat1.pos+Grat4.pos)/2
# c.pos-= (0,0,c.pos[2]-20-30)
# c.length = 250
# c.width = 75
# c.height = 5.8
# c.pos -= (c.length/2,c.width/2,-c.height/2)
# c.draw()
# Stretcher.draw_beams()
# Stretcher.draw_elements()
# ip.spot_diagram(Stretcher._beams[-1],aberration_analysis=True)

# -----------------------------------------------------------------------------
# draw the spot diagram, 
# -----------------------------------------------------------------------------
# ip= Intersection_plane(name="the start of the Stretcher")
# ip_s.spot_diagram(Stretcher._beams[-1])
# ip.set_geom(Stretcher.get_geom())
# ip.spot_diagram(Stretcher._beams[0])
# # ip.spot_diagram(Stretcher._beams[14])
# ip.draw()
# ip_s.draw()
# pathlength = {}
# for ii in range(Stretcher._beams[0]._ray_count):
#   wavelength = Stretcher._beams[0].get_all_rays()[ii].wavelength
#   pathlength[wavelength] = 0
# for jj in range(len(Stretcher._beams)-1):
#   for ii in Stretcher._beams[jj].get_all_rays():
#     a=pathlength[ii.wavelength]
#     pathlength[ii.wavelength] = a +ii.length
    
# """
# add the optical path length in crystal
# """
# # Crystal_length = 10
# # for ii in range(Stretcher._beams[0]._ray_count):
# #     w1 = Stretcher._beams[0].get_all_rays()[ii].wavelength
# #     w = w1*1000
# #     n = np.sqrt(8.393 + 0.14383/(w**2-0.2421**2) + 4430.99/(w**2-36.71**2)) #ZnS
# #     # print(n)
# #     n = np.sqrt(2.2864 + 1.1280*(w**2)/(w**2 - 0.0562) - 0.0188*(w**2)) # RTP
# #     pathlength[w1] += n * Crystal_length
# # -----------------------------------------------------------------------------
# """
# calculate the GDD,TOD
# """
# ray_lam = [ray.wavelength for ray in Stretcher._beams[0].get_all_rays()]
# path = [pathlength[ii] for ii in ray_lam]
# path_diff = [ii-path[int(len(path)/2)] for ii in path]
# fai = [path_diff[ii]/ray_lam[ii]*2*np.pi for ii in range(len(path))]
# omega = [c0/ii*2*np.pi for ii in ray_lam]
# omega = [ii - c0/lambda_mid*2*np.pi for ii in omega]
# para = np.polyfit(omega, fai, 6)
# fai = [para[0]*ii**6 + para[1]*ii**5 + para[2]*ii**4 + para[3]*ii**3 + para[4]*ii**2 for ii in omega]
# fai2 = [30*para[0]*ii**4 + 20*para[1]*ii**3 + 12*para[2]*ii**2 + 6*para[3]*ii + 2*para[4] for ii in omega] # Taylor Expantion
# fai3 = [120*para[0]*ii**3 + 60*para[1]*ii**2 + 24*para[2]*ii + 6*para[3] for ii in omega]

# # para = np.polyfit(omega, fai, 5)
# # fai2 = [20*para[0]*ii**3 + 12*para[1]*ii**2 + 6*para[2]*ii + 2*para[3] for ii in omega] # Taylor Expantion
# # fai3 = [60*para[0]*ii**2 + 24*para[1]*ii + 6*para[2] for ii in omega]

# fai_function = interp1d(omega, fai)
# fai_new = fai_function(omega)

# # fai2_new=[derivative(fai_function, omega[ii],dx=1,n=2,order=5) for ii in range(1,len(omega)-1)]
# # fai3_new=[derivative(fai_function, omega[ii],dx=1,n=3,order=5) for ii in range(1,len(omega)-1)]

# delay_mid = path[int(len(path)/2)]/c0
# delay = [(pa/c0-delay_mid)*1E9 for pa in path]
# # plt.figure()
# # ax1=plt.subplot(1,2,1)
# # plt.plot(ray_lam,path)
# # plt.ylabel("pathlength (mm)")
# # plt.xlabel("wavelength (mm)")
# # plt.title("Pathlength at different wavelength")
# # plt.axhline(path[int(len(path)/2)], color = 'black', linewidth = 1)
# # ax2=plt.subplot(1,2,2)
# # plt.plot(ray_lam,delay)
# # plt.ylabel("delay (ns)")
# # plt.xlabel("wavelength (mm)")
# # plt.title("Delay at different wavelength")
# # plt.axhline(0, color = 'black', linewidth = 1)
# # plt.show()

# plt.figure()
# ax1=plt.subplot(1,3,1)
# plt.scatter(omega,fai,label="φ(ω)")
# plt.plot(omega,fai_new,label="φ(ω)")
# plt.title("Relationship of phase with angular frequency φ(ω)")
# plt.xlabel("angular frequency ω (rad/s)")
# plt.ylabel("wave phase φ (rad)")
# plt.axhline(fai[int(len(fai)/2)], color = 'black', linewidth = 1)
# ax2=plt.subplot(1,3,2)
# plt.plot(omega,fai2)
# # omega_d = omega
# # del omega_d[0]
# # del omega_d[-1]
# # plt.plot(omega_d,fai2_new)
# plt.title("Group delay dispersion")
# plt.xlabel("angular frequency ω (rad/s)")
# plt.ylabel("The second order derivative of φ(ω)")
# plt.axhline(fai2[int(len(fai2)/2)], color = 'black', linewidth = 1)
# print("Group delay dispersion at the center wavelength:",fai2[int(len(fai2)/2)])

# ax3=plt.subplot(1,3,3)
# plt.plot(omega,fai3)
# # plt.plot(omega_d,fai3_new)
# plt.title("Third order dispersion")
# plt.xlabel("angular frequency ω (rad/s)")
# plt.ylabel("The third order derivative of φ(ω)")
# plt.axhline(fai3[int(len(fai3)/2)], color = 'black', linewidth = 1)
# print("3rd order dispersion at the center wavelength:",fai3[int(len(fai3)/2)])


# # Stretcher.draw_beams()