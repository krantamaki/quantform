"""
TODO
"""
from abc import ABC, abstractmethod
from typing import Iterator, Tuple


class EquityPriceProcessABC(ABC):
  """
  TODO
  """
  
  def __call__(self, start_price: float, years: float, steps: int) -> Iterator:
    """
    TODO
    """
    pass
  

  def __iter__(self) -> Tuple[float, float]:
    """
    TODO
    """
    pass
  