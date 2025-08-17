"""@package quantform.pylib.equity.derivative.EquityDerivativeABC
@author Kasper Rantamäki
Submodule for an abstact base class for equity derivatives
"""
from typing import Optional, Tuple, List, Dict
from abc import ABC, abstractmethod
from itertools import product
import numpy as np

from ...QfDate import QfDate
from ..pricer.EquityPricerABC import EquityPricerABC


class EquityDerivativeABC(ABC):
  """Abstract base class for equity derivatives"""
  
  def __call__(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any, any]) -> float:
    """Call method
    
    Call method that calculates the price for the derivative given the value of the underlying and the valuation date.
    Uses the pricer specified when initializing the obejct instance.
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The value of the derivative
    """
    return self.pricer(underlying_value, report_date, *args, **kwargs)
  
  
  def __str__(self) -> str:
    """Simple string representation"""
    return self.contract_id
  
  
  def __repr__(self) -> str:
    """Exhaustive string representation"""
    return f"Contract: {self.contract_id}\nPricer: {repr(self.pricer)}"
  
  
  @property
  @abstractmethod
  def contract_id(self) -> str:
    """The derivative contract identifier"""
    pass
  
  
  @property
  @abstractmethod
  def underlying(self) -> str:
    """The identifier for the underlying for the contract"""
    pass
  
  
  @property
  @abstractmethod
  def maturity_date(self) -> Optional[QfDate]:
    """The maturity (expiration) date for the contract"""
    pass
  
  
  @property
  @abstractmethod
  def strike(self) -> Optional[float]:
    """The strike price for the contract"""
    pass
  
  
  @property
  @abstractmethod
  def market_price(self) -> Optional[float]:
    """The market price for the contract at the time of initialization"""
    pass
  
  
  @property
  @abstractmethod
  def pricer(self) -> EquityPricerABC:
    """The used pricer object"""
    pass
  
  
  def delta(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any, any]) -> float:
    """The delta of the derivative
    
    Calculates the delta (sensitivity to the value of the underlying) for the derivative
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The delta of the derivative
    """
    return self.pricer.delta(underlying_value, report_date, *args, **kwargs)
  
  
  def vega(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any, any]) -> float:
    """The vega of the derivative
    
    Calculates the vega (sensitivity to the volatility) for the derivative
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The vega of the derivative
    """
    return self.pricer.vega(underlying_value, report_date, *args, **kwargs)
  
  
  def gamma(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any, any]) -> float:
    """The gamma of the derivative
    
    Calculates the gamma (sensitivity to the delta) for the derivative
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The gamma of the derivative
    """
    return self.pricer.gamma(underlying_value, report_date, *args, **kwargs)
  
