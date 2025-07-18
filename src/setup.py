"""@package quantform
@author Kasper Rantamäki
Setup script for the QuantForm platform

The setup script does a couple of things needed before running the main file. It 
compiles the C++ libraries, runs tests and if everything is successful, it adds the 
quantform into the Python site-packages directory so that it can be imported as a library.
"""
import os
from setuptools import setup


# Compile the C++ functionality
...


# Run the setup
setup(
  name             = "quantform",
  version          = "0.0.1",
  description      = "Platform for quantitative analysis and trading",
  url              = "https://github.com/krantamaki/quantform",
  author           = "Kasper Rantamäki",
  license          = "All rights are reserved",
  packages         = ["quantform"],
  install_requires = ["pandas",  # TODO: add version specifiers
                      "numpy",
                      "plotly",
                      "flask",
                      "dash",
                      "itables",
                      "quantlib"]
)