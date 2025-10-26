"""@package quantform.pylib.curve.GenericCurve
@author Kasper Rantamäki
A submodule for a generic curve defined by a set of x and y values
"""
from typing import Literal
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.ndimage import gaussian_filter1d

from .CurveABC import CurveABC


class GenericCurve(CurveABC):
  """Generic curve class"""

  def __init__(self, x_values: np.ndarray, y_values: np.ndarray, apply_gaussian_filter: bool = False, 
               gaussian_filter_sd: float = 2., extrapolation_method: Literal["CubicSpline", "Constant"] = "CubicSpline") -> None:
    """Constructor method
    
    Constructor method that stores the passed parameters as instance variables and initializes a CubicSpline
    object. Additionally, if wanted runs a Gaussian filter on the datapoints to smooth the data.
    
    @param x_values               The x values for the datapoints
    @param y_values               The y values for the datapoints
    @param apply_gaussian_filter  Boolean flag specifying if a Gaussian filter should be applied to the datapoints.
                                  Optional, defaults to False
    @param gaussian_filter_sd     The standard deviation for the Gaussian filter if applied. Optional, defaults to 2
    @param extrapolation_method   Method used to extrapolate beyond the given value range. Optional, defaults to 'CubicSpline'
    @raises AssertionError        Raised if the dimensions of x and y arrays don't match
    @return                       None
    """

    assert len(x_values) == len(y_values), f"The arrays must have the same dimensions! ({len(x_values)} != {len(y_values)})"
    assert extrapolation_method.lower() in ["cubicspline", "constant"], f"Invalid extrapolation method specified! {extrapolation_method} not in ['CubicSpline', 'Constant']"

    self.__x = np.array(x_values)
    self.__y = np.array(y_values)
    self.__extrapolation_method = extrapolation_method
    
    self.__gaussian_sd = gaussian_filter_sd
    
    if apply_gaussian_filter:
      # The extrapolation method is "Constant" extend the point arrays in both directions with constant values to smooth the transition to extrapolation
      if extrapolation_method.lower() == "constant":
        point_dist = np.mean(np.diff(self.__x))
        self.__x = np.concat([np.linspace(max(0, self.__x[0] - point_dist * 11), self.__x[0] - point_dist, 10), self.__x, np.linspace(self.__x[-1] + point_dist, self.__x[-1] + point_dist * 11, 10)])
        self.__y = np.concat([np.array([self.__y[0]] * 10), self.__y, np.array([self.__y[-1]] * 10)])
        self.__y = gaussian_filter1d(self.__y, self.__gaussian_sd)
      else:
        self.__y = gaussian_filter1d(self.__y, self.__gaussian_sd)
    
    self.__interpolator = CubicSpline(self.__x, self.__y)
    

  def __call__(self, x: float) -> float:
    if (x < self.min) and (self.__extrapolation_method == "Constant"):
      return self.__y[0]
    
    if (x > self.max) and (self.__extrapolation_method == "Constant"):
      return self.__y[-1]
    
    return self.__interpolator(x)


  @property
  def max(self) -> float:
    return self.__x[-1]


  @property
  def min(self) -> float:
    return self.__x[0]
  
