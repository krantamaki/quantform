"""@package quantform.pylib.CurveABC
@author Kasper Rantamäki
Submodule with a generic abstract base class for various curves
"""
from typing import Optional, Tuple
from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt


class CurveABC(ABC):
  """Abstract base class for generic curves"""

  @abstractmethod
  def __call__(self, val: float) -> float:
    """Call method
    
    Call method that returns the value on the curve for a given point
    
    @param val  The value for which the curve point is wanted
    @return     The point on the curve
    """
    pass
  
  
  @abstractmethod
  @property
  def max(self) -> float:
    """The maximum value for which the curve is defined"""
    pass
  
  
  @abstractmethod
  @property
  def min(self) -> float:
    """The minimum value for which the curve is defined"""
    pass
  

  def plot(self, n_points: int, value_range: Optional[Tuple[float, float]], fig: Optional[plt.Figure] = None, 
           ax: Optional[plt.Axes] = None, linewidth: float = 1, label: str = '', show_fig_legend: bool = False,
           save_as: Optional[str] = None, ) -> plt.Figure:
    """Plotting function
    
    Function for plotting the curve on a given interval
    
    @param n_points         The number of points on which the curve is evaluated
    @param value_range      The range of value on which the curve is evaluated. Optional, defaults to using the 
                            minimum and maximum values for which the curve is defined.
    @param fig              A pyplot Figure object to which the plot is to be added. Optional, defaults to 
                            None i.e. new Figure object is created
    @param ax               A pyplot Axes object specifying to which the plot is added. Optional, defaults to
                            None i.e. no Axes object is used
    @param linewidth        The linewidth for the line plot. Optional, defaults to 1
    @param label            The label for the curve. Optional, defaults to '' (empty string)
    @param show_fig_legend  Boolean flag specifying if the legend is shown on the figure. Optional, defaults to False
    @param save_as          The path (as a str object) specifying the path to which the figure is saved. Optional,
                            defaults to None i.e. the figure is not saved.
    @return                 The Figure object with the curve plotted on it
    """
    
    if value_range is None:
      value_range = (self.min, self.max)

    xx = np.linspace(value_range[0], value_range[1], n_points)
    yy = np.array([self(x) for x in xx])

    if fig is None:
      fig = plt.figure(figsize=(12, 6))

    if ax is not None:
      ax.plot(xx, yy, linewidth=linewidth, label=label)
    else:
      plt.plot(xx, yy, linewidth=linewidth, label=label)

    if show_fig_legend:
      fig.legend()

    if save_as is not None:
      fig.savefig(save_as)
      
    return fig
  
