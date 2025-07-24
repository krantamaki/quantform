"""@package quantform.ui.Site
@author Kasper Rantamäki
Class implementation for a Flask based website with multiple different pages
"""
from typing import List, Optional, Union
from flask import Flask, Blueprint
from dash import Dash


class Site:
  """The website object
  
  A simple class for initializing a Flask website
  """

  def __init__(self, pages: List[Union[Page, Dash]]) -> None:
    """Constructor method
    
    Constructor method that stores the passed parameters as instance variables 
    and initializes a Flask application with the given webpages
    
    @param pages          A list of page instances used in the 
    @raises RuntimeError  Raised if an invalid page instance is passed
    @return               None
    """

    self.__app   = Flask(__name__)
    self.__pages = pages

    for page in self.__pages:

      # If the page is an instance of Page abstract class then the function that is used in routing
      # is the call method of the object
      if issubclass(page, Page):
        self.__app.add_url_rule(page.route, view_func=page, methods=page.methods)

      # If the page is a Dash app then the app needs to be hosted by the main Flask website
      elif issubclass(page, DashApp):
        with self.__app.app_context():
          self.__app = page()

      # No other page types are not currently supported
      else:
        raise RuntimeError(f"Instance of invalid class {type(page).__name__}")


  def __call__(self) -> Flask:
    """Call method
    
    Call method that returns the initialized Flask object
    
    @return  The Flask class instance
    """
    return self.__app
