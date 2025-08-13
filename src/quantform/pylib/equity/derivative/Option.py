"""@package quantform.pylib.equity.derivative.Option
@author Kasper Rantamäki
Submodule with a class implementation for a generic European option
"""
from __future__ import annotations
import numpy as np
from typing import Literal, Optional

from .EquityDerivativeABC import EquityDerivativeABC
from ...QfDate import QfDate
from ..pricer import BlackScholesPricer, EquityPricerABC
from ..utils import discount, form_option_id, parse_option_id


class Option(EquityDerivativeABC):
  """Class for European options"""
  
  def __init__(self, contract_id: str, underlying: str, maturity_date: QfDate, type: Literal["Call", "Put"], strike: float,
               risk_free_rate: float, volatility: Optional[float] = None, pricer: Literal["BlackScholes"] = "BlackScholes", 
               market_price: Optional[float] = None, underlying_value: Optional[float] = None, report_date: Optional[QfDate] = None) -> None:
    """Constructor method
    
    Constructor method that stores the given parameters as instance variables and initializes the wanted pricer object.
    
    @param contract_id       The identifier for the option
    @param underlying        The identifier for the underlying
    @param maturity_date     The maturity date for the option
    @param type              The type of option ('Call' or 'Put')
    @param strike            The strike price of the option
    @param risk_free_rate    The prevailing risk-free rate
    @param volatility        The volatility of the underlying. Optional, defaults to None
    @param pricer            The name of the wanted pricer method
    @param market_price      The market price for the option. Optional, defaults to None
    @param underlying_value  The value of the underlying for the market price. Optional, defaults to None
    @param report_date       The date for the market price and the underlying value. Optional, defaults to None
    @raises AssertionError   Raised if volatility is not given and cannot be computed or if an invalid parameter for 'type' or 'pricer' is passed
    @return                  None
    """
    
    assert type.lower() in ["call", "put"], f"Invalid option type specified! ({type} not in ['Call', 'Put'])"
    assert (volatility is not None) or ((market_price is not None) and (underlying_value is not None) and (report_date is not None)), "Either the volatility term or market price must be specified for proper pricer initialization!"
    
    self.__contract_id      = contract_id
    self.__underlying       = underlying
    self.__maturity_date    = maturity_date
    self.__type             = type
    self.__strike           = strike
    self.__risk_free_rate   = risk_free_rate
    self.__volatility       = volatility
    self.__market_price     = market_price
    self.__pricer           = None
   
    match pricer.lower():
      case "blackscholes":
        self.__pricer = BlackScholesPricer(self.__maturity_date, self.__type, self.__strike, self.__risk_free_rate, self.__volatility,
                                           self.__market_price, underlying_value, report_date)
      case _:
        assert False, f"Invalid pricer name given! ({pricer} not in ['BlackScholes'])"
        
      
  @property
  def type(self) -> str:
    """The option type ('Call' or 'Put')"""
    return self.__type
  
  
  @property
  def contract_id(self) -> str:
    return self.__contract_id
  
  
  @property
  def underlying(self) -> str:
    return self.__underlying
  
  
  @property
  def maturity_date(self) -> Optional[QfDate]:
    return self.__maturity_date
  
  
  @property
  def strike(self) -> Optional[float]:
    return self.__strike
  
  
  @property
  def market_price(self) -> Optional[float]:
    return self.__market_price
  
  
  @property
  def pricer(self) -> EquityPricerABC:
    return self.__pricer
  
  
  def parity(self, underlying_value: float, report_date: QfDate) -> Option:
    """Put-call parity
    
    Method that returns a new Option instance that satisfies the put-call parity
    
    @param underlying_value  The value of the underlying security
    @param report_date       The valuation date
    @return                  The put or call option satisfying put-call parity
    """
    if self.type.lower() == "call":
      put_id = form_option_id(self.__underlying, self.__maturity_date, "Put", self.__strike)
      return Option(put_id, *parse_option_id(put_id, calendar=self.__maturity_date.calendar, convention=self.__maturity_date.convention), 
                    self.__risk_free_rate, 
                    market_price = self(underlying_value, report_date) - discount(self.__risk_free_rate, report_date.timedelta(self.__maturity_date)) * (underlying_value - self.__strike),
                    underlying_value = underlying_value,
                    report_date = report_date)
                    
    else:
      call_id = form_option_id(self.__underlying, self.__maturity_date, "Call", self.__strike)
      return Option(call_id, *parse_option_id(call_id, calendar=self.__maturity_date.calendar, convention=self.__maturity_date.convention),
                    self.__risk_free_rate, 
                    market_price = self(underlying_value, report_date) + discount(self.__risk_free_rate, report_date.timedelta(self.__maturity_date)) * (underlying_value - self.__strike),
                    underlying_value = underlying_value,
                    report_date = report_date)
  
