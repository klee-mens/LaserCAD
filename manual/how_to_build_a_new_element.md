# How to build new shapes and elements

In this section we will go through some examples to create custom shapes for
objects, mounts and optical elements. Let's start with an easy example:

## Inserting a Detector

In the beginning we need of course a suitalbe 3D fromat file that describes the
shape of our detector. I recommend stl files since they are universal and quick
to load, however they contain only surface information and no color, so we need
to add that afterwards. Step files are also possible to import in FreeCAD, but
you have to wirte your own function. A possible start you can find in
*freecad_models/utils.p*.
For this example we will take the [PDA10A2](https://www.thorlabs.com/thorproduct.cfm?partnumber=PDA10A2)
Detector. Thorlabs provide a step file for this, which needs to be adjusted in
FreeCAD like this:

<img src="images/How-to-new-Element/Step_Alignment.png" alt="StretcherStuff" title="" />

The rules for aligning are:
1. The point where the object shall get hit by the beam is (0,0,0), see the
red sphere.
2. The object shall face the -x direction.
3. Its vertical direction shall be aligned with the z-axis.

Now you can export the object from FreeCAD as step or stl file, in this case
as "Diode.stl" and save it under freecad_models/misc_meshes.
Now we have to bind our new shape to an object and for the beginning we choose
a Geom_Obj.
Here is the usual header:
```python
import sys
pfad = __file__
pfad = pfad.replace("\\","/") #folder conventions windows linux stuff
pfad = pfad.lower()
ind = pfad.rfind("lasercad")
pfad = pfad[0:ind-1]
if not pfad in sys.path:
  sys.path.append(pfad)
```
And here the actual code to bind the shape:
```python
from LaserCAD.basic_optics import Geom_Object
from LaserCAD.freecad_models.utils import freecad_da, clear_doc, setview, load_STL, thisfolder

if freecad_da:
  clear_doc()

stl_file = thisfolder+"misc_meshes/pockels_cell_easy_steal-Body.stl"

detector = Geom_Object()
detector.freecad_model = load_STL
detector.draw_dict["stl_file"]=stl_file
detector.draw()

if freecad_da:
  setview()
```
First you need to set the *freecad_model* to *load_stl*. Be aware that this line
conects a function pointer to the *freecad_model*, so don't use brackets after
the names, we really want to set the value *freecad_model* to a function, not to
its result. Afterwards we set the *draw_dict* entry for *stl_file* to the path
where we saved the stl file. You can see the result of this in the following
terminal snippet:

<img src="images/How-to-new-Element/Geom_obj_draw_dict_terminal.png" alt="StretcherStuff" title="" />

Fine, now we cn add a beam to the scenary, set the detector to its and and look
at the result in FreeCAD. Code and output looks like this:
```python
from LaserCAD.basic_optics import Geom_Object, Beam
from LaserCAD.freecad_models.utils import freecad_da, clear_doc, setview, load_STL, thisfolder

if freecad_da:
  clear_doc()

stl_file = thisfolder+"misc_meshes/Diode.stl"

detector = Geom_Object()
detector.freecad_model = load_STL
detector.draw_dict["stl_file"]=stl_file

b = Beam()
b.set_length(100)
detector.pos += (100,0,0)
b.draw()
detector.draw()

if freecad_da:
  setview()
```

<img src="images/How-to-new-Element/Geom_Obj_stl_with_beam.png" alt="StretcherStuff" title="" />

As I said hte stl format is quick, but unfortunately does not provide colours.
We can give it one by adding this line, to change the draw_dict once more:
```pyhon
detector.draw_dict["color"]=(0.1, 0.1, 0.1)
```
Like this we can give the shape a colour in RGB values going from 0.0 to 1.0.
Et voila, the black detector:

<img src="images/How-to-new-Element/Geom_Obj_stl_with_beam_BLACK.png" alt="StretcherStuff" title="" />

Now that we have the shape bound to an Geom_Object, we can place it where ever
we want via the *set_geom* funciton or with *pos* and *normal*.

If we need multiple detectors, we can now of course copy paste these lines over
and over, nevertheless more elegant would be to define an own class for this.
The follwoing code shows how:
```python
class Detector(Geom_Object):
  def __init__(self, name="Det_PDA10A2", **kwargs):
    super().__init__(name, **kwargs)
    stl_file = thisfolder+"misc_meshes/Diode.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(0.1, 0.1, 0.1)
    self.freecad_model = load_STL
```
You see, that it is not really much more effort, to make it directly a class.
Now that we have it, we can start playing aaround and creating multiple instanses
like this
```python
detector = Detector()
detector.pos += (100,0,0)
detector.draw()

detector2 = Detector()
detector2.pos += (0,50,0)
detector2.normal = (-3,1,0)
detector2.draw()

b = Beam()
b.set_length(100)
b.draw()
```

Resulting in a 3D model like this:

<img src="images/How-to-new-Element/Geom_obj_2_instanses.png" alt="StretcherStuff" title="" />

To include our new element in a real setup (= a *composition*), we ave to give
it a suitable mount and post, thus making it a *Component*. Only this would not
change much, each Component has a standard *Unit_Mount*, but those are more like
abstract templates of mounts, providing all the theoretical member variables and
functions, but no useful drawing function. For this we have to override the
*set_mount_to_default* function and define an invisble Unit_Mount to define the
docking position of the half_inch_post. For more information about mounts and
docking positions you can read the Custom Mirror Mount section. The code and
output look now like this.
```pyhton
from LaserCAD.basic_optics import Geom_Object, Beam, Component
from LaserCAD.basic_optics import Composed_Mount, Unit_Mount, Post
from LaserCAD.freecad_models.utils import freecad_da, clear_doc, setview, load_STL, thisfolder

if freecad_da:
  clear_doc()

class Detector(Component):
  def __init__(self, name="Det_PDA10A2", **kwargs):
    super().__init__(name, **kwargs)
    stl_file = thisfolder+"misc_meshes/Diode.stl"
    self.draw_dict["stl_file"]=stl_file
    self.draw_dict["color"]=(0.1, 0.1, 0.1)
    self.freecad_model = load_STL
    self.set_mount_to_default()

  def set_mount_to_default(self):
    invis_adapter = Unit_Mount()
    invis_adapter.docking_obj.pos += (10.5, 0, -25)
    comp = Composed_Mount(name=self.name + "_mount")
    comp.add(invis_adapter)
    comp.add(Post(model="0.5inch_post"))
    # comp.add(Post())
    comp.set_geom(self.get_geom())
    self.Mount = comp

detector = Detector()
detector.draw()
detector.draw_mount()
```

The magic of the post drawing algorithms will nor care, that the post will grow
according to the z-height of the detector. You can play araound with the detector
*pos* to see how it works.

<img src="images/How-to-new-Element/Detector_with_post.png" alt="StretcherStuff" title="" />


## Custom Mirror Mount - The Spartan

The goal of this section is to understand how to create a new mount and what
are its defining properties. For this we first chose a very random shape, that
we want to use as a mirror mount. In this case I looked on [Yeggi](https://www.yeggi.com)
for a stl file and dragged it into FreeCAD. Thanks to the guys there designing
these models and offer them for free!
Next we have to align them. For any Mount, not matter if Composed or not, there
are 3 important positions:
One is where the Mount should touch a mirror, the other is the docking position.
The docking object is an geometrical object, describing where and in which
direction the next Mount or post shall dock on the previous Mount.
To test and align this, we will create a mirror at (0,0,0) and drag a little
blue test sphere to the docking position. In this case the docking position
looks best, when the sphere is placed at (24, 2, -35). In the following screen
shot you can see the stl file alligned manually to an (0,0,0) mirror together
with an (0,0,0) red sphere and the blue docking sphere.

<img src="images/How-to-new-Element/Spartan_alignement.png" alt="StretcherStuff" title="" />

Note that the default normal of a mirror also points in (1,0,0) direction and
the mount has to be placed behind so in fact our spartan faces the (-1,0,0)
direction with his shield, as all mirror mounts do in default position.

That was the modelling part, now comes the coding. We now start directly making
our spartan an universal class. For this we will inherit from the *Unit_Mount*
class to get all the member functions and override the docking position with
our derived docking position.
```python
class Spartan_Mount(Unit_Mount):
  def __init__(self):
    super().__init__()
    self.model = "Spartan"
    self.path = thisfolder + "misc_meshes/"
    self.docking_obj.pos += (24, 2, -35) # from manual adjustments in FreeCAD
```

Let's see how this turns out with a test mirror. For this we simply bind a new
instance of our Unit_Mount to the mirror with the *set_mount* function.

```python
mir = Mirror()
mir.set_mount(Spartan_Mount())
mir.draw()
mir.draw_mount()
```

The result looks pretty similar, but be aware, that hte mount now follows the
mirror position and direction, (0,0,80) in this case.
Fine, but in a real setup we would quickly notice, that the mount is most of
the times freely floating in hte air. A proper post is needed. Posts are in its
idea also just unit mounts, but with the property to be always straight in z -
direction and having an *_lower_limit* which is 0 by default and indicates the
ground level to which the post will extend, due to He Z. functions. For some
purposes the limit could be set higher, e.g. when working with a base bread bord
plate. To bring spartan and post toegether we have to define a *Composed_Mount*,
like it is done in the following code.
```python
class Spartan_Mount(Composed_Mount):
  def __init__(self):
    super().__init__()
    um = Unit_Mount()
    um.model = "Spartan"
    um.path = thisfolder + "misc_meshes/"
    um.docking_obj.pos += (24, 2, -35) # from manual adjustments in FreeCAD
    self.add(um)
    self.add(Post())
```

As you see, in its constructor 2 unit mounts are defined: our old spartan and
than a simple default Post, which is one inch in diameter. For the half inch post
you may have a look in the previous section. The *add* function simply but both
mounts fitting together. Fitting means, that the post is set to the docking pos
of the spartan. Bulding the same mirror and binding the mount with the same code
as above we get:
```python
mir = Mirror()
mir.set_mount(Spartan_Mount())
mir.draw()
mir.draw_mount()
```

<img src="images/How-to-new-Element/Spartan_composed.png" alt="StretcherStuff" title="" />

OK, you see, this was a fun example, but I hope you got an idea of how to create
arbitrary mounts for your optics. With the composed mount you could also stack
an arbitrary amount of predefined unit mounts together, useful for example for
xyz-stages. A general unit_mount secret is, that most of them have member
variables like *self.is_horizontal = True* that sets its axes always to a certain
constraint, now matter how you try to change it. In this case the inner coordinate
system axes can only change in the xy plane, the z-axis is fixed. To understand
why you can look in the Discussion and Reference in the Docs or read the code in
basic_optics/mounts.

At the end of this section let's have some fun and spice up a setup. We will
start with this rather boring 3 mirror structure:
```python
mir3 = Mirror(phi=75)
mir4 = Mirror(phi=-60)
mir5 = Mirror(phi=90)

comp = Composition(name="MirrorAssembly")
comp.pos += (-200, -300, 0)
comp.propagate(200)
comp.add_on_axis(mir3)
comp.propagate(200)
comp.add_on_axis(mir4)
comp.propagate(200)
comp.add_on_axis(mir5)
comp.propagate(200)

comp.draw()
```

<img src="images/How-to-new-Element/3_Mirror_boring.png" alt="StretcherStuff" title="" />

Now lets insert our new mounts to the setup and see how qucik we can alter the
look.
```python
mir3 = Mirror(phi=75)
mir3.set_mount(Spartan_Mount())
mir4 = Mirror(phi=-60)
mir4.set_mount(Spartan_Mount())
mir5 = Mirror(phi=90)
mir5.set_mount(Spartan_Mount())
```

And here is the result. An optical setup with style ;)

<img src="images/How-to-new-Element/3_Mirror_spartan.png" alt="StretcherStuff" title="" />


## Custom Optical Element and next ray function

ToDo:
Get to Component , make a custom mount?


Custom Element: Fake Trippel_Mirror

Custom Composition: 3 Mirror Polarisation Rotator ?
