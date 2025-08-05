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
  def __call__(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]):
    """
    TODO
    """
    pass
  

  @abstractmethod
  def delta(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    pass
  

  @abstractmethod
  def vega(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    pass
    

  @abstractmethod
  def gamma(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    pass
    
