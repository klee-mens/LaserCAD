from .. basic_optics import Mirror, Composition, Component, Unit_Mount, Composed_Mount, Post
from .. freecad_models.utils import load_STL

import numpy as np

class Polarization_Rotator(Composition):
    def __init__(self, name="Polarisationsdreher", **kwargs):
        """Creates a polarization rotator with three mirrors and a housing.
        The mirrors are arranged in a way that the beam polarization is rotated by 90 degrees.
        
        Attributes:
            name (str): Name of the polarization rotator.
            path_length (float): Total beam path length of the polarization rotator. 
            geometric_length (float): Geometric distance between input and output of the polarization rotator.
            length_diff (float): Difference between path length and geometric length.
            PDM1 (Mirror): First mirror in the polarization rotator.
            PDM2 (Mirror): Second mirror in the polarization rotator.
            PDM3 (Mirror): Third mirror in the polarization rotator.
        """
        super().__init__(name=name,**kwargs)
        self.name = name 
        sep = 28.3
        PD_theta = 45*np.pi/180
        L = 80.3
        start_length = 14.496

        self.path_length = 192.066
        self.geometric_length = sep + 2*start_length
        self.length_diff = self.path_length- self.geometric_length

        PDM1 = Mirror(name="Polarisationsdreher M1")
        PDM2 = Mirror(name="Polarisationsdreher M2")
        PDM3 = Mirror(name="Polarisationsdreher M3")
        PDM2.pos += (start_length + sep/2, L*np.cos(PD_theta), L*np.sin(PD_theta))
        PDM3.pos += (start_length + sep,0,0)

        self.add_on_axis(self.add_housing())
        self.propagate(start_length)
        self.add_on_axis(PDM1)
        PDM1.set_normal_with_2_points(self.pos-(1,0,0), PDM2.pos)
        self.add_fixed_elm(PDM2)
        PDM2.set_normal_with_2_points(PDM1.pos, PDM3.pos)
        self.add_fixed_elm(PDM3)
        PDM3.set_normal_with_2_points(PDM2.pos, PDM3.pos + (1,0,0))
        self.propagate(start_length)

        PDM1.set_mount(Unit_Mount())
        PDM2.set_mount(Unit_Mount())
        PDM3.set_mount(Unit_Mount())

    def add_housing(self):
        Housing = Unit_Mount("Polarization_rotator-Fusion")
        Housing.draw_dict["color"]=(239/255, 239/255, 239/255)
        Housing.docking_obj.pos += (28.65,38.89, -41.89)
        Housing.docking_obj.normal = (0,0,1)

        Rotator_box = Composed_Mount()
        Rotator_box.add(Housing)
        Rotator_box.add(Post())
        Rotator_housing=Component()
        Rotator_housing.draw_dict["stl_file"]="dont_draw"
        Rotator_housing.freecad_model = load_STL
        Rotator_housing.Mount = Rotator_box

        return Rotator_housing