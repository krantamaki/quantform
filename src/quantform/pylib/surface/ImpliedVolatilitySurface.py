"""@package quantform.pylib.surface.ImpliedVolatilitySurface
@author Kasper Rantamäki
A submodule for computing the implied volatility surface for a given set of options
"""
import numpy as np
from typing import List

from ..equity.derivative.Option import Option
from .GenericSurface import GenericSurface
from ..QfDate import QfDate


class ImpliedVolatilitySurface(GenericSurface):
  """Implied volatility surface calculated from a set of options"""
  
  def __init__(self, options: List[Option], underlying_value: float, report_date: QfDate, apply_gaussian_filter: bool = False, 
               gaussian_filter_sd: float = 2.) -> None:
    """Constructor method
    
    Constructor method that calculates the implied volatilities for the options and initializes a CloughTocher2DInterpolator object based 
    on them. It is up to the user to make sure the value of the underlying and the report date used in calculating the 
    implied volatility are correct for the options market price. Additionally, if wanted runs a Gaussian filter on the datapoints 
    to smooth the data.
    
    Once the object is initialized it can be called with a tuple (<value of underlying>, <time from report date in years>).
    
    @param options                The options from which the implied volatility curve is interpolated. The options must
                                  have been initialized with the 'market_price' parameter.
    @param underlying_value       The value of the underlying at the time of option valuation
    @param apply_gaussian_filter  Boolean flag specifying if a Gaussian filter should be applied to the datapoints.
                                  Optional, defaults to False
    @param gaussian_filter_sd     The standard deviation for the Gaussian filter if applied. Optional, defaults to 2
    @raises AssertionError        Raised if the market price is not available for any of the options or if the options are 
                                  not for the same underlying and maturing on the same date
    @return                       None
    """
    assert sum([int(option.market_price is not None) for option in options]) == len(options), "The options must have a set market price!"
    assert len(set([option.underlying for option in options])) == 1, f"The options must have the same underlying! (Found underlyings: {set([option.underlying for option in options])})"
  
    # Note that the order doesn't matter as the GenericSurface object will sort the arrays anyways
    volatilities = np.array([option.implied_volatility(underlying_value, report_date) for option in options])
    strikes      = np.array([option.strike for option in options])
    taus         = np.array([report_date.time_delta(option.maturity_date, convention = "trading") for option in options])
    
    super.__init__(np.append(strikes, taus, 1), volatilities, apply_gaussian_filter=apply_gaussian_filter, gaussian_filter_sd=gaussian_filter_sd)

