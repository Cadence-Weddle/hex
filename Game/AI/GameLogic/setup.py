from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

setup(
  name = 'GetGameState',
  ext_modules = cythonize("GetGameState.pyx"),
  include_dirs=[np.get_include()]

)