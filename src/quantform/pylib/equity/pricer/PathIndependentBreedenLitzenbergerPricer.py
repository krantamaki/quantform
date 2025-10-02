"""@package quantform.pylib.equity.pricer.PathIndependentBreedenLitzenbergerPricer
@author Kasper Rantamäki
Submodule with a Breeden-Litzenberger pricer for path-independent exotics
value of which is derived from the stock price process at the maturity of the contract
"""
import numpy as np
from typing import Callable, Literal, Optional, Tuple
from scipy.integrate import quad
from scipy.stats import norm

from .EquityPricerABC import EquityPricerABC
from .BlackScholesPricer import BlackScholesPricer
from ...curve import ImpliedVolatilityCurve, ProbabilityDensityCurve
from ..utils import discount
from ...QfDate import QfDate


class PathIndependentBreedenLitzenbergerPricer(EquityPricerABC):
  """Breeden-Litzenberger pricer for path-independent exotics"""

  def __init__(self, maturity_date: QfDate, payoff_function: Callable[[float], float],
               volatility_curve: ImpliedVolatilityCurve, risk_free_rate: float,
               option_pricer: Literal["BlackScholes"] = "BlackScholes") -> None:
    """Constructor method
    
    Constructor method that stores the passed parameters as instance variables.
    
    @param maturity_date     The maturity date for the exotic contract
    @param payoff_function   The state-contingent claim of the exotic contract 
    @param volatility_curve  The implied volatility curve for the maturity date
    @param risk_free_rate    The discount rate for the maturity date
    @param option_pricer     The used call option pricer. Optional, defaults to 'BlackScholes'
    @raises AssertionError   Raised if the maturity date doesn't use 'Business/252' convention
    @raises ValueError       Raised if an invalid option pricer is specified 
    @return                  None
    """
    assert maturity_date.convention == "Business/252", f"Maturity date has an invalid day count convention! ({maturity_date.convention} != 'Business/252')"

    self.__maturity_date = maturity_date
    self.__payoff        = payoff_function
    self.__vol           = volatility_curve
    self.__rf            = risk_free_rate

    if option_pricer.lower() == "blackscholes":
      self.__pricer = BlackScholesPricer
    else:
      raise ValueError(f"Invalid option pricer specified! ({option_pricer} not in ['BlackScholes'])")


  def __call__(self, underlying_value: float, report_date: QfDate, integration_interval: Optional[Tuple[float, float]] = None) -> float:
    """
    """
    if integration_interval is None:
      integration_interval = (0, self.__vol.max * 1.5)
    
    def integrand(x: float) -> float:
      return self.__payoff(x) * self.__pricer(self.__maturity_date, 'Call', x, self.__rf, self.__vol(x)).gamma(underlying_value, report_date)
    
    return quad(integrand, integration_interval[0], integration_interval[1])[0]


  def __str__(self) -> str:
    """
    """
    pass


  def __repr__(self) -> str:
    """
    """
    pass
  
  
  @property
  def volatility(self) -> float:
    raise NotImplementedError("Not applicable")


  def delta(self, underlying_value: float, report_date: QfDate, integration_interval: Optional[Tuple[float, float]] = None) -> float:
    """
    """
    if integration_interval is None:
      integration_interval = (0, self.__vol.max * 1.5)
    
    def integrand(x: float) -> float:
      vol = self.__vol(x)
      d_plus = self.__pricer(self.__maturity_date, 'Call', x, self.__rf, vol).d_plus(underlying_value, report_date)
      timedelta = report_date.timedelta(self.__maturity_date)
      
      return -self.__payoff(x) * (d_plus * norm.pdf(d_plus) + vol * np.sqrt(timedelta) * norm.pdf(d_plus)) \
        / np.square(underlying_value * vol * np.sqrt(timedelta))
    
    return quad(integrand, integration_interval[0], integration_interval[1])[0]


  def gamma(self, underlying_value: float, report_date: QfDate, integration_interval: Optional[Tuple[float, float]] = None) -> float:
    """
    """
    raise NotImplementedError("The gamma has not been implemented yet!")


  def vega(self, underlying_value: float, report_date: QfDate, integration_interval: Optional[Tuple[float, float]] = None) -> float:
    """
    """
    if integration_interval is None:
      integration_interval = (0, self.__vol.max * 1.5)
    
    def integrand(x: float) -> float:
      vol = self.__vol(x)
      d_plus = self.__pricer(self.__maturity_date, 'Call', x, self.__rf, vol).d_plus(underlying_value, report_date)
      timedelta = report_date.timedelta(self.__maturity_date)
      
      return -self.__payoff(x) * (vol * d_plus * norm.pdf(d_plus) * (d_plus / vol - np.sqrt(timedelta)) - norm.pdf(d_plus)) \
        / (underlying_value * np.sqrt(timedelta) * np.square(vol))
    
    return quad(integrand, integration_interval[0], integration_interval[1])[0]


  def implied_density(self, underlying_value: float, report_date: QfDate, integration_interval: Optional[Tuple[float, float]] = None) -> ProbabilityDensityCurve:
    """
    
    """
    if integration_interval is None:
      integration_interval = (0, self.__vol.max * 1.5)
    
    def unnorm_pdf(x: float) -> float:
      return self.__pricer(self.__maturity_date, 'Call', x, self.__rf, self.__vol(x)).gamma(underlying_value, report_date) / discount(self.__rf, report_date.timedelta(self.__maturity_date))
    
    norm_factor = 1 / quad(unnorm_pdf, integration_interval[0], integration_interval[1])[0]

    def pdf(x: float) -> float:
      return norm_factor * unnorm_pdf(x)
    
    return ProbabilityDensityCurve(pdf, (integration_interval[0], integration_interval[1]))


