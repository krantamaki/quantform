"""
TODO
"""
from abc import ABC, abstractmethod
from typing import List, Dict

from ...QfDate import QfDate


class EquityPricerABC(ABC):
  """
  TODO
  """

  @abstractmethod
  def __call__(self, report_date: QfDate, underlying_value: float, *args: List[any], **kwargs: Dict[any]):
    """
    TODO
    """
    pass
  

  @abstractmethod
  def delta(self, report_date: QfDate, underlying_value: float, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    pass
  

  @abstractmethod
  def vega(self, report_date: QfDate, underlying_value: float, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    pass
    

  @abstractmethod
  def gamma(self, report_date: QfDate, underlying_value: float, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    pass
    

