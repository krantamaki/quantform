"""@package quantform.pylib.surface.ImpliedVolatilitySurface
@author Kasper Rantamäki
A submodule for computing the implied volatility surface for a given set of options
"""
import numpy as np
from typing import Tuple, Optional
from itertools import product

from ..equity.derivative.EquityDerivativeABC import EquityDerivativeABC
from .GenericSurface import GenericSurface
from ..QfDate import QfDate


class PriceSurface(GenericSurface):
  """Price surface calculated for a given derivative"""
  
  def __init__(self, derivative: EquityDerivativeABC, n_points: Tuple[int, int], n_days_back: int = 252, 
               max_underlying_value: Optional[int] = None,
               min_underlying_value: int = 0,
               end_date: Optional[QfDate] = None) -> None:
    """Constructor method
    
    Constructor method that calculates the value of the given derivative in the specified points and initializes a CloughTocher2DInterpolator object based 
    on them.
    
    @param n_points              The number of points on the 'time to maturity' and 'underlying value' dimensions on which the surface is evaluated as a tuple
    @param n_days_back           The number of days back from the maturity date for which the derivative is priced. Optional, defaults to 252 (one year in trading days)
    @param max_underlying_value  The maximum value of the underlying for which the derivative is priced. Optional, defaults to None i.e. 2 times the strike is used.
                                 If the derivative has no strike price the parameter must be specified
    @param end_date              The end date for pricing. Optional, defaults to None i.e. the maturity date being used. If the derivative has no maturity date
                                 the parameter must be specified
    @return                      None
    """
    max_underlying_value = max_underlying_value if max_underlying_value is not None else 2 * derivative.strike
    end_date             = end_date if end_date is not None else derivative.maturity_date
    
    start_date = end_date - n_days_back
    time_to_maturity = float(str(start_date.timedelta(end_date))[:4])
    
    xx = np.linspace(0, time_to_maturity, n_points[0])
    yy = np.linspace(min_underlying_value, max_underlying_value, n_points[1])

    xy = np.array(list(product(xx, yy)))
    vals = np.array([derivative(tup[1], start_date * tup[0]) for tup in xy]) 
    
    super().__init__(xy, vals)

