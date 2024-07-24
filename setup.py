from setuptools import setup

setup(name='lasercad',
      version='1.0.0',
      description='Attempt of OpticDesign Software that is slightly less annoying',
      url='http://github.com/klee-mens/LaserCAD',
      author='Clemens Anschütz',
      author_email='clemens.anschuetz@uni-jena.de',
      license='MIT',
      packages=['lasercad','lasercad.basic_optics','lasercad.freecad_models','lasercad.non_interactings'],
      install_requires=['numpy','matplotlib'],
      zip_safe=False)
