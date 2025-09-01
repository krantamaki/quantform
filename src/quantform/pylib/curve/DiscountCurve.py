"""@package quantform.pylib.curve.DiscountCurve
@author Kasper Rantamäki
TODO
"""
import numpy as np

from .GenericCurve import GenericCurve


class DiscountCurve(GenericCurve):
  """TODO"""
  
  def __init__(self, time_to_maturities: np.ndarray, yields: np.ndarray) -> None:
    """Constructor method
    
    TODO
    
    @param time_to_maturities  The times to maturity in years
    @param yields              The discount rates (yields)
    @return                    None
    """
    super().__init__(time_to_maturities, yields, apply_gaussian_filter=False)
    
    
  def discount(self, time_to_maturity: float, amount: float = 1.) -> float:
    """
    TODO
    """
    return amount * np.exp(-self(time_to_maturity) * time_to_maturity)
  
