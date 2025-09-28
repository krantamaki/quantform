"""
"""
from abc import ABC, abstractmethod

from ...QfDate import QfDate


class UnivariateStrategyABC(ABC):
  """Abstact base class for an equity derivatives strategy on a single underlying"""

  @abstractmethod
  def __call__(self, underlying_value: float, report_date: QfDate) -> float:
    """
    """
    pass


  @abstractmethod
  def delta(self, underlying_value: float, report_date: QfDate) -> float:
    """
    """
    pass


  @abstractmethod
  def gamma(self, underlying_value: float, report_date: QfDate) -> float:
    """
    """
    pass


  @abstractmethod
  def vega(self, underlying_value: float, report_date: QfDate) -> float:
    """
    """
    pass
