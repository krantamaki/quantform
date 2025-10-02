"""@package quantform.pylib.curve.ImpliedVolatilityCurve
@author Kasper Rantamäki
A submodule for computing the implied volatility curve for a given set of options
"""
import numpy as np
from typing import List

# from ..equity.derivative.Option import Option
# from ..equity.pricer.BlackScholesPricer import BlackScholesPricer
from .GenericCurve import GenericCurve
from ..QfDate import QfDate


class ImpliedVolatilityCurve(GenericCurve):
  """Implied volatility curve calculated from a set of options"""
  
  def __init__(self, options: List[callable], underlying_value: float, report_date: QfDate, apply_gaussian_filter: bool = False, 
               gaussian_filter_sd: float = 2.) -> None:
    """Constructor method
    
    Constructor method that calculates the implied volatilities for the options and initializes a CubicSpline object based 
    on them. It is up to the user to make sure the value of the underlying and the report date used in calculating the 
    implied volatility are correct for the options market price. Additionally, if wanted runs a Gaussian filter on the datapoints 
    to smooth the data.
    
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
    assert len(set([option.maturity_date for option in options])) == 1, f"The options must have the same maturity date! (Found maturity dates: {set([option.maturity_date for option in options])})"

    try:
      volatilities = np.array([option.pricer.implied_volatility(option.market_price, underlying_value, report_date) for option in options])
    except AttributeError as e:
      assert False, f"Only BlackScholesPricer implements the implied volatility method! ({e})"
    
    strikes = np.array([option.strike for option in options])
    
    # Note that constant extrapolation is used. This is in line with discussion by Carr and Wu (2008) (https://academic.oup.com/rfs/article-abstract/22/3/1311/1581057)
    super().__init__(strikes, volatilities, apply_gaussian_filter=apply_gaussian_filter, gaussian_filter_sd=gaussian_filter_sd, extrapolation_method="Constant")

