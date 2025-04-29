#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 00:27:52 2024

@author: mens
"""

import numpy as np
from LaserCAD.basic_optics import Mirror, Composition, Lens, Beam, Composed_Mount
from LaserCAD.non_interactings import Lambda_Plate
from LaserCAD.freecad_models import freecad_da, clear_doc, setview

if freecad_da:
  clear_doc()






from LaserCAD.basic_optics import Curved_Mirror, LinearResonator
from LaserCAD.non_interactings import Pockels_Cell, Crystal
# =============================================================================
# even simpler Res
# =============================================================================
# calculus
# A_target = 4.908738521234052 #from gain simlutation area in mm^2
focal = 2500
lam_mid = 2.4e-3
inch = 25.4
# A_natural = lam_mid * focal
# geometrie_factor = A_target / A_natural
total_length = focal / 2
tfp_push_aside = 5 # distance in mm to push the TFP aside, so that the beam can pass through

# design params
width_pz = 80
dist_mir_pz = 20 + width_pz
dist_pz_lambda = 115 - width_pz
dist_lambda_tfp = 70
dist_tfp_fold1 = 65
# dist_fold1_fold2 = 300
dist_crystal_end = 20
last = total_length - dist_mir_pz - dist_pz_lambda - dist_lambda_tfp -dist_tfp_fold1
tfp_aperture = 2*inch
tfp_angle = 65
tfp_thickness = 6.35


# optics

cm0 = Curved_Mirror(radius=focal*2, phi = 180, name="Curved_Far")
mir1 = Mirror(phi=180 + 7, name="Dichroit")
mir1.aperture = 0.5 * inch
mir1.set_mount_to_default()

TFP_Amp1 = Mirror(phi= 180 - 2*tfp_angle, name="TFP_Amp1")
TFP_Amp1.draw_dict["color"] = (1.0, 0.0, 2.0)
TFP_Amp1.aperture = tfp_aperture
TFP_Amp1.thickness = tfp_thickness
TFP_Amp1.set_mount_to_default()
pol_mount = TFP_Amp1.Mount.mount_list[0]
pol_mount.flip()
# TFP_Amp1.mount_dict["Flip90"]=True

cm = Curved_Mirror(radius=focal*2, phi = 180, name="Curved_PZ")
PockelsCell = Pockels_Cell(name="PockelZelleRes1")
Lambda_Regen = Lambda_Plate()
fold1 = Mirror(phi=90)


simres = LinearResonator(name="Regen")
simres.set_wavelength(lam_mid)

simres.add_on_axis(cm0)
simres.propagate(total_length)

simres.add_on_axis(mir1)

simres.propagate(dist_crystal_end)
laser_crys = Crystal(width=6, thickness=10, n=2.45)
simres.add_on_axis(laser_crys)

simres.propagate(last-dist_crystal_end)

simres.add_on_axis(fold1)

simres.propagate(dist_tfp_fold1)

simres.add_on_axis(TFP_Amp1)
# x,y,z = TFP_Amp1.get_coordinate_system()
# TFP_Amp1.pos += y * tfp_push_aside

simres.propagate(dist_lambda_tfp)

simres.add_on_axis(Lambda_Regen)

simres.propagate(dist_pz_lambda)

simres.add_on_axis(PockelsCell)

simres.propagate(dist_mir_pz)

simres.add_on_axis(cm)

simres.compute_eigenmode()

# PockelsCell.rotate(PockelsCell.normal, np.pi/2)


# Amplifier_I = Make_Amplifier_I()
Amplifier_I = simres
# Amplifier_I.set_input_coupler_index(1, False)
# ppos, paxes = Pump.last_geom()

Amplifier_I.set_input_coupler_index(1)
# Amplifier_I.set_geom(Pump.last_geom())
# Amplifier_I.pos = ppos

# =============================================================================
# Amp1 Mode
# =============================================================================
amp_len = [x.length  for x in Amplifier_I._optical_axis]
s1 = amp_len[5]
s2 = sum(amp_len[6::])


def MatProp(x):
  mat = np.eye(2)
  mat[0,1] = x
  return mat

def MatCm(R):
  mat = np.eye(2)
  mat[1,0] = -2/R
  return mat

MatRes = MatProp(s2) @ MatCm(2*focal) @ MatProp(s2) @ MatProp(s1) @ MatCm(2*focal) @ MatProp(s1)

[[A,B], [C,D]] = MatRes

z2 = (A-D) / 2 / C
r2 = abs(1/2/C) * np.sqrt(4 - (A+D)**2)



# =============================================================================
# complicated calculation for compensation
# =============================================================================
PropA = 1695.724204685186

adapt_focal = 1029

a = PropA
f = adapt_focal
r1 = 2.5**2 * np.pi / 4 / 2.4e-3

v = r1/r2
al = 1 - a/f
ph = 1/f

p = al / (al**2 + ph**2 * r1**2)
q = (1-v) / (al**2 + ph**2 * r1**2)

x1 = -p + np.sqrt(p**2 - q)
x2 = -p - np.sqrt(p**2 - q)
x = x1

def bet(x):
  nen = (1 + al*x)**2 + (ph*x*r1)**2
  return (z2*nen +f*al*(1+al*x) + ph*x*r1**2) / ((1+al*x)**2*f + ph*x**2*r1**2 ) * -1

delta = x*f
beta = bet(x)
b = f*(1-beta )


# Test
L = 2*f + delta

def Kogel(mat, q):
  return (mat[0,0]*q + mat[0,1]) / (mat[1,0]*q + mat[1,1])

q1 = 0 + 1j*r1
q2 = z2 + 1j*r2

mattele = MatProp(b) @ MatCm(2*f) @ MatProp(2*f+delta) @MatCm(2*f) @ MatProp(a)

print("q1", q1)
print("q2", q2)
print("Kogelnik", Kogel(mattele, q1))

print()
print("delta:", delta)
print("b:", b)
 

def complete_solver_del_b(a=1695.7, f=1029, r1=2045.3, r2=2165, z2=1045):
  v = r1/r2
  al = 1 - a/f
  ph = 1/f
  
  p = al / (al**2 + ph**2 * r1**2)
  q = (1-v) / (al**2 + ph**2 * r1**2)
  
  x1 = -p + np.sqrt(p**2 - q)
  x2 = -p - np.sqrt(p**2 - q)
  x = x1
  
  bet1 = (z2*v +f*al*(1+al*x) + ph*x*r1**2) / ((1+al*x)**2*f + ph*x**2*r1**2 ) * -1
  
  x = x2
  bet2 = (z2*v +f*al*(1+al*x) + ph*x*r1**2) / ((1+al*x)**2*f + ph*x**2*r1**2 ) * -1
  
  delta1 = x1*f
  delta2 = x2*f
  b1 = f*(1-bet1)
  b2 = f*(1-bet2)
  return [(delta1, b1), (delta2, b2)]

a = np.linspace(PropA*0.9, PropA*1.5, 2000)

[(delta1, b1), (delta2, b2)] = complete_solver_del_b(a=a)


# =============================================================================
# AdaptTeles
# =============================================================================


AdaptTeles = Composition()

AdaptTeles.propagate(70)
AdaptTeles.add_on_axis(Mirror(phi=-90))
AdaptTeles.propagate(100)

L1 = Lens(f=adapt_focal)
AdaptTeles.add_on_axis(L1)
L1.pos += L1.get_coordinate_system()[1]*-7.5
AdaptTeles.recompute_optical_axis()
AdaptTeles.propagate(adapt_focal + delta/2)

M_tele = Mirror()
AdaptTeles.add_on_axis(M_tele)
M_tele.normal = L1.normal

AdaptTeles.set_sequence([0,1,2,1])
AdaptTeles.recompute_optical_axis()
AdaptTeles.propagate(50)
M_tele2 = Mirror(phi = -90)
M_tele2.set_mount(Composed_Mount(unit_model_list=["MH25_KMSS", "1inch_post"]))
AdaptTeles.add_on_axis(M_tele2)
AdaptTeles.propagate(130)

AdaptTeles._lightsource.draw_dict["model"] = "ray_group" 
 
# =============================================================================
# Draw selection
# =============================================================================
AdaptTeles.draw_elements()
AdaptTeles.draw_mounts()
AdaptTeles.draw_beams()


if freecad_da:
  setview()