"""@package quantform.pylib.equity.pricer.NeubergerPricer
@author Kasper Rantamäki
Submodule with a Neuberger pricer for pricing log-contracts
"""
import numpy as np
from typing import Callable, Literal

from .EquityPricerABC import EquityPricerABC
from ...QfDate import QfDate


class NeubergerPricer(EquityPricerABC):
  """Neuberger model for pricing log-contracts"""
  
  def __init__(self, maturity_date: QfDate, strike: float, volatility: float) -> None:
    """
    TODO
    """
    assert maturity_date.convention == "Business/252", f"Maturity date has an invalid day count convention! ({maturity_date.convention} != 'Business/252')"
    
    self.__maturity_date = maturity_date
    self.__strike        = strike
    self.__vol           = volatility 
    
    
  def __call__(self, underlying_value: float, report_date: QfDate) -> float:
    return np.log(underlying_value / self.__strike) - 0.5 * np.square(self.__vol) * report_date.timedelta(self.__maturity_date)
  
  
  def __str__(self) -> str:
    """Simple string representation"""
    return f"Neuberger Pricer"
  
  
  def __repr__(self) -> str:
    """Exhaustive string representation"""
    return f"Neuberger Pricer\nMaturity Date: {self.__maturity_date}\nStrike: {self.__strike}\nVolatility: {self.__vol}"
  
  
  @property
  def volatility(self) -> float:
    return self.__vol
  
  
  def delta(self, underlying_value: float, report_date: QfDate) -> float:
    return 1 / underlying_value
  
  
  def vega(self, underlying_value: float, report_date: QfDate) -> float:
    return -self.__vol * report_date.timedelta(self.__maturity_date)
            
  
  def gamma(self, underlying_value: float, report_date: QfDate) -> float:
    return -1 / np.square(underlying_value)