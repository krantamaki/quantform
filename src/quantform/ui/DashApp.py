"""@package quantform.ui.DashApp
@author Kasper Rantamäki
Abstact class for a dash app that is used in conjunction with the Site class and Flask.
"""
from abc import ABC, abstractmethod
from flask import g
from dash import Dash
from typing import List, Dictionary


class DashApp(ABC):
  """Abstract base class for Dash apps
  
  Abstract base class that provides a framework for defining Dash apps and hosting them
  on the Flask site. For introduction to Dash apps see e.g. https://ploomber.io/blog/dash-in-flask/ 
  and https://dash.plotly.com/minimal-app. 
  """

  def __init__(self, route: str, *args, **kwargs) -> None:
    """Constructor method
    
    Default constructor that stores the passed parameters as instance variables
    
    @param route          The route to the page on the website
    @param *args          Arguments that can be passed to the object and used in e.g. the call method
    @param **kwargs       Kwargs that can be passed to the object and used in e.g. the call method
    @raises RuntimeError  Raised if the Dash app initialization fails
    """
    self.__name   = name
    self.__route  = route
    self.__args   = args
    self.__kwargs = kwargs
    
    try:
      self.__app    = Dash(server=g.cur_app, url_base_pathname=route)
    except Exception as e:
      raise RuntimeError(f"Couldn't initialize the Dash app! (Cause: {e})")


  @abstractmethod
  def __call__(self) -> any:
    """Call method
    
    The call method that initializes the Dash app and returns it.
    
    @raises RuntimeError  Raised if the app cannot be created
    @return               The server for the Dash app
    """
    pass


  @property
  def route(self) -> str:
    """The route to the page on the website
    """
    return self.__route


  @property
  def args(self) -> List[any]:
    """Arguments that can be passed to the object and used in e.g. the call method
    """
    return self.__args


  @property
  def kwargs(self) -> Dictionary[any, any]:
    """Kwargs that can be passed to the object and used in e.g. the call method
    """
    return self.__kwargs


  @abstractmethod
  def __callback(self) -> any:
    """Callback method 
    
    Used to define the dynamic functionality for the Dash app
    
    @raises RuntimeError  Raised if the dynamic callback fails
    @return               Anything
    """
    pass
