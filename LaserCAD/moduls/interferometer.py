#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 11:20:33 2025

@author: clemens
"""

from LaserCAD import Beam, ThinBeamsplitter, Mirror, Rectangular_Thin_Beamsplitter, Multi_Beamline_Composition

# =============================================================================
# Michelson Interferometer with Thin Beamsplitter
# =============================================================================

def Make_Michelson_Interferometer():
  startbeam = Beam(radius=1)
  thinBS_t = Rectangular_Thin_Beamsplitter(transmission=True)
  # thinBS_t.set_mount(Composed_Mount(["KS1", "1inch_post"]))

  invis_thinBS_r = ThinBeamsplitter(transmission=False, angle_of_incidence=0)
  invis_thinBS_r.invisible = True
  invis_thinBS_r.Mount.invisible = True


  michelson_thin = Multi_Beamline_Composition(name="MichelsonThinBS")
  michelson_thin.set_light_source(startbeam)
  michelson_thin.propagate(75)
  michelson_thin.add_on_axis(thinBS_t)
  michelson_thin.propagate(80)
  michelson_thin.add_on_axis(Mirror())
  michelson_thin.propagate(80)
  invis_thinBS_r.set_geom(thinBS_t.get_geom())
  michelson_thin.add_fixed_elm(invis_thinBS_r)
  michelson_thin.recompute_optical_axis()
  michelson_thin.propagate(100)

  michelson_thin.compute_beams()

  michelson_thin.add_new_line(thinBS_t.get_alternative_beam())

  invis_thinBS_t = ThinBeamsplitter(transmission=True, angle_of_incidence=0)
  invis_thinBS_t.invisible = True
  invis_thinBS_t.Mount.invisible = True
  invis_thinBS_t.set_geom(thinBS_t.get_geom())

  michelson_thin.propagate(90)
  michelson_thin.add_on_axis(Mirror())
  michelson_thin.propagate(90)
  michelson_thin.add_fixed_elm(invis_thinBS_t)
  michelson_thin.recompute_optical_axis()
  michelson_thin.propagate(100)
  return michelson_thin



# # =============================================================================
# # Mach Zehnder
# # =============================================================================

def Make_Machzehnder_Interferometer():
  mz_firstprop = 70
  mz_horiz = 180
  mz_vert = 80
  mz_lastprop = 75

  first_BS = Rectangular_Thin_Beamsplitter(transmission=True, angle_of_incidence=-45, height=25, width=40)
  second_BS = Rectangular_Thin_Beamsplitter(transmission=False, angle_of_incidence=+45, height=25, width=40)

  machzehnder1 = Multi_Beamline_Composition(name="MachZehnder")
  # machzehnder1.pos = mzpos
  machzehnder1.propagate(mz_firstprop)
  machzehnder1.add_on_axis(first_BS)
  machzehnder1.propagate(mz_horiz)
  machzehnder1.add_on_axis(Mirror(phi=-90))
  machzehnder1.propagate(mz_vert)
  machzehnder1.add_on_axis(second_BS)
  machzehnder1.propagate(mz_lastprop)

  # mz_arm2_bs1 = ThinBeamsplitter(transmission=False, angle_of_incidence=-45)
  # mz_arm2_bs1.invisible = True
  # mz_arm2_bs1.Mount.invisible = True

  mz_arm2_bs2 = ThinBeamsplitter(transmission=True, angle_of_incidence=-45)
  mz_arm2_bs2.invisible = True
  mz_arm2_bs2.Mount.invisible = True

  machzehnder1.compute_beams()
  machzehnder1.add_new_line(first_BS.get_alternative_beam())

  # machzehnder1.propagate(mz_firstprop)
  # machzehnder1.add_on_axis(mz_arm2_bs1)
  machzehnder1.propagate(mz_vert)
  machzehnder1.add_on_axis(Mirror(phi=+90))
  machzehnder1.propagate(mz_horiz)
  machzehnder1.add_on_axis(mz_arm2_bs2)
  machzehnder1.propagate(mz_lastprop)

  # machzehnder1.draw()
  # mach_arm2.draw()
  return machzehnder1






# from LaserCAD import Composition

# def Make_Michelson_Interferomter_old():
#   startbeam = Beam(radius=1)
#   thinBS_t = ThinBeamsplitter(transmission=True)
#   # thinBS_t.set_mount(Composed_Mount(["KS1", "1inch_post"]))

#   invis_thinBS_r = ThinBeamsplitter(transmission=False, angle_of_incidence=0)
#   invis_thinBS_r.invisible = True
#   invis_thinBS_r.Mount.invisible = True


#   michelson_thin = Composition(name="MichelsonThinBS")
#   michelson_thin.propagate(75)
#   michelson_thin.add_on_axis(thinBS_t)
#   michelson_thin.propagate(80)
#   michelson_thin.add_on_axis(Mirror())
#   michelson_thin.propagate(80)
#   invis_thinBS_r.set_geom(thinBS_t.get_geom())
#   michelson_thin.add_fixed_elm(invis_thinBS_r)
#   michelson_thin.recompute_optical_axis()
#   michelson_thin.propagate(100)


#   mir = Mirror()
#   mir.set_geom(thinBS_t.get_geom())
#   mthin_arm2_ls = mir.next_beam(startbeam)
#   mthin_arm2_ls.draw_dict["color"] = (1.0, 0.3, 0.0)

#   invis_thinBS_t = ThinBeamsplitter(transmission=True, angle_of_incidence=0)
#   invis_thinBS_t.invisible = True
#   invis_thinBS_t.Mount.invisible = True
#   invis_thinBS_t.set_geom(thinBS_t.get_geom())

#   mthin_arm2 = Composition()
#   mthin_arm2.set_geom(mthin_arm2_ls.get_geom())
#   mthin_arm2.set_light_source(mthin_arm2_ls)
#   mthin_arm2.propagate(90)
#   mthin_arm2.add_on_axis(Mirror())
#   mthin_arm2.propagate(90)
#   mthin_arm2.add_fixed_elm(invis_thinBS_t)
#   mthin_arm2.recompute_optical_axis()
#   mthin_arm2.propagate(100)


#   # michelson_thin.draw()
#   # mthin_arm2.draw()
#   return michelson_thin, mthin_arm2


# # =============================================================================
# # Mach Zehnder
# # =============================================================================
# def Make_Machzehnder_Interferometer_old():
#   mzpos = (300, 100, 90)
#   mz_firstprop = 70
#   mz_horiz = 180
#   mz_vert = 80
#   mz_lastprop = 75

#   machzehnder1 = Composition(name="MachZehnder")
#   machzehnder1.pos = mzpos
#   machzehnder1.propagate(mz_firstprop)
#   machzehnder1.add_on_axis(ThinBeamsplitter(transmission=True, angle_of_incidence=-45))
#   machzehnder1.propagate(mz_horiz)
#   machzehnder1.add_on_axis(Mirror(phi=-90))
#   machzehnder1.propagate(mz_vert)
#   machzehnder1.add_on_axis(ThinBeamsplitter(transmission=False, angle_of_incidence=45))
#   machzehnder1.propagate(mz_lastprop)

#   mz_arm2_bs1 = ThinBeamsplitter(transmission=False, angle_of_incidence=-45)
#   mz_arm2_bs1.invisible = True
#   mz_arm2_bs1.Mount.invisible = True

#   mz_arm2_bs2 = ThinBeamsplitter(transmission=True, angle_of_incidence=-45)
#   mz_arm2_bs2.invisible = True
#   mz_arm2_bs2.Mount.invisible = True

#   mach_arm2 = Composition()
#   mach_arm2.set_geom(machzehnder1.get_geom())
#   mach_arm2.propagate(mz_firstprop)
#   mach_arm2.add_on_axis(mz_arm2_bs1)
#   mach_arm2.propagate(mz_vert)
#   mach_arm2.add_on_axis(Mirror(phi=+90))
#   mach_arm2.propagate(mz_horiz)
#   mach_arm2.add_on_axis(mz_arm2_bs2)
#   mach_arm2.propagate(mz_lastprop)

#   machzehnder1.draw()
#   mach_arm2.draw()
#   return machzehnder1, mach_arm2
