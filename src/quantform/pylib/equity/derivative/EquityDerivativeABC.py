"""@package quantform.pylib.equity.derivative.EquityDerivativeABC
@author Kasper Rantamäki
Submodule for an abstact base class for equity derivatives
"""
from typing import Optional, Tuple, List, Dict
from abc import ABC
from itertools import product
import numpy as np

from ...QfDate import QfDate
from ...surface import GenericSurface
from ..pricer import EquityPricerABC


class EquityDerivativeABC(ABC):
  """Abstract base class for equity derivatives"""
  
  def __call__(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
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
  
  
  @property
  def contract_id(self) -> str:
    """The derivative contract identifier"""
    return self.__contract_id
  
  
  @property
  def underlying(self) -> str:
    """The identifier for the underlying for the contract"""
    return self.__underlying
  
  
  @property
  def maturity_date(self) -> Optional[QfDate]:
    """The maturity (expiration) date for the contract"""
    return self.__maturity_date
  
  
  @property
  def strike(self) -> Optional[float]:
    """The strike price for the contract"""
    return self.__strike
  
  
  @property
  def market_price(self) -> Optional[float]:
    """The market price for the contract at the time of initialization"""
    return self.__market_price
  
  
  @property
  def pricer(self) -> EquityPricerABC:
    """The used pricer object"""
    return self.__pricer
  
  
  def delta(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
    """The delta of the derivative
    
    Calculates the delta (sensitivity to the value of the underlying) for the derivative
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The delta of the derivative
    """
    return self.pricer.delta(underlying_value, report_date, *args, **kwargs)
  
  
  def vega(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
    """The vega of the derivative
    
    Calculates the vega (sensitivity to the volatility) for the derivative
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The vega of the derivative
    """
    return self.pricer.vega(underlying_value, report_date, *args, **kwargs)
  
  
  def gamma(self, underlying_value: float, report_date: QfDate, *args: List[any], **kwargs: Dict[any]) -> float:
    """The gamma of the derivative
    
    Calculates the gamma (sensitivity to the delta) for the derivative
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @*args                   Additional class specific arguments
    @**kwargs                Additional class specific keyword arguments
    @return                  The gamma of the derivative
    """
    return self.pricer.gamma(underlying_value, report_date, *args, **kwargs)
  
  
  def surface(self, n_points: Tuple[int, int], n_days_back: int = 252, max_underlying_value: Optional[int] = None,
              end_date: Optional[QfDate] = None) -> GenericSurface:
    """Method for computing the price surface for the derivative
    
    Method that generates a GenericSurface object from points computed using the derivatives pricer
    
    @param n_points     The number of points on the 'time to maturity' and 'underlying value' dimensions on which the surface is evaluated as a tuple
    @param n_days_back  The number of days back from the maturity date for which the derivative is priced. Optional, defaults to 252 (one year in trading days)
    @param max_strike   The maximum value of the underlying for which the derivative is priced. Optional, defaults to None i.e. 3 times the strike is used.
                        If the derivative has no strike price the parameter must be specified
    @param end_date     The end date for pricing. Optional, defaults to None i.e. the maturity date being used. If the derivative has no maturity date
                        the parameter must be specified
    @return             A GenericSurface object for the derivative prices
    """
    
    max_underlying_value = max_underlying_value if max_underlying_value is not None else 3 * self.strike
    end_date             = end_date if end_date is not None else self.maturity_date
    
    start_date = end_date - n_days_back
    time_to_maturity = start_date.timedelta(end_date)
    
    xx = np.linspace(0, time_to_maturity, n_points[0])
    yy = np.linspace(0, max_underlying_value, n_points[1])

    xy = np.array(list(product(xx, yy)))
    vals = np.array([self(tup[1], start_date * tup[0]) for tup in xy])    
    
    return GenericSurface(xy, vals)
    
  