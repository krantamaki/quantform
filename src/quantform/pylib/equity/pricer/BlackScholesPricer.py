"""@package quantform.pylib.equity.pricer.BlackScholesPricer
@author Kasper Rantamäki
Submodule with a very basic analytical Black-Scholes pricer
"""
from typing import Callable, Optional, Literal
import numpy as np
from scipy.stats import norm

from .EquityPricerABC import EquityPricerABC
from ...QfDate import QfDate
from ..utils import bisection_method, discount


class BlackScholesPricer(EquityPricerABC):
  """Option pricer based on the Black-Scholes model"""
  
  def __init__(self, maturity_date: QfDate, type: Literal["Call", "Put"], strike: float, risk_free_rate: float, volatility: Optional[float] = None, 
               market_price: Optional[float] = None, underlying_value: Optional[float] = None,
               report_date: Optional[QfDate] = None) -> None:
    """
    TODO
    """
    assert (volatility is not None) or (market_price is not None and underlying_value is not None and report_date is not None), 
    "Either volatility or market parameters need to be defined!"

    self.__maturity_date = maturity_date
    self.__option_type   = type
    self.__strike        = strike
    self.__rf            = risk_free_rate
    self.__vol           = volatility if volatility is not None else self.implied_volatility(market_price, underlying_value, report_date)
    
    
  def __call__(self, underlying_value: float, report_date: QfDate, vol: Optional[float] = None) -> float:
    """
    TODO
    """
    assert self.__maturity_date >= report_date, f"Report date must be at most maturity date! ({report_date} > {self.__maturity_date})"
  
    if self.__maturity_date == report_date: 
      if self.__option_type == 'Call': return max(0, underlying_value - self.__strike)
      else: return max(0, self.__strike - underlying_value)
    
    if self.__option_type == 'Call':
      return norm.cdf(self.d_plus(underlying_value, report_date, vol = vol)) * underlying_value -\
             norm.cdf(self.d_minus(underlying_value, report_date, vol = vol)) * self.__strike *\
             discount(self.__rf, report_date.timedelta(self.__maturity_date))

    # Else
    return norm.cdf(-self.d_minus(underlying_value, report_date, vol = vol)) * self.__strike *\
           discount(self.__rf, report_date.timedelta(self.__maturity_date)) -\
           norm.cdf(-self.d_plus(underlying_value, report_date, vol = vol)) * underlying_value
           
  
  def delta(self, underlying_value: float, report_date: QfDate) -> float:
    """
    TODO
    """
    return norm.cdf(self.d_plus(underlying_value, report_date))
  
  
  def vega(self, underlying_value: float, report_date: QfDate) -> float:
    """
    TODO
    """
    return underlying_value * np.exp(-self.d_plus(underlying_value, report_date) ** 2 / 2) * \
           np.sqrt(report_date.timedelta(self.__maturity_date)) / np.sqrt(2 * np.pi)
            
  
  def gamma(self, underlying_value: float, report_date: QfDate) -> float:
    """
    TODO
    """
    return self.__strike * discount(self.__rf, report_date.timedelta(self.__maturity_date)) * \
           norm.pdf(self.d_minus(underlying_value, report_date)) / (underlying_value ** 2 * self.__vol * \
           np.sqrt(report_date.timedelta(self.__maturity_date))
                                               
  
  def implied_volatility(self, market_price: float, underlying_value: float, report_date: QfDate) -> float:
    """
    TODO
    """
    
    diff_func = self.__diff_factory(market_price, underlying_value, report_date)
    
    lower = 1e-6
    assert diff(lower) < 0, f"Implied volatility can't be calculated as the lower bound difference is not negative! (Lower bound is {diff(lower)})"

    upper = 0.01
    while diff(upper) < 0 and upper < 100:
        upper += 0.1

    assert upper < 100, "Implied volatility can't be calculated as the difference is not positive for any upped bound!"

    implied_vol = bisection_method(diff, lower, upper)

    return implied_vol
  
  
  def d_plus(self, underlying_value: float, report_date: QfDate, vol: float = None) -> float:
    """
    TODO
    """
    
    if vol is None:
      return 1 / (self.__vol * np.sqrt(report_date.timedelta(self.__maturity_date))) *\
             (np.log(underlying_value / self.__strike) + (self.__rf + self.__vol ** 2 / 2) *\
             report_date.timedelta(self.__maturity_date))
    
    else:
      return 1 / (vol * np.sqrt(report_date.timedelta(self.__maturity_date))) *\
             (np.log(underlying_value / self.__strike) + (self.__rf + vol ** 2 / 2) *\
             report_date.timedelta(self.__maturity_date))


  def d_minus(self, underlying_value: float, report_date: datetime, vol: float = None) -> float:
    
    if vol is None:
      return self.d_plus(underlying_value, report_date) -\
             self.__vol * np.sqrt(report_date.timedelta(self.__maturity_date))
    
    else:
      return self.d_plus(underlying_value, report_date, vol = vol) -\
             vol * np.sqrt(report_date.timedelta(self.__maturity_date))
  