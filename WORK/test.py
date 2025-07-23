# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:01:12 2024

@author: 12816
"""
from LaserCAD.freecad_models import freecad_da, clear_doc, setview
from LaserCAD import Composition, Beam, ThinBeamsplitter, Mirror, Composed_Mount, ThickBeamsplitter


if freecad_da:
  clear_doc()

# =============================================================================
# Michelson Interferometer with Thin Beamsplitter
# =============================================================================

startbeam = Beam(radius=1)
thinBS_t = ThinBeamsplitter(transmission=True)
# thinBS_t.set_mount(Composed_Mount(["KS1", "1inch_post"]))

invis_thinBS_r = ThinBeamsplitter(transmission=False, angle_of_incidence=0)
invis_thinBS_r.invisible = True
invis_thinBS_r.Mount.invisible = True


michelson_thin = Composition(name="MichelsonThinBS")
michelson_thin.propagate(75)
michelson_thin.add_on_axis(thinBS_t)
michelson_thin.propagate(80)
michelson_thin.add_on_axis(Mirror())
michelson_thin.propagate(80)
invis_thinBS_r.set_geom(thinBS_t.get_geom())
michelson_thin.add_fixed_elm(invis_thinBS_r)
michelson_thin.recompute_optical_axis()
michelson_thin.propagate(100)


mir = Mirror()
mir.set_geom(thinBS_t.get_geom())
mthin_arm2_ls = mir.next_beam(startbeam)
mthin_arm2_ls.draw_dict["color"] = (1.0, 0.3, 0.0)

invis_thinBS_t = ThinBeamsplitter(transmission=True, angle_of_incidence=0)
invis_thinBS_t.invisible = True
invis_thinBS_t.Mount.invisible = True
invis_thinBS_t.set_geom(thinBS_t.get_geom())

mthin_arm2 = Composition()
mthin_arm2.set_geom(mthin_arm2_ls.get_geom())
mthin_arm2.set_light_source(mthin_arm2_ls)
mthin_arm2.propagate(90)
mthin_arm2.add_on_axis(Mirror())
mthin_arm2.propagate(90)
mthin_arm2.add_fixed_elm(invis_thinBS_t)
mthin_arm2.recompute_optical_axis()
mthin_arm2.propagate(100)


michelson_thin.draw()
mthin_arm2.draw()



# =============================================================================
# Mach Zehnder
# =============================================================================
mzpos = (300, 100, 90)
mz_firstprop = 70
mz_horiz = 180
mz_vert = 80
mz_lastprop = 75

machzehnder1 = Composition(name="MachZehnder")
machzehnder1.pos = mzpos
machzehnder1.propagate(mz_firstprop)
machzehnder1.add_on_axis(ThinBeamsplitter(transmission=True, angle_of_incidence=-45))
machzehnder1.propagate(mz_horiz)
machzehnder1.add_on_axis(Mirror(phi=-90))
machzehnder1.propagate(mz_vert)
machzehnder1.add_on_axis(ThinBeamsplitter(transmission=False, angle_of_incidence=45))
machzehnder1.propagate(mz_lastprop)

mz_arm2_bs1 = ThinBeamsplitter(transmission=False, angle_of_incidence=-45)
mz_arm2_bs1.invisible = True
mz_arm2_bs1.Mount.invisible = True

mz_arm2_bs2 = ThinBeamsplitter(transmission=True, angle_of_incidence=-45)
mz_arm2_bs2.invisible = True
mz_arm2_bs2.Mount.invisible = True

mach_arm2 = Composition()
mach_arm2.set_geom(machzehnder1.get_geom())
mach_arm2.propagate(mz_firstprop)
mach_arm2.add_on_axis(mz_arm2_bs1)
mach_arm2.propagate(mz_vert)
mach_arm2.add_on_axis(Mirror(phi=+90))
mach_arm2.propagate(mz_horiz)
mach_arm2.add_on_axis(mz_arm2_bs2)
mach_arm2.propagate(mz_lastprop)

machzehnder1.draw()
mach_arm2.draw()

# # =============================================================================
# # Michelson Interferometer with Thick Beamsplitter
# # =============================================================================

# startbeam = Beam(radius=1)
# thickBS_t = ThickBeamsplitter(transmission=True)
# # thickBS_t.set_mount(Composed_Mount(["KS1", "1inch_post"]))

# invis_thickBS_r = ThickBeamsplitter(transmission=False, angle_of_incidence=0)
# invis_thickBS_r.invisible = True
# invis_thickBS_r.Mount.invisible = True


# michelson_thick = Composition(name="MichelsonthickBS")
# michelson_thick.propagate(75)
# michelson_thick.add_on_axis(thickBS_t)
# michelson_thick.propagate(80)
# michelson_thick.add_on_axis(Mirror())
# michelson_thick.propagate(80)
# invis_thickBS_r.set_geom(thickBS_t.get_geom())
# michelson_thick.add_fixed_elm(invis_thickBS_r)
# michelson_thick.recompute_optical_axis()
# michelson_thick.propagate(100)


# mir = Mirror()
# mir.set_geom(thickBS_t.get_geom())
# mthick_arm2_ls = mir.next_beam(startbeam)
# mthick_arm2_ls.draw_dict["color"] = (1.0, 0.3, 0.0)

# invis_thickBS_t = ThickBeamsplitter(transmission=True, angle_of_incidence=0)
# invis_thickBS_t.invisible = True
# invis_thickBS_t.Mount.invisible = True
# invis_thickBS_t.set_geom(thickBS_t.get_geom())

# mthick_arm2 = Composition()
# mthick_arm2.set_geom(mthick_arm2_ls.get_geom())
# mthick_arm2.set_light_source(mthick_arm2_ls)
# mthick_arm2.propagate(90)
# mthick_arm2.add_on_axis(Mirror())
# mthick_arm2.propagate(90)
# mthick_arm2.add_fixed_elm(invis_thickBS_t)
# mthick_arm2.recompute_optical_axis()
# mthick_arm2.propagate(100)


# michelson_thick.pos += (200, 50, 0)
# mthick_arm2.pos += (200, 50, 0)

# michelson_thick.draw()
# mthick_arm2.draw()



if freecad_da:
  setview()