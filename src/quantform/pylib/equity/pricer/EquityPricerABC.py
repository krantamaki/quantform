"""@package quantform.pylib.equity.pricer.EquityPricerABC
@author Kasper Rantamäki
Submodule with an abstract base class for equity derivative pricers
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Callable

from ...QfDate import QfDate


class EquityPricerABC(ABC):
  """Abstract base class for equity derivative pricers"""

  @abstractmethod
  def __call__(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any, any]):
    """Call method
    
    Call method that calculates the price for the derivative given the value of the underlying and the valuation date.
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The value of the derivative
    """
    pass
  
  
  @abstractmethod
  def __str__(self) -> str:
    """Simple string representation"""
    pass
  
  
  @abstractmethod
  def __repr__(self) -> str:
    """Exhaustive string representation"""
    pass
  

  @abstractmethod
  def delta(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any, any]) -> float:
    """The delta of the derivative
    
    Calculates the delta (sensitivity to the value of the underlying) for the derivative
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The delta of the derivative
    """
    pass
  

  @abstractmethod
  def vega(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any, any]) -> float:
    """The vega of the derivative
    
    Calculates the vega (sensitivity to the volatility) for the derivative
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The vega of the derivative
    """
    pass
    

  @abstractmethod
  def gamma(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any, any]) -> float:
    """The gamma of the derivative
    
    Calculates the gamma (sensitivity to the delta) for the derivative
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The gamma of the derivative
    """
    pass
    
    
  def _diff_factory(self, market_price: float, underlying_value: float, report_date: QfDate) -> Callable:
    """Method for generating a function that gives the difference between the model price and market price
    
    Note that this method should only be accessed by implied volatility methods and similar.
    
    @param market_price      The market price for the derivative
    @param underlying_value  The value of the underlying for the market price
    @param report_date       The date for the market price and the underlying value
    @return                  The difference function
    """
    return lambda vol: self(underlying_value, report_date, vol = vol) - market_price

