"""@package quantform.pylib.curve.GenericCurve
@author Kasper Rantamäki
A submodule for a generic curve defined by a set of x and y values
"""
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.ndimage import gaussian_filter1d

from .CurveABC import CurveABC


class GenericCurve(CurveABC):
  """Generic curve class"""

  def __init__(self, x_values: np.ndarray, y_values: np.ndarray, apply_gaussian_filter: bool = False, 
               gaussian_filter_sd: float = 2., allow_extrapolation: bool = True) -> None:
    """Constructor method
    
    Constructor method that stores the passed parameters as instance variables and initializes a CubicSpline
    object. Additionally, if wanted runs a Gaussian filter on the datapoints to smooth the data.
    
    @param x_values               The x values for the datapoints
    @param y_values               The y values for the datapoints
    @param apply_gaussian_filter  Boolean flag specifying if a Gaussian filter should be applied to the datapoints.
                                  Optional, defaults to False
    @param gaussian_filter_sd     The standard deviation for the Gaussian filter if applied. Optional, defaults to 2
    @param allow_extrapolation    Boolean flag telling if extrapolating beyond the dataset is permitted. Optional, defaults to True
    @raises AssertionError        Raised if the dimensions of x and y arrays don't match
    @return                       None
    """

    assert len(x_values) == len(y_values), f"The arrays must have the same dimensions! ({len(x_values)} != {len(y_values)})"

    self.__x = x_values
    self.__y = y_values
    
    self.__gaussian_sd = gaussian_filter_sd
    
    if apply_gaussian_filter:
      self.__y = gaussian_filter1d(self.__y, self.__gaussian_sd)
    
    self.__interpolator = CubicSpline(self.__x, self.__y)
    self.__extrapolate  = allow_extrapolation


  def __call__(self, x: float) -> float:
    assert self.__extrapolate or ((x >= self.min) and (x <= self.max)), f"Extrapolation is not allowed! ({x} not between {self.min} and {self.max})" 
    return self.__interpolator(x)


  @property
  def max(self) -> float:
    return max(self.__x)


  @property
  def min(self) -> float:
    return min(self.__x)
  
