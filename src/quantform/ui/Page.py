"""@package quantform.ui.Page
@author Kasper Rantamäki
Abstact class for a HTML webpage that is used in conjunction with the Site class and Flask.
"""
from abc import ABC, abstractmethod
from flask import render_template_string, render_template
from typing import List, Optional

class Page(ABC):
  """
  TODO
  """

  def __init__(self, name: str, route: str, methods: List[str], template: Optional[str], template_path: Optional[str]) -> None:
    """
    TODO
    """
    self.__name            = name
    self.__route           = route
    self.__methods         = methods
    self.__template        = template
    self.__template_path   = template_path


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
  def methods(self) -> List[str]:
    """
    TODO
    """
    return self.__methods


  @property
  def render(self) -> any:
    """
    TODO
    """
    if self.__template is not None:
      return render_template_string(self.__template)
    
    elif self.__template_path is not None:
      return render_template(self.__template_path)
    
    else:
      raise RuntimeError("No template specified!")

