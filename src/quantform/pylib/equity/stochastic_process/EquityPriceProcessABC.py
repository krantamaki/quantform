"""
TODO
"""
from abc import ABC, abstractmethod
from typing import Iterator, Tuple, Optional


class EquityPriceProcessABC(ABC):
  """
  TODO
  """
  
  @abstractmethod
  def __call__(self, start_price: float, years: float, steps: int, volatility: Optional[float] = None) -> Iterator:
    """
    TODO
    """
    pass
  

  @abstractmethod
  def __iter__(self) -> Tuple[float, float]:
    """
    TODO
    """
    pass
  
  
  @property
  def volatility(self) -> float:
    """
    TODO
    """
    return self.__volatility
  