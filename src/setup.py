"""@package quantform
@author Kasper Rantamäki
Setup script for the QuantForm platform

The setup script does a couple of things needed before running the main file. It 
compiles the C++ libraries, runs tests and if everything is successful, it adds the 
quantform into the Python site-packages directory so that it can be imported as a library.
"""
import subprocess
from setuptools import setup, find_packages


# Compile the C++ functionality
proc = subprocess.run("g++ -c -fPIC -static -std=c++17 -mavx -fopenmp -Wall quantform/cpplib/linsolve.cpp -lm -o quantform/cpplib/linsolve.o".split(' '), capture_output=True)
if proc.returncode == 0:
  proc = subprocess.run("g++ -shared -o quantform/cpplib/linsolve.so quantform/cpplib/linsolve.o -lgomp".split(' '), capture_output=True)
else:
  raise RuntimeError(f"Could not compile the 'linsolve' submodule! Cause:\n{proc.stdout}")
if proc.returncode != 0:
  raise RuntimeError(f"Could not convert the 'linsolve' submodule into a shared object! Cause:\n{proc.stdout}")


# Run the setup
setup(
  name             = "quantform",
  version          = "0.0.1",
  description      = "Platform for quantitative analysis and trading",
  url              = "https://github.com/krantamaki/quantform",
  author           = "Kasper Rantamäki",
  license          = "All rights are reserved",
  packages         = ["quantform", 
                      "quantform.pylib",
                      "quantform.pylib.equity",
                      "quantform.pylib.equity.derivative",
                      "quantform.pylib.equity.portfolio",
                      "quantform.pylib.equity.pricer",
                      "quantform.pylib.equity.stochastic_process",
                      "quantform.pylib.curve",
                      "quantform.pylib.risk_management",
                      "quantform.pylib.surface"
                      ],
  install_requires = ["pandas",  # TODO: add version specifiers
                      "numpy",
                      "matplotlib",
                      "scipy",
                      "quantlib"
                      # "plotly",
                      # "flask",
                      # "dash",
                      # "itables"
                     ]
)