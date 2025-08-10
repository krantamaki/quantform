"""@package quantform.pylib.equity.utils
@author Kasper Rantamäki
Module with general utility functions
"""
from typing import Tuple, Callable, Literal
import numpy as np

from ..QfDate import QfDate


__all__ = ["discount", "parse_option_id", "form_option_id", "bisection_method"]


def discount(risk_free_rate: float, time_to_maturity: float, cashflow: float = 1.) -> float:
  """Simple function that computes the discounted cashflow
  
  @param risk_free_rate    The annualised risk-free (discount) rate that matches the time to maturity
  @param time_to_maturity  The time to maturity in years
  @param cashflow          The cashflow to be discounted. Optional, defaults to 1 i.e. only the discount factor is calculated
  @return                  The discounted cashflow
  """
  return cashflow * np.exp(-risk_free_rate * time_to_maturity)
  

def parse_option_id(contract_id: str, calendar: Literal["Eurex", "Frankfurt", "Xetra", "London", "NYSE"] = "Frankfurt", 
                    convention: Literal["30/360", "ACT/365", "ACT/360", "Business/252"] = "Business/252") -> Tuple[str, QfDate, Literal['Call', 'Put'], float]:
  """Function for breaking an option id (e.g. 'AAPL250815C00237500') into it's constituent parts
  
  @param contract_id  The option identifier to be parsed
  @param calendar     The name of the calendar used with the maturity date. Optional, defaults to 'Frankfurt'
  @param convention   The day count convention used with the maturity date. Optional, defaults to 'Business/252'
  @return             A tuple containing the constituent parts
  """

  strike = float(f"{contract_id[-8:-3]}.{contract_id[-3:]}")

  if contract_id[-9] == 'C':
    option_type = 'Call'
  else:
    option_type = 'Put'

  maturity_date_str = contract_id[-15:-9]
  maturity_date = QfDate(2000 + int(maturity_date_str[:2]), 
                         int(maturity_date_str[2:4]),
                         int(maturity_date_str[4:]),
                         calendar,
                         convention)
  
  underlying = contract_id[:-15]

  return (underlying, maturity_date, option_type, strike)


def form_option_id(underlying: str, maturity_date: QfDate, option_type: Literal['Call', 'Put'], strike: float) -> str:
  """Function for forming a option id (e.g. 'AAPL250815C00237500') from it's constituent parts
  
  @param underlying   The identifier (ticker) for the underlying 
  @param mature_date  The maturity (expiration) date for the option
  @param option_type  The type of option ('Call' or 'Put')
  @param strike       The strike price for the option
  """

  contract_name = ""

  strike_split = f"{strike:.3f}".split('.')
  contract_name = f"{strike_split[0].rjust(5, '0')}{strike_split[1].ljust(3, '0')}" + contract_name

  if option_type == 'Call':
    contract_name = 'C' + contract_name
  else:
    contract_name = 'P' + contract_name

  contract_name = f"{maturity_date.year - 2000}{str(maturity_date.month).rjust(2, '0')}{str(maturity_date.day).rjust(2, '0')}" + contract_name

  return underlying + contract_name


def bisection_method(func: Callable, lower: float, upper: float, tol: float = 1e-6) -> float:
  """Generic bisection method for finding the root of a function
  
  @param func             The function which root is to be found
  @param lower            The lower bound for the search interval
  @param upper            The upper bound for the search interval
  @paral tol              The tolerance to which the search is continued
  @raises AssertionError  Raised if the lower and upper bounds are invalid
  @return                 The root of the function
  """

  assert upper > lower, f"Upper bound should be greater than lower bound! ({upper} !> {lower})"
  assert func(upper) > 0 and func(lower) < 0, f"The upper and lower bound should get different signs from function 'func'! (sign({func(upper)}) == sign({func(lower)}))"
  
  while upper - lower > tol:
      mid = (upper + lower) / 2.
      
      if func(mid) < 0.:
          lower = mid
      elif func(mid) > 0:
          upper = mid
      else:
          return mid
      
  return (upper + lower) / 2.

