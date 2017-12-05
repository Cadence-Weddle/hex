from distutils.core import setup
from Cython.Build import cythonize



setup(
    name="alpha_beta"
    ext_modules=cythonize('alpha_beta.pyx')
)