"""@package quantform.ui.Page
@author Kasper Rantamäki
Abstact class for a HTML webpage that is used in conjunction with the Site class and Flask.
"""
from abc import ABC, abstractmethod
from flask import render_template_string, render_template
from typing import List, Optional


class Page(ABC):
  """Abstact base class for a basic web page
  
  Abstact base class that provides a framework for defining basic Flask based web pages. 
  For introduction to Flask, see e.g. the tutorial https://flask.palletsprojects.com/en/stable/tutorial/.
  """

  def __init__(self, route: str, methods: List[str], 
               template: Optional[str], template_path: Optional[str],
               stylesheet: Optional[str], stylesheet_path: Optional[str]) -> None:
    """Constructor method
    
    Default constructor that stores the passed parameters as instance variables.
    
    @param route            The route to the page on the website
    @param methods          List of methods that the page implements
    @param template         HTML template string. Optional
    @param template_path    Path to the HTML template file. Optional
    @param stylesheet       The CSS stylesheet string. Optional
    @param stylesheet_path  Path to the CSS stylesheet file. Optional
    @return                 None
    """
    self.__route           = route
    self.__methods         = methods
    self.__template        = template
    self.__template_path   = template_path
    self.__stylesheet      = stylesheet
    self.__stylesheet_path = stylesheet_path


  @abstractmethod
  def __call__(self) -> any:
    """Call method
    
    The call method for the page. Handles the HTTP request.
    
    @raises RuntimeError  Raised if an improper request is passed
    @return               Anything
    """
    pass


  @property
  def route(self) -> str:
    """The route to the page on the website
    """
    return self.__route


  @property
  def methods(self) -> List[str]:
    """List of methods that the page implements
    """
    return self.__methods
