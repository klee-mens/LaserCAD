from setuptools import setup, find_packages

setup(name='lasercad',
      version='1.0.0',
      description='Attempt of OpticDesign Software that is slightly less annoying',
      url='http://github.com/klee-mens/LaserCAD',
      author='Clemens Anschütz',
      author_email='clemens.anschuetz@uni-jena.de',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['numpy','matplotlib'],
      zip_safe=False)
