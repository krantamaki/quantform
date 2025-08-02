"""@package quantform.pylib.equity.boundaries
@author Kasper Rantamäki
Submodule with various boundary function factories and 
"""
from typing import Callable, Tuple
import numpy as np


__all__ = ["futures_boundary_factory",
           "call_option_boundary_factory",
           "put_option_boundary_factory",
           "constant_boundary_factory",
           "out_boundary_factory",
           "trivial_lower_boundary",
           "trivial_expiration_boundary"]


def futures_boundary_factory(strike: float, short_position: bool = False) -> Callable[[float], float]:
  """Expiration boundary function factory for a generic futures contract
  
  @param strike          The strike price of the futures contract
  @param short_position  Boolean flag for choosing between short and long position. Defaults to false.
  @return                Function that takes as argument the value of the underlying at expiration and returns the value 
                         of the future
  """
  mult = 1 if not short_position else -1
  
  def func(underlying_value: float) -> float:
    return mult * (underlying_value - strike)
  
  return func


def call_option_boundary_factory(strike: float, short_position: bool = False) -> Callable[[float], float]:
  """Expiration boundary function factory for a call option contract
  
  @param strike          The strike price of the call option
  @param short_position  Boolean flag for choosing between short and long position. Defaults to false.
  @return                Function that takes as argument the value of the underlying at expiration and returns the value 
                         of the call option
  """
  mult = 1 if not short_position else -1
  
  def func(underlying_value: float) -> float:
    return mult * np.max(0., underlying_value - strike)
  
  return func


def put_option_boundary_factory(strike: float, short_position: bool = False) -> Callable[[float], float]:
  """Expiration boundary function factory for a put option contract
  
  @param strike          The strike price of the put option
  @param short_position  Boolean flag for choosing between short and long position. Defaults to false.
  @return                Function that takes as argument the value of the underlying at expiration and returns the value 
                         of the put option
  """
  mult = 1 if not short_position else -1
  
  def func(underlying_value: float) -> float:
    return mult * np.max(0., strike - underlying_value)
  
  return func


def constant_boundary_factory(strike: float, constant_value: float) -> Callable[[float], Tuple[float, float]]:
  """Side boundary factory with a constant payoff
  
  @param strike          The strike price for the boundary
  @param constant_value  The constant value on the boundary
  @return                Function that takes as argument the time to maturity and returns the value of the strike level and the 
                         payoff on the strike level
  """
  def func(time_to_maturity: float) -> float:
    return (strike, constant_value)


def out_boundary_factory(strike: float) -> Callable[[float], Tuple[float, float]]:
  """Side boundary factory with a zero payoff
  
  @param strike          The strike price for the boundary
  @return                Function that takes as argument the time to maturity and returns the value of the strike level and the 
                         payoff on the strike level
  """
  return constant_boundary_factory(strike, 0.)
  
  
def trivial_lower_boundary(time_to_maturity: float) -> Tuple[float, float]:
  """Side boundary function paying zero when the value of the underlying is zero i.e. the company goes to bancruptcy
  
  @param time_to_maturity  The time to maturity for the contract
  @return                  The value of the strike level (zero) and the payoff on the strike level (zero)
  """
  return (0, 0)


def trivial_expiration_boundary(underlying_value: float) -> float:
  """Expiration boundary function paying the value of the underlying at maturity
  
  @param underlying_value  The value of the underlying at the maturity
  @return                  The payoff i.e. the value of the underlying
  """
  return futures_boundary_factory(0.)

