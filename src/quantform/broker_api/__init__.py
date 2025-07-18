"""@package quantform.broker_api
@author Kasper Rantamäki
Module containing wrappers for easier interaction with the brokers.

The module implements a BrokerAPI abstract base class and an InteractiveBrokersAPI class which wraps the
interactive brokers RESTful API. The API can be used for both accessing market data and executing trades.
"""


__all__ = ["BrokerAPI"]


from .BrokerAPI import BrokerAPI
