"""
"""
from typing import List

from ..derivative import EquityDerivativeABC
from .UnivariateStrategyABC import UnivariateStrategyABC
from ...QfDate import QfDate


class GenericUnivariateStrategy(UnivariateStrategyABC):
  """Generic class for equity derivatives strategies on a single underlying"""


  def __init__(self, derivatives: List[EquityDerivativeABC], position_sizes: List[float]) -> None:
    """
    """
    assert len(derivatives) == len(position_sizes), f"The lengths of the given arrays must match! ({len(derivatives)} != {len(position_sizes)})"
    
    self.__derivatives = derivatives
    self.__position_sizes = position_sizes


  def __call__(self, underlying_value: float, report_date: QfDate) -> float:
    """
    """
    return sum([self.__position_sizes[i] * self.__derivatives[i](underlying_value, report_date) for i in range(len(self.__derivatives))])


  def delta(self, underlying_value: float, report_date: QfDate) -> float:
    """
    """
    return sum([self.__position_sizes[i] * self.__derivatives[i].delta(underlying_value, report_date) for i in range(len(self.__derivatives))])


  def gamma(self, underlying_value: float, report_date: QfDate) -> float:
    """
    """
    return sum([self.__position_sizes[i] * self.__derivatives[i].gamma(underlying_value, report_date) for i in range(len(self.__derivatives))])


  def vega(self, underlying_value: float, report_date: QfDate) -> float:
    """
    """
    return sum([self.__position_sizes[i] * self.__derivatives[i].vega(underlying_value, report_date) for i in range(len(self.__derivatives))])
  