from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Pathfinder',
    ext_modules=cythonize("cython_stuff.py"),
    zip_safe=False,
)
