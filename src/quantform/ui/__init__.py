"""@package quantform.ui
@author Kasper Rantamäki
Module for creating a locally hosted webpage with Flask

The module is used to create a user interface for viewing the done trades
and open positions as well as some needed reports
"""


__all__ = ["Site", "Page", "DashApp", "trade_alert"]


from .DashApp import DashApp
from .Page import Page
from .Site import Site
from .trade_alert import trade_alert
