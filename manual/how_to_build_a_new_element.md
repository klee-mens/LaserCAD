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
IMAGE OF ALIGNED Detector