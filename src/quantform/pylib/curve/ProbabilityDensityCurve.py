"""@package quantform.pylib.curve.ProbabilityDensityCurve
@author Kasper Rantamäki
TODO
"""
from __future__ import annotations
from typing import Callable, Tuple
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import CubicSpline

from .CurveABC import CurveABC


class ProbabilityDensityCurve(CurveABC):
  """TODO"""
  
  def __init__(self, pdf_func: Callable[[float], float], value_range: Tuple[float, float]) -> None:
    """Constructor method
    
    TODO
    
    @param 
    @param 
    @return                       None
    """
    self.__interpolator = pdf_func
    self.__min = value_range[0]
    self.__max = value_range[1]
    
    self.__mean = self.moment(1)
    self.__std  = self.moment(2)
    self.__skew = self.moment(3)
    self.__kurt = self.moment(4)


  def __call__(self, x: float) -> float:
    assert (x >= self.min) and (x <= self.max), f"Given value outside of value range! ({x} not between {self.min} and {self.max})" 
    return self.__interpolator(x)
  
  
  @classmethod
  def from_points(cls, x_values: np.ndarray, y_values: np.ndarray, value_range: Tuple[float, float]) -> ProbabilityDensityCurve:
    """...
    
    TODO
    """
    assert len(x_values) == len(y_values), f"The arrays must have the same dimensions! ({len(x_values)} != {len(y_values)})"
    
    interp = CubicSpline(x_values, y_values)
    return cls(interp, value_range)
    
  
  @property
  def max(self) -> float:
    return max(self.__max)


  @property
  def min(self) -> float:
    return min(self.__min)
  
  
  @property
  def mean(self) -> float:
    """
    TODO
    """
    return self.__mean
  
  
  @property
  def std(self) -> float:
    """
    TODO
    """
    return self.__std
  
  
  @property
  def skew(self) -> float:
    """
    TODO
    """
    return self.__skew
  
  
  @property
  def kurtosis(self) -> float:
    """
    TODO
    """
    return self.__kurt
  
  
  def cdf(self, x: float) -> float:
    """Cumulative density function
    
    TODO
    
    ...
    """
    assert (x >= self.min) and (x <= self.max), f"Given value outside of value range! ({x} not between {self.min} and {self.max})" 
    return quad(self.__interpolator, self.__min, x)[0]
    
  
  def moment(self, n: int, c: float = 0.) -> float:
    """
    TODO
    """
    integrand = lambda x: (x - c) ** n * self(x)
    
    return quad(integrand, self.__min, self.__max)[0]

