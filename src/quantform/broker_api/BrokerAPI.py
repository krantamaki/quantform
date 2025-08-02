"""@package quantform.broker_api.BrokerAPI
@author Kasper Rantamäki
Submodule contraining an abstract base class that standardizes the API interface used elsewhere in the platform
"""
from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd


class BrokerAPI(ABC):
  """Abstract base class providing a standardized interface that API classes must satisfy."""

  @abstractmethod
  def __init__(self, **kwargs) -> None:
    """Constructor method

    The constructor method should establish the API connection. It doesn't have any positional arguments, 
    but can take keyword arguments if needed for the connection. However, generally API keys and similar 
    should be included in the config file and used from there. 

    @param **kwargs       Possible additional arguments needed by the constructor as key-value pairs 
    @raises RuntimeError  Raised if the API connection fails to be formed 
    @return               None 
    """
    pass


  @abstractmethod
  def __del__(self) -> None:
    """Destructor method

    The destructor should be implemented so that the API connection is closed when the API object is 
    garbage collected.
    """
    pass


  @abstractmethod
  def bid(self, instrument_id: str, bid_price: float, bid_size: float, **kwargs) -> tuple[int, Optional[float], Optional[float]]:
    """Method for making buy (bid) requests

    The method makes a request to purchase the wanted amount of the specified instrument for the given price 
    through the API connection. If the request fails the method should return a tuple of form 
    (<return code>, None, None). If the request succeeds the method should return a tuple of form
    (<return code>, <bid price>, <bid size>), where the price and amount can differ from the parameters passed
    to the method depending on the broker and the passed keyword arguments.

    @param instrument_id  The identifier for the instrument to be purchased
    @param bid_price      The price at which the instrument should be purchased
    @param bid_size       The amount of the instrument to be purchased
    @param **kwargs       Possible additional arguments needed by the method as key-value pairs
    @return               Tuple of form (<return code>, <bid price>, <bid size>)
    """
    pass


  @abstractmethod
  def ask(self, instrument_id: str, ask_price: float, ask_size: float, **kwargs) -> tuple[int, Optional[float], Optional[float]]:
    """Method for making sale (ask) requests

    The method makes a request to sell the wanted amount of the specified instrument for the given price 
    through the API connection. If the request fails the method should return a tuple of form 
    (<return code>, None, None). If the request succeeds the method should return a tuple of form
    (<return code>, <ask price>, <ask size>), where the price and amount can differ from the parameters passed
    to the method depending on the broker and the passed keyword arguments.

    @param instrument_id  Identifier for the instrument to be sold
    @param ask_price      The price at which the instrument should be sold
    @param ask_size       The amount of the instrument to be sold
    @param **kwargs       Possible additional arguments needed by the method as key-value pairs
    @return               Tuple of form (<return code>, <ask price>, <ask size>)
    """
    pass


  @abstractmethod
  def snap(self, instrument_ids: list[str], **kwargs) -> tuple[int, Optional[pd.Dataframe]]:
    """Method for requesting a snapshot of the wanted instruments

    The methods makes a request to get the current bids and asks for the wanted instruments. 
    If the request is successful the method returns a tuple of form (<return code>, <dataframe>), 
    where the dataframe contrains columns ['Timestamp', 'InstrumentID', 'Bid', 'BidSize', 'Ask', 'AskSize']. 
    If the request for whatever reason fails the methods returns a tuple (<return code>, None). 

    @param instrument_ids  List of identifiers for the instruments for which the snap is wanted
    @param **kwargs        Possible additional arguments needed by the method as key-value pairs
    @return                Tuple of form (<return code>, <dataframe>)
    """
    pass


  @abstractmethod
  def history(self, instrument_id: str, start_time: str, end_time: str, step_size: str, **kwargs) -> tuple[int, Optional[pd.Dataframe]]:
    """Method for requesting historical market data for a given instrument

    The method request historical market data for the given instrument. If the request is successful 
    the method returns a tuple of form (<return code>, <dataframe>), where the columns in the dataframe 
    are ['Timestamp', 'Open Value', 'Close Value', 'High Value', 'Low Value', 'Volume']. If the request 
    fails the method returns a tuple (<return code>, None). 

    @param instrument_id  Identifier for the instrument for which historical data is requested
    @param start_time     The requested interval start time
    @param end_time       The requested interval end_time
    @param step_size      The step size specifying the granularity for the requested data
    @param **kwargs       Possible additional arguments needed by the method as key-value pairs
    @return               Tuple of form (<return code>, <dataframe>)
    """
    pass


  @abstractmethod
  def fields(self, instrument_ids: list[str], field_ids: list[str], 
             field_map: Optional[dict[str, str]] = None, **kwargs) -> tuple[int, Optional[pd.Dataframe]]:
    """Method for requesting arbitrary field values for the wanted instruments

    The method request wanted fields for the given instruments. The fields can be anything that the broker 
    provides, but common choices would probably be sensitivities, volatilities and yields. If the request 
    is successful the method returns a tuple of form (<return code>, <dataframe>), where the dataframe has 
    columns 'InstrumentID' and whatever the field ids are. Alternatively, a field map can be given to the 
    method, which is used to map the used field ids to their respective identifier that is used as  the name of 
    the column. If the request fails the method returns a tuple (<return code>, None).

    @param instrument_ids  List of identifiers for the instruments for which the field values are wanted 
    @param field_ids       List of identifiers specifying the wanted fields for the instruments 
    @param field_map       Dictionary for mapping the field ids into some other identifier. Optional 
    @param **kwargs        Possible additional arguments needed by the method as key-value pairs
    @return                Tuple of form (<return code>, <dataframe>)
    """
    pass

