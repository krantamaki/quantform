"""@package quantform.pylib.equity.pricer.MonteCarloPricer
@author Kasper Rantamäki
Submodule for a generic Monte Carlo pricer for various stochastic processes and boundary conditions
"""
from typing import Callable, Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt

from .EquityPricerABC import EquityPricerABC
from ..stochastic_process.EquityPriceProcessABC import EquityPriceProcessABC
from ...QfDate import QfDate


def __trivial_lower_boundary(time_to_maturity: float) -> Tuple[float, float]:
  """
  
  """
  return (0., 0.)


def __trivial_expiration_boundary(equity_price: float) -> float:
  """
  
  """
  return equity_price


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

    if expiration_boundary is not None:
      assert maturity_date is not None, "If the expiration boundary is defined, the maturity date must be as well!"

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

  
  def __call__(self, report_date: QfDate, underlying_value: float, save_paths: Optional[bool] = False,
               n_simulations: Optional[int] = 1000, n_steps: Optional[int] = 1000) -> float:
    """
    TODO
    """

    # Define the max simulation time as either until the maturity date or 100 years from the report date
    years = report_date.time_delta(self.__maturity_date, convention="trading") if self.__maturity_date is not None else 100

    discounted_payoffs = []
    simulation_paths   = [[] * n_simulations]

    for simulation_i in range(0, n_simulations):
      for step_years, step_price in self.__price_process(underlying_value, years, n_steps):

        if save_paths:
          simulation_paths[simulation_i].append((step_years, step_price))

        if step_years >= years:
          discounted_payoffs.append(self.__discount(step_years, self.__expiration_boundary(step_price)))
          break
        
        in_bounds, payoff = self.__in_bounds(step_years, step_price)

        if not in_bounds:
          discounted_payoffs.append(self.__discount(step_years, payoff))
          break

    if save_paths:
      self.__simulation_paths = simulation_paths
        
    return np.mean(discounted_payoffs)


  def __discount(self, time_to_maturity: float, cashflow: float) -> float:
    """
    
    """
    return cashflow * np.exp(-self.__rf * time_to_maturity)


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


  def plot_simulation_paths(self) -> plt.Figure:
    """
    TODO
    """
    pass

