from ..basic_optics import Component, Unit_Mount, Composed_Mount, Post
from ..freecad_models.utils import thisfolder, load_STL

class Spectrometer(Component):
  def __init__(self, name="Ocean Optics spectrometer", model="SR", **kwargs):
    self.model = model
    super().__init__(name, **kwargs)
    """
    Spectrometer class for LaserCAD.
    
    params: model: str, choose between "SR" and "HR" for different spectrometer models.
    """
    stl_file = thisfolder+f"misc_meshes/OceanOptics_{model}_spectrometer.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(0.1, 0.1, 0.1)
    self.freecad_model = load_STL
    self.set_mount_to_default()

  def set_mount_to_default(self):
    invis_adapter = Unit_Mount()

    if self.model == "SR":
        invis_adapter.docking_obj.pos += (28, 19.8, -10.8)
    elif self.model == "HR":
        invis_adapter.docking_obj.pos += (32.0, 22, -18)
    comp = Composed_Mount(name=self.name + "_mount")
    comp.add(invis_adapter)
    comp.add(Post(model="0.5inch_post"))
    # comp.add(Post())
    comp.set_geom(self.get_geom())
    self.Mount = comp