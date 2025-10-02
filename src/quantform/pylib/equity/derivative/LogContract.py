"""@package quantform.pylib.equity.derivative.LogContract
@author Kasper Rantamäki
Submodule with a class implementation for log-contract
"""
from __future__ import annotations
import numpy as np
from typing import Literal, Optional

from .EquityDerivativeABC import EquityDerivativeABC
from ...QfDate import QfDate
from ..pricer import PathIndependentBreedenLitzenbergerPricer
from ..pricer import EquityPricerABC
from ..pricer import NeubergerPricer
from ...curve import ImpliedVolatilityCurve


class LogContract(EquityDerivativeABC):
  """Class for log contracts"""
  
  def __init__(self, contract_id: str, underlying: str, maturity_date: QfDate, strike: float,
               risk_free_rate: float, volatility_curve: ImpliedVolatilityCurve, pricer: Literal["BreedenLitzenberger", "Neuberger"] = "BreedenLitzenberger") -> None:
    """Constructor method
    
    Constructor method that stores the given parameters as instance variables and initializes the wanted pricer object.
    
    @param contract_id       The identifier for the option
    @param underlying        The identifier for the underlying
    @param maturity_date     The maturity date for the option
    @param strike            The initial value of the underlying used to define the contract
    @param risk_free_rate    The prevailing risk-free rate
    @param volatility_curve  The implied volatility curve for the underlying on the given maturity date
    @param pricer            The name of the wanted pricer method. Optional, defaults to 'BreedenLitzenberger'
    @raises AssertionError   Raised if an invalid parameter for 'pricer' is passed
    @return                  None
    """
    
    self.__contract_id    = contract_id
    self.__underlying     = underlying
    self.__maturity_date  = maturity_date
    self.__strike         = strike
    self.__risk_free_rate = risk_free_rate
    self.__vol            = volatility_curve
    self.__pricer         = None
    self.__payoff         = lambda x: np.log(x / self.__strike)
   
    match pricer.lower():
      case "breedenlitzenberger":
        self.__pricer = PathIndependentBreedenLitzenbergerPricer(self.__maturity_date, self.__payoff, self.__vol, self.__risk_free_rate, 'BlackScholes')
      case "neuberger":
        self.__pricer = NeubergerPricer(self.__maturity_date, self.__strike, self.__vol(self.__strike))
      case _:
        assert False, f"Invalid pricer name given! ({pricer} not in ['BreedenLitzenberger'])"
        
  
  @property
  def contract_id(self) -> str:
    return self.__contract_id
  
  
  @property
  def underlying(self) -> str:
    return self.__underlying
  
  
  @property
  def maturity_date(self) -> QfDate:
    return self.__maturity_date
  
  
  @property
  def strike(self) -> float:
    return self.__strike
  
  
  @property
  def market_price(self) -> Optional[float]:
    return None
  
  
  @property
  def pricer(self) -> EquityPricerABC:
    return self.__pricer
