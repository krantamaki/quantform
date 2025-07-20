"""@package quantform.ui.DashApp
@author Kasper Rantamäki
Abstact class for a dash app that is used in conjunction with the Site class and Flask.
"""
from abc import ABC, abstractmethod
from flask import g
from dash import Dash


class DashApp(ABC):
  """
  TODO
  """

  def __init__(self, name:str, route: str) -> None:
    """
    TODO
    """
    self.__name   = name
    self.__route  = route
    self.__app    = Dash(server=g.cur_app, url_base_pathname=route)

  @abstractmethod
  def __call__(self) -> str:
    """
    TODO
    """
    pass


  @property
  def name(self) -> str:
    """
    TODO
    """
    return self.__name


  @property
  def route(self) -> str:
    """
    TODO
    """
    return self.__route


  @property
  def app(self) -> Dash:
    """
    TODO
    """
    return self.__app
