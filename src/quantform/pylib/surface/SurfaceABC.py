"""@package quantform.pylib.surface.SurfaceABC
@author Kasper Rantamäki
Submodule with a generic abstract base class for various surfaces
"""
from typing import Optional, Tuple
from abc import ABC, abstractmethod
from itertools import product
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class SurfaceABC(ABC):
  """Abstract base class for generic surfaces"""

  @abstractmethod
  def __call__(self, point: Tuple[float, float]) -> float:
    """Call method
    
    Call method that returns the value on the surface for a given point
    
    @param point  The point for which the surface value is wanted
    @return       The value on the surface
    """
    pass
  
  
  @abstractmethod
  @property
  def max_x(self) -> float:
    """The maximum 'x' value for which the surface is defined"""
    pass
  
  
  @abstractmethod
  @property
  def min_x(self) -> float:
    """The minimum 'x' value for which the surface is defined"""
    pass
  
  
  @abstractmethod
  @property
  def max_y(self) -> float:
    """The maximum 'y' value for which the surface is defined"""
    pass
  
  
  @abstractmethod
  @property
  def min_y(self) -> float:
    """The minimum 'y' value for which the surface is defined"""
    pass
  

  def plot(self, n_points: Tuple[int, int], value_range: Optional[Tuple[Tuple[float, float], Tuple[float, float]]] = None, 
           plot_heatmap: bool = True, cmap_name: str = 'coolwarm', fig: Optional[plt.Figure] = None, ax: Optional[plt.Axes] = None, 
           linewidth: float = 1, label: str = '', show_fig_legend: bool = False, save_as: Optional[str] = None, **kwargs) -> plt.Figure:
    """Plotting function
    
    Function for plotting the surface on a given interval. Can plot both a heatmap and a 3D surface.
    
    @param n_points         The number of points on the 'x' and 'y' dimensions on which the surface is evaluated as a tuple
    @param value_range      The range of value on which the surface is evaluated. A tuple of tuples the first specifying the range 
                            in 'x' dimension and the second in 'y' dimension. Optional, defaults to using the minimum and maximum 
                            values for which the surface is defined.
    @param plot_heatmap     Boolean flag specifying if a heatmap should be plotted instead of a 3D surface. Optional, defaults to True
    @param cmap_name        The name of the used colormap. See matplotlib.colormaps for possible values. Optional, defaults to 'coolwarm'
    @param fig              A pyplot Figure object to which the plot is to be added. Optional, defaults to 
                            None i.e. new Figure object is created
    @param ax               A pyplot Axes object specifying to which the plot is added. Optional, defaults to
                            None i.e. no Axes object is used
    @param linewidth        The linewidth for the line plot. Optional, defaults to 1
    @param label            The label for the surface. Optional, defaults to '' (empty string)
    @param show_fig_legend  Boolean flag specifying if the legend is shown on the figure. Optional, defaults to False
    @param save_as          The path (as a str object) specifying the path to which the figure is saved. Optional,
                            defaults to None i.e. the figure is not saved.
    @param **kwargs         Additional keyword arguments to be passed to the plotting function
    @return                 The Figure object with the surface plotted on it
    """
    
    if value_range is None:
      value_range = ((self.min_x, self.max_x), (self.min_y, self.max_y))
    
    xx = np.linspace(value_range[0][0], value_range[0][1], n_points[0])
    yy = np.linspace(value_range[1][0], value_range[1][1], n_points[1])

    xy = np.array(list(product(xx, yy)))

    zz = list()

    for tup in xy:
      zz.append(self(tup))

    X = np.reshape(xy[:, 0], n_points)
    Y = np.reshape(xy[:, 1], n_points)
    Z = np.reshape(np.array(zz), n_points)

    if fig is None:
      fig = plt.figure(figsize=(7, 5))

    if plot_heatmap:

      if ax is None:
        ax = plt.axes()
        fig.add_subplot(ax)

      pheatmap = ax.pcolormesh(X, Y, Z, cmap=matplotlib.colormaps[cmap_name], linewidth=linewidth, **kwargs)
      fig.colorbar(pheatmap)

    else:

      if ax is None:
        ax = plt.axes(projection ='3d')
        fig.add_subplot(ax)

      surf = ax.plot_surface(X, Y, Z, cmap=matplotlib.colormaps[cmap_name], linewidth=linewidth, **kwargs)

      ax.view_init(15, 80)
      ax.invert_xaxis()
      ax.invert_yaxis()

    if show_fig_legend:
      fig.legend()

    if save_as is not None:
      fig.savefig(save_as)
      
    return fig
  
