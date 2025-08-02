"""@package quantform.pylib.surface.GenericSurface
@author Kasper Rantamäki
A submodule for a generic surface defined by a set of (x, y) points and z values
"""
import numpy as np
from typing import Tuple
from scipy.interpolate import CloughTocher2DInterpolator
from scipy.ndimage import gaussian_filter

from .SurfaceABC import SurfaceABC


class GenericSurface(SurfaceABC):
  """Generic surface class"""

  def __init__(self, points: np.ndarray, values: np.ndarray, apply_gaussian_filter: bool = False, 
               gaussian_filter_sd: float = 2.) -> None:
    """Constructor method
    
    Constructor method that stores the passed parameters as instance variables and initializes a CloughTocher2DInterpolator
    object. Additionally, if wanted runs a Gaussian filter on the datapoints to smooth the data.
    
    @param points                 The 2D array of datapoint coordinates (i.e. [(x, y), (x, y), ...])
    @param values                 The values for the datapoints (i.e. [z, z, ...])
    @param apply_gaussian_filter  Boolean flag specifying if a Gaussian filter should be applied to the datapoints.
                                  Optional, defaults to False
    @param gaussian_filter_sd     The standard deviation for the Gaussian filter if applied. Optional, defaults to 2
    @return                       None
    """

    assert len(points) == len(values), f"There must be a value for each point! ({len(points)} != {len(values)})"
    
    # Form temporary numpy arrays for the given arrays
    tmp_points = np.array(points)
    tmp_values = np.array(values)
    
    assert tmp_points.shape[1] == 2 f"The point array must be a list of tuples! ({tmp_points.shape[1]} != 2)"
    assert len(tmp_values.shape) == 1 f"The value array must be a one dimensional Numpy array! ({len(tmp_values.shape)} != 1)"

    # Order the points first by rows and second by columns
    tmp_arr = np.append(tmp_points, tmp_values, 1)
    tmp_arr = sorted(tmp_arr, key = lambda row: (row[0], row[1]))

    self.__points = tmp_arr[0:1, :]
    self.__values = tmp_arr[2, :]
    
    self.__max = np.max(self.__points, axis = 0)
    self.__min = np.min(self.__points, axis = 0)
    
    self.__gaussian_sd = gaussian_filter_sd
    
    if apply_gaussian_filter:
      # Reshape the values into a multidimensional array based on the row values
      values_reshapen = []
      cur_row         = 0
      cur_row_arr     = []
      
      for i, point in enumerate(self.__points):
        row, col = *point
        
        if row > cur_row:
          values_reshapen.append(cur_row_arr)
          cur_row_arr = [self.__values[i]]
          
        else:
          cur_row_arr.append(self.__values[i])
    
      # Apply the Gaussian filter to the reshapen array and flatten the result
      self.__values = gaussian_filter(np.array(values_reshapen), self.__gaussian_sd).flatten()
    
    self.__interpolator = CloughTocher2DInterpolator(self.__points, self.__values)


  def __call__(self, point: Tuple[float, float]) -> float:
    return self.__interpolator(point)


  @property
  def max_x(self) -> float:
    return self.__max[0]
  
  
  @property
  def max_y(self) -> float:
    return self.__max[1]


  @property
  def min_x(self) -> float:
    return self.__min[0]
  
  
  @property
  def min_y(self) -> float:
    return self.__min[1]
  
