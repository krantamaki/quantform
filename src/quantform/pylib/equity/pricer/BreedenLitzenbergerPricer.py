"""
TODO
"""
from typing import List, Dict, Literal

from .EquityPricerABC import EquityPricerABC
from .BlackScholesPricer import BlackScholesPricer
from ...curve import ProbabilityDensityCurve
from ...QfDate import QfDate


class BreedenLitzenbergerPricer(EquityPricerABC):
  """
  """
  
  def __init__(self, volatility_surface: ImpliedVolatilitySurface, option_pricer: Literal["BlackScholes"], risk_free_rate: float,  
               maturity_date: Optional[QfDate] = None, expiration_boundary: Optional[Callable[[float], float]] = None,
               upper_boundary: Optional[Callable[[float], Tuple[float, float]]] = None, 
               lower_boundary: Optional[Callable[[float], Tuple[float, float]]] = None) -> None:
    """
    """
    pass
    
    
  def __call__(self, report_date: QfDate, underlying_value: float, *args: List[any], **kwargs: Dict[any]):
    """
    TODO
    """
    pass
  

  def delta(self, report_date: QfDate, underlying_value: float, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    pass
  

  def vega(self, report_date: QfDate, underlying_value: float, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    pass
    

  def gamma(self, report_date: QfDate, underlying_value: float, *args: List[any], **kwargs: Dict[any]) -> float:
    """
    TODO
    """
    pass
  
  
  @property 
  def implied_pdf(self) -> ProbabilityDensityCurve:
    """
    """
    pass
   
    