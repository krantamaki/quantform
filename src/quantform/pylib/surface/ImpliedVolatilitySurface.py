"""@package quantform.pylib.surface.ImpliedVolatilitySurface
@author Kasper Rantamäki
A submodule for computing the implied volatility surface for a given set of options
"""
import numpy as np
from typing import List, Tuple, Optional

from ..equity.derivative.Option import Option
from .GenericSurface import GenericSurface
from ..curve import ImpliedVolatilityCurve
from ..QfDate import QfDate


class ImpliedVolatilitySurface(GenericSurface):
  """Implied volatility surface calculated from a set of options"""
  
  def __init__(self, options: List[Option], underlying_value: float, report_date: QfDate, interp_range: Optional[Tuple[float, float]] = None,
               extrap_range: Optional[Tuple[float, float]] = None, n_points: int = 100, apply_gaussian_filter: bool = False, gaussian_filter_sd: float = 2.) -> None:
    """Constructor method
    
    Constructor method that calculates the implied volatilities for the options and initializes a CloughTocher2DInterpolator object based 
    on them. It is up to the user to make sure the value of the underlying and the report date used in calculating the 
    implied volatility are correct for the options market price. Additionally, if wanted runs a Gaussian filter on the datapoints 
    to smooth the data.
    
    Once the object is initialized it can be called with a tuple (<value of underlying>, <time from report date in years>).
    
    @param options                The options from which the implied volatility curve is interpolated. The options must
                                  have been initialized with the 'market_price' parameter.
    @param underlying_value       The value of the underlying at the time of option valuation
    @param report_date            The date for which the value of the underlying is quoted
    @param interp_range           The range over which volatilities are interpolated range used. Optional, defaults to None i.e. using all available options
    @param extrap_range           The range over which volatilities are inter- and extrapolated. Optional, defaults to None i.e. not extrapolating
    @param n_points               The number of uniformly distributed points in the strike range for which volatility is inter- and extrapolated. 
                                  Optional, defaults to 100
    @param apply_gaussian_filter  Boolean flag specifying if a Gaussian filter should be applied to the datapoints.
                                  Optional, defaults to False
    @param gaussian_filter_sd     The standard deviation for the Gaussian filter if applied. Optional, defaults to 2
    @raises AssertionError        Raised if the market price is not available for any of the options or if the options are 
                                  not for the same underlying and maturing on the same date
    @return                       None
    """
    assert sum([int(option.market_price is not None) for option in options]) == len(options), "The options must have a set market price!"
    assert len(set([option.underlying for option in options])) == 1, f"The options must have the same underlying! (Found underlyings: {set([option.underlying for option in options])})"
  
    used_options = options
  
    if interp_range is None:
      strikes = np.array([option.strike for option in options])
      if extrap_range is None:
        extrap_range = (np.min(strikes), np.max(strikes))
    else:
      used_options = [option for option in options if option.strike >= interp_range[0] and option.strike <= interp_range[1]]
      if extrap_range is None:
        extrap_range = interp_range
      
    # Group the options by maturity date
    maturity_dict = {}
    for option in used_options:
      if option.maturity_date not in maturity_dict:
        maturity_dict[option.maturity_date] = [option]
      else:
        maturity_dict[option.maturity_date].append(option)
      
    # Form ImpliedVolatilityCurve objects for each maturity
    curve_dict = {}
    for maturity_date, date_options in maturity_dict.items():
      curve_dict[maturity_date] = ImpliedVolatilityCurve(date_options, underlying_value, report_date, apply_gaussian_filter=apply_gaussian_filter, gaussian_filter_sd=gaussian_filter_sd)
      
    # Use the implied volatility curves to calculate the points passed to the GenericSurface class
    volatilities = []
    points       = []
    strikes = np.linspace(extrap_range[0], extrap_range[1], n_points)
    
    for maturity_date, curve in curve_dict.items():
      taus = [report_date.timedelta(maturity_date)] * n_points
      points += zip(strikes, taus)
      volatilities += [curve(strike) for strike in strikes]
    
    super().__init__(points, volatilities, apply_gaussian_filter=False)

