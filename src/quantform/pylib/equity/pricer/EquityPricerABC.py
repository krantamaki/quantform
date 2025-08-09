"""
TODO
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Callable

from ...QfDate import QfDate


class EquityPricerABC(ABC):
  """
  TODO
  """

  @abstractmethod
  def __call__(self, underlying_value: float, report_date: QfDate, vol; Optional[float] = None, *args: List[any], **kwargs: Dict[any]):
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
    
    
  def __diff_factory(self, market_price: float, underlying_value: float, report_date: QfDate) -> Callable:
    """
    TODO
    """
    return lambda vol: self(underlying_value, report_date, vol = vol) - option_value

