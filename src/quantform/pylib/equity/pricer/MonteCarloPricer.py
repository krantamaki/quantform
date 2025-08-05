"""@package quantform.pylib.equity.pricer.MonteCarloPricer
@author Kasper Rantamäki
Submodule for a generic Monte Carlo pricer for various stochastic processes and boundary conditions
"""
from typing import Callable, Optional, Tuple, Union
import numpy as np
import matplotlib.pyplot as plt

from .EquityPricerABC import EquityPricerABC
from ..stochastic_process.EquityPriceProcessABC import EquityPriceProcessABC
from ...QfDate import QfDate
from ..boundaries import trivial_lower_boundary, trivial_expiration_boundary
from ..utils import discount


class MonteCarloPricer(EquityPricerABC):
  """
  TODO
  """

  def __init__(self, price_process: EquityPriceProcessABC, risk_free_rate: float,  
               maturity_date: Optional[QfDate] = None, expiration_boundary: Optional[Callable[[float], float]] = None,
               upper_boundary: Optional[Callable[[float], Tuple[float, float]]] = None, 
               lower_boundary: Optional[Callable[[float], Tuple[float, float]]] = None) -> None:
    """
    TODO
    """
    self.__price_process = price_process
    self.__rf            = risk_free_rate

    if maturity_date is not None:
      assert expiration_boundary is not None, "If the maturity date is defined the expiration boundary should be as well!"

    if expiration_boundary is None:
      assert upper_boundary is not None or lower_boundary is not None, "At least one boundary must be defined!"

    self.__maturity_date  = maturity_date
    self.__upper_boundary = upper_boundary

    if expiration_boundary is None:
      self.__expiration_boundary = __trivial_expiration_boundary
    else:
      self.__expiration_boundary = expiration_boundary

    if lower_boundary is None:
      self.__lower_boundary = __trivial_lower_boundary
    else:
      self.__lower_boundary = lower_boundary

    self.__simulation_paths = None

  
  def __call__(self, report_date: QfDate, underlying_value: float, save_paths: bool = False, 
               n_simulations: int = 1000, n_steps: int = 1000, return_estimate_error: bool = False, 
               process_vol: float = None) -> Union[float, Tuple[float, float]]:
    """
    TODO
    """

    # Define the max simulation time as either until the maturity date or 100 years from the report date
    years = report_date.time_delta(self.__maturity_date, convention="trading") if self.__maturity_date is not None else 100

    discounted_payoffs = []
    simulation_paths   = [[] * n_simulations]

    for simulation_i in range(0, n_simulations):
      for step_years, step_price in self.__price_process(underlying_value, years, n_steps, vol=process_vol):

        if save_paths:
          simulation_paths[simulation_i].append((step_years, step_price))

        if step_years >= years:
          discounted_payoffs.append(self.discount(step_years, self.__expiration_boundary(step_price)))
          break
        
        in_bounds, payoff = self.__in_bounds(step_years, step_price)

        if not in_bounds:
          discounted_payoffs.append(self.discount(step_years, payoff))
          break

    if save_paths:
      self.__simulation_paths = simulation_paths
      
    mean = np.mean(discounted_payoffs)
    std  = np.std(discounted_payoffs)
    
    if return_estimate_error:
      return (mean, std / np.sqrt(n_simulations))
        
    return mean


  def __in_bounds(self, years: float, price: float) -> Tuple[bool, Optional[float]]:
    """
    TODO
    """

    above_lower = price > self.__lower_boundary(years)[0]

    if not above_lower:
      return (False, self.__lower_boundary(years)[1])
    
    if self.__upper_boundary is not None:
      below_upper = price < self.__upper_boundary(years)[0]

      if not below_upper:
        return (False, self.__upper_boundary(years)[1])

    return (True, None)
  
  
  def delta(self, report_date: QfDate, underlying_value: float, difference: float = 1e-6,
            n_simulations: int = 1000, n_steps: int = 1000, return_estimate_error: bool = False) -> Union[float, Tuple[float, float]]:
    """
    
    """
    
    if return_estimate_error:
      forward  = self(report_date, underlying_value + difference / 2, n_simulations=n_simulations, n_steps=n_steps, return_estimate_error=True)
      backward = self(report_date, underlying_value - difference / 2, n_simulations=n_simulations, n_steps=n_steps, return_estimate_error=True)
      return ((forward[0] - backward[0]) / difference, forward[0] + backward[0])
      
    return (self(report_date, underlying_value + difference / 2, n_simulations=n_simulations, n_steps=n_steps) - \ 
            self(report_date, underlying_value - difference / 2, n_simulations=n_simulations, n_steps=n_steps)) \ / 
           difference
    
    
  def vega(self, report_date: QfDate, underlying_value: float, difference: float = 1e-6,
          n_simulations: int = 1000, n_steps: int = 1000, return_estimate_error: bool = False) -> Union[float, Tuple[float, float]]:
    """
    
    """

    vol = self.__price_process.volatility
    
    if return_estimate_error:
        forward  = self(report_date, underlying_value, n_simulations=n_simulations, n_steps=n_steps, return_estimate_error=True, process_vol=vol + difference / 2)
        backward = self(report_date, underlying_value, n_simulations=n_simulations, n_steps=n_steps, return_estimate_error=True, process_vol=vol - difference / 2)
        return ((forward[0] - backward[0]) / difference, forward[1] + backward[1])
        
      return (self(report_date, underlying_value, n_simulations=n_simulations, n_steps=n_steps, process_vol=vol + difference / 2) - \ 
              self(report_date, underlying_value, n_simulations=n_simulations, n_steps=n_steps, process_vol=vol - difference / 2)) \ / 
            difference
    

  def gamma(self, report_date: QfDate, underlying_value: float, difference: float = 1e-6,
            n_simulations: int = 1000, n_steps: int = 1000, return_estimate_error: bool = False) -> Union[float, Tuple[float, float]]:
    """
    
    """
    if return_estimate_error:
        forward  = self(report_date, underlying_value + difference, n_simulations=n_simulations, n_steps=n_steps, return_estimate_error=True)
        backward = self(report_date, underlying_value - difference, n_simulations=n_simulations, n_steps=n_steps, return_estimate_error=True)
        central  = self(report_date, underlying_value, n_simulations=n_simulations, n_steps=n_steps, return_estimate_error=True)
        return ((forward[0] - 2 * central[0] +  backward[0]) / difference ** 2, forward[1] + backward[1] + 2 * central[1] )
        
      return (self(report_date, underlying_value + difference, n_simulations=n_simulations, n_steps=n_steps) - \ 
              2 * self(report_date, underlying_value, n_simulations=n_simulations, n_steps=n_steps)) + \
              self(report_date, underlying_value - difference, n_simulations=n_simulations, n_steps=n_steps) / \
            difference ** 2


  def plot_simulation_paths(self) -> plt.Figure:
    """
    TODO
    """
    pass

