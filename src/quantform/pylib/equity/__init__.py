"""@package quantform.pylib.equity
@author Kasper Rantamäki
Module for calculations on equity products and derivatives
"""


__all__ = ["futures_boundary_factory",
           "call_option_boundary_factory",
           "put_option_boundary_factory",
           "constant_boundary_factory",
           "out_boundary_factory",
           "trivial_lower_boundary",
           "trivial_expiration_boundary",
           "discount", 
           "parse_option_id", 
           "form_option_id", 
           "bisection_method"]


from .boundaries import *
from .utils import *

