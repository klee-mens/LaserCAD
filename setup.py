from setuptools import setup, find_packages

# setup(
#     name="LaserCAD",
#     version="1.0.0",
#     packages=find_packages(include=['basic_optics.*', 'freecad_models.*', 'non_interactings.*']),
# )


setup(
    name="LaserCAD",
    version="1.1.0",
    packages=find_packages(include=["LaserCAD", "LaserCAD.*"]),
)