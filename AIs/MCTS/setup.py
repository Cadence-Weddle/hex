from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = "MCTS",
    ext_modules = cythonize('MonteCarloTreeSearch.pyx')
)