"""@package quantform.pylib.equity.derivative.Option
@author Kasper Rantamäki

"""
import numpy as np
from typing import Literal

from .EquityDerivativeABC import EquityDerivativeABC
from ...QfDate import QfDate
from ..pricer import BlackScholesPricer
from ..utils import discount, form_option_id, parse_option_id


class Option(EquityDerivativeABC):
  """TODO"""
  
  def __init__(self, contract_id: str, underlying: str, maturity_date: QfDate, type: Literal["Call", "Put"], strike: float,
               risk_free_rate: float, volatility: Optional[float] = None, pricer: Literal["BlackScholes"] = "BlackScholes", 
               market_price: Optional[float] = None, underlying_value: Optional[float] = None, report_date: Optional[QfDate] = None) -> None:
    """
    TODO
    """
    assert type.lower() in ["call", "put"], f"Invalid option type specified! ({type} not in ['Call', 'Put'])"
    assert (volatility is not None) or (market_price is not None and underlying_value is not None and report_date is not None), 
    "Either the volatility term or market price must be specified for proper pricer initialization!"
    
    self.__contract_id      = contract_id
    self.__underlying       = underlying
    self.__maturity_date    = maturity_date
    self.__type             = type
    self.__strike           = strike
    self.__risk_free_rate   = risk_free_rate
    self.__volatility       = volatility
    self.__market_price     = market_price
   
    match pricer.lower():
      case "blackscholes":
        self.__pricer = BlackScholesPricer(self.__maturity_date, self.__strike, self.__risk_free_rate, self.__volatility,
                                           self.__market_price, underlying_value, report_date)
      case _:
        assert False, f"Invalid pricer name given! ({pricer} not in ['BlackScholes'])"
        
      
  @property
  def type(self) -> str:
    """
    TODO
    """
    return self.__type
  
  
  def parity(self, underlying_value: float, report_date: QfDate) -> Option:
    """
    TODO
    """
    if self.type.lower() == "call":
      put_id = form_option_id(self.__underlying, self.__maturity_date, "Put", self.__strike)
      return Option(put_id, *parse_option_id(put_id), self.__risk_free_rate, 
                    market_price = self(underlying_value, report_date) - discount(self.__risk_free_rate, report_date.timedelta(self.__maturity_date)) * (underlying_value - self.__strike),
                    underlying_value = underlying_value,
                    report_date = report_date)
                    
    else:
      call_id = form_option_id(self.__underlying, self.__maturity_date, "Call", self.__strike)
      return Option(call_id, *parse_option_id(call_id), self.__risk_free_rate, 
                    market_price = self(underlying_value, report_date) + discount(self.__risk_free_rate, report_date.timedelta(self.__maturity_date)) * (underlying_value - self.__strike),
                    underlying_value = underlying_value,
                    report_date = report_date)
  
