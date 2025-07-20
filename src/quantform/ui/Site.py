"""@package quantform.ui.Site
@author Kasper Rantamäki
Class implementation for a Flask based website with multiple different pages
"""
from typing import List, Optional, Union
from flask import Flask

from .Page import Page
from .DashApp import DashApp


class Site:
  """
  TODO
  """

  def __init__(self, pages: List[Union[Page, DashApp]]) -> None:
    """
    TODO
    """

    self.__app   = Flask(__name__)
    self.__pages = pages

    # Kind of a dangerous way of handling this, but makes the site very modular
    for page in self.__pages:

      # If the page is an instance of Page abstract class then the function that is used in routing
      # is just the call method of the object
      if issubclass(page, Page):
        exec(f"""
        self.__app.route({page.route}, methods={page.methods})
        def {page.name}():
          return {page()}
        """)

      # If the page is a Dash app then the app needs to be hosted by the main Flask website
      elif issubclass(page, DashApp):
        with self.__app.app_context():
          self.__app = page()

      # No other page types are not currently supported
      else:
        raise RuntimeError(f"Instance of invalid class {type(page).__name__}")


  def __call__(self) -> Flask:
    """
    TODO
    """
    return self.__app
