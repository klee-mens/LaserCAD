from .. basic_optics import ThinBeamsplitter, Composition, Component, Unit_Mount, Composed_Mount, Post
from .. freecad_models.utils import load_STL

import numpy as np


class Motorized_TSF(Composition):
    def __init__(self, name="Motorized_TSF", flip=False, **kwargs):
        """Creates a motorized filter holder with two mirrors (non-interacting) and a housing.
        
        Attributes:
            name (str): Name of the motorized filter holder
            path_length (float): Total beam path length of the motorized filter holder. 
            geometric_length (float): Geometric distance between input and output of the motorized filter holder.
            length_diff (float): Difference between path length and geometric length.
            flip (bool): If True, the motorized filter holder is flipped along the y-axis.
        """
        self.flip = flip
        flip_factor = -1 if flip else 1
        super().__init__(name=name,**kwargs)
        self.name = name 
        self.geometric_length = 67.2

        TBS1 = ThinBeamsplitter(name="Motorized_TSF 1", angle_of_incidence=-30*flip_factor)
        TBS2 = ThinBeamsplitter(name="Motorized_TSF 2", angle_of_incidence=30*flip_factor)

        TBS1.pos += (13.5, 0, 0) 
        TBS2.pos += (51, 1.8*flip_factor, 0) 

        self.add_on_axis(self.add_housing())
        self.add_fixed_elm(TBS1)
        self.add_fixed_elm(TBS2)
        

    def add_housing(self):
        Housing = Unit_Mount("Spiegelhalter_160021_V1")
        
        Rotator_box = Composed_Mount()
        Rotator_box.add(Housing)
        Rotator_box.add(Post())
        Rotator_housing=Component()
        Rotator_housing.draw_dict["stl_file"]="dont_draw"
        Rotator_housing.freecad_model = load_STL
        Rotator_housing.Mount = Rotator_box
        if self.flip: 
            Rotator_housing.Mount.reverse()
            Rotator_housing.Mount.pos += (self.geometric_length-5, 0, 0)
    
        return Rotator_housing