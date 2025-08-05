"""@package quantform.pylib.equity.derivative.EquityDerivativeABC
@author Kasper Rantamäki

"""
from typing import Optional, Tuple, List, Dict
from abc import ABC, abstractmethod
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from ...QfDate import QfDate
from ..pricer import EquityPricerABC


class EquityDerivativeABC(ABC):
  """TODO"""
  
  def __call__(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    return self.pricer(underlying_value, report_date, *args, **kwargs)
  
  
  @property
  def contract_id(self) -> str:
    """
    TODO
    """
    return self.__contract_id
  
  
  @property
  def underlying(self) -> str:
    """
    TODO
    """
    return self.__underlying
  
  
  @property
  def maturity_date(self) -> Optional[QfDate]:
    """
    TODO
    """
    return self.__maturity_date
  
  
  @property
  def strike(self) -> Optional[float]:
    """
    TODO
    """
    return self.__strike
  
  
  @property
  def market_price(self) -> Optional[float]:
    """
    TODO
    """
    return self.__market_price
  
  
  @property
  def pricer(self) -> EquityPricerABC:
    """
    TODO
    """
    return self.__pricer
  
  
  def delta(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    return self.pricer.delta(underlying_value, report_date, *args, **kwargs)
  
  
  def gamma(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    return self.pricer.gamma(underlying_value, report_date, *args, **kwargs)
  
  
  def vega(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    return self.pricer.vega(underlying_value, report_date, *args, **kwargs)
  
  
  def plot() -> plt.Figure:
    """
    TODO
    """
    pass
  
