# LaserCAD
Authors: Clemens Anschütz clemens.anschuetz@uni-jena.de
He Zhuang he.zhuang@uni-jena.de
Procrastination next level!

In short: LaserCAD helps you quickly prototyping and scripting your optical
setup with as few commands as possible in the language of geometric optics and
a ton of default values. It approximates the ray tracing and shows you a 3D
view of everything in FreeCAD.

The creed is:
1. Make the common case simple.
2. The user should be able to set everything in the script, but the default values should also be set so well that it is not necessary.
3. The code should be designed in such a way that you know where to reprogram something if necessary. (OK, let's see.)

# How to use:
- Install [FreeCAD](https://www.freecad.org/downloads.php)

- Have any kind of python interpreter and a numpy version.

- Download the repository to an arbitrary location
```
git clone https://github.com/klee-mens/LaserCAD.git
```
If you used the **Download ZIP** function, make sure to rename the folder to 
**LaserCAD** and not LaserCAD-main or something like that, or the import lines 
at the beginning of each tutorial script will not work.
Now you can execute e.g. the /tutorial/0_Opening.py in your interpreter.
You should get some text output that ends with something like
```
The geometric object <Composed_Mount:unnamed> is drawn to the position[108.51854, 264.70476,  80.     ] with the direction [-0.95766,  0.2566 , -0.13053]
```
and many more lines. When you open the exact same file in FreeCAD and execute it as a macro by
pressing on the green arrow or F6 you get a new FreeCAD document with the 3D
model looks like this:

![Screenshot von 0_Opening.py in Spyder und in FreeCAD](manual/images/Tutorial-images/0_Opening.png)

# Setting the paths
Currently there is no proper installation process, for 2 reasons:
1. FreeCAD uses its own python libraries and will most likely have other sys 
search paths than your standard python interpreter, so one would have to deal 
with links and stuff, or using 2 copies of the project, but then it's harder to
change the source code and no.
2. I have no clue how to do it. And I'm too lazy to search for it.

So right now, there are 2 ways:
## Copy the path in the executable
In each executable script, the first lines import the location of LaserCAD in
the sys.path list so that python and FreeCAD can find the package. Make sure,
that every executable script has these lines 
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
on top and is in the work directory or somewhere in the LaserCAD package itself.

For the best support from your python IDE I can recommend copying the LaserCAD
folder in your standard python search path, so, for example, side by side with
the numpy package.

## Add the path by macro and IDE
You can also leave the folder were it is (say /home/mens/projects/) and add it to
your python IDE (e.g. Spyder) and FreeCAD manually. For Spyder you can do this
with Tools -> PYTHONPATH manager +
For FreeCAD you have to create yourself a short [macro](https://wiki.freecad.org/Macros), that does the trick.
Click on record and stop it, then you can edit it and insert the following lines
```python
import sys
sys.path.append('/home/mens/projects/')
```
Of course you ahve to replace /home/mens/projects/ with the path to the LaserCAD
clone folder. You can fix the macro to the toolbar with the according dialogue
in FreeCAD (Macro -> add to toolbar).


# Some notes and tips

After that, you can continue executing the other tutorials and tests. Some may
take a few seconds, but most likely, the rendering time is less than a minute.
In the manual folder, you can find some more or less useful texts about the
program and the ideas behind it. Some other documents may follow.


# Some examples
Just to show some of the capabilities of LaserCAD you can see the following
examples in the manual under how-to-build-a-white-cell and
how-to-build-a-stretcher:

<img src="manual/images/how-to-white-cell/white-cell-final.png" alt="Oopsie-NotFound" title="" />

<img src="manual/images/How-to-stretcher/complete.png" alt="StretcherStuff" title="" />

Have fun!