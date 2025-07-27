"""@package quantform.pylib.risk_management.VaR
@author Kasper Rantamäki
Submodule implementing some Value-at-Risk calculations for wanter 
market variables
"""
from typing import Optional, List, Literal, Tuple
from math import floor, sqrt
from itertools import product
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


class VaR:
  """
  Class implementation of different methods for calculating the Value-at-Risk measure. The VaR calculations
  in this class are based on Chapter 22 in the book 'Options, Futures and Other Derivatives' (ninth edition)
  by Hull.
  """

  def __init__(self, historical_data: pd.DataFrame, quantities: Optional[List[float]] = None, cov: Optional[np.ndarray] = None) -> None:
    """Constructor

    Default constructor that stores the given parameters as instance variables and does some basic
    calculations in preparation for calls to the instance. Note that it is recommended that the covariance matrix
    is passed as a parameter as otherwise a naive approach will be taken to calculate it. For different ways
    of approximating covariance see Chapter 23 in 'Options, Futures and Other Derivatives' (ninth edition)
    by Hull.

    @param historical_data  The historical values of the market variables. Generally, it is recommended
                            that the values are for unit amount of the variable and the portfolio specific
                            quantities are passed as the 'quantities' parameter. The amounts are assumed to
                            be denoted in the same currency. The oldest values should be on row index 0 and newest
                            on row index -1.
    @param quantities       The quantities of the market variables in the portfolio. Optional and if not passed
                            the values from historical data are assumed not to be for unit amount.
    @param cov              The covariance matrix between the market variables. Optional, defaults to None, i.e. naive
                            covariance matrix will be used.
    @raises RuntimeError    Raised if the percentage changes or the covariance matrix cannot be calculated
    @return                 None
    """

    self.__data            = historical_data
    self.__scenario_losses = None
    self.__cov             = cov

    if quantities is None:
      self.__quantities = np.array([1.] * self.__data.shape[1])
    else:
      assert len(quantities) == self.__data.shape[1], f"Data and quantity dimensions don't match! ({len(quantities)} != {self.__data.shape[1]})"
      self.__quantities = np.array(quantities)

    try:
      self.__returns = historical_data.pct_change()

      if cov is None:
        self.__cov = self.__returns.cov().to_numpy()

      self.__portfolio_var = self.__quantities.T @ self.__cov @ self.__quantities
    except Exception as e:
      raise RuntimeError(f"Invalid historical data given! (Error: {e})")
  

  def __call__(self, model: Literal["historical", "linear", "quadratic"], time_horizon: int, confidence_level: float,) -> float:
    """Call method

    Call method that calculates the VaR value using the specified model, for the given time horizon and 
    confidence level. Note! The quadratic model is not yet implemented and will raise a NotImplementedError.

    @param model             The chosen model used in calculating the VaR measure. Options are 'historical', 'linear'
                             and 'quadratic'
    @param time_horizon      The number of days 'N' over which the loss level is evaluated
    @param confidence_level  The level 'X' corresponding to the (100-X)th percentile of the distribution of the loss in the
                             value of the portfolio over the next 'N' days
    @raises RuntimeError     Raised if an invalid model name is passed
    @return                  The value of the VaR measure
    """

    if model.lower()   == "historical":
      return self.__historical(time_horizon, confidence_level)
    
    elif model.lower() == "linear":
      return self.__linear(time_horizon, confidence_level)

    elif model.lower() == "quadratic":
      return self.__quadratic(time_horizon, confidence_level)
    
    else:
      raise RuntimeError(f"Invalid model name '{model}' passed!")
    

  def __historical(self, time_horizon: int, confidence_level: float) -> float:
    """Historical simulation VaR

    VaR measure calculated based on historical returns. The returns for each day are considered
    as a possible future scenario for which the loss level is evaluated. The loss levels found this
    way are ordered and the percentile losses corresponding with the given confidence level is returned 
    as the VaR value.

    @param time_horizon      The number of days 'N' over which the loss level is evaluated
    @param confidence_level  The level 'X' corresponding to the (100-X)th percentile of the distribution of the loss in the
                             value of the portfolio over the next 'N' days
    @return                  The value of the VaR measure
    """

    if self.__scenario_losses is None:
      scenarios = self.__data.iloc[-1, :] * (self.__returns + 1)
      self.__scenario_losses = ((scenarios - self.__data.iloc[-1, :]) * self.__quantities).sum(axis=1).to_numpy().sort()
    
    percentile_index = floor(len(self.__scenario_losses) * (1 - confidence_level))

    return sqrt(time_horizon) * self.__scenario_losses[percentile_index]


  def __linear(self, time_horizon: int, confidence_level: float) -> float:
    """Linear model VaR
    
    VaR measure calculated by assuming that the market variables follow a joint multivariate normal distribution, meaning
    that the portfolio value follows a normal distribution. The VaR value is then found by using the cumulative normal
    distribution, with the portfolio variance and zero mean.

    @param time_horizon      The number of days 'N' over which the loss level is evaluated
    @param confidence_level  The level 'X' corresponding to the (100-X)th percentile of the distribution of the loss in the
                             value of the portfolio over the next 'N' days
    @return                  The value of the VaR measure
    """
    return sum(self.__data.iloc[-1, :].to_numpy()) * \
           norm.cdf(1 - confidence_level, loc=0, scale=sqrt(self.__portfolio_var)) * \
           sqrt(self.__portfolio_var * time_horizon) 
  

  def __quadratic(self, time_horizon: int, confidence_level: float) -> float:
    """
    TODO: Description
    """
    raise NotImplementedError("The quadratic model has not yet been implemented!")


  def stressed_var(self, time_horizon: int, confidence_level: float, standard_deviation: float) -> float:
    """Stressed linear model VaR

    Linear model VaR measure with a given standard deviation. Can be used to test how the portfolio
    would have fared, if it had a standard deviation other than the one calculated from historical
    data.

    @param time_horizon        The number of days 'N' over which the loss level is evaluated
    @param confidence_level    The level 'X' corresponding to the (100-X)th percentile of the distribution of the loss in the
                               value of the portfolio over the next 'N' days
    @param standard_deviation  The given portfolio standard deviation
    @return                    The value of the VaR measure
    """
    return sum(self.__data.iloc[-1, :].to_numpy()) * \
           norm.cdf(1 - confidence_level, loc=0, scale=sqrt(standard_deviation)) * \
           sqrt(standard_deviation * time_horizon) 


  def plot(self, model: Literal["historical", "linear", "quadratic"], time_horizon: int, n_levels: int, 
           level_range: Tuple[float, float] = (0., 1.), fig: Optional[plt.Figure] = None, ax: Optional[plt.Axes] = None, 
           linewidth: float = 1, label: str = '', show_fig_legend: bool = False, save_as: Optional[str] = None) -> plt.Figure:
    """Plot method

    Plots the VaR measure values given by the chosen model for various confidence levels. Note that 
    for a large number of confidence levels this method can take a while.

    @param model            The chosen model used to calculate VaR values
    @param time_horizon     The number of days over which the loss level is evaluated
    @param n_levels         The number of confidence levels for which the VaR is calculated
    @param level_range      The range of confidence levels for which the VaR is calculated. Optional, defaults to (0, 1)
    @param fig              The figure in which the plot is added. Optional, defaults to None, i.e. new figure is created
    @param ax               The ax in the given figure in which the plot is added. Optional, defaults to None, i.e. no axis used
    @param linewidth        The linewidth of the plot. Optional, defaults to 1
    @param label            The label given to the plot. Optional, defaults to '' 
    @param show_fig_legend  Boolean flag telling if the legend should be added to the figure. Optional, defaults to False.
    @param save_as          The path to which the figure is saved. Optional, defaults to None i.e. the figure is not saved
    @return                 The updated figure
    """

    xx = np.linspace(level_range[0], level_range[1], n_levels)
    yy = np.array([self(model, time_horizon, x) for x in xx])

    if fig is None:
      fig = plt.figure(figsize=(7, 5))

    if ax is not None:
      ax.plot(xx, yy, linewidth=linewidth, label=label)
    else:
      plt.plot(xx, yy, linewidth=linewidth, label=label)

    if show_fig_legend:
      fig.legend()

    if save_as is not None:
      fig.savefig(save_as)

    return fig


  def plot_scenario_histogram(self, n_bins, fig: Optional[plt.Figure] = None, ax: Optional[plt.Axes] = None, 
                              label: str = '', show_fig_legend: bool = False, save_as: Optional[str] = None) -> plt.Figure:
    """Historical scenario histogram visualization

    Plots a histogram for the 1-day losses (or gains) based on the historical data. 
    
    @param n_bins           The number of equal width bars in the histogram
    @param fig              The figure in which the plot is added. Optional, defaults to None, i.e. new figure is created
    @param ax               The ax in the given figure in which the plot is added. Optional, defaults to None, i.e. no axis used
    @param label            The label given to the plot. Optional, defaults to '' 
    @param show_fig_legend  Boolean flag telling if the legend should be added to the figure. Optional, defaults to False.
    @param save_as          The path to which the figure is saved. Optional, defaults to None i.e. the figure is not saved
    @return                 The updated figure
    """

    # If the historical method has not been called yet, call it so that the scenario losses get calculated
    if self.__scenario_losses is None:
      self("historical", 0.99, 1)
    
    if fig is None:
      fig = plt.figure(figsize=(7, 5))

    if ax is not None:
      ax.hist(self.__scenario_losses, bins=n_bins, label=label)
    else:
      plt.hist(self.__scenario_losses, bins=n_bins, label=label)

    if show_fig_legend:
      fig.legend()

    if save_as is not None:
      fig.savefig(save_as)

    return fig
  