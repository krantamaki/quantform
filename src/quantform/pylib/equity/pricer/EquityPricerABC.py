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
  def __call__(self, maturity_date: QfDate, underlying_value: float, *args: List[any], **kwargs: Dict[any]):
    """
    TODO
    """
    pass
  

  @abstractmethod
  def delta():
    pass
  

  @abstractmethod
  def vega():
    

  @abstractmethod
  def gamma():
    

