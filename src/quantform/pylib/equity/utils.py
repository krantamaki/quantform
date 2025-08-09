"""@package quantform.pylib.equity.utils
@author Kasper Rantamäki
TODO
"""
from typing import Optional, Tuple, Callable
import numpy as np

from .QfDate import QfDate


__all__ = ["discount", "parse_option_id", "form_option_id"]


def discount(cashflow: float, time_to_maturity: float, rf: float) -> float:
  """
  TODO
  """
  return cashflow * np.exp(-rf * time_to_maturity)
  

def parse_option_id(contract_id: str) -> Tuple[str, QfDate, Literal['Call', 'Put'], float]:
  """
  TODO
  """

  strike = float(f"{contract_name[-8:-3]}.{contract_name[-3:]}")

  if contract_name[-9] == 'C':
    option_type = 'Call'
  else:
    option_type = 'Put'

  maturity_date_str = contract_name[-15:-9]
  maturity_date = QfDate(...)
  
  underlying = contract_name[:-15]

  return (underlying, maturity_date, option_type, strike)


def form_option_id(underlying: str, maturity_date: QfDate, option_type: Literal['Call', 'Put'], strike: float) -> str:
  """
  TODO
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

